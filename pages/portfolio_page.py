"""Portfolio / gallery section.

Note: the original JS `Portfolio.title()` referenced `this.page.tile`
(undefined) and would have thrown at runtime — `hover_section_title()`
below is the corrected version, wired up to the actual `section_title`
locator.

Author: Satyendra Kumar Namdeo
Project: Darshan Hotel — Playwright + Pytest + Allure Automation Framework
This authorship notice is part of the project source and must be preserved
in copies and forks (see NOTICE.md and LICENSE at the repository root).
"""
from __future__ import annotations

from playwright.sync_api import Page

from pages.base_page import BasePage
from utils.wait_helper import wait_for_visible


class PortfolioPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.portfolio_nav_link = page.locator(
            '//a[@class="nav-link" and text()="Portfolio"]'
        )
        self.footer = page.locator('//footer[text()]')
        self.section_title = page.locator('//h2[@class="section-title"]')
        self.project_cards = page.locator('//div[@class="col"]')
        self.facility_titles = page.locator('//h3[text()]')

    def open_portfolio(self) -> None:
        self.hover(self.portfolio_nav_link)
        self.click(self.portfolio_nav_link)

    def scroll_to_footer(self) -> None:
        self.scroll_into_view(self.footer)

    def hover_section_title(self) -> None:
        self.hover(self.section_title)

    def open_all_projects(self) -> None:
        """Scroll to, hover, and toggle every project card.

        Mirrors the original click-open / click-close interaction pattern,
        with a short pause in between so any open animation settles.
        """
        count = self.project_cards.count()
        for i in range(count):
            card = self.project_cards.nth(i)
            card.scroll_into_view_if_needed()
            card.hover()
            card.click()
            self.wait(1)
            card.click()

    def get_facility_names(self) -> list[str]:
        wait_for_visible(self.facility_titles.first)
        return self.get_all_texts(self.facility_titles)
