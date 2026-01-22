---
name: refactor
description: >
  Restructure code architecture without changing external behavior.
  Supports pattern application, module extraction, and architectural changes.
  Trigger words: refactor, restructure, extract, reorganize code.
user-invocable: true
disable-model-invocation: false
argument-hint: "<target> [--pattern <pattern>]"
---

# Refactor

Restructure code without changing external behavior.

## Usage

```
/epci:refactor src/services/auth.py
/epci:refactor src/utils/ --pattern "extract module"
/epci:refactor "split UserService into smaller services"
```

## Patterns

| Pattern | Description |
|---------|-------------|
| `extract-method` | Pull code into new method |
| `extract-module` | Create new module/file |
| `inline` | Merge small units |
| `rename` | Consistent naming |
| `restructure` | Architectural change |

## Workflow

1. **Understand** - Map current structure
2. **Plan** - Define target architecture
3. **Execute** - Step-by-step transformation
4. **Verify** - Tests must pass throughout

## Shared Components Used

- `complexity-calculator` - Estimate scope
- `tdd-enforcer` - Ensure behavior preserved
- `breakpoint-system` - Step validation
- `state-manager` - Track multi-session refactors

## Implementation

TODO: Implement in Phase 2+

## References

See [references/](references/) for additional documentation.
