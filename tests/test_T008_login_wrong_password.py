"""
T008 — Login fails with incorrect password
Function: F1 — User login
Tester: Caroline Potres
Steps:
  1) Create an account
  2) Attempt login with correct email and wrong password
Expected: Error shown or remain on login page.
"""
import pytest
from .helpers import create_account, LOGIN_URL
from .utils import try_xpath_any, get_body_text_stable


@pytest.mark.ui
def test_T008_login_wrong_password(driver):
    email, _ = create_account(driver)
    driver.get(LOGIN_URL)
    driver.find_element("id", "input-email").send_keys(email)
    driver.find_element("id", "input-password").send_keys("wrongpass")
    try_xpath_any(driver, ["//input[@type='submit']", "//button[contains(.,'Login')]"]).click()
    url = driver.current_url
    alerts = driver.find_elements("css selector", ".alert-danger, .alert-warning")
    body = get_body_text_stable(driver)
    assert ("route=account/login" in url) or alerts or ("returning customer" in body) or ("login" in body)
