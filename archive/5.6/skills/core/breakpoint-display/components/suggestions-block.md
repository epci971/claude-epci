# Suggestions Block Component

## Overview

Composant réutilisable pour afficher des suggestions proactives dans les breakpoints.
Activé via flag `--suggest` dans `/brainstorm` (Discovery Mode).

## Input Schema

```yaml
suggestions:
  - pattern: "{pattern_id}"
    text: "{suggestion_text}"
    priority: "P1|P2|P3"
    action: "{command_or_null}"
```

## Display Format

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ 💡 SUGGESTIONS PROACTIVES                                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│ 🔴 [P1] {text}                                                              │
│        → {action}                                                           │
│ 🟡 [P2] {text}                                                              │
│        → {action}                                                           │
│ 🟢 [P3] {text}                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Priority Icons

| Priority | Icon | Meaning |
|----------|------|---------|
| P1 | 🔴 | Critical - strongly recommended |
| P2 | 🟡 | Important - recommended |
| P3 | 🟢 | Nice-to-have - optional |

## Rules

1. **Max 3 suggestions** displayed per breakpoint
2. **Sort by priority** (P1 first, then P2, then P3)
3. **Skip if empty** - don't display block if no suggestions
4. **Action optional** - if no action, don't display `→` line
5. **Truncate text** at 70 chars with `...`

## Rendering Logic

```
IF suggestions is NULL or EMPTY:
   RETURN ""

SORT suggestions BY priority ASC (P1 < P2 < P3)
TAKE first 3

RENDER header "💡 SUGGESTIONS PROACTIVES"

FOR EACH suggestion:
   icon = PRIORITY_ICONS[suggestion.priority]
   text = TRUNCATE(suggestion.text, 70)
   RENDER "{icon} [{priority}] {text}"

   IF suggestion.action:
      RENDER "       → {action}"
```

## Examples

### With action

```yaml
suggestions:
  - pattern: "security-early"
    text: "Patterns auth détectés — considérez @security-auditor preview"
    priority: P1
    action: "security-check"
```

Output:
```
│ 🔴 [P1] Patterns auth détectés — considérez @security-auditor preview       │
│        → security-check                                                     │
```

### Without action (info-only)

```yaml
suggestions:
  - pattern: "scope-large"
    text: "Projet estimé LARGE — considérez /decompose après brief"
    priority: P2
    action: null
```

Output:
```
│ 🟡 [P2] Projet estimé LARGE — considérez /decompose après brief             │
```

### Multiple suggestions

```yaml
suggestions:
  - pattern: "coverage-low"
    text: "Coverage à 35% — essayez Six Hats"
    priority: P2
    action: "technique six-hats"
  - pattern: "security-early"
    text: "Patterns auth détectés"
    priority: P1
    action: "security-check"
  - pattern: "similar-feature"
    text: "Feature similaire: auth-oauth"
    priority: P3
    action: null
```

Output (sorted by priority):
```
┌─────────────────────────────────────────────────────────────────────────────┐
│ 💡 SUGGESTIONS PROACTIVES                                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│ 🔴 [P1] Patterns auth détectés                                              │
│        → security-check                                                     │
│ 🟡 [P2] Coverage à 35% — essayez Six Hats                                   │
│        → technique six-hats                                                 │
│ 🟢 [P3] Feature similaire: auth-oauth                                       │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Integration

Used by breakpoint types:
- `ems-status` (brainstorm)
- `plan-review` (transition/finalization)
- `analysis` (brief)
- `decomposition` (optional)
- `diagnostic` (optional)

See skill `proactive-suggestions` for pattern catalog.
