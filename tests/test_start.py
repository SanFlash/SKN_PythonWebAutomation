"""Smoke test — landing page loads and the Rooms/Services section works.

Author: Satyendra Kumar Namdeo
Project: Darshan Hotel — Playwright + Pytest + Allure Automation Framework
This authorship notice is part of the project source and must be preserved
in copies and forks (see NOTICE.md and LICENSE at the repository root).
"""
from __future__ import annotations

import allure
import pytest

from utils.logger import get_logger

logger = get_logger(__name__)


@allure.epic("Darshan Hotel")
@allure.feature("Home")
@allure.story("Landing page & Rooms")
@allure.severity(allure.severity_level.BLOCKER)
@pytest.mark.smoke
@pytest.mark.rooms
def test_home_page_loads_and_rooms_are_listed(start_page, service_page):
    with allure.step("Open the home page"):
        start_page.goto()
        title = start_page.get_title()
        logger.info("Page title: %s", title)
        assert title, "Expected the home page to return a non-empty <title>"

    with allure.step("Navigate to the Rooms section under Our Services"):
        service_page.scroll_to_services()
        service_page.open_rooms()
        service_page.hover_all_rooms()

    with allure.step("Verify at least one room card is listed"):
        room_names = service_page.get_room_names()
        logger.info("Rooms discovered: %s", room_names)
        allure.attach("\n".join(room_names), name="Room names", attachment_type=allure.attachment_type.TEXT)
        assert len(room_names) > 0, "Expected at least one room card under the Rooms section"
