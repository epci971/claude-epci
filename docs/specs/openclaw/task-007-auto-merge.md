---
id: task-007
title: Implement auto-merge system
slug: auto-merge
feature: openclaw
complexity: M
estimated_minutes: 90
dependencies:
  - task-006
files_affected:
  - path: lib/automerge.sh
    action: create
  - path: .github/workflows/auto-merge-safe.yml
    action: create
  - path: pipeline-runner.sh
    action: modify
  - path: run-task.sh
    action: modify
  - path: tests/test-automerge.sh
    action: create
test_approach: Integration
---

# Task 007: Implement auto-merge system

## Objective

Implement the 3-level auto-merge system: Level 2 (GitHub auto-merge via `gh pr merge --auto --squash`), Level 3 (pipeline-safe label + GitHub Action auto-approve for simple tasks), and merge detection (health check detects merged PRs and updates Notion to "Termine"). This enables the pipeline to chain tasks without waiting for manual review.

---

## Context

The auto-merge system operates in 3 complementary levels (section 4.7). Level 1 (dependency management) is already handled by pipeline-runner.sh (task-006). Level 2 activates GitHub's native auto-merge after PR creation. Level 3 adds a `pipeline-safe` label for simple, successful tasks that triggers a GitHub Action to auto-approve. Prerequisites: "Allow auto-merge" must be ON in repo settings, and "Allow GitHub Actions to create and approve pull requests" must be enabled.

Key decisions from brief:
- D10: gh pr merge --auto --squash after PR creation
- D11: pipeline-safe label + GitHub Action for zero-intervention PRs
- US6-AC1/AC2/AC3: Auto-merge by default, safe PRs auto-approved, non-safe waits
- Flag `no_auto_merge` disables all auto-merge

---

## Acceptance Criteria

### AC1: Level 2 — GitHub auto-merge activated by default

- **Given**: A PR created by the pipeline, and the task does NOT have flag `no_auto_merge`
- **When**: `enable_auto_merge` is called after PR creation
- **Then**: `gh pr merge --auto --squash` is executed, and the log confirms "Auto-merge enabled for PR {url}"

### AC2: Level 3 — Safe PRs get auto-approve label

- **Given**: A PR for a task with complexity "Simple", JSON status SUCCESS, tests pass, 0 errors, and <=2 warnings
- **When**: `evaluate_pr_safety` runs
- **Then**: The label `pipeline-safe` is added to the PR, triggering the GitHub Action to auto-approve and merge

### AC3: Merge detection updates Notion

- **Given**: A PR that was previously "En review" has been merged (by auto-merge or manual)
- **When**: The health check runs at the start of a new cycle
- **Then**: The Notion task status is updated to "Termine", and `Auto-merged: true` is set if the merge was automatic

### AC4: no_auto_merge flag disables everything

- **Given**: A task with flag `no_auto_merge` in its Notion Flags property
- **When**: The task is processed
- **Then**: Neither `gh pr merge --auto` nor the `pipeline-safe` label is applied; the PR requires 100% manual review and merge

---

## Steps

### Step 1: Implement auto-merge functions (30 min)

**Input**: GitHub CLI docs, brief section 4.7

**Actions**:
1. Create `lib/automerge.sh` sourcing `lib/common.sh`
2. Implement `enable_auto_merge()` accepting PR URL and task flags:
   - Check if `no_auto_merge` flag is present → skip if yes
   - Run `gh pr merge "$PR_URL" --auto --squash`
   - Log result
3. Implement `evaluate_pr_safety()` accepting task JSON and implement-auto result JSON:
   - Criteria: complexity == "Simple" AND status == "SUCCESS" AND tests pass AND errors == 0 AND warnings <= 2
   - If all criteria met: return "safe"
   - Else: return "not_safe"
4. Implement `label_safe_pr()` accepting PR URL:
   - `gh pr edit "$PR_URL" --add-label "pipeline-safe"`

**Output**: Auto-merge helper functions

**Validation**: Correct label applied based on safety criteria

### Step 2: Create GitHub Action for auto-approve (30 min)

**Input**: GitHub Actions docs, brief D11

**Actions**:
1. Create `.github/workflows/auto-merge-safe.yml`:
   ```yaml
   name: Auto-approve pipeline-safe PRs
   on:
     pull_request:
       types: [labeled]
   jobs:
     auto-approve:
       if: github.event.label.name == 'pipeline-safe'
       runs-on: ubuntu-latest
       permissions:
         pull-requests: write
       steps:
         - uses: hmarr/auto-approve-action@v4
           with:
             github-token: ${{ secrets.GITHUB_TOKEN }}
   ```
2. Document prerequisites in a README section:
   - Repo settings: Allow auto-merge ON
   - Repo settings: Allow GitHub Actions to create and approve pull requests
   - Branch protection: Require 1 approval (GitHub Action provides it)
3. Test the workflow definition syntax with `actionlint` if available

**Output**: GitHub Action workflow file

**Validation**: YAML is valid, action triggers on correct label

### Step 3: Implement merge detection and integration (30 min)

**Input**: GitHub CLI docs for PR status, pipeline-runner health check

**Actions**:
1. Implement `detect_merged_prs()`:
   - Query Notion for tasks with status "En review" or "En review (partiel)" that have a PR URL
   - For each: check PR status via `gh pr view "$PR_URL" --json state,mergedAt`
   - If merged: update Notion to "Termine", set "Auto-merged" checkbox, set "Termine le" date
2. Integrate into pipeline-runner.sh health check (modify task-006):
   - Call `detect_merged_prs()` after orphan recovery
3. Integrate enable_auto_merge into run-task.sh handle_success (modify task-005):
   - After PR creation: call `enable_auto_merge()` and `evaluate_pr_safety()`
4. Write tests for safety evaluation logic and merge detection

**Output**: Complete auto-merge system with integration

**Validation**: Full flow: PR created → auto-merge enabled → safe label → merged → Notion updated

---

## Files

| Path | Action | Description |
|------|--------|-------------|
| `lib/automerge.sh` | create | Auto-merge helper functions (enable, evaluate, label) |
| `.github/workflows/auto-merge-safe.yml` | create | GitHub Action for auto-approving pipeline-safe PRs |
| `pipeline-runner.sh` | modify | Add detect_merged_prs to health check |
| `run-task.sh` | modify | Add enable_auto_merge and evaluate_pr_safety to handle_success |
| `tests/test-automerge.sh` | create | Tests for auto-merge logic |

---

## Test Approach

- **Type**: Integration
- **Framework**: bats or inline test functions
- **Location**: tests/test-automerge.sh
- **Coverage Target**: 80%

### Test Cases

| # | Description | Type | Priority |
|---|-------------|------|----------|
| 1 | enable_auto_merge runs gh pr merge --auto | Integration | High |
| 2 | no_auto_merge flag prevents auto-merge | Unit | High |
| 3 | evaluate_pr_safety returns "safe" for qualifying PRs | Unit | High |
| 4 | evaluate_pr_safety returns "not_safe" for complex tasks | Unit | High |
| 5 | detect_merged_prs updates Notion for merged PRs | Integration | High |
| 6 | GitHub Action YAML is valid | Unit | Medium |

---

## Dependencies

### Requires (blockedBy)

- **task-006**: Pipeline runner must exist for integration (health check, task loop)

### Blocks

*No other tasks depend on this one*

---

## Notes

- The GitHub Action uses `hmarr/auto-approve-action@v4` — verify this is the latest stable version
- The `pipeline-safe` label must be created in each target repo (can be done manually or via `gh label create`)
- Auto-merge requires CI to pass first — ensure repos have branch protection with required checks
- If GitHub Action fails (permissions issue): PR stays open, log ERROR, no retry

---

*Task specification generated by /spec v1.0 — EPCI v6.0*
