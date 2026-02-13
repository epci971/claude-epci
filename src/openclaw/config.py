"""Configuration module for OpenClaw — JSON config loading and env var management."""

import json
import os
from pathlib import Path

DEFAULTS = {
    "rate_limit_sleep": 0.35,
    "log_level": "INFO",
}


class ConfigError(Exception):
    """Raised when configuration is invalid or missing."""


def get_notion_key() -> str:
    """Read NOTION_API_KEY from environment.

    Returns:
        The API key string.

    Raises:
        ConfigError: If NOTION_API_KEY is not set.
    """
    key = os.environ.get("NOTION_API_KEY")
    if not key:
        raise ConfigError("NOTION_API_KEY not set")
    return key


def load_config(path: str) -> dict:
    """Load JSON config file and apply defaults for optional fields.

    Args:
        path: Path to the JSON config file.

    Returns:
        Config dict with defaults applied.

    Raises:
        ConfigError: If file not found or invalid JSON.
    """
    config_path = Path(path)
    if not config_path.exists():
        raise ConfigError(f"Config file not found: {path}")

    try:
        data = json.loads(config_path.read_text())
    except json.JSONDecodeError as e:
        raise ConfigError(f"Invalid JSON in {path}: {e}") from e

    for key, default in DEFAULTS.items():
        data.setdefault(key, default)

    return data
