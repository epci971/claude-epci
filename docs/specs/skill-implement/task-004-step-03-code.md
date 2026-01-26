---
id: task-004
title: Update step-03-code.md
slug: step-03-code
feature: skill-implement
complexity: M
estimated_minutes: 75
dependencies:
  - task-001
files_affected:
  - path: src/skills/implement/steps/step-03-code.md
    action: modify
test_approach: Manual
---

# Task 004: Update step-03-code.md

## Objective

Enhance the step-03-code.md file to include the pre-code TDD check (test rouge exists?), explicit tdd-enforcer invocation at each TDD cycle phase, and stack conventions application during implementation.

---

## Context

The CODE step is where implementation happens. The brief specifies strict TDD with:
- Pre-code check ensuring failing tests exist before coding
- tdd-enforcer validation at each RED/GREEN/REFACTOR phase
- Stack conventions applied during GREEN phase
- 80% coverage target

Key decisions from brief:
- D3: Strict TDD (RED-GREEN-REFACTOR obligatoire)
- D11: Pre-code check "Test rouge existe?"
- D12: Stack conventions inherited by implementation

---

## Acceptance Criteria

### AC1: Pre-Code TDD Check

- **Given**: A task ready for implementation
- **When**: CODE step starts for that task
- **Then**: Check verifies failing test exists, generates test skeleton if not

### AC2: TDD Enforcer Integration

- **Given**: Each phase of TDD cycle (RED, GREEN, REFACTOR, VERIFY)
- **When**: Phase completes
- **Then**: tdd-enforcer validates compliance before proceeding

### AC3: Stack Conventions Applied

- **Given**: GREEN phase implementation
- **When**: Code is written
- **Then**: Stack-specific patterns from rules-templates are applied

### AC4: Coverage Verification

- **Given**: VERIFY phase
- **When**: Full test suite runs
- **Then**: Coverage is checked against 80% target, warning if below

---

## Steps

### Step 1: Add Pre-Code TDD Check Protocol (20 min)

**Input**: Decision D11, tdd-enforcer skill

**Actions**:
1. Add "## Pre-Code TDD Check" section before TDD cycle
2. Document check algorithm:
   - Identify test file for current task
   - Check if failing test exists for task's acceptance criteria
   - If no failing test → generate test skeleton from AC
   - Run test to confirm RED state
3. Add mandatory rule: "NEVER proceed to GREEN without RED confirmation"
4. Show test skeleton generation template

**Output**: Pre-code TDD check protocol

**Validation**: Protocol prevents implementation without failing tests

---

### Step 2: Enhance TDD Cycle with tdd-enforcer (25 min)

**Input**: Current TDD cycle, tdd-enforcer skill

**Actions**:
1. Update each TDD phase with explicit tdd-enforcer invocation
2. RED phase:
   - tdd-enforcer: validate test fails
   - tdd-enforcer: validate failure is for expected reason
3. GREEN phase:
   - tdd-enforcer: validate test passes
   - tdd-enforcer: validate no other tests broken
4. REFACTOR phase:
   - tdd-enforcer: validate all tests still pass
   - tdd-enforcer: check for code smells
5. Add cycle state tracking

**Output**: Enhanced TDD cycle with enforcer calls

**Validation**: Each phase has explicit enforcer validation

---

### Step 3: Add Stack Conventions Application (15 min)

**Input**: Stack skills rules-templates, context variable from INIT

**Actions**:
1. Add "### Stack Conventions" subsection in GREEN phase
2. Document how to apply patterns:
   - Load rules-templates content
   - Apply naming conventions
   - Apply architectural patterns (e.g., service layer for Django)
   - Apply testing patterns (e.g., pytest fixtures)
3. Reference detected stack from INIT step
4. Note that conventions are non-negotiable for that stack

**Output**: Stack conventions application protocol

**Validation**: Clear instructions for applying stack patterns

---

### Step 4: Add Coverage Verification (15 min)

**Input**: Decision D3 (80% coverage), testing frameworks

**Actions**:
1. Enhance VERIFY phase with coverage check
2. Document coverage commands per stack:
   - Python: `pytest --cov --cov-fail-under=80`
   - JS/TS: `vitest --coverage` or `jest --coverage`
   - PHP: `phpunit --coverage-min=80`
   - Java: JaCoCo with 80% threshold
3. Add warning protocol if coverage < 80%
4. Add option to continue with justification

**Output**: Coverage verification protocol

**Validation**: Coverage check runs for all supported stacks

---

## Files

| Path | Action | Description |
|------|--------|-------------|
| `src/skills/implement/steps/step-03-code.md` | modify | Add pre-code check, enhanced TDD, stack conventions |

---

## Test Approach

- **Type**: Manual
- **Framework**: Scenario walkthrough
- **Location**: N/A (manual review)
- **Coverage Target**: N/A

### Test Cases

| # | Description | Type | Priority |
|---|-------------|------|----------|
| 1 | Pre-code check generates test if missing | Scenario | High |
| 2 | tdd-enforcer validates RED phase | Scenario | High |
| 3 | Stack conventions applied in GREEN | Scenario | High |
| 4 | Coverage check runs in VERIFY | Scenario | High |
| 5 | Warning shown if coverage < 80% | Scenario | Medium |

---

## Dependencies

### Requires (blockedBy)

- **task-001**: Updated mandatory rules must reference TDD requirements

### Blocks

- **task-006**: Reference files will detail TDD rules and stack testing patterns

---

## Notes

- Pre-code check should not be skippable for STANDARD+ complexity
- tdd-enforcer calls should be lightweight (no external API)
- Stack conventions must match actual rules-templates content
- Coverage tools vary by stack — document all variants

---

*Task specification generated by /spec v1.0 — EPCI v6.0*
