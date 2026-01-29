---
name: step-03-breakpoint
description: User validates the refactoring plan before execution
prev_step: steps/step-02-planning.md
next_step: steps/step-04-execute.md
conditional_next:
  - condition: "Modify plan"
    step: steps/step-02-planning.md
  - condition: "Cancel"
    step: null
  - condition: "--dry-run flag"
    step: null
---

# Step 03: Breakpoint

> User validates the refactoring plan before execution.

## Trigger

- Previous step: `step-02-planning.md` completed

## Inputs

| Input | Source |
|-------|--------|
| Transformation plan | From step-02 |
| Impact estimate | From step-02 |
| Mikado graph (optional) | From step-02 |

## Protocol

### 1. BREAKPOINT: Plan Validation (OBLIGATOIRE)

AFFICHE cette boîte:

┌─────────────────────────────────────────────────────────────────────┐
│ 📋 VALIDATION PLAN REFACTORING                                      │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│ MÉTRIQUES                                                           │
│ • Scope: {scope}                                                    │
│ • Score complexité: {transformations_count}                         │
│ • Fichiers impactés: {files_count}                                  │
│ • Temps estimé: {estimate}                                          │
│ • Niveau risque: {LOW|MEDIUM|HIGH}                                  │
│ • Description risque: {highest risk transformation}                 │
│                                                                     │
│ VALIDATIONS                                                         │
│ • @plan-validator: APPROVED                                         │
│   - Complétude: {transformations_count} transformations définies    │
│   - Cohérence: Ordre dépendances validé                             │
│   - Faisabilité: Toutes transformations atomiques                   │
│   - Qualité: Stratégie TDD par transformation                       │
│                                                                     │
│ PREVIEW TRANSFORMATIONS                                             │
│ | T1: {transformation_1_title} | ~{estimate} |                      │
│ | T2: {transformation_2_title} | ~{estimate} |                      │
│ | T3: {transformation_3_title} | ~{estimate} |                      │
│                                                                     │
│ Target: {target_file}                                               │
│                                                                     │
├─────────────────────────────────────────────────────────────────────┤
│ SUGGESTIONS PROACTIVES                                              │
│ [P1] Lancer tests d'abord pour confirmer baseline verte             │
│ [P2] {highest_risk_transformation} pourrait être split en steps     │
│ [P3] Utiliser --atomic flag pour rollback facile                    │
├─────────────────────────────────────────────────────────────────────┤
│ ┌─ Options ──────────────────────────────────────────────────────┐ │
│ │  [A] Exécuter (Recommended) — TDD-enforced transformations     │ │
│ │  [B] Modifier plan — Ajuster transformations ou ordre          │ │
│ │  [C] Annuler — Abandonner refactoring                          │ │
│ │  [?] Autre réponse...                                          │ │
│ └────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘

APPELLE AskUserQuestion({
  questions: [{
    question: "Procéder avec le plan de refactoring?",
    header: "Plan Review",
    multiSelect: false,
    options: [
      { label: "Exécuter (Recommended)", description: "Procéder avec transformations TDD-enforced" },
      { label: "Modifier plan", description: "Ajuster transformations ou ordre" },
      { label: "Annuler", description: "Abandonner refactoring" }
    ]
  }]
})

⏸️ ATTENDS la réponse utilisateur avant de continuer.

### 2. Expected Metrics Delta (displayed in breakpoint)

Include in the plan-review data:
- LOC: {before} → {after} ({delta}%)
- CC (Cyclomatic Complexity): {before} → {after} ({delta}%)
- MI (Maintainability Index): {before} → {after} ({delta}%)

### 3. Handle Response

| Response | Action |
|----------|--------|
| Execute | → `step-04-execute.md` |
| Modify Plan | → Allow user to adjust, return to step-02 |
| Cancel | → Abort with summary of analysis done |

### 4. If --dry-run Flag

Skip execution, generate report:

```
## Dry Run Complete

Plan generated but not executed (--dry-run flag).

### To execute this plan:
/refactor src/services/auth.py --scope module

### Plan exported to:
.claude/refactor-plans/auth-refactor-{timestamp}.md
```

## Outputs

| Output | Destination |
|--------|-------------|
| User decision | Workflow routing |
| Plan export (dry-run) | File system |

## Next Step

| Decision | Next Step |
|----------|-----------|
| Execute | → `step-04-execute.md` |
| Modify | → `step-02-planning.md` (revise) |
| Cancel | → Exit with analysis summary |
| --dry-run | → Exit with plan export |

## Error Handling

| Error | Resolution |
|-------|------------|
| User timeout | Remind and wait |
| Ambiguous response | Clarify options |
