#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EPCI Hook: post-phase-3-memory-update

Automatically saves feature history to Project Memory after Phase 3 completion.
Updates velocity metrics and triggers calibration.

Usage:
    Activate by symlinking to hooks/active/:
    ln -s ../examples/post-phase-3-memory-update.py hooks/active/

Context expected (stdin JSON):
    - feature_slug: Feature identifier
    - files_modified: List of modified files
    - complexity: TINY|SMALL|STANDARD|LARGE
    - estimated_time: Estimated duration (optional)
    - actual_time: Actual duration (optional)
    - test_results: Test execution results (optional)
    - agents_used: List of subagents invoked (optional)
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
    # Find the project-memory directory
    script_dir = Path(__file__).resolve().parent.parent.parent
    pm_dir = script_dir / "project-memory"

    if not pm_dir.exists():
        pm_dir = Path.cwd() / "src" / "project-memory"

    if not pm_dir.exists():
        return None

    # Load the module using importlib
    init_file = pm_dir / "__init__.py"
    if not init_file.exists():
        return None

    spec = importlib.util.spec_from_file_location("project_memory", init_file,
                                                   submodule_search_locations=[str(pm_dir)])
    module = importlib.util.module_from_spec(spec)
    sys.modules["project_memory"] = module

    # Also need to load submodules
    manager_file = pm_dir / "manager.py"
    manager_spec = importlib.util.spec_from_file_location("project_memory.manager", manager_file)
    manager_module = importlib.util.module_from_spec(manager_spec)
    sys.modules["project_memory.manager"] = manager_module
    manager_spec.loader.exec_module(manager_module)

    return manager_module


def main():
    """Main hook entry point."""
    result = {
        "status": "success",
        "message": "Feature history saved to Project Memory",
        "details": {}
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

        # Extract feature data
        feature_slug = context.get("feature_slug", "")
        if not feature_slug:
            result["status"] = "warning"
            result["message"] = "No feature_slug in context, skipping memory update"
            print(json.dumps(result))
            return

        # Load project-memory module
        manager_module = load_project_memory()
        if not manager_module:
            result["status"] = "warning"
            result["message"] = "Project Memory module not found"
            print(json.dumps(result))
            return

        ProjectMemoryManager = manager_module.ProjectMemoryManager
        FeatureHistory = manager_module.FeatureHistory

        # Initialize manager
        project_root = context.get("project_root", os.getcwd())
        manager = ProjectMemoryManager(Path(project_root))

        if not manager.is_initialized():
            result["status"] = "warning"
            result["message"] = "Project Memory not initialized. Run /epci-memory init first."
            print(json.dumps(result))
            return

        # Build feature history
        now = datetime.utcnow().isoformat() + "Z"
        files_modified = context.get("files_modified", [])

        feature = FeatureHistory(
            slug=feature_slug,
            title=context.get("feature_title", feature_slug.replace("-", " ").title()),
            created_at=context.get("created_at", now),
            completed_at=now,
            complexity=context.get("complexity", "STANDARD"),
            complexity_score=context.get("complexity_score", 0.5),
            files_modified=files_modified,
            files_created=context.get("files_created", 0),
            files_updated=context.get("files_updated", len(files_modified)),
            loc_added=context.get("loc_added", 0),
            loc_removed=context.get("loc_removed", 0),
            tests_created=context.get("tests_created", 0),
            test_coverage=context.get("test_coverage"),
            estimated_time=context.get("estimated_time"),
            actual_time=context.get("actual_time"),
            phases={
                "phase_1": context.get("phase_1_completed", now),
                "phase_2": context.get("phase_2_completed", now),
                "phase_3": now,
            },
            agents_used=context.get("agents_used", []),
            issues_found=context.get("issues_found", {}),
            related_features=context.get("related_features", []),
            feature_document=context.get("feature_document"),
            commit_hash=context.get("commit_hash"),
            branch=context.get("branch"),
        )

        # Save feature history
        if manager.save_feature_history(feature):
            result["details"]["feature_saved"] = True
            result["details"]["feature_slug"] = feature_slug
        else:
            result["status"] = "warning"
            result["message"] = "Failed to save feature history"
            print(json.dumps(result))
            return

        # Update velocity metrics
        if manager.update_velocity_from_feature(feature):
            result["details"]["velocity_updated"] = True

        # Trigger calibration if times available
        if feature.estimated_time and feature.actual_time:
            if manager.trigger_calibration(feature):
                result["details"]["calibration_triggered"] = True

        # Update context with features count
        ctx = manager.load_context()
        ctx.epci.features_completed += 1
        ctx.epci.last_session = now
        manager.save_context(ctx)
        result["details"]["features_completed"] = ctx.epci.features_completed

        result["message"] = f"Feature '{feature_slug}' saved to Project Memory (total: {ctx.epci.features_completed})"

    except json.JSONDecodeError as e:
        result["status"] = "error"
        result["message"] = f"Invalid JSON context: {e}"
    except Exception as e:
        result["status"] = "warning"
        result["message"] = f"Error updating Project Memory: {e}"

    print(json.dumps(result))


if __name__ == "__main__":
    main()
