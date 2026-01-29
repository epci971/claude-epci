---
id: task-006
title: Update documentation
slug: documentation
feature: worktree-implement
complexity: S
estimated_minutes: 45
dependencies:
  - task-003
  - task-004
  - task-005
files_affected:
  - path: src/skills/implement/SKILL.md
    action: modify
test_approach: Review
---

## Objective

Update the /implement skill documentation to reflect the new worktree capability, including the new step, flags, and workflow changes.

## Context

The SKILL.md file is the primary documentation for the /implement skill. After worktree integration, it needs to document:
- New step-00c-worktree in the workflow
- Worktree-related behavior and options
- Updated step table
- Usage examples with worktree

## Acceptance Criteria

### AC1: Workflow Overview Update
- **Given**: Current SKILL.md workflow diagram
- **When**: Diagram is updated
- **Then**:
  - step-00c-worktree appears between init and explore
  - Conditional path from init to worktree step shown
  - Worktree step shown as optional

### AC2: Step Table Update
- **Given**: Current step table in SKILL.md
- **When**: Table is updated
- **Then**:
  - New row for step-00c-worktree added
  - Skippable marked as "Yes (opt-out)"
  - Description accurate

### AC3: Usage Examples
- **Given**: Usage examples section
- **When**: Examples are updated
- **Then**:
  - Example shows worktree creation flow
  - Example shows skip worktree flow
  - Example shows --continue with worktree

## Steps

### Step 1: Update workflow overview (20 min)

**Input**: Current SKILL.md, new step structure

**Actions**:
1. Read current SKILL.md
2. Find Workflow Overview section
3. Update ASCII/Mermaid diagram to include:
```
Step 00: INIT
  +- Parse input, detect complexity
  +- Route: TINY/SMALL → turbo | STANDARD+ → worktree

Step 00c: WORKTREE (NEW - STANDARD+ only)
  +- Check existing worktree
  +- Offer worktree creation (opt-in)
  +- If accepted: create worktree, cd into it

Step 01: EXPLORE [E]
  +- (runs in worktree if created)
  ...

Step 07: MEMORY [M]
  +- Update index.json
  +- If worktree: offer finalization
```
4. Update any workflow text descriptions

**Output**: Updated workflow section

**Validation**:
- Diagram accurate
- Text matches diagram

### Step 2: Update step table and flags (25 min)

**Input**: Step table, flags section

**Actions**:
1. Find Steps table
2. Add new row:
```markdown
| 00c | worktree | [W] | Worktree setup for parallel dev | Yes (opt-out) |
```
3. Renumber if needed (00c comes after 00, before 01)
4. Update Flags section if any new flags added:
```markdown
| `--no-worktree` | off | Skip worktree creation for STANDARD+ |
```
5. Update any step count references
6. Add Worktree section under Features:
```markdown
## Worktree Support

For STANDARD and LARGE features, /implement offers optional worktree isolation:

| Aspect | Behavior |
|--------|----------|
| Location | ../worktrees/{feature-slug}/ |
| Branch | feature/{feature-slug} |
| Activation | Opt-in via breakpoint |
| Cleanup | Offered at step-07 completion |

Benefits:
- Parallel development of multiple features
- Clean rollback on failure
- Isolated testing environment
```

**Output**: Updated tables and sections

**Validation**:
- Table formatting correct
- All steps accounted for

## Files

| Path | Action | Description |
|------|--------|-------------|
| `src/skills/implement/SKILL.md` | modify | Add worktree documentation |

## Test Approach

- **Type**: Review
- **Framework**: Manual review
- **Location**: N/A
- **Coverage Target**: All new features documented

### Test Cases

| # | Description | Type | Priority |
|---|-------------|------|----------|
| 1 | Workflow diagram accurate | Review | High |
| 2 | Step table complete | Review | High |
| 3 | No broken internal links | Review | Medium |
| 4 | Examples work as documented | Review | Medium |

## Dependencies

### Requires (blockedBy)
- **task-003**: step-00c must be complete
- **task-004**: init modifications must be complete
- **task-005**: memory modifications must be complete

### Blocks (blocks)
- None (final task)
