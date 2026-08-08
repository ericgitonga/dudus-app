"""Golden path for the card browser (issue #4): full list renders, search filters correctly.

Nothing here hardcodes a total count or a specific species — the card set changes over time
(species get added or withdrawn, as in issue #14), so every expectation is derived from CARDS
(the actual bundled data, loaded in _common.py) at test time.

Locators are scoped to specific data-testid elements, never page.text_content("body") — the
body's textContent includes Next.js's inline RSC hydration payload (a <script> tag serializing
the full card list for the client), which contains every species name regardless of what's
actually rendered/filtered on screen. An unscoped body-text assertion here would always find
every species, whether or not it's actually shown.
"""

from _common import CARDS, browser_page

TOTAL = len(CARDS)


def test_full_list_renders():
    with browser_page() as page:
        page.goto("/")
        page.wait_for_selector("text=Dudus")
        assert f"{TOTAL} of {TOTAL} species" in page.text_content(
            '[data-testid="result-count"]'
        )
        list_text = page.text_content('[data-testid="card-list"]')
        # Every card in the index should appear in the rendered list exactly once.
        for card in CARDS:
            assert list_text.count(card["common_name"]) == 1, card["common_name"]


def test_search_filters_to_matching_subset():
    # Use the first word of some card's name as the query, and compute which cards should
    # match from the actual data — never assume a fixed expected count.
    query = CARDS[0]["common_name"].split()[0]
    expected = [c for c in CARDS if query.lower() in c["common_name"].lower()]
    not_expected = [c for c in CARDS if c not in expected]

    with browser_page() as page:
        page.goto("/")
        page.fill('input[aria-label="Search species by common name"]', query)
        page.wait_for_selector(f"text={len(expected)} of {TOTAL} species")
        list_text = page.text_content('[data-testid="card-list"]')
        for card in expected:
            assert card["common_name"] in list_text
        for card in not_expected:
            assert card["common_name"] not in list_text


def test_search_no_match_shows_empty_state():
    with browser_page() as page:
        page.goto("/")
        page.fill(
            'input[aria-label="Search species by common name"]', "zzzznomatchxyz"
        )
        page.wait_for_selector('[data-testid="no-results"]')
        assert "No species match" in page.text_content('[data-testid="no-results"]')


TESTS = [
    test_full_list_renders,
    test_search_filters_to_matching_subset,
    test_search_no_match_shows_empty_state,
]

if __name__ == "__main__":
    for t in TESTS:
        t()
        print(f"PASS {t.__name__}")
