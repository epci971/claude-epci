# Review Checklists

> Quality checklists for implement-auto review phase.
> Self-review runs as automated pre-filter, then @code-reviewer / @security-auditor / @qa-reviewer for deep analysis.

---

## Self-Review Checklist (Automated)

> Automated grep-based checks. Always runs as first pass.

### 1. Tests Quality

| # | Check | Severity | How to Verify |
|---|-------|----------|---------------|
| T1 | All tests pass | critical | Run test suite, exit code 0 |
| T2 | Tests exist for each component | error | Count test files vs components |
| T3 | Tests cover happy path | warning | Grep for assertion patterns |
| T4 | Tests cover error cases | warning | Grep for error/exception tests |
| T5 | No skipped/disabled tests | warning | Grep for skip/xit/xdescribe |

### 2. Code Quality

| # | Check | Severity | How to Verify |
|---|-------|----------|---------------|
| C1 | No debug prints/console.log | error | Grep for print/console.log |
| C2 | No hardcoded secrets | critical | Grep for password/secret/api_key patterns |
| C3 | No commented-out code blocks | warning | Grep for large comment blocks |
| C4 | No TODO/FIXME/HACK markers | warning | Grep for TODO/FIXME/HACK |
| C5 | Files follow project naming conventions | warning | Check against CLAUDE.md patterns |

### 3. Architecture

| # | Check | Severity | How to Verify |
|---|-------|----------|---------------|
| A1 | Follows existing patterns from explore | warning | Compare with identified patterns |
| A2 | No circular dependencies introduced | error | Check import graph |
| A3 | No duplicate functionality | warning | Grep for similar function signatures |

### 4. Security Basics

| # | Check | Severity | How to Verify |
|---|-------|----------|---------------|
| S1 | No SQL injection patterns | critical | Grep for string concatenation in queries |
| S2 | No command injection patterns | critical | Grep for os.system/exec/eval |
| S3 | Input validation present | warning | Check public API entry points |
| S4 | No sensitive data in logs | error | Grep for logging of credentials/tokens |

### Self-Review Execution Protocol

```
FOR each check in checklist:
  result = execute_verification(check)
  IF result.passed:
    items_passed += 1
  ELSE:
    items_warned += 1
    findings.append({
      check_id: check.id,
      severity: check.severity,
      message: result.message,
      file: result.file,
      line: result.line
    })

self_review = {
  status: items_warned == 0 ? "pass" : (has_critical ? "fail" : "warn"),
  items_checked: total_checks,
  items_passed: items_passed,
  items_warned: items_warned,
  findings: findings
}
```

### Severity Impact on Status

| Severity | Impact on Task Status |
|----------|----------------------|
| critical | Logged but does NOT block (headless mode) |
| error | Logged as warning |
| warning | Informational only |

In headless mode, self-review findings are recorded but never block execution.
The orchestrator/reviewer decides action based on the JSON output.

---

## Code Review Checklist (@code-reviewer)

> Used by @code-reviewer (Opus) for deep analysis. Runs by default (skip with `--skip-review`).

### Functionality
- [ ] Code implements requirements correctly
- [ ] Edge cases handled
- [ ] Error handling appropriate
- [ ] No obvious bugs or logic errors

### Code Quality
- [ ] Follows existing patterns in codebase
- [ ] DRY: No unnecessary duplication
- [ ] KISS: Simple, not over-engineered
- [ ] Clear naming (variables, functions, classes)
- [ ] Appropriate comments (why, not what)
- [ ] No dead code or unused imports

### Testing
- [ ] Unit tests for new code
- [ ] Tests cover happy paths
- [ ] Tests cover error paths
- [ ] Tests cover edge cases
- [ ] Coverage target met (>= 70% STANDARD, >= 80% LARGE)
- [ ] Tests are readable and maintainable

### Performance
- [ ] No N+1 query issues
- [ ] No unnecessary loops or iterations
- [ ] Appropriate data structures used
- [ ] No blocking operations in hot paths
- [ ] Caching where appropriate

### Security (Basic)
- [ ] Input validation present
- [ ] No hardcoded secrets
- [ ] No SQL injection risks
- [ ] No XSS vulnerabilities
- [ ] Authentication/authorization correct

---

## Security Review Checklist (OWASP Top 10)

> Used by @security-auditor (Opus). Triggered when auth/security patterns detected or complexity is LARGE. Skip with `--skip-security`.

### A01: Broken Access Control
- [ ] Authorization checks on all protected resources
- [ ] CORS properly configured
- [ ] Directory traversal prevented
- [ ] Rate limiting in place
- [ ] Session management secure

### A02: Cryptographic Failures
- [ ] Sensitive data encrypted at rest
- [ ] HTTPS/TLS for data in transit
- [ ] Strong algorithms used (no MD5, SHA1 for security)
- [ ] Keys managed securely
- [ ] No sensitive data in logs

### A03: Injection
- [ ] Parameterized queries (no string concatenation)
- [ ] Input sanitization
- [ ] Command injection prevented
- [ ] LDAP injection prevented
- [ ] NoSQL injection prevented

### A04: Insecure Design
- [ ] Threat modeling considered
- [ ] Secure defaults
- [ ] Fail securely
- [ ] Principle of least privilege
- [ ] Defense in depth

### A05: Security Misconfiguration
- [ ] Default credentials changed
- [ ] Unnecessary features disabled
- [ ] Error messages don't reveal internals
- [ ] Security headers configured
- [ ] Dependencies up to date

### A06: Vulnerable and Outdated Components
- [ ] Dependencies reviewed for vulnerabilities
- [ ] No known CVEs in dependencies
- [ ] Dependencies from trusted sources
- [ ] Automatic security updates enabled

### A07: Authentication Failures
- [ ] Strong password policy
- [ ] Multi-factor where appropriate
- [ ] Session timeout implemented
- [ ] Account lockout for brute force
- [ ] Secure password storage (bcrypt, argon2)

### A08: Data Integrity Failures
- [ ] Code signing where applicable
- [ ] Integrity checks on downloads
- [ ] Secure CI/CD pipeline
- [ ] Auto-updates verified

### A09: Security Logging and Monitoring
- [ ] Security events logged
- [ ] No sensitive data in logs
- [ ] Log injection prevented
- [ ] Alerting configured

### A10: SSRF
- [ ] URL validation on user input
- [ ] Whitelist for external requests
- [ ] Internal networks not accessible
- [ ] Metadata endpoints blocked

### Security Pattern Detection

Trigger @security-auditor when ANY of these patterns are detected in modified files:

```
Path patterns: **/auth/**, **/security/**, **/middleware/**
Keywords: password, jwt, oauth, encrypt, decrypt, token, session, cookie, csrf, cors, authenticate, authorize
File names: auth.*, security.*, middleware.*, permissions.*
```

OR when `complexity == LARGE` (mandatory).

---

## QA Validation Checklist (@qa-reviewer)

> Used by @qa-reviewer (Sonnet). Triggered when >3 AC or >5 components or LARGE complexity. Skip with `--skip-qa`.

### Acceptance Criteria
- [ ] All acceptance criteria verified
- [ ] Criteria mapped to test cases
- [ ] Edge cases from AC covered

### Functional Testing
- [ ] Happy path works correctly
- [ ] All input types handled
- [ ] Output matches specification
- [ ] State changes correct

### Error Handling
- [ ] Invalid input rejected gracefully
- [ ] Error messages user-friendly
- [ ] Error messages don't expose internals
- [ ] Recovery paths work

### Edge Cases
- [ ] Empty inputs handled
- [ ] Null/undefined handled
- [ ] Boundary values tested
- [ ] Large inputs handled
- [ ] Special characters handled
- [ ] Unicode handled

### Usability
- [ ] UI responsive (if applicable)
- [ ] Clear feedback for actions
- [ ] Loading states present
- [ ] Error states clear

### QA Activation Thresholds

```
qa_review_active = (
  acceptance_criteria_count > 3
  OR plan_components_count > 5
  OR complexity == "LARGE"
) AND flag_skip_qa != true
```

---

## Documentation Review Checklist

### Completeness
- [ ] Feature Document updated
- [ ] API documentation current
- [ ] README reflects changes
- [ ] CHANGELOG entry added

### Quality
- [ ] Clear and concise
- [ ] Examples provided
- [ ] No outdated information
- [ ] Technical accuracy verified

### Breaking Changes
- [ ] Migration guide if needed
- [ ] Deprecation notices
- [ ] Version compatibility noted

---

## Review Severity Levels

| Level | Description | Action (headless) |
|-------|-------------|-------------------|
| CRITICAL | Security vulnerability, data loss risk | Logged in errors[], severity: critical |
| HIGH | Bug, significant issue | Logged in errors[], severity: error |
| MEDIUM | Code quality issue | Logged in warnings[] |
| LOW | Style, minor improvement | Logged in warnings[] |
| INFO | Suggestion, FYI | Logged in warnings[] |
