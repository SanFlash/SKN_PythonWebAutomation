"""Food Services section.

Author: Satyendra Kumar Namdeo
Project: Darshan Hotel — Playwright + Pytest + Allure Automation Framework
This authorship notice is part of the project source and must be preserved
in copies and forks (see NOTICE.md and LICENSE at the repository root).
"""
from __future__ import annotations

from playwright.sync_api import Page

from pages.base_page import BasePage
from utils.wait_helper import wait_for_visible


class FoodServicePage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.food_heading = page.locator('//h4[normalize-space()="Food Services"]')
        self.food_cards = page.locator('//div[@class="service-card"]')
        self.food_titles = page.locator('//div[@class="service-info"]//h5')

    def open_food_section(self) -> None:
        self.hover(self.food_heading)
        self.click(self.food_heading)

    def hover_all_food_cards(self) -> None:
        self.hover_all(self.food_cards)

    def get_food_names(self) -> list[str]:
        wait_for_visible(self.food_titles.first)
        return self.get_all_texts(self.food_titles)
