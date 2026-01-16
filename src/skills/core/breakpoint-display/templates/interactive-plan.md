# Template: Interactive Plan Breakpoint

## Overview

Breakpoint pour orchestration avec DAG interactif, reorder, et skip options.

**Usage:** `/orchestrate` Phase 3

## Data Structure

```typescript
{
  type: "interactive-plan",
  title: "PLAN D'EXÉCUTION",
  data: {
    specs_count: {number},
    estimated_duration: "{TIME}",
    dag_graph: "{MERMAID_CODE}",
    execution_plan: [
      {
        wave: {number},
        specs: ["{spec1}", "{spec2}", ...],
        parallel: {true|false}
      },
      ...
    ],
    recommendations: ["{rec1}", "{rec2}", ...]
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

## Example

```typescript
{
  type: "interactive-plan",
  title: "PLAN D'EXÉCUTION",
  data: {
    specs_count: 8,
    estimated_duration: "12h optimisé (vs 23h séquentiel)",
    dag_graph: "graph TD\n  S01-->S02\n  S01-->S03\n  ...",
    execution_plan: [
      {wave: 1, specs: ["S01"], parallel: false},
      {wave: 2, specs: ["S02", "S03"], parallel: true},
      {wave: 3, specs: ["S04"], parallel: false}
    ],
    recommendations: [
      "Wave 2 peut être parallélisée (S02 et S03 indépendants)",
      "S04 attend completion de S02 et S03"
    ]
  },
  ask: {
    question: "Valider ce plan d'exécution ?",
    header: "🚀 Execution",
    options: [
      {label: "Lancer (Recommended)", description: "Exécuter selon ce plan"},
      {label: "Réorganiser", description: "Modifier ordre/waves"},
      {label: "Skip specs", description: "Exclure certaines specs"},
      {label: "Annuler", description: "Ne pas exécuter"}
    ]
  }
}
```

## Token Savings

**Avant:** ~320 tokens
**Après:** ~95 tokens
**Gain:** 70%
