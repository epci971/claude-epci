---
name: step-04c-qa
description: QA validation review
prev_step: steps/step-04-review.md
next_step: steps/step-05-document.md
---

# Step 04c: QA Review

## Reference Files

@../references/review-checklists.md
@../references/output-templates.md

| Reference | Purpose |
|-----------|---------|
| review-checklists.md | QA validation checklist (section #qa-validation-checklist) |
| output-templates.md | QA output format (section #qa-output) |

*(Breakpoint templates are inline in this file)*

## MANDATORY EXECUTION RULES (READ FIRST):

- 🔴 NEVER skip acceptance criteria verification
- 🔴 NEVER approve without testing happy paths
- 🔴 NEVER ignore error handling validation
- ✅ ALWAYS invoke @qa-reviewer agent
- ✅ ALWAYS verify all acceptance criteria met
- ✅ ALWAYS test edge cases and error paths
- 🔵 YOU ARE A QA ENGINEER finding bugs before users do
- 💭 FOCUS on user experience and error handling

## EXECUTION PROTOCOLS:

1. **Invoke** @qa-reviewer agent
   - Pass feature requirements
   - Pass acceptance criteria
   - Pass implementation code

2. **Verify** acceptance criteria
   - Map each criterion to test
   - Confirm all criteria met
   - Document any gaps

3. **Test** happy paths
   - Normal usage scenarios
   - Expected inputs
   - Standard workflows

4. **Test** edge cases
   - Boundary conditions
   - Empty/null inputs
   - Large inputs
   - Concurrent access

5. **Test** error handling
   - Invalid inputs
   - System failures
   - Network issues
   - User error recovery

6. **Document** test results
   - Pass/fail for each scenario
   - Defects found
   - Recommendations

## CONTEXT BOUNDARIES:

- This step expects: Implemented feature with passing unit tests
- This step produces: QA validation report, defect list

## QA CHECKLIST:

APPLY checklist from review-checklists.md (section #qa-validation-checklist importé ci-dessus).

## OUTPUT FORMAT:

APPLY template from output-templates.md (section #qa-output importé ci-dessus).

## BREAKPOINT: QA Review Complete (OBLIGATOIRE)

AFFICHE cette boîte:

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

Remplis les variables:
- `{feature-slug}`: Feature identifier
- `{ac_passed}`: Acceptance criteria passed
- `{ac_total}`: Total acceptance criteria
- `{test_success_rate}`: Test success percentage
- `{defects_count}`: Number of defects found

APPELLE:
```
AskUserQuestion({
  questions: [{
    question: "Accepter le resultat de la validation QA?",
    header: "QA Review",
    multiSelect: false,
    options: [
      { label: "Continuer (Recommended)", description: "Validation QA reussie" },
      { label: "Corriger defauts d'abord", description: "Traiter les issues trouves" },
      { label: "Accepter issues connues", description: "Documenter et continuer" }
    ]
  }]
})
```

⏸️ ATTENDS la reponse utilisateur avant de continuer.

## NEXT STEP TRIGGER:

When QA validation passes, proceed to `step-05-document.md`.
