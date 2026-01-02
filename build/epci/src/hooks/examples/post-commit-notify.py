#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EPCI Hook: post-commit-notify

Sends notifications after a successful git commit.
Only runs when user chooses "Commiter" at the pre-commit breakpoint.

Supported notification channels (via environment variables):
- EPCI_SLACK_WEBHOOK: Slack incoming webhook URL
- EPCI_DISCORD_WEBHOOK: Discord webhook URL
- EPCI_TEAMS_WEBHOOK: Microsoft Teams webhook URL

Usage:
    1. Set environment variable(s) for your notification channel(s)
    2. Activate by symlinking to hooks/active/:
       ln -s ../examples/post-commit-notify.py hooks/active/

Context expected (stdin JSON):
    - feature_slug: Feature identifier (REQUIRED)
    - commit_hash: Git commit hash (REQUIRED)
    - branch: Branch name
    - files_committed: List of committed files
"""

import json
import os
import sys
import urllib.request
import urllib.error
from datetime import datetime
from typing import Any, Dict, List, Optional


def send_slack_notification(webhook_url: str, message: Dict[str, Any]) -> bool:
    """Send notification to Slack."""
    payload = {
        "text": message.get("text", "EPCI Commit"),
        "blocks": [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": f"✅ Feature Committed: {message.get('feature_slug', 'Unknown')}",
                    "emoji": True
                }
            },
            {
                "type": "section",
                "fields": [
                    {"type": "mrkdwn", "text": f"*Commit:*\n`{message.get('commit_hash', 'N/A')}`"},
                    {"type": "mrkdwn", "text": f"*Branch:*\n{message.get('branch', 'N/A')}"},
                ]
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Files:* {message.get('file_count', 0)} files committed"
                }
            }
        ]
    }

    try:
        data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(webhook_url, data=data, headers={'Content-Type': 'application/json'})
        with urllib.request.urlopen(req, timeout=10) as response:
            return response.status == 200
    except Exception:
        return False


def send_discord_notification(webhook_url: str, message: Dict[str, Any]) -> bool:
    """Send notification to Discord."""
    payload = {
        "embeds": [
            {
                "title": f"✅ Feature Committed: {message.get('feature_slug', 'Unknown')}",
                "color": 5763719,  # Green
                "fields": [
                    {"name": "Commit", "value": f"`{message.get('commit_hash', 'N/A')}`", "inline": True},
                    {"name": "Branch", "value": message.get('branch', 'N/A'), "inline": True},
                    {"name": "Files", "value": f"{message.get('file_count', 0)} files", "inline": True},
                ],
                "timestamp": datetime.utcnow().isoformat() + "Z"
            }
        ]
    }

    try:
        data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(webhook_url, data=data, headers={'Content-Type': 'application/json'})
        with urllib.request.urlopen(req, timeout=10) as response:
            return response.status in (200, 204)
    except Exception:
        return False


def send_teams_notification(webhook_url: str, message: Dict[str, Any]) -> bool:
    """Send notification to Microsoft Teams."""
    payload = {
        "@type": "MessageCard",
        "@context": "http://schema.org/extensions",
        "themeColor": "00FF00",
        "summary": f"Feature Committed: {message.get('feature_slug', 'Unknown')}",
        "sections": [
            {
                "activityTitle": f"✅ Feature Committed: {message.get('feature_slug', 'Unknown')}",
                "facts": [
                    {"name": "Commit", "value": message.get('commit_hash', 'N/A')},
                    {"name": "Branch", "value": message.get('branch', 'N/A')},
                    {"name": "Files", "value": f"{message.get('file_count', 0)} files committed"},
                ],
                "markdown": True
            }
        ]
    }

    try:
        data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(webhook_url, data=data, headers={'Content-Type': 'application/json'})
        with urllib.request.urlopen(req, timeout=10) as response:
            return response.status == 200
    except Exception:
        return False


def main():
    """Main hook entry point."""
    result = {
        "status": "success",
        "message": "Post-commit notifications processed",
        "details": {
            "notifications_sent": [],
            "notifications_failed": []
        }
    }

    try:
        # Read context from stdin
        context_str = sys.stdin.read()
        if not context_str.strip():
            result["status"] = "warning"
            result["message"] = "No context provided"
            print(json.dumps(result))
            return

        context = json.loads(context_str)

        # Extract required fields
        feature_slug = context.get("feature_slug", "")
        commit_hash = context.get("commit_hash", "")

        if not commit_hash:
            result["status"] = "warning"
            result["message"] = "No commit_hash in context, skipping notifications"
            print(json.dumps(result))
            return

        # Build message
        message = {
            "feature_slug": feature_slug,
            "commit_hash": commit_hash,
            "branch": context.get("branch", "unknown"),
            "file_count": len(context.get("files_committed", [])),
            "text": f"Feature '{feature_slug}' committed: {commit_hash}"
        }

        # Check for configured webhooks and send notifications
        slack_webhook = os.environ.get("EPCI_SLACK_WEBHOOK")
        discord_webhook = os.environ.get("EPCI_DISCORD_WEBHOOK")
        teams_webhook = os.environ.get("EPCI_TEAMS_WEBHOOK")

        if not any([slack_webhook, discord_webhook, teams_webhook]):
            result["status"] = "success"
            result["message"] = "No notification webhooks configured (set EPCI_SLACK_WEBHOOK, EPCI_DISCORD_WEBHOOK, or EPCI_TEAMS_WEBHOOK)"
            print(json.dumps(result))
            return

        # Send to configured channels
        if slack_webhook:
            if send_slack_notification(slack_webhook, message):
                result["details"]["notifications_sent"].append("slack")
            else:
                result["details"]["notifications_failed"].append("slack")

        if discord_webhook:
            if send_discord_notification(discord_webhook, message):
                result["details"]["notifications_sent"].append("discord")
            else:
                result["details"]["notifications_failed"].append("discord")

        if teams_webhook:
            if send_teams_notification(teams_webhook, message):
                result["details"]["notifications_sent"].append("teams")
            else:
                result["details"]["notifications_failed"].append("teams")

        # Update status based on results
        sent = result["details"]["notifications_sent"]
        failed = result["details"]["notifications_failed"]

        if sent and not failed:
            result["message"] = f"Notifications sent to: {', '.join(sent)}"
        elif sent and failed:
            result["status"] = "warning"
            result["message"] = f"Sent to {', '.join(sent)}, failed for {', '.join(failed)}"
        elif failed:
            result["status"] = "warning"
            result["message"] = f"All notifications failed: {', '.join(failed)}"

    except json.JSONDecodeError as e:
        result["status"] = "error"
        result["message"] = f"Invalid JSON context: {e}"
    except Exception as e:
        result["status"] = "warning"
        result["message"] = f"Error sending notifications: {e}"

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
