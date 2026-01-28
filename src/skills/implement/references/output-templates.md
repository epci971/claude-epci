# Output Templates

> Standard output format templates for implement skill phases.

---

## Plan Output {#plan-output}

```markdown
## Implementation Plan

### Phase 1: Foundation
1. {Component} - {description}
   - Test: {test approach}
   - Files: {files to modify/create}

### Phase 2: Core Logic
2. {Component} - {description}
   - Test: {test approach}
   - Files: {files}

### Phase 3: Integration
3. {Component} - {description}
   - Test: {test approach}
   - Files: {files}

### Test Strategy
- Unit tests: {approach}
- Integration tests: {approach}
- Coverage target: {%}

### Acceptance Criteria Mapping
| Criteria | Component | Test |
|----------|-----------|------|
| {AC1} | {component} | {test} |
```

---

## Review Output {#review-output}

```markdown
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

---

## Security Output {#security-output}

```markdown
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

---

## QA Output {#qa-output}

```markdown
## QA Validation Report

### Acceptance Criteria
| # | Criterion | Status | Notes |
|---|-----------|--------|-------|
| 1 | {AC1} | {PASS|FAIL} | {notes} |
| 2 | {AC2} | {PASS|FAIL} | {notes} |

### Test Results
- Happy paths: {N}/{N} passed
- Edge cases: {N}/{N} passed
- Error handling: {N}/{N} passed

### Defects Found
| # | Severity | Description | Steps to Reproduce |
|---|----------|-------------|-------------------|
| 1 | {sev} | {desc} | {steps} |

### Verdict
{PASS | FAIL}
```

---

## Documentation Output {#documentation-output}

```markdown
## Documentation Complete

### Feature Document
- Location: `.epci/features/{feature-slug}/FEATURE.md`
- Status: COMPLETED

### Updated Docs
- {doc 1}: {changes}
- {doc 2}: {changes}

### Breaking Changes
{none | list of changes with migration steps}
```

---

## Finish Output {#finish-output}

```markdown
## Implementation Complete

### Feature: {feature-slug}
- Status: COMPLETED
- Complexity: {STANDARD|LARGE}
- Duration: {time}

### Deliverables
- Implementation code
- Unit tests ({coverage}%)
- Integration tests
- Feature Document
- Documentation updates

### Files Summary
| Action | Count | Files |
|--------|-------|-------|
| Created | {N} | {list} |
| Modified | {N} | {list} |

### Test Summary
- Total tests: {N}
- All passing: yes
- Coverage: {%}

### Key Decisions
- {decision 1}
- {decision 2}

### Known Limitations
- {limitation 1 if any}

### Next Steps
1. Review changes: `git diff`
2. Stage files: `git add {files}`
3. Commit: `git commit -m "feat({scope}): {description}"`
4. Create PR (if applicable)
```
