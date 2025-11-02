import os
import pytest
from datetime import datetime
import re
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

BASE_URL = os.environ.get(
    "ECOM_BASE_URL",
    "https://ecommerce-playground.lambdatest.io/index.php?route=common/home",
)

ARTIFACTS_DIR = Path(__file__).resolve().parent.parent / "artifacts"
SCREENSHOT_DIR = ARTIFACTS_DIR / "screenshots"


def _ensure_dirs():
    SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)


def pytest_addoption(parser):
    parser.addoption(
        "--headed",
        action="store_true",
        default=False,
        help="Run browser in headed (non-headless) mode",
    )


@pytest.fixture(scope="session")
def base_url():
    return BASE_URL


@pytest.fixture(scope="session")
def driver(request):
    """Provide a session-scoped Chrome WebDriver.

    Uses headless Chrome by default; pass --headed to see the browser.
    """
    _ensure_dirs()

    headed = request.config.getoption("--headed")
    opts = Options()
    if not headed:
        # Use new headless if available
        opts.add_argument("--headless=new")
    # Common flags for CI stability
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")

    service = Service(ChromeDriverManager().install())
    drv = webdriver.Chrome(service=service, options=opts)
    drv.set_window_size(1440, 900)

    yield drv

    drv.quit()


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    """Capture a screenshot for each test outcome (PASS/FAIL/SKIP/XFAIL/XPASS).

    Filenames: <TESTCASEID>_<OUTCOME>_<timestamp>.png, e.g., T001_PASS_20251102-123000.png
    Falls back to sanitized nodeid if no T### pattern is found.
    """
    outcome = yield
    rep = outcome.get_result()

    # Determine outcome label
    label = None
    if rep.when == "call":
        if rep.failed:
            label = "FAIL"
        elif rep.passed:
            label = "XPASS" if getattr(rep, "wasxfail", False) else "PASS"
    elif rep.when == "setup" and rep.skipped:
        label = "XFAIL" if getattr(rep, "wasxfail", False) else "SKIP"

    if label:
        try:
            drv = item.funcargs.get("driver")
        except Exception:
            drv = None
        if drv:
            ts = datetime.now().strftime("%Y%m%d-%H%M%S")
            # Extract test case id like T001 from nodeid
            nodeid = item.nodeid
            m = re.search(r"T\d{3}", nodeid)
            case_id = m.group(0) if m else nodeid.replace('::', '__').replace('/', '_')
            fname = f"{case_id}_{label}_{ts}.png"
            path = SCREENSHOT_DIR / fname
            try:
                drv.save_screenshot(str(path))
                rep.extra = getattr(rep, "extra", []) + [str(path)]
            except Exception:
                pass
