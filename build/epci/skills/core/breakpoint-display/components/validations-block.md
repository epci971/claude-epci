# Component: Validations Block

## Overview

Composant réutilisable pour afficher verdicts des subagents.

**Usage:** `plan-review`

## Input Structure

```typescript
{
  plan_validator: {
    verdict: "{VERDICT}",
    completeness: "{STATUS}",
    consistency: "{STATUS}",
    feasibility: "{STATUS}",
    quality: "{STATUS}"
  },
  code_reviewer: {
    verdict: "{VERDICT}",
    summary: "{TEXT}"
  },
  security_auditor: {
    verdict: "{VERDICT}"
  },
  qa_reviewer: {
    verdict: "{VERDICT}"
  }
}
```

## Display Format

### Phase 1 (plan-validator only)

```
│ ✅ VALIDATIONS                                                      │
│ ├── @plan-validator: {verdict}                                     │
│ │   ├── Completeness: {status}                                     │
│ │   ├── Consistency: {status}                                      │
│ │   ├── Feasibility: {status}                                      │
│ │   └── Quality: {status}                                          │
│ └── Skills chargés: {skills_list}                                  │
```

### Phase 2 (multiple reviewers)

```
│ ✅ VALIDATIONS                                                      │
│ ├── @code-reviewer: {verdict} ({summary})                          │
│ ├── @security-auditor: {verdict}                                   │
│ └── @qa-reviewer: {verdict}                                        │
```

## Example: Phase 1

```typescript
Input:
{
  plan_validator: {
    verdict: "APPROVED",
    completeness: "OK",
    consistency: "OK",
    feasibility: "OK",
    quality: "OK"
  }
}

Output:
│ ✅ VALIDATIONS                                                      │
│ ├── @plan-validator: APPROVED                                      │
│ │   ├── Completeness: OK                                           │
│ │   ├── Consistency: OK                                            │
│ │   ├── Feasibility: OK                                            │
│ │   └── Quality: OK                                                │
│ └── Skills chargés: testing-strategy, php-symfony, security-patterns │
```

## Example: Phase 2

```typescript
Input:
{
  code_reviewer: {
    verdict: "APPROVED",
    summary: "Code quality excellent, naming conventions respected"
  },
  security_auditor: {
    verdict: "APPROVED"
  },
  qa_reviewer: {
    verdict: "APPROVED"
  }
}

Output:
│ ✅ VALIDATIONS                                                      │
│ ├── @code-reviewer: APPROVED (Code quality excellent, naming conventions respected) │
│ ├── @security-auditor: APPROVED                                    │
│ └── @qa-reviewer: APPROVED                                         │
```

## Conditional Display

Only display agents that were invoked:
- `@plan-validator`: Always in Phase 1
- `@code-reviewer`: Always in Phase 2
- `@security-auditor`: Only if auth/security patterns detected
- `@qa-reviewer`: Only if 5+ test files
