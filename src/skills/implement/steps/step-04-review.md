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

## MANDATORY EXECUTION RULES (READ FIRST):

- :red_circle: NEVER auto-approve without thorough analysis
- :red_circle: NEVER skip security consideration
- :red_circle: NEVER ignore edge cases
- :white_check_mark: ALWAYS invoke @code-reviewer agent
- :white_check_mark: ALWAYS check for OWASP top 10 vulnerabilities
- :white_check_mark: ALWAYS verify test coverage meets target
- :white_check_mark: ALWAYS verify code follows identified patterns
- :large_blue_circle: YOU ARE A SKEPTICAL REVIEWER, not a defender
- :thought_balloon: FOCUS on what could go wrong, not what went right

## EXECUTION PROTOCOLS:

1. **Invoke** @code-reviewer agent
   - Pass all modified/created files
   - Request comprehensive review

2. **Review** test coverage
   - Verify coverage target met (min 70%)
   - Identify untested paths
   - Check edge case coverage

3. **Security** assessment
   - Check for injection vulnerabilities
   - Check for authentication/authorization issues
   - Check for data exposure risks
   - If concerns found → proceed to step-04b-security

4. **Code quality** check
   - Verify patterns followed
   - Check naming conventions
   - Review error handling
   - Check for code smells

5. **Determine** additional reviews needed
   - Security review required?
   - QA validation required?
   - Performance review required?

## CONTEXT BOUNDARIES:

- This step expects: Implemented code, passing tests
- This step produces: Review findings, approval or revision requests

## REVIEW CHECKLIST:

```
### Code Quality
- [ ] Follows existing patterns
- [ ] Proper error handling
- [ ] No code duplication
- [ ] Clear naming
- [ ] No dead code

### Tests
- [ ] Coverage target met
- [ ] Edge cases covered
- [ ] Failure modes tested
- [ ] Integration tested

### Security
- [ ] No injection vulnerabilities
- [ ] Auth/authz correct
- [ ] No sensitive data exposure
- [ ] Input validation present

### Performance
- [ ] No N+1 queries
- [ ] Appropriate caching
- [ ] No blocking operations in hot paths
```

## OUTPUT FORMAT:

```
## Code Review Results

### Summary
- Files reviewed: {N}
- Issues found: {N}
- Severity: {HIGH|MEDIUM|LOW|NONE}

### Findings
| # | Severity | File | Issue | Recommendation |
|---|----------|------|-------|----------------|
| 1 | {severity} | {file} | {issue} | {fix} |

### Test Coverage
- Achieved: {%}
- Target: {%}
- Status: {PASS|FAIL}

### Verdict
{APPROVED | CHANGES_REQUIRED | SECURITY_REVIEW_NEEDED | QA_NEEDED}
```

## BREAKPOINT:

┌─────────────────────────────────────────────────────────────────────┐
│ :pause_button: BREAKPOINT — Code Review Complete                                │
├─────────────────────────────────────────────────────────────────────┤
│ Feature: {feature-slug}                                             │
│                                                                     │
│ Review Summary:                                                     │
│ • Issues: {N} ({severity breakdown})                                │
│ • Coverage: {%}                                                     │
│ • Security: {status}                                                │
│                                                                     │
│ Verdict: {APPROVED | CHANGES_REQUIRED}                              │
│                                                                     │
│ ┌─ Options ──────────────────────────────────────────────────────┐ │
│ │  1. Accept and proceed to documentation (Recommended if PASS)  │ │
│ │  2. Request security review                                    │ │
│ │  3. Request QA validation                                      │ │
│ │  4. Address findings first                                     │ │
│ └────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘

## NEXT STEP TRIGGER:

When review is approved and no additional reviews needed, proceed to `step-05-document.md`.

If security concerns identified, proceed to `step-04b-security.md`.

If QA validation needed, proceed to `step-04c-qa.md`.
