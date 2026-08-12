# 🚀 Darshan Hotel — Playwright + Pytest Automation Framework (Python)

![Playwright](https://img.shields.io/badge/Playwright-Automation-green)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Pytest](https://img.shields.io/badge/Pytest-Framework-yellow)
![Allure](https://img.shields.io/badge/Reporting-Allure-orange)
![Status](https://img.shields.io/badge/Status-Active-brightgreen)
![Author](https://img.shields.io/badge/Author-Satyendra%20Kumar%20Namdeo-blueviolet)

> Built and maintained by **Satyendra Kumar Namdeo**. See
> [NOTICE.md](NOTICE.md) for the full attribution notice.

## 📌 Overview

A Python port of the original JavaScript/Playwright suite for
**[Darshan Hotel](https://sanflash.github.io/DarshanHotel.com/)**, rebuilt as
a layered, industry-standard **Playwright + Pytest + Allure** framework.

It keeps the original Page Object Model design and covers the same six
modules (Start, Rooms/Services, Food, Gym, Portfolio, Booking, Contact), but
adds:

- **Layered fixtures** — browser/context, page objects, test data, and Allure
  glue each live in their own module under `fixtures/`, not one giant
  `conftest.py`
- **A `utils/` toolkit** — centralized logger, screenshot helper, JSON data
  reader, typed test-data models, explicit-wait helpers
- **Allure reporting** — `allure.step()` for readable test narratives,
  severity/epic/feature/story tagging, automatic failure screenshots, a
  populated Environment tab, and custom failure categories
- **An automatic, animated 3D dashboard** — a real Three.js 3D outcome
  visualization, Chart.js pie/doughnut/bar charts, count-up animations,
  and a filterable results table, generated and opened in your browser
  the instant the suite finishes, no extra command required
- **Data-driven tests** — booking and contact scenarios come from
  `test_data/*.json`, not hardcoded literals
- **Multi-environment config** — `config/environments.yaml` + `.env`
  overrides, switch with `APP_ENV=staging pytest`
- **Two bug fixes** carried over from the original JS version (see below)
- **Docker + Makefile** for reproducible local/CI runs
- A ready-to-use **GitHub Actions** workflow that also builds and uploads the
  Allure HTML report

## 🛠️ Tech Stack

- 🎭 Playwright (Python, sync API) via `pytest-playwright`
- 🐍 Pytest
- 🧱 Page Object Model (POM)
- 📊 Allure (`allure-pytest`) — primary report
- 📄 `pytest-html` — lightweight secondary report
- 🎨 Chart.js + Three.js (vendored) — animated, 3D visual dashboard
- 🔁 `pytest-rerunfailures` — optional flake mitigation
- 🐳 Docker (official Playwright image)

## 📂 Project Structure

```
darshanhotel-playwright-python/
│
├── assets/                      # Vendored front-end assets
│   ├── chart.umd.min.js         # Chart.js — inlined into the dashboard (offline, no CDN)
│   └── three.min.js             # Three.js — powers the 3D outcome skyline
│
├── config/                     # Environment & reporting configuration
│   ├── environments.yaml       # dev / staging / prod base URLs & timeouts
│   ├── settings.py             # loader: env-var > YAML > fallback
│   ├── allure_categories.json  # custom Allure failure categories
│   └── __init__.py             # re-exports settings (backward-compatible)
│
├── fixtures/                   # Pytest fixtures, split by concern
│   ├── browser_fixtures.py     # viewport, timeouts (autouse)
│   ├── page_fixtures.py        # one fixture per Page Object
│   ├── data_fixtures.py        # session-scoped typed datasets
│   ├── allure_fixtures.py      # environment.properties, categories,
│   │                            # auto screenshot-on-failure
│   └── dashboard_fixtures.py   # collects results, auto-builds + opens
│                                # the visual HTML dashboard on session finish
│
├── utils/                      # Reusable framework toolkit
│   ├── logger.py                # console + rotating file logger
│   ├── screenshot_helper.py     # capture + attach to Allure
│   ├── data_reader.py           # load JSON from test_data/
│   ├── models.py                # BookingCase / ContactCase dataclasses
│   ├── wait_helper.py           # named explicit-wait wrappers
│   └── dashboard_generator.py   # builds the colorful HTML dashboard
│
├── pages/                      # Page Object Models
│   ├── base_page.py             # shared click/hover/fill/scroll helpers
│   ├── start_page.py
│   ├── service_page.py          # "Our Services" / Rooms
│   ├── food_service_page.py
│   ├── gym_service_page.py
│   ├── portfolio_page.py
│   ├── book_service_page.py
│   └── contact_page.py
│
├── test_data/                  # Data-driven test inputs
│   ├── booking_data.json
│   └── contact_data.json
│
├── tests/
│   ├── test_start.py           # smoke: home page + rooms
│   ├── test_services.py        # food services
│   ├── test_gym.py
│   ├── test_portfolio.py
│   ├── test_book.py            # data-driven booking
│   └── test_contact.py         # data-driven contact form
│
├── .github/workflows/tests.yml # CI: run suite, build Allure + pytest-html reports
├── conftest.py                  # registers fixtures/, pytest-html hooks
├── Dockerfile
├── Makefile
├── pytest.ini                   # markers, reporting, logging
├── requirements.txt
├── .env.example
├── LICENSE                       # MIT — © Satyendra Kumar Namdeo
├── NOTICE.md                     # authorship notice for the whole project
└── README.md
```

## ⚙️ Setup

```bash
# 1. Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Install browser binaries
playwright install

# (optional) copy the env template if you need to override defaults
cp .env.example .env
```

Or with `make`:

```bash
make install
```

## ▶️ Running Tests

Every invocation — a full run, `--collect-only`, a single `-k` filtered
test — prints an author/project banner first, before collection or any
test executes:

```
===================== Darshan Hotel — Automation Framework =====================
  Author      : Satyendra Kumar Namdeo
  Project     : Darshan Hotel E2E UI Automation
  Framework   : Python + Playwright + Pytest + Allure
  Environment : dev
  Target      : https://sanflash.github.io/DarshanHotel.com/
================================================================================
============================= test session starts ==============================
...
```

```bash
# Run everything (chromium by default)
pytest

# Run a specific module
pytest tests/test_book.py

# Run by marker
pytest -m smoke
pytest -m "regression and booking"

# Run in headed mode, slowed down for debugging
pytest --headed --slowmo 300

# Run against a different browser
pytest --browser firefox
pytest --browser webkit

# Run in parallel
pytest -n auto

# Rerun flaky failures once, with a short delay (pytest-rerunfailures)
pytest --reruns 1 --reruns-delay 2

# Target a different environment (see config/environments.yaml)
APP_ENV=staging pytest
```

Or with `make`:

```bash
make test        # full suite
make smoke        # -m smoke
make regression   # -m regression
```

### Environment overrides

Resolution order: **env var > `config/environments.yaml` > hard-coded
fallback**. Set only what you need to change:

| Variable                     | Default                                            |
|-------------------------------|-----------------------------------------------------|
| `APP_ENV`                     | `dev` (`dev` / `staging` / `prod`)                   |
| `BASE_URL`                    | from `environments.yaml` for the active `APP_ENV`    |
| `DEFAULT_TIMEOUT`              | from `environments.yaml` (`15000`ms in dev)          |
| `DEFAULT_NAVIGATION_TIMEOUT`   | from `environments.yaml` (`30000`ms in dev)          |
| `VIEWPORT_WIDTH` / `HEIGHT`   | `1440` / `900`                                       |

## 📊 Reports & Debugging

### 🎨 Visual Dashboard (automatic, zero setup)

The moment `pytest` finishes — no extra command, no CLI to install — a
colorful, animated, 3D-enhanced HTML dashboard is generated at
**`reports/dashboard.html`** and opened automatically in your default
browser (skipped in CI, where there's no display to open one).

It includes:
- A real, interactive **3D "outcome skyline"** (Three.js) — three lit,
  colored bars sized by pass/fail/skip count, auto-rotating, and
  steerable with your mouse (or drag on touch devices)
- Animated **count-up numbers** on every summary card
- **3D tilt-on-hover** for every card (mouse-tracked perspective effect)
- An animated **circular gauge** for the pass rate
- A **doughnut chart** of pass/fail/skip outcomes and a **pie chart** of
  tests by module, both with elastic-feeling entrance animations
- A **bar chart** of duration per test, with gradient fills, color-coded
  by outcome
- A **filterable results table** (All / Passed / Failed / Skipped buttons)
- A subtly animated gradient header, staggered card entrance animations,
  and a pulsing glow on the Failed card whenever there's at least one
  failure

It's a single self-contained file — Chart.js and Three.js are vendored at
`assets/chart.umd.min.js` and `assets/three.min.js` and inlined directly
into the page, so it renders fully offline with no CDN dependency. If a
browser can't do WebGL, the 3D skyline degrades gracefully to a text
notice — the rest of the dashboard (charts, cards, table) is unaffected.
This dashboard is a fast, visually rich at-a-glance summary; Allure below
remains the full, industry-standard report for deep debugging and
historical trends.

To disable the browser auto-open (e.g. running locally but don't want a
tab popping open every time), set `CI=true` in your shell — the same flag
that already suppresses it in CI.

### Allure (primary, full-featured)

```bash
pytest                                            # writes allure-results/
allure generate allure-results --clean -o allure-report
allure open allure-report
```

Or: `make allure-report` (requires the
[Allure commandline tool](https://allurereport.org/docs/install/) —
`npm install -g allure-commandline`, `brew install allure`, or a Java-based
install, depending on your platform).

The report includes:
- Step-by-step test narratives (`allure.step`) mirroring the original JS
  suite's `test.step()` structure
- Severity, epic/feature/story tagging for filtering and trends
- A populated **Environment** tab (`App Under Test`, `Environment`,
  `Framework`, `Author`)
- Custom **failure categories** (assertion failures, timeouts, locator
  issues) via `config/allure_categories.json`
- An automatic full-page **screenshot attached to every failed test**

### pytest-html (secondary)

A self-contained report also lands at **`reports/report.html`** — useful for
a quick pass/fail glance without the Allure CLI installed.

### Raw failure artifacts

On failure, Playwright saves a screenshot, video, and trace under
`test-results/`:

```bash
playwright show-trace test-results/<test-folder>/trace.zip

```

### Logs

Every run also writes to `logs/automation.log` (rotated at 2MB, 3 backups
kept) via the centralized `utils.logger.get_logger()`.

## 🐳 Docker

```bash
make docker-build
make docker-test
```

Or directly:

```bash
docker build -t darshanhotel-playwright-python .
docker run --rm \
  -v $(pwd)/allure-results:/app/allure-results \
  -v $(pwd)/reports:/app/reports \
  darshanhotel-playwright-python
```

## 🧪 Data-driven testing

`test_book.py` and `test_contact.py` load their cases from
`test_data/*.json` via `utils.data_reader.load_json()`, converted into typed
`BookingCase` / `ContactCase` dataclasses (`utils/models.py`) instead of raw
dicts. Add a new scenario by adding a JSON object — no code changes needed:

```json
{
  "guest_name": "New Guest",
  "guest_email": "new.guest@example.com",
  "check_in": "2026-07-01",
  "check_out": "2026-07-03",
  "room_type_index": 1
}
```

## 🐛 Bugs fixed from the original JS version

| File               | Issue                                                                 | Fix                                                                 |
|--------------------|------------------------------------------------------------------------|------------------------------------------------------------------------|
| `Portfolio.js`     | `title()` called `this.page.tile.hover()` — `tile` doesn't exist, would throw | `hover_section_title()` now hovers the real `section_title` locator     |
| `StartPage.js`     | `scroll()` called `locator.scrollIntoViewIfNeeded()` inside `page.evaluate()` with an undefined `locator` | Replaced with the shared `scroll_into_view()` helper from `BasePage`    |

## 🗺️ Method mapping (JS → Python)

| JS (original)                        | Python (this repo)                              |
|----------------------------------------|--------------------------------------------------|
| `StartPage.goto()`                     | `StartPage.goto()`                                |
| `ServicePage.roomclick()`              | `ServicePage.open_rooms()`                        |
| `ServicePage.hoverAllRooms()`          | `ServicePage.hover_all_rooms()`                   |
| `ServicePage.printRoomNames()`         | `ServicePage.get_room_names()` → returns a list   |
| `FoodService.fodserclick()`            | `FoodServicePage.open_food_section()`             |
| `GymService.gymserclick()`             | `GymServicePage.open_gym_section()`               |
| `Portfolio.portfolclick()`             | `PortfolioPage.open_portfolio()`                  |
| `Portfolio.noa()`                      | `PortfolioPage.open_all_projects()`               |
| `BookService.butclick()`               | `BookServicePage.open_booking_modal()`            |
| `BookService.book(in, out)`            | `BookServicePage.select_dates(in, out)`           |
| `ContactPage.confill()`                | `ContactPage.open_contact_section()`              |
| `ContactPage.conForm()`                | `ContactPage.fill_contact_form(name, email, msg)` |

## 🧠 Design notes

- Locators are carried over unchanged from the original XPath/CSS selectors
  so both suites target the exact same elements.
- Assertions were added deliberately conservatively: only on things
  confirmed by the original DOM structure (heading text, card counts, form
  field values) — nothing was invented about post-submit behaviour that
  wasn't visible in the source project.
- `pytest-playwright` gives every test a fresh, isolated browser context —
  no shared state or session leakage between tests.
- Fixtures are registered as pytest plugins (`pytest_plugins` in
  `conftest.py`) rather than piled into one file — each concern (browser
  config, page objects, test data, Allure) is independently testable and
  readable.
- `wait_helper` functions wrap Playwright's auto-retrying `expect()` API —
  prefer these (or `expect()` directly) over fixed-duration sleeps.

## 🚀 Future Enhancements

- Publish the Allure report to GitHub Pages on every `main` push
- API-level seeding/cleanup if the app grows a backend
- Visual regression checks via Playwright's screenshot assertions

## 👨‍💻 Author

**Satyendra Kumar Namdeo**

This framework — its architecture, page objects, fixtures, utilities,
configuration, test data, and reporting setup — was designed and built by
Satyendra Kumar Namdeo. See [NOTICE.md](NOTICE.md) and [LICENSE](LICENSE)
for the full authorship notice, which also appears at the top of every
source file in this repository (`.py` modules, `pytest.ini`, `Dockerfile`,
`Makefile`, `requirements.txt`, `config/environments.yaml`, the CI
workflow, and both the pytest-html and Allure report metadata).

If you fork or reuse this project, please keep the attribution intact.

