---
id: task-004
title: Create ralph.sh Template
slug: ralph-script
complexity: M
estimated_minutes: 90
dependencies: [task-002, task-003]
source_stories: [US4]
test_approach: Integration
---

# Task 004: Create ralph.sh Template

## Objective

Create a complete ralph.sh template that loops through stories using `/ralph-exec`, includes the circuit breaker, parses RALPH_STATUS blocks, and supports command-line flags.

## Context

The ralph.sh script is the entry point for overnight autonomous execution. It must handle fresh context per story (via separate claude calls), detect completion/stuck states, log progress, and support operational flags.

## Acceptance Criteria

### AC1: Autonomous Mode
**Given** the script runs
**When** `--dangerously-skip-permissions` is used
**Then** execute without human intervention

### AC2: Loop with MAX_ITERATIONS
**Given** script configuration
**When** MAX_ITERATIONS env var or default
**Then** loop up to that limit (default 50)

### AC3: /ralph-exec Invocation
**Given** each iteration
**When** executing
**Then** call `claude --dangerously-skip-permissions "/ralph-exec --prd $PRD_FILE"`

### AC4: RALPH_STATUS Parsing
**Given** claude output
**When** parsing status
**Then** extract STATUS, EXIT_SIGNAL and decide continue/stop

### AC5: Progress Display
**Given** verbose mode (default)
**When** each iteration
**Then** display completed/total, elapsed time, current story

### AC6: CLI Flags
**Given** script arguments
**When** --quiet, --dry-run, --help provided
**Then** adjust behavior accordingly

### AC7: Progress Logging
**Given** each iteration
**When** completing
**Then** append timestamped entry to progress.txt

## Steps

### Step 1: Create Template Structure (20min)
- **Input**: ralph.sh template from v5.6, requirements
- **Output**: Template with placeholders {{FEATURE_SLUG}}, {{PRD_FILE}}, etc.
- **Validation**: All placeholders documented

### Step 2: Integrate Circuit Breaker (20min)
- **Input**: Circuit breaker snippet from task-003
- **Output**: Inline circuit breaker in template
- **Validation**: No external dependencies

### Step 3: Implement RALPH_STATUS Parser (25min)
- **Input**: Status block format from task-002
- **Output**: parse_ralph_status() function with dual-condition logic
- **Validation**: Handles all STATUS values and EXIT_SIGNAL

### Step 4: Add CLI Flags and Progress (25min)
- **Input**: UX requirements
- **Output**: Complete template with flags, colors, progress bar
- **Validation**: --help works, progress displays correctly

## Files

| Path | Action | Description |
|------|--------|-------------|
| src/skills/spec/templates/ralph.sh.template | create | Complete ralph.sh template |

## Dependencies

- **task-002**: RALPH_STATUS format must be defined
- **task-003**: Circuit breaker code must be ready
