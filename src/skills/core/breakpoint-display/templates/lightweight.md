# Template: Lightweight Breakpoint

## Overview

Breakpoint léger avec auto-continue après timeout (3 secondes).

**Usage:** `/quick` with `--confirm` flag

## Data Structure

```typescript
{
  type: "lightweight",
  title: "{TITLE}",
  data: {
    summary: "{TEXT}",
    action: "{TEXT}",
    timeout: 3  // seconds
  },
  ask: {
    question: "{QUESTION}",
    header: "{HEADER}",
    options: [
      {label: "{LABEL}", description: "{DESCRIPTION}"},
      ...
    ]
  }
}
```

## Display Format

```
┌─────────────────────────────────────────────────────────────────────┐
│ ⏸️  {TITLE}                                                          │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│ {summary}                                                           │
│                                                                     │
│ Action: {action}                                                    │
│                                                                     │
│ ⏱️  Auto-continue dans 3 secondes...                                │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

Then invoke `AskUserQuestion` with options (but auto-select first option after timeout).

## Example

```typescript
{
  type: "lightweight",
  title: "QUICK MODE",
  data: {
    summary: "Plan EPCT prêt (8 fichiers, ~2h)",
    action: "Implémentation TDD avec tests",
    timeout: 3
  },
  ask: {
    question: "Continuer ?",
    header: "⚡ Quick",
    options: [
      {label: "Continuer (Recommended)", description: "Auto-continue in 3s"},
      {label: "Annuler", description: "Arrêter workflow"}
    ]
  }
}
```

## Token Savings

**Avant:** ~100 tokens
**Après:** ~40 tokens
**Gain:** 60%
