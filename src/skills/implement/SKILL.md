---
name: implement
description: >
  Full implementation workflow for STANDARD and LARGE features with multi-phase
  execution. Includes planning, TDD implementation, and validation.
  Trigger words: implement feature, build, develop, create feature.
user-invocable: true
disable-model-invocation: false
argument-hint: "<feature-slug> [@spec-path]"
---

# Implement

Full implementation workflow for STANDARD and LARGE features.

## Usage

```
/epci:implement feature-slug
/epci:implement feature-slug @docs/specs/feature.md
```

## Workflow

### Phase 1: Planning
- Explore codebase
- Create implementation plan
- Validate with breakpoint

### Phase 2: Implementation
- TDD cycle (RED → GREEN → REFACTOR)
- Progressive implementation
- Code review checkpoint

### Phase 3: Finalization
- Documentation update
- Final validation
- Commit preparation

## Shared Components Used

- `state-manager` - Track progress across sessions
- `complexity-calculator` - Scope validation
- `tdd-enforcer` - Ensure TDD compliance
- `breakpoint-system` - Phase checkpoints
- `project-memory` - Context persistence

## Implementation

TODO: Implement in Phase 2+

## References

See [references/](references/) for additional documentation.
