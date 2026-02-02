---
id: task-002
title: Create Skill /ralph-exec
slug: ralph-exec
complexity: L
estimated_minutes: 120
dependencies: [task-001]
source_stories: [US2, US3]
test_approach: Integration
---

# Task 002: Create Skill /ralph-exec

## Objective

Create a new `/ralph-exec` skill that executes a single user story from a PRD.json file, following TDD workflow and emitting a RALPH_STATUS block for completion detection.

## Context

Ralph loops need to call a fresh Claude Code instance per story to avoid context buildup. The `/ralph-exec` skill receives the PRD path, identifies the next pending story, implements it with TDD, updates the PRD, and emits a structured status block.

## Acceptance Criteria

### AC1: Skill Structure
**Given** the skill directory
**When** created
**Then** it must contain: SKILL.md, steps/step-00-init.md, steps/step-01-execute.md, steps/step-02-report.md, references/status-block.md

### AC2: PRD Argument
**Given** the skill is invoked
**When** `--prd <path>` argument is provided
**Then** the skill must read and parse the PRD.json file

### AC3: Story Selection
**Given** a parsed PRD with multiple stories
**When** selecting next story
**Then** choose first story where `status: pending` AND `passes: false` AND all `depends_on` stories have `passes: true`

### AC4: TDD Execution
**Given** a story to execute
**When** implementing
**Then** follow RED-GREEN cycle (skip REFACTOR for speed): write failing test, implement to pass

### AC5: PRD Update
**Given** story execution completes
**When** writing results
**Then** update PRD.json with: `status`, `passes`, `execution.attempts++`, `execution.files_modified[]`, `execution.completed_at`

### AC6: RALPH_STATUS Emission
**Given** execution completes (success or failure)
**When** generating response
**Then** emit RALPH_STATUS block at end with all 7 fields

## Steps

### Step 1: Create SKILL.md (20min)
- **Input**: Brief requirements, skill template
- **Output**: Complete SKILL.md with frontmatter, rules, workflow
- **Validation**: Frontmatter valid, workflow diagram complete

### Step 2: Create step-00-init.md (25min)
- **Input**: PRD schema, dependency rules
- **Output**: Init step that parses PRD and selects next story
- **Validation**: Handles missing PRD, respects dependencies

### Step 3: Create step-01-execute.md (30min)
- **Input**: TDD enforcer patterns, story structure
- **Output**: Execute step with RED-GREEN cycle
- **Validation**: Tests written before implementation

### Step 4: Create step-02-report.md (25min)
- **Input**: RALPH_STATUS format, PRD update rules
- **Output**: Report step that updates PRD and emits status
- **Validation**: Status block parseable, PRD valid after update

### Step 5: Create references/status-block.md (20min)
- **Input**: RALPH_STATUS format from brief
- **Output**: Reference doc with format spec and examples
- **Validation**: All 7 fields documented with valid values

## Files

| Path | Action | Description |
|------|--------|-------------|
| src/skills/ralph-exec/SKILL.md | create | Main skill definition |
| src/skills/ralph-exec/steps/step-00-init.md | create | Initialization step |
| src/skills/ralph-exec/steps/step-01-execute.md | create | Execution step |
| src/skills/ralph-exec/steps/step-02-report.md | create | Reporting step |
| src/skills/ralph-exec/references/status-block.md | create | Status format reference |

## Dependencies

- **task-001**: PRD schema must be finalized to know userStory structure
