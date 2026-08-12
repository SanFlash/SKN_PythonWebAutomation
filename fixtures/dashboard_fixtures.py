"""Auto-generated, colorful HTML test dashboard.

Collects each test's outcome, duration, module, and markers during the
run, then — the moment the whole session finishes — renders a
self-contained HTML dashboard (doughnut/pie/bar charts via a vendored
copy of Chart.js, colored summary cards, a filterable results table)
and opens it automatically in the default browser.

This is separate from Allure and pytest-html: those remain the full,
industry-standard reports; this is a fast, colorful, zero-install visual
summary generated automatically on every run — no `allure generate`
step, no manual "open the report" step.

Author: Satyendra Kumar Namdeo
Project: Darshan Hotel — Playwright + Pytest + Allure Automation Framework
This authorship notice is part of the project source and must be preserved
in copies and forks (see NOTICE.md and LICENSE at the repository root).
"""
from __future__ import annotations

import os
import webbrowser
from datetime import datetime
from pathlib import Path
from typing import Any

import pytest

from config import APP_ENV, BASE_URL
from utils.dashboard_generator import build_dashboard_html
from utils.logger import get_logger

logger = get_logger(__name__)

_RESULTS: dict[str, dict[str, Any]] = {}
_REPORTS_DIR = Path("reports")
_DASHBOARD_PATH = _REPORTS_DIR / "dashboard.html"


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Capture the final outcome for every test.

    `call` overwrites an earlier `setup` capture for the same test (the
    normal pass/fail/error case); a `setup` report is kept as-is only
    when the test never reaches the call phase at all (e.g. it's
    skipped, or a fixture errors before the test body runs).
    """
    outcome = yield
    report = outcome.get_result()

    is_relevant_setup = report.when == "setup" and report.outcome in ("failed", "skipped")
    is_call = report.when == "call"

    if is_relevant_setup or is_call:
        module_name = item.module.__name__ if getattr(item, "module", None) else ""
        _RESULTS[item.nodeid] = {
            "name": item.name,
            "nodeid": item.nodeid,
            "module": module_name.rsplit(".", 1)[-1],
            "outcome": report.outcome,
            "duration": round(report.duration, 3),
            "markers": [m.name for m in item.iter_markers() if m.name != "parametrize"],
        }


def pytest_sessionfinish(session, exitstatus):  # noqa: ARG001 - pytest hook signature
    """Build and auto-open the dashboard once the whole suite has finished."""
    if not _RESULTS:
        return

    try:
        _REPORTS_DIR.mkdir(exist_ok=True)
        html = build_dashboard_html(
            results=list(_RESULTS.values()),
            app_env=APP_ENV,
            base_url=BASE_URL,
            generated_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        )
        _DASHBOARD_PATH.write_text(html, encoding="utf-8")
        logger.info("Visual dashboard written to %s", _DASHBOARD_PATH.resolve())
    except Exception as exc:  # noqa: BLE001 - reporting must never break the test run
        logger.warning("Could not generate the visual dashboard: %s", exc)
        return

    # Auto-open locally; skip in CI (no display — opening would just error or hang).
    is_ci = os.getenv("CI", "").strip().lower() in ("1", "true", "yes")
    if is_ci:
        logger.info("CI environment detected — skipping browser auto-open.")
        return

    try:
        webbrowser.open(f"file://{_DASHBOARD_PATH.resolve()}")
    except Exception as exc:  # noqa: BLE001 - best-effort convenience, never fatal
        logger.warning("Could not auto-open the dashboard in a browser: %s", exc)
