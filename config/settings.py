"""Environment-aware configuration loader.

Resolution order (highest priority first):
  1. An actual environment variable (e.g. `BASE_URL=... pytest ...`)
  2. The block matching `APP_ENV` in `config/environments.yaml`
  3. A hard-coded fallback (only used if the YAML file is somehow missing)

This is what lets the exact same test suite run against dev, staging, or
prod without touching a single line of code — just `APP_ENV=staging pytest`.

Author: Satyendra Kumar Namdeo
Project: Darshan Hotel — Playwright + Pytest + Allure Automation Framework
This authorship notice is part of the project source and must be preserved
in copies and forks (see NOTICE.md and LICENSE at the repository root).
"""
from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import yaml
from dotenv import load_dotenv

load_dotenv()  # pulls in a local .env file if present; no-op otherwise

_CONFIG_DIR = Path(__file__).resolve().parent
_ENVIRONMENTS_FILE = _CONFIG_DIR / "environments.yaml"

APP_ENV: str = os.getenv("APP_ENV", "dev")


def _load_environment_block(env_name: str) -> dict[str, Any]:
    if not _ENVIRONMENTS_FILE.exists():
        return {}
    with open(_ENVIRONMENTS_FILE, encoding="utf-8") as f:
        all_environments = yaml.safe_load(f) or {}
    if env_name not in all_environments:
        valid = ", ".join(sorted(all_environments)) or "(none defined)"
        raise ValueError(
            f"Unknown APP_ENV='{env_name}'. Valid options in "
            f"environments.yaml: {valid}"
        )
    return all_environments[env_name]


_env_block = _load_environment_block(APP_ENV)

BASE_URL: str = os.getenv(
    "BASE_URL", _env_block.get("base_url", "https://sanflash.github.io/DarshanHotel.com/")
)
DEFAULT_TIMEOUT: int = int(os.getenv("DEFAULT_TIMEOUT", _env_block.get("timeout", 15000)))
DEFAULT_NAVIGATION_TIMEOUT: int = int(
    os.getenv("DEFAULT_NAVIGATION_TIMEOUT", _env_block.get("navigation_timeout", 30000))
)

VIEWPORT_WIDTH: int = int(os.getenv("VIEWPORT_WIDTH", "1440"))
VIEWPORT_HEIGHT: int = int(os.getenv("VIEWPORT_HEIGHT", "900"))
