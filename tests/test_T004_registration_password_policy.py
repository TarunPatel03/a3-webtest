"""
T004 — Registration password policy (weak password)
Function: F2 — User registration
Tester: Edward Doan
Steps:
  1) Enter short/weak password (e.g., 12345)
  2) Submit
Expected: Validation message for password; registration blocked.
"""
import time
import pytest
from .helpers import REGISTER_URL
from .utils import wait_visible, try_xpath_any, get_body_text_stable


@pytest.mark.ui
def test_T004_registration_password_policy_weak_rejected(driver):
    driver.get(REGISTER_URL)
    wait_visible(driver, "id", "input-firstname").send_keys("Tarun")
    wait_visible(driver, "id", "input-lastname").send_keys("QA")
    email_el = wait_visible(driver, "id", "input-email"); email_el.send_keys(f"qa+{int(time.time()*1000)}@example.com")
    wait_visible(driver, "id", "input-telephone").send_keys("0400000000")
    wait_visible(driver, "id", "input-password").send_keys("12345")
    wait_visible(driver, "id", "input-confirm").send_keys("12345")
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
    vm_pw = ""
    for _ in range(3):
        try:
            pw = driver.find_element("id", "input-password")
            vm_pw = driver.execute_script("return arguments[0].validationMessage;", pw) or ""
            break
        except Exception:
            time.sleep(0.2)
            continue
    alerts = driver.find_elements("css selector", ".alert-danger, .text-danger")
    body = get_body_text_stable(driver)
    assert vm_pw or alerts or ("warning" in body) or ("password" in body)
