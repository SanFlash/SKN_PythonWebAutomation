"""Session-scoped test-data fixtures.

For `pytest.mark.parametrize`, data is needed at collection time, so the
test modules import `load_json(...)` directly at module scope for that.
These fixtures are for tests that just need the dataset handed to them
at run time instead (e.g. picking a random or specific case).

Author: Satyendra Kumar Namdeo
Project: Darshan Hotel — Playwright + Pytest + Allure Automation Framework
This authorship notice is part of the project source and must be preserved
in copies and forks (see NOTICE.md and LICENSE at the repository root).
"""
from __future__ import annotations

import pytest

from utils.data_reader import load_json
from utils.models import BookingCase, ContactCase


@pytest.fixture(scope="session")
def booking_dataset() -> list[BookingCase]:
    return [BookingCase(**case) for case in load_json("booking_data.json")]


@pytest.fixture(scope="session")
def contact_dataset() -> list[ContactCase]:
    return [ContactCase(**case) for case in load_json("contact_data.json")]
