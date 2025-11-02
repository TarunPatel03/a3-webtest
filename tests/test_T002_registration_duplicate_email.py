
import pytest
from .helpers import fill_registration_form, unique_email, REGISTER_URL, LOGOUT_URL
from .utils import wait_visible, try_xpath_any, get_body_text_stable


@pytest.mark.ui
def test_T002_registration_duplicate_email_blocked(driver):
    base_email = unique_email()
    fill_registration_form(driver, fname="Tarun", lname="QA", email=base_email, phone="0400000000", password="P@ssw0rd!123")
    # Ensure we are logged out before attempting to re-register with the same email,
    # otherwise the site may redirect to account pages instead of showing an error.
    try:
        driver.get(LOGOUT_URL)
    except Exception:
        pass

    driver.get(REGISTER_URL)
    wait_visible(driver, "id", "input-firstname").send_keys("Tarun")
    wait_visible(driver, "id", "input-lastname").send_keys("QA")
    wait_visible(driver, "id", "input-email").send_keys(base_email)
    wait_visible(driver, "id", "input-telephone").send_keys("0400000000")
    wait_visible(driver, "id", "input-password").send_keys("P@ssw0rd!123")
    wait_visible(driver, "id", "input-confirm").send_keys("P@ssw0rd!123")
    try:
        agree = driver.find_element("name", "agree")
        if not agree.is_selected():
            agree.click()
    except Exception:
        pass
    btn = try_xpath_any(driver, [
        "//form[contains(@action,'account/register')]//input[@type='submit']",
        "//input[@type='submit' and @value='Continue']",
        "//button[contains(.,'Continue')]",
    ])
    try:
        btn.click()
    except Exception:
        driver.execute_script("arguments[0].click();", btn)
    alerts = driver.find_elements("css selector", ".alert-danger, .text-danger")
    body = get_body_text_stable(driver)
    assert alerts or ("already registered" in body) or ("warning" in body)
