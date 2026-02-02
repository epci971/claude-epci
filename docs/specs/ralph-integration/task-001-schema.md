---
id: task-001
title: Update PRD Schema v2
slug: schema
complexity: M
estimated_minutes: 60
dependencies: []
source_stories: [US1]
test_approach: Unit
---

# Task 001: Update PRD Schema v2

## Objective

Update the `src/schemas/prd-v2.json` schema to use the `userStories[]` format with full execution tracking fields, replacing the current `tasks[]` structure for better Ralph integration.

## Context

The current prd-v2.json schema uses a `tasks[]` array focused on specification. For Ralph autonomous execution, we need `userStories[]` with additional fields: `passes`, `execution.attempts`, `acceptanceCriteria[].done`, etc.

## Acceptance Criteria

### AC1: Schema Structure
**Given** the prd-v2.json schema file
**When** it is validated
**Then** it must use `userStories[]` as the main array instead of `tasks[]`

### AC2: Execution Tracking Fields
**Given** a userStory object in the schema
**When** it is defined
**Then** it must include `execution` object with: `attempts`, `last_error`, `files_modified[]`, `completed_at`, `iteration`

### AC3: Status Tracking
**Given** a userStory object
**When** defined
**Then** it must include: `status` (enum: pending|in_progress|completed|failed|blocked) and `passes` (boolean)

### AC4: AC and Tasks Tracking
**Given** a userStory object
**When** defined
**Then** `acceptanceCriteria[]` and `tasks[]` items must have `done` boolean field

## Steps

### Step 1: Backup and Analyze Current Schema (15min)
- **Input**: Current src/schemas/prd-v2.json
- **Output**: Backup file, analysis of current structure
- **Validation**: Backup exists, current fields documented

### Step 2: Define userStory Object Schema (20min)
- **Input**: v5.6 ralph-converter reference, brief requirements
- **Output**: Complete userStory JSON Schema definition
- **Validation**: All 9 ACs from US1 covered in schema

### Step 3: Update Root Schema Structure (15min)
- **Input**: userStory schema, meta/config requirements
- **Output**: Updated prd-v2.json with new structure
- **Validation**: JSON Schema valid, includes meta, config, userStories, metrics

### Step 4: Write Unit Tests (10min)
- **Input**: Updated schema
- **Output**: Test file validating schema compliance
- **Validation**: Tests pass for valid/invalid examples

## Files

| Path | Action | Description |
|------|--------|-------------|
| src/schemas/prd-v2.json | modify | Update to userStories[] format |
| src/schemas/prd-v2.json.bak | create | Backup of original |
| src/scripts/test_prd_schema.py | create | Schema validation tests |

## Dependencies

None — this is a root task.
