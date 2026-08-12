"""Loads JSON test-data fixtures from the top-level `test_data/` directory.

Keeping data out of test files means the same test can be extended with
new cases by editing a JSON file — no code change needed.

Author: Satyendra Kumar Namdeo
Project: Darshan Hotel — Playwright + Pytest + Allure Automation Framework
This authorship notice is part of the project source and must be preserved
in copies and forks (see NOTICE.md and LICENSE at the repository root).
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

_DATA_DIR = Path(__file__).resolve().parent.parent / "test_data"


def load_json(filename: str) -> Any:
    """Load and parse a JSON file from `test_data/`.

    Raises FileNotFoundError with a clear message if the file is missing,
    rather than a bare traceback deep in `json`.
    """
    path = _DATA_DIR / filename
    if not path.exists():
        raise FileNotFoundError(f"Test data file not found: {path}")
    with open(path, encoding="utf-8") as f:
        return json.load(f)
