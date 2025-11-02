
import pytest
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from .utils import wait_visible, wait_all_present, try_xpath_any, scroll_into_view_and_click


@pytest.mark.ui
def test_T019_add_multiple_items_to_cart(driver, base_url):
    driver.get(base_url)
    s = wait_visible(driver, "name", "search")
    s.clear(); s.send_keys("phone"); s.send_keys(Keys.ENTER)
    try:
        cards = wait_all_present(driver, "css selector", ".product-layout")
    except TimeoutException:
        s = wait_visible(driver, "name", "search")
        s.clear(); s.send_keys("iphone"); s.send_keys(Keys.ENTER)
        cards = wait_all_present(driver, "css selector", ".product-layout")
    for idx in range(min(2, len(cards))):
        add_btn = try_xpath_any(
            driver,
            [
                f"(//div[contains(@class,'product-layout')])[{idx+1}]//button[contains(@title,'Add to Cart') or contains(@data-original-title,'Add to Cart') or contains(.,'Add to Cart') or contains(.,'Add to cart')]",
            ],
        )
        scroll_into_view_and_click(driver, add_btn)
    driver.get("https://ecommerce-playground.lambdatest.io/index.php?route=checkout/cart")
    rows = driver.find_elements("css selector", ".table-responsive tbody tr, table tbody tr")
    qty_inputs = driver.find_elements("css selector", "input[name*='quantity']")
    total_qty = 0
    for q in qty_inputs:
        try:
            total_qty += int(q.get_attribute("value") or 0)
        except Exception:
            pass
    assert (len(rows) >= 2) or (total_qty >= 2)
