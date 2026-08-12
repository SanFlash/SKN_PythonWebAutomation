"""Room booking form — data-driven from test_data/booking_data.json.

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
from utils.models import BookingCase

logger = get_logger(__name__)

BOOKING_CASES = [BookingCase(**case) for case in load_json("booking_data.json")]


@allure.epic("Darshan Hotel")
@allure.feature("Booking")
@allure.story("Room booking form")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.regression
@pytest.mark.booking
@pytest.mark.parametrize("case", BOOKING_CASES, ids=lambda c: c.guest_name)
def test_booking_form_accepts_valid_details(start_page, book_service_page, case: BookingCase):
    with allure.step("Open the home page and the booking modal"):
        start_page.goto()
        book_service_page.open_booking_modal()

    with allure.step(f"Fill guest details for {case.guest_name}"):
        book_service_page.fill_guest_details(name=case.guest_name, email=case.guest_email)
        book_service_page.select_dates(case.check_in, case.check_out)
        book_service_page.select_room_type(index=case.room_type_index)

    with allure.step("Verify the form holds what was entered before submitting"):
        assert book_service_page.name_input.input_value() == case.guest_name
        assert book_service_page.email_input.input_value() == case.guest_email
        assert book_service_page.check_in_input.input_value() == case.check_in
        assert book_service_page.check_out_input.input_value() == case.check_out

    with allure.step("Submit the booking"):
        book_service_page.submit()
        logger.info(
            "Booking form submitted for %s (%s -> %s)",
            case.guest_name,
            case.check_in,
            case.check_out,
        )
