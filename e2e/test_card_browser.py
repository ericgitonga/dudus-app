"""Golden path for the card browser (issue #4): full list renders, search filters correctly.

Locators are scoped to specific data-testid elements, never page.text_content("body") — the
body's textContent includes Next.js's inline RSC hydration payload (a <script> tag serializing
the full card list for the client), which contains every species name regardless of what's
actually rendered/filtered on screen. An unscoped body-text assertion here would always find
every species, whether or not it's actually shown.
"""

from _common import browser_page


def test_full_list_renders():
    with browser_page() as page:
        page.goto("/")
        page.wait_for_selector("text=Dudus")
        assert "31 of 31 species" in page.text_content('[data-testid="result-count"]')
        assert page.text_content('[data-testid="card-list"]').count("Wolf Spiders") == 1


def test_search_filters_to_one_result():
    with browser_page() as page:
        page.goto("/")
        page.fill('input[aria-label="Search species by common name"]', "wolf")
        page.wait_for_selector("text=1 of 31 species")
        list_text = page.text_content('[data-testid="card-list"]')
        assert "Wolf Spiders" in list_text
        assert "Picasso Bug" not in list_text


def test_search_no_match_shows_empty_state():
    with browser_page() as page:
        page.goto("/")
        page.fill('input[aria-label="Search species by common name"]', "zzzznomatch")
        page.wait_for_selector('[data-testid="no-results"]')
        assert "No species match" in page.text_content('[data-testid="no-results"]')


TESTS = [
    test_full_list_renders,
    test_search_filters_to_one_result,
    test_search_no_match_shows_empty_state,
]

if __name__ == "__main__":
    for t in TESTS:
        t()
        print(f"PASS {t.__name__}")
