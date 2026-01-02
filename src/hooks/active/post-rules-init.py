#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EPCI Hook: post-rules-init

Logs rules generation and updates Project Memory settings after /rules command.
Sets rules_initialized flag to track project rules status.

Usage:
    Automatically active when placed in hooks/active/

Context expected (stdin JSON):
    - project_root: Project root path (optional, defaults to cwd)
    - stacks_detected: List of detected stacks (e.g., ["django", "react"])
    - files_generated: List of generated rule files
    - validation_status: "VALID" | "VALID_WITH_WARNINGS" | "INVALID"
    - token_summary: Dict with token counts per file
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict


def update_project_memory_settings(project_root: Path, context: Dict[str, Any]) -> bool:
    """
    Update .project-memory/settings.json with rules_initialized flag.

    Returns True if settings were updated successfully.
    """
    settings_path = project_root / ".project-memory" / "settings.json"

    if not settings_path.parent.exists():
        # Project Memory not initialized
        return False

    try:
        # Load existing settings or create new
        if settings_path.exists():
            with open(settings_path, "r", encoding="utf-8") as f:
                settings = json.load(f)
        else:
            settings = {}

        # Update rules settings
        settings["rules_initialized"] = True
        settings["rules_generated_at"] = datetime.utcnow().isoformat() + "Z"
        settings["rules_stacks"] = context.get("stacks_detected", [])
        settings["rules_file_count"] = len(context.get("files_generated", []))
        settings["rules_validation"] = context.get("validation_status", "VALID")

        # Write back
        with open(settings_path, "w", encoding="utf-8") as f:
            json.dump(settings, f, indent=2)

        return True

    except Exception:
        return False


def log_rules_generation(context: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generate a structured log entry for rules generation.

    Returns log entry dict.
    """
    return {
        "event": "rules_generated",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "stacks": context.get("stacks_detected", []),
        "files": context.get("files_generated", []),
        "validation": context.get("validation_status", "VALID"),
        "tokens": context.get("token_summary", {}),
        "architecture": context.get("architecture_detected"),
        "conventions": context.get("conventions_detected", []),
    }


def main():
    """
    Main hook entry point.

    Updates Project Memory settings and logs rules generation.
    """
    result = {
        "status": "success",
        "message": "Rules generation logged",
        "details": {}
    }

    try:
        # Read context from stdin
        context_str = sys.stdin.read()
        if not context_str.strip():
            context = {}
        else:
            context = json.loads(context_str)

        # Initialize project root
        project_root = Path(context.get("project_root", os.getcwd()))

        # Update Project Memory settings
        if update_project_memory_settings(project_root, context):
            result["details"]["settings_updated"] = True
            result["details"]["settings_path"] = str(
                project_root / ".project-memory" / "settings.json"
            )
        else:
            result["details"]["settings_updated"] = False
            result["details"]["reason"] = "Project Memory not initialized"

        # Generate log entry
        log_entry = log_rules_generation(context)
        result["details"]["log_entry"] = log_entry

        # Summary
        stacks = context.get("stacks_detected", [])
        files = context.get("files_generated", [])
        validation = context.get("validation_status", "VALID")

        result["message"] = (
            f"Rules logged: {len(files)} files for {', '.join(stacks) if stacks else 'unknown stack'} "
            f"(validation: {validation})"
        )

    except json.JSONDecodeError as e:
        result["status"] = "error"
        result["message"] = f"Invalid JSON context: {e}"
    except Exception as e:
        result["status"] = "warning"
        result["message"] = f"Error in post-rules-init hook: {e}"

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
