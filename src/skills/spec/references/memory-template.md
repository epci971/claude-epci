# MEMORY.md Template

> Template structure for Ralph execution state persistence.

## Overview

MEMORY.md tracks execution state for:
- Progress monitoring during execution
- Resumption after interruption
- History of modifications and decisions

**Key Principle**: MEMORY.md is the single source of truth for Ralph execution state. Claude Code reads it on resume and updates it after each task.

---

## Complete Template

```markdown
# Ralph Memory — {Feature Title}

## Current State

- **Feature**: {feature-slug}
- **Started**: {ISO-8601 timestamp}
- **Current Task**: {task-id or "none"}
- **Status**: {PENDING|IN_PROGRESS|PAUSED|COMPLETED}

## Progress

| Task | Status | Completed At | Notes |
|------|--------|--------------|-------|
| task-001 | pending | - | - |
| task-002 | pending | - | - |
| task-003 | pending | - | - |

## Files Modified

| File | Action | Task |
|------|--------|------|
| - | - | - |

## Tests Added

| Test | Coverage | Task |
|------|----------|------|
| - | - | - |

## Issues Encountered

| Issue | Resolution | Task |
|-------|------------|------|
| - | - | - |

## Decisions Made

| Decision | Rationale | Task |
|----------|-----------|------|
| - | - | - |

## Context Notes

{Free-form notes for context preservation across sessions}

---

*Last updated: {ISO-8601 timestamp}*
```

---

## Section Descriptions

### Current State

Tracks the overall execution status.

| Field | Description | Example |
|-------|-------------|---------|
| Feature | Feature slug being implemented | `auth-oauth` |
| Started | When execution began | `2026-01-28T10:30:00Z` |
| Current Task | Task being worked on | `task-002` |
| Status | Overall status | `IN_PROGRESS` |

### Progress

Table of all tasks with their completion status.

**Columns**:
- **Task**: Task ID from spec
- **Status**: Current status (see Status Values below)
- **Completed At**: ISO-8601 timestamp when completed
- **Notes**: Brief completion note

### Files Modified

Track all files created or changed during execution.

**Columns**:
- **File**: Relative path
- **Action**: `created` | `modified` | `deleted`
- **Task**: Which task made this change

### Tests Added

Track all tests created.

**Columns**:
- **Test**: Test file path or test name
- **Coverage**: Coverage achieved (if measurable)
- **Task**: Which task added this test

### Issues Encountered

Document problems and their resolutions.

**Columns**:
- **Issue**: Brief description of the problem
- **Resolution**: How it was resolved
- **Task**: Which task encountered this

### Decisions Made

Record technical decisions for future reference.

**Columns**:
- **Decision**: What was decided
- **Rationale**: Why this choice was made
- **Task**: Which task required this decision

### Context Notes

Free-form section for:
- Important context for resumption
- Warnings for future tasks
- Links to relevant documentation
- Partial progress within a task

---

## Status Values

### Task Status

| Status | Meaning | When to Use |
|--------|---------|-------------|
| `pending` | Not yet started | Initial state for all tasks |
| `in_progress` | Currently executing | Task started, not complete |
| `completed` | Successfully finished | All steps done, tests pass |
| `blocked` | Waiting on external factor | Dependency not met |
| `failed` | Encountered unrecoverable error | Needs manual intervention |

### Overall Status

| Status | Meaning |
|--------|---------|
| `PENDING` | Execution not started |
| `IN_PROGRESS` | Actively executing |
| `PAUSED` | Stopped mid-execution |
| `COMPLETED` | All tasks done |

---

## Update Protocol

### After Each Task Completion

1. **Update task status** to `completed` in Progress table
2. **Add timestamp** in Completed At column
3. **Add files** to Files Modified table
4. **Add tests** to Tests Added table
5. **Record decisions** if any were made
6. **Update Current Task** to next task ID
7. **Update Last updated** timestamp

### Example Update

Before:
```markdown
## Progress

| Task | Status | Completed At | Notes |
|------|--------|--------------|-------|
| task-001 | in_progress | - | Working on step 2 |
| task-002 | pending | - | - |
```

After task-001 completion:
```markdown
## Progress

| Task | Status | Completed At | Notes |
|------|--------|--------------|-------|
| task-001 | completed | 2026-01-28T11:00:00Z | All tests pass |
| task-002 | in_progress | - | Starting |

## Files Modified

| File | Action | Task |
|------|--------|------|
| src/models/user.py | created | task-001 |
| tests/test_user.py | created | task-001 |

## Tests Added

| Test | Coverage | Task |
|------|----------|------|
| test_user_creation | 95% | task-001 |
| test_user_validation | 90% | task-001 |
```

---

## Resumption

When resuming execution:

1. **Read Current State** to know where we stopped
2. **Check Progress** table for last completed task
3. **Find next pending** task by dependency order
4. **Read Context Notes** for important information
5. **Continue from there** (don't repeat completed work)

### Resumption Commands

```bash
# View current memory state
cat .ralph/{feature-slug}/MEMORY.md

# Check git commits for this feature
git log --oneline --grep="{feature-slug}"

# Verify test status
{test_command}
```

---

## Generation Notes

When generating MEMORY.md in step-03:

1. Initialize all tasks as `pending`
2. Set Current Task to first task ID
3. Set Status to `PENDING`
4. Set Started to current timestamp
5. Leave tables empty (will be filled during execution)
6. Add Context Notes placeholder
