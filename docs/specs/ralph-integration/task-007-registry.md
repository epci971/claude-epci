---
id: task-007
title: Create Registry index.json
slug: registry
complexity: S
estimated_minutes: 30
dependencies: [task-006]
source_stories: [US8]
test_approach: Unit
---

# Task 007: Create Registry index.json

## Objective

Create the JSON schema for `.ralph/index.json` registry and implement the creation/update logic in /spec step-03.

## Context

The registry tracks all Ralph-enabled features in the project, their status, and paths to artifacts. This enables listing available features and checking their completion status.

## Acceptance Criteria

### AC1: Schema Definition
**Given** the schema file
**When** validated
**Then** include: slug, title, created_at, status, complexity, stories_count, spec_path, ralph_path, prd_path

### AC2: Status Enum
**Given** a feature entry
**When** status is set
**Then** must be one of: ready, running, completed, paused, failed

### AC3: No Duplicates
**Given** step-03 runs
**When** adding a feature
**Then** check for existing slug and update instead of duplicate

### AC4: Auto-Creation
**Given** no index.json exists
**When** step-03 runs
**Then** create new file with single feature entry

## Steps

### Step 1: Create JSON Schema (15min)
- **Input**: Registry requirements from brief
- **Output**: src/schemas/ralph-index-v1.json
- **Validation**: Schema valid, all fields documented

### Step 2: Implement Update Logic (15min)
- **Input**: Schema, step-03 context
- **Output**: Logic to read/create/update index.json
- **Validation**: Handles create, update, no-duplicate cases

## Files

| Path | Action | Description |
|------|--------|-------------|
| src/schemas/ralph-index-v1.json | create | Registry JSON schema |
| src/skills/spec/steps/step-03-generate-ralph.md | modify | Add registry update logic |

## Dependencies

- **task-006**: step-03 must be updated to call registry logic
