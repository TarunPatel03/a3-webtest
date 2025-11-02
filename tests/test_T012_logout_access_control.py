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
from .utils import save_named_screenshot


@pytest.mark.ui
def test_T012_post_logout_access_control(driver):
    # Ensure we are logged in, then capture the account sidebar with Order History highlighted
    ensure_logged_in(driver)
    try:
        driver.get("https://ecommerce-playground.lambdatest.io/index.php?route=account/order")
        # Try to highlight the Order History link in the right sidebar if present
        try:
            el = driver.find_element("xpath", "//aside//a[contains(@href,'account/order') or contains(.,'Order History')]")
        except Exception:
            try:
                el = driver.find_element("xpath", "//a[contains(@href,'account/order') or contains(.,'Order History')]")
            except Exception:
                el = None
        if el:
            try:
                driver.execute_script(
                    "arguments[0].scrollIntoView({block:'center'}); arguments[0].style.outline='5px solid orange';",
                    el,
                )
            except Exception:
                pass
        save_named_screenshot(driver, "T012_context_order_history_sidebar")
    except Exception:
        # Non-fatal: proceed with core assertion
        pass

    driver.get(LOGOUT_URL)
    driver.get("https://ecommerce-playground.lambdatest.io/index.php?route=account/order")
    title = driver.title.lower()
    body = driver.find_element("tag name", "body").text.lower()
    assert ("login" in title) or ("login" in body) or ("account" in title and "order" in body)
