"""
T007 — Successful user login
Function: F1 — User login (depends on F2)
Tester: Caroline Potres
Steps:
  1) Create an account
  2) Login with correct credentials
Expected: Account dashboard visible.
"""
import pytest
from .helpers import create_account, LOGIN_URL
from .utils import try_xpath_any, get_body_text_stable


@pytest.mark.ui
def test_T007_login_success(driver):
    email, password = create_account(driver)
    driver.get(LOGIN_URL)
    driver.find_element("id", "input-email").send_keys(email)
    driver.find_element("id", "input-password").send_keys(password)
    try_xpath_any(driver, ["//input[@type='submit']", "//button[contains(.,'Login')]"]).click()
    body = get_body_text_stable(driver)
    assert ("my account" in body) or ("account" in driver.title.lower())
