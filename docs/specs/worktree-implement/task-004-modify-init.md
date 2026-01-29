---
id: task-004
title: Modify step-00-init.md
slug: modify-init
feature: worktree-implement
complexity: S
estimated_minutes: 60
dependencies:
  - task-003
files_affected:
  - path: src/skills/implement/steps/step-00-init.md
    action: modify
test_approach: Integration
---

## Objective

Modify the initialization step to integrate worktree routing. After complexity detection, STANDARD+ features are routed to the new step-00c-worktree instead of directly to step-01-explore.

## Context

Currently step-00-init routes:
- TINY/SMALL → step-00b-turbo (redirect to /quick)
- STANDARD/LARGE → step-01-explore

After modification:
- TINY/SMALL → step-00b-turbo (unchanged)
- STANDARD/LARGE → step-00c-worktree (new routing)

The worktree step then routes to step-01-explore after user decision.

## Acceptance Criteria

### AC1: Frontmatter Update
- **Given**: Current step-00-init.md frontmatter
- **When**: Frontmatter is updated
- **Then**:
  - `next_step` becomes `steps/step-00c-worktree.md` (for STANDARD+)
  - `conditional_next` updated to reflect new routing
  - Existing TINY/SMALL routing preserved

### AC2: Worktree Resume Check
- **Given**: A feature with existing worktree in state
- **When**: --continue flag is used
- **Then**:
  - State is loaded and worktree.enabled checked
  - If enabled: working directory changed to worktree.path
  - Resume continues in correct context

### AC3: Documentation Update
- **Given**: Step documentation
- **When**: Next step trigger section is updated
- **Then**:
  - New routing clearly documented
  - Both paths (worktree and turbo) explained

## Steps

### Step 1: Update frontmatter navigation (15 min)

**Input**: Current step-00-init.md

**Actions**:
1. Read current file
2. Update frontmatter:
```yaml
---
name: step-00-init
description: Initialize implement workflow and detect complexity
prev_step: null
next_step: steps/step-00c-worktree.md
conditional_next:
  - condition: "complexity == TINY or complexity == SMALL"
    step: steps/step-00b-turbo.md
  - condition: "complexity == STANDARD or complexity == LARGE"
    step: steps/step-00c-worktree.md
---
```
3. Verify YAML is valid

**Output**: Updated frontmatter

**Validation**:
- YAML parses correctly
- All paths valid

### Step 2: Add worktree resume logic (25 min)

**Input**: State schema with worktree field

**Actions**:
1. Add new section after "Load State" (if --continue):
```markdown
### Resume Worktree Context (if --continue)

IF resuming from state AND state.worktree.enabled == true:
  1. Verify worktree exists: call worktree-status.sh
  2. If exists and active:
     - Change working directory to state.worktree.path
     - Log: "Resumed in worktree: {path}"
  3. If exists but not active:
     - Warn: "Worktree exists but status is {status}"
     - Offer to recreate or continue in main repo
  4. If not exists:
     - Warn: "Worktree no longer exists"
     - Offer to recreate or continue in main repo
```
2. Ensure this runs before complexity detection on resume
3. Add error handling for missing worktree

**Output**: Resume logic added

**Validation**:
- All resume paths documented
- Error cases handled

### Step 3: Update next step trigger section (20 min)

**Input**: Current NEXT STEP TRIGGER section

**Actions**:
1. Find NEXT STEP TRIGGER section
2. Update to:
```markdown
## NEXT STEP TRIGGER:

### For STANDARD or LARGE complexity:
When complexity is STANDARD or LARGE and user confirms, proceed to `step-00c-worktree.md`.

The worktree step will:
- Offer worktree creation for parallel development
- If accepted: create worktree, then proceed to explore
- If declined: proceed to explore in main repo

### For TINY or SMALL complexity:
Proceed to `step-00b-turbo.md` (redirect to /quick).
```
3. Update any inline references to next step

**Output**: Updated trigger documentation

**Validation**:
- All paths documented
- No orphan references

## Files

| Path | Action | Description |
|------|--------|-------------|
| `src/skills/implement/steps/step-00-init.md` | modify | Add worktree routing and resume logic |

## Test Approach

- **Type**: Integration
- **Framework**: Manual workflow testing
- **Location**: N/A (step file)
- **Coverage Target**: All routing paths

### Test Cases

| # | Description | Type | Priority |
|---|-------------|------|----------|
| 1 | STANDARD routes to worktree step | Integration | High |
| 2 | SMALL routes to turbo step | Integration | High |
| 3 | Resume with active worktree | Integration | High |
| 4 | Resume with missing worktree | Integration | Medium |

## Dependencies

### Requires (blockedBy)
- **task-003**: step-00c must exist for routing

### Blocks (blocks)
- **task-006**: Documentation needs updated flow
