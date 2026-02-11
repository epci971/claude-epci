---
id: task-009
title: Implement dry-run mode and E2E testing
slug: dry-run-e2e
feature: openclaw
complexity: M
estimated_minutes: 90
dependencies:
  - task-006
files_affected:
  - path: pipeline-runner.sh
    action: modify
  - path: run-task.sh
    action: modify
  - path: notify.sh
    action: modify
  - path: tests/e2e-test.sh
    action: create
  - path: tests/fixtures/
    action: create
test_approach: E2E
---

# Task 009: Implement dry-run mode and E2E testing

## Objective

Add `--dry-run` flag to pipeline-runner.sh that simulates the full pipeline without side effects (no Notion updates, no PRs, no notifications), with `[DRY-RUN]` prefix on all logged actions. Create an E2E test harness with mock APIs and fixture data to validate the complete pipeline flow including dependency handling.

---

## Context

Dry-run mode (US3-AC2) is essential for validating the pipeline before production runs. It must exercise the full code path (query, filter, execute) without calling external APIs. The E2E test (Phase 9 in the brief) uses 3-5 mock tasks including one with a dependency to test the full cycle.

Key decisions from brief:
- US3-AC2: --dry-run flag, [DRY-RUN] prefix, no side effects
- Section 10, Phase 9: Test E2E with 3-5 real tasks
- All components must be testable in isolation (dry-run mode)

---

## Acceptance Criteria

### AC1: Dry-run lists tasks without executing

- **Given**: The `--dry-run` flag is passed to pipeline-runner.sh
- **When**: The pipeline runs
- **Then**: Tasks are queried and listed but not executed, no Notion updates are made, no notifications are sent, and all logged actions are prefixed with `[DRY-RUN]`

### AC2: Dry-run exercises full code path

- **Given**: The `--dry-run` flag is active
- **When**: The pipeline runs with tasks available
- **Then**: The lock is acquired/released, health check runs (read-only), tasks are filtered by dependencies, quota is checked, but no Claude Code or git operations happen

### AC3: E2E test validates complete flow

- **Given**: Mock fixture data with 5 tasks (3 ready, 1 blocked, 1 with dependency on a ready task)
- **When**: The E2E test runs with mock APIs
- **Then**: The 3 ready tasks are "executed" (mock), the blocked task is skipped, the dependent task waits, and all expected notifications are sent

---

## Steps

### Step 1: Implement DRY_RUN mode in all scripts (30 min)

**Input**: US3-AC2, all existing scripts

**Actions**:
1. Add `DRY_RUN` environment variable support to all scripts
2. Modify `pipeline-runner.sh`:
   - Parse `--dry-run` flag and export `DRY_RUN=true`
   - In `health_check()`: read-only queries, no Notion updates
   - In task loop: log `[DRY-RUN] Would execute task: {name}` instead of calling run_task
3. Modify `run-task.sh`:
   - If DRY_RUN: skip worktree creation, Claude execution, PR creation
   - Log all would-be actions with `[DRY-RUN]` prefix
4. Modify `notify.sh`:
   - If DRY_RUN: log `[DRY-RUN] Would notify: {message}` instead of calling Telegram API
5. Ensure all Notion write calls check DRY_RUN before executing

**Output**: DRY_RUN mode in all scripts

**Validation**: Pipeline runs end-to-end with --dry-run without any external API calls

### Step 2: Create test fixtures and mock framework (30 min)

**Input**: E2E test requirements, API response formats

**Actions**:
1. Create `tests/fixtures/` directory with:
   - `mock-notion-tasks.json` — 5 tasks with various statuses and dependencies
   - `mock-notion-blocks.json` — Sample page body blocks
   - `mock-implement-auto-result.json` — SUCCESS/PARTIAL/FAILED JSON outputs
   - `mock-projects.json` — Test project configuration
   - `mock.env` — Test environment variables (fake tokens)
2. Create mock API framework in `tests/mock-api.sh`:
   - Override `curl` function to return fixture data based on URL patterns
   - Override `gh` function to simulate PR creation/status
   - Override `claude` function to return mock JSON results
3. Implement `setup_test_env()` and `teardown_test_env()` functions

**Output**: Test fixtures and mock framework

**Validation**: Mock functions return expected data for each API pattern

### Step 3: Create E2E test scenarios (30 min)

**Input**: Full pipeline flow, all edge cases from brief

**Actions**:
1. Create `tests/e2e-test.sh` with test scenarios:
   - **Scenario 1: Happy path** — 3 tasks execute successfully, heartbeat sent
   - **Scenario 2: Dependency handling** — task B blocked by task A, B skipped until A completes
   - **Scenario 3: Circuit breaker** — 3 consecutive failures, pipeline stops
   - **Scenario 4: Kill switch** — /kill message detected, pipeline stops gracefully
   - **Scenario 5: Partial success** — task returns PARTIAL, draft PR created
   - **Scenario 6: Stale lock recovery** — lockfile from dead process cleaned up
2. Each scenario:
   - Sets up fixtures
   - Runs pipeline with mocks
   - Asserts expected outcomes (log patterns, mock API calls, exit codes)
3. Add a `run_all_e2e()` function that runs all scenarios and reports results

**Output**: Complete E2E test suite

**Validation**: All 6 scenarios pass

---

## Files

| Path | Action | Description |
|------|--------|-------------|
| `pipeline-runner.sh` | modify | Add --dry-run flag and DRY_RUN checks |
| `run-task.sh` | modify | Add DRY_RUN checks to skip execution |
| `notify.sh` | modify | Add DRY_RUN checks to skip Telegram calls |
| `tests/e2e-test.sh` | create | E2E test scenarios (6 scenarios) |
| `tests/mock-api.sh` | create | Mock API framework for curl/gh/claude |
| `tests/fixtures/mock-notion-tasks.json` | create | Mock Notion task data |
| `tests/fixtures/mock-notion-blocks.json` | create | Mock Notion page body |
| `tests/fixtures/mock-implement-auto-result.json` | create | Mock Claude Code results |
| `tests/fixtures/mock-projects.json` | create | Mock project configuration |
| `tests/fixtures/mock.env` | create | Mock environment variables |

---

## Test Approach

- **Type**: E2E
- **Framework**: Custom test runner with mock APIs
- **Location**: tests/e2e-test.sh
- **Coverage Target**: 70% (integration-level)

### Test Cases

| # | Description | Type | Priority |
|---|-------------|------|----------|
| 1 | Happy path: 3 tasks succeed, heartbeat sent | E2E | High |
| 2 | Dependency: blocked task skipped | E2E | High |
| 3 | Circuit breaker: 3 failures stop pipeline | E2E | High |
| 4 | Kill switch: pipeline stops gracefully | E2E | High |
| 5 | Partial: draft PR created | E2E | Medium |
| 6 | Stale lock: recovered and cleaned | E2E | Medium |
| 7 | Dry-run: no external calls made | E2E | High |

---

## Dependencies

### Requires (blockedBy)

- **task-006**: Pipeline runner must be complete for E2E testing and dry-run mode

### Blocks

*No other tasks depend on this one*

---

## Notes

- The mock API framework can be reused for future testing of pipeline extensions
- E2E tests should run in under 30 seconds (no real API calls, no real Claude execution)
- Consider adding a `--test-mode` flag that automatically loads mocks (alternative to DRY_RUN)
- The fixture data should be realistic enough to catch edge cases but small enough to be readable

---

*Task specification generated by /spec v1.0 — EPCI v6.0*
