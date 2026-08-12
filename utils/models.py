"""Typed test-data models.

Loading JSON into dataclasses instead of passing raw dicts around gives
IDE autocomplete, catches typos in field names at load time (via
`**dict` unpacking), and makes test signatures self-documenting.

Author: Satyendra Kumar Namdeo
Project: Darshan Hotel — Playwright + Pytest + Allure Automation Framework
This authorship notice is part of the project source and must be preserved
in copies and forks (see NOTICE.md and LICENSE at the repository root).
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class BookingCase:
    guest_name: str
    guest_email: str
    check_in: str
    check_out: str
    room_type_index: int = 1


@dataclass(frozen=True)
class ContactCase:
    name: str
    email: str
    message: str
