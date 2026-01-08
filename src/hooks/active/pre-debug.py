#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EPCI Hook: pre-debug

Logs the start of a debug session and loads project context.
Provides environment info and similar past bugs if available.

Usage:
    Automatically executed at the start of /debug command.

Context expected:
    {
        "error": "Error message or description",
        "project_root": "/path/to/project"
    }

Output:
    Returns enriched context for the debug session.
"""

import importlib.util
import json
import os
import sys
from datetime import datetime
from pathlib import Path


def load_project_memory():
    """
    Load project_memory module from project-memory directory.
    Handles the hyphenated directory name by using importlib.
    """
    script_dir = Path(__file__).resolve().parent.parent.parent
    pm_dir = script_dir / "project-memory"

    if not pm_dir.exists():
        pm_dir = Path.cwd() / "src" / "project-memory"

    if not pm_dir.exists():
        return None

    manager_file = pm_dir / "manager.py"
    if not manager_file.exists():
        return None

    spec = importlib.util.spec_from_file_location("project_memory.manager", manager_file)
    manager_module = importlib.util.module_from_spec(spec)
    sys.modules["project_memory.manager"] = manager_module
    spec.loader.exec_module(manager_module)

    return manager_module


def main():
    """Main hook entry point."""
    result = {
        "status": "success",
        "message": "Debug session started",
        "debug_context": {
            "started_at": datetime.now().isoformat(),
        }
    }

    try:
        # Read context from stdin
        context_str = sys.stdin.read()
        context = json.loads(context_str) if context_str.strip() else {}

        error_msg = context.get("error", "Unknown error")
        result["debug_context"]["error_summary"] = error_msg[:200] if len(error_msg) > 200 else error_msg

        # Load project-memory module
        manager_module = load_project_memory()
        if not manager_module:
            result["debug_context"]["memory_available"] = False
            print(json.dumps(result))
            return

        ProjectMemoryManager = manager_module.ProjectMemoryManager

        # Initialize manager
        project_root = context.get("project_root", os.getcwd())
        manager = ProjectMemoryManager(Path(project_root))

        if not manager.is_initialized():
            result["debug_context"]["memory_available"] = False
            result["message"] = "Debug session started (no project memory)"
            print(json.dumps(result))
            return

        result["debug_context"]["memory_available"] = True

        # Load project context
        ctx = manager.load_context()
        result["debug_context"]["project"] = {
            "name": ctx.project.name,
            "stack": ctx.project.stack,
        }

        # Check for similar past bugs
        bugs_dir = Path(project_root) / ".project-memory" / "history" / "bugs"
        if bugs_dir.exists():
            bug_files = list(bugs_dir.glob("*.json"))
            result["debug_context"]["past_bugs_count"] = len(bug_files)

            # Simple keyword matching for similar bugs
            if error_msg and bug_files:
                error_keywords = set(error_msg.lower().split())
                similar_bugs = []

                for bug_file in bug_files[-10:]:  # Check last 10 bugs
                    try:
                        with open(bug_file) as f:
                            bug_data = json.load(f)
                            bug_error = bug_data.get("error", "").lower()
                            bug_keywords = set(bug_error.split())
                            overlap = len(error_keywords & bug_keywords)
                            if overlap >= 2:
                                similar_bugs.append({
                                    "slug": bug_data.get("slug", bug_file.stem),
                                    "mode": bug_data.get("mode", "unknown"),
                                    "date": bug_data.get("resolved_at", "unknown"),
                                })
                    except (json.JSONDecodeError, IOError):
                        continue

                if similar_bugs:
                    result["debug_context"]["similar_bugs"] = similar_bugs[:3]

        result["message"] = f"Debug session started for {ctx.project.name}"

    except json.JSONDecodeError:
        result["status"] = "warning"
        result["message"] = "Invalid JSON context, debug session started anyway"
    except Exception as e:
        result["status"] = "warning"
        result["message"] = f"Debug session started with warning: {e}"

    print(json.dumps(result))


if __name__ == "__main__":
    main()
