# Solution Scoring — Decision Framework

## Overview

When multiple solutions exist for a bug fix, use weighted scoring to make
an objective, justified decision. The score ranges from 1-100.

## Scoring Formula

```
Score = (Simplicity * 0.30) + (Risk * 0.25) + (Time * 0.20) + (Maintainability * 0.25)
```

| Axis | Weight | Description |
|------|--------|-------------|
| **Simplicity** | 30% | How simple is the fix? |
| **Risk** | 25% | What's the chance of side effects? |
| **Time** | 20% | How long to implement? |
| **Maintainability** | 25% | How easy to maintain long-term? |

## Axis Calculations

### Simplicity (30%)

```
Simplicity = 100 - (LOC * 2)
```

| LOC Changed | Score | Label |
|-------------|-------|-------|
| 1-5 | 90-100 | Trivial |
| 6-15 | 70-89 | Simple |
| 16-30 | 40-69 | Moderate |
| 31-50 | 0-39 | Complex |
| 50+ | 0 | Very Complex |

**Adjustments:**
- Single file: +5
- Multiple files: -5 per additional file
- New dependency: -10

### Risk (25%)

```
Risk = 100 - (Impact * 20)
```

| Impact Level | Multiplier | Examples |
|--------------|------------|----------|
| 1 (None) | 20 | Isolated code, no dependencies |
| 2 (Low) | 40 | Single module affected |
| 3 (Medium) | 60 | Multiple modules, tested paths |
| 4 (High) | 80 | Core functionality, many callers |
| 5 (Critical) | 100 | Security, payments, data integrity |

**Adjustments:**
- Full test coverage: +10
- No tests: -20
- Breaking change: -30

### Time (20%)

```
Time = 100 - (Minutes / 2)
```

| Time Estimate | Score | Label |
|---------------|-------|-------|
| < 10 min | 95-100 | Immediate |
| 10-30 min | 85-94 | Quick |
| 30-60 min | 70-84 | Standard |
| 1-2 hours | 40-69 | Extended |
| 2+ hours | 0-39 | Long |

**Adjustments:**
- Known pattern: +10
- Research required: -15
- External dependency: -10

### Maintainability (25%)

Expert assessment based on:

| Criterion | Good (+) | Bad (-) |
|-----------|----------|---------|
| **Readability** | Clear intent | Clever tricks |
| **Consistency** | Follows patterns | New pattern |
| **Documentation** | Self-documenting | Needs comments |
| **Testability** | Easy to test | Hard to isolate |
| **Reversibility** | Easy to undo | Permanent change |

**Score guide:**
- 90-100: Exemplary, improves codebase
- 70-89: Good, follows standards
- 50-69: Acceptable, minor concerns
- 30-49: Questionable, tech debt
- 0-29: Poor, avoid if possible

## Output Format

```
💡 SOLUTIONS PROPOSÉES
┌─────────────────────────────────────────────────────────────────┐
│ #1 [Solution title] — Score: XX/100                             │
├─────────────────────────────────────────────────────────────────┤
│ Simplicity: XX | Risk: XX | Time: XX | Maintainability: XX      │
│                                                                 │
│ Justification: [Why this score, key factors]                    │
└─────────────────────────────────────────────────────────────────┘
```

## Example Scoring

### Bug: Missing null check causing NullPointerException

**Solution A: Add null check with early return**
```
Simplicity:      95 (3 LOC, single file)         × 0.30 = 28.5
Risk:            80 (low impact, tested)         × 0.25 = 20.0
Time:            95 (5 min)                      × 0.20 = 19.0
Maintainability: 85 (clear, follows pattern)     × 0.25 = 21.25
──────────────────────────────────────────────────────────────
Total:                                                    88.75 → 89/100
```

**Solution B: Refactor to use Optional pattern**
```
Simplicity:      60 (20 LOC, 3 files)            × 0.30 = 18.0
Risk:            70 (medium impact)              × 0.25 = 17.5
Time:            60 (45 min)                     × 0.20 = 12.0
Maintainability: 95 (modern, type-safe)          × 0.25 = 23.75
──────────────────────────────────────────────────────────────
Total:                                                    71.25 → 71/100
```

**Winner: Solution A (89/100)** — Simpler, faster, lower risk for this specific fix.

## When to Override Scoring

Scoring is a guide, not absolute. Override when:

- **Security**: Always prioritize security over speed
- **User impact**: Visible bugs may need faster, riskier fixes
- **Technical debt**: Sometimes the "right" fix is worth the time
- **Learning opportunity**: Team might benefit from longer approach

Document overrides with justification.
