---
name: step-02-generate-specs
description: Generate specification files
prev_step: steps/step-01-analyze.md
next_step: steps/step-03-generate-ralph.md
---

# Step 02: Generate Specifications

## Reference Files

@../references/task-format.md
@../references/prd-schema.md

| Reference | Purpose |
|-----------|---------|
| task-format.md | Task file structure |
| prd-schema.md | PRD.json schema |

*(Breakpoint templates are inline in this file)*

## MANDATORY EXECUTION RULES (READ FIRST):

- 🔴 NEVER generate without APPROVED decomposition
- 🔴 NEVER skip acceptance criteria in task files
- 🔴 NEVER create PRD.json without all required fields
- ✅ ALWAYS use templates from templates/
- ✅ ALWAYS include Mermaid DAG in index.md
- ✅ ALWAYS validate JSON before writing
- 🔵 YOU ARE A TECHNICAL WRITER creating actionable specs
- 💭 FOCUS on clarity and completeness

## EXECUTION PROTOCOLS:

### 1. Create Directory Structure

```bash
mkdir -p docs/specs/{feature-slug}/
```

Verify directory created successfully.

### 2. Generate index.md

Use template from `templates/index.md.template`.

**Template variables:**
- `{{FEATURE_TITLE}}`: Human-readable title
- `{{DATE}}`: Generation date
- `{{TASK_COUNT}}`: Number of tasks
- `{{TOTAL_HOURS}}`: Estimated hours
- `{{DESCRIPTION}}`: Brief description from source
- `{{SCOPE_IN}}`: In-scope items list
- `{{SCOPE_OUT}}`: Out-of-scope items list
- `{{TASKS}}`: Task list with metadata
- `{{PHASES}}`: Grouped by dependency phase
- `{{EDGES}}`: DAG edges for Mermaid
- `{{EXECUTION_ORDER}}`: Topological sort order
- `{{STEP_COUNT}}`: Total steps across tasks
- `{{CRITICAL_PATH}}`: Tasks on critical path
- `{{OPTIMIZED_HOURS}}`: Parallel execution time
- `{{COMPLEXITY}}`: TINY/SMALL/STANDARD/LARGE
- `{{RECOMMENDED_SKILL}}`: /quick or /implement
- `{{RECOMMENDED_COMMAND}}`: Full command
- `{{SOURCE_PATH}}`: Source brief path

### 3. Generate task-XXX.md Files

For each task, use template from `templates/task.md.template`.

Follow structure defined in task-format.md (importé ci-dessus).

**Required sections per task:**
- YAML frontmatter with all fields
- Objective (2-3 sentences)
- Context (relevant background)
- Acceptance Criteria (minimum 2, Given-When-Then format)
- Steps (15-30 min each)
- Files table
- Test Approach
- Dependencies

### 4. Generate PRD.json

Create machine-readable version following prd-schema.md (importé ci-dessus).

**Validation before writing:**
- All required fields present
- All tasks have >= 2 acceptance criteria
- No circular dependencies in graph
- JSON is valid (parseable)
- Duration bounds respected (tasks 60-120 min, steps 15-30 min)

### 5. Write Files

Write in order:
1. `index.md`
2. `task-001-{slug}.md`, `task-002-{slug}.md`, ...
3. `{feature}.prd.json`

Verify each file written successfully.

## CONTEXT BOUNDARIES:

- This step expects: Approved decomposition, task list, DAG
- This step produces: index.md, task-XXX.md files, PRD.json

## OUTPUT FORMAT:

```
## Specs Generated

Location: docs/specs/{feature-slug}/

### Files Created
- [x] index.md (orchestrator)
- [x] task-001-{slug}.md
- [x] task-002-{slug}.md
- [x] ...
- [x] {feature}.prd.json

### Summary
- Tasks: {count}
- Total Steps: {step_count}
- Lines: {total_lines}
- JSON valid: Yes
```

## BREAKPOINT: Specifications Generated (OBLIGATOIRE)

AFFICHE cette boîte:

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

Remplis les variables:
- `{complexity}`: `TINY`/`SMALL`/`STANDARD`/`LARGE`
- `{score}`: Complexity score
- `{task_count}`: Number of task files
- `{step_count}`: Total steps across tasks
- `{total_hours}`: Estimated hours
- `{lines}`: Lines in index.md
- `{slug}`: Task slug for preview
- `{estimate}`: Estimated minutes for task
- `{feature}`: Feature slug
- `{size}`: PRD.json size in KB
- `{feature-slug}`: Feature identifier

APPELLE AskUserQuestion:
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

⏸️ ATTENDS la reponse utilisateur avant de continuer.

## NEXT STEP TRIGGER:

When user approves specs, proceed to `step-03-generate-ralph.md`.

If user selects "Skip Ralph", proceed to completion summary.
