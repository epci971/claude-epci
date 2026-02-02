---
id: task-005
title: Create Generation Templates
slug: templates
complexity: S
estimated_minutes: 45
dependencies: [task-001]
source_stories: [US7]
test_approach: Unit
---

# Task 005: Create Generation Templates

## Objective

Create template files for PRD.json, PROMPT.md, MEMORY.md with clear placeholders that /spec step-03 can fill during generation.

## Context

Templates ensure consistent artifact generation and make maintenance easier. Each template uses `{{VARIABLE}}` placeholders that are replaced during generation.

## Acceptance Criteria

### AC1: PRD.json Template
**Given** the template file
**When** used by step-03
**Then** produce valid JSON following prd-v2.json schema

### AC2: PROMPT.md Template
**Given** the template file
**When** generated
**Then** include feature context, stack guidelines, execution rules

### AC3: MEMORY.md Template
**Given** the template file
**When** initialized
**Then** include progress table, current task, files/tests/issues tables

### AC4: Variable Documentation
**Given** each template
**When** reviewed
**Then** all `{{VARIABLE}}` placeholders are documented in comments

## Steps

### Step 1: Create prd.json.template (15min)
- **Input**: Updated prd-v2.json schema from task-001
- **Output**: Template with userStories structure
- **Validation**: Parses as valid JSON when placeholders filled

### Step 2: Create prompt.md.template (15min)
- **Input**: Existing prompt template, stack guidelines
- **Output**: Template with feature/stack/rules sections
- **Validation**: All sections present, variables documented

### Step 3: Create memory.md.template (15min)
- **Input**: Memory tracking requirements
- **Output**: Template with state tracking tables
- **Validation**: Table headers correct, placeholders clear

## Files

| Path | Action | Description |
|------|--------|-------------|
| src/skills/spec/templates/prd.json.template | create | PRD template |
| src/skills/spec/templates/prompt.md.template | modify | Update with new format |
| src/skills/spec/templates/memory.md.template | modify | Update tracking tables |

## Dependencies

- **task-001**: PRD schema structure must be finalized
