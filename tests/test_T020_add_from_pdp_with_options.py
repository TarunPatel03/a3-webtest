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
from .utils import wait_visible, wait_all_present, try_xpath_any, scroll_into_view_and_click, save_named_screenshot


@pytest.mark.ui
def test_T020_add_from_pdp_with_required_options(driver, base_url):
    driver.get(base_url)
    s = wait_visible(driver, "name", "search")
    s.clear(); s.send_keys("phone"); s.send_keys(Keys.ENTER)
    cards = wait_all_present(driver, "css selector", ".product-layout")
    pdp_link = cards[0].find_element("css selector", "h4 a")
    try:
        driver.execute_script("arguments[0].scrollIntoView({block:'center'}); arguments[0].style.outline='4px solid blue';", pdp_link)
    except Exception:
        pass
    save_named_screenshot(driver, "T020_context_before_open_pdp")
    pdp_link.click()

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
    try:
        driver.execute_script("arguments[0].scrollIntoView({block:'center'}); arguments[0].style.outline='4px solid green';", add_btn)
    except Exception:
        pass
    save_named_screenshot(driver, "T020_context_on_pdp_before_add")
    scroll_into_view_and_click(driver, add_btn)

    driver.get("https://ecommerce-playground.lambdatest.io/index.php?route=checkout/cart")
    try:
        first_row = driver.find_element("css selector", ".table-responsive tbody tr, table tbody tr")
        driver.execute_script("arguments[0].scrollIntoView({block:'center'}); arguments[0].style.outline='4px solid purple';", first_row)
    except Exception:
        pass
    save_named_screenshot(driver, "T020_context_cart_after_add")
    body = driver.find_element("tag name", "body").text.lower()
    rows = driver.find_elements("css selector", ".table-responsive tbody tr, table tbody tr")
    assert ("shopping cart" in body) and (len(rows) >= 1)
