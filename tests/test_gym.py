"""Gymming / fitness facilities module.

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
@allure.feature("Services")
@allure.story("Gym Facilities")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.regression
@pytest.mark.gym
def test_gym_facilities_are_listed(start_page, gym_service_page):
    with allure.step("Open the home page"):
        start_page.goto()

    with allure.step("Open the Gymming section"):
        gym_service_page.open_gym_section()
        gym_service_page.hover_all_facility_cards()

    with allure.step("Verify at least one gym facility card is listed"):
        facility_names = gym_service_page.get_facility_names()
        logger.info("Gym facilities discovered: %s", facility_names)
        allure.attach(
            "\n".join(facility_names), name="Gym facility names", attachment_type=allure.attachment_type.TEXT
        )
        assert len(facility_names) > 0, "Expected at least one gym facility card to be listed"
