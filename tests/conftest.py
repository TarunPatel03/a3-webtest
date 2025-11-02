import os
import pytest
from datetime import datetime
import re
from pathlib import Path
from urllib.parse import urlparse, parse_qs

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
            # Derive a short page context from URL/title/DOM state to distinguish pages
            try:
                url = drv.current_url
                parsed = urlparse(url)
                qs = parse_qs(parsed.query)
                route = (qs.get('route', [""])[0] or "").strip()
                if route:
                    context = route.replace('/', '-')
                else:
                    # fallback to path segment or title
                    context = (parsed.path.strip('/').replace('/', '-') or drv.title or "page").lower().replace(' ', '-')
                # include a short title slug
                title_slug = (drv.title or "").lower().strip().replace(' ', '-')
                title_slug = re.sub(r"[^a-z0-9\-]", "", title_slug)[:24]
                # include presence of alert banners as a signal (e.g., login failure)
                try:
                    has_alert = bool(drv.find_elements("css selector", ".alert-danger, .alert-warning"))
                except Exception:
                    has_alert = False
                alert_slug = "alert" if has_alert else "noalert"
                # include presence of login form fields to differentiate login page vs account area
                try:
                    has_login_form = bool(drv.find_elements("id", "input-email")) and bool(drv.find_elements("id", "input-password"))
                except Exception:
                    has_login_form = False
                form_slug = "loginform" if has_login_form else "noform"
                # normalize primary context and combine
                context = re.sub(r"[^a-zA-Z0-9\-]", "", context)[:28] or "page"
                combined_ctx = "__".join(filter(None, [context, title_slug, alert_slug, form_slug]))
            except Exception:
                combined_ctx = "page"
            fname = f"{case_id}_{label}_{ts}__{combined_ctx}.png"
            path = SCREENSHOT_DIR / fname
            try:
                drv.save_screenshot(str(path))
                rep.extra = getattr(rep, "extra", []) + [str(path)]
            except Exception:
                pass
