"""'Our Services' section — Rooms listing.

Author: Satyendra Kumar Namdeo
Project: Darshan Hotel — Playwright + Pytest + Allure Automation Framework
This authorship notice is part of the project source and must be preserved
in copies and forks (see NOTICE.md and LICENSE at the repository root).
"""
from __future__ import annotations

from playwright.sync_api import Page

from pages.base_page import BasePage
from utils.wait_helper import wait_for_visible


class ServicePage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.services_heading = page.locator('//h2[normalize-space()="Our Services"]')
        self.rooms_link = page.locator(
            '//div[@class="service-info"]//h4[normalize-space()="Rooms"]'
        )
        self.room_cards = page.locator('//div[@class="room-card"]')
        self.room_titles = page.locator('//div[@class="room-info"]//h5')

    def scroll_to_services(self) -> None:
        self.scroll_into_view(self.services_heading)

    def open_rooms(self) -> None:
        self.hover(self.rooms_link)
        self.click(self.rooms_link)

    def hover_all_rooms(self) -> None:
        self.hover_all(self.room_cards)

    def get_room_names(self) -> list[str]:
        wait_for_visible(self.room_titles.first)
        return self.get_all_texts(self.room_titles)
