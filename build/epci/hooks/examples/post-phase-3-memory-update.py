#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EPCI Hook: post-phase-3-memory-update

Automatically saves feature history to Project Memory after Phase 3 completion.
Auto-extracts rich information from Feature Document and git.

Usage:
    Activate by symlinking to hooks/active/:
    ln -s ../examples/post-phase-3-memory-update.py hooks/active/

Context expected (stdin JSON):
    - feature_slug: Feature identifier (REQUIRED)
    - project_root: Project root path (optional, defaults to cwd)

Auto-extracted data:
    - Feature Document parsing (title, files, agents, phases, issues)
    - Git: commit hash, branch, LOC added/removed
    - Agent results from §3 reviews
"""

import importlib.util
import json
import os
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


# =============================================================================
# AUTO-EXTRACTION: Feature Document Parser
# =============================================================================

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
    Parse Feature Document to extract rich information.

    Returns dict with:
        - title: Feature title from header
        - complexity: Category from §1
        - complexity_score: Score if present
        - files_modified: List from §2 table
        - files_created: Count of Create actions
        - files_updated: Count of Modify actions
        - tasks_total: Total tasks in §2
        - tasks_completed: Completed tasks in §3
        - agents_used: List of agents from §3 Reviews
        - agents_skipped: Agents marked N/A
        - issues_found: Dict with critical/important/minor counts
        - estimated_time: From §2 or §1
        - phases: Dict with phase timestamps
        - acceptance_criteria: Dict of AC statuses
        - commit_hash: From §4
        - key_decisions: List of decisions
        - deviations: List of deviations
    """
    result = {
        "title": "",
        "complexity": "STANDARD",
        "complexity_score": 0.5,
        "files_modified": [],
        "files_created": 0,
        "files_updated": 0,
        "tasks_total": 0,
        "tasks_completed": 0,
        "agents_used": [],
        "agents_skipped": [],
        "issues_found": {"critical": 0, "important": 0, "minor": 0, "details": []},
        "estimated_time": None,
        "phases": {},
        "acceptance_criteria": {},
        "commit_hash": None,
        "key_decisions": [],
        "deviations": [],
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

    # Extract complexity score
    score_match = re.search(r'score[:\s]+(\d+\.?\d*)', content, re.IGNORECASE)
    if score_match:
        try:
            result["complexity_score"] = float(score_match.group(1))
        except ValueError:
            pass

    # Extract files from §2 table (| file | action | risk |)
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
            if action.lower() == 'create':
                result["files_created"] += 1
            else:
                result["files_updated"] += 1

    # Count tasks from §2 ([ ] or [x] patterns)
    tasks_in_plan = re.findall(r'^\s*-?\s*\[[ x]\]\s+', content, re.MULTILINE)
    result["tasks_total"] = len(tasks_in_plan)

    # Count completed tasks from §3
    completed_tasks = re.findall(r'^\s*-?\s*\[x\]\s+', content, re.MULTILINE)
    result["tasks_completed"] = len(completed_tasks)

    # Extract agent results from §3 Reviews section
    agent_patterns = [
        (r'\*\*@plan-validator\*\*:\s*(\w+)', "plan-validator"),
        (r'\*\*@code-reviewer\*\*:\s*(\w+)', "code-reviewer"),
        (r'\*\*@security-auditor\*\*:\s*(\w+|N/A)', "security-auditor"),
        (r'\*\*@qa-reviewer\*\*:\s*(\w+|N/A)', "qa-reviewer"),
        (r'\*\*@doc-generator\*\*:\s*(.+?)(?:\n|$)', "doc-generator"),
    ]
    for pattern, agent_name in agent_patterns:
        match = re.search(pattern, content)
        if match:
            verdict = match.group(1).strip()
            if verdict.upper() in ('N/A', 'SKIPPED'):
                result["agents_skipped"].append({"agent": agent_name, "reason": "Not applicable"})
            else:
                result["agents_used"].append(agent_name)

    # Extract issues found (Critical, Important, Minor)
    issues_match = re.search(
        r'(\d+)\s*Critical.*?(\d+)\s*Important.*?(\d+)\s*Minor',
        content, re.IGNORECASE | re.DOTALL
    )
    if issues_match:
        result["issues_found"]["critical"] = int(issues_match.group(1))
        result["issues_found"]["important"] = int(issues_match.group(2))
        result["issues_found"]["minor"] = int(issues_match.group(3))

    # Extract issue details
    issue_details = re.findall(r'[-•]\s*(.+?(?:\.py|\.js|\.ts|\.md):\d+.+?)(?:\n|$)', content)
    if issue_details:
        result["issues_found"]["details"] = issue_details[:10]  # Limit to 10

    # Extract estimated time (multiple patterns)
    # Pattern 1: Explicit "Estimated time: Xh" or "Time estimate: Xh"
    time_patterns = [
        r'Estimated.*?time.*?:\s*([\d]+h[\d]*(?:min)?)',
        r'Time.*?estimate.*?:\s*([\d]+h[\d]*(?:min)?)',
        r'Duration.*?:\s*([\d]+h[\d]*(?:min)?)',
    ]
    for pattern in time_patterns:
        time_match = re.search(pattern, content, re.IGNORECASE)
        if time_match:
            result["estimated_time"] = time_match.group(1).strip()
            break

    # Pattern 2: Sum wave durations (e.g., "Wave 1: Foundation (35 min)")
    if not result["estimated_time"]:
        wave_times = re.findall(r'Wave\s*\d+[^(]*\((\d+)\s*min', content, re.IGNORECASE)
        if wave_times:
            total_minutes = sum(int(t) for t in wave_times)
            hours = total_minutes // 60
            mins = total_minutes % 60
            if hours > 0:
                result["estimated_time"] = f"{hours}h{mins}min" if mins else f"{hours}h"
            else:
                result["estimated_time"] = f"{mins}min"

    # Extract LOC from Summary table (| Total LOC | ~1595 |)
    loc_match = re.search(r'\|\s*(?:Total\s+)?LOC\s*\|\s*~?(\d+)', content, re.IGNORECASE)
    if loc_match:
        result["loc_total"] = int(loc_match.group(1))

    # Extract LOC added from Files table (| file | LOC |)
    loc_entries = re.findall(r'\|\s*\+?(\d+)\s*\|', content)
    if loc_entries:
        total_loc = sum(int(x) for x in loc_entries if int(x) < 10000)
        if total_loc > 0:
            result["loc_added_from_doc"] = total_loc

    # Extract acceptance criteria
    ac_matches = re.findall(r'\[([x ])\]\s*(AC\d+):\s*(.+?)(?:\n|$)', content, re.IGNORECASE)
    for checked, ac_id, desc in ac_matches:
        result["acceptance_criteria"][ac_id] = {
            "description": desc.strip(),
            "status": "passed" if checked.lower() == 'x' else "pending"
        }

    # Extract commit hash from §4
    commit_match = re.search(r'Commit.*?:\s*`?([a-f0-9]{7,40})`?', content, re.IGNORECASE)
    if commit_match:
        result["commit_hash"] = commit_match.group(1)

    # Extract deviations from §3 table
    deviations = re.findall(
        r'\|\s*#?(\d+|[^|]+)\s*\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|',
        content[content.find("Deviation"):] if "Deviation" in content else ""
    )
    for task, deviation, justification in deviations:
        if deviation.strip() and not deviation.strip().startswith('-'):
            result["deviations"].append({
                "task": task.strip(),
                "deviation": deviation.strip(),
                "justification": justification.strip()
            })

    return result


# =============================================================================
# AUTO-EXTRACTION: Git Information
# =============================================================================

def get_git_info(project_root: Path) -> Dict[str, Any]:
    """
    Extract git information: commit, branch, LOC stats.

    Returns dict with:
        - commit_hash: Current HEAD short hash
        - branch: Current branch name
        - loc_added: Lines added in last commit
        - loc_removed: Lines removed in last commit
        - files_in_commit: List of files in last commit
    """
    result = {
        "commit_hash": None,
        "branch": None,
        "loc_added": 0,
        "loc_removed": 0,
        "files_in_commit": [],
    }

    try:
        # Get current branch
        branch_result = subprocess.run(
            ["git", "branch", "--show-current"],
            capture_output=True, text=True, cwd=project_root
        )
        if branch_result.returncode == 0:
            result["branch"] = branch_result.stdout.strip()

        # Get last commit hash
        hash_result = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            capture_output=True, text=True, cwd=project_root
        )
        if hash_result.returncode == 0:
            result["commit_hash"] = hash_result.stdout.strip()

        # Get LOC stats from last commit
        stat_result = subprocess.run(
            ["git", "diff", "--stat", "HEAD~1..HEAD"],
            capture_output=True, text=True, cwd=project_root
        )
        if stat_result.returncode == 0:
            # Parse the summary line: "X files changed, Y insertions(+), Z deletions(-)"
            summary_match = re.search(
                r'(\d+)\s+files?\s+changed(?:,\s+(\d+)\s+insertions?\(\+\))?(?:,\s+(\d+)\s+deletions?\(-\))?',
                stat_result.stdout
            )
            if summary_match:
                result["loc_added"] = int(summary_match.group(2) or 0)
                result["loc_removed"] = int(summary_match.group(3) or 0)

            # Extract file list
            file_lines = stat_result.stdout.strip().split('\n')[:-1]  # Exclude summary
            for line in file_lines:
                file_match = re.match(r'\s*([^\s|]+)', line)
                if file_match:
                    result["files_in_commit"].append(file_match.group(1))

        # Alternative: get stats from numstat for accuracy
        numstat_result = subprocess.run(
            ["git", "diff", "--numstat", "HEAD~1..HEAD"],
            capture_output=True, text=True, cwd=project_root
        )
        if numstat_result.returncode == 0 and numstat_result.stdout.strip():
            added = 0
            removed = 0
            for line in numstat_result.stdout.strip().split('\n'):
                parts = line.split('\t')
                if len(parts) >= 2:
                    try:
                        added += int(parts[0]) if parts[0] != '-' else 0
                        removed += int(parts[1]) if parts[1] != '-' else 0
                    except ValueError:
                        pass
            if added > 0 or removed > 0:
                result["loc_added"] = added
                result["loc_removed"] = removed

    except FileNotFoundError:
        # Git not available
        pass
    except Exception:
        pass

    return result


# =============================================================================
# PHASE TIMING EXTRACTION
# =============================================================================

def extract_phase_times(doc_content: str, now: str) -> Dict[str, Any]:
    """Extract phase timing information from Feature Document."""
    phases = {}

    # Look for explicit timing in document
    phase_patterns = [
        (r'Phase\s*1.*?completed.*?(\d{4}-\d{2}-\d{2})', "phase_1"),
        (r'Phase\s*2.*?completed.*?(\d{4}-\d{2}-\d{2})', "phase_2"),
        (r'Phase\s*3.*?completed.*?(\d{4}-\d{2}-\d{2})', "phase_3"),
    ]

    for pattern, phase_key in phase_patterns:
        match = re.search(pattern, doc_content, re.IGNORECASE)
        if match:
            phases[phase_key] = {"completed_at": match.group(1)}

    # Default to now for phase_3
    if "phase_3" not in phases:
        phases["phase_3"] = {"completed_at": now}

    return phases


# =============================================================================
# PROJECT MEMORY MODULE LOADER
# =============================================================================

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
    """
    Main hook entry point.

    Auto-extracts rich information from:
    1. Feature Document (docs/features/<slug>.md)
    2. Git (commit, branch, LOC)
    3. Context passed via stdin (overrides auto-extracted)
    """
    result = {
        "status": "success",
        "message": "Feature history saved to Project Memory",
        "details": {
            "auto_extracted": {},
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

        # Initialize project root
        project_root = Path(context.get("project_root", os.getcwd()))
        now = datetime.utcnow().isoformat() + "Z"

        # =====================================================================
        # AUTO-EXTRACTION: Feature Document
        # =====================================================================
        doc_data = {}
        doc_path = find_feature_document(feature_slug, project_root)
        if doc_path:
            doc_data = parse_feature_document(doc_path)
            result["details"]["sources"].append(f"Feature Document: {doc_path}")
            result["details"]["auto_extracted"]["from_document"] = {
                "title": doc_data.get("title"),
                "files_count": len(doc_data.get("files_modified", [])),
                "agents_found": doc_data.get("agents_used", []),
                "issues": doc_data.get("issues_found", {}),
            }

        # =====================================================================
        # AUTO-EXTRACTION: Git Information
        # =====================================================================
        git_data = get_git_info(project_root)
        if git_data.get("commit_hash"):
            result["details"]["sources"].append("Git repository")
            result["details"]["auto_extracted"]["from_git"] = {
                "commit": git_data.get("commit_hash"),
                "branch": git_data.get("branch"),
                "loc_added": git_data.get("loc_added"),
                "loc_removed": git_data.get("loc_removed"),
            }

        # =====================================================================
        # MERGE DATA: Context overrides auto-extracted
        # =====================================================================

        # Title: context > document > slug
        title = context.get("feature_title") or doc_data.get("title") or feature_slug.replace("-", " ").title()

        # Files: context > document > git
        files_modified = (
            context.get("files_modified") or
            doc_data.get("files_modified") or
            git_data.get("files_in_commit") or
            []
        )

        # Complexity: context > document
        complexity = context.get("complexity") or doc_data.get("complexity") or "STANDARD"
        complexity_score = context.get("complexity_score") or doc_data.get("complexity_score") or 0.5

        # LOC: context > document (total or added_from_doc) > git
        loc_added = (
            context.get("loc_added") or
            doc_data.get("loc_total") or
            doc_data.get("loc_added_from_doc") or
            git_data.get("loc_added") or
            0
        )
        loc_removed = context.get("loc_removed") or git_data.get("loc_removed") or 0

        # Files count: context > document
        files_created = context.get("files_created") or doc_data.get("files_created") or 0
        files_updated = context.get("files_updated") or doc_data.get("files_updated") or len(files_modified)

        # Agents: context > document
        agents_used = context.get("agents_used") or doc_data.get("agents_used") or []
        agents_skipped = context.get("agents_skipped") or doc_data.get("agents_skipped") or []

        # Issues: context > document
        issues_found = context.get("issues_found") or doc_data.get("issues_found") or {}

        # Git info: context > git
        commit_hash = context.get("commit_hash") or git_data.get("commit_hash") or doc_data.get("commit_hash")
        branch = context.get("branch") or git_data.get("branch")

        # Time estimates: context > document
        estimated_time = context.get("estimated_time") or doc_data.get("estimated_time")
        actual_time = context.get("actual_time")

        # Acceptance criteria from document
        acceptance_criteria = doc_data.get("acceptance_criteria") or {}

        # Deviations from document
        deviations = doc_data.get("deviations") or []

        # =====================================================================
        # LOAD PROJECT MEMORY
        # =====================================================================
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

        # =====================================================================
        # BUILD FEATURE HISTORY
        # =====================================================================
        feature = FeatureHistory(
            slug=feature_slug,
            title=title,
            created_at=context.get("created_at", now),
            completed_at=now,
            complexity=complexity,
            complexity_score=complexity_score,
            files_modified=files_modified,
            files_created=files_created,
            files_updated=files_updated,
            loc_added=loc_added,
            loc_removed=loc_removed,
            tests_created=context.get("tests_created") or doc_data.get("tasks_completed", 0),
            test_coverage=context.get("test_coverage"),
            estimated_time=estimated_time,
            actual_time=actual_time,
            phases={
                "phase_1": context.get("phase_1_completed", now),
                "phase_2": context.get("phase_2_completed", now),
                "phase_3": now,
            },
            agents_used=agents_used,
            issues_found=issues_found,
            related_features=context.get("related_features", []),
            feature_document=str(doc_path) if doc_path else context.get("feature_document"),
            commit_hash=commit_hash,
            branch=branch,
        )

        # =====================================================================
        # SAVE TO PROJECT MEMORY
        # =====================================================================
        if manager.save_feature_history(feature):
            result["details"]["feature_saved"] = True
            result["details"]["feature_slug"] = feature_slug
            result["details"]["data_summary"] = {
                "title": title,
                "complexity": complexity,
                "files": len(files_modified),
                "loc": f"+{loc_added}/-{loc_removed}",
                "agents": agents_used,
                "commit": commit_hash,
            }
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

        result["message"] = (
            f"Feature '{feature_slug}' saved to Project Memory "
            f"(auto-extracted from {len(result['details']['sources'])} sources, "
            f"total features: {ctx.epci.features_completed})"
        )

    except json.JSONDecodeError as e:
        result["status"] = "error"
        result["message"] = f"Invalid JSON context: {e}"
    except Exception as e:
        result["status"] = "warning"
        result["message"] = f"Error updating Project Memory: {e}"
        import traceback
        result["details"]["traceback"] = traceback.format_exc()

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
