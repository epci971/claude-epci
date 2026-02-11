---
id: task-006
title: Implement pipeline orchestrator
slug: pipeline-runner
feature: openclaw
complexity: L
estimated_minutes: 120
dependencies:
  - task-003
  - task-004
  - task-005
files_affected:
  - path: pipeline-runner.sh
    action: create
  - path: tests/test-pipeline.sh
    action: create
test_approach: Integration
---

# Task 006: Implement pipeline orchestrator

## Objective

Implement `pipeline-runner.sh` — the main orchestration loop that coordinates the entire pipeline: acquires a lock, runs health checks, queries Notion for available tasks, filters blocked tasks, executes them sequentially via run-task.sh, enforces the circuit breaker, checks the kill switch, and sends heartbeat notifications. This is the central script triggered by cron.

---

## Context

The pipeline runner is the "brain" of the system (section 10, Phase 5). It integrates all other components: notify.sh (task-003), quota-checker.sh (task-004), and run-task.sh (task-005). It handles guards (lockfile, kill switch, circuit breaker), dependency management (section 4.6), and health checks (section 4.4). The script is designed for cron execution — no interaction, full defensive programming.

Key decisions from brief:
- US2: All guards (kill switch, health check, circuit breaker, lockfile)
- US5: Dependency filtering via "Bloque par" relation
- D6: Kill switch via getUpdates polling (not daemon)
- D9: Dependencies via Notion relation "Bloque par"
- Section 4.6: filter_blocked_tasks(), deblocage naturel

---

## Acceptance Criteria

### AC1: Lockfile prevents concurrent execution

- **Given**: A pipeline-runner.sh process is already running
- **When**: A second cron trigger starts pipeline-runner.sh
- **Then**: The second process detects the lockfile, verifies the PID is alive, logs "Pipeline already running (PID: {pid})", and exits cleanly

### AC2: Kill switch stops the pipeline

- **Given**: The pipeline is processing tasks
- **When**: `check_kill_switch` returns 0 (kill requested)
- **Then**: The current task finishes, no new task is started, a confirmation notification is sent, and the pipeline exits

### AC3: Health check recovers orphan tasks

- **Given**: A task in Notion with status "En cours" but no running process
- **When**: The health check runs at cycle start
- **Then**: The orphan task's worktree is cleaned, its status is set to "Echoue" with "Interrupted: crash recovery", and a notification is sent

### AC4: Dependency filtering works

- **Given**: Task B has "Bloque par" relation pointing to task A (status "En cours")
- **When**: The pipeline queries tasks "A faire"
- **Then**: Task B is filtered out (not executed), and its Notion status is updated to "Bloque"

### AC5: Circuit breaker activates after 3 failures

- **Given**: 3 consecutive tasks have failed
- **When**: The pipeline reaches the 4th task
- **Then**: The cycle stops, a notification "Pipeline paused: 3 consecutive failures" is sent, and the pipeline exits

### AC6: Heartbeat sent at cycle end

- **Given**: At least one task was processed in this cycle
- **When**: The cycle completes (all tasks done or circuit breaker)
- **Then**: A heartbeat notification is sent with: tasks processed, succeeded, failed, and elapsed time

---

## Steps

### Step 1: Implement lock management and health check (30 min)

**Input**: US2-AC4 (lockfile), US2-AC2 (health check)

**Actions**:
1. Create `pipeline-runner.sh` sourcing all lib files and notify.sh, quota-checker.sh
2. Implement `acquire_lock()`:
   - Check for lockfile at `$STATE_DIR/pipeline.lock`
   - If exists: read PID, check if process alive (`kill -0 $pid`)
   - If alive: exit with "Already running (PID: $pid)"
   - If dead (stale lock): remove lockfile, log WARNING
   - Create lockfile with current PID
3. Implement `release_lock()` — remove lockfile, called in trap EXIT
4. Implement `health_check()`:
   - Query Notion for tasks with status "En cours"
   - For each: check if a corresponding worktree/process exists
   - If orphan: cleanup_worktree, update Notion to "Echoue" with "Interrupted: crash recovery"
   - Send notification for each recovered orphan
5. Implement `health_check_tokens()`:
   - Validate NOTION_API_KEY: `curl -s -o /dev/null -w "%{http_code}" https://api.notion.com/v1/users/me`
   - Validate GITHUB_TOKEN: `gh auth status`
   - Validate TELEGRAM_BOT_TOKEN: `curl -s .../getMe`
   - If any fails: notify + exit

**Output**: Lock management and health check functions

**Validation**: Lock prevents concurrent runs, health check detects orphans

### Step 2: Implement task querying and dependency filtering (30 min)

**Input**: US5 (dependencies), section 4.6

**Actions**:
1. Implement `query_available_tasks()`:
   - Call `notion_query` with filter: Statut = "A faire", sorted by Priorite
   - Enrich each task with dependency information (resolve "Bloque par" relation)
2. Implement `filter_blocked_tasks()`:
   - For each task: check if all "Bloque par" dependencies have status "Termine"
   - If blocked: update Notion status to "Bloque", add to blocked list
   - Return only unblocked tasks
3. Implement `detect_circular_deps()`:
   - Check if any pair of tasks blocks each other (A blocks B and B blocks A)
   - If found: log WARNING, notify "Circular dependency: {task_A} <-> {task_B}"
4. Handle edge cases: dependency on "Echoue" task → stays blocked + notification

**Output**: Task querying and dependency filtering

**Validation**: Blocked tasks are correctly filtered, unblocked tasks are returned

### Step 3: Implement main execution loop (30 min)

**Input**: US1, US2-AC3 (circuit breaker)

**Actions**:
1. Implement main `run_pipeline()` function:
   ```
   acquire_lock()
   health_check()
   health_check_tokens()
   tasks = query_available_tasks()
   tasks = filter_blocked_tasks(tasks)
   consecutive_failures = 0
   for task in tasks:
       check_kill_switch → exit if kill
       check_quota_status → exit if throttled/cooldown
       notify_task_start(task)
       result = run_task(task)
       if result == SUCCESS:
           consecutive_failures = 0
       elif result == PARTIAL:
           consecutive_failures = 0  # partial is not a full failure
       else:
           consecutive_failures++
           if consecutive_failures >= 3:
               notify_circuit_breaker()
               break
   notify_heartbeat(stats)
   release_lock()
   ```
2. Track statistics: processed, succeeded, failed, partial, elapsed_time
3. Handle unexpected errors: trap ERR, cleanup, notify

**Output**: Main execution loop

**Validation**: Loop processes tasks in order, respects all guards

### Step 4: Implement CLI interface and cron integration (30 min)

**Input**: US3-AC2 (dry-run preview), cron requirements

**Actions**:
1. Implement CLI argument parsing:
   - `--project <slug>` — filter to single project (optional)
   - `--max-tasks <n>` — limit tasks per cycle (default: unlimited)
   - `--log-dir <path>` — override log directory
   - `--state-dir <path>` — override state directory
2. Implement `main()` function with argument parsing and run_pipeline call
3. Add cron-friendly features: no color output if not a terminal, structured log format
4. Document cron setup:
   ```
   # Run every 30 minutes on weekends
   */30 * * * 6,0 /home/pipeline/openclaw/pipeline-runner.sh >> /var/log/pipeline.log 2>&1
   ```
5. Write integration tests with mock task data

**Output**: Complete pipeline-runner.sh with CLI and cron support

**Validation**: Full pipeline cycle runs with mock data

---

## Files

| Path | Action | Description |
|------|--------|-------------|
| `pipeline-runner.sh` | create | Main pipeline orchestrator (lock, health check, task loop, guards) |
| `tests/test-pipeline.sh` | create | Integration tests for pipeline flow |

---

## Test Approach

- **Type**: Integration
- **Framework**: bats or inline test functions
- **Location**: tests/test-pipeline.sh
- **Coverage Target**: 75%

### Test Cases

| # | Description | Type | Priority |
|---|-------------|------|----------|
| 1 | acquire_lock prevents concurrent runs | Integration | High |
| 2 | Stale lockfile is cleaned up | Integration | High |
| 3 | health_check recovers orphan tasks | Integration | High |
| 4 | filter_blocked_tasks skips blocked tasks | Unit | High |
| 5 | Circuit breaker triggers after 3 failures | Integration | High |
| 6 | Kill switch stops before next task | Integration | High |
| 7 | Heartbeat includes correct stats | Unit | Medium |
| 8 | --max-tasks limits execution | Unit | Medium |

---

## Dependencies

### Requires (blockedBy)

- **task-003**: Needs notify.sh for notifications and kill switch
- **task-004**: Needs quota-checker.sh for quota status
- **task-005**: Needs run-task.sh for task execution

### Blocks

- **task-007**: Auto-merge system extends the pipeline runner
- **task-009**: Dry-run mode and E2E tests depend on the runner

---

## Notes

- The pipeline-runner is designed for zero-interaction cron execution
- All error paths must leave the system in a clean state (no stale worktrees, no stuck locks)
- The circuit breaker threshold (3) should be configurable via `CIRCUIT_BREAKER_THRESHOLD` env var
- Consider adding a `--single-task` mode for debugging (run only the next available task)

---

*Task specification generated by /spec v1.0 — EPCI v6.0*
