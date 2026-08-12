"""Food Services module.

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
@allure.story("Food Services")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.regression
@pytest.mark.food
def test_food_services_are_listed(start_page, food_service_page):
    with allure.step("Open the home page"):
        start_page.goto()

    with allure.step("Open the Food Services section"):
        food_service_page.open_food_section()
        food_service_page.hover_all_food_cards()

    with allure.step("Verify at least one food service card is listed"):
        food_names = food_service_page.get_food_names()
        logger.info("Food services discovered: %s", food_names)
        allure.attach(
            "\n".join(food_names), name="Food service names", attachment_type=allure.attachment_type.TEXT
        )
        assert len(food_names) > 0, "Expected at least one food service card to be listed"
