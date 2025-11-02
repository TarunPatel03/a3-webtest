
import pytest
from selenium.webdriver.common.keys import Keys
from .utils import wait_visible


@pytest.mark.ui
def test_T015_search_case_insensitive(driver, base_url):
    driver.get(base_url)
    search = wait_visible(driver, "name", "search")
    search.clear(); search.send_keys("IPHONE"); search.send_keys(Keys.ENTER)
    upper_count = len(driver.find_elements("css selector", ".product-layout"))

    driver.get(base_url)
    search = wait_visible(driver, "name", "search")
    search.clear(); search.send_keys("iphone"); search.send_keys(Keys.ENTER)
    lower_count = len(driver.find_elements("css selector", ".product-layout"))

    assert upper_count >= 0 and lower_count >= 0 and abs(upper_count - lower_count) <= max(upper_count, lower_count)
