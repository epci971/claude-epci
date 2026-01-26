# Solution Scoring

## Overview

Scoring matrix for ranking potential solutions in COMPLEX debug route.
Used to present user with ranked options at diagnostic breakpoint.

## Scoring Criteria

Each solution is scored on 4 criteria (1-5 scale, 5 = best):

| Criterion | Weight | Description |
|-----------|--------|-------------|
| Simplicity | 25% | How simple is the implementation? |
| Risk | 25% | What's the regression risk? |
| Time | 25% | Estimated implementation time |
| Maintainability | 25% | Long-term code quality impact |

## Criterion Details

### Simplicity (1-5)

| Score | Description | Example |
|-------|-------------|---------|
| 5 | Trivial change | Change config value |
| 4 | Simple code change | Add null check |
| 3 | Moderate change | Modify function logic |
| 2 | Significant change | Refactor component |
| 1 | Major change | Architectural change |

### Risk (1-5)

| Score | Description | Indicators |
|-------|-------------|------------|
| 5 | Minimal risk | Isolated change, good tests |
| 4 | Low risk | Limited scope, some tests |
| 3 | Moderate risk | Multiple touchpoints |
| 2 | High risk | Core logic, sparse tests |
| 1 | Critical risk | Production data, auth |

### Time (1-5)

| Score | Estimated Time | Description |
|-------|---------------|-------------|
| 5 | < 15 min | Quick fix |
| 4 | 15-30 min | Short task |
| 3 | 30-60 min | Medium task |
| 2 | 1-2 hours | Long task |
| 1 | > 2 hours | Major effort |

### Maintainability (1-5)

| Score | Description | Characteristics |
|-------|-------------|-----------------|
| 5 | Excellent | Clean, documented, tested |
| 4 | Good | Follows patterns, tested |
| 3 | Acceptable | Works, may need cleanup |
| 2 | Poor | Tech debt, hard to test |
| 1 | Bad | Hack, will cause issues |

## Scoring Formula

```
total_score = (
  simplicity * 0.25 +
  risk * 0.25 +
  time * 0.25 +
  maintainability * 0.25
)
```

Range: 1.0 - 5.0

## Interpretation

| Score Range | Recommendation |
|-------------|----------------|
| 4.0 - 5.0 | Excellent option, recommend first |
| 3.0 - 3.9 | Good option, consider |
| 2.0 - 2.9 | Acceptable, use if better options fail |
| 1.0 - 1.9 | Last resort only |

## Example Scoring

**Bug**: Cache returns stale data

### Solution 1: Patch cache TTL config

| Criterion | Score | Rationale |
|-----------|-------|-----------|
| Simplicity | 4 | Single config change |
| Risk | 5 | No code change, easy rollback |
| Time | 5 | < 5 minutes |
| Maintainability | 3 | Doesn't address root cause |

**Total**: 4.25

### Solution 2: Refactor cache layer

| Criterion | Score | Rationale |
|-----------|-------|-----------|
| Simplicity | 2 | Major refactoring |
| Risk | 3 | Multiple components affected |
| Time | 2 | 1-2 hours |
| Maintainability | 5 | Proper fix, well-tested |

**Total**: 3.00

### Solution 3: Add cache invalidation hook

| Criterion | Score | Rationale |
|-----------|-------|-----------|
| Simplicity | 3 | New hook, moderate changes |
| Risk | 4 | Isolated addition |
| Time | 3 | 30-45 minutes |
| Maintainability | 4 | Clean pattern |

**Total**: 3.50

### Ranking

1. S1: Patch config (4.25) - **Recommended**
2. S3: Add hook (3.50)
3. S2: Refactor (3.00)

## Presentation Format

```
+-------+------------------------+--------+--------+-------+
| ID    | Solution               | Effort | Risk   | Score |
+-------+------------------------+--------+--------+-------+
| S1    | Patch cache TTL config | Low    | Low    | 4.25  |
| S3    | Add invalidation hook  | Medium | Low    | 3.50  |
| S2    | Refactor cache layer   | High   | Medium | 3.00  |
+-------+------------------------+--------+--------+-------+
```

**Effort mapping:**
- Score >= 4: Low
- Score 2.5-3.9: Medium
- Score < 2.5: High

**Risk mapping:**
- Risk score >= 4: Low
- Risk score 2.5-3.9: Medium
- Risk score < 2.5: High

## Tie-Breaking Rules

If two solutions have same total score:

1. Prefer higher **Risk** score (safer)
2. Prefer higher **Time** score (faster)
3. Prefer higher **Simplicity** score (simpler)
4. Prefer higher **Maintainability** score (cleaner)

## Adjustments

### --turbo Mode

In turbo mode, increase **Time** weight:

```
total_score = (
  simplicity * 0.20 +
  risk * 0.20 +
  time * 0.40 +      // Increased
  maintainability * 0.20
)
```

### Security Context

If security-related bug, increase **Risk** weight:

```
total_score = (
  simplicity * 0.20 +
  risk * 0.40 +      // Increased
  time * 0.20 +
  maintainability * 0.20
)
```

### Production Incident

If production incident, increase **Time** weight:

```
total_score = (
  simplicity * 0.15 +
  risk * 0.30 +
  time * 0.40 +      // Increased
  maintainability * 0.15
)
```

## Constraints

- Minimum 2 solutions must be presented
- Maximum 4 solutions
- At least one solution must score >= 2.5
- If all solutions < 2.5, escalate to user for guidance
