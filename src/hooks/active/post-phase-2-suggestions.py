#!/usr/bin/env python3
# =============================================================================
# Hook: post-phase-2-suggestions.py
# Description: Generate proactive suggestions after Phase 2 code review
# Type: post-phase-2
#
# Usage:
#   1. Copy or symlink this file to hooks/active/
#   2. Ensure .project-memory directory exists for learning features
#
# Context received:
#   - feature_slug: Feature identifier
#   - phase: Current phase (phase-2)
#   - files_changed: List of changed files
#   - review_findings: Findings from @code-reviewer, @security-auditor
#
# Returns:
#   - status: success/warning/error
#   - suggestions: List of proactive suggestions to display
#   - message: Summary message
# =============================================================================

import importlib.util
import sys
import json
from pathlib import Path
from typing import Dict, List, Any


def load_project_memory_modules():
    """
    Load project-memory modules using importlib.
    Handles the hyphenated directory name.
    """
    script_dir = Path(__file__).resolve().parent.parent.parent
    pm_dir = script_dir / "project-memory"

    if not pm_dir.exists():
        pm_dir = Path.cwd() / "src" / "project-memory"

    if not pm_dir.exists():
        return None, None

    modules = {}

    # Load suggestion_engine
    se_file = pm_dir / "suggestion_engine.py"
    if se_file.exists():
        spec = importlib.util.spec_from_file_location("suggestion_engine", se_file)
        modules['suggestion_engine'] = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(modules['suggestion_engine'])

    # Load detector
    det_file = pm_dir / "detector.py"
    if det_file.exists():
        spec = importlib.util.spec_from_file_location("detector", det_file)
        modules['detector'] = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(modules['detector'])

    return modules.get('suggestion_engine'), modules.get('detector')


# Try to load modules
suggestion_engine_module, detector_module = load_project_memory_modules()
MODULES_AVAILABLE = suggestion_engine_module is not None


def generate_suggestions(context: dict) -> Dict[str, Any]:
    """
    Generate proactive suggestions based on Phase 2 context.

    Args:
        context: Hook context with review findings and changed files.

    Returns:
        Dictionary with suggestions and metadata.
    """
    if not MODULES_AVAILABLE:
        return {
            "status": "warning",
            "message": "Suggestion modules not available",
            "suggestions": [],
        }

    # Get classes from loaded modules
    SuggestionEngine = suggestion_engine_module.SuggestionEngine
    Finding = suggestion_engine_module.Finding
    findings_from_subagent = suggestion_engine_module.findings_from_subagent

    # Extract context
    files_changed = context.get('files_changed', [])
    review_findings = context.get('review_findings', {})
    project_root = context.get('project_root', '.')
    memory_dir = Path(project_root) / '.project-memory'

    all_findings = []

    # Convert subagent findings
    if 'code-reviewer' in review_findings:
        all_findings.extend(
            findings_from_subagent('code-reviewer', review_findings['code-reviewer'])
        )

    if 'security-auditor' in review_findings:
        all_findings.extend(
            findings_from_subagent('security-auditor', review_findings['security-auditor'])
        )

    if 'qa-reviewer' in review_findings:
        all_findings.extend(
            findings_from_subagent('qa-reviewer', review_findings['qa-reviewer'])
        )

    # Run pattern detector on changed files if available
    if files_changed and detector_module:
        try:
            PatternDetector = detector_module.PatternDetector
            detector = PatternDetector(Path(project_root))
            file_paths = [Path(project_root) / f for f in files_changed]
            existing_files = [f for f in file_paths if f.exists()]
            if existing_files:
                detector_findings = detector.detect_all(existing_files)
                # Convert PatternFinding to Finding
                for pf in detector_findings:
                    all_findings.append(Finding(
                        pattern_id=pf.pattern_id,
                        file_path=pf.file_path,
                        line_number=pf.line_number,
                        message=pf.message,
                        severity=pf.severity,
                        source='detector',
                    ))
        except Exception:
            # Continue without detector findings
            pass

    # Generate suggestions
    engine = SuggestionEngine(memory_dir if memory_dir.exists() else None)
    suggestions = engine.generate_suggestions(
        findings=all_findings,
        context={
            'phase': 'phase-2',
            'files': files_changed,
        },
        max_suggestions=5,
    )

    # Format for output
    formatted_suggestions = [s.to_dict() for s in suggestions]

    # Generate breakpoint format
    breakpoint_output = engine.format_for_breakpoint(suggestions, compact=False)

    return {
        "status": "success" if suggestions else "info",
        "message": f"Generated {len(suggestions)} suggestions",
        "suggestions": formatted_suggestions,
        "breakpoint_output": breakpoint_output,
        "findings_count": len(all_findings),
    }


def main(context: dict) -> dict:
    """
    Main hook function.

    Args:
        context: Hook context from EPCI workflow.

    Returns:
        Result dict with status, suggestions, and message.
    """
    try:
        result = generate_suggestions(context)
        return result
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error generating suggestions: {str(e)}",
            "suggestions": [],
        }


if __name__ == "__main__":
    # Read context from stdin
    try:
        context = json.loads(sys.stdin.read())
    except json.JSONDecodeError:
        context = {}

    result = main(context)
    print(json.dumps(result, indent=2))
