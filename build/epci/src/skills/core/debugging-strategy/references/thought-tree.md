# Thought Tree — Root Cause Analysis

## Overview

The thought tree is a structured diagnostic tool that maps potential causes
of a bug with confidence percentages, enabling systematic elimination and
prioritized investigation.

## Format

```
🔍 ROOT CAUSE ANALYSIS
├── 🎯 Primary (XX%): [Most likely cause]
│   └── Evidence: [Supporting observations]
├── 🔸 Secondary (XX%): [Second most likely]
│   └── Evidence: [Supporting observations]
└── 🔹 Tertiary (XX%): [Third possibility]
    └── Evidence: [Supporting observations]
```

**Confidence total must equal 100%**

## Confidence Scoring

### Initial Assignment

| Evidence Type | Base Confidence |
|---------------|-----------------|
| Stack trace points directly to cause | +40-60% |
| Error message matches known pattern | +20-30% |
| Recent change in affected area | +15-25% |
| Similar bug in project history | +10-20% |
| Educated guess (no evidence) | +5-10% |

### Adjustments

| Factor | Adjustment |
|--------|------------|
| Reproducible consistently | +10% |
| Environment-specific | -10% |
| Timing-dependent | -15% |
| Multiple possible triggers | -10% |

## Evidence Categories

### Strong Evidence (High Confidence)

- **Stack trace**: Direct pointer to failing line
- **Error message**: Explicit description of failure
- **Logs**: Timestamped sequence of events
- **Reproduction steps**: Consistent trigger

### Weak Evidence (Lower Confidence)

- **Correlation**: "It started after X"
- **Similarity**: "Looks like bug Y"
- **Intuition**: "I think it might be..."

## Examples

### Example 1: NullPointerException

```
🔍 ROOT CAUSE ANALYSIS
├── 🎯 Primary (65%): Null user object from database query
│   └── Evidence: Stack trace line 142, UserService.getUser() returns null
│                 when user ID not found (no null check)
├── 🔸 Secondary (25%): Session expired, user context lost
│   └── Evidence: Error occurs after 30min idle, session timeout is 30min
└── 🔹 Tertiary (10%): Race condition in user loading
    └── Evidence: Sporadic occurrence, multi-threaded context
```

### Example 2: API Timeout

```
🔍 ROOT CAUSE ANALYSIS
├── 🎯 Primary (50%): External service slow response
│   └── Evidence: Timeout logs show 30s+ response times from payment API
├── 🔸 Secondary (30%): Connection pool exhaustion
│   └── Evidence: "No available connections" errors in logs before timeout
└── 🔹 Tertiary (20%): Network configuration issue
    └── Evidence: Only affects production, not staging
```

### Example 3: Logic Bug (No Stack Trace)

```
🔍 ROOT CAUSE ANALYSIS
├── 🎯 Primary (45%): Incorrect comparison operator
│   └── Evidence: Output shows >= instead of > behavior, line 78 uses >=
├── 🔸 Secondary (35%): Off-by-one in loop bounds
│   └── Evidence: Affects last element, loop uses <= instead of <
└── 🔹 Tertiary (20%): Data type coercion issue
    └── Evidence: Comparison involves string and number types
```

## Tree Depth Guidelines

| Bug Complexity | Max Depth | Max Branches |
|----------------|-----------|--------------|
| Trivial | 1 | 1 (skip tree) |
| Simple | 2 | 2-3 |
| Medium | 3 | 3-4 |
| Complex | 4+ | 4-5 |

## Updating the Tree

As investigation proceeds:

1. **Confirm**: Increase confidence to 100%, eliminate others
2. **Eliminate**: Set confidence to 0%, redistribute to remaining
3. **Split**: Break a cause into sub-causes if needed
4. **Add**: New evidence reveals new possible cause

## Anti-patterns

- **Flat tree**: All causes at same confidence (need more investigation)
- **Premature certainty**: 100% confidence without verification
- **Missing evidence**: Causes listed without supporting observations
- **Ignoring low probability**: Sometimes the 10% cause is correct
