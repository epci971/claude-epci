---
id: task-003
title: Create step-00c-worktree.md
slug: step-00c
feature: worktree-implement
complexity: M
estimated_minutes: 90
dependencies:
  - task-001
  - task-002
files_affected:
  - path: src/skills/implement/steps/step-00c-worktree.md
    action: create
test_approach: Integration
---

## Objective

Create a new conditional step in the /implement workflow that handles worktree creation. This step is triggered after complexity detection for STANDARD+ features and provides an opt-in breakpoint for worktree setup.

## Context

The worktree step sits between init (step-00) and explore (step-01). It:
- Is only reached for STANDARD/LARGE complexity features
- Presents a breakpoint asking if user wants worktree isolation
- If accepted, calls worktree-create.sh and updates state
- If declined, proceeds normally without worktree

Key decisions:
- Opt-in via breakpoint (not automatic)
- Integrates with existing step flow
- Persists worktree info in state.json

## Acceptance Criteria

### AC1: Step File Structure
- **Given**: The implement skill step conventions
- **When**: step-00c-worktree.md is created
- **Then**:
  - YAML frontmatter includes proper navigation (prev/next)
  - Mandatory execution rules section present
  - Breakpoint defined with opt-in options
  - Context boundaries documented

### AC2: Worktree Creation Flow
- **Given**: User selects "Create worktree" at breakpoint
- **When**: Step executes creation logic
- **Then**:
  - worktree-create.sh is called with feature-slug
  - Working directory changes to worktree path
  - State.json updated with worktree metadata
  - Next step triggered is step-01-explore

### AC3: Skip Flow
- **Given**: User selects "Skip worktree" at breakpoint
- **When**: Step proceeds without worktree
- **Then**:
  - No worktree created
  - State.json worktree.enabled = false
  - Proceeds to step-01-explore in main repo

### AC4: Existing Worktree Detection
- **Given**: Feature already has a worktree
- **When**: Step initializes
- **Then**:
  - Worktree-status.sh is called
  - If exists and active: offer to resume or recreate
  - If exists and abandoned: offer to cleanup and recreate

## Steps

### Step 1: Create step file skeleton (20 min)

**Input**: Step file conventions from other implement steps

**Actions**:
1. Create `src/skills/implement/steps/step-00c-worktree.md`
2. Add YAML frontmatter:
```yaml
---
name: step-00c-worktree
description: Optional worktree creation for parallel development
prev_step: steps/step-00-init.md
next_step: steps/step-01-explore.md
conditional_next:
  - condition: "worktree declined"
    step: steps/step-01-explore.md
---
```
3. Add mandatory execution rules section
4. Add context boundaries section
5. Add reference to scripts

**Output**: Step file skeleton

**Validation**:
- Frontmatter parses correctly
- Navigation links valid

### Step 2: Implement detection protocol (25 min)

**Input**: worktree-status.sh script

**Actions**:
1. Add "Check Existing Worktree" section:
```markdown
### 1. Check Existing Worktree

Call worktree-status.sh to detect existing worktree:

EXECUTE Bash({
  command: "./scripts/worktree-status.sh {feature-slug}",
  description: "Check worktree status"
})

Parse JSON result:
- If exists && status == active: Breakpoint "Resume or Recreate"
- If exists && status == abandoned: Breakpoint "Cleanup and Recreate"
- If !exists: Breakpoint "Create Worktree"
```
2. Document each detection path
3. Add error handling for script failures

**Output**: Detection protocol complete

**Validation**:
- All detection paths documented
- Error cases covered

### Step 3: Implement main breakpoint (25 min)

**Input**: Breakpoint system conventions

**Actions**:
1. Add ASCII box breakpoint:
```
┌─────────────────────────────────────────────────────────────────────┐
│ 🌳 WORKTREE SETUP                                                   │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│ Feature: {feature-slug}                                             │
│ Complexity: {complexity}                                            │
│ Current worktree: {status}                                          │
│                                                                     │
│ Worktree enables parallel development of multiple features.         │
│ Path: ../worktrees/{feature-slug}/                                  │
│ Branch: feature/{feature-slug}                                      │
│                                                                     │
├─────────────────────────────────────────────────────────────────────┤
│ ┌─ Options ──────────────────────────────────────────────────────┐ │
│ │  [A] Create worktree (Recommended) — Isolated development      │ │
│ │  [B] Skip worktree — Work in main repo                         │ │
│ │  [?] Autre reponse...                                          │ │
│ └────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
```
2. Add AskUserQuestion call
3. Document variable substitutions
4. Add wait instruction

**Output**: Breakpoint section complete

**Validation**:
- Breakpoint follows conventions
- All options documented

### Step 4: Implement creation and state update (20 min)

**Input**: worktree-create.sh, state schema

**Actions**:
1. Add "Execute Worktree Creation" section:
```markdown
### 3. Execute Worktree Creation

IF user selected "Create worktree":

EXECUTE Bash({
  command: "./scripts/worktree-create.sh {feature-slug}",
  description: "Create worktree for feature"
})

Update state.json:
{
  "worktree": {
    "enabled": true,
    "path": "../worktrees/{feature-slug}",
    "branch": "feature/{feature-slug}",
    "status": "active",
    "created_at": "{ISO-8601}"
  }
}

Change working directory to worktree path.
```
2. Add skip flow documentation
3. Add output format section
4. Add next step trigger

**Output**: Complete step file

**Validation**:
- All flows documented
- State update format correct

## Files

| Path | Action | Description |
|------|--------|-------------|
| `src/skills/implement/steps/step-00c-worktree.md` | create | Worktree creation step |

## Test Approach

- **Type**: Integration
- **Framework**: Manual workflow testing
- **Location**: N/A (step file, not code)
- **Coverage Target**: All decision paths

### Test Cases

| # | Description | Type | Priority |
|---|-------------|------|----------|
| 1 | Create worktree path | Integration | High |
| 2 | Skip worktree path | Integration | High |
| 3 | Resume existing worktree | Integration | Medium |
| 4 | Cleanup abandoned worktree | Integration | Medium |
| 5 | Script failure handling | Integration | Medium |

## Dependencies

### Requires (blockedBy)
- **task-001**: Scripts must exist
- **task-002**: State schema must support worktree

### Blocks (blocks)
- **task-004**: init modification references this step
- **task-005**: memory modification references this step
- **task-006**: documentation references this step
