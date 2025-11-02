"""
T001 — Successful user registration
Function: F2 — User registration
Tester: Riya Malvi
Steps:
  1) Open Register page
  2) Fill valid details with unique email
  3) Submit
Expected: Success page/account area appears ("Your Account Has Been Created" or "My Account").
"""
import pytest
from .helpers import fill_registration_form, unique_email
from .utils import get_body_text_stable


@pytest.mark.ui
def test_T001_registration_success(driver):
    email = unique_email()
    fill_registration_form(driver, fname="Tarun", lname="QA", email=email, phone="0400000000", password="P@ssw0rd!123")
    body = get_body_text_stable(driver)
    assert ("your account has been created" in body) or ("my account" in body)
