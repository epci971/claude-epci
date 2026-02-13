---
id: task-004
title: Implement execution runner (implement-auto subprocess wrapper)
slug: execution-runner
feature: notion-runner
complexity: S
estimated_minutes: 75
dependencies: []
files_affected:
  - path: src/openclaw/runner.py
    action: create
  - path: src/openclaw/tests/test_runner.py
    action: create
test_approach: Unit
---

# Task 004: Implement execution runner (implement-auto subprocess wrapper)

## Objective

Implement the subprocess wrapper that executes implement-auto via `claude --print -p` and parses the JSON output. This module bridges the Python orchestrator to the Claude Code execution engine. It handles invocation, timeout detection, and result-to-Notion-property mapping (decision D3).

---

## Context

Decision D3 establishes implement-auto as the execution engine — the Python runner delegates all implementation work (worktree creation, explore, plan, code, inspect, merge, push, PR) to implement-auto via subprocess.

implement-auto produces a JSON output file at `{worktree}/.implement-auto-output.json` with:
- `status`: SUCCESS | PARTIAL | FAILED
- `pr_url`: GitHub PR URL (if created)
- `branch`: Branch name
- `files_modified`: List of modified files
- `duration_seconds`: Execution duration
- `error`: Error message (if failed)

The runner maps these results to OpenClawTasks Notion properties (Branch, PR URL, Files Modified, Duree, Erreurs, Passes, Auto-merged).

---

## Acceptance Criteria

### AC1: Execute implement-auto via subprocess

- **Given**: A valid spec path and feature slug
- **When**: `run_task(slug, spec_path, flags)` is called
- **Then**: `claude --print -p "/implement-auto {slug} @{spec_path} {flags}"` is executed via subprocess

### AC2: Parse SUCCESS output

- **Given**: implement-auto completes with `status=SUCCESS` and PR URL
- **When**: `parse_output(worktree_path)` is called on `.implement-auto-output.json`
- **Then**: Returns dict with `status="SUCCESS"`, `pr_url`, `branch`, `files_modified`, `duration`

### AC3: Parse FAILED output

- **Given**: implement-auto returns `status=FAILED` with error message
- **When**: `parse_output(worktree_path)` is called
- **Then**: Returns dict with `status="FAILED"`, `error` message

### AC4: Parse PARTIAL output

- **Given**: implement-auto returns `status=PARTIAL`
- **When**: `parse_output(worktree_path)` is called
- **Then**: Returns dict with `status="PARTIAL"`, partial results

### AC5: Map results to Notion properties

- **Given**: A parsed result dict with status, pr_url, branch, files, duration
- **When**: `result_to_notion_properties(result)` is called
- **Then**: Returns Notion-ready properties dict mapping:
  - SUCCESS → Statut="Termine", Passes=True, Branch, PR URL, Files Modified, Duree
  - FAILED → Statut="Echoue", Erreurs=error, Attempts+1
  - PARTIAL → Statut="En review (partiel)", Branch, PR URL

---

## Steps

### Step 1: Implement subprocess wrapper for claude CLI invocation (20 min)

**Input**: implement-auto SKILL.md, decision D3

**Actions**:
1. Ensure `src/openclaw/` package directory exists (create `__init__.py` if not present)
2. Create `runner.py`
3. Implement `run_task(slug, spec_path, flags=None)`:
   - Build command: `claude --dangerously-skip-permissions --print -p "/implement-auto {slug} @{spec_path} {flags}"`
   - Map flags from Notion Flags property:
     - `validate_plan` → `--validate-plan`
     - `with_review` → `--with-review`
     - `no_auto_merge` → (omit `--auto-merge`)
   - Execute via `subprocess.run` with timeout
   - Capture stdout and stderr
   - Return CompletedProcess result

**Output**: `run_task` function

**Validation**: Correct command string built from inputs

### Step 2: Implement output JSON parsing (20 min)

**Input**: implement-auto output schema (references/output-json-schema.md)

**Actions**:
1. Implement `parse_output(worktree_path)`:
   - Read `{worktree_path}/.implement-auto-output.json`
   - Parse JSON and extract: status, pr_url, branch, files_modified, duration_seconds, error
   - Handle missing file (execution crashed before writing output)
   - Handle malformed JSON (partial write)
2. Return structured RunResult dataclass/dict

**Output**: `parse_output` function

**Validation**: Correctly parses sample implement-auto output files

### Step 3: Implement result-to-Notion property mapping (15 min)

**Input**: OpenClawTasks schema, parsed results

**Actions**:
1. Implement `result_to_notion_properties(result, current_attempts=0)`:
   - Map SUCCESS: Statut="Termine", Passes=True, Branch, PR URL, Files Modified (JSON string), Duree, Termine le
   - Map FAILED: Statut="Echoue", Erreurs=error, Attempts=current_attempts+1
   - Map PARTIAL: Statut="En review (partiel)", Branch, PR URL
2. Return dict ready for `update_page()` from task-001

**Output**: Property mapping function

**Validation**: Correct Notion property format for each status

### Step 4: Write unit tests with mock subprocess (20 min)

**Input**: Functions from steps 1-3

**Actions**:
1. Test command construction with various flags
2. Test SUCCESS output parsing
3. Test FAILED output parsing
4. Test PARTIAL output parsing
5. Test missing output file handling
6. Test result-to-Notion mapping for all statuses

**Output**: Complete test file

**Validation**: All tests pass

---

## Files

| Path | Action | Description |
|------|--------|-------------|
| `src/openclaw/runner.py` | create | implement-auto subprocess wrapper |
| `src/openclaw/tests/test_runner.py` | create | Unit tests with mock subprocess |

---

## Test Approach

- **Type**: Unit
- **Framework**: pytest (unittest.mock for subprocess)
- **Location**: src/openclaw/tests/test_runner.py
- **Coverage Target**: 90%

### Test Cases

| # | Description | Type | Priority |
|---|-------------|------|----------|
| 1 | Command construction with flags | Unit | High |
| 2 | Parse SUCCESS output JSON | Unit | High |
| 3 | Parse FAILED output JSON | Unit | High |
| 4 | Parse PARTIAL output JSON | Unit | Medium |
| 5 | Handle missing output file | Unit | High |
| 6 | Handle malformed JSON | Unit | Medium |
| 7 | Result-to-Notion mapping (SUCCESS) | Unit | High |
| 8 | Result-to-Notion mapping (FAILED) | Unit | High |

---

## Dependencies

### Requires (blockedBy)

*No dependencies — this task can start immediately*

### Blocks

- **task-005**: Main loop needs `run_task` and `parse_output` for execution

---

## Notes

- The subprocess wrapper runs `claude --dangerously-skip-permissions --print` to enable headless execution without permission prompts
- Timeout is managed externally by the main loop (task-005) — the runner itself doesn't enforce a timeout
- The `__init__.py` bootstrapping in step 1 ensures this task can run in parallel with task-001 (Wave 1)

---

*Task specification generated by /spec v1.0 — EPCI v6.0*
