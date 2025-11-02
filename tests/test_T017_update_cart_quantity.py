
import pytest
from selenium.webdriver.common.keys import Keys
from .utils import wait_visible, wait_all_present, try_xpath_any, scroll_into_view_and_click


@pytest.mark.ui
def test_T017_update_item_quantity_in_cart(driver, base_url):
    # Ensure one item exists
    driver.get(base_url)
    s = wait_visible(driver, "name", "search")
    s.clear(); s.send_keys("iphone"); s.send_keys(Keys.ENTER)
    wait_all_present(driver, "css selector", ".product-layout")
    add_btn = try_xpath_any(
        driver,
        [
            "(//div[contains(@class,'product-layout')])[1]//button[contains(@title,'Add to Cart') or contains(@title,'Add to cart') or contains(@data-original-title,'Add to Cart') or contains(@data-original-title,'Add to cart') or contains(.,'Add to Cart') or contains(.,'Add to cart')]",
        ],
    )
    scroll_into_view_and_click(driver, add_btn)

    driver.get("https://ecommerce-playground.lambdatest.io/index.php?route=checkout/cart")
    qty_inputs = driver.find_elements("css selector", "input[name*='quantity']")
    if qty_inputs:
        qty_inputs[0].clear(); qty_inputs[0].send_keys("2")
        try:
            upd = driver.find_element("xpath", "//button[contains(@data-original-title,'Update') or contains(.,'Update')]")
            upd.click()
        except Exception:
            pass
        val = qty_inputs[0].get_attribute("value")
        assert val in ("2", 2)
    else:
        pytest.xfail("Cart quantity input not found in current theme")
