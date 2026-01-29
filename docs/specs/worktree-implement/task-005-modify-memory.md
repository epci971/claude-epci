---
id: task-005
title: Modify step-07-memory.md
slug: modify-memory
feature: worktree-implement
complexity: S
estimated_minutes: 60
dependencies:
  - task-003
files_affected:
  - path: src/skills/implement/steps/step-07-memory.md
    action: modify
test_approach: Integration
---

## Objective

Modify the memory step to handle worktree finalization at the end of the /implement workflow. When a feature is complete, offer to merge the worktree branch and cleanup the worktree directory.

## Context

The memory step (step-07) is the final step in /implement. It currently:
- Updates index.json with feature summary
- Logs modified files and test count

For worktree integration, it should additionally:
- Check if feature used a worktree
- Offer finalization options (merge, keep, abandon)
- Call worktree-finalize.sh if cleanup selected
- Update state.worktree.status

## Acceptance Criteria

### AC1: Worktree Detection
- **Given**: Feature completion in step-07
- **When**: Step loads state
- **Then**:
  - Check state.worktree.enabled
  - If true: proceed to finalization breakpoint
  - If false: proceed normally (existing behavior)

### AC2: Finalization Breakpoint
- **Given**: Feature completed with worktree enabled
- **When**: Breakpoint is presented
- **Then**:
  - Shows worktree path and branch info
  - Offers options: Finalize (merge+cleanup), Keep worktree, Abandon
  - User can choose action

### AC3: Cleanup Execution
- **Given**: User selects "Finalize"
- **When**: Finalization logic runs
- **Then**:
  - Warns if uncommitted changes exist
  - Calls worktree-finalize.sh
  - Updates state.worktree.status to "merged"
  - Returns to main repo directory

## Steps

### Step 1: Add worktree detection (15 min)

**Input**: State schema, current step-07-memory.md

**Actions**:
1. Read current step-07-memory.md
2. Add section after index.json update:
```markdown
### 7. Check Worktree Status

IF state.worktree?.enabled == true:
  → Proceed to Worktree Finalization Breakpoint
ELSE:
  → Proceed to completion (existing behavior)
```
3. Document state access pattern

**Output**: Detection logic added

**Validation**:
- Detection condition correct
- Fallback to normal behavior

### Step 2: Create finalization breakpoint (25 min)

**Input**: Breakpoint conventions

**Actions**:
1. Add finalization breakpoint:
```
┌─────────────────────────────────────────────────────────────────────┐
│ 🌳 WORKTREE FINALIZATION                                            │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│ Feature: {feature-slug}                                             │
│ Worktree: {worktree.path}                                           │
│ Branch: {worktree.branch}                                           │
│ Status: {clean/uncommitted changes}                                 │
│                                                                     │
│ Feature implementation is complete. Choose how to handle worktree:  │
│                                                                     │
├─────────────────────────────────────────────────────────────────────┤
│ ┌─ Options ──────────────────────────────────────────────────────┐ │
│ │  [A] Finalize (Recommended) — Cleanup worktree, keep branch    │ │
│ │  [B] Keep worktree — Continue working in worktree              │ │
│ │  [C] Abandon — Cleanup worktree, delete branch                 │ │
│ │  [?] Autre reponse...                                          │ │
│ └────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
```
2. Add AskUserQuestion call
3. Document each option behavior

**Output**: Breakpoint section

**Validation**:
- Options clear and distinct
- All status values handled

### Step 3: Implement finalization actions (20 min)

**Input**: worktree-finalize.sh

**Actions**:
1. Add action handlers:
```markdown
### Handle Finalization Choice

**IF "Finalize" selected:**
1. Check for uncommitted changes (warn if present)
2. Execute: `./scripts/worktree-finalize.sh {feature-slug}`
3. Update state.worktree.status = "merged"
4. Change directory back to main repo
5. Log: "Worktree finalized. Branch {branch} ready for PR."

**IF "Keep worktree" selected:**
1. Keep state.worktree.status = "active"
2. Log: "Worktree kept at {path}. Remember to finalize later."

**IF "Abandon" selected:**
1. Execute: `./scripts/worktree-finalize.sh {feature-slug} --force`
2. Update state.worktree.status = "abandoned"
3. Delete branch: `git branch -D {branch}`
4. Log: "Worktree abandoned and cleaned up."
```
2. Add error handling
3. Ensure directory change on finalize

**Output**: Complete action handlers

**Validation**:
- All paths implemented
- State updates correct

## Files

| Path | Action | Description |
|------|--------|-------------|
| `src/skills/implement/steps/step-07-memory.md` | modify | Add worktree finalization |

## Test Approach

- **Type**: Integration
- **Framework**: Manual workflow testing
- **Location**: N/A (step file)
- **Coverage Target**: All finalization paths

### Test Cases

| # | Description | Type | Priority |
|---|-------------|------|----------|
| 1 | Finalize with clean worktree | Integration | High |
| 2 | Keep worktree active | Integration | High |
| 3 | Abandon worktree | Integration | Medium |
| 4 | Handle uncommitted changes | Integration | Medium |
| 5 | No worktree (normal flow) | Integration | High |

## Dependencies

### Requires (blockedBy)
- **task-003**: step-00c must exist (worktree creation)

### Blocks (blocks)
- **task-006**: Documentation needs updated flow
