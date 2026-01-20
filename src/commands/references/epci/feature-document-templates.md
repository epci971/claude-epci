# Feature Document Templates

> Complete templates for all sections of the Feature Document.

## Standard Feature Document Structure

**Location:** `docs/features/<feature-slug>.md`

```markdown
# Feature Document — [Title]

## §1 — Functional Brief
[Created by /brief with thorough exploration]

## §2 — Implementation Plan
[Generated in Phase 1]

## §3 — Implementation & Finalization
[Updated in Phases 2-3]
```

---

## §2 — Implementation Plan Templates

### Scenario A: With Native Plan Import

Use when `--from-native-plan` flag was used. The §2 already contains native plan metadata and original plan. Update only the "✅ Plan Raffiné & Validé" section:

```markdown
### ✅ Plan Raffiné & Validé

#### Impacted Files
| File | Action | Risk |
|------|--------|------|
| src/Service/X.php | Modify | Medium |
| src/Entity/Y.php | Create | Low |
| tests/Unit/XTest.php | Create | Low |

#### Atomic Tasks (2-15 min each)
1. [ ] **Create entity Y** (5 min)
   - File: `src/Entity/Y.php`
   - Test: `tests/Unit/Entity/YTest.php`
   - Dependencies: None
   - From native plan: [reference to original task number or description]

2. [ ] **Modify service X** (10 min)
   - File: `src/Service/X.php`
   - Test: `tests/Unit/Service/XTest.php`
   - Dependencies: Task 1
   - From native plan: [reference to original task number or description]

3. [ ] **Add integration test** (8 min)
   - File: `tests/Integration/XYIntegrationTest.php`
   - Test: Self-validating
   - Dependencies: Task 1, Task 2

#### Risks
| Risk | Probability | Mitigation |
|------|-------------|------------|
| Breaking change | Medium | Regression tests |
| Performance impact | Low | Load testing |

#### Validation
- **@plan-validator**: APPROVED
- **Native plan refined**: ✅ High-level tasks broken down into atomic steps
- **Dependencies mapped**: ✅ All task dependencies identified
```

### Scenario B: Standard Workflow (no native plan)

Use for normal `/brief` → `/epci` workflow without native plan import:

```markdown
## §2 — Implementation Plan

### Impacted Files
| File | Action | Risk |
|------|--------|------|
| src/Service/X.php | Modify | Medium |
| src/Entity/Y.php | Create | Low |
| tests/Unit/XTest.php | Create | Low |

### Tasks
1. [ ] **Create entity Y** (5 min)
   - File: `src/Entity/Y.php`
   - Test: `tests/Unit/Entity/YTest.php`
   - Dependencies: None

2. [ ] **Modify service X** (10 min)
   - File: `src/Service/X.php`
   - Test: `tests/Unit/Service/XTest.php`
   - Dependencies: Task 1

3. [ ] **Add integration test** (8 min)
   - File: `tests/Integration/XYIntegrationTest.php`
   - Test: Self-validating
   - Dependencies: Task 1, Task 2

### Risks
| Risk | Probability | Mitigation |
|------|-------------|------------|
| Breaking change | Medium | Regression tests |
| Performance impact | Low | Load testing |

### Validation
- **@plan-validator**: APPROVED
- **Task granularity**: ✅ All tasks 2-15 min
- **Dependencies mapped**: ✅ Clear execution order
```

---

## §3 — Implementation & Finalization Template

Updated during Phases 2-3:

```markdown
## §3 — Implementation & Finalization

### Code Review (Phase 2)

**@code-reviewer verdict:** APPROVED (or NEEDS_REVISION)

**Issues found:**
- [ ] 🔴 Critical: [Description] → Fixed in commit abc123
- [ ] 🟠 Important: [Description] → Fixed in commit def456
- [ ] 🟡 Minor: [Description] → Acknowledged, no action needed

**Security audit:** (if applicable)
- **@security-auditor verdict:** APPROVED
- Vulnerabilities checked: OWASP Top 10, Auth patterns
- Result: No critical issues

**QA review:** (if applicable)
- **@qa-reviewer verdict:** APPROVED
- Test coverage: 85%
- Edge cases covered: ✅

### Documentation (Phase 3)

**@doc-generator output:**
- API documentation updated: ✅
- README updated: ✅
- Inline comments added: ✅

### Git Status

**Commit:** abc123def456789
**Branch:** feature/[slug]
**Status:** Ready for review

**Files modified:**
- src/Service/X.php
- src/Entity/Y.php
- tests/Unit/XTest.php
- tests/Integration/XYIntegrationTest.php

### Finalization Checklist

- [x] All tasks completed
- [x] Tests passing (100%)
- [x] Code review approved
- [x] Security audit passed (if applicable)
- [x] Documentation updated
- [x] Changes committed
```

---

## Complete Example: Standard Feature

```markdown
# Feature Document — User Authentication

## §1 — Functional Brief

### Objectif
Implement user authentication with JWT tokens

### Contexte Technique
**Stack détecté**: PHP 8.2, Symfony 6.4, Doctrine ORM
**Frameworks**: LexikJWTAuthenticationBundle
**Patterns**: Repository, Service, Controller

### Fichiers Identifiés
- src/Security/JwtAuthenticator.php (Create)
- src/Controller/AuthController.php (Create)
- src/Service/TokenService.php (Create)
- config/packages/security.yaml (Modify)

### Critères d'Acceptation
1. Users can login with email/password
2. JWT token returned on successful login
3. Token expires after 1 hour
4. Refresh token mechanism implemented

### Risques Identifiés
- Token storage security
- Refresh token rotation
- CORS configuration

### Memory Summary
Project uses Symfony best practices, test coverage requirement: >80%

---

## §2 — Implementation Plan

### Impacted Files
| File | Action | Risk |
|------|--------|------|
| src/Security/JwtAuthenticator.php | Create | Medium |
| src/Controller/AuthController.php | Create | Low |
| src/Service/TokenService.php | Create | Low |
| config/packages/security.yaml | Modify | High |
| tests/Unit/Security/JwtAuthenticatorTest.php | Create | Low |

### Tasks
1. [ ] **Install LexikJWTAuthenticationBundle** (3 min)
   - File: `composer.json`
   - Test: Bundle registered check

2. [ ] **Create JwtAuthenticator** (12 min)
   - File: `src/Security/JwtAuthenticator.php`
   - Test: `tests/Unit/Security/JwtAuthenticatorTest.php`
   - Dependencies: Task 1

3. [ ] **Create TokenService** (8 min)
   - File: `src/Service/TokenService.php`
   - Test: `tests/Unit/Service/TokenServiceTest.php`
   - Dependencies: Task 1

4. [ ] **Create AuthController** (10 min)
   - File: `src/Controller/AuthController.php`
   - Test: `tests/Functional/Controller/AuthControllerTest.php`
   - Dependencies: Task 2, Task 3

5. [ ] **Configure security.yaml** (7 min)
   - File: `config/packages/security.yaml`
   - Test: Integration test validates config
   - Dependencies: Task 2

### Risks
| Risk | Probability | Mitigation |
|------|-------------|------------|
| Token storage vulnerability | Medium | Use httpOnly cookies + CSRF protection |
| Misconfigured CORS | Low | Test with frontend integration |
| Weak secret key | Low | Use 256-bit random key from env |

### Validation
- **@plan-validator**: APPROVED
- **Task granularity**: ✅ All tasks 2-15 min
- **Security considerations**: ✅ Covered

---

## §3 — Implementation & Finalization

### Code Review (Phase 2)

**@code-reviewer verdict:** APPROVED

**@security-auditor verdict:** APPROVED
- OWASP Top 10: ✅ No vulnerabilities
- JWT best practices: ✅ Compliant
- Secret management: ✅ Environment variables

**Test coverage:** 87%

### Documentation (Phase 3)

- API documentation: ✅ /docs/api/authentication.md updated
- Setup instructions: ✅ README.md updated
- Security notes: ✅ SECURITY.md created

### Git Status

**Commit:** f7a9c2e1b8d4
**Branch:** feature/user-authentication
**Status:** ✅ Ready for merge

### Finalization Checklist

- [x] All 5 tasks completed
- [x] Tests passing (87% coverage)
- [x] Code review approved
- [x] Security audit passed
- [x] Documentation complete
- [x] Changes committed
```

---

## Usage Guidelines

### When to Use Each Template

| Situation | Template to Use |
|-----------|----------------|
| After `/brief` → `/epci` | Scenario B (Standard) |
| After `--from-native-plan` | Scenario A (Native Plan) |
| During Phase 2 review | §3 Implementation section |
| Phase 3 finalization | §3 Finalization Checklist |

### Key Principles

1. **Atomic tasks**: Each task 2-15 minutes
2. **Clear dependencies**: Explicit task ordering
3. **Test coverage**: One test per task minimum
4. **Risk documentation**: Identify and mitigate
5. **Validation tracking**: Record all agent verdicts

---

## Related Documentation

- **Main command**: `/epci`
- **Native plan import**: @references/epci/native-plan-import.md
- **@plan-validator**: subagent `plan-validator`
- **Project memory**: skill `project-memory`
