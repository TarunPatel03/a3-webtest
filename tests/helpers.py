import time
from .utils import try_xpath_any, wait_visible, get_body_text_stable

REGISTER_URL = "https://ecommerce-playground.lambdatest.io/index.php?route=account/register"
LOGIN_URL = "https://ecommerce-playground.lambdatest.io/index.php?route=account/login"
LOGOUT_URL = "https://ecommerce-playground.lambdatest.io/index.php?route=account/logout"


def unique_email() -> str:
    return f"qa+{int(time.time()*1000)}@example.com"


def fill_registration_form(driver, *, fname: str, lname: str, email: str, phone: str, password: str):
    """Navigate to registration and submit the form; resilient to theme variations."""
    driver.get(REGISTER_URL)
    # Flexible locators by id or name, with fallback nav via Login -> Continue
    from selenium.common.exceptions import TimeoutException
    try:
        wait_visible(driver, "id", "input-firstname").send_keys(fname)
    except TimeoutException:
        driver.get(LOGIN_URL)
        cont = try_xpath_any(
            driver,
            [
                "//a[contains(@href,'account/register') and (contains(.,'Continue') or contains(.,'Register'))]",
                "//form[contains(@action,'account/register')]//input[@type='submit' or @value='Continue']",
                "//button[contains(.,'Continue') or contains(.,'Register')]",
            ],
        )
        try:
            cont.click()
        except Exception:
            driver.execute_script("arguments[0].click();", cont)
        wait_visible(driver, "id", "input-firstname").send_keys(fname)
    wait_visible(driver, "id", "input-lastname").send_keys(lname)
    wait_visible(driver, "id", "input-email").send_keys(email)
    wait_visible(driver, "id", "input-telephone").send_keys(phone)
    wait_visible(driver, "id", "input-password").send_keys(password)
    wait_visible(driver, "id", "input-confirm").send_keys(password)
    # agree to policy if present
    try:
        agree = driver.find_element("name", "agree")
        if not agree.is_selected():
            agree.click()
    except Exception:
        pass
    # submit
    btn = try_xpath_any(driver, [
        "//form[contains(@action,'account/register')]//input[@type='submit']",
        "//input[@type='submit' and @value='Continue']",
        "//button[contains(.,'Continue')]",
    ])
    try:
        btn.click()
    except Exception:
        driver.execute_script("arguments[0].click();", btn)


def create_account(driver):
    """Create an account and then logout to be ready for login scenarios.

    Returns:
        (email, password)
    """
    email = unique_email()
    fill_registration_form(
        driver,
        fname="Tarun",
        lname="QA",
        email=email,
        phone="0400000000",
        password="P@ssw0rd!123",
    )
    try:
        driver.get(LOGOUT_URL)
    except Exception:
        pass
    return email, "P@ssw0rd!123"


def ensure_logged_in(driver):
    body = get_body_text_stable(driver)
    if "my account" in body:
        return
    # else create account and land logged in
    driver.get(REGISTER_URL)
    email = unique_email()
    driver.find_element("id", "input-firstname").send_keys("Tarun")
    driver.find_element("id", "input-lastname").send_keys("QA")
    driver.find_element("id", "input-email").send_keys(email)
    driver.find_element("id", "input-telephone").send_keys("0400000000")
    driver.find_element("id", "input-password").send_keys("P@ssw0rd!123")
    driver.find_element("id", "input-confirm").send_keys("P@ssw0rd!123")
    try:
        agree = driver.find_element("name", "agree")
        if not agree.is_selected():
            agree.click()
    except Exception:
        pass
    try_xpath_any(driver, ["//input[@type='submit']", "//button[contains(.,'Continue')]"]).click()
