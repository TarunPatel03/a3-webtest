
import pytest
from .helpers import fill_registration_form, unique_email
from .utils import get_body_text_stable


@pytest.mark.ui
def test_T001_registration_success(driver):
    email = unique_email()
    fill_registration_form(driver, fname="Tarun", lname="QA", email=email, phone="0400000000", password="P@ssw0rd!123")
    body = get_body_text_stable(driver)
    assert ("your account has been created" in body) or ("my account" in body)
