"""Gymming / fitness facilities section.

Author: Satyendra Kumar Namdeo
Project: Darshan Hotel — Playwright + Pytest + Allure Automation Framework
This authorship notice is part of the project source and must be preserved
in copies and forks (see NOTICE.md and LICENSE at the repository root).
"""
from __future__ import annotations

from playwright.sync_api import Page

from pages.base_page import BasePage
from utils.wait_helper import wait_for_visible


class GymServicePage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.gym_heading = page.locator('//h4[normalize-space()="Gymming"]')
        self.facility_cards = page.locator('//div[@class="facility-card"]')
        self.facility_titles = page.locator('//div[@class="facility-info"]//h5')

    def open_gym_section(self) -> None:
        self.hover(self.gym_heading)
        self.click(self.gym_heading)

    def hover_all_facility_cards(self) -> None:
        self.hover_all(self.facility_cards)

    def get_facility_names(self) -> list[str]:
        wait_for_visible(self.facility_titles.first)
        return self.get_all_texts(self.facility_titles)
