---
id: task-008
title: E2E Test Flow
slug: e2e-test
complexity: M
estimated_minutes: 60
dependencies: [task-007]
source_stories: []
test_approach: E2E
---

# Task 008: E2E Test Flow

## Objective

Validate the complete flow from /spec generation through Ralph execution by running a test feature end-to-end.

## Context

All components are in place. This task verifies they work together: /spec generates artifacts, ralph.sh runs, /ralph-exec processes stories, circuit breaker detects stuck loops, and PRD.json updates correctly.

## Acceptance Criteria

### AC1: Spec Generation
**Given** a test brief
**When** /spec runs
**Then** all artifacts generated in correct locations

### AC2: Ralph Script Execution
**Given** generated ralph.sh
**When** executed (simulated)
**Then** script starts, loads PRD, calls /ralph-exec

### AC3: Status Parsing
**Given** mock /ralph-exec output
**When** ralph.sh parses
**Then** correctly extracts STATUS and EXIT_SIGNAL

### AC4: Circuit Breaker Trigger
**Given** simulated stuck loop (3 same errors)
**When** circuit breaker checks
**Then** exits with code 2 and logs reason

### AC5: PRD Update Verification
**Given** story completion
**When** PRD.json checked
**Then** status, passes, execution fields updated

## Steps

### Step 1: Create Test Brief (15min)
- **Input**: Test scenario requirements
- **Output**: Minimal test brief for 2-3 stories
- **Validation**: Brief parses correctly

### Step 2: Run /spec and Verify Artifacts (25min)
- **Input**: Test brief
- **Output**: Generated specs and Ralph artifacts
- **Validation**: All expected files exist, JSON valid

### Step 3: Simulate Ralph Execution (20min)
- **Input**: Generated ralph.sh, mock /ralph-exec
- **Output**: Execution log showing correct behavior
- **Validation**: Status parsing, circuit breaker, PRD updates all work

## Files

| Path | Action | Description |
|------|--------|-------------|
| tests/e2e/test-ralph-integration/ | create | Test directory |
| tests/e2e/test-ralph-integration/test-brief.md | create | Minimal test brief |
| tests/e2e/test-ralph-integration/run-e2e.sh | create | E2E test runner script |

## Dependencies

- **task-007**: All previous tasks must be complete
