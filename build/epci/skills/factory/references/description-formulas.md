# Description Formulas

Patterns for crafting effective skill descriptions that trigger correctly.

## Master Formula

```
DESCRIPTION = [CAPABILITIES] + [USE CASES] + [TRIGGERS] + [BOUNDARIES]
```

| Component | Purpose | Length |
|-----------|---------|--------|
| CAPABILITIES | What the skill does | 1-2 sentences |
| USE CASES | When to use it | 1-2 "Use when:" phrases |
| TRIGGERS | Natural invocation phrases | 3-5 keywords |
| BOUNDARIES | What it doesn't do | 1 "Not for:" phrase |

---

## Pattern Templates

### Pattern 1: Action-Focused

```yaml
description: >-
  [ACTION VERB]s [OBJECT] for [PURPOSE].
  [ADDITIONAL CAPABILITY].
  Use when: [SCENARIO 1], [SCENARIO 2].
  Triggers: [KEYWORD 1], [KEYWORD 2], [KEYWORD 3].
  Not for: [EXCLUSION].
```

**Example:**
```yaml
description: >-
  Generates API documentation from source code.
  Extracts endpoints, parameters, and response schemas automatically.
  Use when: documenting REST APIs, creating OpenAPI specs, updating endpoint docs.
  Triggers: API docs, document API, endpoint documentation.
  Not for: internal code comments or README files.
```

### Pattern 2: Problem-Focused

```yaml
description: >-
  Solves [PROBLEM] by [METHOD].
  Handles [SPECIFIC CASES].
  Use when: [CONDITION 1], [CONDITION 2].
  Triggers: [KEYWORD 1], [KEYWORD 2].
  Not for: [EXCLUSION].
```

**Example:**
```yaml
description: >-
  Solves merge conflicts by analyzing both versions and suggesting resolutions.
  Handles code conflicts, config file conflicts, and lock file conflicts.
  Use when: git merge fails, resolving PR conflicts, rebasing with conflicts.
  Triggers: merge conflict, resolve conflict, fix merge.
  Not for: binary file conflicts.
```

### Pattern 3: Analysis-Focused

```yaml
description: >-
  Analyzes [SUBJECT] to identify [FINDINGS].
  Provides [OUTPUT TYPE].
  Use when: [SCENARIO 1], [SCENARIO 2].
  Triggers: [KEYWORD 1], [KEYWORD 2].
  Not for: [EXCLUSION].
```

**Example:**
```yaml
description: >-
  Analyzes code performance to identify bottlenecks and optimization opportunities.
  Provides detailed reports with actionable recommendations.
  Use when: investigating slow code, optimizing hot paths, pre-release review.
  Triggers: performance analysis, optimize code, find bottlenecks.
  Not for: memory profiling or network analysis.
```

### Pattern 4: Internal Component

```yaml
description: >-
  [CAPABILITY]. Internal component for EPCI v6.0.
  Use when: [INTERNAL TRIGGER CONDITION].
  Not for: direct user invocation.
```

**Example:**
```yaml
description: >-
  Calculates task complexity (TINY/SMALL/STANDARD/LARGE) for workflow routing.
  Internal component for EPCI v6.0.
  Use when: evaluating new requests, routing to /quick vs /implement.
  Not for: direct user invocation.
```

---

## Action Verbs Library

### Creation
- Generates
- Creates
- Builds
- Produces
- Constructs

### Analysis
- Analyzes
- Evaluates
- Examines
- Inspects
- Reviews

### Transformation
- Converts
- Transforms
- Migrates
- Refactors
- Restructures

### Validation
- Validates
- Verifies
- Checks
- Ensures
- Confirms

### Management
- Manages
- Tracks
- Maintains
- Organizes
- Coordinates

---

## Trigger Words by Domain

### Code Quality
- code review, review code, check code
- lint, analyze, inspect
- quality check, code quality

### Testing
- write tests, add tests, create tests
- test coverage, unit tests, integration tests
- TDD, test first

### Documentation
- document, docs, documentation
- API docs, readme, changelog
- explain code, describe

### Debugging
- debug, fix bug, investigate
- error, exception, stack trace
- troubleshoot, diagnose

### Performance
- optimize, performance, speed
- slow, bottleneck, profiling
- memory, CPU, latency

### Security
- security, vulnerability, audit
- OWASP, injection, XSS
- secure, harden

---

## Anti-Pattern Examples

### Too Vague

```yaml
# ❌ BAD
description: "A helpful coding assistant"

# ✅ GOOD
description: >-
  Generates unit tests for JavaScript functions using Jest.
  Creates test files with full coverage of edge cases.
  Use when: adding tests to existing code, TDD workflow.
  Triggers: write tests, create tests, add Jest tests.
```

### Too Short

```yaml
# ❌ BAD
description: "Reviews PRs"

# ✅ GOOD
description: >-
  Reviews pull requests for code quality, tests, and security issues.
  Checks against team standards and provides actionable feedback.
  Use when: reviewing PRs, checking code changes, pre-merge review.
  Triggers: PR review, review pull request, check PR.
```

### No Triggers

```yaml
# ❌ BAD
description: "Analyzes database queries and suggests optimizations."

# ✅ GOOD
description: >-
  Analyzes database queries and suggests optimizations.
  Identifies slow queries, missing indexes, and N+1 problems.
  Use when: optimizing SQL, investigating slow queries.
  Triggers: optimize query, slow SQL, database performance.
```

### Multi-Purpose

```yaml
# ❌ BAD (too broad)
description: >-
  Handles all code-related tasks including review, testing,
  documentation, debugging, and deployment.

# ✅ GOOD (split into focused skills)
# /code-review - for code review
# /test-generator - for testing
# /doc-generator - for documentation
```

---

## Length Guidelines

| Component | Min | Max | Optimal |
|-----------|-----|-----|---------|
| Total description | 50 words | 150 words | 80-100 words |
| Characters | 200 | 1024 | 400-600 |
| Trigger phrases | 3 | 7 | 4-5 |
| Use cases | 2 | 5 | 3 |

---

## Validation Checklist

Before finalizing description:

- [ ] Starts with action verb
- [ ] Specific (not vague)
- [ ] Has "Use when:" section
- [ ] Has "Triggers:" or natural trigger words
- [ ] Has "Not for:" exclusion
- [ ] Under 1024 characters
- [ ] Between 50-150 words
- [ ] 3+ trigger keywords
