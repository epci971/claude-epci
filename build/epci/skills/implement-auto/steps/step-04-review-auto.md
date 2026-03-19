---
name: step-04-review-auto
description: Self-review + @code-reviewer + @security-auditor + @qa-reviewer [I]
prev_step: steps/step-03-code-auto.md
next_step: steps/step-05-document-auto.md
---

# Step 04: Review (Auto) [I]

## Reference Files

@../references/review-checklist.md
@../references/domain-mapping.md

## MANDATORY EXECUTION RULES:

- NEVER call AskUserQuestion
- ALWAYS execute self-review checklist first (pre-filter)
- ALWAYS invoke @code-reviewer unless --skip-review
- ALWAYS check for security patterns and invoke @security-auditor when detected (unless --skip-security)
- ALWAYS check QA thresholds and invoke @qa-reviewer when met (unless --skip-qa)
- ALWAYS record all findings in JSON output
- ALWAYS continue even if critical findings (headless mode — findings are for orchestrator)

## EXECUTION PROTOCOLS:

### 1. Self-Review Checklist (Always — Pre-Filter)

Execute each check from review-checklist.md "Self-Review Checklist" section on all modified/created files.

#### Tests Quality Checks

| Check | Command |
|-------|---------|
| T1: All tests pass | Run full test suite, verify exit code 0 |
| T2: Tests exist per component | Count test files vs plan components |
| T5: No skipped tests | Grep for skip/xit/xdescribe/pytest.mark.skip |

#### Code Quality Checks

| Check | Command |
|-------|---------|
| C1: No debug prints | Grep for `print(` / `console.log` in created/modified files |
| C2: No hardcoded secrets | Grep for `password\|secret\|api_key\|token` patterns |
| C3: No commented-out code | Grep for large comment blocks (3+ consecutive comment lines) |
| C4: No TODO/FIXME | Grep for `TODO\|FIXME\|HACK\|XXX` in created files |

#### Security Basics Checks

| Check | Command |
|-------|---------|
| S1: No SQL injection | Grep for string concatenation in SQL (f-string + SELECT/INSERT) |
| S2: No command injection | Grep for `os.system\|subprocess.call.*shell=True\|exec(` |

#### Self-Review Results

Build self_review object:

```json
{
  "status": "pass | warn | fail",
  "items_checked": 10,
  "items_passed": 8,
  "items_warned": 2,
  "findings": [
    {
      "check_id": "C1",
      "severity": "error",
      "message": "Debug print found",
      "file": "path/to/file.py",
      "line": 42
    }
  ]
}
```

Status determination:
- `pass`: 0 findings
- `warn`: findings exist but none critical
- `fail`: critical findings exist (still continues in headless mode)

### 2. Invoke @code-reviewer (Default — Deep Analysis)

IF `flag_skip_review` is false (default):

**First check for background reviewer from step-03:**
```
IF background_reviewer_task_id is set:
  Check task status (TaskOutput)
  IF completed:
    Use background reviewer results directly
    SKIP synchronous invocation
  IF still running:
    Wait for completion (with 60s timeout)
    IF completed: use results
    IF timeout: proceed to synchronous invocation
  IF failed:
    Log warning, proceed to synchronous invocation
```

**If no background results available, invoke synchronously:**

```
LANCE Task({
  subagent_type: "code-reviewer",
  model: "opus",
  prompt: "
    ## Code Review Request
    Feature: {feature_slug}
    Requirements: {spec_requirements}

    ## Files to Review
    {list of all modified/created files with content}

    ## Context
    - Patterns from exploration: {patterns}
    - Stack skills loaded: {stack_cache.keys()}
    - Plan: {plan_summary}
    - Self-review findings: {self_review_findings}

    ## Review Focus (from review-checklist.md Code Review Checklist)
    - Functionality: requirements, edge cases, error handling, no bugs
    - Code Quality: patterns, DRY, KISS, naming, comments, no dead code
    - Testing: unit tests, coverage (target {70% or 80%}), happy/error/edge paths
    - Performance: no N+1, efficient loops, data structures, caching
    - Security: input validation, no secrets, no injection, auth correct

    ## Expected Output
    Verdict: APPROVED | CHANGES_REQUIRED | SECURITY_REVIEW_NEEDED
    Findings: [{severity, file, line, message, suggestion}]
    Overall assessment: string
  "
})
```

**Process code-reviewer results:**
- Record verdict in `checks.deep_review.verdict`
- Record findings count and critical count
- If SECURITY_REVIEW_NEEDED: force security review even without pattern detection

IF `flag_skip_review` is true:
- Set `checks.deep_review.status = "skip"`
- Set `checks.deep_review.skipped_reason = "--skip-review flag"`

### 3. Invoke @security-auditor (Conditional — OWASP Top 10)

**Determine if security review is needed:**

```
security_review_needed = false

## Check 1: File path patterns
FOR each modified_file:
  IF path matches **/auth/** OR **/security/** OR **/middleware/**:
    security_review_needed = true

## Check 2: Content keywords
FOR each modified_file:
  IF content contains password|jwt|oauth|encrypt|decrypt|token|session|cookie|csrf|cors|authenticate|authorize:
    security_review_needed = true

## Check 3: Complexity
IF complexity == "LARGE":
  security_review_needed = true

## Check 4: Code reviewer verdict
IF checks.deep_review.verdict == "SECURITY_REVIEW_NEEDED":
  security_review_needed = true
```

IF `security_review_needed` AND `flag_skip_security` is false:

```
LANCE Task({
  subagent_type: "security-auditor",
  model: "opus",
  prompt: "
    ## Security Audit Request
    Feature: {feature_slug}

    ## Files to Audit
    {list of modified/created files with security-relevant content}

    ## Audit Scope (OWASP Top 10)
    A01: Broken Access Control — authorization, CORS, directory traversal, rate limiting, sessions
    A02: Cryptographic Failures — encryption, HTTPS/TLS, algorithms, key management, logs
    A03: Injection — parameterized queries, sanitization, command/LDAP/NoSQL injection
    A04: Insecure Design — threat modeling, secure defaults, fail securely, least privilege
    A05: Security Misconfiguration — credentials, features, error messages, headers, dependencies
    A06: Vulnerable Components — CVE review, trusted sources, updates
    A07: Authentication Failures — password policy, MFA, timeout, lockout, secure storage
    A08: Data Integrity — code signing, integrity checks, CI/CD, auto-updates
    A09: Logging & Monitoring — events logged, no sensitive data, log injection, alerting
    A10: SSRF — URL validation, whitelist, internal network, metadata endpoints

    ## Expected Output
    Verdict: PASS | FAIL_CRITICAL | FAIL_HIGH
    Vulnerabilities: [{owasp_category, severity, location, description, remediation}]
  "
})
```

**Process security-auditor results:**
- Record verdict in `checks.security_review`
- If FAIL_CRITICAL or FAIL_HIGH: add to JSON `errors[]` with severity "critical" or "error"
- Continue execution (headless mode — findings are for orchestrator)

IF NOT `security_review_needed`:
- Set `checks.security_review.status = "skip"`
- Set `checks.security_review.skipped_reason = "no_security_patterns"`

IF `flag_skip_security` is true:
- Set `checks.security_review.status = "skip"`
- Set `checks.security_review.skipped_reason = "--skip-security flag"`

### 4. Invoke @qa-reviewer (Conditional — AC Verification)

**Determine if QA review is needed:**

```
qa_review_needed = (
  acceptance_criteria_count > 3
  OR plan.total_components > 5
  OR complexity == "LARGE"
)
```

IF `qa_review_needed` AND `flag_skip_qa` is false:

```
LANCE Task({
  subagent_type: "qa-reviewer",
  model: "sonnet",
  prompt: "
    ## QA Review Request
    Feature: {feature_slug}
    Requirements: {spec_requirements}
    Acceptance Criteria: {acceptance_criteria_list}

    ## Implementation
    {list of modified/created files}

    ## Test Files
    {list of test files}

    ## QA Focus (from review-checklist.md QA Validation Checklist)
    - Acceptance Criteria: all verified, mapped to tests, edge cases covered
    - Functional Testing: happy path, input types, output matches spec, state changes
    - Error Handling: invalid input, user-friendly messages, recovery paths
    - Edge Cases: empty, null, boundaries, large inputs, special chars, unicode

    ## Expected Output
    Verdict: PASS | FAIL
    AC status: [{criterion, status: pass|fail, test_mapping}]
    Defects: [{severity, description, steps_to_reproduce}]
  "
})
```

**Process qa-reviewer results:**
- Record verdict, AC counts, defects in `checks.qa_review`
- If FAIL: add to JSON `errors[]` with severity "error"

IF NOT `qa_review_needed`:
- Set `checks.qa_review.status = "skip"`
- Set `checks.qa_review.skipped_reason = "below_threshold"`

IF `flag_skip_qa` is true:
- Set `checks.qa_review.status = "skip"`
- Set `checks.qa_review.skipped_reason = "--skip-qa flag"`

### 5. Update Feature Document §4

Use Edit tool to update the Revue & Validation section:

```markdown
## §4 — Revue & Validation

### Self-Review
| Metrique | Valeur |
|----------|--------|
| Status | {self_review.status} |
| Checks | {items_passed}/{items_checked} |
| Findings | {items_warned} |

### @code-reviewer
| Metrique | Valeur |
|----------|--------|
| Verdict | {APPROVED / CHANGES_REQUIRED / skipped} |
| Findings | {findings_count} |
| Critical | {critical_count} |

### @security-auditor
| Metrique | Valeur |
|----------|--------|
| Verdict | {PASS / FAIL_CRITICAL / FAIL_HIGH / skipped} |
| Vulnerabilities | {count} |
| OWASP categories | {list} |

### @qa-reviewer
| Metrique | Valeur |
|----------|--------|
| Verdict | {PASS / FAIL / skipped} |
| AC verified | {passed}/{total} |
| Defects | {count} |
```

### 6. Update JSON Output

Update `.implement-auto-output.json`:
- `phases.completed` += "review"
- `phases.current` = "document"
- `checks.self_review` = self-review results
- `checks.deep_review` = code-reviewer results
- `checks.security_review` = security-auditor results
- `checks.qa_review` = qa-reviewer results

## CONTEXT BOUNDARIES:

- This step expects: Implemented components from step-03, list of modified files, background_reviewer_task_id (if any), complexity level
- This step produces: Complete review findings (self + deep + security + QA), updated Feature Doc §4, updated JSON

## NEXT STEP TRIGGER:

Always proceed to step-05-document-auto.md (reviews never block in headless mode — all findings recorded for orchestrator).
