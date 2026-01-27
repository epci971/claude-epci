---
name: step-04c-qa
description: QA validation review
prev_step: steps/step-04-review.md
next_step: steps/step-05-document.md
---

# Step 04c: QA Review

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

```
### Acceptance Criteria
- [ ] AC1: {description} — {PASS|FAIL}
- [ ] AC2: {description} — {PASS|FAIL}
- [ ] AC3: {description} — {PASS|FAIL}

### Happy Paths
- [ ] Standard user flow works
- [ ] Expected inputs handled
- [ ] Output matches specification

### Edge Cases
- [ ] Boundary values handled
- [ ] Empty inputs handled
- [ ] Large inputs handled
- [ ] Special characters handled

### Error Handling
- [ ] Invalid input rejected gracefully
- [ ] Error messages user-friendly
- [ ] Recovery path available
- [ ] No crashes on errors
```

## OUTPUT FORMAT:

```
## QA Validation Report

### Acceptance Criteria
| # | Criterion | Status | Notes |
|---|-----------|--------|-------|
| 1 | {AC1} | {PASS|FAIL} | {notes} |
| 2 | {AC2} | {PASS|FAIL} | {notes} |

### Test Results
- Happy paths: {N}/{N} passed
- Edge cases: {N}/{N} passed
- Error handling: {N}/{N} passed

### Defects Found
| # | Severity | Description | Steps to Reproduce |
|---|----------|-------------|-------------------|
| 1 | {sev} | {desc} | {steps} |

### Verdict
{PASS | FAIL}
```

## BREAKPOINT: QA Review Complete (OBLIGATOIRE)

AFFICHE cette boîte:

```
┌─────────────────────────────────────────────────────────────────────┐
│ 🧪 QA REVIEW TERMINÉ                                                │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│ Validation QA par @qa-reviewer terminée                             │
│                                                                     │
│ Feature: {feature-slug}                                             │
│ Critères d'acceptation: {N}/{N} validés                             │
│ Taux de succès tests: {%}%                                          │
│ Défauts trouvés: {N}                                                │
│                                                                     │
│ Critère de succès: Tous les AC validés, aucun défaut bloquant       │
│                                                                     │
├─────────────────────────────────────────────────────────────────────┤
│ SUGGESTIONS PROACTIVES                                              │
│ [P1] {N}/{N} critères d'acceptation validés                         │
│ [P2] Réviser {N} défauts trouvés                                    │
├─────────────────────────────────────────────────────────────────────┤
│ ┌─ Options ──────────────────────────────────────────────────────┐ │
│ │  [A] Continuer (Recommended) — Validation QA réussie           │ │
│ │  [B] Corriger défauts d'abord — Traiter les issues trouvés     │ │
│ │  [C] Accepter issues connues — Documenter et continuer         │ │
│ │  [?] Autre réponse...                                          │ │
│ └────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
```

APPELLE:
```
AskUserQuestion({
  questions: [{
    question: "Accepter le résultat de la validation QA?",
    header: "QA Review",
    multiSelect: false,
    options: [
      { label: "Continuer (Recommended)", description: "Validation QA réussie" },
      { label: "Corriger défauts d'abord", description: "Traiter les issues trouvés" },
      { label: "Accepter issues connues", description: "Documenter et continuer" }
    ]
  }]
})
```

⏸️ ATTENDS la réponse utilisateur avant de continuer.

## NEXT STEP TRIGGER:

When QA validation passes, proceed to `step-05-document.md`.
