
import pytest
from selenium.webdriver.common.keys import Keys
from .utils import wait_visible, wait_all_present, try_xpath_any, scroll_into_view_and_click


@pytest.mark.ui
def test_T016_add_first_result_to_cart_from_grid(driver, base_url):
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
    rows = driver.find_elements("css selector", ".table-responsive tbody tr, table tbody tr")
    assert len(rows) > 0
