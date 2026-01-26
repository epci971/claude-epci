---
id: task-003
title: Update step-00-init.md
slug: step-00-init
feature: skill-implement
complexity: M
estimated_minutes: 75
dependencies:
  - task-001
files_affected:
  - path: src/skills/implement/steps/step-00-init.md
    action: modify
test_approach: Manual
---

# Task 003: Update step-00-init.md

## Objective

Enhance the step-00-init.md file to include stack detection protocol, clarification-engine integration for inputs with clarity < 60%, and explicit invocation of state-manager and complexity-calculator core skills.

---

## Context

The INIT step is the gateway for /implement. It must now:
- Detect project stack and load corresponding rules-templates
- Evaluate input clarity and trigger clarification if needed
- Initialize state via state-manager
- Route to /quick for TINY/SMALL complexity

Key decisions from brief:
- D1: Auto-inject rules from detected stack
- D2: Clarify inline with clarification-engine
- D9: Support turbo mode with reduced workflow

---

## Acceptance Criteria

### AC1: Stack Detection Protocol

- **Given**: The INIT step execution
- **When**: Project files are analyzed
- **Then**: Stack is detected using patterns from stack skills, and rules-templates are loaded

### AC2: Clarification Engine Integration

- **Given**: An input with clarity score < 60%
- **When**: INIT step processes input
- **Then**: clarification-engine is invoked for 2-3 targeted questions

### AC3: State Manager Invocation

- **Given**: INIT step starts
- **When**: Feature slug is known
- **Then**: state-manager.loadFeature() or createFeature() is called

### AC4: Complexity Routing

- **Given**: Complexity is calculated
- **When**: Result is TINY or SMALL
- **Then**: User is prompted to use /quick instead, with option to continue

---

## Steps

### Step 1: Add Stack Detection Protocol (25 min)

**Input**: Stack skills detection patterns from SKILL.md

**Actions**:
1. Add "## Stack Detection" section after Input Detection
2. Document detection algorithm:
   - Check for manage.py, pyproject.toml → python-django
   - Check for package.json with react → javascript-react
   - Check for composer.json with symfony → php-symfony
   - Check for pom.xml/build.gradle with spring-boot → java-springboot
   - Check for tailwind.config.* → frontend-editor
3. Add "Load rules-templates" instruction
4. Store detected stack in context variable
5. Note transmission to sub-agents

**Output**: Stack detection section in step-00-init.md

**Validation**: All 5 stacks have detection patterns documented

---

### Step 2: Add Clarification Engine Protocol (20 min)

**Input**: Decision D2, clarification-engine skill

**Actions**:
1. Add "## Input Clarity Check" section
2. Define clarity scoring criteria (explicit requirements, acceptance criteria, files mentioned)
3. Add threshold check: "IF clarity < 60%"
4. Document clarification-engine invocation
5. Limit to 2-3 questions maximum
6. Document how answers are integrated into context

**Output**: Clarity check and clarification protocol

**Validation**: Protocol clearly triggers clarification for vague inputs

---

### Step 3: Add State Manager Invocation (15 min)

**Input**: state-manager skill documentation

**Actions**:
1. Add "## State Initialization" section
2. Document loadFeature(slug) for existing features
3. Document createFeature(slug, spec) for new features
4. Show state.json initialization with lifecycle fields
5. Reference checkpoints for resume capability

**Output**: State initialization protocol

**Validation**: Both load and create scenarios covered

---

### Step 4: Update Complexity Routing (15 min)

**Input**: Current routing logic, decision D9

**Actions**:
1. Update complexity routing section
2. Add AskUserQuestion for TINY/SMALL routing decision
3. Add turbo mode detection (--turbo flag)
4. Document skip conditions for E/P phases in turbo mode
5. Show routing decision tree

**Output**: Updated complexity routing with user choice

**Validation**: User can override routing suggestion

---

## Files

| Path | Action | Description |
|------|--------|-------------|
| `src/skills/implement/steps/step-00-init.md` | modify | Add stack detection, clarification, state protocols |

---

## Test Approach

- **Type**: Manual
- **Framework**: Scenario walkthrough
- **Location**: N/A (manual review)
- **Coverage Target**: N/A

### Test Cases

| # | Description | Type | Priority |
|---|-------------|------|----------|
| 1 | Stack detection for each of 5 stacks | Scenario | High |
| 2 | Clarification triggers at clarity < 60% | Scenario | High |
| 3 | State manager creates new feature state | Scenario | High |
| 4 | TINY complexity prompts /quick suggestion | Scenario | Medium |
| 5 | Turbo mode detected from flag | Scenario | Medium |

---

## Dependencies

### Requires (blockedBy)

- **task-001**: Updated mandatory rules in SKILL.md must exist

### Blocks

- **task-006**: Reference files will detail stack detection patterns

---

## Notes

- Stack detection should be fast (file pattern matching)
- Clarification should not block if user chooses to skip
- State initialization must handle resume scenarios
- Keep step file under 300 lines for readability

---

*Task specification generated by /spec v1.0 — EPCI v6.0*
