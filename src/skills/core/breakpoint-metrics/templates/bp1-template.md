# BP1 Template — Post-Phase 1 (Plan Validé)

## Format

```
┌─────────────────────────────────────────────────────────────────────┐
│ ⏸️  BREAKPOINT PHASE 1 — Plan Validé                                │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│ 📊 MÉTRIQUES                                                        │
│ ├── Complexité: {CATEGORY} (score: {SCORE})                        │
│ ├── Fichiers impactés: {FILE_COUNT}                                │
│ ├── Temps estimé: {TIME_ESTIMATE}                                  │
│ └── Risque: {RISK_LEVEL} {RISK_DESCRIPTION}                        │
│                                                                     │
│ ✅ VALIDATIONS                                                      │
│ ├── @plan-validator: {VERDICT}                                     │
│ │   ├── Completeness: {STATUS}                                     │
│ │   ├── Consistency: {STATUS}                                      │
│ │   ├── Feasibility: {STATUS}                                      │
│ │   └── Quality: {STATUS}                                          │
│ └── Skills chargés: {SKILLS_LIST}                                  │
│                                                                     │
│ 📋 PREVIEW PHASE 2                                                  │
│ ├── Tâche 1: {TASK_1_TITLE} ({TASK_1_TIME})                       │
│ ├── Tâche 2: {TASK_2_TITLE} ({TASK_2_TIME})                       │
│ ├── Tâche 3: {TASK_3_TITLE} ({TASK_3_TIME})                       │
│ └── ... ({REMAINING_TASKS} tâches restantes)                       │
│                                                                     │
│ 🔗 Feature Document: {FEATURE_DOC_PATH}                            │
│                                                                     │
│ 💡 SUGGESTIONS PROACTIVES (F06)                                     │
│ {SUGGESTIONS_SECTION}                                               │
│                                                                     │
├─────────────────────────────────────────────────────────────────────┤
│ Options:                                                            │
│   • Tapez "Continuer" → Passer à Phase 2 (Implémentation)         │
│   • Tapez "Modifier le plan" → Réviser le plan                     │
│   • Tapez "Voir détails" → Afficher Feature Document complet       │
│   • Tapez "Annuler" → Abandonner le workflow                       │
└─────────────────────────────────────────────────────────────────────┘
```

## Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `{CATEGORY}` | Complexity category | STANDARD |
| `{SCORE}` | Normalized score (2 decimals) | 0.58 |
| `{FILE_COUNT}` | Number of impacted files | 7 |
| `{TIME_ESTIMATE}` | Estimated duration | ~2h30 |
| `{RISK_LEVEL}` | Risk level text | Moyen |
| `{RISK_DESCRIPTION}` | Risk context (in parentheses) | (breaking change possible) |
| `{VERDICT}` | @plan-validator result | APPROVED |
| `{STATUS}` | Checklist item status | ✅ or ❌ |
| `{SKILLS_LIST}` | Comma-separated skills | epci-core, architecture-patterns |
| `{TASK_N_TITLE}` | Task short title | Créer entité User |
| `{TASK_N_TIME}` | Task time estimate | 5 min |
| `{REMAINING_TASKS}` | Count of tasks not shown | 4 |
| `{FEATURE_DOC_PATH}` | Relative path to Feature Doc | docs/features/user-auth.md |

## Compact Version (for token optimization)

When context is constrained, use this compact format:

```
---
⏸️ **BP1 — Plan Validé**
📊 {CATEGORY} ({SCORE}) | {FILE_COUNT} fichiers | {TIME_ESTIMATE} | Risque: {RISK_LEVEL}
✅ @plan-validator: {VERDICT}
📋 Preview: {TASK_COUNT} tâches planifiées
🔗 {FEATURE_DOC_PATH}

→ "Continuer" | "Modifier" | "Détails" | "Annuler"
---
```

## Conditional Sections

### When NEEDS_REVISION

Replace validation section with:

```
│ ⚠️ VALIDATIONS                                                      │
│ ├── @plan-validator: NEEDS_REVISION                                │
│ │   └── Issues: {ISSUE_COUNT} à corriger                          │
│ └── Action requise: Corriger les issues critiques                  │
```

### When --large mode

Add persona information:

```
│ 🎭 Mode: --large (validation renforcée)                            │
```

### Suggestions Section (F06)

When proactive suggestions are available, display up to 3:

```
│ 💡 SUGGESTIONS PROACTIVES                                           │
│ ├── [P2] 🏗️ Pattern Repository détecté                             │
│ │   └── Suggestion: Extraire AbstractCrudRepository                │
│ └── [P3] 📚 Documentation API manquante                            │
│     └── Suggestion: Ajouter OpenAPI annotations                    │
│     └── Actions: [Voir détails] [Ignorer]                          │
```

When no suggestions:

```
│ 💡 SUGGESTIONS PROACTIVES                                           │
│ └── Aucune suggestion pour cette phase                             │
```

**Variables:**

| Variable | Description | Example |
|----------|-------------|---------|
| `{SUGGESTIONS_SECTION}` | Formatted suggestions or "Aucune" | See above |

**BP1 suggestion types** (architecture phase):
- P2: Reusable patterns detected
- P3: Documentation opportunities
