"""
Tests for MCP Fallback Module (F12)

Tests fallback strategies, retry behavior, and graceful degradation.
"""

import pytest
from unittest.mock import Mock, call

from ..fallbacks import (
    FallbackStrategy,
    FallbackResult,
    FALLBACK_STRATEGIES,
    get_fallback,
    get_fallback_message,
    get_fallback_description,
    execute_with_fallback,
    FallbackHandler,
)
from ..config import MCPStatus


class TestFallbackStrategies:
    """Tests for fallback strategy constants."""

    def test_context7_fallback(self):
        """Test Context7 uses web search fallback."""
        assert FALLBACK_STRATEGIES["context7"] == FallbackStrategy.WEB_SEARCH

    def test_sequential_fallback(self):
        """Test Sequential uses native reasoning fallback."""
        assert FALLBACK_STRATEGIES["sequential"] == FallbackStrategy.NATIVE_REASONING

    def test_magic_fallback(self):
        """Test Magic uses basic generation fallback."""
        assert FALLBACK_STRATEGIES["magic"] == FallbackStrategy.BASIC_GENERATION

    def test_playwright_fallback(self):
        """Test Playwright uses manual suggestion fallback."""
        assert FALLBACK_STRATEGIES["playwright"] == FallbackStrategy.MANUAL_SUGGESTION


class TestGetFallback:
    """Tests for get_fallback function."""

    def test_get_known_fallback(self):
        """Test getting fallback for known MCP."""
        assert get_fallback("context7") == FallbackStrategy.WEB_SEARCH
        assert get_fallback("sequential") == FallbackStrategy.NATIVE_REASONING

    def test_get_unknown_fallback(self):
        """Test getting fallback for unknown MCP returns SKIP."""
        assert get_fallback("unknown") == FallbackStrategy.SKIP


class TestGetFallbackMessage:
    """Tests for get_fallback_message function."""

    def test_get_message_context7(self):
        """Test fallback message for Context7."""
        message = get_fallback_message("context7")
        assert "Context7" in message
        assert "unreachable" in message

    def test_get_message_sequential(self):
        """Test fallback message for Sequential."""
        message = get_fallback_message("sequential")
        assert "Sequential" in message
        assert "fallback" in message

    def test_get_message_unknown(self):
        """Test fallback message for unknown MCP."""
        message = get_fallback_message("unknown")
        assert "unknown" in message
        assert "unavailable" in message


class TestExecuteWithFallback:
    """Tests for execute_with_fallback function."""

    def test_primary_success(self):
        """Test primary action succeeds."""
        primary = Mock(return_value="success")
        fallback = Mock(return_value="fallback")

        result = execute_with_fallback("context7", primary, fallback)

        assert result.success is True
        assert result.data == "success"
        primary.assert_called_once()
        fallback.assert_not_called()

    def test_primary_fails_fallback_succeeds(self):
        """Test fallback is used when primary fails."""
        primary = Mock(side_effect=Exception("primary failed"))
        fallback = Mock(return_value="fallback_data")

        result = execute_with_fallback("context7", primary, fallback, max_retries=2)

        assert result.success is True
        assert result.data == "fallback_data"
        assert primary.call_count == 3  # 1 initial + 2 retries
        fallback.assert_called_once()

    def test_retry_behavior(self):
        """Test retry happens correct number of times."""
        primary = Mock(side_effect=Exception("fail"))
        on_retry = Mock()

        execute_with_fallback(
            "context7",
            primary,
            max_retries=3,
            on_retry=on_retry,
        )

        # on_retry called for attempts 2, 3, 4 (not the first attempt)
        assert on_retry.call_count == 3

    def test_on_fallback_callback(self):
        """Test on_fallback is called when switching to fallback."""
        primary = Mock(side_effect=Exception("fail"))
        fallback = Mock(return_value="ok")
        on_fallback = Mock()

        execute_with_fallback(
            "context7",
            primary,
            fallback,
            on_fallback=on_fallback,
        )

        on_fallback.assert_called_once()
        # Check the message contains Context7
        call_arg = on_fallback.call_args[0][0]
        assert "Context7" in call_arg

    def test_both_fail(self):
        """Test result when both primary and fallback fail."""
        primary = Mock(side_effect=Exception("primary fail"))
        fallback = Mock(side_effect=Exception("fallback fail"))

        result = execute_with_fallback("context7", primary, fallback)

        assert result.success is False
        assert "fallback fail" in result.message

    def test_no_fallback_action(self):
        """Test result when no fallback action provided."""
        primary = Mock(side_effect=Exception("fail"))

        result = execute_with_fallback("context7", primary, max_retries=1)

        assert result.success is False
        assert "retries" in result.message


class TestFallbackResult:
    """Tests for FallbackResult dataclass."""

    def test_success_result(self):
        """Test successful fallback result."""
        result = FallbackResult(
            success=True,
            strategy=FallbackStrategy.WEB_SEARCH,
            message="completed",
            data={"key": "value"},
        )

        assert result.success is True
        assert result.strategy == FallbackStrategy.WEB_SEARCH
        assert result.data == {"key": "value"}

    def test_failure_result(self):
        """Test failure fallback result."""
        result = FallbackResult(
            success=False,
            strategy=FallbackStrategy.NATIVE_REASONING,
            message="error occurred",
            data=None,
        )

        assert result.success is False
        assert result.data is None


class TestFallbackHandler:
    """Tests for FallbackHandler class."""

    @pytest.fixture
    def handler(self):
        """Create fresh handler."""
        return FallbackHandler()

    def test_record_fallback(self, handler):
        """Test recording fallback occurrence."""
        handler.record_fallback("context7", "timeout")
        handler.record_fallback("context7", "error")

        assert handler.fallback_count["context7"] == 2
        assert len(handler.error_log) == 2

    def test_get_fallback_stats(self, handler):
        """Test getting fallback statistics."""
        handler.record_fallback("context7", "timeout")
        handler.record_fallback("sequential", "error")

        stats = handler.get_fallback_stats()

        assert stats["context7"] == 1
        assert stats["sequential"] == 1

    def test_format_warning(self, handler):
        """Test warning message formatting."""
        warning = handler.format_warning("context7")

        assert "[MCP]" in warning
        assert "Context7" in warning

    def test_format_status_ready(self, handler):
        """Test status formatting for ready server."""
        status = handler.format_status("context7", MCPStatus.READY)

        assert "context7" in status
        assert "ready" in status

    def test_format_status_error(self, handler):
        """Test status formatting for error server."""
        status = handler.format_status("sequential", MCPStatus.ERROR)

        assert "sequential" in status
        assert "error" in status


class TestIntegration:
    """Integration tests for fallback system."""

    def test_full_fallback_flow(self):
        """Test complete fallback flow with handler."""
        handler = FallbackHandler()
        attempts = []

        def primary():
            attempts.append("primary")
            raise Exception("MCP down")

        def fallback():
            attempts.append("fallback")
            return "fallback_result"

        def on_fallback(msg):
            handler.record_fallback("context7", msg)

        result = execute_with_fallback(
            "context7",
            primary,
            fallback,
            max_retries=2,
            on_fallback=on_fallback,
        )

        assert result.success is True
        assert result.data == "fallback_result"
        assert len(attempts) == 4  # 3 primary attempts + 1 fallback
        assert handler.fallback_count["context7"] == 1
