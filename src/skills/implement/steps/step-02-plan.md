---
name: step-02-plan
description: Create implementation plan phase [P]
prev_step: steps/step-01-explore.md
next_step: steps/step-03-code.md
---

# Step 02: Plan [P]

## Reference Files

@../references/output-templates.md

| Reference | Purpose |
|-----------|---------|
| output-templates.md | Plan output format (section #plan-output) |

*(Breakpoint templates are inline in this file)*

## MANDATORY EXECUTION RULES (READ FIRST):

- 🔴 NEVER start coding before plan approval
- 🔴 NEVER create plan without exploration data
- 🔴 NEVER skip test strategy definition
- ✅ ALWAYS define implementation order
- ✅ ALWAYS specify test approach for each component
- ✅ ALWAYS get user approval via breakpoint
- 🔵 YOU ARE AN ARCHITECT designing the build sequence
- 💭 FOCUS on testability and incremental progress

## EXECUTION PROTOCOLS:

### 1. Synthesize Exploration Findings

- Review identified patterns
- Review dependencies
- Review files to modify/create

### 2. Invoke @planner (Sonnet)

Delegate task decomposition to the planner agent:

```typescript
Task({
  subagent_type: "planner",
  model: "sonnet",
  prompt: `
## Feature
{feature_name}

## Requirements
{requirements_from_exploration}

## Identified Files
{files_to_modify_create}

## Constraints
{identified_constraints}

## Output Format
Atomic tasks (2-15 min each) with dependencies, ordered by implementation sequence.
Include test strategy for each task.
  `
})
```

### 3. Validate Plan with @plan-validator (Opus)

```typescript
Task({
  subagent_type: "plan-validator",
  model: "opus",
  prompt: `
## Plan to Validate
{plan_from_planner}

## Feature Requirements
{original_requirements}

## Validation Checklist
- Completeness: All requirements covered
- Consistency: No circular dependencies
- Feasibility: Resources available
- Quality: Tasks atomic and testable (TDD strategy defined)

## Expected Output
APPROVED or NEEDS_REVISION with specific feedback
  `
})
```

**Handle Result:**
- If APPROVED: continue to breakpoint
- If NEEDS_REVISION: apply feedback and re-invoke @planner

### 4. Update Feature Document

- Add implementation plan section
- Add test strategy section
- Add acceptance criteria mapping

## CONTEXT BOUNDARIES:

- This step expects: Exploration findings, dependency map
- This step produces: Implementation plan, test strategy, updated Feature Document

## OUTPUT FORMAT:

APPLY template from output-templates.md (section #plan-output importé ci-dessus).

## BREAKPOINT: Plan Validation (OBLIGATOIRE)

AFFICHE cette boîte:

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

Remplis les variables:
- `{complexity}`: `TINY`/`SMALL`/`STANDARD`/`LARGE`
- `{score}`: Numeric complexity score
- `{files_count}`: Number of files to modify
- `{hours}`: Estimated hours
- `{risk_level}`: `LOW`/`MEDIUM`/`HIGH`
- `{risk_notes}`: Risk description text
- `{validation_status}`: `APPROVED` or issues found
- `{phases}`: Number of phases in plan
- `{summary_1}`, `{summary_2}`, `{summary_3}`: Phase summaries
- `{estimate_1}`, `{estimate_2}`, `{estimate_3}`: Phase estimates
- `{remaining_tasks}`: Tasks beyond preview
- `{feature-slug}`: Feature identifier
- `{coverage_target}`: Target test coverage percentage

APPELLE AskUserQuestion({
  questions: [{
    question: "Approuver le plan d'implementation?",
    header: "Plan Review",
    multiSelect: false,
    options: [
      { label: "Approuver et Coder (Recommended)", description: "Proceder a l'implementation TDD" },
      { label: "Modifier le plan", description: "Ajuster phases ou approche" },
      { label: "Abandonner", description: "Reviser requirements d'abord" }
    ]
  }]
})

⏸️ ATTENDS la reponse utilisateur avant de continuer.

## NEXT STEP TRIGGER:

When plan is approved by user, proceed to `step-03-code.md`.
