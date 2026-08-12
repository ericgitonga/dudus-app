"""Unit tests for the pure helper functions in app.py.

Fast, no Streamlit widget/network round-trip involved — complements (not replaces) the
`streamlit.testing.v1.AppTest`/real end-to-end publish verification this tool has relied on so
far (#31/#34/#40). Run: pytest (from tools/dudu-intake/, or via CI's unit-dudu-intake job).
"""

import fitz
import pytest

from app import (
    find_technical_pdf_path,
    find_technical_ref,
    guess_order_from_technical,
    parse_lay_report,
    resolve_order_default_index,
    serialize_cards,
    slugify,
)


def _pdf_bytes(spans):
    """Build a minimal in-memory PDF: `spans` is a list of (text, size, bold) lines, each
    rendered on its own line, in the same top-to-bottom reading order parse_lay_report expects."""
    doc = fitz.open()
    page = doc.new_page()
    y = 72
    for text, size, bold in spans:
        page.insert_text((72, y), text, fontsize=size, fontname="hebo" if bold else "helv")
        y += size + 6
    return doc.tobytes()


def _lay_report_pdf(title, sections, title_lines=None):
    """sections: list of (heading, body) tuples. `title_lines`, if given, overrides `title` with
    several consecutive title-sized spans — simulating a wrapped H1 that renders across more
    than one visual line."""
    spans = [(line, 20, True) for line in (title_lines or [title])]
    for heading, body in sections:
        spans.append((heading, 15, True))
        spans.append((body, 11, False))
    return _pdf_bytes(spans)


def _technical_pdf(text):
    doc = fitz.open()
    page = doc.new_page()
    page.insert_text((72, 72), text, fontsize=11, fontname="helv")
    return doc.tobytes()


# ── slugify ──────────────────────────────────────────────────────────────────

@pytest.mark.parametrize(
    "text,expected",
    [
        ("White-Ringed Atlas Moth", "white-ringed-atlas-moth"),
        ("  Tropical Bont Tick  ", "tropical-bont-tick"),
        ("Aedes Mosquitoes!", "aedes-mosquitoes"),
        ("Multiple   Spaces", "multiple-spaces"),
        ("Already-Hyphenated", "already-hyphenated"),
    ],
)
def test_slugify(text, expected):
    assert slugify(text) == expected


# ── serialize_cards ──────────────────────────────────────────────────────────

def test_serialize_cards_round_trips_and_is_newline_terminated():
    import json

    cards = [{"id": "aedes-mosquitoes", "common_name": "Aedes Mosquitoes"}]
    raw = serialize_cards(cards)
    assert raw.endswith(b"\n")
    assert json.loads(raw) == cards


def test_serialize_cards_pretty_prints():
    cards = [{"id": "a", "common_name": "A"}]
    raw = serialize_cards(cards)
    assert b"\n  " in raw  # indent=2, not compact


# ── parse_lay_report ─────────────────────────────────────────────────────────

def test_parse_lay_report_extracts_title_and_sections():
    pdf = _lay_report_pdf(
        "White-Ringed Atlas Moth",
        [
            ("What Is It?", "A large moth with white rings on its wings."),
            ("Where Does It Live?", "Forests across East Africa."),
        ],
    )
    title, sections, err = parse_lay_report(pdf)
    assert err is None
    assert title == "White-Ringed Atlas Moth"
    assert sections == [
        {"heading": "What Is It?", "body": "A large moth with white rings on its wings."},
        {"heading": "Where Does It Live?", "body": "Forests across East Africa."},
    ]


@pytest.mark.parametrize(
    "raw_title,expected_title",
    [
        ("The White-Ringed Atlas Moth", "White-Ringed Atlas Moth"),
        ("A Tropical Bont Tick", "Tropical Bont Tick"),
        ("An Aedes Mosquito", "Aedes Mosquito"),
    ],
)
def test_parse_lay_report_strips_leading_article_from_title(raw_title, expected_title):
    pdf = _lay_report_pdf(raw_title, [("What Is It?", "Body text.")])
    title, _sections, err = parse_lay_report(pdf)
    assert err is None
    assert title == expected_title


def test_parse_lay_report_joins_a_title_wrapped_across_lines():
    pdf = _lay_report_pdf(
        None,
        [("What Are They?", "Body text.")],
        title_lines=["The Paper Wasp - An Insect That Builds Its", "Nursery Out of Chewed Wood"],
    )
    title, sections, err = parse_lay_report(pdf)
    assert err is None
    assert title == "Paper Wasp - An Insect That Builds Its Nursery Out of Chewed Wood"
    assert sections == [{"heading": "What Are They?", "body": "Body text."}]


def test_parse_lay_report_errors_when_no_title_found():
    # No bold text at all, so no candidate title.
    pdf = _pdf_bytes([("Just some regular text.", 11, False)])
    title, sections, err = parse_lay_report(pdf)
    assert title is None
    assert sections == []
    assert err is not None


def test_parse_lay_report_errors_when_no_sections_found():
    # A title-sized bold heading, but nothing bold after it.
    pdf = _pdf_bytes([("Title Only", 20, True), ("No headings follow.", 11, False)])
    title, sections, err = parse_lay_report(pdf)
    assert title == "Title Only"
    assert sections == []
    assert err is not None


# ── guess_order_from_technical ────────────────────────────────────────────────

def test_guess_order_from_technical_returns_most_common_match(tmp_path):
    path = tmp_path / "technical.pdf"
    path.write_bytes(
        _technical_pdf(
            "This species belongs to Order Araneae. Other members of Order Araneae share traits."
        )
    )
    assert guess_order_from_technical(path) == "Araneae"


def test_guess_order_from_technical_returns_none_when_no_match(tmp_path):
    path = tmp_path / "technical.pdf"
    path.write_bytes(_technical_pdf("No taxonomic order stated here at all."))
    assert guess_order_from_technical(path) is None


def test_guess_order_from_technical_returns_none_for_missing_path():
    assert guess_order_from_technical(None) is None


# ── find_technical_pdf_path / find_technical_ref ──────────────────────────────

def test_find_technical_pdf_path_finds_sibling_file(monkeypatch, tmp_path):
    import app

    monkeypatch.setattr(app, "DUDUS_ROOT", tmp_path)
    species_dir = tmp_path / "White-Ringed Atlas Moth"
    species_dir.mkdir()
    (species_dir / "atlas-moth-web.pdf").write_bytes(b"%PDF-fake")

    result = find_technical_pdf_path("White-Ringed Atlas Moth", "atlas-moth-web-la.pdf")
    assert result == species_dir / "atlas-moth-web.pdf"


def test_find_technical_pdf_path_returns_none_when_file_missing(monkeypatch, tmp_path):
    import app

    monkeypatch.setattr(app, "DUDUS_ROOT", tmp_path)
    result = find_technical_pdf_path("Nonexistent Species", "report-la.pdf")
    assert result is None


def test_find_technical_pdf_path_returns_none_for_non_lay_filename():
    # Filename doesn't end in "-la.pdf", so there's no technical sibling to derive.
    assert find_technical_pdf_path("Some Species", "report.pdf") is None


def test_find_technical_ref_empty_string_when_no_match(monkeypatch, tmp_path):
    import app

    monkeypatch.setattr(app, "DUDUS_ROOT", tmp_path)
    assert find_technical_ref("Nonexistent Species", "report-la.pdf") == ""


def test_find_technical_ref_returns_relative_path_string(monkeypatch, tmp_path):
    import app

    monkeypatch.setattr(app, "DUDUS_ROOT", tmp_path)
    species_dir = tmp_path / "Tropical Bont Tick"
    species_dir.mkdir()
    (species_dir / "tbt-web.pdf").write_bytes(b"%PDF-fake")

    assert find_technical_ref("Tropical Bont Tick", "tbt-web-la.pdf") == "Tropical Bont Tick/tbt-web.pdf"


# ── resolve_order_default_index ───────────────────────────────────────────────

def test_resolve_order_default_index_for_known_order():
    known = ["Araneae", "Coleoptera"]
    assert resolve_order_default_index(known, "Coleoptera") == 1


def test_resolve_order_default_index_for_detected_but_new_order():
    known = ["Araneae", "Coleoptera"]
    # "Other (type manually)" sits right after "Unknown", i.e. len(known) + 1.
    assert resolve_order_default_index(known, "Phasmatodea") == len(known) + 1


def test_resolve_order_default_index_for_no_detected_order():
    known = ["Araneae", "Coleoptera"]
    # "Unknown (fix later)" sits right after the known orders, i.e. len(known).
    assert resolve_order_default_index(known, None) == len(known)
