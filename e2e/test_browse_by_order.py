"""Golden path for the home page's browse-by-order grid: dudus grouped by order, grid cards
linking to their detail page. Every assertion is derived from the actual bundled card index at
test time — orders and counts are never hardcoded (see _common.py).
"""

from _common import CARDS, browser_page

UNCLASSIFIED_LABEL = "Order not yet identified"


def _orders_present():
    return {c["order"] if c["order"] else UNCLASSIFIED_LABEL for c in CARDS}


def test_only_orders_present_in_data_are_listed():
    with browser_page() as page:
        page.goto("/")
        page.wait_for_selector('[data-testid="order-group"]')
        rendered = set(
            page.locator('[data-testid="order-group"]').evaluate_all(
                "els => els.map(e => e.getAttribute('data-order'))"
            )
        )
        assert rendered == _orders_present()


def test_order_group_contains_exactly_its_own_dudus():
    order = next(c["order"] for c in CARDS if c["order"])
    expected = {c["id"] for c in CARDS if c["order"] == order}
    not_expected = {c["id"] for c in CARDS if c["order"] != order}
    with browser_page() as page:
        page.goto("/")
        group = page.locator(f'[data-testid="order-group"][data-order="{order}"]')
        group.wait_for()
        ids = set(
            group.locator('[data-testid="grid-card"]').evaluate_all(
                "els => els.map(e => e.getAttribute('data-dudu-id'))"
            )
        )
        assert ids == expected
        assert not (ids & not_expected)


def test_unclassified_cards_grouped_under_fallback():
    unclassified = {c["id"] for c in CARDS if not c["order"]}
    if not unclassified:
        print("SKIP test_unclassified_cards_grouped_under_fallback: every card has an order")
        return
    with browser_page() as page:
        page.goto("/")
        group = page.locator(f'[data-testid="order-group"][data-order="{UNCLASSIFIED_LABEL}"]')
        group.wait_for()
        ids = set(
            group.locator('[data-testid="grid-card"]').evaluate_all(
                "els => els.map(e => e.getAttribute('data-dudu-id'))"
            )
        )
        assert ids == unclassified


def test_grid_card_links_to_its_detail_page():
    card = CARDS[0]
    with browser_page() as page:
        page.goto("/")
        page.click(f'[data-testid="grid-card"][data-dudu-id="{card["id"]}"]')
        page.wait_for_selector('[data-testid="dudu-detail"]')
        assert page.url.rstrip("/").endswith(f"/dudus/{card['id']}")


TESTS = [
    test_only_orders_present_in_data_are_listed,
    test_order_group_contains_exactly_its_own_dudus,
    test_unclassified_cards_grouped_under_fallback,
    test_grid_card_links_to_its_detail_page,
]

if __name__ == "__main__":
    for t in TESTS:
        t()
        print(f"PASS {t.__name__}")
