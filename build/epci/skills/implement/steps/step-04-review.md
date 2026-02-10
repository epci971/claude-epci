---
name: step-04-review
description: Code review phase [I]
prev_step: steps/step-03-code.md
next_step: steps/step-05-document.md
conditional_next:
  - condition: "security_concerns == true"
    step: steps/step-04b-security.md
  - condition: "qa_needed == true"
    step: steps/step-04c-qa.md
---

# Step 04: Review [I]

## Reference Files

@../references/review-checklists.md
@../references/output-templates.md

| Reference | Purpose |
|-----------|---------|
| review-checklists.md | Code quality checklist (section #code-review-checklist) |
| output-templates.md | Review output format (section #review-output) |

*(Breakpoint templates are inline in this file)*

## MANDATORY EXECUTION RULES (READ FIRST):

- 🔴 NEVER auto-approve without thorough analysis
- 🔴 NEVER skip security consideration
- 🔴 NEVER ignore edge cases
- ✅ ALWAYS invoke @code-reviewer agent
- ✅ ALWAYS check for OWASP top 10 vulnerabilities
- ✅ ALWAYS verify test coverage meets target
- ✅ ALWAYS verify code follows identified patterns
- 🔵 YOU ARE A SKEPTICAL REVIEWER, not a defender
- 💭 FOCUS on what could go wrong, not what went right

## EXECUTION PROTOCOLS:

### 0. Check for Parallel Review Results (Team Mode)

IF team_config.mode == "active" AND team_config.parallel_agents.code_reviewer.enabled:

The Code Reviewer was launched in background during step-03 coding (by step-03b-team).

```
CHECK background task status for code_reviewer_task_id:
  IF completed:
    READ results from background task output
    LOG "Using parallel Code Reviewer results (ran during coding)"
    SKIP to Section 2 (Process Review Results)
  IF still_running:
    WAIT for completion (with timeout)
    READ results when available
    LOG "Parallel Code Reviewer completed (waited for results)"
    SKIP to Section 2
  IF failed:
    WARN "Parallel Code Reviewer failed, running synchronous review"
    PROCEED to Section 1 (synchronous invocation)
```

IF team_config.mode != "active" OR no background task:
  PROCEED to Section 1 (standard synchronous invocation)

### 1. Invoke @code-reviewer (Opus)

Delegate code review to the code-reviewer agent:

LANCE Task({
  subagent_type: "code-reviewer",
  model: "opus",
  prompt: `
## Files to Review
{modified_files_list}

## Original Requirements
{feature_requirements}

## Implementation Plan Summary
{plan_summary}

## Review Focus
- Code quality: patterns, naming, error handling
- Test coverage: target 70% minimum
- Security: OWASP Top 10 awareness
- Plan alignment: implementation matches plan

## Expected Output
Review report with:
- Files reviewed count
- Issues found (Critical/Important/Minor)
- Test coverage assessment
- Verdict: APPROVED / CHANGES_REQUIRED / SECURITY_REVIEW_NEEDED
  `
})

### 2. Process Review Results

Based on @code-reviewer verdict:
- If APPROVED: continue to breakpoint
- If CHANGES_REQUIRED: address findings before proceeding
- If SECURITY_REVIEW_NEEDED: proceed to step-04b-security

### 3. Verify Test Coverage

- Confirm coverage target met (min 70%)
- Identify any untested paths flagged by reviewer
- Check edge case coverage

### 4. Determine Additional Reviews

Based on review findings:
- Security review required? → step-04b-security
- QA validation required? → step-04c-qa
- Performance concerns? → note for documentation

### 5. Update Feature Document §4

**MANDATORY**: After all reviews complete, use **Edit tool** to fill §4 in the Feature Document.

Path: `docs/features/{feature-slug}-{YYYYMMDD-HHmmss}.md` (from `artifacts.feature_doc`)

EXECUTE Edit({
  file_path: "{feature_doc_path}",
  old_string: "## §4 — Revue & Validation\n> Section remplie par step-04-review [I]\n\n*En attente de la phase Inspect...*",
  new_string: "## §4 — Revue & Validation\n> Rempli par step-04-review [I]\n\n### @code-reviewer\n- Verdict: {cr_verdict}\n- Issues critiques: {cr_critical_count}\n- Issues resolues: {cr_resolved_count}\n- Resume: {cr_summary}\n\n### @security-auditor {si_applicable}\n- Verdict: {sa_verdict}\n- Findings: {sa_findings}\n\n### @qa-reviewer {si_applicable}\n- Verdict: {qa_verdict}\n- Findings: {qa_findings}"
})

Fill variables from actual agent outputs. Omit @security-auditor and @qa-reviewer sections if not invoked (use "N/A - non invoque" as verdict).

## CONTEXT BOUNDARIES:

- This step expects: Implemented code, passing tests, feature_doc_path (from step-00)
- This step produces: Review reports, Feature Document §4 filled

## REVIEW CHECKLIST:

APPLY checklist from review-checklists.md (section #code-review-checklist importé ci-dessus).

## OUTPUT FORMAT:

APPLY template from output-templates.md (section #review-output importé ci-dessus).

## BREAKPOINT: Code Review Complete (OBLIGATOIRE)

AFFICHE cette boîte:

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

Remplis les variables:
- `{duration}`: Time spent in code phase
- `{tasks_completed}`: Number of tasks done
- `{files_modified}`: Files changed count
- `{tests_passing}`: Passing test count
- `{tests_total}`: Total test count
- `{feature_id}`: Feature identifier for checkpoint
- `{coverage}`: Current coverage percentage
- `{issues_count}`: Number of issues found by @code-reviewer
- `{severity}`: Highest severity (`Critical`/`Important`/`Minor`)

APPELLE AskUserQuestion({
  questions: [{
    question: "Proceder avec le resultat de la review?",
    header: "Phase C->I",
    multiSelect: false,
    options: [
      { label: "Accepter et Documenter (Recommended)", description: "Passer a la phase documentation" },
      { label: "Demander Security Review", description: "Audit securite approfondi necessaire" },
      { label: "Demander QA Validation", description: "Tests QA additionnels necessaires" },
      { label: "Traiter les findings", description: "Corriger les issues avant de continuer" }
    ]
  }]
})

⏸️ ATTENDS la reponse utilisateur avant de continuer.

## NEXT STEP TRIGGER:

When review is approved and no additional reviews needed, proceed to `step-05-document.md`.

If security concerns identified, proceed to `step-04b-security.md`.

If QA validation needed, proceed to `step-04c-qa.md`.
