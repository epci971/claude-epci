---
name: improve
description: >
  Enhance existing code for better performance, readability, or maintainability.
  Focuses on optimization without changing functionality.
  Trigger words: improve, optimize, enhance performance, better code.
user-invocable: true
argument-hint: "<target> [--focus <area>]"
---

# Improve

Enhance existing code without changing functionality.

## Usage

```
/epci:improve src/api/handlers.py
/epci:improve src/components/ --focus performance
/epci:improve "database queries are slow"
```

## Focus Areas

| Focus | Description |
|-------|-------------|
| `performance` | Speed and efficiency |
| `readability` | Code clarity |
| `maintainability` | Future changes |
| `security` | Vulnerability fixes |
| `auto` | Detect best focus (default) |

## Workflow

1. **Analyze** - Profile and identify issues
2. **Propose** - Suggest improvements with impact
3. **Implement** - Apply changes incrementally
4. **Verify** - Confirm no functionality change

## Shared Components Used

- `complexity-calculator` - Estimate effort
- `tdd-enforcer` - Preserve behavior
- `breakpoint-system` - Approval checkpoints

## Implementation

TODO: Implement in Phase 2+

## References

See [references/](references/) for additional documentation.
