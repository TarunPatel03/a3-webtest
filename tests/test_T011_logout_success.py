
import pytest
from .helpers import ensure_logged_in, LOGOUT_URL
from .utils import get_body_text_stable


@pytest.mark.ui
def test_T011_logout_success(driver):
    ensure_logged_in(driver)
    driver.get(LOGOUT_URL)
    body = get_body_text_stable(driver)
    assert ("account logout" in body) or ("successfully logged out" in body) or ("logout" in driver.title.lower())
