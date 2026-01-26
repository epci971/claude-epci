---
id: task-005
title: Update step-04-review.md
slug: step-04-review
feature: skill-implement
complexity: M
estimated_minutes: 90
dependencies:
  - task-001
files_affected:
  - path: src/skills/implement/steps/step-04-review.md
    action: modify
test_approach: Manual
---

# Task 005: Update step-04-review.md

## Objective

Completely restructure the step-04-review.md file to implement the parallel fan-out review architecture with @code-reviewer, conditional @security-auditor, and conditional @qa-reviewer, followed by critic synthesis that merges, deduplicates, and classifies findings.

---

## Context

The INSPECT phase is the quality gate. The brief specifies:
- Parallel invocation of multiple review agents
- Conditional triggers for security and QA
- Critic synthesis to merge findings
- Severity classification and auto-fix for minor issues

Key decisions from brief:
- D7: Conditionnel intelligent (security si auth, qa si >5 tests)
- D10: Parallel fan-out + Critic synthesis
- D12: Agents receive stack context

---

## Acceptance Criteria

### AC1: Parallel Fan-Out Implementation

- **Given**: CODE phase complete
- **When**: INSPECT step starts
- **Then**: Multiple review agents are invoked in parallel (single Task call with multiple agents)

### AC2: Conditional Agent Triggers

- **Given**: Codebase characteristics
- **When**: Determining which agents to invoke
- **Then**: @security-auditor triggers if auth patterns detected, @qa-reviewer triggers if >5 tests or LARGE complexity

### AC3: Critic Synthesis

- **Given**: All review agents have returned
- **When**: Synthesis runs
- **Then**: Findings are merged, deduplicated, and classified as Critical/Important/Minor

### AC4: Auto-Fix Protocol

- **Given**: Findings with Minor severity
- **When**: Auto-fix is enabled
- **Then**: Minor issues are fixed automatically, Important require confirmation, Critical require human decision

---

## Steps

### Step 1: Document Conditional Agent Triggers (20 min)

**Input**: Decision D7, file patterns from brief

**Actions**:
1. Add "## Agent Selection" section
2. Document @code-reviewer as always invoked
3. Document @security-auditor triggers:
   - Files match `**/auth/**`, `**/security/**`, `**/api/**`
   - Keywords: password, secret, jwt, oauth, api_key
4. Document @qa-reviewer triggers:
   - >5 test files created/modified
   - Complexity LARGE
   - Integration or E2E tests detected
5. Add stack context transmission note

**Output**: Agent selection protocol with triggers

**Validation**: All conditional triggers documented with patterns

---

### Step 2: Implement Parallel Fan-Out (25 min)

**Input**: Multi-agent patterns from Perplexity research

**Actions**:
1. Add "## Parallel Review Execution" section
2. Document single Task call pattern with multiple agents
3. Show how to invoke agents in parallel:
   ```
   Task tool with 3 parallel invocations:
   - @code-reviewer with full context + stack conventions
   - @security-auditor (if triggered) with security focus
   - @qa-reviewer (if triggered) with test focus
   ```
4. Document context bundle (diff, key files, test status, stack)
5. Add timeout handling (30 min max per agent)

**Output**: Parallel fan-out execution protocol

**Validation**: Single Task call launches multiple agents

---

### Step 3: Implement Critic Synthesis (25 min)

**Input**: Synthesis rules from brief, aggregation pattern

**Actions**:
1. Add "## Critic Synthesis" section
2. Document aggregation process:
   - Collect all agent responses
   - Parse structured findings (location, severity, description, fix)
   - Deduplicate similar findings
   - Resolve conflicts (highest severity wins)
3. Document severity classification:
   - Critical: Security vulnerabilities, data loss risk
   - Important: Performance issues, design flaws
   - Minor: Style, naming, documentation
4. Generate unified review report

**Output**: Critic synthesis protocol

**Validation**: Clear deduplication and classification rules

---

### Step 4: Implement Auto-Fix Protocol (20 min)

**Input**: Decision D10, severity classifications

**Actions**:
1. Add "## Auto-Fix Protocol" section
2. Document auto-fix rules:
   - Minor: Auto-fix without confirmation
   - Important: Propose fix, require confirmation
   - Critical: Present to user, no auto-fix
3. Document fix application process
4. Add verification step (run tests after fixes)
5. Show breakpoint for Critical issues

**Output**: Auto-fix protocol with severity handling

**Validation**: Each severity level has clear handling rules

---

## Files

| Path | Action | Description |
|------|--------|-------------|
| `src/skills/implement/steps/step-04-review.md` | modify | Complete restructure for parallel fan-out and critic synthesis |

---

## Test Approach

- **Type**: Manual
- **Framework**: Scenario walkthrough
- **Location**: N/A (manual review)
- **Coverage Target**: N/A

### Test Cases

| # | Description | Type | Priority |
|---|-------------|------|----------|
| 1 | Auth files trigger @security-auditor | Scenario | High |
| 2 | >5 tests trigger @qa-reviewer | Scenario | High |
| 3 | Parallel invocation uses single Task call | Scenario | High |
| 4 | Duplicate findings are merged | Scenario | High |
| 5 | Critical issues block auto-fix | Scenario | Medium |

---

## Dependencies

### Requires (blockedBy)

- **task-001**: Updated mandatory rules must exist

### Blocks

- **task-006**: Reference file multi-agent-review.md will detail this protocol

---

## Notes

- Parallel execution requires Task tool with multiple invocations
- Agent context must include detected stack for consistency
- Synthesis should produce machine-parseable output
- Breakpoint at end shows unified review report
- Consider timeout handling for slow agents

---

*Task specification generated by /spec v1.0 — EPCI v6.0*
