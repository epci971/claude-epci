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

## BREAKPOINT:

```typescript
@skill:breakpoint-system
  type: validation
  title: "QA Review Complete"
  data: {
    context: "QA validation by @qa-reviewer complete",
    item_to_validate: {
      objectif: "Confirm feature meets acceptance criteria",
      contexte: "Feature: {feature-slug}, AC met: {N}/{N}",
      contraintes: "Test pass rate: {%}%, Defects: {N}",
      success_criteria: "All acceptance criteria met, no blocking defects"
    }
  }
  ask: {
    question: "Accept QA validation outcome?",
    header: "QA Review",
    options: [
      {label: "Proceed (Recommended)", description: "QA validation passed"},
      {label: "Fix Defects First", description: "Address found issues"},
      {label: "Accept Known Issues", description: "Document and proceed"}
    ]
  }
  suggestions: [
    {pattern: "ac", text: "{N}/{N} acceptance criteria met", priority: "P1"},
    {pattern: "defects", text: "Review {N} defects found", priority: "P2"}
  ]
```

## NEXT STEP TRIGGER:

When QA validation passes, proceed to `step-05-document.md`.
