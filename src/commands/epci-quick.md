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

## Pre-Workflow: Memory Context

**Memory is loaded once by `/epci-brief`** and passed via the inline brief (Memory Summary section).

**Reading memory context:**
1. Check inline brief for "Memory Summary" section
2. If present: Use conventions and patterns from brief
3. If absent: Continue with defaults (no separate load needed for TINY/SMALL)

**Note:** For TINY/SMALL features, memory context is lightweight. Full memory loading is not required.

---

## Process

**⚠️ IMPORTANT: Follow ALL steps in sequence. Do NOT skip the Output step.**

### 1. Brief Reception (MANDATORY)

The structured brief is provided by `/epci-brief`.
It already contains:
- Target files identified
- Detected stack
- Mode (TINY/SMALL) determined
- Acceptance criteria

**If brief is absent or incomplete** → Suggest `/epci-brief` first.

### 2. Direct Implementation (MANDATORY)

**⚠️ DO NOT SKIP:** Apply changes using Edit tool. Follow the mode-specific steps below.

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

### 4. Commit Preparation

Prepare Conventional Commits message (do not execute yet):

```
fix(scope): short description
```

or

```
feat(scope): short description
```

### ⏸️ BREAKPOINT PRE-COMMIT (MANDATORY — WAIT FOR USER)

**⚠️ MANDATORY:** Display this breakpoint and WAIT for user choice before proceeding.

```
┌─────────────────────────────────────────────────────────────────────┐
│ ⏸️  BREAKPOINT — Validation Commit                                  │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│ 📝 COMMIT SUGGÉRÉ                                                   │
│    {TYPE}({SCOPE}): {DESCRIPTION}                                  │
│                                                                     │
│ 📋 RÉSUMÉ                                                           │
│ ├── Mode: {TINY | SMALL}                                           │
│ ├── Fichiers: {FILE_LIST}                                          │
│ └── Tests: {TEST_STATUS}                                           │
│                                                                     │
├─────────────────────────────────────────────────────────────────────┤
│ Options:                                                            │
│   • Tapez "Commiter" → Exécuter le commit                          │
│   • Tapez "Terminer" → Finaliser sans commit                       │
│   • Tapez "Modifier" → Éditer le message                           │
│   • Tapez "Annuler" → Abandonner                                   │
└─────────────────────────────────────────────────────────────────────┘
```

**Awaiting user choice:**

#### If user chose "Commiter"

Execute git commit and continue to output.

#### If user chose "Terminer"

Skip commit, continue to output with "Commit: Pending".

#### If user chose "Modifier"

Ask for new message, return to breakpoint.

#### If user chose "Annuler"

Abort workflow.

## Output (MANDATORY)

**⚠️ MANDATORY:** Always display the completion message in this exact format.

### TINY Mode

```markdown
✅ **TINY COMPLETE**
FLAGS: [active flags if any] | (none)

Modification applied to `path/to/file.ext`
- Change: [description]
- Lines: +X / -Y

Commit: {COMMITTED | PENDING}
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

Commit: {COMMITTED | PENDING}
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
| Breakpoints | Yes (1: pre-commit) | Yes (3: P1, P2, pre-commit) |
| @plan-validator | No | Yes |
| @code-reviewer | Light (SMALL) | Full |
| @security-auditor | No | Conditional |
| @qa-reviewer | No | Conditional |
| @doc-generator | No | Yes |
| Thinking | Standard | think / think hard |
