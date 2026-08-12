"""Contact Us form.

Author: Satyendra Kumar Namdeo
Project: Darshan Hotel — Playwright + Pytest + Allure Automation Framework
This authorship notice is part of the project source and must be preserved
in copies and forks (see NOTICE.md and LICENSE at the repository root).
"""
from __future__ import annotations

from playwright.sync_api import Page

from pages.base_page import BasePage


class ContactPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.contact_nav_link = page.locator(
            '//a[@class="nav-link" and normalize-space()="Contact Us"]'
        )
        self.section_title = page.locator('//h2[@class="section-title"]')
        self.name_input = page.locator('//input[@type="text"]')
        self.email_input = page.locator('//input[@type="email"]')
        self.message_textarea = page.locator('//textarea[@id="message"]')
        self.send_button = page.locator('//button[@type="submit"]')

    def open_contact_section(self) -> None:
        self.click(self.contact_nav_link)
        self.hover(self.section_title)
        self.click(self.section_title)

    def fill_contact_form(self, name: str, email: str, message: str) -> None:
        self.fill(self.name_input, name)
        self.fill(self.email_input, email)
        self.fill(self.message_textarea, message)

    def send(self) -> None:
        self.click(self.send_button)
