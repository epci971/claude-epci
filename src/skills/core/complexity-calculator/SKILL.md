---
name: complexity-calculator
description: >-
  Calculates task complexity (TINY/SMALL/STANDARD/LARGE) for workflow routing.
  Analyzes scope, files affected, and estimated effort.
  Use when: evaluating new requests, routing to /quick vs /implement,
  estimating effort, or validating task scope.
  Internal component for EPCI v6.0.
user-invocable: false
disable-model-invocation: false
allowed-tools: Read, Glob, Grep
---

# Complexity Calculator

Internal component for task complexity analysis and workflow routing.

## Overview

Determine appropriate workflow based on task scope:
- Route to `/quick` for TINY/SMALL
- Route to `/implement` for STANDARD/LARGE

## API

| Function | Description | Input | Output |
|----------|-------------|-------|--------|
| `calculate(task)` | Analyze task complexity | task description | Complexity result |
| `validate_scope(complexity, files)` | Check if within limits | complexity, files[] | Boolean |
| `recommend_workflow(result)` | Suggest workflow | ComplexityResult | "/quick" or "/implement" |

## Complexity Categories

| Category | Files | LOC | Duration | Workflow |
|----------|-------|-----|----------|----------|
| TINY | 1 | < 50 | < 30 min | `/quick` |
| SMALL | 2-3 | < 200 | < 2 hours | `/quick` |
| STANDARD | 4-10 | < 1000 | 1-3 days | `/implement` |
| LARGE | 10+ | > 1000 | > 3 days | `/implement --large` |

## Calculation Factors

1. **Files Impacted** - Number of files to modify (weight: 30%)
2. **Lines of Code** - Estimated LOC change (weight: 25%)
3. **Dependencies** - Cross-module dependencies (weight: 20%)
4. **Test Coverage** - Required test additions (weight: 15%)
5. **Risk Level** - Critical path involvement (weight: 10%)

## Result Schema

```json
{
  "category": "TINY | SMALL | STANDARD | LARGE",
  "confidence": 0.0-1.0,
  "factors": {
    "files": 3,
    "loc_estimate": 150,
    "dependencies": 2,
    "test_additions": 5,
    "risk": "low | medium | high"
  },
  "recommended_workflow": "/quick | /implement",
  "reasoning": "string"
}
```

## Usage

Invoked automatically by skills for routing decisions:

```
# Called by /brainstorm for effort estimation
result = complexity.calculate(task_description)
# Returns: { category: "SMALL", workflow: "/quick", ... }

# Called by /spec for task breakdown sizing
complexity.validate_scope("SMALL", files_list)
# Returns: true/false if scope matches

# Called by /implement for scope validation
complexity.recommend_workflow(analysis_result)
# Returns: "/implement" with reasoning
```

## Scoring Algorithm

```
score = (
  files_score * 0.30 +
  loc_score * 0.25 +
  deps_score * 0.20 +
  tests_score * 0.15 +
  risk_score * 0.10
)

if score < 25: TINY
elif score < 50: SMALL
elif score < 75: STANDARD
else: LARGE
```

## Limitations

This component does NOT:
- Predict actual implementation time
- Account for developer experience
- Consider external dependencies (APIs, DBs)
