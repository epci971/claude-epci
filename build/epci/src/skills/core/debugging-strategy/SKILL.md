---
name: debugging-strategy
description: >-
  Structured debugging methodology with thought tree analysis, solution scoring,
  and adaptive routing. Auto-invoke when: /debug called, error/bug mentioned,
  stack trace provided. Do NOT load for: feature development, refactoring without bugs.
allowed-tools: [Read, Glob, Grep, WebSearch, WebFetch]
---

# Debugging Strategy v1.0

## Overview

Systematic approach to bug diagnosis and resolution using:
- **Thought Tree**: Root cause analysis with confidence scoring
- **Solution Scoring**: Objective comparison of fix options
- **Adaptive Routing**: Right-sized process based on complexity

**Reference Documents:**
- [Thought Tree](references/thought-tree.md) — Root cause analysis format
- [Scoring](references/scoring.md) — Solution comparison framework
- [Thresholds](references/thresholds.md) — Routing decision criteria

## Diagnostic Workflow

```
Error/Bug Input
      │
      ▼
┌─────────────────┐
│ 1. GATHER       │ ← Stack trace, logs, reproduction steps
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 2. RESEARCH     │ ← Context7 MCP (docs) + Web Search (known issues)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 3. ANALYZE      │ ← Build thought tree with confidence %
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 4. ROUTE        │ ← Trivial / Quick / Complet
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 5. FIX          │ ← Implement based on mode
└─────────────────┘
```

## Phase 1: Gather Evidence

Collect all available information:

| Source | What to Extract |
|--------|-----------------|
| Stack trace | File, line, call chain |
| Error message | Error type, description |
| Logs | Timestamps, sequence, context |
| Reproduction | Steps to trigger, frequency |
| Recent changes | Git diff, related commits |

## Phase 2: Research

### Context7 MCP Integration

If available, query Context7 for:
- Library/framework documentation
- Known issues with detected versions
- API usage patterns

**Fallback**: If Context7 MCP unavailable:
1. Log warning: "Context7 MCP not configured, using web search only"
2. Continue with web search

### Web Search

Search for:
- Error message + framework name
- GitHub issues (filter: open, recent)
- Stack Overflow (filter: accepted answers, < 2 years)

**Filter criteria:**
- Prioritize official documentation
- Results < 2 years old
- High upvote/accepted answers

## Phase 3: Analyze (Thought Tree)

Build root cause analysis:

```
🔍 ROOT CAUSE ANALYSIS
├── 🎯 Primary (XX%): [Most likely cause]
│   └── Evidence: [Supporting facts]
├── 🔸 Secondary (XX%): [Alternative cause]
│   └── Evidence: [Supporting facts]
└── 🔹 Tertiary (XX%): [Less likely cause]
    └── Evidence: [Supporting facts]
```

**Confidence must total 100%**

→ See [thought-tree.md](references/thought-tree.md) for detailed format

## Phase 4: Route

Evaluate against thresholds:

| Criterion | Trivial | Quick | Complet |
|-----------|---------|-------|---------|
| Causes | 1 obvious | 1 | 2+ |
| LOC | < 10 | < 50 | ≥ 50 |
| Files | 1 | 1-2 | 3+ |
| Risk | None | Low | Medium+ |
| Uncertainty | < 5% | < 20% | ≥ 20% |

**Rule**: ≥ 2 Complet criteria → Complet mode

→ See [thresholds.md](references/thresholds.md) for details

## Phase 5: Fix

### Trivial Mode
- Skip thought tree (cause obvious)
- Direct fix
- Inline summary

### Quick Mode
- Simplified thought tree
- Single solution
- Direct fix
- Inline summary

### Complet Mode
- Full thought tree
- Multiple solutions with scoring
- Breakpoint for approval
- Fix implementation
- @code-reviewer validation
- Debug Report output

## Solution Scoring (Complet Mode)

```
Score = (Simplicity*0.30) + (Risk*0.25) + (Time*0.20) + (Maintainability*0.25)
```

→ See [scoring.md](references/scoring.md) for calculation details

## Output Formats

### Inline Summary (Trivial/Quick)

```
✅ BUG FIXED

Cause: [Root cause identified]
Fix: [What was changed]
Files: [Modified files]

Verification: [How to verify the fix]
```

### Debug Report (Complet)

File: `docs/debug/<slug>-<date>.md`

```markdown
# Debug Report — [Title]

## Problem
[Description of the bug]

## Root Cause Analysis
[Thought tree]

## Solution
[Chosen fix with score]

## Implementation
[Changes made]

## Verification
[Test results, validation]
```

## Integration with EPCI

### During /epci Phase 2

If error encountered during implementation:
1. Skill auto-loads
2. Quick diagnostic
3. Inline fix or suggest `/debug`

### Standalone /debug

Full debugging workflow with all phases.

## Anti-patterns

| Don't | Do Instead |
|-------|------------|
| Guess without evidence | Gather data first |
| Jump to fix immediately | Analyze causes |
| Ignore low-probability causes | Consider all options |
| Skip verification | Always test the fix |
| Over-engineer simple bugs | Match effort to complexity |

## Quick Reference

### Diagnostic Checklist

- [ ] Stack trace captured?
- [ ] Error message understood?
- [ ] Reproduction steps known?
- [ ] Recent changes reviewed?
- [ ] Documentation checked?
- [ ] Similar issues searched?

### Confidence Triggers

| Evidence | Confidence Boost |
|----------|------------------|
| Stack trace points to line | +40-60% |
| Error matches known pattern | +20-30% |
| Reproducible consistently | +10% |
| Recent change in area | +15-25% |
