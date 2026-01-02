# Routing Thresholds — Bug Classification

## Overview

After diagnostic phase, bugs are automatically routed to the appropriate
fix mode based on measured criteria. This ensures proportional effort.

## Routing Decision Table

| Mode | Causes | LOC | Files | Risk | Uncertainty |
|------|--------|-----|-------|------|-------------|
| **Trivial** | 1 (obvious) | < 10 | 1 | None | < 5% |
| **Quick** | 1 | < 50 | 1-2 | Low | < 20% |
| **Complet** | 2+ | ≥ 50 | 3+ | Medium+ | ≥ 20% |

**Rule**: ≥ 2 criteria in "Complet" column → Mode Complet

## Mode Definitions

### Trivial (Direct Fix)

**Characteristics:**
- Obvious cause (typo, missing import, syntax error)
- No thought tree needed (cause is self-evident)
- Fix is immediate and risk-free

**Examples:**
- Typo in variable name
- Missing semicolon/bracket
- Wrong import path
- Incorrect constant value

**Output:** Inline fix + one-line explanation

### Quick (Standard Debug)

**Characteristics:**
- Single root cause identified
- Fix is straightforward
- Minimal side effects expected

**Process:**
1. Thought tree (simplified)
2. Single solution (no scoring needed)
3. Direct fix implementation
4. Inline summary

**Output:** Inline diagnostic + fix + summary

### Complet (Full Debug)

**Characteristics:**
- Multiple possible causes
- Complex fix or significant changes
- Risk of side effects
- Uncertainty about best approach

**Process:**
1. Full thought tree
2. Multiple solutions with scoring
3. Plan with breakpoint
4. Fix implementation
5. Review (@code-reviewer)
6. Debug Report

**Output:** `docs/debug/<slug>-<date>.md`

## Threshold Details

### Cause Count

| Count | Classification | Reasoning |
|-------|----------------|-----------|
| 1 (obvious) | Trivial | Self-evident, no analysis needed |
| 1 (analyzed) | Quick | Single cause, but needed investigation |
| 2+ | Complet | Multiple hypotheses require full process |

### LOC Estimate

| LOC | Classification | Reasoning |
|-----|----------------|-----------|
| < 10 | Trivial | One-liner or minimal change |
| 10-49 | Quick | Contained change, manageable |
| 50+ | Complet | Significant change, needs planning |

### Files Impacted

| Files | Classification | Reasoning |
|-------|----------------|-----------|
| 1 | Trivial/Quick | Isolated impact |
| 2 | Quick | Limited scope |
| 3+ | Complet | Cross-cutting, needs coordination |

### Risk Assessment

| Level | Classification | Indicators |
|-------|----------------|------------|
| None | Trivial | Dead code, isolated, fully tested |
| Low | Quick | Single module, good coverage |
| Medium | Complet | Core paths, partial coverage |
| High | Complet | Security, payments, data integrity |

### Uncertainty

| Level | Classification | Meaning |
|-------|----------------|---------|
| < 5% | Trivial | "I know exactly what's wrong" |
| 5-19% | Quick | "Confident but should verify" |
| ≥ 20% | Complet | "Need to investigate further" |

## Quality Gates

### Pre-Fix Validation

| Check | Trivial | Quick | Complet |
|-------|---------|-------|---------|
| Thought tree | Skip | Simplified | Full |
| Solution scoring | Skip | Skip | Required |
| Plan approval | Skip | Skip | Breakpoint |

### Post-Fix Validation

| Check | Trivial | Quick | Complet |
|-------|---------|-------|---------|
| Test run | Optional | Recommended | Required |
| @code-reviewer | Skip | Optional | Required |
| @security-auditor | Skip | Skip | If security-related |
| Debug Report | Skip | Skip | Required |

## Override Flags

| Flag | Effect |
|------|--------|
| `--full` | Force Complet mode regardless of thresholds |
| `--no-report` | Complet mode without Debug Report file |

## Routing Examples

### Example 1: Typo
```
Cause: 1 (obvious - "usrename" instead of "username")
LOC: 1
Files: 1
Risk: None
Uncertainty: 0%
→ TRIVIAL
```

### Example 2: Missing Validation
```
Cause: 1 (null check missing)
LOC: 15
Files: 1
Risk: Low
Uncertainty: 10%
→ QUICK
```

### Example 3: Race Condition
```
Causes: 3 (timing, state, concurrency)
LOC: 80
Files: 4
Risk: High
Uncertainty: 35%
→ COMPLET (5/5 criteria met)
```

### Example 4: Edge Case (Override)
```
Cause: 1
LOC: 25
Files: 2
Risk: High (payment system)
Uncertainty: 5%
→ COMPLET (Risk overrides other factors)
```
