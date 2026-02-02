---
id: task-006
title: Update /spec step-03
slug: spec-update
complexity: M
estimated_minutes: 60
dependencies: [task-004, task-005]
source_stories: [US6]
test_approach: Integration
---

# Task 006: Update /spec step-03

## Objective

Update the step-03-generate-ralph.md file to generate all Ralph artifacts using the new templates, ensuring the system is ready-to-execute at the end of /spec.

## Context

The current step-03 generates basic Ralph artifacts. We need to enhance it to use the new templates, generate PRD.json in userStories format, include circuit breaker, and update the registry.

## Acceptance Criteria

### AC1: PRD.json Generation
**Given** step-03 executes
**When** generating PRD
**Then** create `docs/specs/{slug}/{slug}.prd.json` using prd.json.template

### AC2: PROMPT.md Generation
**Given** step-03 executes
**When** generating PROMPT
**Then** create `.ralph/{slug}/PROMPT.md` with detected stack

### AC3: MEMORY.md Generation
**Given** step-03 executes
**When** generating MEMORY
**Then** create `.ralph/{slug}/MEMORY.md` initialized for all tasks

### AC4: ralph.sh Generation
**Given** step-03 executes
**When** generating script
**Then** create `.ralph/{slug}/ralph.sh` executable with circuit breaker

### AC5: Registry Update
**Given** step-03 completes
**When** artifacts generated
**Then** update `.ralph/index.json` with new feature entry

### AC6: Final Breakpoint
**Given** step-03 completes
**When** displaying summary
**Then** show execution command and routing recommendation

## Steps

### Step 1: Update Template Loading Logic (15min)
- **Input**: New template files from task-005
- **Output**: Step logic that reads and fills templates
- **Validation**: All placeholders replaced

### Step 2: Update PRD Generation (15min)
- **Input**: Task list, DAG, userStories format
- **Output**: Generation logic for prd.json
- **Validation**: Output validates against schema

### Step 3: Update Script Generation (15min)
- **Input**: ralph.sh.template from task-004
- **Output**: Generation with chmod +x
- **Validation**: Script executable, circuit breaker present

### Step 4: Update Breakpoint Display (15min)
- **Input**: Completion requirements
- **Output**: Breakpoint with execution command
- **Validation**: Routing recommendation correct

## Files

| Path | Action | Description |
|------|--------|-------------|
| src/skills/spec/steps/step-03-generate-ralph.md | modify | Update generation logic |

## Dependencies

- **task-004**: ralph.sh.template must exist
- **task-005**: All generation templates must exist
