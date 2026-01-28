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

@../references/breakpoint-formats.md
@../references/review-checklists.md
@../references/output-templates.md

| Reference | Purpose |
|-----------|---------|
| review-checklists.md | Code quality checklist (section #code-review-checklist) |
| output-templates.md | Review output format (section #review-output) |
| breakpoint-formats.md | Breakpoint ASCII box (section #review) |

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

### 1. Invoke @code-reviewer (Opus)

Delegate code review to the code-reviewer agent:

```typescript
Task({
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
```

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

## CONTEXT BOUNDARIES:

- This step expects: Implemented code, passing tests
- This step produces: Review findings, approval or revision requests

## REVIEW CHECKLIST:

APPLY checklist from [review-checklists.md#code-review-checklist](../references/review-checklists.md#code-review-checklist)

## OUTPUT FORMAT:

APPLY template from [output-templates.md#review-output](../references/output-templates.md#review-output)

## BREAKPOINT: Code Review Complete (OBLIGATOIRE)

AFFICHE le format depuis [breakpoint-formats.md#review](../references/breakpoint-formats.md#review)

APPELLE:
```
AskUserQuestion({
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
```

⏸️ ATTENDS la reponse utilisateur avant de continuer.

## NEXT STEP TRIGGER:

When review is approved and no additional reviews needed, proceed to `step-05-document.md`.

If security concerns identified, proceed to `step-04b-security.md`.

If QA validation needed, proceed to `step-04c-qa.md`.
