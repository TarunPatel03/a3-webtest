"""
T005 — Registration required fields enforcement
Function: F2 — User registration
Tester: Riya Malvi
Steps:
  1) Submit the registration form without filling required fields
Expected: HTML5 validity or server alert prevents submission.
"""
import time
import pytest
from .helpers import REGISTER_URL
from .utils import wait_visible, try_xpath_any, get_body_text_stable


@pytest.mark.ui
def test_T005_registration_required_fields(driver):
    driver.get(REGISTER_URL)
    btn = try_xpath_any(driver, [
        "//form[contains(@action,'account/register')]//input[@type='submit']",
        "//input[@type='submit' and @value='Continue']",
        "//button[contains(.,'Continue')]",
    ])
    try:
        btn.click()
    except Exception:
        driver.execute_script("arguments[0].click();", btn)
    wait_visible(driver, "css selector", "body")
    any_invalid = False
    for _ in range(3):
        try:
            form = driver.find_element("xpath", "//form[contains(@action,'account/register')]")
            any_invalid = driver.execute_script(
                "return Array.from(arguments[0].querySelectorAll('input,textarea')).some(e => !e.checkValidity());",
                form,
            )
            break
        except Exception:
            time.sleep(0.2)
            continue
    alerts = driver.find_elements("css selector", ".alert-danger, .text-danger")
    body = get_body_text_stable(driver)
    url = driver.current_url
    assert any_invalid or alerts or ("required" in body) or ("warning" in body) or ("route=account/register" in url)
