"""Screenshot capture, attached directly to the Allure report.

Used both explicitly inside tests (e.g. "attach a screenshot of the
booking confirmation") and automatically by `fixtures/allure_fixtures.py`
whenever a test fails.

Author: Satyendra Kumar Namdeo
Project: Darshan Hotel — Playwright + Pytest + Allure Automation Framework
This authorship notice is part of the project source and must be preserved
in copies and forks (see NOTICE.md and LICENSE at the repository root).
"""
from __future__ import annotations

import allure
from playwright.sync_api import Page

from utils.logger import get_logger

logger = get_logger(__name__)


def attach_screenshot(page: Page, name: str = "screenshot") -> None:
    """Capture a full-page screenshot and attach it to the Allure report.

    Best-effort: a screenshot failure (e.g. page already closed) is logged
    and swallowed rather than masking the real test failure it was meant
    to help debug.
    """
    try:
        screenshot_bytes = page.screenshot(full_page=True)
        allure.attach(
            screenshot_bytes, name=name, attachment_type=allure.attachment_type.PNG
        )
    except Exception as exc:  # noqa: BLE001 - deliberately broad, best-effort capture
        logger.warning("Could not capture/attach screenshot '%s': %s", name, exc)


def attach_text(content: str, name: str = "details") -> None:
    """Attach arbitrary text (e.g. captured console/network logs) to Allure."""
    allure.attach(content, name=name, attachment_type=allure.attachment_type.TEXT)
