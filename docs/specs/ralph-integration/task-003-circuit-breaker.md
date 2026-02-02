---
id: task-003
title: Implement Circuit Breaker
slug: circuit-breaker
complexity: M
estimated_minutes: 60
dependencies: []
source_stories: [US5]
test_approach: Unit
---

# Task 003: Implement Circuit Breaker

## Objective

Implement an inline circuit breaker in bash that detects stuck loops (no progress, repeated errors) and stops execution gracefully without requiring external library files.

## Context

Ralph loops can get stuck in infinite cycles if Claude keeps making the same mistakes. The circuit breaker tracks state hashes and error patterns across iterations to detect stagnation and trigger early exit with appropriate exit codes.

## Acceptance Criteria

### AC1: Inline Implementation
**Given** the circuit breaker code
**When** integrated into ralph.sh
**Then** it must be fully inline (no external lib/ files required)

### AC2: No-Progress Detection
**Given** file state tracking
**When** 3 consecutive iterations produce the same git diff hash
**Then** trigger circuit breaker with "no progress" message

### AC3: Same-Error Detection
**Given** error tracking
**When** 3 consecutive iterations produce the same error hash
**Then** trigger circuit breaker with "repeated error" message

### AC4: Exit Codes
**Given** circuit breaker triggers
**When** script exits
**Then** use exit code 2 (distinct from 0=success, 1=max iterations)

### AC5: Logging
**Given** circuit breaker activation
**When** triggered
**Then** log timestamp, reason, and iteration count to progress.txt

## Steps

### Step 1: Design State Tracking (15min)
- **Input**: Circuit breaker patterns from research
- **Output**: Bash arrays for FILE_HASHES[], ERROR_HASHES[]
- **Validation**: Efficient tracking without memory bloat

### Step 2: Implement check_circuit_breaker Function (25min)
- **Input**: State tracking design, thresholds
- **Output**: Bash function with no-progress and same-error checks
- **Validation**: Function returns 0 (continue) or 1 (stop)

### Step 3: Write Unit Tests (20min)
- **Input**: Circuit breaker function
- **Output**: Test script simulating stuck scenarios
- **Validation**: Tests pass for all trigger conditions

## Files

| Path | Action | Description |
|------|--------|-------------|
| src/skills/spec/templates/circuit-breaker.sh.snippet | create | Reusable circuit breaker code |
| src/scripts/test_circuit_breaker.sh | create | Unit tests for circuit breaker |

## Dependencies

None — this is a root task (can run parallel with task-001).
