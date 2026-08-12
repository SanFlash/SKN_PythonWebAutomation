"""Portfolio / gallery module.

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
@allure.feature("Portfolio")
@allure.story("Gallery browsing")
@allure.severity(allure.severity_level.MINOR)
@pytest.mark.regression
@pytest.mark.portfolio
def test_portfolio_gallery_is_browsable(start_page, portfolio_page):
    with allure.step("Open the home page and navigate to Portfolio"):
        start_page.goto()
        portfolio_page.open_portfolio()

    with allure.step("Scroll through and open every project card"):
        portfolio_page.scroll_to_footer()
        portfolio_page.open_all_projects()
        portfolio_page.scroll_to_footer()

    with allure.step("Verify at least one portfolio item is listed"):
        facility_names = portfolio_page.get_facility_names()
        logger.info("Portfolio items discovered: %s", facility_names)
        allure.attach(
            "\n".join(facility_names), name="Portfolio item names", attachment_type=allure.attachment_type.TEXT
        )
        assert len(facility_names) > 0, "Expected at least one portfolio item to be listed"
