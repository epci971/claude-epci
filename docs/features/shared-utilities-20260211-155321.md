# Feature: shared-utilities

## Metadata

| Champ | Valeur |
|-------|--------|
| Slug | shared-utilities |
| Date | 2026-02-11 15:53 |
| Branche | feature/shared-utilities |
| Spec source | docs/specs/openclaw/task-001-shared-utilities.md |
| Status | COMPLETED |
| Mode | implement-auto (headless) |

## Objectif

Create the shared Bash utility library (logging, error handling, color output) and the multi-project configuration system (projects.json schema, .env loading, validation). This provides the foundation layer that all other scripts source.

## Criteres d'acceptation

- [x] AC1: Logging functions (log_info, log_warn, log_error, log_debug) output timestamped, color-coded messages to stdout and log file
- [x] AC2: load_env() validates required secrets (NOTION_API_KEY, GITHUB_TOKEN, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID), fails with named error on missing
- [x] AC3: load_projects() validates projects.json structure (required fields: slug, directory, github_repo, notion_project_id)
- [x] AC4: get_project_config() returns correct project config as JSON for a given slug

## Plan d'implementation

> Auto-generated from step-02-plan-auto

| # | Composant | Fichier | Dependances | Status |
|---|-----------|---------|-------------|--------|
| 1 | common-sh | lib/common.sh | - | SUCCESS |
| 2 | projects-json | projects.json | - | SUCCESS |
| 3 | env-example | .env.example | - | SUCCESS |
| 4 | config-sh | lib/config.sh | common-sh, projects-json, env-example | SUCCESS |

### Strategie de test
- Framework: Custom Bash test harness (pass/fail counters, assertions)
- Commande: `bash tests/test-common.sh && bash tests/test-config.sh`
- Approche: TDD RED-GREEN-REFACTOR par composant

## Implementation Log

> Updated incrementally by step-03-code-auto

### Component: common-sh
- Status: SUCCESS
- Tests: 12 (12 pass, 0 fail)
- File: lib/common.sh
- TDD: RED (lib missing) -> GREEN (12/12 pass)

### Component: projects-json
- Status: SUCCESS
- Tests: N/A (data file)
- File: projects.json

### Component: env-example
- Status: SUCCESS
- Tests: N/A (data file)
- File: .env.example

### Component: config-sh
- Status: SUCCESS
- Tests: 9 (9 pass, 0 fail)
- File: lib/config.sh
- TDD: RED (lib missing) -> GREEN (9/9 pass)

## Review

> Auto-generated from step-04-review-auto

### Self-Review Results
- Status: pass
- Checks: 10/10 passed
- Findings: 0 warnings

| Check | Result |
|-------|--------|
| T1: All tests pass | PASS (21/21) |
| T2: Tests exist per component | PASS |
| T5: No skipped tests | PASS |
| C1: No debug prints | PASS |
| C2: No hardcoded secrets | PASS |
| C4: No TODO/FIXME | PASS |
| S1: No SQL injection | PASS (N/A) |
| S2: No command injection | PASS |
| S4: No sensitive data in logs | PASS |
| A1: Follows existing patterns | PASS |

## Resume Executif

Implemented the shared Bash utility library and multi-project configuration system as the foundation layer for the OpenClaw pipeline. Two core libraries were created: `lib/common.sh` provides logging functions (log_info, log_warn, log_error, log_debug) with ISO-8601 timestamps, color-coded terminal output, and dual output to stdout/stderr and log files, along with `die()` for fatal errors and `require_command()` for dependency checking. `lib/config.sh` provides `load_env()` for .env file loading with required variable validation, `load_projects()` for projects.json parsing with structural validation, and `get_project_config()` for slug-based project lookup returning JSON.

The library follows existing codebase conventions: color codes matching the archive pattern, function documentation style, and local variable scoping. The library is designed as a pure function collection (no global shell option changes) so sourcing scripts retain control over their own `set -euo pipefail` behavior. The test approach uses the custom Bash test harness pattern already established in the project (pass/fail counters, assertions).

All 4 acceptance criteria are met, with 21 unit tests covering logging output, timestamps, level markers, file writing, error handling, env loading/validation, JSON structure validation, and project config lookup. Self-review passed all 10 checks with zero findings.

### Metriques

| Metrique | Valeur |
|----------|--------|
| Fichiers crees | 6 |
| Fichiers modifies | 0 |
| Tests ajoutes | 21 |
| Tests passants | 21 |
| Tests echoues | 0 |
| Composants reussis | 4/4 |
