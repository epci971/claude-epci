---
description: >-
  Condensed EPCI workflow for TINY and SMALL features. Single-pass without
  formal Feature Document. TINY mode: <50 LOC, 1 file, no tests.
  SMALL mode: <200 LOC, 2-3 files, optional tests.
argument-hint: "[--fast] [--uc]"
allowed-tools: [Read, Write, Edit, Bash, Grep, Glob, Task]
---

# EPCI Quick — Condensed Workflow

## Overview

Simplified workflow for small modifications.
No formal Feature Document, no breakpoints.

## Modes

### TINY Mode

| Criteria | Value |
|----------|-------|
| Files | 1 only |
| LOC | < 50 |
| Tests | Not required |
| Duration | < 15 minutes |
| Examples | Typo, config, small fix |

### SMALL Mode

| Criteria | Value |
|----------|-------|
| Files | 2-3 |
| LOC | < 200 |
| Tests | Optional |
| Duration | 15-60 minutes |
| Examples | Small feature, local refactor |

## Supported Flags

| Flag | Effect | Auto-Trigger |
|------|--------|--------------|
| `--fast` | Skip optional checks | Never |
| `--uc` | Compressed output | context > 75% |

**Note:** Thinking flags (`--think-hard`, `--ultrathink`) trigger escalation to `/epci`.

## Configuration

| Element | Value |
|---------|-------|
| **Thinking** | `think` (standard) |
| **Skills** | project-memory-loader, epci-core, code-conventions, flags-system, [stack] |
| **Subagents** | @code-reviewer (light mode, SMALL only)

## Pre-Workflow: Load Project Memory

**Skill**: `project-memory-loader`

Load project context from `.project-memory/` before implementation. The skill handles:
- Reading context, conventions, settings, patterns
- Applying naming/structure/style conventions to all generated code

**If `.project-memory/` does not exist:** Continue with defaults.

---

## Process

### 1. Brief Reception

The structured brief is provided by `/epci-brief`.
It already contains:
- Target files identified
- Detected stack
- Mode (TINY/SMALL) determined
- Acceptance criteria

**If brief is absent or incomplete** → Suggest `/epci-brief` first.

### 2. Direct Implementation

#### TINY Mode

```
1. Read target file
2. Identify modification
3. Apply change
4. Verify (lint, syntax)
5. Done
```

#### SMALL Mode

```
1. Read concerned files
2. Plan mentally (no formal doc)
3. For each modification:
   a. If test requested → write test first
   b. Implement change
   c. Verify
4. Run existing tests
5. Quick review if needed
```

### 3. Review (optional)

For SMALL only, invoke @code-reviewer in light mode:
- Focus on obvious bugs
- Syntax/typing errors
- Missing tests (if requested)

**No architecture or optimization review.**

### 4. Commit

Simplified Conventional Commits format:

```
fix(scope): short description
```

or

```
feat(scope): short description
```

## Output

### TINY Mode

```markdown
✅ **TINY COMPLETE**
FLAGS: [active flags if any] | (none)

Modification applied to `path/to/file.ext`
- Change: [description]
- Lines: +X / -Y

Ready to commit.
```

### SMALL Mode

```markdown
✅ **SMALL COMPLETE**
FLAGS: [active flags if any] | (none)

Modified files:
- `path/to/file1.ext` (+X / -Y)
- `path/to/file2.ext` (+Z / -W)

Tests: [X passing | Not required]
Review: [@code-reviewer light | Not required]

Ready to commit.
```

## Examples

### TINY Example

**Brief:** "Fix typo 'recieve' to 'receive' in UserService"

```
→ Mode: TINY
→ File: src/Service/UserService.php
→ Action: Search/replace
→ Commit: fix(user): correct typo in UserService
```

### SMALL Example

**Brief:** "Add isActive() method to User entity"

```
→ Mode: SMALL
→ Files:
  - src/Entity/User.php (add method)
  - tests/Unit/Entity/UserTest.php (add test)
→ Actions:
  1. Write test for isActive()
  2. Implement isActive()
  3. Verify tests
→ Commit: feat(user): add isActive method
```

## When to Escalate to /epci

**Note**: Mode detection is now done by `/epci-brief`. However, escalate if during implementation you discover:
- More than 3 impacted files
- Regression risk identified
- Underestimated complexity
- Integration tests needed

```
⚠️ **ESCALATION RECOMMENDED**

The modification is more complex than anticipated:
- [Reason 1]
- [Reason 2]

Recommendation: Switch to `/epci` for structured workflow.
```

## Differences with /epci

| Aspect | /epci-quick | /epci |
|--------|-------------|-------|
| Feature Document | No | Yes |
| Breakpoints | No | Yes (2) |
| @plan-validator | No | Yes |
| @code-reviewer | Light (SMALL) | Full |
| @security-auditor | No | Conditional |
| @qa-reviewer | No | Conditional |
| @doc-generator | No | Yes |
| Thinking | Standard | think / think hard |
