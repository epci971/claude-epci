# Breakpoint Display Formats

> ASCII box templates for /spec skill breakpoints with AskUserQuestion integration.

## Common Elements

### Progress Indicators

```
Complexity: {TINY|SMALL|STANDARD|LARGE}
Tasks: {count} | Steps: {total_steps}
Estimated: ~{hours}h
```

### Proactive Suggestions Format

```
[P1] High-priority suggestion - most impactful
[P2] Medium-priority suggestion - good to consider
[P3] Low-priority suggestion - optional improvement
```

### Standard Options Block

```
├─────────────────────────────────────────────────────────────────────┤
│ ┌─ Options ──────────────────────────────────────────────────────┐ │
│ │  [A] Primary action (Recommended) — Description               │ │
│ │  [B] Alternative action — Description                         │ │
│ │  [C] Another option — Description                             │ │
│ │  [?] Autre reponse...                                         │ │
│ └────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Clarification Box

**Used in**: step-00-init.md (when clarity < 0.6)

### Template

```
┌─────────────────────────────────────────────────────────────────────┐
│ ❓ CLARIFICATION NECESSAIRE                                         │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│ La description fournie necessite des precisions                     │
│                                                                     │
│ Feature: {feature-slug}                                             │
│ Source: {source_type}                                               │
│ Questions de clarification:                                         │
│ {clarification_questions}                                           │
│                                                                     │
│ Critere de succes: Requirements clairs pour generation spec         │
│                                                                     │
├─────────────────────────────────────────────────────────────────────┤
│ ┌─ Options ──────────────────────────────────────────────────────┐ │
│ │  [A] Repondre aux questions (Recommended)                      │ │
│ │  [B] Fournir fichier brief — Fichier structure                 │ │
│ │  [C] Annuler — Affiner requirements                            │ │
│ │  [?] Autre reponse...                                          │ │
│ └────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
```

### Variables

| Variable | Source | Description |
|----------|--------|-------------|
| `{feature-slug}` | Input parsing | Kebab-case feature identifier |
| `{source_type}` | Input parsing | `text` or `discovery` |
| `{clarification_questions}` | clarification-engine | List of questions to clarify |

### AskUserQuestion

```json
{
  "question": "Comment voulez-vous clarifier?",
  "header": "Clarify",
  "multiSelect": false,
  "options": [
    { "label": "Repondre aux questions (Recommended)", "description": "Fournir clarifications inline" },
    { "label": "Fournir fichier brief", "description": "Fournir un document brief structure" },
    { "label": "Annuler", "description": "Annuler et affiner requirements" }
  ]
}
```

---

## Source Missing Box

**Used in**: step-00-init.md (when discovery mode and no brief found)

### Template

```
┌─────────────────────────────────────────────────────────────────────┐
│ 📄 SOURCE REQUISE                                                   │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│ Aucun brief existant trouve pour cette feature                      │
│                                                                     │
│ Feature: {feature-slug}                                             │
│ Recherche: docs/briefs/{slug}/                                      │
│ Besoin: fichier brief, description texte, ou brainstorm d'abord     │
│                                                                     │
│ Critere de succes: Source valide fournie                            │
│                                                                     │
├─────────────────────────────────────────────────────────────────────┤
│ ┌─ Options ──────────────────────────────────────────────────────┐ │
│ │  [A] Fournir chemin brief — Chemin vers fichier existant       │ │
│ │  [B] Description texte — Decrire requirements inline           │ │
│ │  [C] Lancer /brainstorm d'abord (Recommended) — Explorer       │ │
│ │  [D] Annuler — Abandonner le workflow                          │ │
│ │  [?] Autre reponse...                                          │ │
│ └────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
```

### Variables

| Variable | Source | Description |
|----------|--------|-------------|
| `{feature-slug}` | Input parsing | Kebab-case feature identifier |
| `{slug}` | Input parsing | Same as feature-slug |

### AskUserQuestion

```json
{
  "question": "Comment voulez-vous fournir la source?",
  "header": "Source",
  "multiSelect": false,
  "options": [
    { "label": "Lancer /brainstorm d'abord (Recommended)", "description": "Explorer l'idee avant de specifier" },
    { "label": "Fournir chemin brief", "description": "Chemin vers fichier brief existant" },
    { "label": "Description texte", "description": "Decrire requirements inline" },
    { "label": "Annuler", "description": "Abandonner le workflow" }
  ]
}
```

---

## Decomposition Review Box

**Used in**: step-01-analyze.md (after DAG validated)

### Template

```
┌─────────────────────────────────────────────────────────────────────┐
│ [DECOMPOSITION] Task Breakdown Review                                │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│ Feature: {feature-slug}                                              │
│ Complexity: {level}                                                  │
│ Tasks: {count} | Steps: {total_steps}                                │
│ Estimated: ~{hours}h ({optimized}h optimized)                        │
│                                                                      │
│ ┌─ Tasks ───────────────────────────────────────────────────────┐   │
│ │ 001. {title} ({min} min, {steps} steps)                       │   │
│ │ 002. {title} ({min} min, {steps} steps) <- 001                │   │
│ │ 003. {title} ({min} min, {steps} steps) <- 002                │   │
│ │ ...                                                            │   │
│ └────────────────────────────────────────────────────────────────┘   │
│                                                                      │
│ ┌─ DAG ─────────────────────────────────────────────────────────┐   │
│ │ T001 ──► T002 ──► T003 ──┬──► T005                            │   │
│ │                          └──► T004 ──► T006                   │   │
│ └────────────────────────────────────────────────────────────────┘   │
│                                                                      │
│ Validation: @decompose-validator -> {validation_status}              │
│                                                                      │
│ [P1] Consider splitting task-003 if scope grows                      │
│ [P2] task-004 and task-005 can parallelize                           │
│                                                                      │
├─────────────────────────────────────────────────────────────────────┤
│ ┌─ Options ──────────────────────────────────────────────────────┐ │
│ │  [A] Approve and generate specs (Recommended)                  │ │
│ │  [B] Modify task breakdown                                     │ │
│ │  [C] View task details                                         │ │
│ │  [D] Re-decompose with different strategy                      │ │
│ │  [E] Cancel                                                    │ │
│ │  [?] Autre reponse...                                          │ │
│ └────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
```

### Variables

| Variable | Source | Description |
|----------|--------|-------------|
| `{feature-slug}` | State | Feature identifier |
| `{level}` | complexity-calculator | TINY/SMALL/STANDARD/LARGE |
| `{count}` | Decomposition | Number of tasks |
| `{total_steps}` | Decomposition | Sum of all steps |
| `{hours}` | Decomposition | Sequential hours |
| `{optimized}` | DAG analysis | Parallel hours |
| `{title}` | Task list | Task title |
| `{min}` | Task | Duration in minutes |
| `{steps}` | Task | Step count |
| `{validation_status}` | @decompose-validator | APPROVED or issues found |

### AskUserQuestion

```json
{
  "question": "Comment proceder avec la decomposition?",
  "header": "Decomposition",
  "multiSelect": false,
  "options": [
    { "label": "Approve and generate specs (Recommended)", "description": "Valider et generer les fichiers specs" },
    { "label": "Modify task breakdown", "description": "Ajuster les taches manuellement" },
    { "label": "View task details", "description": "Voir le detail de chaque tache" },
    { "label": "Re-decompose with different strategy", "description": "Refaire la decomposition" },
    { "label": "Cancel", "description": "Annuler le workflow" }
  ]
}
```

---

## Specs Generated Box

**Used in**: step-02-generate-specs.md (after files written)

### Template

```
┌─────────────────────────────────────────────────────────────────────┐
│ 📋 SPECIFICATIONS GENEREES                                          │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│ METRIQUES                                                           │
│ • Complexite: {complexity} (score: {score})                         │
│ • Fichiers/taches: {task_count}                                     │
│ • Temps estime: {total_hours}h                                      │
│ • Niveau risque: LOW (generation spec uniquement)                   │
│                                                                     │
│ VALIDATIONS                                                         │
│ • @plan-validator: APPROVED                                         │
│   - Completude: {task_count} taches avec {step_count} steps         │
│   - Coherence: Toutes dependances mappees dans DAG                  │
│   - Faisabilite: Estimations calibrees                              │
│   - Qualite: Criteres d'acceptation definis par tache               │
│                                                                     │
│ PREVIEW FICHIERS                                                    │
│ | index.md ({lines} lignes) |                                       │
│ | task-001-{slug}.md | ~{estimate} |                                │
│ | {feature}.prd.json ({size} KB) |                                  │
│                                                                     │
│ Location: docs/specs/{feature-slug}/                                │
│                                                                     │
├─────────────────────────────────────────────────────────────────────┤
│ SUGGESTIONS PROACTIVES                                              │
│ [P1] Reviser criteres d'acceptation pour completude                 │
│ [P2] Considerer ajout tests edge cases                              │
├─────────────────────────────────────────────────────────────────────┤
│ ┌─ Options ──────────────────────────────────────────────────────┐ │
│ │  [A] Continuer vers Ralph (Recommended) — Generer artifacts    │ │
│ │  [B] Skip Ralph — Specs uniquement                             │ │
│ │  [C] Editer taches — Modifier fichiers generes                 │ │
│ │  [D] Regenerer — Regenerer avec modifications                  │ │
│ │  [?] Autre reponse...                                          │ │
│ └────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
```

### Variables

| Variable | Source | Description |
|----------|--------|-------------|
| `{complexity}` | State | TINY/SMALL/STANDARD/LARGE |
| `{score}` | complexity-calculator | Numeric score |
| `{task_count}` | Generation | Number of task files |
| `{step_count}` | Generation | Total steps across tasks |
| `{total_hours}` | Metrics | Estimated hours |
| `{lines}` | File stats | Lines in index.md |
| `{slug}` | Task | Task slug |
| `{estimate}` | Task | Estimated minutes |
| `{feature}` | State | Feature slug |
| `{size}` | File stats | PRD.json size in KB |
| `{feature-slug}` | State | Feature identifier |

### AskUserQuestion

```json
{
  "question": "Proceder avec les specifications?",
  "header": "Specs Review",
  "multiSelect": false,
  "options": [
    { "label": "Continuer vers Ralph (Recommended)", "description": "Generer artifacts d'execution" },
    { "label": "Skip Ralph", "description": "Specs uniquement, pas d'artifacts execution" },
    { "label": "Editer taches", "description": "Modifier fichiers taches generes" },
    { "label": "Regenerer", "description": "Regenerer avec modifications" }
  ]
}
```

---

## Completion Summary Box

**Used in**: step-03-generate-ralph.md (final step)

### Template

```
┌─────────────────────────────────────────────────────────────────────┐
│ ✅ SPECIFICATION COMPLETE                                           │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│ Tous les artifacts de spec et Ralph generes                         │
│                                                                     │
│ Feature: {feature-slug}                                             │
│ Complexite: {complexity}                                            │
│ Specs: docs/specs/{slug}/                                           │
│ Ralph: .ralph/{slug}/                                               │
│                                                                     │
│ Critere de succes: Utilisateur selectionne chemin implementation    │
│                                                                     │
├─────────────────────────────────────────────────────────────────────┤
│ SUGGESTIONS PROACTIVES                                              │
│ [P1] Reviser PROMPT.md pour ajustements stack-specific              │
│ [P2] Considerer execution parallele des taches pour optimisation    │
├─────────────────────────────────────────────────────────────────────┤
│ ┌─ Options ──────────────────────────────────────────────────────┐ │
│ │  [A] Lancer {skill} (Recommended)                              │ │
│ │  [B] Run Ralph Batch — Executer ralph.sh                       │ │
│ │  [C] Review fichiers — Inspecter artifacts generes             │ │
│ │  [D] Termine — Fin workflow, implementer plus tard             │ │
│ │  [?] Autre reponse...                                          │ │
│ └────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
```

### Variables

| Variable | Source | Description |
|----------|--------|-------------|
| `{feature-slug}` | State | Feature identifier |
| `{complexity}` | State | TINY/SMALL/STANDARD/LARGE |
| `{slug}` | State | Same as feature-slug |
| `{skill}` | Routing | /quick or /implement based on complexity |

### AskUserQuestion

```json
{
  "question": "Comment voulez-vous proceder?",
  "header": "Next Step",
  "multiSelect": false,
  "options": [
    { "label": "Lancer {skill} (Recommended)", "description": "Demarrer workflow implementation" },
    { "label": "Run Ralph Batch", "description": "Executer ./.ralph/{slug}/ralph.sh" },
    { "label": "Review fichiers", "description": "Inspecter artifacts generes" },
    { "label": "Termine", "description": "Fin workflow, implementer plus tard" }
  ]
}
```

**Note**: Replace `{skill}` with `/quick` or `/implement` based on complexity routing.

---

## Usage in Steps

When displaying a breakpoint in a step file, use this pattern:

```markdown
## BREAKPOINT: {Type} (OBLIGATOIRE)

AFFICHE le format depuis [references/breakpoint-formats.md#{anchor}](../references/breakpoint-formats.md#{anchor}).

Remplis les variables:
- {var1}: {source}
- {var2}: {source}

APPELLE AskUserQuestion avec les options depuis la reference.

⏸️ ATTENDS la reponse utilisateur avant de continuer.
```

This keeps steps as orchestrators while centralizing the display formats.
