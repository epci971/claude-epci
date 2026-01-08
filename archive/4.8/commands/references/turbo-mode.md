# Turbo Mode Reference

> Speed-optimized workflow mode for experienced projects.

## Overview

`--turbo` reduces workflow time by 30-50% by:
- Using faster models for non-critical tasks
- Running reviews in parallel
- Reducing breakpoints
- Auto-accepting high-confidence suggestions

## Agent Distribution

| Agent | Model | Role |
|-------|-------|------|
| @clarifier | **haiku** | Fast clarification |
| @planner | **sonnet** | Rapid planning |
| @implementer | **sonnet** | Code execution |
| @plan-validator | **opus** | Critical validation |
| @code-reviewer | **opus** | Quality validation |
| @security-auditor | **opus** | Security validation |
| @qa-reviewer | **sonnet** | Test review |
| @doc-generator | **sonnet** | Documentation |

## Command-Specific Behavior

### /brief --turbo
- @Explore with Haiku model
- Maximum 2 clarification questions
- Auto-accept suggestions if confidence > 0.7

### /epci --turbo
- @planner for Phase 1 (skip manual planning)
- @implementer for Phase 2 (task-by-task execution)
- Parallel reviews (single Task call with multiple agents)
- Single breakpoint (pre-commit only)
- Auto-fix minor issues

### /quick --turbo
- @implementer for SMALL features
- Skip optional review
- Auto-commit suggestion

### /brainstorm --turbo
- @clarifier for questions (Haiku)
- Maximum 3 iterations
- Auto-finish if EMS > 60

### /debug --turbo
- Haiku for initial diagnostic
- Single solution (no scoring)
- Auto-apply best solution
- Skip breakpoint if confidence > 70%

## Parallel Reviews Pattern

```
⚠️ MANDATORY in turbo mode: Launch ALL reviews in SINGLE message:

Task 1: @code-reviewer (opus)
Task 2: @security-auditor (opus) — if applicable
Task 3: @qa-reviewer (sonnet) — if applicable

DO NOT run sequentially.
```

## Auto-Activation

Turbo is **suggested** (not auto-activated) when:
- `.project-memory/` exists (experienced project)
- Category is not LARGE
- Coming from /brainstorm with EMS > 60

## Precedence

| Combination | Result |
|-------------|--------|
| `--turbo` + `--large` | Warning, `--large` wins |
| `--turbo` + `--ultrathink` | `--ultrathink` overrides |
| `--turbo` + `--safe` | Both active |
