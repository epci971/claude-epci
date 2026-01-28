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

## Reference Files

@../references/review-checklists.md
@../references/output-templates.md

| Reference | Purpose |
|-----------|---------|
| review-checklists.md | OWASP Top 10 checklist (section #security-review-checklist) |
| output-templates.md | Security audit output format (section #security-output) |

*(Breakpoint templates are inline in this file)*

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
Verify against all categories (see review-checklists.md#security-review-checklist)

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

APPLY checklist from review-checklists.md (section #security-review-checklist importé ci-dessus).

## OUTPUT FORMAT:

APPLY template from output-templates.md (section #security-output importé ci-dessus).

## BREAKPOINT: Security Review Complete (OBLIGATOIRE)

AFFICHE cette boîte:

```
┌─────────────────────────────────────────────────────────────────────┐
│ SECURITY REVIEW TERMINE                                             │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│ Audit securite par @security-auditor termine                        │
│                                                                     │
│ Feature: {feature-slug}                                             │
│ Vulnerabilites totales: {vuln_total}                                │
│ - Critical/High: {vuln_critical} (a corriger obligatoirement)       │
│ - Medium/Low: {vuln_low} (recommande)                               │
│                                                                     │
│ Critere de succes: Aucune vulnerabilite CRITICAL/HIGH non resolue   │
│                                                                     │
├─────────────────────────────────────────────────────────────────────┤
│ SUGGESTIONS PROACTIVES                                              │
│ [P1] OWASP Top 10 verifie                                           │
│ [P2] Reviser {vuln_total} findings avant de continuer               │
├─────────────────────────────────────────────────────────────────────┤
│ ┌─ Options ──────────────────────────────────────────────────────┐ │
│ │  [A] Continuer (Recommended) - Posture securite acceptable     │ │
│ │  [B] Corriger issues critiques - Traiter high-severity d'abord │ │
│ │  [C] Accepter le risque - Documenter et continuer              │ │
│ │  [?] Autre reponse...                                          │ │
│ └────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
```

Remplis les variables:
- `{feature-slug}`: Feature identifier
- `{vuln_total}`: Total vulnerabilities found
- `{vuln_critical}`: Critical/High severity count
- `{vuln_low}`: Medium/Low severity count

APPELLE:
```
AskUserQuestion({
  questions: [{
    question: "Accepter le resultat de la security review?",
    header: "Security",
    multiSelect: false,
    options: [
      { label: "Continuer (Recommended)", description: "Posture securite acceptable" },
      { label: "Corriger issues critiques", description: "Traiter les findings high-severity d'abord" },
      { label: "Accepter le risque", description: "Documenter la raison et continuer" }
    ]
  }]
})
```

⏸️ ATTENDS la reponse utilisateur avant de continuer.

## NEXT STEP TRIGGER:

When security review passes (no CRITICAL/HIGH unresolved), proceed to `step-05-document.md`.

If QA validation also needed, proceed to `step-04c-qa.md` first.
