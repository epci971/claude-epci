---
id: task-004
title: Implement quota management
slug: quota-checker
feature: openclaw
complexity: S
estimated_minutes: 60
dependencies: []
files_affected:
  - path: quota-checker.sh
    action: create
  - path: tests/test-quota.sh
    action: create
test_approach: Unit
---

# Task 004: Implement quota management

## Objective

Implement `quota-checker.sh` — a reactive quota management script that detects Claude Code throttling by scanning logs for rate limit patterns (M2) and applies a 30-minute cooldown timer (M3). The quota checker is deliberately simple in V1, with proactive tracking deferred until real usage data is available.

---

## Context

Claude Max has no API for quota consultation. The V1 strategy is purely reactive (D4): detect throttle in Claude Code logs, apply cooldown, and stop the cycle. Proactive tracking (M1) is deferred after calibration with real data (section 4.2). The assumed budget is ~15-30 tasks per weekend with Max 5x plan.

Key decisions from brief:
- D4: Reactive M2+M3 only, proactive M1 deferred
- Section 4.2: Throttle detection via log patterns, 30min cooldown
- Seuils speculatifs (27 sessions/window, 3 sessions/task) to be validated after first runs

---

## Acceptance Criteria

### AC1: Detect throttle patterns in logs

- **Given**: Claude Code log output containing `rate_limit`, `429`, or `too_many_requests`
- **When**: `check_quota_status` is called with the log file path
- **Then**: Returns `throttled` status with the detected pattern

### AC2: Apply cooldown timer

- **Given**: A throttle has been detected
- **When**: `start_cooldown` is called
- **Then**: A cooldown file is created with expiry timestamp (now + 30 min), and subsequent `check_quota_status` calls return `cooldown` until expiry

### AC3: Return quota status

- **Given**: No throttle detected and no active cooldown
- **When**: `check_quota_status` is called
- **Then**: Returns `ok` status, allowing the pipeline to proceed

---

## Steps

### Step 1: Implement throttle detection (30 min)

**Input**: Claude Code log patterns for rate limiting

**Actions**:
1. Create `quota-checker.sh` sourcing `lib/common.sh`
2. Implement `check_throttle()` that scans a log file for patterns: `rate_limit`, `429`, `too_many_requests`, `capacity`, `overloaded`
3. Use grep with multiple patterns on the last 100 lines of the log
4. Implement `check_cooldown()` that reads a cooldown file (`$STATE_DIR/cooldown.json`) and checks if expiry timestamp has passed
5. Implement `start_cooldown()` that creates the cooldown file with `{"expires_at": "$(date -d '+30 minutes' -Iseconds)", "reason": "throttle_detected"}`
6. Implement `clear_cooldown()` that removes the cooldown file

**Output**: Throttle detection and cooldown management functions

**Validation**: Correctly identifies throttle patterns in sample log output

### Step 2: Implement status API and tests (30 min)

**Input**: Integration requirements from pipeline-runner.sh

**Actions**:
1. Implement `check_quota_status()` — main entry point that returns JSON:
   ```json
   {"status": "ok|throttled|cooldown", "reason": "...", "cooldown_remaining_seconds": 0}
   ```
2. Logic: check cooldown first (if active, return cooldown), then check throttle (if found, start cooldown and return throttled), else return ok
3. Implement `quota_status_summary()` for logging — human-readable status string
4. Write unit tests: detect each pattern, cooldown creation/expiry, status transitions
5. Test edge cases: empty log file, no log file, corrupted cooldown file

**Output**: Complete quota-checker.sh with status API and tests

**Validation**: All unit tests pass, status transitions are correct

---

## Files

| Path | Action | Description |
|------|--------|-------------|
| `quota-checker.sh` | create | Reactive quota management (throttle detection + cooldown) |
| `tests/test-quota.sh` | create | Unit tests for quota checking |

---

## Test Approach

- **Type**: Unit
- **Framework**: bats or inline test functions
- **Location**: tests/test-quota.sh
- **Coverage Target**: 90%

### Test Cases

| # | Description | Type | Priority |
|---|-------------|------|----------|
| 1 | Detects "rate_limit" pattern in log | Unit | High |
| 2 | Detects "429" pattern in log | Unit | High |
| 3 | Returns "ok" when no throttle and no cooldown | Unit | High |
| 4 | Creates cooldown file with correct expiry | Unit | High |
| 5 | Returns "cooldown" when cooldown is active | Unit | High |
| 6 | Clears cooldown after expiry | Unit | Medium |
| 7 | Handles missing log file gracefully | Unit | Medium |

---

## Dependencies

### Requires (blockedBy)

*No dependencies — this task can start immediately*

### Blocks

- **task-006**: Pipeline runner needs quota status check before each task

---

## Notes

- The cooldown duration (30 min) should be configurable via environment variable `QUOTA_COOLDOWN_MINUTES`
- V1.1 will add proactive tracking after calibrating with real usage data from 3-4 weekends
- The `$STATE_DIR` defaults to `.pipeline/state/` — created by pipeline-runner.sh on first run

---

*Task specification generated by /spec v1.0 — EPCI v6.0*
