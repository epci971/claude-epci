---
id: task-001
title: Create worktree shell scripts
slug: worktree-scripts
feature: worktree-implement
complexity: M
estimated_minutes: 90
dependencies: []
files_affected:
  - path: scripts/worktree-create.sh
    action: create
  - path: scripts/worktree-finalize.sh
    action: create
  - path: scripts/worktree-status.sh
    action: create
test_approach: Integration
---

## Objective

Create shell scripts for automated git worktree lifecycle management. These scripts enable transparent creation, status checking, and cleanup of worktrees for parallel feature development.

## Context

Git worktrees allow multiple working directories from a single repository. For /implement integration, we need scripts that:
- Create worktrees with consistent naming conventions
- Clean up worktrees after feature completion
- Check worktree status for session resumption

Key decisions from brief:
- Path: `../worktrees/{feature-slug}/`
- Branch naming: `feature/{feature-slug}`
- Naming aligned with global-git-workflow.md conventions

## Acceptance Criteria

### AC1: Worktree Creation
- **Given**: A feature-slug and base branch (default: main)
- **When**: `worktree-create.sh <feature-slug>` is executed
- **Then**:
  - Directory `../worktrees/{feature-slug}/` is created
  - Branch `feature/{feature-slug}` is created from base
  - Script returns 0 on success, non-zero on error
  - Error message displayed if worktree already exists

### AC2: Worktree Finalization
- **Given**: An existing worktree for a feature
- **When**: `worktree-finalize.sh <feature-slug>` is executed
- **Then**:
  - Worktree directory is removed
  - Associated branch is deleted (if merged) or kept (if unmerged)
  - Script warns if uncommitted changes exist
  - Returns 0 on success

### AC3: Worktree Status
- **Given**: A feature-slug
- **When**: `worktree-status.sh <feature-slug>` is executed
- **Then**:
  - Returns JSON with: exists, path, branch, clean (no uncommitted changes)
  - Returns `{"exists": false}` if no worktree

## Steps

### Step 1: Create worktree-create.sh (25 min)

**Input**: Shell scripting conventions, git worktree documentation

**Actions**:
1. Create `scripts/worktree-create.sh`
2. Add shebang and set -euo pipefail
3. Parse arguments: feature-slug (required), base-branch (optional, default main)
4. Validate feature-slug is kebab-case
5. Check if worktree already exists
6. Calculate paths:
   - worktree_path: `../worktrees/${feature_slug}`
   - branch_name: `feature/${feature_slug}`
7. Execute: `git worktree add -b "${branch_name}" "${worktree_path}" "${base_branch}"`
8. Output success message with path
9. Make executable: `chmod +x`

**Output**: Working worktree-create.sh script

**Validation**:
```bash
./scripts/worktree-create.sh test-feature
ls ../worktrees/test-feature/
git worktree list | grep test-feature
```

### Step 2: Create worktree-finalize.sh (25 min)

**Input**: worktree-create.sh pattern

**Actions**:
1. Create `scripts/worktree-finalize.sh`
2. Add shebang and set -euo pipefail
3. Parse arguments: feature-slug (required), --force flag (optional)
4. Validate worktree exists
5. Check for uncommitted changes, warn if present
6. If --force or clean:
   - `git worktree remove "${worktree_path}"`
   - Check if branch is merged to main
   - If merged: `git branch -d "${branch_name}"`
   - If not merged: warn but don't delete branch
7. Run `git worktree prune`
8. Output success message

**Output**: Working worktree-finalize.sh script

**Validation**:
```bash
./scripts/worktree-finalize.sh test-feature
ls ../worktrees/ | grep -v test-feature
```

### Step 3: Create worktree-status.sh (20 min)

**Input**: JSON output format requirements

**Actions**:
1. Create `scripts/worktree-status.sh`
2. Add shebang
3. Parse arguments: feature-slug
4. Check if worktree directory exists
5. If exists:
   - Get current branch: `git -C "${path}" branch --show-current`
   - Check if clean: `git -C "${path}" status --porcelain`
   - Output JSON: `{"exists": true, "path": "...", "branch": "...", "clean": true/false}`
6. If not exists:
   - Output: `{"exists": false}`

**Output**: Working worktree-status.sh script

**Validation**:
```bash
./scripts/worktree-status.sh test-feature | jq .
```

### Step 4: Add error handling and tests (20 min)

**Input**: All three scripts created

**Actions**:
1. Add consistent error codes:
   - 1: Invalid arguments
   - 2: Worktree already exists (create) / not found (finalize)
   - 3: Uncommitted changes (finalize without --force)
   - 4: Git command failed
2. Add usage functions with help text
3. Create test script `scripts/test-worktree-scripts.sh`:
   - Test create, status, finalize cycle
   - Test error conditions
   - Cleanup after tests
4. Run test script, verify all pass

**Output**: Robust scripts with error handling

**Validation**:
```bash
./scripts/test-worktree-scripts.sh
echo $?  # Should be 0
```

## Files

| Path | Action | Description |
|------|--------|-------------|
| `scripts/worktree-create.sh` | create | Create worktree with branch |
| `scripts/worktree-finalize.sh` | create | Remove worktree, optionally delete branch |
| `scripts/worktree-status.sh` | create | Check worktree status (JSON output) |
| `scripts/test-worktree-scripts.sh` | create | Integration tests for scripts |

## Test Approach

- **Type**: Integration
- **Framework**: Shell scripts (bash)
- **Location**: scripts/test-worktree-scripts.sh
- **Coverage Target**: All success and error paths

### Test Cases

| # | Description | Type | Priority |
|---|-------------|------|----------|
| 1 | Create worktree succeeds | Integration | High |
| 2 | Create existing worktree fails | Integration | High |
| 3 | Status returns correct JSON | Integration | High |
| 4 | Finalize removes worktree | Integration | High |
| 5 | Finalize warns on uncommitted changes | Integration | Medium |
| 6 | Invalid feature-slug rejected | Unit | Medium |

## Dependencies

### Requires (blockedBy)
- None (foundation task)

### Blocks (blocks)
- **task-003**: step-00c-worktree needs these scripts
