---
name: step-05-review
description: Conditional code, security, and QA reviews based on scope and patterns
prev_step: steps/step-04-execute.md
next_step: steps/step-06-verify.md
conditional_next:
  - condition: "Scope is single"
    step: steps/step-06-verify.md
  - condition: "--turbo flag"
    step: steps/step-06-verify.md
  - condition: "Critical issues found"
    step: steps/step-05-review.md
---

# Step 05: Review

> Conditional code, security, and QA reviews based on scope and patterns.

## Trigger

- Previous step: `step-04-execute.md` completed
- Condition: Scope is `module`, `cross-module`, or `architecture`

## Skip Conditions

| Condition | Action |
|-----------|--------|
| Scope is `single` | → Skip to `step-06-verify.md` |
| `--turbo` flag | → Skip to `step-06-verify.md` |
| No files modified | → Skip to `step-06-verify.md` |

## Inputs

| Input | Source |
|-------|--------|
| Modified files list | From step-04 |
| Scope | From step-00 |
| Stack context | From step-00 |

## Protocol

### 1. Determine Reviews Needed

Apply subagent invocation matrix:

```python
reviews_needed = []

# Code Review
if scope in ['module', 'cross-module', 'architecture']:
    if len(modified_files) > 5 or scope != 'module':
        reviews_needed.append('code-reviewer')

# Security Audit
security_patterns = ['**/auth/**', '**/security/**', '**/login/**', '**/token/**']
if any(file matches security_patterns for file in modified_files):
    reviews_needed.append('security-auditor')
elif scope == 'architecture':
    reviews_needed.append('security-auditor')  # Always for architecture

# QA Review
test_files_modified = [f for f in modified_files if 'test' in f]
if len(test_files_modified) >= 5 or scope in ['cross-module', 'architecture']:
    reviews_needed.append('qa-reviewer')
```

### 2. Launch Reviews (Parallel if Multiple)

#### @code-reviewer

```
Task: Review refactoring changes for quality
Focus:
  - Behavior preservation (no functional changes)
  - Code quality improvement
  - Naming consistency
  - Pattern application correctness

Context:
  - This is a REFACTORING, not a feature change
  - External APIs must remain unchanged
  - Internal structure improvement is the goal

Files: <modified_files>
Scope: <scope>
```

#### @security-auditor

```
Task: Security review of refactored code
Focus:
  - No security regression
  - Auth/session handling unchanged
  - No new vulnerabilities introduced
  - Secrets handling preserved

Context:
  - This is a REFACTORING, behavior should be identical
  - Security properties must be preserved

Files: <security_relevant_files>
```

#### @qa-reviewer

```
Task: QA review of refactored tests
Focus:
  - Test coverage maintained
  - Test quality not degraded
  - New tests for extracted components appropriate
  - No test duplication

Context:
  - Refactoring should not reduce coverage
  - New tests for new files are expected

Files: <test_files_modified>
```

### 3. Collect Review Results

```json
{
  "reviews": {
    "code-reviewer": {
      "status": "passed|issues|critical",
      "findings": [
        {
          "severity": "minor",
          "file": "auth.py",
          "line": 45,
          "message": "Consider more descriptive name for _validate()"
        }
      ]
    },
    "security-auditor": {
      "status": "passed",
      "findings": []
    },
    "qa-reviewer": {
      "status": "issues",
      "findings": [
        {
          "severity": "important",
          "file": "test_token_validator.py",
          "message": "Missing edge case test for expired tokens"
        }
      ]
    }
  }
}
```

### 4. Handle Review Findings

| Severity | Action |
|----------|--------|
| Critical | STOP, require fix before proceeding |
| Important | Flag for user decision |
| Minor | Log, continue |

If critical issues found:

```
## Review Found Critical Issues

**@code-reviewer** found 1 critical issue:

1. [CRITICAL] Behavior change detected in authenticate()
   - Before: Returns None on invalid credentials
   - After: Raises AuthError

   This changes the external API behavior, which violates
   refactoring principles.

**Options**:
[A] Fix issue and re-run reviews
[B] Acknowledge as intentional (not pure refactoring)
[C] Revert transformation T2
```

### 5. Display Review Summary

```
## Review Results

| Reviewer | Status | Findings |
|----------|--------|----------|
| @code-reviewer | PASSED | 2 minor suggestions |
| @security-auditor | PASSED | No issues |
| @qa-reviewer | ISSUES | 1 important finding |

### Important Findings (require attention)

1. **Missing test coverage** (@qa-reviewer)
   - File: test_token_validator.py
   - Add test for expired token edge case

### Minor Suggestions (optional)

1. Consider renaming _validate() to _validate_user_credentials()
2. Add docstring to TokenValidator class
```

## Outputs

| Output | Destination |
|--------|-------------|
| Review results | State |
| Findings list | User display |
| Action items (if any) | User decision |

## Next Step

| Review Status | Next Step |
|---------------|-----------|
| All passed | → `step-06-verify.md` |
| Critical issues | → Fix, then re-review |
| Important issues | → User decision, then continue |

## Error Handling

| Error | Resolution |
|-------|------------|
| Subagent timeout | Retry once, then proceed with warning |
| Subagent unavailable | Skip that review, log warning |
| Conflicting findings | Present both, user decides |
