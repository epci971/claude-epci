# Output Patterns - Standardized Subagent Reports

> Templates and conventions for consistent, actionable subagent outputs

---

## Core Principles

| Principle | Description |
|-----------|-------------|
| **Structured** | Predictable format for automation |
| **Actionable** | Clear next steps, not just findings |
| **Evidence-Based** | File locations, line numbers, code snippets |
| **Verdict-Driven** | Clear conclusion with reasoning |

---

## Standard Output Structure

```markdown
## [Report Title]

### Summary
[1-2 sentences: overall assessment]

### Findings
[Detailed analysis organized by category]

### Issues (if any)
[Structured list with severity, location, fix]

### Verdict
**[VERDICT]**
**Reasoning:** [Technical justification]
```

---

## Verdict Types

### Binary Verdicts

| Verdict | Meaning | When to Use |
|---------|---------|-------------|
| `APPROVED` | Passes all checks | Validation agents |
| `REJECTED` | Critical failures | Quality gates |

### Graduated Verdicts

| Verdict | Meaning | When to Use |
|---------|---------|-------------|
| `APPROVED` | No issues found | All checks pass |
| `APPROVED_WITH_NOTES` | Minor suggestions | Non-blocking issues |
| `NEEDS_REVISION` | Issues to address | Fixable problems |
| `REJECTED` | Fundamental problems | Blocking issues |

### Research Verdicts

| Verdict | Meaning | When to Use |
|---------|---------|-------------|
| `GO` | Proceed with approach | Spike, exploration |
| `NO_GO` | Abandon approach | Spike, exploration |
| `MORE_RESEARCH` | Need more information | Inconclusive spike |

---

## Severity Levels

### Standard Severity Scale

| Level | Symbol | Criteria | Action |
|-------|--------|----------|--------|
| **Critical** | 🔴 | Security risk, data loss, breaking | Must fix before merge |
| **High** | 🟠 | Bugs, performance issues | Should fix before merge |
| **Medium** | 🟡 | Code quality, maintainability | Fix in follow-up |
| **Low** | 🟢 | Style, minor improvements | Optional fix |

### Severity Decision Tree

```
Is it a security vulnerability?
├── Yes → 🔴 Critical
└── No → Could it cause data loss or breaking change?
         ├── Yes → 🔴 Critical
         └── No → Is it a bug affecting functionality?
                  ├── Yes → 🟠 High
                  └── No → Does it impact performance significantly?
                           ├── Yes → 🟠 High
                           └── No → Is it a code quality issue?
                                    ├── Yes → 🟡 Medium
                                    └── No → 🟢 Low
```

---

## Issue Documentation Format

### Standard Issue Template

```markdown
#### 🔴 Critical: [Issue Title]
- **Location**: `src/file.ts:45`
- **Issue**: [Clear description of the problem]
- **Evidence**: [Code snippet or proof]
- **Fix**: [Suggested solution]
- **References**: [Link to best practice or documentation]
```

### Minimal Issue Format

```markdown
- 🔴 **[Title]** — `file.ts:45` — [Description] → [Fix]
```

### Issue Table Format

```markdown
| Severity | File | Line | Issue | Fix |
|----------|------|------|-------|-----|
| 🔴 Critical | auth.ts | 45 | SQL injection | Use parameterized query |
| 🟠 High | api.ts | 112 | No error handling | Add try-catch |
```

---

## Report Templates by Agent Type

### Code Review Report

```markdown
## Code Review Report

### Summary
Reviewed X files with Y changes. Found Z issues (A critical, B high).

### Quality Assessment

| Aspect | Score | Notes |
|--------|-------|-------|
| Correctness | ⭐⭐⭐⭐ | Logic is sound |
| Readability | ⭐⭐⭐ | Some complex functions |
| Testing | ⭐⭐ | Missing edge cases |

### Issues

#### 🔴 Critical
[None found / List issues]

#### 🟠 High
1. **Missing null check**
   - **Location**: `src/utils/parser.ts:67`
   - **Issue**: Input not validated before use
   - **Fix**: Add `if (!input) return null;`

#### 🟡 Medium
[Issues list]

### Positive Patterns
- Good use of TypeScript types
- Consistent error handling pattern

### Verdict
**APPROVED_WITH_NOTES**

**Reasoning:** No critical issues. 2 high-priority items should be addressed before merge.
```

### Security Audit Report

```markdown
## Security Audit Report

### Summary
Security review of authentication module. Found 1 critical vulnerability.

### Vulnerability Assessment

| OWASP Category | Status | Findings |
|----------------|--------|----------|
| A01: Broken Access Control | ⚠️ | 1 issue |
| A02: Cryptographic Failures | ✅ | None |
| A03: Injection | ✅ | None |
| A07: Auth Failures | ⚠️ | 1 issue |

### Issues

#### 🔴 Critical
1. **Hardcoded API Key**
   - **Location**: `src/config/auth.ts:12`
   - **Issue**: API key exposed in source code
   - **Evidence**: `const API_KEY = "sk-prod-xxx"`
   - **Fix**: Move to environment variable
   - **OWASP**: A02 - Cryptographic Failures

### Verdict
**REJECTED**

**Reasoning:** Critical security vulnerability must be fixed before deployment.
```

### Plan Validation Report

```markdown
## Plan Validation Report

### Summary
Reviewed implementation plan for feature X. Plan is well-structured.

### Validation Checklist

| Criterion | Status |
|-----------|--------|
| Tasks are atomic (2-15 min) | ✅ |
| Dependencies are ordered | ✅ |
| Tests planned for each task | ⚠️ Partial |
| Risks identified | ✅ |
| Rollback strategy | ❌ Missing |

### Issues

#### 🟠 High
1. **Missing test plan for Task 3**
   - **Task**: "Implement caching layer"
   - **Issue**: No tests specified
   - **Fix**: Add unit tests for cache invalidation

#### 🟡 Medium
1. **No rollback strategy**
   - **Issue**: Plan doesn't address failure recovery
   - **Fix**: Add rollback steps for database migration

### Verdict
**NEEDS_REVISION**

**Reasoning:** Add missing test plan and rollback strategy before proceeding.
```

### Documentation Generation Report

```markdown
## Documentation Generated

### Summary
Generated documentation for 5 modules.

### Files Created

| File | Type | Lines |
|------|------|-------|
| `docs/api/auth.md` | API Reference | 145 |
| `docs/api/users.md` | API Reference | 98 |
| `README.md` | Updated | +23 |

### Coverage

| Module | Documented | Notes |
|--------|------------|-------|
| auth | ✅ | Complete |
| users | ✅ | Complete |
| admin | ⚠️ | Private methods skipped |

### Verdict
**APPROVED**

**Reasoning:** All public APIs documented. README updated with quick start guide.
```

---

## Formatting Guidelines

### Code Snippets

```markdown
**Before:**
```typescript
function process(input) {
  return input.value;  // No null check
}
```

**After:**
```typescript
function process(input: Input | null): Value | null {
  if (!input) return null;
  return input.value;
}
```
```

### Location References

| Format | Use When |
|--------|----------|
| `file.ts:45` | Single line |
| `file.ts:45-52` | Line range |
| `file.ts:fn:processData` | Function reference |
| `src/module/file.ts:45` | Full path when ambiguous |

---

## Quick Reference

```
+------------------------------------------+
|          SUBAGENT OUTPUT PATTERN          |
+------------------------------------------+
| ## [Report Title]                         |
| ### Summary         <- 1-2 sentences      |
| ### Findings        <- Organized details  |
| ### Issues          <- Severity + Fix     |
| ### Verdict         <- APPROVED/REJECTED  |
+------------------------------------------+
| SEVERITY: 🔴 Critical > 🟠 High > 🟡 Med  |
| FORMAT: Location + Issue + Evidence + Fix |
+------------------------------------------+
```
