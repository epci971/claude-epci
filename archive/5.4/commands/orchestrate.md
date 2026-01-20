---
description: >-
  Execute batch of EPCI specs with DAG-based dependency ordering,
  priority sorting, and auto-retry. Dual journaling (MD+JSON).
  Use for overnight automated implementation of multiple specs.
argument-hint: "<specs-dir> [--dry-run] [--continue] [--max-retries N] [--skip S01,S02] [--only S01] [--no-commit] [--verbose]"
allowed-tools: [Read, Write, Edit, Bash, Grep, Glob, Task]
---

# EPCI Orchestrate

> **⚠️ DEPRECATION NOTICE**: For overnight autonomous execution, consider using `/ralph` instead.
> Ralph Wiggum provides better safety features (circuit breaker, rate limiting) and is optimized
> for unattended multi-hour execution. `/orchestrate` remains available for DAG-based batch
> execution with user supervision.

## Overview

Automates the execution of multiple EPCI specs from a directory. Parses INDEX.md
for dependencies, builds a DAG, sorts by priority and effort, then executes each
spec sequentially with auto-retry on failure.

**Use case**: Launch before leaving, return to find all features implemented,
tested, and committed.

## Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `<specs-dir>` | Directory containing INDEX.md and spec files | Required |
| `--dry-run` | Show execution plan without running | false |
| `--continue` | Resume interrupted orchestration | false |
| `--max-retries N` | Max retries per spec | 3 |
| `--skip S01,S02` | Skip specific specs | - |
| `--only S01` | Execute only specific specs | - |
| `--no-commit` | Disable automatic commits | false |
| `--verbose` | Detailed real-time logging | false |
| `--no-hooks` | Disable all hook execution | false |

## Configuration

| Element | Value |
|---------|-------|
| **Thinking** | `think hard` (LARGE batch) |
| **Skills** | orchestrator-batch, project-memory, epci-core, breakpoint-display |
| **Subagents** | None (invokes /brief, /epci, /quick internally) |

## Process

### Phase 0: Load Context

**Skill**: `project-memory`

Load project context and check for interrupted orchestration state.

```
IF --continue AND checkpoint exists:
   → Load checkpoint from .project-memory/orchestration/
   → Resume from last incomplete spec
ELSE:
   → Fresh start
```

### Phase 1: Parse & Validate (MANDATORY)

**Read INDEX.md** and extract:
- Spec IDs, titles, effort estimates
- Dependencies between specs
- Priority overrides (optional field)

**Validation checks:**
- INDEX.md exists and is valid markdown
- All referenced spec files exist
- No circular dependencies in DAG

```
IF validation fails:
   ╔══════════════════════════════════════════════════════════════╗
   ║ ❌ ERROR: [Specific error message]                           ║
   ╠══════════════════════════════════════════════════════════════╣
   ║ [Details and suggestions]                                    ║
   ╚══════════════════════════════════════════════════════════════╝
   ABORT
```

### Phase 2: Build Execution Plan

**Reference**: `dag-building.md`, `priority-sorting.md`

1. **Build DAG** using `dag_builder.py`
2. **Sort specs** at same DAG level by:
   - Priority (1-99, lower = higher priority)
   - Effort (TINY < SMALL < STANDARD < LARGE)
   - Alphabetical (tiebreaker)
3. **Propagate priority** if high-priority spec depends on lower-priority spec
4. **Calculate estimates** per spec

### Phase 3: Interactive Plan (MANDATORY BREAKPOINT)

**MANDATORY:** Display the execution plan via `@skill:breakpoint-display` and WAIT for user validation.

**Skill**: `breakpoint-display`

```yaml
@skill:breakpoint-display
  type: interactive-plan
  title: "ORCHESTRATION PLAN"
  data:
    specs_count: {N}
    specs:
      - {order: 1, id: "S02-xxx", effort: "2h", priority: 1, deps: "-", est: "15min"}
      - {order: 2, id: "S01-xxx", effort: "4h", priority: "2*", deps: "-", est: "25min"}
      - {order: 3, id: "S03-xxx", effort: "3h", priority: "-", deps: "S01,S02", est: "20min"}
    notes: ["* Priority inherited from dependent"]
    total_time: "{TIME}"
    max_retries: {N}
  ask:
    question: "Comment souhaitez-vous procéder ?"
    header: "🚀 Exécution"
    options:
      - {label: "Lancer (Recommended)", description: "Démarrer l'exécution du plan"}
      - {label: "Modifier", description: "Ajuster priorités ou ordre"}
      - {label: "Skip specs", description: "Ignorer certaines specs"}
      - {label: "Annuler", description: "Abandonner l'orchestration"}
```

**Si choix "Modifier":** Demander les modifications via AskUserQuestion.

**Si choix "Skip specs":** Demander la liste des specs à ignorer.

**--dry-run behavior**: Display plan and exit without executing.

### Phase 4: Execution Loop

**Reference**: `auto-retry-strategy.md`

For each spec in order:

```
┌─────────────────────────────────────────────────────────────────────┐
│ 📦 SPEC: {ID} — {Title}                                             │
│ ├── Effort: {EFFORT}                                               │
│ ├── Dependencies: {DEPS or "None"}                                 │
│ └── Status: STARTING                                               │
└─────────────────────────────────────────────────────────────────────┘

1. Check dependencies resolved (or skip if not)
2. Invoke /brief with spec content
3. Follow routing to /epci or /quick (--autonomous mode)
4. Run validation (tests + lint)
5. IF validation fails:
   - Retry up to max-retries with error context
   - If all retries fail: mark FAILED, log, continue
6. IF validation passes:
   - Auto-commit (unless --no-commit)
   - Update INDEX.md progress
7. Save checkpoint
8. Clear context for next spec
```

**Timeout per spec:**
| Complexity | Timeout |
|------------|---------|
| TINY | 15 min |
| SMALL | 30 min |
| STANDARD | 1 hour |
| LARGE | 2 hours |

### Phase 5: Journaling

**Reference**: `dual-journaling.md`

Write journals in real-time:

1. **Markdown journal** (`orchestration-journal.md`)
   - Human-readable format
   - Updated after each spec

2. **JSON journal** (`orchestration-journal.json`)
   - Machine-parseable
   - Full metrics and timing

3. **INDEX.md update**
   - Progress column updated in real-time

### Phase 6: Report

Generate final report (`orchestration-report.md`):

```markdown
# Orchestration Report — {DATE}

## Summary
| Metric | Value |
|--------|-------|
| Total Specs | {N} |
| Succeeded | {N} ({%}) |
| Failed | {N} |
| Skipped | {N} |
| Duration | {TIME} |
| Commits | {N} |

## Results by Spec
[Table with status, duration, retries, commit]

## Errors Encountered
[Details of any failures]

## Recommendations
[Suggestions based on results]
```

## Error Handling

| Error | Action |
|-------|--------|
| INDEX.md missing | Abort with clear message |
| Spec file missing | Skip spec, warn, continue |
| Cycle in DAG | Abort with cycle visualization |
| Git conflict | Abort, require manual intervention |
| All specs failed | Complete run, report 0/N, exit code 1 |
| Timeout | Skip spec, mark "timeout" |

## Hooks

| Hook | Trigger | Context |
|------|---------|---------|
| `pre-orchestrate` | Before Phase 4 | specs_count, plan |
| `post-spec` | After each spec | spec_id, status, duration |
| `post-orchestrate` | After Phase 6 | summary, journal_path |

## See Also

- `/ralph` — **Recommended** for overnight autonomous execution (safer, optimized)
- Skill: `orchestrator-batch` for detailed logic
- References: `dag-building.md`, `priority-sorting.md`, `auto-retry-strategy.md`, `dual-journaling.md`
