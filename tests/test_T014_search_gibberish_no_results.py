
import pytest
from selenium.webdriver.common.keys import Keys
from .utils import wait_visible, get_body_text_stable


@pytest.mark.ui
def test_T014_search_gibberish_no_results(driver, base_url):
    driver.get(base_url)
    search = wait_visible(driver, "name", "search")
    search.clear(); search.send_keys("zzzzqwerty12345"); search.send_keys(Keys.ENTER)
    body = get_body_text_stable(driver)
    assert ("no product" in body) or ("no results" in body) or ("0 item" in body) or (len(driver.find_elements("css selector", ".product-layout")) == 0)
