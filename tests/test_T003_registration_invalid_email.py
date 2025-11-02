
import pytest
from .helpers import REGISTER_URL
from .utils import wait_visible, try_xpath_any, get_body_text_stable


@pytest.mark.ui
def test_T003_registration_invalid_email_validation(driver):
    driver.get(REGISTER_URL)
    wait_visible(driver, "id", "input-firstname").send_keys("Tarun")
    wait_visible(driver, "id", "input-lastname").send_keys("QA")
    email_el = wait_visible(driver, "id", "input-email"); email_el.send_keys("invalid")
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
        "//input[@type='submit']",
        "//button[contains(.,'Continue')]",
    ])
    try:
        btn.click()
    except Exception:
        driver.execute_script("arguments[0].click();", btn)
    vm = driver.execute_script("return arguments[0].validationMessage;", email_el) or ""
    alerts = driver.find_elements("css selector", ".alert-danger, .text-danger")
    body = get_body_text_stable(driver)
    assert vm or alerts or ("invalid" in body) or ("warning" in body)
