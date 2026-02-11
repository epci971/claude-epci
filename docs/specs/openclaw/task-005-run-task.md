---
id: task-005
title: Implement single task executor
slug: run-task
feature: openclaw
complexity: L
estimated_minutes: 120
dependencies:
  - task-001
  - task-002
files_affected:
  - path: run-task.sh
    action: create
  - path: tests/test-run-task.sh
    action: create
test_approach: Integration
---

# Task 005: Implement single task executor

## Objective

Implement `run-task.sh` — the script that executes a single Notion task end-to-end: reads the spec content (from Notion body or Git file), creates a Git worktree, runs Claude Code headless (`claude -p`), parses the JSON result, creates a PR, and updates the Notion task status. This is the core execution unit called by the pipeline orchestrator.

---

## Context

Each task in Notion has either spec content in the page body (default, D1r) or a `Spec Path` property pointing to a Git file. The execution uses `claude -p` with `--output-format json` and `--permission-mode bypassPermissions` (section 8, headless constraint). The worktree pattern is fan-out from main (section 4.1). The JSON output from implement-auto follows the schema in `src/skills/implement-auto/references/output-json-schema.md`.

Key decisions from brief:
- D1r: Spec in Notion body by default, Git file if Spec Path is set
- US1-AC1/AC2/AC3: Success, failure, and partial handling
- Section 4.1: `extract_spec_content()` handles both sources
- Worktree: `git worktree add .worktrees/{slug} -b feature/{slug} origin/main`

---

## Acceptance Criteria

### AC1: Hybrid spec reading works

- **Given**: A Notion task with spec content in the page body (Spec Path empty)
- **When**: `extract_spec_content` is called with the task's page_id
- **Then**: Returns the Markdown content from the Notion page body

### AC2: Git spec fallback works

- **Given**: A Notion task with `Spec Path` set to `docs/specs/feature/task-001.md`
- **When**: `extract_spec_content` is called
- **Then**: Returns the content of the Git file

### AC3: Successful execution creates PR

- **Given**: A valid spec and available Claude Code quota
- **When**: `run_task` executes the task
- **Then**: A worktree is created, Claude Code runs implement-auto, a PR is created with `gh pr create`, the Notion task status is updated to "En review", and the PR URL is stored

### AC4: Failed execution is handled properly

- **Given**: A task where Claude Code fails (timeout, tests KO, etc.)
- **When**: `run_task` detects the failure from the JSON result
- **Then**: The worktree is cleaned up, the Notion task status is set to "Echoue" with the error message, and the function returns a failure status

### AC5: Partial execution creates draft PR

- **Given**: A task where implement-auto returns PARTIAL status
- **When**: `run_task` processes the result
- **Then**: A draft PR is created (`gh pr create --draft`), the Notion task is set to "En review (partiel)", and the notification includes the number of failed components

---

## Steps

### Step 1: Implement spec content extraction (30 min)

**Input**: Notion API (task-002), brief section 4.1

**Actions**:
1. Create `run-task.sh` sourcing `lib/common.sh`, `lib/config.sh`, `lib/notion.sh`
2. Implement `extract_spec_content()` accepting a task JSON object:
   - Read `Spec Path` property from task
   - If Spec Path is set and file exists: read file content, return it
   - If Spec Path is set but file missing: return error "Spec not found: {path}"
   - If Spec Path is empty: call `notion_read_body` to get page body content
   - If body is also empty: return error "No spec content: body empty and no Spec Path"
3. Return the spec Markdown content

**Output**: extract_spec_content function in run-task.sh

**Validation**: Correctly reads from both Notion body and Git file

### Step 2: Implement worktree management (30 min)

**Input**: Git worktree documentation, brief architecture

**Actions**:
1. Implement `create_worktree()` accepting task slug and project config:
   - `git fetch origin main`
   - `git worktree add ".worktrees/${slug}" -b "feature/${slug}" origin/main`
   - Return worktree path
2. Implement `cleanup_worktree()` accepting task slug:
   - `git worktree remove ".worktrees/${slug}" --force`
   - `git branch -D "feature/${slug}"` if PR not created
3. Handle edge cases: worktree already exists (cleanup first), branch already exists

**Output**: Worktree management functions

**Validation**: Can create and clean up worktrees without leaving artifacts

### Step 3: Implement Claude Code headless execution (30 min)

**Input**: Claude Code CLI docs, implement-auto output schema

**Actions**:
1. Implement `execute_claude()` accepting worktree path, spec content, and project config:
   ```bash
   claude -p "$PROMPT" \
     --output-format json \
     --allowedTools "Bash,Read,Write,Edit,Glob,Grep" \
     --permission-mode bypassPermissions \
     --max-turns 50
   ```
2. Build prompt from spec content: inject spec + instruction to use implement-auto skill
3. Capture JSON output, handle timeout (configurable, default 1800s)
4. Parse result JSON: extract `status` (SUCCESS/PARTIAL/FAILED), `metrics`, `errors`, `warnings`
5. Handle Claude Code crash: if no valid JSON, generate fallback JSON with error

**Output**: execute_claude function with JSON parsing

**Validation**: Parses sample implement-auto JSON output correctly

### Step 4: Implement PR creation and Notion updates (30 min)

**Input**: GitHub CLI docs, Notion update API (task-002)

**Actions**:
1. Implement `handle_success()` — push branch, create PR with `gh pr create`:
   - PR title: `[Pipeline] {task_title}`
   - PR body: Feature Document + summary from JSON result
   - Set labels, link to Notion task
2. Implement `handle_failure()` — cleanup worktree, update Notion:
   - Set Statut to "Echoue"
   - Set Erreurs to error message
   - Set Termine le to now
3. Implement `handle_partial()` — push branch, create draft PR:
   - `gh pr create --draft`
   - Set Statut to "En review (partiel)"
4. Implement main `run_task()` function that orchestrates the full flow
5. Write integration tests with mock Claude Code output

**Output**: Complete run-task.sh with all handlers

**Validation**: Full flow works with mock Claude Code output

---

## Files

| Path | Action | Description |
|------|--------|-------------|
| `run-task.sh` | create | Single task executor (spec reading → worktree → claude → PR → Notion) |
| `tests/test-run-task.sh` | create | Integration tests with mock Claude output |

---

## Test Approach

- **Type**: Integration
- **Framework**: bats or inline test functions
- **Location**: tests/test-run-task.sh
- **Coverage Target**: 75%

### Test Cases

| # | Description | Type | Priority |
|---|-------------|------|----------|
| 1 | extract_spec_content reads from Notion body | Integration | High |
| 2 | extract_spec_content reads from Git file | Integration | High |
| 3 | extract_spec_content fails on empty body and no Spec Path | Unit | High |
| 4 | handle_success creates PR and updates Notion | Integration | High |
| 5 | handle_failure cleans worktree and updates Notion | Integration | High |
| 6 | handle_partial creates draft PR | Integration | Medium |
| 7 | execute_claude handles timeout | Unit | Medium |
| 8 | execute_claude generates fallback JSON on crash | Unit | Medium |

---

## Dependencies

### Requires (blockedBy)

- **task-001**: Needs lib/common.sh and lib/config.sh for utilities and project config
- **task-002**: Needs lib/notion.sh for notion_read_body, notion_update

### Blocks

- **task-006**: Pipeline runner calls run_task for each task in the loop

---

## Notes

- The `claude -p` prompt should include the full spec content + a clear instruction to use implement-auto
- Worktree path `.worktrees/` should be in `.gitignore`
- PR body has a ~65K char limit on GitHub — truncate if needed and link to Feature Document
- The `--max-turns 50` default can be overridden in projects.json per project

---

*Task specification generated by /spec v1.0 — EPCI v6.0*
