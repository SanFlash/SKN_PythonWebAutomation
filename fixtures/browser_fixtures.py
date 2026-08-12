"""Browser and context configuration.

Registered as a pytest plugin from the root `conftest.py`
(`pytest_plugins = ["fixtures.browser_fixtures", ...]`).

Author: Satyendra Kumar Namdeo
Project: Darshan Hotel — Playwright + Pytest + Allure Automation Framework
This authorship notice is part of the project source and must be preserved
in copies and forks (see NOTICE.md and LICENSE at the repository root).
"""
from __future__ import annotations

import pytest

from config import (
    DEFAULT_NAVIGATION_TIMEOUT,
    DEFAULT_TIMEOUT,
    VIEWPORT_HEIGHT,
    VIEWPORT_WIDTH,
)


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """Extend pytest-playwright's default context args with our viewport."""
    return {
        **browser_context_args,
        "viewport": {"width": VIEWPORT_WIDTH, "height": VIEWPORT_HEIGHT},
        "ignore_https_errors": True,
    }


@pytest.fixture(autouse=True)
def _configure_timeouts(page):
    """Applied to every test automatically — no need to call it explicitly."""
    page.set_default_timeout(DEFAULT_TIMEOUT)
    page.set_default_navigation_timeout(DEFAULT_NAVIGATION_TIMEOUT)
    yield
