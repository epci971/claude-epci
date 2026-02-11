---
id: task-003
title: Implement Telegram notification wrapper
slug: telegram-notify
feature: openclaw
complexity: S
estimated_minutes: 75
dependencies: []
files_affected:
  - path: notify.sh
    action: create
  - path: tests/test-notify.sh
    action: create
test_approach: Unit
---

# Task 003: Implement Telegram notification wrapper

## Objective

Implement `notify.sh` — a Telegram Bot API wrapper that sends formatted notifications (task start, success, failure, partial), checks for kill switch messages via getUpdates, and sends heartbeat summaries at cycle end. This provides the observability layer for the pipeline.

---

## Context

Telegram is used in basic mode: notifications per task + kill switch (D3). The kill switch works without a daemon: the pipeline checks recent messages via getUpdates in each cycle (D6, D8). The kill switch reaction delay equals the cron interval (max 30 min). Notifications are non-critical — if Telegram fails, the pipeline continues with a WARNING log.

Key decisions from brief:
- D3: Telegram basique (notifications + kill switch only)
- D6: Polling via getUpdates (no daemon, no webhook)
- D8: Kill switch integrated in pipeline-runner.sh, not a separate service
- Section 4.3: notify.sh = curl wrapper around sendMessage

---

## Acceptance Criteria

### AC1: Send formatted notification

- **Given**: Valid TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID
- **When**: `notify_task_start "task-name" "project"` is called
- **Then**: A formatted message is sent via Telegram sendMessage API with task name, project, and timestamp

### AC2: Kill switch detection

- **Given**: A recent Telegram message containing `/kill`
- **When**: `check_kill_switch` is called
- **Then**: Returns exit code 0 (kill requested) and the function extracts the /kill message from getUpdates response

### AC3: Heartbeat summary

- **Given**: A completed pipeline cycle with stats (tasks processed, succeeded, failed)
- **When**: `notify_heartbeat 10 8 2` is called
- **Then**: A summary message is sent: "Pipeline cycle complete: 10 processed, 8 OK, 2 failed"

### AC4: Graceful degradation on Telegram failure

- **Given**: Telegram API is unreachable or returns an error
- **When**: Any notify function is called
- **Then**: A WARNING is logged, the function returns success (exit 0), and the pipeline continues

---

## Steps

### Step 1: Implement sendMessage wrapper and formatters (25 min)

**Input**: Telegram Bot API documentation for sendMessage

**Actions**:
1. Create `notify.sh` sourcing `lib/common.sh`
2. Implement `_telegram_send()` — low-level curl POST to `https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage`
3. Set parse_mode to "HTML" for formatting (bold, code, etc.)
4. Implement `notify_task_start "task_name" "project"` — formats and sends start notification
5. Implement `notify_task_success "task_name" "project" "pr_url" "duration"` — success with PR link
6. Implement `notify_task_failure "task_name" "project" "error_msg" "phase"` — failure with error context
7. Implement `notify_task_partial "task_name" "project" "pr_url" "failed_count"` — partial success
8. Handle curl errors: if sendMessage fails, log_warn and return 0

**Output**: notify.sh with all send functions

**Validation**: Each function produces correct curl command (dry-run mode)

### Step 2: Implement kill switch check via getUpdates (25 min)

**Input**: Telegram Bot API documentation for getUpdates

**Actions**:
1. Implement `check_kill_switch()` — GET request to `getUpdates?offset=-10&limit=10`
2. Parse response with jq: find messages where `text == "/kill"` in the last 30 minutes
3. Filter by chat_id matching TELEGRAM_CHAT_ID (security: only owner can kill)
4. Return 0 if /kill found (kill requested), 1 if no kill message
5. Implement `notify_kill_acknowledged()` — confirms kill switch received
6. Handle API errors: if getUpdates fails, log_warn and return 1 (assume no kill = continue)

**Output**: check_kill_switch function in notify.sh

**Validation**: Correctly detects /kill message in mock getUpdates response

### Step 3: Implement heartbeat and tests (25 min)

**Input**: US3-AC3 requirements for cycle summary

**Actions**:
1. Implement `notify_heartbeat "processed" "succeeded" "failed"` — formats summary message
2. Include elapsed time, tasks breakdown, and any error highlights
3. Implement `notify_pipeline_error "error_msg"` — critical pipeline error (token invalid, etc.)
4. Write unit tests: mock curl responses for sendMessage and getUpdates
5. Test kill switch detection with sample getUpdates JSON
6. Test graceful degradation: mock curl failure, verify log_warn and exit 0

**Output**: Complete notify.sh with heartbeat and all tests

**Validation**: All unit tests pass

---

## Files

| Path | Action | Description |
|------|--------|-------------|
| `notify.sh` | create | Telegram notification wrapper (send, kill switch, heartbeat) |
| `tests/test-notify.sh` | create | Unit tests with mock Telegram API |

---

## Test Approach

- **Type**: Unit
- **Framework**: bats or inline test functions
- **Location**: tests/test-notify.sh
- **Coverage Target**: 80%

### Test Cases

| # | Description | Type | Priority |
|---|-------------|------|----------|
| 1 | notify_task_success sends formatted message | Unit | High |
| 2 | notify_task_failure includes error and phase | Unit | High |
| 3 | check_kill_switch detects /kill in recent messages | Unit | High |
| 4 | check_kill_switch ignores /kill from other chats | Unit | Medium |
| 5 | check_kill_switch returns 1 when no /kill found | Unit | High |
| 6 | Telegram API failure logs WARNING and continues | Unit | High |

---

## Dependencies

### Requires (blockedBy)

*No dependencies — this task can start immediately*

### Blocks

- **task-006**: Pipeline runner needs notify functions and kill switch check

---

## Notes

- HTML parse_mode is preferred over Markdown for Telegram (fewer escaping issues)
- The getUpdates offset=-10 approach gets the last 10 messages — sufficient for kill switch detection
- Consider adding a `TELEGRAM_ENABLED=true/false` flag in .env for environments without Telegram

---

*Task specification generated by /spec v1.0 — EPCI v6.0*
