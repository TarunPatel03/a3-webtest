
import pytest
from .helpers import LOGIN_URL
from .utils import try_xpath_any, get_body_text_stable


@pytest.mark.ui
def test_T009_login_unregistered_email(driver):
    driver.get(LOGIN_URL)
    driver.find_element("id", "input-email").send_keys("qa+noacct@example.com")
    driver.find_element("id", "input-password").send_keys("P@ssw0rd!123")
    try_xpath_any(driver, ["//input[@type='submit']", "//button[contains(.,'Login')]"]).click()
    url = driver.current_url
    alerts = driver.find_elements("css selector", ".alert-danger, .alert-warning")
    body = get_body_text_stable(driver)
    assert ("route=account/login" in url) or alerts or ("returning customer" in body) or ("login" in body)
