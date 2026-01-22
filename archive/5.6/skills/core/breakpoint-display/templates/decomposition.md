# Template: Decomposition Breakpoint

## Overview

Breakpoint pour validation découpage PRD avec table specs et menu modifications.

**Usage:** `/decompose` validation phase

## Data Structure

```typescript
{
  type: "decomposition",
  title: "VALIDATION DÉCOUPAGE",
  data: {
    source_file: "{FILENAME}",
    analysis: {
      lines: {number},
      total_effort: {number},
      structure: "{TEXT}"
    },
    specs: [
      {
        id: "{ID}",
        title: "{TITLE}",
        effort: {number},
        priority: "{PRIORITY|-}",
        deps: "{DEPS|-}",
        status: "{STATUS}"
      },
      ...
    ],
    parallelization: {number},
    optimized_duration: {number},
    sequential_duration: {number},
    alerts: ["{alert1}", ...] || null,
    validator_verdict: "{TEXT}"
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
│ ⏸️  VALIDATION DÉCOUPAGE                                            │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│ ANALYSE DE: {source_file}                                           │
│ ├── Lignes: {lines}                                                │
│ ├── Effort total détecté: {total_effort} jours                     │
│ └── Structure: {structure}                                          │
│                                                                     │
│ DÉCOUPAGE PROPOSÉ: {count} sous-specs                               │
│                                                                     │
│ | ID  | Title        | Effort | Priority | Dependencies | Status  | │
│ |-----|--------------|--------|----------|--------------|---------|  │
│ | S01 | {title}      | {d}j   | -        | -            | Pending | │
│ | S02 | {title}      | {d}j   | -        | S01          | Pending | │
│ | ... | ...          | ...    | ...      | ...          | ...     | │
│                                                                     │
│ PARALLÉLISATION: {count} specs parallélisables                      │
│ DURÉE OPTIMISÉE: {optimized}j (vs {sequential}j seq)                │
│                                                                     │
│ [If alerts:]                                                        │
│ ALERTES:                                                            │
│   • {alert1}                                                        │
│   • {alert2}                                                        │
│                                                                     │
│ @decompose-validator: {verdict}                                     │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

Then invoke `AskUserQuestion` with options.

## Example

```typescript
{
  type: "decomposition",
  title: "VALIDATION DÉCOUPAGE",
  data: {
    source_file: "prd-migration.md",
    analysis: {
      lines: 450,
      total_effort: 23,
      structure: "5 phases, 12 steps"
    },
    specs: [
      {id: "S01", title: "Auth Base", effort: 3, priority: "-", deps: "-", status: "Pending"},
      {id: "S02", title: "OAuth Integration", effort: 5, priority: "-", deps: "S01", status: "Pending"},
      {id: "S03", title: "User Migration", effort: 2, priority: "-", deps: "S01", status: "Pending"}
    ],
    parallelization: 2,
    optimized_duration: 15,
    sequential_duration: 23,
    alerts: ["S02 effort élevé - considérer split"],
    validator_verdict: "APPROVED with minor suggestions"
  },
  ask: {
    question: "Le découpage vous convient-il ?",
    header: "📋 Découpage",
    options: [
      {label: "Valider (Recommended)", description: "Générer fichiers sous-specs"},
      {label: "Modifier", description: "Ajuster découpage avant génération"},
      {label: "Annuler", description: "Abandonner décomposition"}
    ]
  }
}
```

## Two-Level Questions

If user chooses "Modifier", display second-level question:

```typescript
{
  type: "decomposition-modify",
  title: "MODIFICATION DÉCOUPAGE",
  ask: {
    question: "Que souhaitez-vous modifier ?",
    header: "🔧 Modifier",
    multiSelect: true,
    options: [
      {label: "Fusionner specs", description: "Ex: Fusionner S04 et S05"},
      {label: "Découper spec", description: "Ex: Découper S07 en 2 parties"},
      {label: "Renommer", description: "Ex: S03 → Modèles Fondamentaux"},
      {label: "Changer dépendances", description: "Ex: S06 ne dépend plus de S03"},
      {label: "Ajuster estimation", description: "Ex: S08 = 3 jours au lieu de 5"}
    ]
  }
}
```

Then wait for free text input describing the modifications.

## Token Savings

**Avant:** ~300 tokens
**Après:** ~85 tokens
**Gain:** 72%
