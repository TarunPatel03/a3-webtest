"""
T013 — Search returns results for common term
Function: F3 — Product search
Tester: Jaiden Valencia
Steps:
  1) Search for "iphone"
Expected: One or more products listed.
"""
import pytest
from selenium.webdriver.common.keys import Keys
from .utils import wait_visible, wait_all_present


@pytest.mark.ui
def test_T013_search_returns_results(driver, base_url):
    driver.get(base_url)
    search = wait_visible(driver, "name", "search")
    search.clear(); search.send_keys("iphone"); search.send_keys(Keys.ENTER)
    cards = wait_all_present(driver, "css selector", ".product-layout")
    assert len(cards) > 0
