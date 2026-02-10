---
name: step-00-init
description: Initialize implement workflow and detect complexity
prev_step: null
next_step: steps/step-00c-worktree.md
conditional_next:
  - condition: "complexity == TINY or complexity == SMALL"
    step: steps/step-00b-turbo.md
  - condition: "complexity == STANDARD or complexity == LARGE"
    step: steps/step-00c-worktree.md
---

# Step 00: Initialization

## Reference Files

@../references/feature-document-template.md

| Reference | Purpose |
|-----------|---------|
| feature-document-template.md | Feature Document structure and section ownership |

*(Breakpoint templates are inline in this file)*

## MANDATORY EXECUTION RULES (READ FIRST):

- 🔴 NEVER skip complexity detection
- 🔴 NEVER proceed without valid feature-slug
- ✅ ALWAYS parse input arguments first
- ✅ ALWAYS invoke complexity-calculator
- ✅ ALWAYS create Feature Document skeleton if STANDARD+
- 💭 FOCUS on correct routing based on complexity

## EXECUTION PROTOCOLS:

1. **Parse** input arguments
   - Extract feature-slug (required)
   - Extract spec-path (optional, prefixed with @)
   - Extract flags:
     - `--team`: Force team mode (multi-agent orchestration)
     - `--no-team`: Disable team mode (classic sequential execution)

2. **Validate** input
   - feature-slug must be kebab-case
   - If spec-path provided, verify file exists
   - If both `--team` AND `--no-team` provided: ERROR "Conflicting flags: --team and --no-team cannot be used together"
   - Store flags in execution context: `{ flag_team: bool, flag_no_team: bool }`

3. **Load** spec if provided
   - Read spec file content
   - Extract requirements, acceptance criteria

4. **Detect** complexity using complexity-calculator
   - Analyze scope from spec or description
   - Estimate LOC and file count
   - Determine complexity level: TINY, SMALL, STANDARD, LARGE

5. **Route** based on complexity
   - TINY/SMALL → step-00b-turbo (redirect to /quick)
   - STANDARD/LARGE → step-00c-worktree (worktree setup, then explore)

6. **Resume Worktree Context** (if --continue with existing state)

IF resuming from state AND state.worktree.enabled == true:

EXECUTE Bash({
  command: "./scripts/worktree-status.sh {feature-slug}",
  description: "Check existing worktree status"
})

Parse result:
- If exists AND status == "active":
  - Change working directory to state.worktree.path
  - Log: "Resumed in worktree: {path}"
- If exists but status != "active":
  - Warn: "Worktree exists but status is {status}"
  - Offer to recreate or continue in main repo
- If not exists:
  - Warn: "Worktree no longer exists"
  - Offer to recreate or continue in main repo

7. **Initialize** Feature Document (STANDARD+ only)

Generate timestamp: `YYYYMMDD-HHmmss` format (e.g., `20260210-143052`)
Construct path: `feature_doc_path = docs/features/{feature-slug}-{YYYYMMDD-HHmmss}.md`

EXECUTE Bash({
  command: "mkdir -p docs/features",
  description: "Ensure docs/features directory exists"
})

EXECUTE Write({
  file_path: "{feature_doc_path}",
  content: "Feature Document template from @feature-document-template.md with:
    - §0 filled: slug, complexity, date, branch, spec source
    - §1 filled: IF @spec-path provided, extract objective + criteria from spec
                  ELSE write placeholder for user to complete
    - §2-§5: placeholder text (will be filled by subsequent steps)"
})

Store `feature_doc_path` for all subsequent steps.

Update state-manager:
```
state_manager.updateFeature("{feature-slug}", {
  artifacts: { feature_doc: "{feature_doc_path}" }
})
```

## CONTEXT BOUNDARIES:

- This step expects: User input (feature-slug, optional @spec-path)
- This step produces: Validated context, complexity level, routing decision, feature_doc_path

## OUTPUT FORMAT:

```
## Initialization Complete

Feature: {feature-slug}
Spec: {spec-path or "none provided"}
Complexity: {TINY|SMALL|STANDARD|LARGE}

Routing: {next step path}
```

## BREAKPOINT (for STANDARD+ only) - OBLIGATOIRE

AFFICHE cette boîte:

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

Remplis les variables:
- `{feature-slug}`: Kebab-case feature identifier from input
- `{complexity}`: `TINY`, `SMALL`, `STANDARD`, or `LARGE` from complexity-calculator
- `{loc}`: Estimated lines of code
- `{files}`: Estimated number of files

APPELLE AskUserQuestion({
  questions: [{
    question: "Proceder avec la complexite detectee?",
    header: "Complexity",
    multiSelect: false,
    options: [
      { label: "Continuer avec EPCI (Recommended)", description: "Workflow complet pour features STANDARD+" },
      { label: "Retrograder vers /quick", description: "Plus simple qu'estime, utiliser quick workflow" },
      { label: "Abandonner", description: "Affiner les requirements d'abord" }
    ]
  }]
})

⏸️ ATTENDS la reponse utilisateur avant de continuer.

## NEXT STEP TRIGGER:

### For STANDARD or LARGE complexity:
When complexity is STANDARD or LARGE and user confirms, proceed to `step-00c-worktree.md`.

The worktree step will:
- Offer worktree creation for parallel development
- If accepted: create worktree, then proceed to explore
- If declined: proceed to explore in main repo

### For TINY or SMALL complexity:
Proceed to `step-00b-turbo.md` (redirect to /quick).
