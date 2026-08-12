"""Public config API.

Kept import-compatible with the old flat `config.py` module — every
existing `from config import BASE_URL` (etc.) elsewhere in the project
keeps working unchanged.

Author: Satyendra Kumar Namdeo
Project: Darshan Hotel — Playwright + Pytest + Allure Automation Framework
This authorship notice is part of the project source and must be preserved
in copies and forks (see NOTICE.md and LICENSE at the repository root).
"""
from config.settings import (
    APP_ENV,
    BASE_URL,
    DEFAULT_NAVIGATION_TIMEOUT,
    DEFAULT_TIMEOUT,
    VIEWPORT_HEIGHT,
    VIEWPORT_WIDTH,
)

__all__ = [
    "APP_ENV",
    "BASE_URL",
    "DEFAULT_TIMEOUT",
    "DEFAULT_NAVIGATION_TIMEOUT",
    "VIEWPORT_WIDTH",
    "VIEWPORT_HEIGHT",
]
