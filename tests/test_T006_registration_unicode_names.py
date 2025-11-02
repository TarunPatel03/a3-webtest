
import pytest
from .helpers import unique_email, REGISTER_URL
from .utils import wait_visible, try_xpath_any, get_body_text_stable


@pytest.mark.ui
def test_T006_registration_unicode_names_success(driver):
    email = unique_email()
    driver.get(REGISTER_URL)
    wait_visible(driver, "id", "input-firstname").send_keys("Łukasz")
    wait_visible(driver, "id", "input-lastname").send_keys("Галина")
    wait_visible(driver, "id", "input-email").send_keys(email)
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
    body = get_body_text_stable(driver)
    assert ("your account has been created" in body) or ("my account" in body)
