# Assignment 3 — System Test

## 1. Overview

| Item | Details |
|------|---------|
| Website | E‑commerce Playground (demo store for testing) |
| Business goals | Allow visitors to discover products, register accounts, search the catalog, manage carts, and complete orders; demonstrate a modern e‑commerce flow for QA practice. |
| Primary user roles | Visitor (anonymous), Registered Customer (authenticated). Admin functions are out of scope for this assignment. |
| Scope of testing | Customer‑facing flows: Registration (F2), Login (F1), Logout (F5), Product Search (F3), Add to Cart (F4). |

Overview statement: We validate core customer flows that support the site’s goal of converting visitors into customers—ensuring users can create accounts, authenticate, discover items, and manage their shopping cart reliably. The chosen flows reflect high‑value entry, discovery, and conversion paths and are representative of broader system reliability.

---

## 2. System Functions

| ID | Name | Brief description | Web location (URL/route) | Dependencies |
|----|------|-------------------|---------------------------|--------------|
| F1 | User login | Authenticate an existing user via email and password; redirect to account dashboard on success. | `/index.php?route=account/login` | Depends on F2 (a registered account must exist). |
| F2 | User registration | Create a new customer account with required profile fields and password. | `/index.php?route=account/register` | None |
| F3 | Product search | Find products by keyword via global search box; present result grid and zero‑result states. | `/index.php?route=product/search` (initiated from home) | None |
| F4 | Add to cart | Add products to the shopping cart from search grid or product detail pages; update/remove items. | `/index.php?route=checkout/cart` (cart view) | May depend on F3 to locate products. |
| F5 | User logout | End authenticated session and reflect logged‑out state in UI. | `/index.php?route=account/logout` | Depends on F1 (must be logged in). |

Dependencies summary: F2 → F1 → (F5), and F3 → (F4). F4 can be reached via F3 (recommended) or direct navigation to PDPs.

---

## 3. Test Team

Fill SIDs and full names precisely to satisfy marking. Roles and responsibilities must map to Functions in Section 2.

| SID | Name | Role | Responsibilities (Functions) |
|-----|------|------|-------------------------------|
| 25485715 | Riya Malvi | Team Leader | F2: User Registration (3 test cases) |
| 24525192 | Caroline Potres | Login & Authentication Tester | F1: User Login (3 test cases) |
| 25445750 | Jaiden Valencia | Search Functionality Tester | F3: Product Search (3 test cases) |
| 25492000 | Tarun Patel | Shopping Cart Tester | F4: Add to Cart (3 test cases) |
| 24507271 | Ethan Do | Session Tester | F5: User Logout (3 test cases) |
| 25131754 | Edward Doan | Cross‑Function Tester | F2: Registration edge cases (3 test cases) |

Notes: Each member owns a distinct set of at least three detailed test cases (see Section 6). Some members cover an additional case by team agreement.

---

## 4. Task Schedule

| Member | Ordered test focus | Parallelization notes |
|--------|--------------------|-----------------------|
| Riya Malvi | Task 1 — F2 (User Registration) | Independent; unblocks F1. |
| Caroline Potres | Task 2 — F1 (User Login) | Dependent on F2; core auth coverage. |
| Jaiden Valencia | Task 3 — F3 (Product Search) | Independent of F1/F2; can run in parallel. |
| Tarun Patel | Task 4 — F4 (Add to Cart) | Independent; runs alongside Task 3. |
| Ethan Do | Task 5 — F5 (User Logout) | Dependent on F1; executes after Task 2. |
| Edward Doan | Parallel with Task 1 — F2 edge cases | Can execute in parallel with registration core tests. |

Parallel testing explanation: Registration‑dependent flows (F1/F5) are serialized per test account, but search/cart flows (F3/F4) are independent and safe to execute concurrently on separate browsers without data contention.

---

## 5. Test Environments and Tools

| Member | OS | Browser | Language/Runtime | Libraries/Tools | Notes |
|--------|----|---------|------------------|-----------------|-------|
| Riya Malvi | macOS | Chrome (stable) | Python 3.x | Selenium WebDriver | Uses VS Code |
| Caroline Potres | macOS | Chrome (stable) | Python 3.x | Selenium WebDriver | Uses VS Code |
| Jaiden Valencia | macOS | Chrome (stable) | Python 3.x | Selenium WebDriver | Uses VS Code |
| Tarun Patel | macOS | Chrome 141 (headed and headless) | Python 3.12 | selenium 4.38.0, pytest 8.4.2, webdriver‑manager 4.0.2 | Runs via `pytest --headed` for visible sessions. |
| Ethan Do | macOS | Chrome (stable) | Python 3.x | Selenium WebDriver | Uses VS Code |
| Edward Doan | macOS | Chrome (stable) | Python 3.x | Selenium WebDriver | Uses VS Code |

Infrastructure: Screenshots on failure saved to `artifacts/screenshots/`. Config in `pytest.ini`; base URL defaults to the LambdaTest playground.

---

# Functional Test Cases (E‑commerce Playground)

This document defines at least 18 test cases covering the requested functions:

- F2: User registration (depends on none)
- F1: User login (depends on F2)
- F5: User logout (depends on F1)
- F3: Product search (independent)
- F4: Add to cart (independent)

Conventions
- Tester: Tarun
- Base URL: https://ecommerce-playground.lambdatest.io/index.php?route=common/home
- Dynamic data: use unique email e.g., qa+<timestamp>@example.com
- Evidence: screenshots saved for each test case under `artifacts/screenshots/` as `T###_<OUTCOME>_<timestamp>.png`.

---

## T001 — Successful user registration

| Field | Value |
|------|-------|
| Test case ID | T001 |
| Function IDs/Name | F2 — User registration |
| Tester | Riya Malvi |

### Test scenario/steps

| Step | Test action |
|-----:|-------------|
| 1 | Navigate to My account → Register (URL: `/index.php?route=account/register`). |
| 2 | Enter First Name: "Tarun", Last Name: "QA". |
| 3 | Enter E‑mail: `qa+<timestamp>@example.com`. |
| 4 | Enter Telephone: any valid number (e.g., `0400000000`). |
| 5 | Enter Password: `P@ssw0rd!123` and confirm same. |
| 6 | Agree to Privacy Policy if required. |
| 7 | Click Continue/Submit. |

### Test results
- Expected: Registration success page displays and user account area is accessible. Account name appears in header.

---

## T002 — Registration with existing email blocked

| Field | Value |
|------|-------|
| Test case ID | T002 |
| Function IDs/Name | F2 — User registration |
| Tester | Edward Doan |

### Test scenario/steps

| Step | Test action |
|-----:|-------------|
| 1 | Attempt registration using an email that is already registered. |
| 2 | Fill all other fields validly and submit. |

### Test results
- Expected: Error message indicates the E‑mail address is already registered; registration is not created.

---

## T003 — Registration input validation (invalid email)

| Field | Value |
|------|-------|
| Test case ID | T003 |
| Function IDs/Name | F2 — User registration |
| Tester | Edward Doan |

### Test scenario/steps

| Step | Test action |
|-----:|-------------|
| 1 | On Register page, enter email without `@` (e.g., `invalidemail`). |
| 2 | Fill other fields validly; submit. |

### Test results
- Expected: Inline validation or error banner indicates invalid email format; registration blocked.

---

## T004 — Registration password policy (weak password)

| Field | Value |
|------|-------|
| Test case ID | T004 |
| Function IDs/Name | F2 — User registration |
| Tester | Edward Doan |

### Test scenario/steps

| Step | Test action |
|-----:|-------------|
| 1 | Enter a weak password (e.g., `12345`) and confirm same. |
| 2 | Submit. |

### Test results
- Expected: Validation message for password requirements (min length or complexity); registration blocked.

---

## T005 — Registration required fields enforcement

| Field | Value |
|------|-------|
| Test case ID | T005 |
| Function IDs/Name | F2 — User registration |
| Tester | Riya Malvi |

### Test scenario/steps

| Step | Test action |
|-----:|-------------|
| 1 | Leave First Name blank (or other required field). |
| 2 | Submit. |

### Test results
- Expected: Field‑level error message appears; cannot proceed.

---

## T006 — Registration with international characters

| Field | Value |
|------|-------|
| Test case ID | T006 |
| Function IDs/Name | F2 — User registration |
| Tester | Riya Malvi |

### Test scenario/steps

| Step | Test action |
|-----:|-------------|
| 1 | Register with First/Last name containing Unicode characters (e.g., "Łukasz", "Галина"). |
| 2 | Submit. |

### Test results
- Expected: Registration succeeds; names render correctly on account page.

---

## T007 — Successful user login

| Field | Value |
|------|-------|
| Test case ID | T007 |
| Function IDs/Name | F1 — User login (depends on F2) |
| Tester | Caroline Potres |

### Test scenario/steps

| Step | Test action |
|-----:|-------------|
| 1 | Navigate to My account → Login. |
| 2 | Enter a registered email and correct password. |
| 3 | Click Login. |

### Test results
- Expected: User is redirected to Account Dashboard; username visible in header.

---

## T008 — Login fails with incorrect password

| Field | Value |
|------|-------|
| Test case ID | T008 |
| Function IDs/Name | F1 — User login |
| Tester | Caroline Potres |

### Test scenario/steps

| Step | Test action |
|-----:|-------------|
| 1 | On Login page, input registered email and wrong password. |
| 2 | Submit. |

### Test results
- Expected: Error message indicates mismatch; user remains on login page.

---

## T009 — Login with unregistered email

| Field | Value |
|------|-------|
| Test case ID | T009 |
| Function IDs/Name | F1 — User login |
| Tester | Caroline Potres |

### Test scenario/steps

| Step | Test action |
|-----:|-------------|
| 1 | Enter non‑existent email (qa+noacct@example.com) and valid‑looking password. |
| 2 | Submit. |

### Test results
- Expected: Error message; no login.

---

## T010 — Case sensitivity check (email, password)

| Field | Value |
|------|-------|
| Test case ID | T010 |
| Function IDs/Name | F1 — User login |
| Tester | Caroline Potres |

### Test scenario/steps

| Step | Test action |
|-----:|-------------|
| 1 | Try logging in with upper‑cased email vs. saved lowercase; use correct password. |
| 2 | Try logging in with correct email but password using different casing if policy allows; submit. |

### Test results
- Expected: Email should be case‑insensitive; password case‑sensitive. Login only succeeds for the correct password.

---

## T011 — Successful logout from header

| Field | Value |
|------|-------|
| Test case ID | T011 |
| Function IDs/Name | F5 — User logout (depends on F1) |
| Tester | Ethan Do |

### Test scenario/steps

| Step | Test action |
|-----:|-------------|
| 1 | While logged in, click My account → Logout. |

### Test results
- Expected: Logout confirmation page shown; header reflects logged‑out state.

---

## T012 — Access control after logout

| Field | Value |
|------|-------|
| Test case ID | T012 |
| Function IDs/Name | F5 — User logout |
| Tester | Ethan Do |

### Test scenario/steps

| Step | Test action |
|-----:|-------------|
| 1 | After logout, attempt to open a protected page (e.g., order history). |

### Test results
- Expected: Redirected to login page or error shown; no access granted.

---

## T013 — Search returns results for common term

| Field | Value |
|------|-------|
| Test case ID | T013 |
| Function IDs/Name | F3 — Product search |
| Tester | Jaiden Valencia |

### Test scenario/steps

| Step | Test action |
|-----:|-------------|
| 1 | From home, search for "iphone" and submit. |

### Test results
- Expected: Results page lists one or more products. [Automated: PASS] 

---

## T014 — Search with gibberish shows no results message

| Field | Value |
|------|-------|
| Test case ID | T014 |
| Function IDs/Name | F3 — Product search |
| Tester | Jaiden Valencia |

### Test scenario/steps

| Step | Test action |
|-----:|-------------|
| 1 | Search for a random string like `zzzzqwerty12345`. |

### Test results
- Expected: Page shows a clear "no results" state.

---

## T015 — Search is case‑insensitive

| Field | Value |
|------|-------|
| Test case ID | T015 |
| Function IDs/Name | F3 — Product search |
| Tester | Jaiden Valencia |

### Test scenario/steps

| Step | Test action |
|-----:|-------------|
| 1 | Search for `IPHONE` and compare count with `iphone`. |

### Test results
- Expected: Result set comparable; case‑insensitive behavior.

---

## T016 — Add first result to cart from grid

| Field | Value |
|------|-------|
| Test case ID | T016 |
| Function IDs/Name | F4 — Add to cart |
| Tester | Tarun Patel |

### Test scenario/steps

| Step | Test action |
|-----:|-------------|
| 1 | Search for "iphone". |
| 2 | On results grid, click Add to Cart on the first visible product. |
| 3 | Open cart page. |

### Test results
- Expected: Cart shows at least one item. [Automated: PASS]

---

## T017 — Update item quantity in cart

| Field | Value |
|------|-------|
| Test case ID | T017 |
| Function IDs/Name | F4 — Add to cart |
| Tester | Tarun Patel |

### Test scenario/steps

| Step | Test action |
|-----:|-------------|
| 1 | On cart page, change quantity of first item from 1 → 2 and update. |

### Test results
- Expected: Quantity updates and totals recalc accordingly.

---

## T018 — Remove item from cart

| Field | Value |
|------|-------|
| Test case ID | T018 |
| Function IDs/Name | F4 — Add to cart |
| Tester | Tarun Patel |

### Test scenario/steps

| Step | Test action |
|-----:|-------------|
| 1 | On cart page, click Remove for any listed item(s). |

### Test results
- Expected: Item removed; cart reflects new state (possibly empty). [Automated: PASS]

---

## T019 — Search then add multiple items to cart
| Field | Value |
|------|-------|
| Test case ID | T019 |
| Function IDs/Name | F3, F4 — Search + Add to cart |
| Tester | Ethan Do |

### Test scenario/steps

| Step | Test action |
|-----:|-------------|
| 1 | Search for a common term (e.g., "phone"). Add the first two results to cart. |
| 2 | Open cart page. |

### Test results
- Expected: Cart shows 2 line items; total quantity = 2.

---

## T020 — Add to cart from product detail page (with required options)

| Field | Value |
|------|-------|
| Test case ID | T020 |
| Function IDs/Name | F4 — Add to cart |
| Tester | Tarun Patel |

### Test scenario/steps

| Step | Test action |
|-----:|-------------|
| 1 | Search for a product that requires options (e.g., a phone with color/size). |
| 2 | Open PDP; select any valid required options. |
| 3 | Click Add to Cart; open cart page. |

### Test results
- Expected: Item added with selected options displayed in cart.

---

Notes
- Automated coverage includes T001–T020 only. Non‑essential tests and scripts were removed for submission clarity.
- Registration/login tests auto‑create throwaway accounts and run headless by default; use `--headed` to observe flows interactively.

---

## Visible run results

- Mode: Headed (visible Chrome)
- Environment: macOS; Chrome 141; Python 3.12; selenium 4.38.0
- Command: `pytest --headed -q`
- Outcome: 20 passed, 0 deselected, 0 xfailed; 0 failed
- Date: Generated during this session; screenshots saved for each test case in `artifacts/screenshots/`

### Run status per test case (headed)

| ID   | Function | Status | Notes |
|------|----------|--------|-------|
| T001 | F2 — Registration | PASS (Automated) | Headed run 2025-11-02 |
| T002 | F2 — Registration duplicate | PASS (Automated) | Headed run 2025-11-02 |
| T003 | F2 — Registration invalid email | PASS (Automated) | Headed run 2025-11-02 |
| T004 | F2 — Password policy | PASS (Automated) | Headed run 2025-11-02 |
| T005 | F2 — Required fields | PASS (Automated) | Headed run 2025-11-02 |
| T006 | F2 — Unicode names | PASS (Automated) | Headed run 2025-11-02 |
| T007 | F1 — Login success | PASS (Automated) | Headed run 2025-11-02 |
| T008 | F1 — Wrong password | PASS (Automated) | Headed run 2025-11-02 |
| T009 | F1 — Unregistered email | PASS (Automated) | Headed run 2025-11-02 |
| T010 | F1 — Case sensitivity | PASS (Automated) | Headed run 2025-11-02 |
| T011 | F5 — Logout | PASS (Automated) | Headed run 2025-11-02 |
| T012 | F5 — Post-logout access control | PASS (Automated) | Headed run 2025-11-02 |
| T013 | F3 — Search results | PASS (Automated) | Headed run 2025-11-02 |
| T014 | F3 — Search no results | PASS (Automated) | Headed run 2025-11-02 |
| T015 | F3 — Search case-insensitive | PASS (Automated) | Headed run 2025-11-02 |
| T016 | F4 — Add to cart (grid) | PASS (Automated) | Headed run 2025-11-02 |
| T017 | F4 — Update cart quantity | PASS (Automated) | Headed run 2025-11-02 |
| T018 | F4 — Remove from cart | PASS (Automated) | Headed run 2025-11-02 |
| T019 | F3+F4 — Add multiple items | PASS (Automated) | Headed run 2025-11-02 |
| T020 | F4 — Add from PDP with options | PASS (Automated) | Headed run 2025-11-02 |

---

## 7. Analysis & Reflections

Basic statistics (group):
- Automated suite (headed Chrome, 2025‑11‑02): 20 passed, 0 deselected, 0 xfailed; 0 failed
- Coverage: T001–T020 are fully automated and passing in headed mode; one file per test case; screenshots saved for each.

Defects observed (if any):
- No functional defects in the site under test (F1–F5) during the final headed run.
- Notes from automation stability work (not product bugs):
	- Primary actions vary between <input> and <button>; we use flexible locators/XPaths to handle both.
	- Chrome 141 occasionally raised a transient “Node with given id … does not belong to the document” when reading body text; mitigated by JS `document.body.innerText` with retries.
	- Theme wording for “no results” can differ; assertions allow equivalent messages.

Successes:
- Achieved fully green headed run for all target cases (T001–T020) after stabilizing waits and click strategies.
- Covered core business flows end‑to‑end: Registration → Login → Search → Cart → Logout.
- Tests resilient to minor UI/theme variations; failures now diagnose real regressions rather than timing.
- Clear ownership: three unique test cases per member (with two intentional extras to fill T010 and T020).
 - Specific fixes that improved reliability:
 	- Rewrote `get_body_text_stable` to use JS innerText with retries to avoid ChromeDriver staleness.
 	- Ensured logout before the duplicate‑email registration attempt (T002) to trigger the expected validation path.

Failures/limitations:
- Single‑browser certification (Chrome) only; no cross‑browser matrix executed.
- No accessibility/performance checks included; scope limited to functional happy/negative paths.

Lessons learned:
- Invest early in robust synchronization (document.readyState + JS innerText + re‑locate on staleness) to eliminate flakes.
- Keep assertions tolerant to content wording variations while remaining outcome‑specific.
- Partition data and isolate accounts to allow safe parallelization without cross‑test interference.
- Centralize stability helpers (wait/click/text) to enforce consistency across tests.

If doing it again differently:
- Introduce Page Object Model for higher reuse and clearer intent, especially for PDPs with required options.
- Add CI with pytest‑xdist and a cross‑browser matrix (Chrome/Firefox/Safari) for broader coverage.
- Include basic accessibility smoke (axe‑core) and simple performance timings on critical flows.
- Externalize or seed test data where possible to decouple from live indexing/timing and improve determinism.

---

## 8. Presentation (Week 12)

Optional: prepare a 5–7 minute walkthrough covering the Overview, System Functions, one representative test case per member, and the headed run result summary. Early feedback can be incorporated before final submission.

