"""Allure reporting glue.

- Writes `allure-results/environment.properties` so the report's
  Environment tab shows what was actually tested (env, base URL, framework).
- Copies the custom failure-category definitions into `allure-results/`
  so `allure generate` picks them up automatically.
- Attaches a full-page screenshot to Allure for every failing test.

Author: Satyendra Kumar Namdeo
Project: Darshan Hotel — Playwright + Pytest + Allure Automation Framework
This authorship notice is part of the project source and must be preserved
in copies and forks (see NOTICE.md and LICENSE at the repository root).
"""
from __future__ import annotations

import shutil
from pathlib import Path

import pytest

from config import APP_ENV, BASE_URL
from utils.logger import get_logger
from utils.screenshot_helper import attach_screenshot

logger = get_logger(__name__)

_ALLURE_RESULTS_DIR = Path("allure-results")
_CATEGORIES_SOURCE = Path(__file__).resolve().parent.parent / "config" / "allure_categories.json"


@pytest.fixture(scope="session", autouse=True)
def _allure_environment_and_categories():
    """Runs once per session: seeds allure-results/ before any test, and
    (re)writes the environment file after the run in case the dir was
    cleared by the `--alluredir` CLI flag mid-session.
    """
    _ALLURE_RESULTS_DIR.mkdir(exist_ok=True)
    _write_environment_properties()
    _copy_categories()

    yield

    _write_environment_properties()
    _copy_categories()


def _write_environment_properties() -> None:
    env_file = _ALLURE_RESULTS_DIR / "environment.properties"
    env_file.write_text(
        "\n".join(
            [
                f"App.Under.Test={BASE_URL}",
                f"Environment={APP_ENV}",
                "Framework=Python + Playwright + Pytest + Allure",
                "Author=Satyendra Kumar Namdeo",
            ]
        )
    )


def _copy_categories() -> None:
    if _CATEGORIES_SOURCE.exists():
        shutil.copy(_CATEGORIES_SOURCE, _ALLURE_RESULTS_DIR / "categories.json")


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        page = item.funcargs.get("page")
        if page is not None:
            attach_screenshot(page, name=f"failure-{item.name}")
        logger.error("Test failed: %s", item.nodeid)
