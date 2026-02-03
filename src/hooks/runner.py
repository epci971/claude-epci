#!/usr/bin/env python3
"""
EPCI Hooks Runner - Placeholder Implementation

This is a minimal placeholder for the hooks system.
Currently, hooks are logged but not executed.

Future implementation should:
1. Load hook definitions from configuration
2. Execute registered hooks for each event
3. Handle hook failures gracefully
4. Provide feedback to the calling skill

Usage:
    python src/hooks/runner.py <hook-name> --context '<json>'

Example:
    python src/hooks/runner.py post-brainstorm --context '{"slug": "auth-oauth"}'
"""

import argparse
import json
import sys
from datetime import datetime


def log_hook(hook_name: str, context: dict) -> None:
    """Log hook invocation (placeholder for future implementation)."""
    timestamp = datetime.now().isoformat()
    print(f"[HOOK] {timestamp} - {hook_name}")
    print(f"[HOOK] Context: {json.dumps(context, indent=2)}")
    print(f"[HOOK] Status: logged (hooks not yet implemented)")


def main():
    parser = argparse.ArgumentParser(description="EPCI Hooks Runner")
    parser.add_argument("hook_name", help="Name of the hook to execute")
    parser.add_argument(
        "--context",
        type=str,
        default="{}",
        help="JSON context for the hook"
    )

    args = parser.parse_args()

    try:
        context = json.loads(args.context)
    except json.JSONDecodeError as e:
        print(f"[HOOK] Warning: Invalid JSON context: {e}", file=sys.stderr)
        context = {"raw": args.context}

    log_hook(args.hook_name, context)

    # Return success - hooks are logged but not blocking
    return 0


if __name__ == "__main__":
    sys.exit(main())
