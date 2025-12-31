#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EPCI Hook: on-breakpoint-memory-context

Loads Project Memory context at each breakpoint for display in the breakpoint dashboard.
Provides velocity metrics, similar features, and learning status.

Usage:
    Activate by symlinking to hooks/active/:
    ln -s ../examples/on-breakpoint-memory-context.py hooks/active/

Output:
    Returns memory context data for enriched breakpoint display.
"""

import importlib.util
import json
import os
import sys
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
        "message": "Memory context loaded",
        "memory_context": {}
    }

    try:
        # Read context from stdin
        context_str = sys.stdin.read()
        context = json.loads(context_str) if context_str.strip() else {}

        # Load project-memory module
        manager_module = load_project_memory()
        if not manager_module:
            result["status"] = "warning"
            result["message"] = "Project Memory module not found"
            print(json.dumps(result))
            return

        ProjectMemoryManager = manager_module.ProjectMemoryManager

        # Initialize manager
        project_root = context.get("project_root", os.getcwd())
        manager = ProjectMemoryManager(Path(project_root))

        if not manager.is_initialized():
            result["status"] = "warning"
            result["message"] = "Project Memory not initialized"
            result["memory_context"]["initialized"] = False
            print(json.dumps(result))
            return

        memory_ctx = {"initialized": True}

        # Load velocity metrics
        velocity = manager.load_velocity()
        memory_ctx["velocity"] = {
            "total_features": velocity.total_features,
            "trend": velocity.velocity_trend,
            "last_5": velocity.last_5_features[-3:] if velocity.last_5_features else [],
        }

        # Load project context
        ctx = manager.load_context()
        memory_ctx["project"] = {
            "name": ctx.project.name,
            "stack": ctx.project.stack,
            "features_completed": ctx.epci.features_completed,
            "last_session": ctx.epci.last_session,
        }

        # Find similar features if feature_slug provided
        feature_slug = context.get("feature_slug", "")
        if feature_slug:
            keywords = feature_slug.replace("-", " ").split()
            similar = manager.find_similar_features(keywords, threshold=0.2)
            if similar:
                memory_ctx["similar_features"] = [
                    {
                        "slug": s["slug"],
                        "score": round(s["score"] * 100),
                        "complexity": s.get("complexity", "?"),
                    }
                    for s in similar[:3]
                ]

        # Get learning status
        learning = manager.get_learning_status()
        if learning.get("available"):
            memory_ctx["learning"] = {
                "calibration_points": learning.get("calibration", {}).get("total_points", 0),
                "corrections": learning.get("learning", {}).get("total_corrections", 0),
            }

        result["memory_context"] = memory_ctx
        result["message"] = f"Memory loaded: {velocity.total_features} features tracked"

    except json.JSONDecodeError:
        result["status"] = "warning"
        result["message"] = "Invalid JSON context"
    except Exception as e:
        result["status"] = "warning"
        result["message"] = f"Error loading memory: {e}"

    print(json.dumps(result))


if __name__ == "__main__":
    main()
