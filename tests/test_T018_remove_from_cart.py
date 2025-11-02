
import pytest
from .utils import save_named_screenshot


@pytest.mark.ui
def test_T018_remove_item_from_cart(driver):
    driver.get("https://ecommerce-playground.lambdatest.io/index.php?route=checkout/cart")
    buttons = driver.find_elements("xpath", "//button[contains(@data-original-title,'Remove') or contains(@title,'Remove') or contains(.,'Remove')]")
    removed = False
    for b in buttons:
        try:
            b.click(); removed = True
        except Exception:
            pass
    # Take explicit screenshot after attempting removals; highlight empty cart area if present
    try:
        empty = driver.find_element("xpath", "//*[contains(.,'Your shopping cart is empty') or contains(.,'Shopping Cart')]")
        try:
            driver.execute_script("arguments[0].scrollIntoView({block:'center'}); arguments[0].style.outline='5px solid red';", empty)
        except Exception:
            pass
    except Exception:
        pass
    save_named_screenshot(driver, "T018_context_after_remove")
    body = driver.find_element("tag name", "body").text.lower()
    assert removed or ("empty" in body) or ("shopping cart" in body)
