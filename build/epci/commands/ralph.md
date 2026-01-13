---
description: >-
  Execute Ralph Wiggum autonomous loop for overnight feature development.
  Supports two modes: hook (same session, simple) and script (fresh context, robust).
  Use for complex features that can run autonomously for hours.
argument-hint: "<specs-dir> [--mode hook|script] [--max-iterations N] [--dry-run] [--overnight] [--safety-level minimal|moderate|strict]"
allowed-tools: [Read, Write, Edit, Bash, Grep, Glob, Task]
---

# EPCI Ralph

## Overview

Execute autonomous feature development using the Ralph Wiggum methodology.
Ralph loops continuously through user stories until all are complete or a
stopping condition is met.

**Key innovation**: Two execution modes for different use cases.

| Mode | Context | Best for | Robustness |
|------|---------|----------|------------|
| `hook` | Same session | Short runs (<2h) | Medium |
| `script` | Fresh each iteration | Overnight (>2h) | High |

## Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `<specs-dir>` | Directory with prd.json and specs | Required |
| `--mode` | Execution mode: `hook` or `script` | Auto-select |
| `--max-iterations` | Maximum loop iterations | 50 |
| `--dry-run` | Show plan without executing | false |
| `--continue` | Resume from checkpoint | false |
| `--overnight` | Force script mode + safety | false |
| `--safety-level` | Security level | moderate |
| `--calls` | Rate limit per hour | 100 |
| `--reset-circuit` | Reset circuit breaker state | false |
| `--no-hooks` | Disable hook execution | false |

## Configuration

| Element | Value |
|---------|-------|
| **Thinking** | `think hard` |
| **Skills** | ralph-converter, ralph-analyzer, project-memory, epci-core |
| **Subagents** | @ralph-executor |
| **Hooks** | ralph-session-init, ralph-iteration, ralph-stop |

## Pre-Workflow: Validation

### Step 1: Check Prerequisites

```
IF NOT exists(<specs-dir>/prd.json):
   ╔══════════════════════════════════════════════════════════════╗
   ║ ❌ ERROR: prd.json not found                                  ║
   ╠══════════════════════════════════════════════════════════════╣
   ║ Ralph requires a prd.json file with user stories.            ║
   ║                                                              ║
   ║ Generate it with:                                            ║
   ║ → /decompose <PRD.md> --wiggum                               ║
   ╚══════════════════════════════════════════════════════════════╝
   ABORT
```

### Step 2: Load prd.json

Read and validate structure:
- `branchName`: string
- `userStories`: array of objects with id, title, passes, priority, acceptanceCriteria

### Step 3: Mode Selection

```
IF --mode specified:
   → Use specified mode
ELIF --overnight:
   → Use script mode
ELIF stories.count < 10 AND estimated_duration < 2h:
   → Use hook mode
ELSE:
   → Use script mode

Display:
┌─────────────────────────────────────────────────────────────────────┐
│ 🔄 MODE SÉLECTIONNÉ: {MODE}                                         │
├─────────────────────────────────────────────────────────────────────┤
│ Raison: {REASON}                                                   │
│ Stories: {COUNT} ({PENDING} pending)                               │
│ Durée estimée: {DURATION}                                          │
│ Max iterations: {MAX}                                              │
└─────────────────────────────────────────────────────────────────────┘
```

## Process: Mode Hook

### Hook Mode Overview

Uses Claude Code's stop hook mechanism to intercept exits and reinject prompts.
Context is preserved between iterations (same session).

### Step H1: Initialize State File

Create `.claude/ralph-loop.local.md`:

```yaml
---
iteration: 1
max_iterations: {MAX}
completion_promise: "COMPLETE"
mode: hook
started_at: {TIMESTAMP}
status: RUNNING
stories_completed: 0
stories_total: {COUNT}
---

{PROMPT_CONTENT}
```

### Step H2: Start Loop

```bash
# Hook mode runs within Claude Code session
# Stop hook intercepts exit and reinjects prompt
```

The stop hook (`ralph-stop-hook.sh`) will:
1. Read state file
2. Check for `<promise>COMPLETE</promise>` in output
3. If not complete and iteration < max: increment and reinject
4. If complete or max reached: allow exit

### Step H3: Completion Detection

Loop continues until:
- `<promise>COMPLETE</promise>` detected
- max_iterations reached
- `/cancel-ralph` invoked

## Process: Mode Script

### Script Mode Overview

Uses external bash script with fresh Claude context per iteration.
More robust for long-running overnight sessions.

### Step S1: Generate ralph.sh

If not exists, generate from template:

```bash
#!/bin/bash
# Generated by /ralph for {PROJECT}
set -e
source lib/circuit_breaker.sh
source lib/response_analyzer.sh

MAX_ITERATIONS={MAX}
for ((i=1; i<=MAX_ITERATIONS; i++)); do
    # Check circuit breaker
    if should_halt_execution; then exit 1; fi

    # Run Claude
    OUTPUT=$(claude --print -f PROMPT.md -f prd.json -f progress.txt)

    # Analyze response
    EXIT_DECISION=$(analyze_response "$OUTPUT" "$i")

    case "$EXIT_DECISION" in
        project_complete) exit 0 ;;
        blocked) exit 2 ;;
        max_iterations) exit 1 ;;
    esac

    # Update circuit breaker
    FILES_CHANGED=$(git diff --name-only | wc -l)
    record_loop_result "$i" "$FILES_CHANGED" "false"
done
```

### Step S2: Execute Script

```bash
cd <specs-dir>
./ralph.sh
```

### Step S3: Monitor Progress

Display real-time status:

```
┌─────────────────────────────────────────────────────────────────────┐
│ 🔄 RALPH LOOP — Iteration {N}/{MAX}                                 │
├─────────────────────────────────────────────────────────────────────┤
│ Story: {CURRENT_STORY}                                             │
│ Status: {IN_PROGRESS|TESTING|COMMITTING}                           │
│ Progress: {COMPLETED}/{TOTAL} stories                              │
│ Circuit Breaker: {CLOSED|HALF_OPEN}                                │
│ Rate: {CALLS}/{LIMIT} this hour                                    │
└─────────────────────────────────────────────────────────────────────┘
```

## @ralph-executor Integration

For each story, invoke @ralph-executor:

```
Task: Execute story {STORY_ID}
Input:
  - Story JSON from prd.json
  - Parent spec context (S0X.md)
  - Project memory

@ralph-executor will:
  1. Call /brief with story as input
  2. Route to /quick (TINY/SMALL) or /epci (STANDARD+)
  3. Execute autonomously (--autonomous flag)
  4. Return result (pass/fail/blocked)
```

## Circuit Breaker Integration

The Circuit Breaker pattern prevents runaway loops:

| State | Trigger | Action |
|-------|---------|--------|
| CLOSED | Normal | Continue execution |
| HALF_OPEN | 2 loops no progress | Monitor closely |
| OPEN | 3+ loops no progress | Halt execution |

**Thresholds** (configurable):
- `CB_NO_PROGRESS_THRESHOLD`: 3 loops without file changes
- `CB_SAME_ERROR_THRESHOLD`: 5 loops with same error

## RALPH_STATUS Block

Claude MUST output this block at end of each iteration:

```
---RALPH_STATUS---
STATUS: IN_PROGRESS | COMPLETE | BLOCKED
TASKS_COMPLETED_THIS_LOOP: <number>
FILES_MODIFIED: <number>
TESTS_STATUS: PASSING | FAILING | NOT_RUN
WORK_TYPE: IMPLEMENTATION | TESTING | DOCUMENTATION | REFACTORING
EXIT_SIGNAL: false | true
RECOMMENDATION: <one line summary>
---END_RALPH_STATUS---
```

**EXIT_SIGNAL Rules**:
- `false`: Continue to next iteration
- `true`: Stop loop (project complete)
- EXIT_SIGNAL has priority over heuristic detection

## Safety Levels

| Level | Features |
|-------|----------|
| `minimal` | Max iterations only |
| `moderate` | + Rate limiting, circuit breaker |
| `strict` | + Sandbox mode, restricted commands |

## --dry-run Output

```
┌─────────────────────────────────────────────────────────────────────┐
│ 📋 RALPH DRY RUN — Execution Plan                                   │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│ Mode: {hook|script}                                                │
│ Stories: {PENDING} pending / {TOTAL} total                         │
│ Max iterations: {MAX}                                              │
│ Safety level: {LEVEL}                                              │
│                                                                     │
│ Execution order:                                                   │
│ 1. {STORY_1} — {TITLE} ({PRIORITY})                               │
│ 2. {STORY_2} — {TITLE} ({PRIORITY})                               │
│ ...                                                                │
│                                                                     │
│ Estimated duration: {HOURS}h                                       │
│ Estimated cost: ~${COST}                                           │
│                                                                     │
├─────────────────────────────────────────────────────────────────────┤
│ Launch with: /ralph <specs-dir> (remove --dry-run)                 │
└─────────────────────────────────────────────────────────────────────┘
```

## Completion

```
┌─────────────────────────────────────────────────────────────────────┐
│ ✅ RALPH COMPLETE                                                   │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│ Stories completed: {COMPLETED}/{TOTAL}                             │
│ Iterations used: {ITERATIONS}                                      │
│ Duration: {DURATION}                                               │
│ Commits: {COMMITS}                                                 │
│                                                                     │
│ Failed stories:                                                    │
│ • {STORY_ID}: {REASON}                                            │
│                                                                     │
│ Next steps:                                                        │
│ → Review commits: git log --oneline -n {COMMITS}                   │
│ → Check failed stories manually                                    │
│ → Create PR: gh pr create                                          │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

## Error Handling

| Error | Action |
|-------|--------|
| prd.json missing | Suggest /decompose --wiggum |
| All stories already pass | Exit with success message |
| Circuit breaker open | Show status, suggest --reset-circuit |
| Rate limit reached | Wait for reset, show countdown |
| Git conflict | Abort, require manual resolution |

## See Also

- `/decompose --wiggum` — Generate prd.json from PRD
- `/cancel-ralph` — Cancel active loop
- `/orchestrate` — Legacy batch execution (deprecated)
