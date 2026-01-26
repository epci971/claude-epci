---
id: task-001
title: Update SKILL.md Structure
slug: skill-md-structure
feature: skill-implement
complexity: M
estimated_minutes: 90
dependencies: []
files_affected:
  - path: src/skills/implement/SKILL.md
    action: modify
test_approach: Manual
---

# Task 001: Update SKILL.md Structure

## Objective

Update the main SKILL.md file structure to accommodate new sections for stack skills integration, enhanced mandatory rules, and improved workflow overview. This establishes the foundation for all subsequent tasks.

---

## Context

The current SKILL.md has a basic structure but lacks:
- Explicit mandatory rules for stack skills usage
- Placeholder for the new "Stack & Core Skills Integration" section
- Updated workflow overview with 4 breakpoints
- Mode turbo documentation in decision tree

Key decisions from brief:
- D4: Triple couverture (section + rules + steps)
- D5: 4 breakpoints (E, P, C*, I)
- D9: Mode turbo supported

---

## Acceptance Criteria

### AC1: Frontmatter Updated

- **Given**: The existing SKILL.md frontmatter
- **When**: The task is complete
- **Then**: Description mentions stack skills, core skills integration, and plan-first workflow clearly

### AC2: Mandatory Rules Enhanced

- **Given**: The MANDATORY EXECUTION RULES section
- **When**: Updated with stack skills rules
- **Then**: At least 2 new rules explicitly mention stack skills loading and core skills invocation

### AC3: Workflow Overview Updated

- **Given**: The current workflow ASCII diagram
- **When**: Enhanced with breakpoint markers
- **Then**: Shows 4 breakpoints clearly marked (E, P, C*, I) with LARGE annotation for C

### AC4: Section Placeholder Added

- **Given**: Current section order in SKILL.md
- **When**: Placeholder added
- **Then**: "Stack & Core Skills Integration" section appears after "Workflow Overview" with TODO marker

---

## Steps

### Step 1: Analyze Current Structure (15 min)

**Input**: Current SKILL.md content

**Actions**:
1. Read current SKILL.md
2. Identify all existing sections
3. Map current mandatory rules
4. Note token count baseline

**Output**: Analysis notes for modification plan

**Validation**: Clear understanding of current structure

---

### Step 2: Update Frontmatter Description (20 min)

**Input**: Analysis notes, brief decisions

**Actions**:
1. Enhance description to explicitly mention:
   - Stack skills auto-injection
   - Core skills integration
   - Plan-first workflow support
2. Keep under 1024 characters
3. Maintain trigger words for routing

**Output**: Updated frontmatter

**Validation**: Description accurately reflects v6 capabilities

---

### Step 3: Enhance Mandatory Rules (25 min)

**Input**: Current mandatory rules, decisions D1, D3, D11

**Actions**:
1. Add rule: "ALWAYS load detected stack skills rules in INIT phase"
2. Add rule: "ALWAYS invoke core skills at designated phases"
3. Add rule: "NEVER skip pre-code TDD check for STANDARD+ complexity"
4. Ensure rules are in red/critical section
5. Add emoji markers consistent with existing rules

**Output**: Enhanced mandatory rules section

**Validation**: 3 new rules added, formatting consistent

---

### Step 4: Update Workflow Overview (20 min)

**Input**: Current workflow ASCII, decision D5

**Actions**:
1. Add BREAKPOINT markers at E, P, C*, I phases
2. Add note "(LARGE only)" for C phase breakpoint
3. Update step descriptions to reference stack/core skills
4. Ensure ASCII renders correctly in terminal

**Output**: Updated workflow ASCII diagram

**Validation**: 4 breakpoints visible, LARGE annotation present

---

### Step 5: Add Section Placeholder (10 min)

**Input**: Updated SKILL.md

**Actions**:
1. Add "## Stack & Core Skills Integration" section after Workflow Overview
2. Add TODO marker: "<!-- TODO: task-002 will populate this section -->"
3. Add brief description of what section will contain
4. Verify section order is logical

**Output**: SKILL.md with placeholder section

**Validation**: Section exists, TODO visible, structure coherent

---

## Files

| Path | Action | Description |
|------|--------|-------------|
| `src/skills/implement/SKILL.md` | modify | Main skill file structure update |

---

## Test Approach

- **Type**: Manual
- **Framework**: Visual inspection + validation script
- **Location**: N/A (manual review)
- **Coverage Target**: N/A

### Test Cases

| # | Description | Type | Priority |
|---|-------------|------|----------|
| 1 | Frontmatter description under 1024 chars | Manual | High |
| 2 | New mandatory rules visible and formatted | Manual | High |
| 3 | Workflow shows 4 breakpoints | Manual | High |
| 4 | Placeholder section exists | Manual | Medium |
| 5 | Token count < 5000 | Script | High |

---

## Dependencies

### Requires (blockedBy)

*No dependencies — this task can start immediately*

### Blocks

- **task-002**: Needs structure in place to add full section content
- **task-003**: Needs updated rules to reference in step file
- **task-004**: Needs updated rules to reference in step file
- **task-005**: Needs updated rules to reference in step file

---

## Notes

- Keep backwards compatibility with existing invocations
- Token budget is critical — stay well under 5000
- Frontmatter changes affect plugin manifest indexing
- Run `python src/scripts/validate_all.py` after completion

---

*Task specification generated by /spec v1.0 — EPCI v6.0*
