---
name: step-04c-qa
description: QA validation review
prev_step: steps/step-04-review.md
next_step: steps/step-05-document.md
---

# Step 04c: QA Review

## Reference Files

@../references/breakpoint-formats.md
@../references/review-checklists.md
@../references/output-templates.md

| Reference | Purpose |
|-----------|---------|
| review-checklists.md | QA validation checklist (section #qa-validation-checklist) |
| output-templates.md | QA output format (section #qa-output) |
| breakpoint-formats.md | Breakpoint ASCII box (section #qa) |

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

AFFICHE la boîte QA (section #qa du fichier breakpoint-formats.md importé ci-dessus).

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
