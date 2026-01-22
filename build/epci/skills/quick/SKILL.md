---
name: quick
description: >
  Fast implementation for TINY and SMALL tasks. Single-phase execution
  with optional TDD. Ideal for bug fixes, small features, and quick changes.
  Trigger words: quick fix, small change, tiny feature, fast implementation.
user-invocable: true
disable-model-invocation: false
argument-hint: "<task> [@plan-path]"
---

# Quick

Fast implementation for TINY and SMALL tasks.

## Usage

```
/epci:quick "fix the login button alignment"
/epci:quick "add validation to email field"
/epci:quick @docs/plans/fix-auth.md
```

## Workflow

1. **[E]xplore** - Quick codebase scan (skipped if plan provided)
2. **[P]lan** - Minimal planning (skipped if plan provided)
3. **[C]ode** - Direct implementation with optional TDD
4. **[T]est** - Validation and verification

## Complexity Limits

| Category | Files | LOC |
|----------|-------|-----|
| TINY | 1 | < 50 |
| SMALL | 2-3 | < 200 |

## Shared Components Used

- `state-manager` - Track progress
- `complexity-calculator` - Validate scope
- `tdd-enforcer` - Optional TDD
- `project-memory` - Context

## Implementation

TODO: Implement in Phase 2+

## References

See [references/](references/) for additional documentation.
