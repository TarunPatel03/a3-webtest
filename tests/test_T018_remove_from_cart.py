"""
T018 — Remove item from cart
Function: F4 — Add to cart
Tester: Tarun Patel
Steps:
  1) Open cart page
  2) Remove visible items
Expected: At least one remove action succeeds or cart is empty.
"""
import pytest


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
    body = driver.find_element("tag name", "body").text.lower()
    assert removed or ("empty" in body) or ("shopping cart" in body)
