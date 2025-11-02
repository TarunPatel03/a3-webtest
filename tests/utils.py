from typing import Optional, List
import time
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    StaleElementReferenceException,
    NoSuchElementException,
    WebDriverException,
)


DEFAULT_TIMEOUT = 15


def wait_visible(driver: WebDriver, by: str, selector: str, timeout: int = DEFAULT_TIMEOUT):
    return WebDriverWait(driver, timeout).until(
        EC.visibility_of_element_located((by, selector))
    )


def wait_all_present(driver: WebDriver, by: str, selector: str, timeout: int = DEFAULT_TIMEOUT):
    return WebDriverWait(driver, timeout).until(
        EC.presence_of_all_elements_located((by, selector))
    )


def try_xpath_any(driver: WebDriver, xpaths: List[str], timeout: int = DEFAULT_TIMEOUT):
    for xp in xpaths:
        try:
            el = WebDriverWait(driver, timeout).until(
                EC.presence_of_element_located((By.XPATH, xp))
            )
            return el
        except Exception:
            continue
    raise TimeoutError(f"None of the XPaths became present: {xpaths}")


def wait_clickable(driver: WebDriver, by: str, selector: str, timeout: int = DEFAULT_TIMEOUT):
    return WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable((by, selector))
    )


def scroll_into_view_and_click(driver: WebDriver, element):
    try:
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", element)
    except Exception:
        pass
    try:
        element.click()
    except Exception:
        # Fallback to JS click
        try:
            driver.execute_script("arguments[0].click();", element)
        except Exception:
            raise


def wait_document_ready(driver: WebDriver, timeout: int = DEFAULT_TIMEOUT):
    WebDriverWait(driver, timeout).until(
        lambda d: d.execute_script("return document.readyState") in ("interactive", "complete")
    )


def get_body_text_stable(driver: WebDriver, timeout: int = DEFAULT_TIMEOUT) -> str:
    """Return page body text robustly, tolerating DOM refreshes and ChromeDriver quirks.

    Strategy:
    - Wait for document readiness
    - Prefer JS to read document.body.innerText to avoid holding a WebElement reference
    - On transient driver errors (including "Node with given id ..."), retry until timeout
    - Fallback to locating <body>.text if JS repeatedly fails
    """
    wait_document_ready(driver, timeout)
    end = time.time() + timeout
    last_exc: Optional[Exception] = None

    # First try a JS-driven approach which avoids stale element references
    while time.time() < end:
        try:
            text = driver.execute_script(
                "return (document && document.body) ? document.body.innerText : '';"
            )
            return (text or "").lower()
        except WebDriverException as e:
            # Covers cases like: "Node with given id does not belong to the document"
            last_exc = e
            time.sleep(0.2)
            continue

    # Fallback: attempt via element lookup with staleness retry
    end = time.time() + max(1, int(DEFAULT_TIMEOUT / 2))
    while time.time() < end:
        try:
            el = driver.find_element("css selector", "body")
            return (el.text or "").lower()
        except (StaleElementReferenceException, NoSuchElementException, WebDriverException) as e:
            last_exc = e
            time.sleep(0.2)
            continue

    if last_exc:
        raise last_exc
    return ""


def safe_click_with_retry(driver: WebDriver, by: str, selector: str, timeout: int = DEFAULT_TIMEOUT):
    """Click an element located by (by, selector) with staleness retry.

    Refetches the element if it becomes stale between resolution and click.
    """
    wait_document_ready(driver, timeout)
    end = time.time() + timeout
    last_exc: Optional[Exception] = None
    while time.time() < end:
        try:
            el = wait_clickable(driver, by, selector, timeout=max(1, int(end - time.time())))
            scroll_into_view_and_click(driver, el)
            return
        except (StaleElementReferenceException, NoSuchElementException) as e:
            last_exc = e
            time.sleep(0.2)
            continue
    if last_exc:
        raise last_exc
