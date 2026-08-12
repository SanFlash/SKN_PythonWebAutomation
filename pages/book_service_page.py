"""Room booking form.

Author: Satyendra Kumar Namdeo
Project: Darshan Hotel — Playwright + Pytest + Allure Automation Framework
This authorship notice is part of the project source and must be preserved
in copies and forks (see NOTICE.md and LICENSE at the repository root).
"""
from __future__ import annotations

from playwright.sync_api import Page

from pages.base_page import BasePage


class BookServicePage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.view_button = page.locator('//button[@data-aos="bounce"]')
        self.section_title = page.locator('//h2[@class="section-title"]')
        self.name_input = page.locator('//input[@id="name"]')
        self.email_input = page.locator('//input[@id="email"]')
        self.check_in_input = page.locator("#checkIn")
        self.check_out_input = page.locator("#checkOut")
        self.room_type_select = page.locator('//select[@id="roomType"]')
        self.book_now_button = page.locator('button:has-text("Book Now")')

    def open_booking_modal(self) -> str:
        self.hover(self.view_button)
        self.click(self.view_button)
        return self.get_text(self.section_title)

    def fill_guest_details(self, name: str, email: str) -> None:
        self.fill(self.name_input, name)
        self.fill(self.email_input, email)

    def select_dates(self, check_in: str, check_out: str) -> None:
        self.fill(self.check_in_input, check_in)
        self.fill(self.check_out_input, check_out)

    def select_room_type(self, index: int = 1) -> None:
        self.room_type_select.select_option(index=index)

    def submit(self) -> None:
        self.click(self.book_now_button)
