"""Root conftest.

Fixtures live in the `fixtures/` package, registered below as pytest
plugins — this keeps browser config, page objects, test data, and Allure
glue each in their own file instead of one growing conftest.py.

This file itself only handles pytest-html reporting concerns (it's a
separate reporting backend from Allure, so its hooks live separately
from `fixtures/allure_fixtures.py`).

Author: Satyendra Kumar Namdeo
Project: Darshan Hotel — Playwright + Pytest + Allure Automation Framework
This authorship notice is part of the project source and must be preserved
in copies and forks (see NOTICE.md and LICENSE at the repository root).
"""
from __future__ import annotations

from pathlib import Path

import pytest
from pytest_metadata.plugin import metadata_key

from config import APP_ENV, BASE_URL
from utils.logger import get_logger

pytest_plugins = [
    "fixtures.browser_fixtures",
    "fixtures.page_fixtures",
    "fixtures.data_fixtures",
    "fixtures.allure_fixtures",
    "fixtures.dashboard_fixtures",
]

logger = get_logger(__name__)


# --------------------------------------------------------------------------- #
# Startup banner — prints before collection/tests run, on every invocation
# --------------------------------------------------------------------------- #
def pytest_sessionstart(session):
    """Print an author/project banner before anything else runs.

    Routed through pytest's own `terminalreporter` plugin (rather than a
    bare `print()`) so it renders correctly regardless of `-q`/`-s`/output
    capturing settings, and fires for every invocation — full runs,
    `--collect-only`, a single `-k` filtered test, all of it.
    """
    terminalreporter = session.config.pluginmanager.get_plugin("terminalreporter")
    if terminalreporter is None:
        return

    terminalreporter.write_sep("=", "Darshan Hotel — Automation Framework")
    terminalreporter.write_line("  Author      : Satyendra Kumar Namdeo", bold=True)
    terminalreporter.write_line("  Project     : Darshan Hotel E2E UI Automation")
    terminalreporter.write_line("  Framework   : Python + Playwright + Pytest + Allure")
    terminalreporter.write_line(f"  Environment : {APP_ENV}")
    terminalreporter.write_line(f"  Target      : {BASE_URL}")
    terminalreporter.write_sep("=")


# --------------------------------------------------------------------------- #
# pytest-html reporting
# --------------------------------------------------------------------------- #
@pytest.hookimpl(trylast=True)
def pytest_configure(config):
    # trylast=True: run after pytest-metadata's own pytest_configure has
    # initialised the metadata stash, so our keys are appended, not wiped.
    # pytest-html 4.x reads from `config.stash[metadata_key]` (pytest-metadata
    # >= 3.0), not the legacy `config._metadata` attribute.
    if metadata_key in config.stash:
        config.stash[metadata_key]["Project"] = "Darshan Hotel — E2E UI Automation"
        config.stash[metadata_key]["App Under Test"] = BASE_URL
        config.stash[metadata_key]["Framework"] = "Python + Playwright + Pytest + Allure"
        config.stash[metadata_key]["Author"] = "Satyendra Kumar Namdeo"
    elif hasattr(config, "_metadata"):
        # Fallback for pytest-metadata < 3.0
        config._metadata["Project"] = "Darshan Hotel — E2E UI Automation"
        config._metadata["App Under Test"] = BASE_URL
        config._metadata["Framework"] = "Python + Playwright + Pytest + Allure"
        config._metadata["Author"] = "Satyendra Kumar Namdeo"


def pytest_html_report_title(report):
    report.title = "Darshan Hotel — Automation Test Report"


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when != "call":
        return

    report.extra = getattr(report, "extra", [])

    if report.failed:
        try:
            from pytest_html import extras

            artifacts_dir = Path("test-results").resolve()
            report.extra.append(
                extras.text(
                    f"Screenshot / video / trace for this run are saved under: "
                    f"{artifacts_dir}. A screenshot is also attached to the "
                    f"Allure report for this test.",
                    name="Artifacts",
                )
            )
        except ImportError:
            # pytest-html not installed — report still works, just without the note.
            pass
