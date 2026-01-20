#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EPCI Hook: pre-commit-memory

Saves feature history to Project Memory BEFORE the commit decision.
This ensures memory is updated regardless of whether user commits or not.

Unlike post-phase-3-memory-update.py, this hook:
- Does NOT require commit_hash (not available yet)
- Sets pending_commit: true in the feature history
- Will be complemented by post-commit hook if user commits

Usage:
    Activate by symlinking to hooks/active/:
    ln -s ../examples/pre-commit-memory.py hooks/active/

Context expected (stdin JSON):
    - feature_slug: Feature identifier (REQUIRED)
    - project_root: Project root path (optional, defaults to cwd)
    - commit_message: Prepared commit message
    - pending_commit: true (always)
"""

import importlib.util
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional


def find_feature_document(feature_slug: str, project_root: Path) -> Optional[Path]:
    """Find the Feature Document for a given slug."""
    candidates = [
        project_root / "docs" / "features" / f"{feature_slug}.md",
        project_root / f"docs/features/{feature_slug}.md",
        Path.cwd() / "docs" / "features" / f"{feature_slug}.md",
    ]
    for path in candidates:
        if path.exists():
            return path
    return None


def parse_feature_document(doc_path: Path) -> Dict[str, Any]:
    """
    Parse Feature Document to extract information.
    Simplified version for pre-commit context.
    """
    result = {
        "title": "",
        "complexity": "STANDARD",
        "files_modified": [],
        "agents_used": [],
        "estimated_time": None,
    }

    try:
        content = doc_path.read_text(encoding="utf-8")
    except Exception:
        return result

    # Extract title from header
    title_match = re.search(r'^#\s+Feature Document\s*[—–-]\s*(.+)$', content, re.MULTILINE)
    if title_match:
        result["title"] = title_match.group(1).strip()

    # Extract complexity from §1
    complexity_match = re.search(r'\*\*Category\*\*:\s*(\w+)', content, re.IGNORECASE)
    if not complexity_match:
        complexity_match = re.search(r'Category:\s*(\w+)', content, re.IGNORECASE)
    if complexity_match:
        result["complexity"] = complexity_match.group(1).upper()

    # Extract files from §2 table
    files_table = re.findall(
        r'\|\s*`?([^|`]+)`?\s*\|\s*(Create|Modify|Update|Delete)\s*\|',
        content, re.IGNORECASE
    )
    seen_files = set()
    for file_path, action in files_table:
        file_path = file_path.strip()
        if file_path and not file_path.startswith('--') and file_path not in seen_files:
            seen_files.add(file_path)
            result["files_modified"].append(file_path)

    # Extract agent results from §3 Reviews section
    agent_patterns = [
        (r'\*\*@plan-validator\*\*:\s*(\w+)', "plan-validator"),
        (r'\*\*@code-reviewer\*\*:\s*(\w+)', "code-reviewer"),
        (r'\*\*@security-auditor\*\*:\s*(\w+|N/A)', "security-auditor"),
        (r'\*\*@qa-reviewer\*\*:\s*(\w+|N/A)', "qa-reviewer"),
    ]
    for pattern, agent_name in agent_patterns:
        match = re.search(pattern, content)
        if match:
            verdict = match.group(1).strip()
            if verdict.upper() not in ('N/A', 'SKIPPED'):
                result["agents_used"].append(agent_name)

    return result


def load_project_memory():
    """Load project_memory module from project-memory directory."""
    script_dir = Path(__file__).resolve().parent.parent.parent
    pm_dir = script_dir / "project-memory"

    if not pm_dir.exists():
        pm_dir = Path.cwd() / "src" / "project-memory"

    if not pm_dir.exists():
        return None

    init_file = pm_dir / "__init__.py"
    if not init_file.exists():
        return None

    spec = importlib.util.spec_from_file_location("project_memory", init_file,
                                                   submodule_search_locations=[str(pm_dir)])
    module = importlib.util.module_from_spec(spec)
    sys.modules["project_memory"] = module

    manager_file = pm_dir / "manager.py"
    manager_spec = importlib.util.spec_from_file_location("project_memory.manager", manager_file)
    manager_module = importlib.util.module_from_spec(manager_spec)
    sys.modules["project_memory.manager"] = manager_module
    manager_spec.loader.exec_module(manager_module)

    return manager_module


def main():
    """
    Main hook entry point.

    Saves feature history to Project Memory before commit decision.
    Does not require commit_hash - that will be added by post-commit hook.
    """
    result = {
        "status": "success",
        "message": "Feature history prepared in Project Memory (pending commit)",
        "details": {
            "sources": []
        }
    }

    try:
        # Read context from stdin
        context_str = sys.stdin.read()
        if not context_str.strip():
            result["status"] = "warning"
            result["message"] = "No context provided (feature_slug required)"
            print(json.dumps(result))
            return

        context = json.loads(context_str)

        # Extract feature slug (REQUIRED)
        feature_slug = context.get("feature_slug", "")
        if not feature_slug:
            result["status"] = "warning"
            result["message"] = "No feature_slug in context, skipping memory update"
            print(json.dumps(result))
            return

        # Initialize
        project_root = Path(context.get("project_root", os.getcwd()))
        now = datetime.utcnow().isoformat() + "Z"

        # Parse Feature Document
        doc_data = {}
        doc_path = find_feature_document(feature_slug, project_root)
        if doc_path:
            doc_data = parse_feature_document(doc_path)
            result["details"]["sources"].append(f"Feature Document: {doc_path}")

        # Merge data
        title = context.get("feature_title") or doc_data.get("title") or feature_slug.replace("-", " ").title()
        files_modified = context.get("files_modified") or doc_data.get("files_modified") or []
        complexity = context.get("complexity") or doc_data.get("complexity") or "STANDARD"
        agents_used = context.get("agents_used") or doc_data.get("agents_used") or []

        # Load Project Memory
        manager_module = load_project_memory()
        if not manager_module:
            result["status"] = "warning"
            result["message"] = "Project Memory module not found"
            print(json.dumps(result))
            return

        ProjectMemoryManager = manager_module.ProjectMemoryManager
        FeatureHistory = manager_module.FeatureHistory

        manager = ProjectMemoryManager(project_root)

        if not manager.is_initialized():
            result["status"] = "warning"
            result["message"] = "Project Memory not initialized. Run /memory init first."
            print(json.dumps(result))
            return

        # Build Feature History (without commit_hash)
        feature = FeatureHistory(
            slug=feature_slug,
            title=title,
            created_at=context.get("created_at", now),
            completed_at=now,
            complexity=complexity,
            files_modified=files_modified,
            agents_used=agents_used,
            estimated_time=context.get("estimated_time"),
            feature_document=str(doc_path) if doc_path else None,
            commit_hash=None,  # Will be set by post-commit hook
            branch=context.get("branch"),
        )

        # Save to Project Memory
        if manager.save_feature_history(feature):
            result["details"]["feature_saved"] = True
            result["details"]["feature_slug"] = feature_slug
            result["details"]["pending_commit"] = True
            result["message"] = f"Feature '{feature_slug}' prepared in Project Memory (awaiting commit decision)"
        else:
            result["status"] = "warning"
            result["message"] = "Failed to save feature history"

    except json.JSONDecodeError as e:
        result["status"] = "error"
        result["message"] = f"Invalid JSON context: {e}"
    except Exception as e:
        result["status"] = "warning"
        result["message"] = f"Error updating Project Memory: {e}"

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
