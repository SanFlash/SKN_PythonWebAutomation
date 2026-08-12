"""Base Page Object.

Every page class inherits from `BasePage`, which wraps the handful of
Playwright actions used across the whole suite (click, hover, fill,
read text, scroll, hover-all). Keeping these in one place means a
behavioural fix (e.g. how we scroll, how we read text) only has to be
made once.

Page-specific logic and locators belong in the subclasses, not here.

Author: Satyendra Kumar Namdeo
Project: Darshan Hotel — Playwright + Pytest + Allure Automation Framework
This authorship notice is part of the project source and must be preserved
in copies and forks (see NOTICE.md and LICENSE at the repository root).
"""
from __future__ import annotations

import logging

from playwright.sync_api import Locator, Page

logger = logging.getLogger(__name__)


class BasePage:
    def __init__(self, page: Page) -> None:
        self.page = page

    # --- basic interactions -------------------------------------------------
    def click(self, locator: Locator) -> None:
        locator.click()

    def hover(self, locator: Locator) -> None:
        locator.hover()

    def fill(self, locator: Locator, value: str) -> None:
        locator.fill(value)

    # --- reading ---------------------------------------------------------
    def get_text(self, locator: Locator) -> str:
        return (locator.text_content() or "").strip()

    def get_all_texts(self, locator: Locator) -> list[str]:
        """Return the trimmed text of every element matched by `locator`."""
        return [text.strip() for text in locator.all_text_contents() if text.strip()]

    # --- scrolling / hovering over collections ----------------------------
    def scroll_into_view(self, locator: Locator) -> None:
        locator.scroll_into_view_if_needed()

    def hover_all(self, locator: Locator) -> None:
        """Scroll to and hover every element matched by `locator`.

        Useful for cards/tiles whose content or animation only renders
        once they've been scrolled into view (AOS-style animations).
        """
        count = locator.count()
        for i in range(count):
            item = locator.nth(i)
            item.scroll_into_view_if_needed()
            item.hover()

    # --- waiting -----------------------------------------------------------
    def wait(self, seconds: float) -> None:
        """Explicit wait. Used sparingly — only where the UI genuinely needs
        a beat (e.g. a hover-triggered CSS transition) and there's no
        reliable state/assertion to wait on instead.
        """
        self.page.wait_for_timeout(seconds * 1000)
