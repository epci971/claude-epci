# Review Checklists

Reference checklists for code review in EPCI implementation workflow.

---

## Code Review Checklist

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
- [ ] Coverage target met (>= 70%)
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

---

## QA Validation Checklist

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

| Level | Description | Action |
|-------|-------------|--------|
| 🔴 CRITICAL | Security vulnerability, data loss risk | Must fix before merge |
| 🟠 HIGH | Bug, significant issue | Must fix before merge |
| 🟡 MEDIUM | Code quality issue | Should fix |
| 🔵 LOW | Style, minor improvement | Optional |
| ⚪ INFO | Suggestion, FYI | No action required |

---

## Review Response Template

```markdown
## Code Review: {feature-slug}

### Summary
- Files reviewed: {N}
- Total comments: {N}
- Blocking issues: {N}

### Verdict
{APPROVED | CHANGES_REQUIRED | NEEDS_DISCUSSION}

### Blocking Issues
| # | Severity | Location | Issue |
|---|----------|----------|-------|
| 1 | {sev} | {file:line} | {description} |

### Suggestions (Non-blocking)
| # | Location | Suggestion |
|---|----------|------------|
| 1 | {file:line} | {suggestion} |

### Positive Notes
- {something done well}
```
