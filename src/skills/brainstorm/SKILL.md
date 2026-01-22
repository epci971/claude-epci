---
name: brainstorm
description: >
  Transform vague ideas into structured specifications through guided exploration.
  Uses iterative refinement with EMS scoring to progressively clarify requirements.
  Trigger words: brainstorm, explore idea, clarify requirements, vague concept.
user-invocable: true
disable-model-invocation: false
argument-hint: "<idea>"
---

# Brainstorm

Transform vague ideas into actionable specifications through structured exploration.

## Usage

```
/epci:brainstorm "your idea or concept"
```

## Workflow

1. **Diverge** - Explore possibilities and perspectives
2. **Evaluate** - Score clarity using EMS (Exploration Maturity Score)
3. **Converge** - Refine and structure the concept
4. **Output** - Structured brief ready for `/spec`

## Shared Components Used

- `clarification-engine` - Smart questions generation
- `breakpoint-system` - Interactive checkpoints
- `project-memory` - Context awareness

## Implementation

TODO: Implement in Phase 2+

## References

See [references/](references/) for additional documentation.
