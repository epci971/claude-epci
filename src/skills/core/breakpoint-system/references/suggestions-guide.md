# Proactive Suggestions Guide

How to use the P1/P2/P3 proactive suggestions system in breakpoints.

## Overview

Proactive suggestions provide contextual recommendations to users during breakpoints.
They are sorted by priority and displayed before the options block.

## Priority Levels

| Priority | Icon | Meaning | When to Use |
|----------|------|---------|-------------|
| P1 | `[!]` | Critical | Security issues, blocking problems, must-address |
| P2 | `[*]` | Important | Best practices, recommended actions, should-do |
| P3 | `[i]` | Nice-to-have | Optimizations, enhancements, could-do |

## Suggestion Structure

```typescript
interface Suggestion {
  pattern: string;      // Identifier for the suggestion type
  text: string;         // Human-readable suggestion text
  priority: "P1" | "P2" | "P3";
  action?: string;      // Optional action or command to execute
}
```

## Example Suggestions

```typescript
suggestions: [
  {
    pattern: "security-auth",
    text: "Patterns auth detectes - considerez audit securite",
    priority: "P1",
    action: "voir security-patterns skill"
  },
  {
    pattern: "coverage-low",
    text: "Coverage EMS a 35% - essayez Six Hats pour perspectives",
    priority: "P2",
    action: "technique six-hats"
  },
  {
    pattern: "refactor-opportunity",
    text: "Code duplique detecte - refactoring possible",
    priority: "P3",
    action: "/refactor src/services/"
  }
]
```

## Display Rules

1. **Sort by priority**: P1 first, then P2, then P3
2. **Max 3 displayed**: Even if more suggestions provided
3. **Show action if present**: Arrow notation `-> {action}`
4. **Skip if empty**: No suggestions block if array empty

## Rendering

```
├─────────────────────────────────────────────────────────────────────┤
│ SUGGESTIONS PROACTIVES                                              │
│ [!] [P1] Patterns auth detectes - considerez audit securite         │
│    -> voir security-patterns skill                                  │
│ [*] [P2] Coverage EMS a 35% - essayez Six Hats pour perspectives    │
│    -> technique six-hats                                            │
│ [i] [P3] Code duplique detecte - refactoring possible               │
│    -> /refactor src/services/                                       │
├─────────────────────────────────────────────────────────────────────┤
```

## Common Patterns

### For /brainstorm (ems-status)

| Pattern | Trigger | Priority | Text |
|---------|---------|----------|------|
| `coverage-low` | coverage < 50% | P2 | "Coverage faible - explorer plus de perspectives" |
| `clarity-high` | clarity > 80% | P3 | "Clarte elevee - pret pour convergence" |
| `stalled` | delta < 5 for 2 iterations | P1 | "Progression bloquee - changer approche" |
| `security-detected` | auth/security keywords | P1 | "Patterns securite detectes" |

### For /spec (plan-review)

| Pattern | Trigger | Priority | Text |
|---------|---------|----------|------|
| `large-task` | task > 2h estimate | P2 | "Tache volumineuse - considerer split" |
| `no-tests` | test coverage = 0 | P1 | "Aucun test prevu - ajouter strategie TDD" |
| `high-risk` | risk = HIGH | P1 | "Risque eleve - prevoir plan mitigation" |
| `parallel-opportunity` | independent tasks | P3 | "Taches parallelisables detectees" |

### For /debug (diagnostic)

| Pattern | Trigger | Priority | Text |
|---------|---------|----------|------|
| `known-issue` | matches known patterns | P1 | "Pattern connu - solution documentee" |
| `test-missing` | no test for area | P2 | "Zone non testee - ajouter tests" |
| `quick-fix` | simple solution available | P3 | "Solution rapide possible" |

### For /implement (phase-transition)

| Pattern | Trigger | Priority | Text |
|---------|---------|----------|------|
| `tests-failing` | test status = fail | P1 | "Tests echouent - corriger avant continuer" |
| `uncommitted` | dirty working tree | P2 | "Changements non commites" |
| `checkpoint-old` | last checkpoint > 1h | P3 | "Checkpoint ancien - sauvegarder" |

## Generating Suggestions

Calling skills are responsible for generating suggestions based on context.
breakpoint-system only displays them.

Example in calling skill:

```typescript
// In /brainstorm skill
function generateSuggestions(emsData: EMSData): Suggestion[] {
  const suggestions: Suggestion[] = [];
  
  if (emsData.axes.coverage < 50) {
    suggestions.push({
      pattern: "coverage-low",
      text: `Coverage a ${emsData.axes.coverage}% - explorer plus de perspectives`,
      priority: "P2",
      action: "technique six-hats"
    });
  }
  
  if (emsData.delta < 5 && iteration > 2) {
    suggestions.push({
      pattern: "stalled",
      text: "Progression bloquee depuis 2 iterations",
      priority: "P1",
      action: "changer approche ou terminer"
    });
  }
  
  return suggestions;
}
```

## Integration with Skills

| Skill | Suggestions Support | Common Patterns |
|-------|---------------------|-----------------|
| `/brainstorm` | Yes | coverage, clarity, stalled, security |
| `/spec` | Yes | large-task, no-tests, high-risk |
| `/implement` | Yes | tests-failing, uncommitted, checkpoint |
| `/debug` | Yes | known-issue, test-missing, quick-fix |
| `/refactor` | Optional | complexity, duplication |
| `/quick` | No | Too fast for suggestions |
| `/factory` | No | Simple validation only |

## Best Practices

1. **Be specific**: Generic suggestions are ignored
2. **Actionable**: Include action when possible
3. **Contextual**: Base on actual data, not assumptions
4. **Prioritize correctly**: P1 only for truly critical
5. **Limit quantity**: Max 3 even if more available
6. **Skip if none**: Don't show empty suggestions block
