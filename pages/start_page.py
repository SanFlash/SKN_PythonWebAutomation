"""Landing page — top navigation and hero sections.

Author: Satyendra Kumar Namdeo
Project: Darshan Hotel — Playwright + Pytest + Allure Automation Framework
This authorship notice is part of the project source and must be preserved
in copies and forks (see NOTICE.md and LICENSE at the repository root).
"""
from __future__ import annotations

from playwright.sync_api import Page

from config import BASE_URL
from pages.base_page import BasePage
from utils.logger import get_logger

logger = get_logger(__name__)


class StartPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.nav = page.locator('//ul[@class="navbar-nav ms-auto"]')
        self.services_heading = page.locator('//h2[text()="Our Services"]')
        self.about_heading = page.locator('//h2[text()="About Us"]')
        self.seasonal_offers_heading = page.locator('//h2[text()="Seasonal Offers"]')
        self.view_offers_btn = page.locator('//button[text()="View Offers"]')
        self.book_now_btn = page.locator('//button[text()="Book Now"]')
        self.follow_us_heading = page.locator('//h2[text()="Follow Us"]')
        self.rooms_heading = page.locator('//h4[text()="Rooms"]')

    def goto(self) -> None:
        logger.info("Navigating to %s", BASE_URL)
        self.page.goto(BASE_URL)

    def get_title(self) -> str:
        return self.page.title()

    def click_rooms(self) -> None:
        self.click(self.rooms_heading)

    def click_book_now(self) -> None:
        self.click(self.book_now_btn)

    def click_view_offers(self) -> None:
        self.click(self.view_offers_btn)
