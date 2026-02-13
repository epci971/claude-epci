"""Tests for config module — load_config and get_notion_key."""

import json
import os

import pytest


def test_get_notion_key_returns_env_value(monkeypatch):
    """AC4: get_notion_key reads NOTION_API_KEY from environment."""
    from openclaw.config import get_notion_key

    monkeypatch.setenv("NOTION_API_KEY", "secret-test-key-123")
    assert get_notion_key() == "secret-test-key-123"


def test_get_notion_key_raises_when_missing(monkeypatch):
    """AC4: ConfigError raised with clear message when key not set."""
    from openclaw.config import ConfigError, get_notion_key

    monkeypatch.delenv("NOTION_API_KEY", raising=False)
    with pytest.raises(ConfigError, match="NOTION_API_KEY not set"):
        get_notion_key()


def test_load_config_reads_json_file(tmp_path):
    """AC5: load_config reads JSON config and returns dict."""
    from openclaw.config import load_config

    config_file = tmp_path / "config.json"
    config_file.write_text(json.dumps({
        "database_id": "abc-123",
        "log_level": "DEBUG",
    }))

    result = load_config(str(config_file))
    assert result["database_id"] == "abc-123"
    assert result["log_level"] == "DEBUG"


def test_load_config_applies_defaults(tmp_path):
    """AC5: Defaults applied for optional fields."""
    from openclaw.config import load_config

    config_file = tmp_path / "config.json"
    config_file.write_text(json.dumps({"database_id": "abc-123"}))

    result = load_config(str(config_file))
    assert result["database_id"] == "abc-123"
    assert result["rate_limit_sleep"] == 0.35
    assert result["log_level"] == "INFO"


def test_load_config_raises_on_missing_file():
    """load_config raises ConfigError for non-existent file."""
    from openclaw.config import ConfigError, load_config

    with pytest.raises(ConfigError, match="Config file not found"):
        load_config("/nonexistent/config.json")


def test_load_config_raises_on_invalid_json(tmp_path):
    """load_config raises ConfigError for malformed JSON."""
    from openclaw.config import ConfigError, load_config

    config_file = tmp_path / "config.json"
    config_file.write_text("not valid json {{{")

    with pytest.raises(ConfigError, match="Invalid JSON"):
        load_config(str(config_file))
