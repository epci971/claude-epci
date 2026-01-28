# Breakpoint Formats

> ASCII box templates for implement skill interactive breakpoints.

## Common Elements

### Progress Bars

```
Format: [{filled}{empty}] {score}/100

Filled char: █
Empty char: ░

Examples:
[████████░░] 80/100
[██████░░░░] 60/100
```

### Proactive Suggestions

```
Format: [P{n}] {suggestion}

Priority levels:
[P1] — Critical/Most impactful
[P2] — Important/Recommended
[P3] — Nice-to-have/Optional
```

### Standard Options Block

```
├─────────────────────────────────────────────────────────────────────┤
│ ┌─ Options ──────────────────────────────────────────────────────┐ │
│ │  [A] {primary} (Recommended) — {description}                   │ │
│ │  [B] {secondary} — {description}                               │ │
│ │  [C] {tertiary} — {description}                                │ │
│ │  [?] Autre reponse...                                          │ │
│ └────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Init Breakpoint {#init}

Used in: step-00-init.md (complexity evaluation)

### Template

```
┌─────────────────────────────────────────────────────────────────────┐
│ EVALUATION COMPLEXITE                                               │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│ Detection complexite terminee                                       │
│                                                                     │
│ Feature: {feature-slug}                                             │
│ Complexite: {complexity}                                            │
│ Estimation: ~{loc} LOC sur {files} fichiers                         │
│                                                                     │
│ Critere de succes: L'utilisateur confirme le workflow approprie     │
│                                                                     │
├─────────────────────────────────────────────────────────────────────┤
│ ┌─ Options ──────────────────────────────────────────────────────┐ │
│ │  [A] Continuer avec EPCI (Recommended) - Workflow complet      │ │
│ │  [B] Retrograder vers /quick - Plus simple qu'estime           │ │
│ │  [C] Abandonner - Affiner les requirements d'abord             │ │
│ │  [?] Autre reponse...                                          │ │
│ └────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
```

### Variables

| Variable | Source | Description |
|----------|--------|-------------|
| `{feature-slug}` | Input parsing | Kebab-case feature identifier |
| `{complexity}` | complexity-calculator | TINY/SMALL/STANDARD/LARGE |
| `{loc}` | complexity-calculator | Estimated lines of code |
| `{files}` | complexity-calculator | Estimated number of files |

### AskUserQuestion

```json
{
  "question": "Comment voulez-vous proceder?",
  "header": "Complexity",
  "multiSelect": false,
  "options": [
    { "label": "Continuer avec EPCI (Recommended)", "description": "Workflow complet pour features STANDARD+" },
    { "label": "Retrograder vers /quick", "description": "Plus simple qu'estime, utiliser quick workflow" },
    { "label": "Abandonner", "description": "Affiner les requirements d'abord" }
  ]
}
```

---

## Explore Breakpoint {#explore}

Used in: step-01-explore.md (phase transition E->P)

### Template

```
┌─────────────────────────────────────────────────────────────────────┐
│ EXPLORATION TERMINEE [E->P]                                         │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│ RESUME DE PHASE                                                     │
│ - Phase terminee: explore                                           │
│ - Phase suivante: plan                                              │
│ - Duree: {duration}                                                 │
│ - Fichiers modifies: aucun (read-only)                              │
│ - Tests: N/A                                                        │
│                                                                     │
│ CHECKPOINT                                                          │
│ - ID: {feature_id}-checkpoint-explore                               │
│ - Reprise possible: oui                                             │
│                                                                     │
├─────────────────────────────────────────────────────────────────────┤
│ SUGGESTIONS PROACTIVES                                              │
│ [P1] Reviser {files_count} fichiers a modifier avant planning       │
│ [P2] Suivre les patterns identifies: {patterns}                     │
├─────────────────────────────────────────────────────────────────────┤
│ ┌─ Options ──────────────────────────────────────────────────────┐ │
│ │  [A] Continuer vers Plan (Recommended) - Planifier impl        │ │
│ │  [B] Etendre exploration - Explorer plus de fichiers           │ │
│ │  [C] Abandonner - Scope trop large                             │ │
│ │  [?] Autre reponse...                                          │ │
│ └────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
```

### Variables

| Variable | Source | Description |
|----------|--------|-------------|
| `{duration}` | State tracking | Time spent in explore phase |
| `{feature_id}` | State | Feature identifier for checkpoint |
| `{files_count}` | Exploration | Number of files identified to modify |
| `{patterns}` | Exploration | Identified code patterns (e.g., "Repository, Service") |

### AskUserQuestion

```json
{
  "question": "Passer a la phase de planification?",
  "header": "Explore",
  "multiSelect": false,
  "options": [
    { "label": "Continuer vers Plan (Recommended)", "description": "Proceder a la planification" },
    { "label": "Etendre exploration", "description": "Explorer plus de fichiers avant de planifier" },
    { "label": "Abandonner", "description": "Scope trop large, annuler implementation" }
  ]
}
```

---

## Plan Validation Breakpoint {#plan}

Used in: step-02-plan.md (plan review before coding)

### Template

```
┌─────────────────────────────────────────────────────────────────────┐
│ VALIDATION DU PLAN                                                  │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│ METRIQUES                                                           │
│ - Complexite: {complexity} (score: {score})                         │
│ - Fichiers impactes: {files_count}                                  │
│ - Temps estime: {hours}h                                            │
│ - Niveau de risque: {risk_level}                                    │
│ - Description risque: {risk_notes}                                  │
│                                                                     │
│ VALIDATIONS                                                         │
│ - @plan-validator: {validation_status}                              │
│   - Completude: {phases} phases definies                            │
│   - Coherence: Dependances mappees                                  │
│   - Faisabilite: Dans le scope                                      │
│   - Qualite: Strategie TDD definie                                  │
│                                                                     │
│ PREVIEW TACHES                                                      │
│ | Phase 1: {summary_1} | ~{estimate_1} |                            │
│ | Phase 2: {summary_2} | ~{estimate_2} |                            │
│ | Phase 3: {summary_3} | ~{estimate_3} |                            │
│ Taches restantes: {remaining_tasks}                                 │
│                                                                     │
│ Skills charges: tdd-enforcer, state-manager                         │
│ Doc feature: .epci/features/{feature-slug}/FEATURE.md               │
│                                                                     │
├─────────────────────────────────────────────────────────────────────┤
│ SUGGESTIONS PROACTIVES                                              │
│ [P1] Cycle TDD enforced: RED -> GREEN -> REFACTOR                   │
│ [P2] Cible coverage: {coverage_target}%                             │
├─────────────────────────────────────────────────────────────────────┤
│ ┌─ Options ──────────────────────────────────────────────────────┐ │
│ │  [A] Approuver et Coder (Recommended) - Passer au TDD          │ │
│ │  [B] Modifier le plan - Ajuster phases ou approche             │ │
│ │  [C] Abandonner - Reviser requirements d'abord                 │ │
│ │  [?] Autre reponse...                                          │ │
│ └────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
```

### Variables

| Variable | Source | Description |
|----------|--------|-------------|
| `{complexity}` | complexity-calculator | TINY/SMALL/STANDARD/LARGE |
| `{score}` | complexity-calculator | Numeric complexity score |
| `{files_count}` | Plan analysis | Number of files to modify |
| `{hours}` | Plan analysis | Estimated hours |
| `{risk_level}` | Plan analysis | LOW/MEDIUM/HIGH |
| `{risk_notes}` | Plan analysis | Risk description text |
| `{validation_status}` | @plan-validator | APPROVED or issues found |
| `{phases}` | Plan | Number of phases in plan |
| `{summary_1}`, `{summary_2}`, `{summary_3}` | Plan | Phase summaries |
| `{estimate_1}`, `{estimate_2}`, `{estimate_3}` | Plan | Phase estimates |
| `{remaining_tasks}` | Plan | Tasks beyond preview |
| `{feature-slug}` | State | Feature identifier |
| `{coverage_target}` | Plan | Target test coverage percentage |

### AskUserQuestion

```json
{
  "question": "Approuver le plan et passer au code?",
  "header": "Plan Review",
  "multiSelect": false,
  "options": [
    { "label": "Approuver et Coder (Recommended)", "description": "Proceder a l'implementation TDD" },
    { "label": "Modifier le plan", "description": "Ajuster phases ou approche" },
    { "label": "Abandonner", "description": "Reviser requirements d'abord" }
  ]
}
```

---

## Code Review Breakpoint {#review}

Used in: step-03-code.md (phase transition C->I)

### Template

```
┌─────────────────────────────────────────────────────────────────────┐
│ CODE REVIEW TERMINE [C->I]                                          │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│ RESUME DE PHASE                                                     │
│ - Phase terminee: code                                              │
│ - Phase suivante: inspect                                           │
│ - Duree: {duration}                                                 │
│ - Taches completees: {tasks_completed}                              │
│ - Fichiers modifies: {files_modified}                               │
│ - Tests: {tests_passing}/{tests_total} passing                      │
│                                                                     │
│ CHECKPOINT                                                          │
│ - ID: {feature_id}-checkpoint-code                                  │
│ - Reprise possible: oui                                             │
│                                                                     │
├─────────────────────────────────────────────────────────────────────┤
│ SUGGESTIONS PROACTIVES                                              │
│ [P1] Coverage: {coverage}% atteint                                  │
│ [P2] {issues_count} issues trouves ({severity})                     │
├─────────────────────────────────────────────────────────────────────┤
│ ┌─ Options ──────────────────────────────────────────────────────┐ │
│ │  [A] Accepter et Documenter (Recommended) - Passer a la doc    │ │
│ │  [B] Demander Security Review - Audit securite approfondi      │ │
│ │  [C] Demander QA Validation - Tests QA additionnels            │ │
│ │  [D] Traiter les findings - Corriger avant de continuer        │ │
│ │  [?] Autre reponse...                                          │ │
│ └────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
```

### Variables

| Variable | Source | Description |
|----------|--------|-------------|
| `{duration}` | State tracking | Time spent in code phase |
| `{tasks_completed}` | State | Number of tasks done |
| `{files_modified}` | Git diff | Files changed count |
| `{tests_passing}` | Test runner | Passing test count |
| `{tests_total}` | Test runner | Total test count |
| `{feature_id}` | State | Feature identifier for checkpoint |
| `{coverage}` | Test runner | Current coverage percentage |
| `{issues_count}` | @code-reviewer | Number of issues found |
| `{severity}` | @code-reviewer | Highest severity (Critical/Important/Minor) |

### AskUserQuestion

```json
{
  "question": "Comment proceder apres le code review?",
  "header": "Code Review",
  "multiSelect": false,
  "options": [
    { "label": "Accepter et Documenter (Recommended)", "description": "Passer a la phase documentation" },
    { "label": "Demander Security Review", "description": "Audit securite approfondi necessaire" },
    { "label": "Demander QA Validation", "description": "Tests QA additionnels necessaires" },
    { "label": "Traiter les findings", "description": "Corriger les issues avant de continuer" }
  ]
}
```

---

## Security Review Breakpoint {#security}

Used in: step-04-inspect.md (optional security audit)

### Template

```
┌─────────────────────────────────────────────────────────────────────┐
│ SECURITY REVIEW TERMINE                                             │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│ Audit securite par @security-auditor termine                        │
│                                                                     │
│ Feature: {feature-slug}                                             │
│ Vulnerabilites totales: {vuln_total}                                │
│ - Critical/High: {vuln_critical} (a corriger obligatoirement)       │
│ - Medium/Low: {vuln_low} (recommande)                               │
│                                                                     │
│ Critere de succes: Aucune vulnerabilite CRITICAL/HIGH non resolue   │
│                                                                     │
├─────────────────────────────────────────────────────────────────────┤
│ SUGGESTIONS PROACTIVES                                              │
│ [P1] OWASP Top 10 verifie                                           │
│ [P2] Reviser {vuln_total} findings avant de continuer               │
├─────────────────────────────────────────────────────────────────────┤
│ ┌─ Options ──────────────────────────────────────────────────────┐ │
│ │  [A] Continuer (Recommended) - Posture securite acceptable     │ │
│ │  [B] Corriger issues critiques - Traiter high-severity d'abord │ │
│ │  [C] Accepter le risque - Documenter et continuer              │ │
│ │  [?] Autre reponse...                                          │ │
│ └────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
```

### Variables

| Variable | Source | Description |
|----------|--------|-------------|
| `{feature-slug}` | State | Feature identifier |
| `{vuln_total}` | @security-auditor | Total vulnerabilities found |
| `{vuln_critical}` | @security-auditor | Critical/High severity count |
| `{vuln_low}` | @security-auditor | Medium/Low severity count |

### AskUserQuestion

```json
{
  "question": "Comment gerer les findings securite?",
  "header": "Security",
  "multiSelect": false,
  "options": [
    { "label": "Continuer (Recommended)", "description": "Posture securite acceptable" },
    { "label": "Corriger issues critiques", "description": "Traiter les findings high-severity d'abord" },
    { "label": "Accepter le risque", "description": "Documenter la raison et continuer" }
  ]
}
```

---

## QA Review Breakpoint {#qa}

Used in: step-04-inspect.md (optional QA validation)

### Template

```
┌─────────────────────────────────────────────────────────────────────┐
│ QA REVIEW TERMINE                                                   │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│ Validation QA par @qa-reviewer terminee                             │
│                                                                     │
│ Feature: {feature-slug}                                             │
│ Criteres d'acceptation: {ac_passed}/{ac_total} valides              │
│ Taux de succes tests: {test_success_rate}%                          │
│ Defauts trouves: {defects_count}                                    │
│                                                                     │
│ Critere de succes: Tous les AC valides, aucun defaut bloquant       │
│                                                                     │
├─────────────────────────────────────────────────────────────────────┤
│ SUGGESTIONS PROACTIVES                                              │
│ [P1] {ac_passed}/{ac_total} criteres d'acceptation valides          │
│ [P2] Reviser {defects_count} defauts trouves                        │
├─────────────────────────────────────────────────────────────────────┤
│ ┌─ Options ──────────────────────────────────────────────────────┐ │
│ │  [A] Continuer (Recommended) - Validation QA reussie           │ │
│ │  [B] Corriger defauts d'abord - Traiter les issues trouves     │ │
│ │  [C] Accepter issues connues - Documenter et continuer         │ │
│ │  [?] Autre reponse...                                          │ │
│ └────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
```

### Variables

| Variable | Source | Description |
|----------|--------|-------------|
| `{feature-slug}` | State | Feature identifier |
| `{ac_passed}` | @qa-reviewer | Acceptance criteria passed |
| `{ac_total}` | @qa-reviewer | Total acceptance criteria |
| `{test_success_rate}` | @qa-reviewer | Test success percentage |
| `{defects_count}` | @qa-reviewer | Number of defects found |

### AskUserQuestion

```json
{
  "question": "Comment gerer les resultats QA?",
  "header": "QA Review",
  "multiSelect": false,
  "options": [
    { "label": "Continuer (Recommended)", "description": "Validation QA reussie" },
    { "label": "Corriger defauts d'abord", "description": "Traiter les issues trouves" },
    { "label": "Accepter issues connues", "description": "Documenter et continuer" }
  ]
}
```

---

## Finish Summary {#finish}

Used in: step-05-finish.md (implementation complete)

### Template

```
┌─────────────────────────────────────────────────────────────────────┐
│ IMPLEMENTATION COMPLETE                                             │
├─────────────────────────────────────────────────────────────────────┤
│ Feature: {feature-slug}                                             │
│                                                                     │
│ Summary:                                                            │
│ - {files_created} files created                                     │
│ - {files_modified} files modified                                   │
│ - {tests_added} tests added ({coverage}% coverage)                  │
│ - Documentation complete                                            │
│                                                                     │
│ EPCI Phases Completed:                                              │
│ [E] Explore                                                         │
│ [P] Plan                                                            │
│ [C] Code                                                            │
│ [I] Inspect                                                         │
│                                                                     │
│ Ready for commit and review.                                        │
└─────────────────────────────────────────────────────────────────────┘
```

### Variables

| Variable | Source | Description |
|----------|--------|-------------|
| `{feature-slug}` | State | Feature identifier |
| `{files_created}` | Git diff | New files count |
| `{files_modified}` | Git diff | Modified files count |
| `{tests_added}` | Test analysis | New tests count |
| `{coverage}` | Test runner | Final coverage percentage |

**Note:** Info-only display, no AskUserQuestion needed.

---

## Memory Summary {#memory}

Used in: step-06-memory.md (feature index update)

### Template

```
+------------------------------------------------------------------+
| [M] MEMORY PHASE COMPLETE                                        |
+------------------------------------------------------------------+
| Feature: {feature-slug}                                          |
|                                                                  |
| Summary: {summary}                                               |
|                                                                  |
| Modified Files: {files_count}                                    |
| Tests Added: {tests_count}                                       |
|                                                                  |
| index.json updated at:                                           |
| .claude/state/features/index.json                                |
+------------------------------------------------------------------+
```

### Variables

| Variable | Source | Description |
|----------|--------|-------------|
| `{feature-slug}` | State | Feature identifier |
| `{summary}` | Generation | 1-2 sentence implementation summary |
| `{files_count}` | Git diff | Files modified count |
| `{tests_count}` | Test analysis | Tests added count |

**Note:** Info-only display, no AskUserQuestion needed.
