"""Page Object fixtures — one per site module.

Function-scoped: each test gets a fresh instance bound to its own
`page`, which pytest-playwright already isolates per test.

Author: Satyendra Kumar Namdeo
Project: Darshan Hotel — Playwright + Pytest + Allure Automation Framework
This authorship notice is part of the project source and must be preserved
in copies and forks (see NOTICE.md and LICENSE at the repository root).
"""
from __future__ import annotations

import pytest

from pages.book_service_page import BookServicePage
from pages.contact_page import ContactPage
from pages.food_service_page import FoodServicePage
from pages.gym_service_page import GymServicePage
from pages.portfolio_page import PortfolioPage
from pages.service_page import ServicePage
from pages.start_page import StartPage


@pytest.fixture
def start_page(page):
    return StartPage(page)


@pytest.fixture
def service_page(page):
    return ServicePage(page)


@pytest.fixture
def food_service_page(page):
    return FoodServicePage(page)


@pytest.fixture
def gym_service_page(page):
    return GymServicePage(page)


@pytest.fixture
def portfolio_page(page):
    return PortfolioPage(page)


@pytest.fixture
def book_service_page(page):
    return BookServicePage(page)


@pytest.fixture
def contact_page(page):
    return ContactPage(page)
