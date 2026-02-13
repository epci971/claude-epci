---
id: task-007
title: Integration tests and validation
slug: integration-tests
feature: notion-runner
complexity: M
estimated_minutes: 90
dependencies:
  - task-005
  - task-006
files_affected:
  - path: src/openclaw/tests/conftest.py
    action: create
  - path: src/openclaw/tests/test_integration.py
    action: create
  - path: src/openclaw/tests/fixtures/mock_notion_tasks.json
    action: create
  - path: src/openclaw/tests/fixtures/mock_implement_auto_output.json
    action: create
  - path: src/openclaw/tests/fixtures/sample_prd.json
    action: create
test_approach: Integration
---

# Task 007: Integration tests and validation

## Objective

Create comprehensive integration tests that validate the full OpenClaw pipeline: task selection → execution → Notion update (loop flow) and PRD.json → Notion injection (injector flow). Includes a mock urllib framework for Notion API simulation and test fixtures representing realistic data from the OpenClawTasks schema.

---

## Context

Unit tests for individual modules exist in task-001 through task-006. This task adds cross-module integration tests that verify the complete workflows work end-to-end with mocked external dependencies (Notion API, subprocess for Claude CLI).

The test infrastructure uses:
- `unittest.mock.patch` for urllib.request.urlopen
- `conftest.py` for shared fixtures and mock setup
- JSON fixture files for realistic Notion API responses

All tests must run without network access or external dependencies.

---

## Acceptance Criteria

### AC1: Loop integration test

- **Given**: Mock Notion API returning 3 tasks (P0, P1, P2) and mock subprocess for implement-auto
- **When**: Full loop integration test runs
- **Then**: Tasks are selected in priority order, mock-executed, and Notion status updated correctly (A faire → En cours → Termine)

### AC2: PRD injection integration test

- **Given**: A sample PRD.json fixture with 3 tasks and dependencies
- **When**: PRD injection integration test runs with mock Notion API
- **Then**: 3 pages are created, dependency relations are patched, no errors

### AC3: Circuit breaker integration test

- **Given**: Mock subprocess returning FAILED for all executions
- **When**: Loop runs with 3 tasks
- **Then**: Loop stops after 3 consecutive failures with circuit breaker message

---

## Steps

### Step 1: Create test fixtures (20 min)

**Input**: OpenClawTasks schema, implement-auto output schema, PRD v2.0 schema

**Actions**:
1. Create `tests/fixtures/` directory
2. Create `mock_notion_tasks.json`:
   - 3 tasks with varying priorities (P0, P1, P2)
   - 1 blocked task (dependency on another)
   - Realistic OpenClawTasks property structure
   - Includes pagination response format
3. Create `mock_implement_auto_output.json`:
   - SUCCESS result with PR URL, branch, files
   - FAILED result with error message
   - PARTIAL result
4. Create `sample_prd.json`:
   - 3 tasks with dependencies (task-001 → task-002 → task-003)
   - Acceptance criteria in Given-When-Then format
   - Steps with durations

**Output**: Test fixtures directory with JSON files

**Validation**: Fixtures parse correctly as JSON

### Step 2: Create mock urllib framework (25 min)

**Input**: Notion API endpoints used by openclaw modules

**Actions**:
1. Create `conftest.py` with shared fixtures:
   - `mock_notion_api` fixture — patches urllib.request.urlopen
   - Routes requests by URL pattern:
     - POST /databases/{id}/query → mock_notion_tasks.json
     - PATCH /pages/{id} → success response
     - GET /blocks/{id}/children → empty blocks
     - POST /pages → created page response
   - Tracks all API calls for assertion
2. Create `mock_subprocess` fixture:
   - Patches subprocess.run
   - Returns configurable CompletedProcess
   - Creates mock .implement-auto-output.json file
3. Create `mock_config` fixture:
   - Provides test config dict with mock database_id

**Output**: conftest.py with reusable test fixtures

**Validation**: Fixtures integrate correctly with pytest

### Step 3: Write loop integration test (25 min)

**Input**: loop.py from task-005, mock fixtures

**Actions**:
1. Test `test_full_loop_three_tasks`:
   - Setup: 3 mock tasks (P0, P1, P2), mock subprocess returning SUCCESS
   - Assert: Tasks selected in priority order
   - Assert: Notion updates called with correct status transitions
   - Assert: All 3 tasks processed
2. Test `test_loop_circuit_breaker`:
   - Setup: 3 mock tasks, mock subprocess returning FAILED
   - Assert: Loop stops after 3 failures
   - Assert: Exit message contains "Circuit breaker"
3. Test `test_loop_dry_run`:
   - Setup: 3 mock tasks, --dry-run flag
   - Assert: No subprocess calls made
   - Assert: No Notion updates made
   - Assert: Task list printed to stdout
4. Test `test_loop_recovery`:
   - Setup: 1 task with status "En cours" (orphan)
   - Assert: Task reset to "A faire" before main loop starts

**Output**: Loop integration tests

**Validation**: All tests pass

### Step 4: Write PRD injection integration test (20 min)

**Input**: prd_injector.py from task-006, mock fixtures

**Actions**:
1. Test `test_inject_prd_creates_pages`:
   - Setup: sample_prd.json fixture, mock Notion API
   - Assert: create_page called 3 times
   - Assert: Properties mapped correctly (Name, Story ID, Complexite)
   - Assert: Page body contains acceptance criteria
2. Test `test_inject_prd_resolves_dependencies`:
   - Setup: PRD with task-002 depending on task-001
   - Assert: update_page called to patch "Bloque par" relation
3. Test `test_inject_prd_skips_duplicates`:
   - Setup: Story ID already exists in mock database query
   - Assert: Existing task skipped, warning logged

**Output**: PRD injection integration tests

**Validation**: All tests pass

---

## Files

| Path | Action | Description |
|------|--------|-------------|
| `src/openclaw/tests/conftest.py` | create | Shared test fixtures and mock framework |
| `src/openclaw/tests/test_integration.py` | create | Cross-module integration tests |
| `src/openclaw/tests/fixtures/mock_notion_tasks.json` | create | Mock Notion task responses |
| `src/openclaw/tests/fixtures/mock_implement_auto_output.json` | create | Mock implement-auto output |
| `src/openclaw/tests/fixtures/sample_prd.json` | create | Sample PRD.json for injection tests |

---

## Test Approach

- **Type**: Integration
- **Framework**: pytest (unittest.mock, conftest.py fixtures)
- **Location**: src/openclaw/tests/test_integration.py
- **Coverage Target**: 80% (cross-module paths)

### Test Cases

| # | Description | Type | Priority |
|---|-------------|------|----------|
| 1 | Full loop with 3 tasks (success) | Integration | High |
| 2 | Circuit breaker after 3 failures | Integration | High |
| 3 | Dry-run mode (no side effects) | Integration | High |
| 4 | Recovery at startup (orphan reset) | Integration | High |
| 5 | PRD injection creates pages | Integration | High |
| 6 | PRD injection resolves deps | Integration | High |
| 7 | PRD injection skips duplicates | Integration | Medium |

---

## Dependencies

### Requires (blockedBy)

- **task-005**: Needs complete loop.py for loop integration tests
- **task-006**: Needs complete prd_injector.py for injection integration tests

### Blocks

*No other tasks depend on this one — this is the final task*

---

## Notes

- The mock urllib framework should be reusable by all openclaw tests — import from conftest.py
- Integration tests should verify the correct sequence of API calls (e.g., query → update status → execute → update result)
- Test fixtures should match the exact Notion API response format to catch parsing issues

---

*Task specification generated by /spec v1.0 — EPCI v6.0*
