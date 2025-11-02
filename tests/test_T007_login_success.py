
import pytest
from .helpers import create_account, LOGIN_URL, ACCOUNT_URL
from .utils import try_xpath_any, get_body_text_stable, wait_visible, safe_click_with_retry, save_named_screenshot


@pytest.mark.ui
def test_T007_login_success(driver):
  email, password = create_account(driver)
  driver.get(LOGIN_URL)
  wait_visible(driver, "id", "input-email").send_keys(email)
  wait_visible(driver, "id", "input-password").send_keys(password)
  # Robust click on login
  try:
    btn = try_xpath_any(
      driver,
      [
        "//form[contains(@action,'account/login')]//input[@type='submit']",
        "//input[@type='submit' and @value='Login']",
        "//button[contains(.,'Login')]",
      ],
    )
    btn.click()
  except Exception:
    safe_click_with_retry(driver, "css selector", "input[type='submit'], button")

  # Take an explicit context screenshot after login attempt
  save_named_screenshot(driver, "T007_context_after_login_click")
  # Keep original success criteria to avoid false negatives on themed pages
  body = get_body_text_stable(driver)
  assert ("my account" in body) or ("account" in driver.title.lower())
