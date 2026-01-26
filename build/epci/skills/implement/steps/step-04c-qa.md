---
name: step-04c-qa
description: QA validation review
prev_step: steps/step-04-review.md
next_step: steps/step-05-document.md
---

# Step 04c: QA Review

## MANDATORY EXECUTION RULES (READ FIRST):

- :red_circle: NEVER skip acceptance criteria verification
- :red_circle: NEVER approve without testing happy paths
- :red_circle: NEVER ignore error handling validation
- :white_check_mark: ALWAYS invoke @qa-reviewer agent
- :white_check_mark: ALWAYS verify all acceptance criteria met
- :white_check_mark: ALWAYS test edge cases and error paths
- :large_blue_circle: YOU ARE A QA ENGINEER finding bugs before users do
- :thought_balloon: FOCUS on user experience and error handling

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

┌─────────────────────────────────────────────────────────────────────┐
│ :pause_button: BREAKPOINT — QA Review Complete                                  │
├─────────────────────────────────────────────────────────────────────┤
│ Feature: {feature-slug}                                             │
│                                                                     │
│ QA Summary:                                                         │
│ • Acceptance Criteria: {N}/{N} met                                  │
│ • Test Pass Rate: {%}                                               │
│ • Defects: {N} ({severity breakdown})                               │
│                                                                     │
│ Verdict: {PASS | FAIL}                                              │
│                                                                     │
│ ┌─ Options ──────────────────────────────────────────────────────┐ │
│ │  1. Proceed (if PASS)                                          │ │
│ │  2. Fix defects first                                          │ │
│ │  3. Request additional testing                                 │ │
│ │  4. Accept known issues (document)                             │ │
│ └────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘

## NEXT STEP TRIGGER:

When QA validation passes, proceed to `step-05-document.md`.
