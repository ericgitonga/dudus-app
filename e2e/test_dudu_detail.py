"""Golden path for the dudu detail view (issue #5): taxonomy + sections render, 404s cleanly,
navigation from the browser list works.

Nothing here hardcodes a specific dudu — picks whatever qualifies out of CARDS (the actual
bundled data) at test time, so the suite survives dudus being added or withdrawn (issue #14).

Locators scoped to the [data-testid="dudu-detail"] container, never bare body text — see
_common.py's docstring on why an unscoped body-text assertion is unreliable on this app.
"""

from _common import CARDS, browser_page


def test_detail_page_renders_taxonomy_and_sections():
    card = next(c for c in CARDS if c["family"] and c["order"] and c["sections"])
    with browser_page() as page:
        page.goto(f"/dudus/{card['id']}")
        text = page.locator('[data-testid="dudu-detail"]').text_content()
        assert card["common_name"] in text
        assert card["family"] in text
        assert card["order"] in text
        first_section = card["sections"][0]
        assert first_section["heading"] in text
        assert first_section["body"][:50] in text


def test_detail_page_handles_missing_scientific_name():
    card = next(c for c in CARDS if c["scientific_name"] is None)
    with browser_page() as page:
        page.goto(f"/dudus/{card['id']}")
        text = page.locator('[data-testid="dudu-detail"]').text_content()
        assert "null" not in text.lower()


def test_unknown_dudu_id_404s():
    with browser_page() as page:
        resp = page.goto("/dudus/not-a-real-dudu-id")
        assert resp.status == 404


def test_browser_link_navigates_to_its_own_detail_page():
    with browser_page() as page:
        page.goto("/")
        page.wait_for_selector('[data-testid="card-list"]')
        page.click('[data-testid="card-list"] a >> nth=0')
        page.wait_for_selector('[data-testid="dudu-detail"]')
        landed_id = page.url.rstrip("/").split("/dudus/")[-1]
        card = next(c for c in CARDS if c["id"] == landed_id)
        assert card["common_name"] in page.locator(
            '[data-testid="dudu-detail"]'
        ).text_content()


TESTS = [
    test_detail_page_renders_taxonomy_and_sections,
    test_detail_page_handles_missing_scientific_name,
    test_unknown_dudu_id_404s,
    test_browser_link_navigates_to_its_own_detail_page,
]

if __name__ == "__main__":
    for t in TESTS:
        t()
        print(f"PASS {t.__name__}")
