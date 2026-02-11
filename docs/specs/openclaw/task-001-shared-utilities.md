---
id: task-001
title: Create shared utilities and project configuration
slug: shared-utilities
feature: openclaw
complexity: S
estimated_minutes: 75
dependencies: []
files_affected:
  - path: lib/common.sh
    action: create
  - path: lib/config.sh
    action: create
  - path: projects.json
    action: create
  - path: .env.example
    action: create
test_approach: Unit
---

# Task 001: Create shared utilities and project configuration

## Objective

Create the shared Bash utility library (logging, error handling, color output) and the multi-project configuration system (projects.json schema, .env loading, validation). This provides the foundation layer that all other scripts source.

---

## Context

The pipeline uses Bash + jq exclusively (D2). All scripts share common functions for logging, error handling, and configuration. The multi-project config (section 4.5) maps each project to its local directory, GitHub repo, Notion project ID, and default parameters. Secrets are stored in `.env` with 600 permissions (section 4.4).

Key decisions from brief:
- D2: curl/jq only, no Python, no framework
- D5: Dedicated spec directories per project
- Section 4.5: projects.json maps project → directory, repo, Notion ID, defaults

---

## Acceptance Criteria

### AC1: Logging functions work correctly

- **Given**: A script sources `lib/common.sh`
- **When**: It calls `log_info`, `log_warn`, `log_error`, `log_debug`
- **Then**: Messages are timestamped, color-coded (if terminal), and written to both stdout and a log file

### AC2: Environment loading validates secrets

- **Given**: A `.env` file with NOTION_API_KEY, GITHUB_TOKEN, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID
- **When**: `load_env()` is called
- **Then**: All required variables are exported, missing variables cause a named error

### AC3: projects.json is validated on load

- **Given**: A `projects.json` with entries for multiple projects
- **When**: `load_projects()` is called
- **Then**: Each entry is validated (required fields: slug, directory, github_repo, notion_project_id), invalid entries are reported, and the function returns a jq-parseable structure

### AC4: Project lookup resolves correctly

- **Given**: A valid projects.json and a project slug
- **When**: `get_project_config "gardel"` is called
- **Then**: Returns the project's directory, github_repo, notion_project_id, and default flags as JSON

---

## Steps

### Step 1: Create lib/common.sh — Logging and utility functions (25 min)

**Input**: Pipeline requirements for consistent logging and error handling

**Actions**:
1. Create `lib/common.sh` with shebang and `set -euo pipefail`
2. Implement `log_info`, `log_warn`, `log_error`, `log_debug` with ISO-8601 timestamps
3. Implement color output detection (isatty check)
4. Implement `log_to_file()` that appends to `$LOG_DIR/pipeline-$(date +%Y%m%d).log`
5. Implement `die()` function for fatal errors with cleanup
6. Implement `require_command()` to check for jq, curl, gh, git, claude

**Output**: lib/common.sh with all utility functions

**Validation**: Source the file and call each function without errors

### Step 2: Create lib/config.sh — Environment and project loading (25 min)

**Input**: .env format and projects.json schema from brief

**Actions**:
1. Create `lib/config.sh` that sources `lib/common.sh`
2. Implement `load_env()` that reads `.env`, exports variables, validates required keys
3. Implement `load_projects()` that reads and validates `projects.json`
4. Implement `get_project_config()` that returns a single project's config as JSON
5. Implement `validate_projects_json()` that checks all required fields per entry

**Output**: lib/config.sh with config management functions

**Validation**: Load a sample .env and projects.json, verify all values accessible

### Step 3: Create projects.json schema and .env.example (25 min)

**Input**: Section 4.5 of brief (multi-project config)

**Actions**:
1. Create `projects.json` with sample structure:
   ```json
   {
     "projects": [
       {
         "slug": "gardel",
         "directory": "/home/pipeline/apps/gardel",
         "github_repo": "epci971/gardel",
         "notion_project_id": "xxx-xxx-xxx",
         "defaults": {
           "model": "sonnet",
           "timeout": 1800,
           "flags": ["validate_plan"]
         }
       }
     ]
   }
   ```
2. Create `.env.example` with all required variables documented
3. Write unit tests: validate good JSON, reject malformed JSON, reject missing fields
4. Write unit tests: load_env with missing variable, load_env with all variables

**Output**: projects.json, .env.example, and test scripts

**Validation**: All unit tests pass

---

## Files

| Path | Action | Description |
|------|--------|-------------|
| `lib/common.sh` | create | Shared logging and utility functions |
| `lib/config.sh` | create | Environment and project configuration loader |
| `projects.json` | create | Multi-project configuration (sample with gardel) |
| `.env.example` | create | Template for required environment variables |

---

## Test Approach

- **Type**: Unit
- **Framework**: bats (Bash Automated Testing System) or inline test functions
- **Location**: tests/test-common.sh, tests/test-config.sh
- **Coverage Target**: 80%

### Test Cases

| # | Description | Type | Priority |
|---|-------------|------|----------|
| 1 | log_info outputs timestamped message | Unit | High |
| 2 | log_error writes to stderr | Unit | High |
| 3 | load_env fails on missing required variable | Unit | High |
| 4 | load_projects validates JSON structure | Unit | High |
| 5 | get_project_config returns correct project | Unit | Medium |
| 6 | require_command fails on missing command | Unit | Medium |

---

## Dependencies

### Requires (blockedBy)

*No dependencies — this task can start immediately*

### Blocks

- **task-005**: Task executor needs config and utility functions
- **task-006**: Pipeline runner needs config and utility functions

---

## Notes

- `set -euo pipefail` is mandatory in all scripts (defensive Bash)
- Log rotation (7 days) is a Could Have — can be added as a cron job later
- projects.json should include a `"version": "1.0"` field for future schema evolution

---

*Task specification generated by /spec v1.0 — EPCI v6.0*
