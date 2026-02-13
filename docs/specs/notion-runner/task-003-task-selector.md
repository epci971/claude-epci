---
id: task-003
title: Implement task selector with priority and dependency resolution
slug: task-selector
feature: notion-runner
complexity: M
estimated_minutes: 90
dependencies:
  - task-001
files_affected:
  - path: src/openclaw/task_selector.py
    action: create
  - path: src/openclaw/tests/test_task_selector.py
    action: create
test_approach: Unit
---

# Task 003: Implement task selector with priority and dependency resolution

## Objective

Implement the task selection algorithm that determines which Notion task to execute next. The selector filters eligible tasks (status "A faire"), sorts by priority (P0 > P1 > P2 > P3), resolves dependencies via "Bloque par" relations, and detects circular dependencies. This is the brain of the orchestrator (US2).

---

## Context

The OpenClawTasks Notion database has:
- **Statut** select with options: A faire, Bloque, En cours, En review, En review (partiel), Echoue, Termine
- **Priorite** select with options: P0, P1, P2, P3
- **Bloque par** relation (bidirectional) to self — tasks this task depends on
- **Story ID** text — used as tiebreaker for equal priority

The selector uses `query_database` from task-001 to fetch tasks, then applies the selection algorithm locally. Tasks whose dependencies are not all "Termine" are marked "Bloque" in Notion.

---

## Acceptance Criteria

### AC1: Selection by priority

- **Given**: 3 tasks "A faire": T1 (P2), T2 (P0), T3 (P1)
- **When**: `select_next_task(tasks)` is called
- **Then**: Returns T2 (P0 is highest priority)

### AC2: Dependency respect

- **Given**: T1 (P0, "A faire") depends on T2 (P1, "A faire") via "Bloque par"
- **When**: `select_next_task(tasks)` is called
- **Then**: T2 is selected (T1 is blocked by unfinished T2)

### AC3: Circular dependency detection

- **Given**: T1 depends on T2, T2 depends on T1 (circular)
- **When**: `select_next_task(tasks)` evaluates these tasks
- **Then**: Both are marked "Bloque" and neither is selected

### AC4: Story ID tiebreaker

- **Given**: T1 (P1, Story ID "US-003") and T2 (P1, Story ID "US-001")
- **When**: `select_next_task(tasks)` is called with equal priority tasks
- **Then**: T2 is selected (US-001 < US-003 in alphanumeric order)

---

## Steps

### Step 1: Implement eligible task filtering and data parsing (20 min)

**Input**: Raw Notion query results from `query_database`

**Actions**:
1. Create `task_selector.py`
2. Implement `parse_task(notion_page)` — extract relevant fields from Notion page object:
   - page_id, name, story_id, status, priority, complexity
   - bloque_par (list of related page IDs)
   - spec_path, flags
3. Implement `get_eligible_tasks(tasks)` — filter where status == "A faire"

**Output**: Task parsing and filtering functions

**Validation**: Correctly parses mock Notion page objects

### Step 2: Implement priority sorting with Story ID tiebreaker (20 min)

**Input**: Parsed task list from step 1

**Actions**:
1. Define priority order: P0=0, P1=1, P2=2, P3=3 (lower = higher priority)
2. Implement `sort_by_priority(tasks)` — sort by priority, then by Story ID
3. Handle missing priority (default to P3)

**Output**: Priority sorting function

**Validation**: Correctly orders tasks by priority then Story ID

### Step 3: Implement dependency resolution and circular detection (25 min)

**Input**: Parsed task list with dependency relations

**Actions**:
1. Implement `resolve_dependencies(tasks, all_tasks)`:
   - For each task, check if all "Bloque par" targets have status "Termine"
   - If any dependency is not "Termine", task is considered blocked
   - If dependency has status "Echoue", task is also blocked
2. Implement `detect_circular_dependencies(tasks)`:
   - Build dependency graph
   - Use DFS-based cycle detection
   - Return list of tasks involved in cycles
3. Implement `select_next_task(all_tasks)` — main entry point:
   - Parse all tasks
   - Resolve dependencies (filter out blocked)
   - Detect and exclude circular dependencies
   - Sort eligible by priority
   - Return first task or None

**Output**: Dependency resolution and main selector function

**Validation**: Correctly handles all dependency scenarios

### Step 4: Write unit tests for all selection scenarios (25 min)

**Input**: Functions from steps 1-3

**Actions**:
1. Test priority selection (P0 > P1 > P2)
2. Test dependency blocking (task with unfinished dep)
3. Test circular dependency detection
4. Test Story ID tiebreaker
5. Test edge cases: no eligible tasks, single task, all blocked
6. Test dependency on failed task (blocks downstream)

**Output**: Complete test file

**Validation**: All tests pass

---

## Files

| Path | Action | Description |
|------|--------|-------------|
| `src/openclaw/task_selector.py` | create | Task selection algorithm |
| `src/openclaw/tests/test_task_selector.py` | create | Unit tests for selector |

---

## Test Approach

- **Type**: Unit
- **Framework**: pytest
- **Location**: src/openclaw/tests/test_task_selector.py
- **Coverage Target**: 95%

### Test Cases

| # | Description | Type | Priority |
|---|-------------|------|----------|
| 1 | Select highest priority task | Unit | High |
| 2 | Skip blocked task (dependency not done) | Unit | High |
| 3 | Detect circular dependency | Unit | High |
| 4 | Tiebreaker by Story ID | Unit | Medium |
| 5 | No eligible tasks returns None | Unit | High |
| 6 | Single task selected | Unit | Medium |
| 7 | All tasks blocked returns None | Unit | Medium |
| 8 | Dependency on failed task | Unit | High |

---

## Dependencies

### Requires (blockedBy)

- **task-001**: Needs `query_database` for fetching tasks from Notion

### Blocks

- **task-005**: Main loop needs `select_next_task` for task selection

---

## Notes

- The selector operates on locally fetched data — a single `query_database` call fetches all tasks, then selection logic runs in-memory
- Circular dependency detection uses standard graph DFS — no external library needed
- Tasks with missing priority default to P3 (lowest) to avoid blocking the pipeline

---

*Task specification generated by /spec v1.0 — EPCI v6.0*
