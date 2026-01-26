---
name: spec
description: >
  Create comprehensive specifications (PRD/CDC) from requirements or brainstorm output.
  Generates Ralph-compatible task breakdowns for automated execution.
  Trigger words: write spec, create PRD, document feature, specification.
user-invocable: true
argument-hint: "<requirement or @brief-path>"
---

# Spec

Create comprehensive specifications from requirements or brainstorm output.

## Usage

```
/epci:spec "feature description"
/epci:spec @docs/briefs/feature-brief.md
```

## Workflow

1. **Analyze** - Parse input (direct or from brainstorm)
2. **Structure** - Create PRD with user stories
3. **Decompose** - Break into implementable tasks
4. **Generate** - Output Ralph-compatible format

## Output

- Feature specification document
- Task breakdown (Ralph format)
- Dependency graph

## Shared Components Used

- `complexity-calculator` - Estimate effort
- `clarification-engine` - Fill gaps
- `breakpoint-system` - Validation checkpoints

## Implementation

TODO: Implement in Phase 2+

## Templates

See [templates/](templates/) for PRD and Ralph templates.

## References

See [references/](references/) for additional documentation.
