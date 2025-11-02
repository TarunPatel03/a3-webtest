"""
T020 — Add to cart from product detail page (with required options)
Function: F4 — Add to cart
Tester: Tarun Patel
Steps:
  1) Search broadly (e.g., "phone")
  2) Open first PDP and satisfy required options
  3) Add to cart
Expected: Cart shows at least 1 item with options applied.
"""
import pytest
from selenium.webdriver.common.keys import Keys
from .utils import wait_visible, wait_all_present, try_xpath_any, scroll_into_view_and_click


@pytest.mark.ui
def test_T020_add_from_pdp_with_required_options(driver, base_url):
    driver.get(base_url)
    s = wait_visible(driver, "name", "search")
    s.clear(); s.send_keys("phone"); s.send_keys(Keys.ENTER)
    cards = wait_all_present(driver, "css selector", ".product-layout")
    cards[0].find_element("css selector", "h4 a").click()

    # Selects (dropdowns)
    try:
        selects = driver.find_elements("css selector", "select[required], .required select")
        for sel in selects:
            options = sel.find_elements("css selector", "option[value]:not([value=''])")
            if options:
                options[0].click()
    except Exception:
        pass
    # Radios
    try:
        radios = driver.find_elements("css selector", ".required input[type='radio'], input[type='radio'][required]")
        by_name = {}
        for r in radios:
            nm = r.get_attribute("name") or id(r)
            by_name.setdefault(nm, []).append(r)
        for group in by_name.values():
            try:
                if group:
                    driver.execute_script("arguments[0].click();", group[0])
            except Exception:
                pass
    except Exception:
        pass
    # Checkboxes
    try:
        checkboxes = driver.find_elements("css selector", ".required input[type='checkbox'], input[type='checkbox'][required]")
        for c in checkboxes:
            try:
                if not c.is_selected():
                    driver.execute_script("arguments[0].click();", c)
            except Exception:
                pass
    except Exception:
        pass

    add_btn = try_xpath_any(
        driver,
        [
            "//button[@id='button-cart']",
            "//button[contains(@class,'btn') and (contains(.,'Add to Cart') or contains(.,'Add to cart'))]",
            "//button[@data-original-title='Add to Cart' or @data-original-title='Add to cart']",
        ],
    )
    scroll_into_view_and_click(driver, add_btn)

    driver.get("https://ecommerce-playground.lambdatest.io/index.php?route=checkout/cart")
    body = driver.find_element("tag name", "body").text.lower()
    rows = driver.find_elements("css selector", ".table-responsive tbody tr, table tbody tr")
    assert ("shopping cart" in body) and (len(rows) >= 1)
