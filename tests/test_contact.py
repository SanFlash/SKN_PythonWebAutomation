"""Contact Us form — data-driven from test_data/contact_data.json.

Author: Satyendra Kumar Namdeo
Project: Darshan Hotel — Playwright + Pytest + Allure Automation Framework
This authorship notice is part of the project source and must be preserved
in copies and forks (see NOTICE.md and LICENSE at the repository root).
"""
from __future__ import annotations

import allure
import pytest

from utils.data_reader import load_json
from utils.logger import get_logger
from utils.models import ContactCase

logger = get_logger(__name__)

CONTACT_CASES = [ContactCase(**case) for case in load_json("contact_data.json")]


@allure.epic("Darshan Hotel")
@allure.feature("Contact")
@allure.story("Contact Us form")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.regression
@pytest.mark.contact
@pytest.mark.parametrize("case", CONTACT_CASES, ids=lambda c: c.name)
def test_contact_form_accepts_valid_message(start_page, contact_page, case: ContactCase):
    with allure.step("Open the home page and the Contact Us section"):
        start_page.goto()
        contact_page.open_contact_section()

    with allure.step(f"Fill the contact form as {case.name}"):
        contact_page.fill_contact_form(name=case.name, email=case.email, message=case.message)

    with allure.step("Verify the form holds what was entered before submitting"):
        assert contact_page.name_input.input_value() == case.name
        assert contact_page.email_input.input_value() == case.email
        assert contact_page.message_textarea.input_value() == case.message

    with allure.step("Submit the contact form"):
        contact_page.send()
        logger.info("Contact form submitted for %s", case.name)
