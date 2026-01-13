#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EPCI Hook: post-debug

Saves debug session to history and updates metrics.
Creates a record in .project-memory/history/bugs/.

Usage:
    Automatically executed at the end of /debug command.

Context expected:
    {
        "error": "Error message or description",
        "mode": "trivial|quick|complet",
        "success": true|false,
        "cause": "Root cause identified",
        "fix": "Fix description",
        "files_modified": ["path/to/file.ext"],
        "duration_seconds": 120,
        "project_root": "/path/to/project"
    }

Output:
    Returns status of bug record creation.
"""

import importlib.util
import json
import os
import sys
from datetime import datetime
from pathlib import Path
import hashlib


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


def generate_bug_slug(error: str, timestamp: str) -> str:
    """Generate a unique slug for the bug record."""
    # Take first 3 words of error message
    words = error.lower().split()[:3]
    slug_base = "-".join(w for w in words if w.isalnum())[:30]

    # Add short hash for uniqueness
    hash_input = f"{error}{timestamp}"
    short_hash = hashlib.md5(hash_input.encode()).hexdigest()[:6]

    return f"{slug_base}-{short_hash}" if slug_base else f"bug-{short_hash}"


def main():
    """Main hook entry point."""
    result = {
        "status": "success",
        "message": "Debug session recorded",
        "bug_record": {}
    }

    try:
        # Read context from stdin
        context_str = sys.stdin.read()
        context = json.loads(context_str) if context_str.strip() else {}

        # Extract debug session data
        error_msg = context.get("error", "Unknown error")
        mode = context.get("mode", "unknown")
        success = context.get("success", False)
        cause = context.get("cause", "")
        fix = context.get("fix", "")
        files_modified = context.get("files_modified", [])
        duration = context.get("duration_seconds", 0)
        project_root = context.get("project_root", os.getcwd())

        timestamp = datetime.now().isoformat()
        slug = generate_bug_slug(error_msg, timestamp)

        # Build bug record
        bug_record = {
            "slug": slug,
            "error": error_msg[:500],  # Limit error length
            "mode": mode,
            "success": success,
            "cause": cause,
            "fix": fix,
            "files_modified": files_modified,
            "duration_seconds": duration,
            "resolved_at": timestamp,
        }

        result["bug_record"] = {
            "slug": slug,
            "mode": mode,
            "success": success,
        }

        # Save to project memory if available
        bugs_dir = Path(project_root) / ".project-memory" / "history" / "bugs"

        if not bugs_dir.parent.parent.exists():
            result["status"] = "warning"
            result["message"] = "Debug session completed (no project memory to save to)"
            print(json.dumps(result))
            return

        # Create bugs directory if it doesn't exist
        bugs_dir.mkdir(parents=True, exist_ok=True)

        # Save bug record
        bug_file = bugs_dir / f"{slug}.json"
        with open(bug_file, "w") as f:
            json.dump(bug_record, f, indent=2)

        result["bug_record"]["saved_to"] = str(bug_file)

        # Update debug metrics if manager available
        manager_module = load_project_memory()
        if manager_module:
            try:
                ProjectMemoryManager = manager_module.ProjectMemoryManager
                manager = ProjectMemoryManager(Path(project_root))

                if manager.is_initialized():
                    # Try to update metrics (velocity-like tracking for bugs)
                    metrics_file = Path(project_root) / ".project-memory" / "metrics" / "debug.json"
                    metrics_file.parent.mkdir(parents=True, exist_ok=True)

                    if metrics_file.exists():
                        with open(metrics_file) as f:
                            metrics = json.load(f)
                    else:
                        metrics = {
                            "total_bugs": 0,
                            "by_mode": {"trivial": 0, "quick": 0, "complet": 0},
                            "success_rate": 0,
                            "avg_duration_by_mode": {"trivial": 0, "quick": 0, "complet": 0},
                        }

                    # Update metrics
                    metrics["total_bugs"] += 1
                    if mode in metrics["by_mode"]:
                        metrics["by_mode"][mode] += 1

                    # Update average duration
                    if mode in metrics["avg_duration_by_mode"] and duration > 0:
                        count = metrics["by_mode"].get(mode, 1)
                        old_avg = metrics["avg_duration_by_mode"].get(mode, 0)
                        metrics["avg_duration_by_mode"][mode] = int(
                            (old_avg * (count - 1) + duration) / count
                        )

                    # Calculate success rate
                    if metrics["total_bugs"] > 0:
                        # Count successful bugs from history
                        success_count = sum(
                            1 for f in bugs_dir.glob("*.json")
                            if json.load(open(f)).get("success", False)
                        )
                        metrics["success_rate"] = round(
                            success_count / metrics["total_bugs"] * 100, 1
                        )

                    with open(metrics_file, "w") as f:
                        json.dump(metrics, f, indent=2)

                    result["message"] = f"Debug session recorded: {slug} ({mode} mode)"
                    result["bug_record"]["metrics_updated"] = True

            except Exception as e:
                result["bug_record"]["metrics_error"] = str(e)

        if success:
            result["message"] = f"Bug fixed and recorded: {slug}"
        else:
            result["message"] = f"Debug session recorded (unresolved): {slug}"

    except json.JSONDecodeError:
        result["status"] = "error"
        result["message"] = "Invalid JSON context"
    except Exception as e:
        result["status"] = "error"
        result["message"] = f"Error recording debug session: {e}"

    print(json.dumps(result))


if __name__ == "__main__":
    main()
