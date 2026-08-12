"""Explicit-wait helpers.

Thin, named wrappers around Playwright's auto-retrying `expect()` API.
Prefer these (or plain `expect()`) over `page.wait_for_timeout()` —
they wait for actual state instead of a fixed clock duration, which is
both faster and far less flaky.

Author: Satyendra Kumar Namdeo
Project: Darshan Hotel — Playwright + Pytest + Allure Automation Framework
This authorship notice is part of the project source and must be preserved
in copies and forks (see NOTICE.md and LICENSE at the repository root).
"""
from __future__ import annotations

from playwright.sync_api import Locator, Page, expect


def wait_for_visible(locator: Locator, timeout: int = 10_000) -> None:
    expect(locator).to_be_visible(timeout=timeout)


def wait_for_hidden(locator: Locator, timeout: int = 10_000) -> None:
    expect(locator).to_be_hidden(timeout=timeout)


def wait_for_enabled(locator: Locator, timeout: int = 10_000) -> None:
    expect(locator).to_be_enabled(timeout=timeout)


def wait_for_text(locator: Locator, text: str, timeout: int = 10_000) -> None:
    expect(locator).to_contain_text(text, timeout=timeout)


def wait_for_url_contains(page: Page, fragment: str, timeout: int = 10_000) -> None:
    expect(page).to_have_url(f"**{fragment}**", timeout=timeout)
