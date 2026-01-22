---
name: breakpoint-system
description: >-
  Interactive checkpoint system for user validation during EPCI workflows.
  Displays status boxes and prompts for decisions at critical points.
  Use when: showing progress, requesting approval, presenting options,
  or pausing for user confirmation during multi-phase workflows.
  Internal component for EPCI v6.0.
user-invocable: false
disable-model-invocation: false
allowed-tools: AskUserQuestion
---

# Breakpoint System

Internal component for interactive checkpoints during workflows.

## Overview

Provide structured pause points where users can:
- Review progress
- Approve next steps
- Modify direction
- Cancel workflow

## API

| Function | Description | Input | Output |
|----------|-------------|-------|--------|
| `checkpoint(type, data)` | Display checkpoint | type, data | User response |
| `validation(title, checks)` | Show validation box | title, checks[] | Approved boolean |
| `decision(question, options)` | Prompt for decision | question, options[] | Selected option |
| `progress(phase, status)` | Show progress update | phase, status | void |

## Breakpoint Types

| Type | Use Case | Display |
|------|----------|---------|
| `analysis` | After exploration phase | Summary + findings |
| `validation` | Before proceeding to next phase | Checklist + approve |
| `completion` | After phase completion | Results + next steps |
| `decision` | Multiple options available | Options + selection |
| `progress` | Status update (no pause) | Info only |

## Display Format

Uses ASCII box format for clear visibility:

```
┌─────────────────────────────────────────┐
│ [TYPE] Title                            │
├─────────────────────────────────────────┤
│ Content...                              │
│ • Item 1                                │
│ • Item 2                                │
├─────────────────────────────────────────┤
│ [A] Continue  [B] Modify  [C] Cancel    │
└─────────────────────────────────────────┘
```

## Usage

Invoked automatically by all skills at phase boundaries:

```
# Analysis breakpoint after exploration
breakpoint.checkpoint("analysis", {
  title: "Exploration Complete",
  findings: [...],
  recommendations: [...]
})

# Validation before code phase
breakpoint.validation("Ready to Implement?", [
  { check: "Plan approved", status: true },
  { check: "Tests defined", status: true }
])

# Decision point with options
breakpoint.decision("Implementation approach?", [
  { label: "TDD", description: "Write tests first" },
  { label: "Code-first", description: "Quick prototype" }
])
```

## Integration with AskUserQuestion

Breakpoints use Claude's `AskUserQuestion` tool internally:

```yaml
AskUserQuestion:
  questions:
    - question: "Approve this plan?"
      header: "Phase 1"
      options:
        - label: "Approve"
          description: "Continue to implementation"
        - label: "Modify"
          description: "Request changes"
```

## Limitations

This component does NOT:
- Store breakpoint history (use state-manager)
- Support async notifications
- Provide timeout mechanisms
