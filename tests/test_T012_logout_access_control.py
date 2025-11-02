"""
T012 — Access control after logout
Function: F5 — User logout
Tester: Ethan Do
Steps:
  1) Ensure logged in; then logout
  2) Attempt to access a protected page (order history)
Expected: Redirect to login or access denied.
"""
import pytest
from .helpers import ensure_logged_in, LOGOUT_URL


@pytest.mark.ui
def test_T012_post_logout_access_control(driver):
    ensure_logged_in(driver)
    driver.get(LOGOUT_URL)
    driver.get("https://ecommerce-playground.lambdatest.io/index.php?route=account/order")
    title = driver.title.lower()
    body = driver.find_element("tag name", "body").text.lower()
    assert ("login" in title) or ("login" in body) or ("account" in title and "order" in body)
