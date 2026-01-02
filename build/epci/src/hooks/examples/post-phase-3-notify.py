#!/usr/bin/env python3
# =============================================================================
# Hook: post-phase-3-notify.py
# Description: Send notification when feature is complete
# Type: post-phase-3
#
# Usage:
#   1. Copy or symlink this file to hooks/active/
#   2. Set environment variables for your notification service
#
# Environment Variables:
#   SLACK_WEBHOOK_URL - Slack incoming webhook URL
#   DISCORD_WEBHOOK_URL - Discord webhook URL
#   NOTIFY_EMAIL - Email address (requires sendmail)
#
# Dependencies:
#   - requests (optional, for Slack/Discord)
#   - Standard library only for basic logging
# =============================================================================

import sys
import json
import os
from datetime import datetime


def send_slack_notification(webhook_url: str, message: str) -> bool:
    """Send notification to Slack."""
    try:
        import requests
        response = requests.post(
            webhook_url,
            json={"text": message},
            timeout=10
        )
        return response.status_code == 200
    except ImportError:
        return False
    except Exception:
        return False


def send_discord_notification(webhook_url: str, message: str) -> bool:
    """Send notification to Discord."""
    try:
        import requests
        response = requests.post(
            webhook_url,
            json={"content": message},
            timeout=10
        )
        return response.status_code in (200, 204)
    except ImportError:
        return False
    except Exception:
        return False


def log_to_file(message: str, log_file: str = "epci-notifications.log") -> bool:
    """Log notification to file as fallback."""
    try:
        with open(log_file, 'a') as f:
            timestamp = datetime.now().isoformat()
            f.write(f"[{timestamp}] {message}\n")
        return True
    except Exception:
        return False


def main(context: dict) -> dict:
    """
    Main hook function.

    Args:
        context: Hook context with phase, feature_slug, etc.

    Returns:
        Result dict with status and message
    """
    feature_slug = context.get('feature_slug', 'unknown')
    phase = context.get('phase', 'phase-3')

    # Build notification message
    message = f"EPCI Feature Complete: `{feature_slug}` - Phase {phase} finished successfully"

    notifications_sent = []

    # Try Slack
    slack_url = os.environ.get('SLACK_WEBHOOK_URL')
    if slack_url:
        if send_slack_notification(slack_url, message):
            notifications_sent.append('Slack')

    # Try Discord
    discord_url = os.environ.get('DISCORD_WEBHOOK_URL')
    if discord_url:
        if send_discord_notification(discord_url, message):
            notifications_sent.append('Discord')

    # Always log to file as fallback
    if log_to_file(message):
        notifications_sent.append('File')

    if notifications_sent:
        return {
            "status": "success",
            "message": f"Notified via: {', '.join(notifications_sent)}"
        }
    else:
        return {
            "status": "warning",
            "message": "No notification channels configured or available"
        }


if __name__ == "__main__":
    # Read context from stdin
    try:
        context = json.loads(sys.stdin.read())
    except json.JSONDecodeError:
        context = {}

    result = main(context)
    print(json.dumps(result))
