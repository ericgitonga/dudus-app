"""
Local-only admin tool for dudus-app (issue #31, scoped in #15).

Adds a new card to src/data/card_index.json (with an optional photo) and lets an existing
card's photo be added, replaced, or removed. Never deployed — lives outside the Next.js build
(nothing under tools/ is imported by the app or referenced by next.config.ts), reachable only by
running it locally. It edits the working tree directly; committing/PR'ing the result goes
through the normal repo workflow (ONBOARDING.md), same as any other change.

Run from the repo root:
    conda run -n ds streamlit run tools/dudu-intake/app.py
"""

import json
import re
from pathlib import Path

import streamlit as st
from PIL import Image, ImageOps

REPO_ROOT = Path(__file__).resolve().parents[2]
CARD_INDEX_PATH = REPO_ROOT / "src" / "data" / "card_index.json"
PHOTOS_DIR = REPO_ROOT / "public" / "photos"

CARD_KEY_ORDER = [
    "id",
    "common_name",
    "scientific_name",
    "family",
    "order",
    "taxon_rank",
    "sourcing",
    "sections",
    "source_report_ref",
    "photo_ref",
    "reviewed_by",
    "reviewed_at",
]

TAXON_RANKS = ["species", "genus", "family", "order"]
SOURCING_OPTIONS = ["/dudus", "/dudusonline"]

TARGET_RATIO = 3 / 2
RATIO_TOLERANCE = 0.02


def load_cards():
    with open(CARD_INDEX_PATH) as f:
        return json.load(f)


def save_cards(cards):
    with open(CARD_INDEX_PATH, "w") as f:
        f.write(json.dumps(cards, indent=2, ensure_ascii=False) + "\n")


def slugify(text):
    slug = re.sub(r"[^a-z0-9]+", "-", text.strip().lower())
    return slug.strip("-")


def split_refs(raw):
    """A single path, or comma-separated paths -> str | list[str], matching source_report_ref's shape."""
    parts = [p.strip() for p in raw.split(",") if p.strip()]
    if len(parts) <= 1:
        return parts[0] if parts else ""
    return parts


def order_card(card):
    return {k: card.get(k) for k in CARD_KEY_ORDER}


def process_photo(uploaded_file):
    """
    Strip EXIF/GPS metadata and bake in orientation, mirroring stripPhotoMetadata.ts (#10) so
    admin-uploaded photos get the same treatment as in-app captures. Then apply the pad-to-3:2
    convention from SKILL.md: only pads (never crops) since "crop tight to the dudu" is a manual
    judgment call the tool can't make. Returns (image, warning | None).
    """
    img = Image.open(uploaded_file)
    img = ImageOps.exif_transpose(img)
    img = img.convert("RGB")

    w, h = img.size
    ratio = w / h
    warning = None

    if ratio < TARGET_RATIO - RATIO_TOLERANCE:
        target_w = round(h * TARGET_RATIO)
        padded = Image.new("RGB", (target_w, h), "white")
        padded.paste(img, ((target_w - w) // 2, 0))
        img = padded
    elif ratio > TARGET_RATIO + RATIO_TOLERANCE:
        warning = (
            f"This photo is wider than 3:2 ({w}x{h}). The tool only pads narrow photos — "
            "it won't crop into the subject automatically. Crop it tighter yourself first "
            "(see SKILL.md's photo convention), or upload as-is and expect some edge crop "
            "on the site's 3:2/4:3 views."
        )

    return img, warning


def save_photo(img, card_id, ext):
    PHOTOS_DIR.mkdir(parents=True, exist_ok=True)
    filename = f"{card_id}.{ext}"
    fmt = "PNG" if ext == "png" else "JPEG"
    img.save(PHOTOS_DIR / filename, fmt)
    return f"/photos/{filename}"


def delete_photo(photo_ref):
    if not photo_ref:
        return
    path = REPO_ROOT / "public" / photo_ref.lstrip("/")
    if path.exists():
        path.unlink()


st.set_page_config(page_title="dudus-app intake", layout="wide")
st.title("dudus-app admin intake")
st.caption(
    "Local-only authoring tool — for entering already-researched content (via /dudus or "
    "/dudusonline), not for researching a species itself."
)

tab_new, tab_existing = st.tabs(["Add new card", "Existing cards"])

with tab_new:
    if "sections" not in st.session_state:
        st.session_state.sections = [{"uid": 0, "heading": "", "body": ""}]
        st.session_state.section_uid_counter = 1

    if "new_card_message" in st.session_state:
        st.success(st.session_state.pop("new_card_message"))

    st.session_state.setdefault("photo_uploader_version", 0)

    st.subheader("Card details")
    col1, col2 = st.columns(2)
    with col1:
        common_name = st.text_input("Common name", key="new_common_name")
        card_id = st.text_input(
            "ID (slug)",
            help="Used as the URL segment and photo filename.",
            key="new_card_id",
        )
        if common_name:
            # Streamlit only honours a text_input's `value=` on the render where its keyed
            # session_state doesn't exist yet, so a live-updating suggestion can't use `value=`
            # once the widget has rendered once — shown as a copyable caption instead.
            st.caption(f"Suggested ID: `{slugify(common_name)}`")
        scientific_name = st.text_input("Scientific name (optional)", key="new_scientific_name")
        sourcing = st.selectbox("Sourced via", SOURCING_OPTIONS, key="new_sourcing")
    with col2:
        family = st.text_input("Family (optional)", key="new_family")
        order = st.text_input("Order (optional)", key="new_order")
        taxon_rank = st.selectbox("Taxon rank", TAXON_RANKS, key="new_taxon_rank")

    st.subheader("Source report references")
    col3, col4 = st.columns(2)
    with col3:
        technical_ref = st.text_input(
            "Technical report path(s)",
            help="Comma-separate if more than one, e.g. multiple research passes.",
            key="new_technical_ref",
        )
    with col4:
        lay_ref = st.text_input(
            "Lay report path(s)", help="Comma-separate if more than one.", key="new_lay_ref"
        )

    st.subheader("Sections")
    for section in st.session_state.sections:
        # Keyed by each section's own stable uid, not its list position — keying by index would
        # leave a later row's widget showing an earlier row's stale text once a row before it is
        # removed, since Streamlit's session_state (not the fresh `value=`) wins once a key exists.
        uid = section["uid"]
        with st.container(border=True):
            hcol, xcol = st.columns([6, 1])
            section["heading"] = hcol.text_input(
                "Heading", value=section["heading"], key=f"section_heading_{uid}"
            )
            if xcol.button("Remove", key=f"remove_section_{uid}") and len(st.session_state.sections) > 1:
                st.session_state.sections = [
                    s for s in st.session_state.sections if s["uid"] != uid
                ]
                st.rerun()
            section["body"] = st.text_area(
                "Body", value=section["body"], key=f"section_body_{uid}", height=120
            )

    if st.button("+ Add section"):
        st.session_state.sections.append(
            {"uid": st.session_state.section_uid_counter, "heading": "", "body": ""}
        )
        st.session_state.section_uid_counter += 1
        st.rerun()

    st.subheader("Photo (optional)")
    uploaded_photo = st.file_uploader(
        "Upload a pre-cropped photo",
        type=["jpg", "jpeg", "png"],
        key=f"new_photo_{st.session_state.photo_uploader_version}",
    )
    preview_img, photo_warning = (None, None)
    if uploaded_photo is not None:
        preview_img, photo_warning = process_photo(uploaded_photo)
        st.image(preview_img, caption="After metadata strip + 3:2 pad", width=400)
        if photo_warning:
            st.warning(photo_warning)

    st.divider()
    if st.button("Create card", type="primary"):
        cards = load_cards()
        errors = []
        if not card_id:
            errors.append("ID is required.")
        elif any(c["id"] == card_id for c in cards):
            errors.append(f"A card with id '{card_id}' already exists.")
        if not common_name:
            errors.append("Common name is required.")
        if not any(s["heading"].strip() and s["body"].strip() for s in st.session_state.sections):
            errors.append("At least one section (heading + body) is required.")

        if errors:
            for e in errors:
                st.error(e)
        else:
            photo_ref = None
            if uploaded_photo is not None:
                ext = "png" if uploaded_photo.type == "image/png" else "jpg"
                photo_ref = save_photo(preview_img, card_id, ext)

            new_card = order_card(
                {
                    "id": card_id,
                    "common_name": common_name,
                    "scientific_name": scientific_name or None,
                    "family": family or None,
                    "order": order or None,
                    "taxon_rank": taxon_rank,
                    "sourcing": sourcing,
                    "sections": [
                        {"heading": s["heading"], "body": s["body"]}
                        for s in st.session_state.sections
                        if s["heading"].strip() and s["body"].strip()
                    ],
                    "source_report_ref": {
                        "technical": split_refs(technical_ref),
                        "lay": split_refs(lay_ref),
                    },
                    "photo_ref": photo_ref,
                    "reviewed_by": None,
                    "reviewed_at": None,
                }
            )
            cards.append(new_card)
            save_cards(cards)
            # Fresh uid on reset (not uid 0 again) so the new blank row doesn't inherit a
            # just-submitted row's stale widget state under the same key.
            fresh_uid = st.session_state.section_uid_counter
            st.session_state.section_uid_counter += 1
            st.session_state.sections = [{"uid": fresh_uid, "heading": "", "body": ""}]
            for key in [
                "new_common_name", "new_card_id", "new_scientific_name", "new_family",
                "new_order", "new_sourcing", "new_taxon_rank", "new_technical_ref", "new_lay_ref",
            ]:
                st.session_state.pop(key, None)
            st.session_state.photo_uploader_version += 1
            # st.rerun() below aborts this script run immediately, so a message shown here would
            # never actually reach the browser — stash it and show it after the rerun instead.
            st.session_state.new_card_message = f"Added '{common_name}' ({card_id}) to card_index.json."
            st.rerun()

with tab_existing:
    if "existing_card_message" in st.session_state:
        st.success(st.session_state.pop("existing_card_message"))

    cards = load_cards()
    if not cards:
        st.info("No cards yet.")
    for card in cards:
        with st.expander(f"{card['common_name']} ({card['id']})"):
            left, right = st.columns([1, 2])
            with left:
                if card["photo_ref"]:
                    photo_path = REPO_ROOT / "public" / card["photo_ref"].lstrip("/")
                    if photo_path.exists():
                        st.image(str(photo_path), width=250)
                    else:
                        st.warning(f"photo_ref set but file missing: {card['photo_ref']}")
                else:
                    st.write("No photo yet.")

            with right:
                replacement = st.file_uploader(
                    "Add / replace photo",
                    type=["jpg", "jpeg", "png"],
                    key=f"upload_{card['id']}",
                )
                if replacement is not None:
                    new_img, warn = process_photo(replacement)
                    st.image(new_img, caption="After metadata strip + 3:2 pad", width=300)
                    if warn:
                        st.warning(warn)
                    if st.button("Save photo", key=f"save_{card['id']}"):
                        delete_photo(card["photo_ref"])
                        ext = "png" if replacement.type == "image/png" else "jpg"
                        card["photo_ref"] = save_photo(new_img, card["id"], ext)
                        save_cards(cards)
                        st.session_state.existing_card_message = f"Photo saved for {card['common_name']}."
                        st.rerun()

                if card["photo_ref"]:
                    confirm = st.checkbox("Confirm removal", key=f"confirm_{card['id']}")
                    if st.button(
                        "Remove photo", key=f"remove_{card['id']}", disabled=not confirm
                    ):
                        delete_photo(card["photo_ref"])
                        card["photo_ref"] = None
                        save_cards(cards)
                        st.session_state.existing_card_message = f"Photo removed for {card['common_name']}."
                        st.rerun()
