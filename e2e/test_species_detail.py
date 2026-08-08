"""Golden path for the card detail view (issue #5): taxonomy + sections render, 404s cleanly,
navigation from the browser list works.

Locators scoped to the [data-testid="species-detail"] container, never bare body text — see
_common.py's docstring on why an unscoped body-text assertion is unreliable on this app.
"""

from _common import browser_page


def test_detail_page_renders_taxonomy_and_sections():
    with browser_page() as page:
        page.goto("/species/wolf-spiders")
        detail = page.locator('[data-testid="species-detail"]')
        text = detail.text_content()
        assert "Wolf Spiders" in text
        assert "Lycosidae" in text
        assert "Araneae" in text
        # A section heading and a fact from its body, to confirm sections actually render.
        assert "The Dancing Mama" in text
        assert "40,000 spider species" in text


def test_detail_page_handles_species_with_no_scientific_name():
    with browser_page() as page:
        page.goto("/species/wolf-spiders")
        detail = page.locator('[data-testid="species-detail"]')
        # Wolf Spiders has no confirmed scientific_name (taxon_rank: family) — the page must not
        # render a stray "null" or empty italic line.
        assert "null" not in detail.text_content().lower()


def test_unknown_species_id_404s():
    with browser_page() as page:
        resp = page.goto("/species/not-a-real-species")
        assert resp.status == 404


def test_browser_links_navigate_to_detail_page():
    with browser_page() as page:
        page.goto("/")
        page.fill('input[aria-label="Search species by common name"]', "wolf")
        page.wait_for_selector("text=1 of 31 species")
        page.click('[data-testid="card-list"] a')
        page.wait_for_selector('[data-testid="species-detail"]')
        assert "/species/wolf-spiders" in page.url
        assert "Wolf Spiders" in page.locator('[data-testid="species-detail"]').text_content()


TESTS = [
    test_detail_page_renders_taxonomy_and_sections,
    test_detail_page_handles_species_with_no_scientific_name,
    test_unknown_species_id_404s,
    test_browser_links_navigate_to_detail_page,
]

if __name__ == "__main__":
    for t in TESTS:
        t()
        print(f"PASS {t.__name__}")
