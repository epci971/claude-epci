# Step 03: Breakpoint

> User validates the refactoring plan before execution.

## Trigger

- Previous step: `step-02-planning.md` completed

## Inputs

| Input | Source |
|-------|--------|
| Transformation plan | From step-02 |
| Impact estimate | From step-02 |
| Mikado graph (optional) | From step-02 |

## Protocol

### 1. Display Plan Summary

Present the complete plan with all transformations:

```
┌─────────────────────────────────────────────────────────────────┐
│ [PLAN-REVIEW] Refactoring Plan Validation                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│ Target: src/services/auth.py                                    │
│ Scope: module                                                   │
│ Transformations: 4                                              │
│                                                                  │
│ ## Transformation Order                                         │
│                                                                  │
│ 1. T1: Extract validate_credentials() [Low Risk]                │
│ 2. T2: Extract TokenValidator class [Medium Risk]               │
│ 3. T3: Move user lookups [Low Risk]                             │
│ 4. T4: Inline dead refresh code [Low Risk]                      │
│                                                                  │
│ ## Expected Metrics Delta                                       │
│ - LOC: 450 → ~400 (-11%)                                        │
│ - CC: 25 → ~12 (-52%)                                           │
│ - MI: 45 → ~65 (+44%)                                           │
│                                                                  │
│ ## Files Affected                                               │
│ - Modified: auth.py, user.py, test_auth.py                      │
│ - Created: validators/token_validator.py, test_token_validator.py│
│                                                                  │
│ ## TDD Strategy                                                 │
│ Each transformation will follow RED-GREEN-REFACTOR:             │
│ - Verify existing tests pass (GREEN)                            │
│ - Apply transformation                                          │
│ - Verify tests still pass (GREEN)                               │
│ - Revert if any test fails                                      │
│                                                                  │
├─────────────────────────────────────────────────────────────────┤
│ [A] Execute  [B] Modify Plan  [C] Cancel                        │
└─────────────────────────────────────────────────────────────────┘
```

### 2. Present Options

Use `AskUserQuestion` with breakpoint-system:

```json
{
  "type": "plan-review",
  "context": {
    "target": "auth.py",
    "scope": "module",
    "transformations_count": 4,
    "estimated_risk": "medium"
  },
  "options": [
    {
      "label": "Execute (Recommended)",
      "description": "Proceed with TDD-enforced transformations",
      "action": "step-04-execute"
    },
    {
      "label": "Modify Plan",
      "description": "Adjust transformations or order",
      "action": "revise-plan"
    },
    {
      "label": "Cancel",
      "description": "Abort refactoring",
      "action": "abort"
    }
  ],
  "proactive_suggestions": [
    "P1: Consider running tests first to ensure baseline is green",
    "P2: T2 (Medium Risk) could be split into smaller steps",
    "P3: Use --atomic flag for easier rollback if needed"
  ]
}
```

### 3. Handle Response

| Response | Action |
|----------|--------|
| Execute | → `step-04-execute.md` |
| Modify Plan | → Allow user to adjust, return to step-02 |
| Cancel | → Abort with summary of analysis done |

### 4. If --dry-run Flag

Skip execution, generate report:

```
## Dry Run Complete

Plan generated but not executed (--dry-run flag).

### To execute this plan:
/refactor src/services/auth.py --scope module

### Plan exported to:
.claude/refactor-plans/auth-refactor-{timestamp}.md
```

## Outputs

| Output | Destination |
|--------|-------------|
| User decision | Workflow routing |
| Plan export (dry-run) | File system |

## Next Step

| Decision | Next Step |
|----------|-----------|
| Execute | → `step-04-execute.md` |
| Modify | → `step-02-planning.md` (revise) |
| Cancel | → Exit with analysis summary |
| --dry-run | → Exit with plan export |

## Error Handling

| Error | Resolution |
|-------|------------|
| User timeout | Remind and wait |
| Ambiguous response | Clarify options |
