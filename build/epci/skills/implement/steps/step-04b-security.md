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

- 🔴 NEVER approve code with HIGH severity vulnerabilities
- 🔴 NEVER skip OWASP top 10 verification
- 🔴 NEVER ignore authentication/authorization issues
- ✅ ALWAYS invoke @security-auditor agent
- ✅ ALWAYS verify input validation on all entry points
- ✅ ALWAYS check for sensitive data handling
- 🔵 YOU ARE A SECURITY AUDITOR assuming hostile input
- 💭 FOCUS on attack vectors and data protection

## EXECUTION PROTOCOLS:

### 1. Invoke @security-auditor (Opus)

Delegate security audit to the security-auditor agent:

```typescript
Task({
  subagent_type: "security-auditor",
  model: "opus",
  prompt: `
## Files to Audit
{auth_security_files}

## Audit Scope
- Authentication/Authorization code
- Data validation and sanitization
- Secret handling and storage
- API security and input handling

## OWASP Top 10 Checklist
Verify against all categories:
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

## Expected Output
Security audit report with:
- Vulnerability count by severity (Critical/High/Medium/Low)
- OWASP category for each finding
- Location (file:line)
- Remediation recommendations
- Verdict: PASS / FAIL_CRITICAL / FAIL_HIGH
  `
})
```

### 2. Process Security Audit Results

Based on @security-auditor verdict:
- If PASS: continue to breakpoint
- If FAIL_CRITICAL/FAIL_HIGH: must fix before proceeding
- Medium/Low: recommended but not blocking

### 3. Verify Input Validation

Confirm audit covered:
- All user inputs validated
- Proper sanitization applied
- Type checking enforced

### 4. Document Security Posture

- Record audit findings in feature document
- Note any accepted risks with justification
- Track remediation for non-critical issues

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

## BREAKPOINT: Security Review Complete (OBLIGATOIRE)

AFFICHE cette boîte:

```
┌─────────────────────────────────────────────────────────────────────┐
│ 🔐 SECURITY REVIEW TERMINÉ                                          │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│ Audit sécurité par @security-auditor terminé                        │
│                                                                     │
│ Feature: {feature-slug}                                             │
│ Vulnérabilités totales: {N}                                         │
│ • Critical/High: {N} (à corriger obligatoirement)                   │
│ • Medium/Low: {N} (recommandé)                                      │
│                                                                     │
│ Critère de succès: Aucune vulnérabilité CRITICAL/HIGH non résolue   │
│                                                                     │
├─────────────────────────────────────────────────────────────────────┤
│ SUGGESTIONS PROACTIVES                                              │
│ [P1] OWASP Top 10 vérifié                                           │
│ [P2] Réviser {N} findings avant de continuer                        │
├─────────────────────────────────────────────────────────────────────┤
│ ┌─ Options ──────────────────────────────────────────────────────┐ │
│ │  [A] Continuer (Recommended) — Posture sécurité acceptable     │ │
│ │  [B] Corriger issues critiques — Traiter high-severity d'abord │ │
│ │  [C] Accepter le risque — Documenter et continuer              │ │
│ │  [?] Autre réponse...                                          │ │
│ └────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
```

APPELLE:
```
AskUserQuestion({
  questions: [{
    question: "Accepter le résultat de la security review?",
    header: "Security",
    multiSelect: false,
    options: [
      { label: "Continuer (Recommended)", description: "Posture sécurité acceptable" },
      { label: "Corriger issues critiques", description: "Traiter les findings high-severity d'abord" },
      { label: "Accepter le risque", description: "Documenter la raison et continuer" }
    ]
  }]
})
```

⏸️ ATTENDS la réponse utilisateur avant de continuer.

## NEXT STEP TRIGGER:

When security review passes (no CRITICAL/HIGH unresolved), proceed to `step-05-document.md`.

If QA validation also needed, proceed to `step-04c-qa.md` first.
