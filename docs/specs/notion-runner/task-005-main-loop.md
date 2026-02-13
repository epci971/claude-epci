---
id: task-005
title: Implement main orchestration loop
slug: main-loop
feature: notion-runner
complexity: L
estimated_minutes: 120
dependencies:
  - task-001
  - task-003
  - task-004
files_affected:
  - path: src/openclaw/loop.py
    action: create
  - path: src/openclaw/tests/test_loop.py
    action: create
test_approach: Integration
---

# Task 005: Implement main orchestration loop

## Objective

Implement the main orchestration loop (`loop.py`) that ties all components together: fetch tasks from Notion, select the most eligible, execute via implement-auto, update Notion with results, and repeat. Includes CLI interface, lock file management, recovery at startup, circuit breaker, dry-run mode, and structured logging (US1, US5, US6).

---

## Context

This is the central module of OpenClaw. It orchestrates the full lifecycle:
1. **Startup**: Load config, acquire lock, recover orphaned tasks/worktrees
2. **Loop**: Select next task → set "En cours" → execute → update status → repeat
3. **Shutdown**: Release lock, log summary

Key decisions:
- D4: Recovery at startup (detect orphaned "En cours" tasks)
- D7: Circuit breaker — 3 consecutive failures = automatic stop
- D8: Logging to file + stdout (colored)
- D9: Dry-run mode via `--dry-run` flag
- D11: Worktrees delegated to implement-auto, Python does orphan cleanup only

Dependencies:
- `notion_client.query_database`, `update_page` (task-001)
- `task_selector.select_next_task` (task-003)
- `runner.run_task`, `parse_output`, `result_to_notion_properties` (task-004)

---

## Acceptance Criteria

### AC1: Full execution loop

- **Given**: 3 tasks "A faire" (P0, P1, P2) in Notion
- **When**: `python src/openclaw/loop.py` runs
- **Then**: Tasks execute in order P0 → P1 → P2, each passing through "En cours" → "Termine" in Notion

### AC2: Dry-run mode

- **Given**: `--dry-run` flag is passed
- **When**: loop.py runs
- **Then**: Ordered task list is printed (ID, name, priority, deps) without execution or Notion modifications

### AC3: Circuit breaker

- **Given**: 3 consecutive task failures
- **When**: Circuit breaker checks after 3rd failure
- **Then**: Loop stops with "Circuit breaker triggered: 3 consecutive failures" message and exit code 1

### AC4: Orphaned task recovery

- **Given**: A task with status "En cours" in Notion without active process (previous crash)
- **When**: loop.py starts (startup recovery phase)
- **Then**: Task status is reset to "A faire" in Notion, warning logged

### AC5: Orphaned worktree cleanup

- **Given**: Orphaned git worktrees exist from previous crash
- **When**: loop.py starts
- **Then**: Worktrees are cleaned up via `git worktree prune`, warning logged

### AC6: Lock file prevents concurrent execution

- **Given**: Lock file `/tmp/openclaw.lock` exists with active PID
- **When**: A second instance of loop.py starts
- **Then**: Exits immediately with "Another instance running (PID: {pid})" message

---

## Steps

### Step 1: Implement CLI argument parsing and config loading (20 min)

**Input**: Decision D9 (dry-run), config.py from task-001

**Actions**:
1. Create `loop.py`
2. Implement CLI with argparse:
   - `--dry-run` — preview selection without execution
   - `--config PATH` — config file path (default: `src/openclaw/config.json`)
   - `--max-tasks N` — maximum tasks per run (default: unlimited)
   - `--log-file PATH` — log file path (default: `openclaw.log`)
3. Load config via `config.load_config()`
4. Validate NOTION_API_KEY is set

**Output**: CLI entry point with config loading

**Validation**: `python loop.py --help` shows all options

### Step 2: Implement lock file management (20 min)

**Input**: Decision about concurrent execution prevention

**Actions**:
1. Implement `acquire_lock(lock_path="/tmp/openclaw.lock")`:
   - Check if lock file exists
   - If exists, read PID and check if process is alive (`os.kill(pid, 0)`)
   - If process dead, remove stale lock
   - If process alive, exit with error message
   - Write current PID to lock file
2. Implement `release_lock(lock_path)`:
   - Remove lock file
3. Use atexit to ensure lock is released on exit

**Output**: Lock management functions

**Validation**: Second instance detected correctly

### Step 3: Implement recovery at startup (25 min)

**Input**: Decision D4 (recovery), D11 (worktree delegation)

**Actions**:
1. Implement `recover_orphaned_tasks(notion_client, database_id)`:
   - Query Notion for tasks with Statut="En cours"
   - For each, reset Statut to "A faire", log warning
   - Reset Demarre le to None
2. Implement `cleanup_orphaned_worktrees()`:
   - Run `git worktree list` via subprocess
   - Run `git worktree prune` to clean orphans
   - Log any cleaned worktrees

**Output**: Recovery functions

**Validation**: Orphaned tasks detected and reset

### Step 4: Implement main loop with circuit breaker (30 min)

**Input**: Selector (task-003), runner (task-004), notion_client (task-001)

**Actions**:
1. Implement `main_loop(config, dry_run=False)`:
   - Query all tasks from Notion
   - Call `select_next_task(tasks)` to pick next task
   - If None: log "No eligible tasks remaining", exit 0
   - If dry_run: print task list and exit
   - Set task status to "En cours" + "Demarre le" timestamp
   - Read spec content (Spec Path first, fallback Notion body)
   - Call `runner.run_task(slug, spec_path, flags)`
   - Parse output and map to Notion properties
   - Update Notion with result
   - Circuit breaker: track consecutive_failures
     - If 3 consecutive → log "Circuit breaker triggered", exit 1
     - Reset counter on success
   - Loop back to task selection
2. Handle KeyboardInterrupt for graceful shutdown

**Output**: Main orchestration loop

**Validation**: Full loop with mock components

### Step 5: Implement logging and entry point (25 min)

**Input**: Decision D8 (file + stdout), Python logging module

**Actions**:
1. Configure Python `logging` module:
   - File handler: detailed logs to `openclaw.log`
   - Stream handler: colored output to stdout
   - Format: `[%(asctime)s] %(levelname)s: %(message)s`
2. Implement task header display (like Ralph):
   ```
   ╔══════════════════════════════════════╗
   ║ Task: US-001 — Setup config module  ║
   ║ Priority: P0 | Complexity: Simple   ║
   ╚══════════════════════════════════════╝
   ```
3. Implement run summary at exit:
   - Total tasks processed, succeeded, failed
   - Total duration
   - Exit reason (no tasks / circuit breaker / interrupt)
4. Wire up `if __name__ == "__main__":` entry point

**Output**: Complete loop.py with logging

**Validation**: Full execution with formatted output

---

## Files

| Path | Action | Description |
|------|--------|-------------|
| `src/openclaw/loop.py` | create | Main orchestration loop with CLI, lock, recovery, circuit breaker |
| `src/openclaw/tests/test_loop.py` | create | Integration tests with mocked components |

---

## Test Approach

- **Type**: Integration
- **Framework**: pytest (unittest.mock for Notion API and subprocess)
- **Location**: src/openclaw/tests/test_loop.py
- **Coverage Target**: 80%

### Test Cases

| # | Description | Type | Priority |
|---|-------------|------|----------|
| 1 | Full loop with 3 mock tasks | Integration | High |
| 2 | Dry-run prints task list | Integration | High |
| 3 | Circuit breaker after 3 failures | Integration | High |
| 4 | Orphaned task recovery at startup | Integration | High |
| 5 | Lock file prevents concurrent run | Unit | High |
| 6 | No eligible tasks exits cleanly | Integration | Medium |
| 7 | Graceful shutdown on KeyboardInterrupt | Unit | Medium |
| 8 | Spec Path priority over Notion body | Integration | Medium |

---

## Dependencies

### Requires (blockedBy)

- **task-001**: Needs `query_database`, `update_page` from notion_client
- **task-003**: Needs `select_next_task` from task_selector
- **task-004**: Needs `run_task`, `parse_output`, `result_to_notion_properties` from runner

### Blocks

- **task-007**: Integration tests need the complete loop

---

## Notes

- The spec reading logic (Spec Path vs Notion body) uses `read_page_body` from task-002 as fallback, but this is optional — if task-002 is not yet complete, the runner only uses Spec Path files
- The `--max-tasks` flag is useful for testing (run only 1-2 tasks) and for controlled batching
- Lock file uses PID checking (`os.kill(pid, 0)`) rather than flock for stdlib compatibility

---

*Task specification generated by /spec v1.0 — EPCI v6.0*
