---
id: task-002
title: Add Stack & Core Skills Section
slug: stack-core-section
feature: skill-implement
complexity: M
estimated_minutes: 90
dependencies:
  - task-001
files_affected:
  - path: src/skills/implement/SKILL.md
    action: modify
test_approach: Manual
---

# Task 002: Add Stack & Core Skills Section

## Objective

Create the comprehensive "Stack & Core Skills Integration" section in SKILL.md with detailed tables for stack skills, core skills, and a Mermaid diagram showing the integration flow. This section makes the integration requirements explicit and enforceable.

---

## Context

Per decision D4 (triple couverture), the SKILL.md must have a dedicated section documenting stack and core skills integration. This section is the primary reference for understanding how /implement uses the EPCI ecosystem.

Key decisions from brief:
- D1: Auto-inject rules-templates from detected stack
- D6: Format as Tableau + Mermaid
- D12: All agents receive stack context

---

## Acceptance Criteria

### AC1: Stack Skills Table Present

- **Given**: The new section in SKILL.md
- **When**: Stack skills table is added
- **Then**: Table contains all 5 stack skills with detection patterns, rules injected, and phase usage

### AC2: Core Skills Table Present

- **Given**: The new section in SKILL.md
- **When**: Core skills table is added
- **Then**: Table contains all 6 core skills with trigger conditions, phases, and purposes

### AC3: Mermaid Diagram Renders

- **Given**: The Mermaid code block in the section
- **When**: Viewed in GitHub/IDE with Mermaid support
- **Then**: Diagram shows complete flow from INIT through MEMORY with all skill invocations

### AC4: Injection Protocol Documented

- **Given**: The Stack Skills subsection
- **When**: Reading the protocol
- **Then**: 4-step injection process is clearly documented (detect, load, transmit, apply)

---

## Steps

### Step 1: Create Stack Skills Subsection (25 min)

**Input**: Brief section 4.1, stack skills from src/skills/stack/

**Actions**:
1. Add "### Stack Skills (Auto-injected)" heading
2. Create table with columns: Stack, Detection, Rules Injected, Phase Usage
3. Add 5 rows (python-django, javascript-react, php-symfony, java-springboot, frontend-editor)
4. Document injection protocol (4 steps)
5. Add note about transmission to sub-agents

**Output**: Complete Stack Skills subsection

**Validation**: All 5 stacks documented with accurate detection patterns

---

### Step 2: Create Core Skills Subsection (25 min)

**Input**: Brief section 4.2, core skills from src/skills/core/

**Actions**:
1. Add "### Core Skills (Auto-triggered)" heading
2. Create table with columns: Core Skill, Trigger, Phase, Purpose
3. Add 6 rows (state-manager, complexity-calculator, project-memory, clarification-engine, tdd-enforcer, breakpoint-system)
4. Mark conditional triggers clearly (e.g., "If clarity < 60%")
5. Mark LARGE-only breakpoint for C phase

**Output**: Complete Core Skills subsection

**Validation**: All 6 core skills documented with correct triggers

---

### Step 3: Create Mermaid Integration Diagram (25 min)

**Input**: Brief section 4.3, architecture diagram

**Actions**:
1. Add "### Integration Flow" heading
2. Create Mermaid graph TD block
3. Show INIT node with stack detection and state-manager
4. Show complexity routing (STANDARD/LARGE vs TINY/SMALL)
5. Show E→P→C→I→D→F→M flow with skill invocations
6. Show parallel reviews fan-out and synthesis
7. Style nodes appropriately

**Output**: Complete Mermaid diagram

**Validation**: Diagram renders correctly, shows all integration points

---

### Step 4: Add Integration Notes (15 min)

**Input**: Brief decisions D1, D12

**Actions**:
1. Add subsection "### Integration Notes"
2. Document that stack context is transmitted to all agents
3. Explain that rules-templates are loaded into global context
4. Note that project-memory provides calibration data
5. Reference the detailed reference files (to be created in task-006)

**Output**: Integration notes subsection

**Validation**: Clear explanation of how integration works

---

## Files

| Path | Action | Description |
|------|--------|-------------|
| `src/skills/implement/SKILL.md` | modify | Add complete Stack & Core Skills Integration section |

---

## Test Approach

- **Type**: Manual
- **Framework**: Visual inspection + Mermaid preview
- **Location**: N/A (manual review)
- **Coverage Target**: N/A

### Test Cases

| # | Description | Type | Priority |
|---|-------------|------|----------|
| 1 | Stack skills table has 5 rows | Manual | High |
| 2 | Core skills table has 6 rows | Manual | High |
| 3 | Mermaid renders without errors | Preview | High |
| 4 | Injection protocol has 4 steps | Manual | Medium |
| 5 | Token count still < 5000 | Script | High |

---

## Dependencies

### Requires (blockedBy)

- **task-001**: Section placeholder must exist in SKILL.md structure

### Blocks

- **task-006**: References files will detail this section's content

---

## Notes

- Mermaid syntax must be compatible with GitHub rendering
- Keep tables compact to save tokens
- Use abbreviations where clear (e.g., "C, I" for phases)
- Diagram should focus on clarity over comprehensiveness

---

*Task specification generated by /spec v1.0 — EPCI v6.0*
