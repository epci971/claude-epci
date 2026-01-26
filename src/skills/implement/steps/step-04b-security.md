---
name: step-04b-security
description: Security-focused code review
prev_step: steps/step-04-review.md
next_step: steps/step-05-document.md
conditional_next:
  - condition: "qa_needed == true"
    step: steps/step-04c-qa.md
---

# Step 04b: Security Review

## MANDATORY EXECUTION RULES (READ FIRST):

- :red_circle: NEVER approve code with HIGH severity vulnerabilities
- :red_circle: NEVER skip OWASP top 10 verification
- :red_circle: NEVER ignore authentication/authorization issues
- :white_check_mark: ALWAYS invoke @security-auditor agent
- :white_check_mark: ALWAYS verify input validation on all entry points
- :white_check_mark: ALWAYS check for sensitive data handling
- :large_blue_circle: YOU ARE A SECURITY AUDITOR assuming hostile input
- :thought_balloon: FOCUS on attack vectors and data protection

## EXECUTION PROTOCOLS:

1. **Invoke** @security-auditor agent
   - Pass all code handling external input
   - Pass authentication/authorization code
   - Pass data storage code

2. **OWASP Top 10** verification
   - A01: Broken Access Control
   - A02: Cryptographic Failures
   - A03: Injection
   - A04: Insecure Design
   - A05: Security Misconfiguration
   - A06: Vulnerable Components
   - A07: Auth Failures
   - A08: Data Integrity Failures
   - A09: Logging Failures
   - A10: SSRF

3. **Input validation** check
   - All user inputs validated
   - Proper sanitization
   - Type checking

4. **Data protection** review
   - Sensitive data encrypted
   - No secrets in code
   - Proper access controls

5. **Report** findings
   - Severity classification
   - Remediation recommendations
   - Re-review requirements

## CONTEXT BOUNDARIES:

- This step expects: Code with potential security concerns
- This step produces: Security audit report, remediation requirements

## SECURITY CHECKLIST:

```
### OWASP Top 10
- [ ] A01: Access control properly enforced
- [ ] A02: Cryptography correctly implemented
- [ ] A03: No injection vulnerabilities
- [ ] A04: Secure design patterns used
- [ ] A05: No misconfigurations
- [ ] A06: Dependencies up to date
- [ ] A07: Authentication robust
- [ ] A08: Data integrity verified
- [ ] A09: Proper logging without sensitive data
- [ ] A10: No SSRF vulnerabilities

### Input Handling
- [ ] All inputs validated
- [ ] Inputs sanitized before use
- [ ] Type checking enforced
- [ ] Size limits enforced

### Data Protection
- [ ] Sensitive data encrypted at rest
- [ ] Sensitive data encrypted in transit
- [ ] No secrets in code
- [ ] Proper key management
```

## OUTPUT FORMAT:

```
## Security Audit Report

### Summary
- Vulnerabilities: {N}
- Critical: {N}
- High: {N}
- Medium: {N}
- Low: {N}

### Findings
| # | Severity | Category | Location | Issue | Remediation |
|---|----------|----------|----------|-------|-------------|
| 1 | {sev} | {OWASP} | {file:line} | {desc} | {fix} |

### Required Fixes
{Critical and High must be fixed before proceeding}

### Verdict
{PASS | FAIL_CRITICAL | FAIL_HIGH}
```

## BREAKPOINT:

┌─────────────────────────────────────────────────────────────────────┐
│ :pause_button: BREAKPOINT — Security Review Complete                            │
├─────────────────────────────────────────────────────────────────────┤
│ Feature: {feature-slug}                                             │
│                                                                     │
│ Security Summary:                                                   │
│ • Vulnerabilities: {N total}                                        │
│ • Critical/High: {N} (must fix)                                     │
│ • Medium/Low: {N} (recommended fix)                                 │
│                                                                     │
│ Verdict: {PASS | FAIL}                                              │
│                                                                     │
│ ┌─ Options ──────────────────────────────────────────────────────┐ │
│ │  1. Proceed (if PASS)                                          │ │
│ │  2. Fix critical issues first                                  │ │
│ │  3. Request additional security review                         │ │
│ │  4. Accept risk (document reason)                              │ │
│ └────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘

## NEXT STEP TRIGGER:

When security review passes (no CRITICAL/HIGH unresolved), proceed to `step-05-document.md`.

If QA validation also needed, proceed to `step-04c-qa.md` first.
