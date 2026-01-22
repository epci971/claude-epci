---
name: debug
description: >
  Structured debugging workflow with hypothesis-driven investigation.
  Routes to appropriate complexity level (trivial, quick, complex).
  Trigger words: debug, fix bug, investigate error, troubleshoot.
user-invocable: true
disable-model-invocation: false
argument-hint: "<bug description or error>"
---

# Debug

Structured debugging with hypothesis-driven investigation.

## Usage

```
/epci:debug "users can't login after password reset"
/epci:debug "TypeError in checkout flow"
```

## Workflow

1. **Analyze** - Understand the bug report
2. **Hypothesize** - Generate potential causes
3. **Investigate** - Systematic verification
4. **Fix** - Implement solution
5. **Verify** - Confirm resolution

## Routing

| Complexity | Symptoms | Action |
|------------|----------|--------|
| Trivial | Typo, obvious fix | Direct fix |
| Quick | Single component | `/quick` style |
| Complex | Multi-component | Full investigation |

## Shared Components Used

- `complexity-calculator` - Route appropriately
- `tdd-enforcer` - Regression test
- `breakpoint-system` - Investigation checkpoints
- `project-memory` - Similar bugs history

## Implementation

TODO: Implement in Phase 2+

## References

See [references/](references/) for additional documentation.
