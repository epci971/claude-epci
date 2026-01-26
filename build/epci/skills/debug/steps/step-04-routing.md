---
name: step-04-routing
description: Evaluate complexity and route to appropriate fix strategy
prev_step: steps/step-03-thought-tree.md
next_step: null
conditional_next:
  - condition: "route == TRIVIAL"
    step: steps/step-05-trivial.md
  - condition: "route == QUICK"
    step: steps/step-06-quick.md
  - condition: "route == COMPLEX OR --full"
    step: steps/step-07-complex.md
---

# Step 04: Routing

## MANDATORY EXECUTION RULES (READ FIRST):

- :red_circle: NEVER override routing without explicit --full flag
- :red_circle: NEVER route COMPLEX bugs as TRIVIAL
- :white_check_mark: ALWAYS use complexity-calculator
- :white_check_mark: ALWAYS evaluate all routing criteria
- :white_check_mark: ALWAYS apply >=2 COMPLEX criteria rule
- :thought_balloon: FOCUS on accurate routing to optimize fix time

## EXECUTION PROTOCOLS:

### 1. Evaluate Routing Criteria

Use `complexity-calculator` with debug-specific criteria:

| Criterion | TRIVIAL | QUICK | COMPLEX |
|-----------|---------|-------|---------|
| Causes | 1 obvious | 1 | 2+ |
| LOC to fix | <10 | <50 | >=50 |
| Files affected | 1 | 1-2 | 3+ |
| Uncertainty | <5% | <20% | >=20% |
| Research needed | No | Minimal | Significant |

### 2. Scoring Matrix

Score each criterion:

```
ROUTING SCORE:

Causes:
- 1 obvious cause = TRIVIAL (0)
- 1 cause = QUICK (1)
- 2+ causes = COMPLEX (2)

LOC estimate:
- <10 = TRIVIAL (0)
- 10-49 = QUICK (1)
- >=50 = COMPLEX (2)

Files affected:
- 1 = TRIVIAL/QUICK (0-1)
- 2 = QUICK (1)
- 3+ = COMPLEX (2)

Uncertainty:
- <5% = TRIVIAL (0)
- 5-19% = QUICK (1)
- >=20% = COMPLEX (2)

COMPLEX_CRITERIA_COUNT = count(score == 2)

if COMPLEX_CRITERIA_COUNT >= 2:
  route = COMPLEX
elif max(scores) == 0:
  route = TRIVIAL
else:
  route = QUICK
```

### 3. TRIVIAL Detection

Route TRIVIAL if ALL:
- Single, obvious cause
- Fix is < 10 LOC
- Single file
- Confidence > 95%
- No tests needed (obvious fix)

**TRIVIAL Examples:**
- Typo in variable name
- Missing import statement
- Wrong string literal
- Off-by-one in condition
- Missing null check (obvious)

### 4. QUICK Detection

Route QUICK if:
- Single cause identified
- Fix is < 50 LOC
- 1-2 files affected
- Confidence > 80%
- Regression test feasible

**QUICK Examples:**
- Logic error in single function
- Missing validation
- Wrong API parameter
- Incorrect state update
- Missing error handling

### 5. COMPLEX Detection

Route COMPLEX if ANY:
- Multiple potential causes (2+)
- Fix requires >= 50 LOC
- 3+ files affected
- Uncertainty >= 20%
- Security implications
- Data integrity concerns

**COMPLEX Examples:**
- Race condition
- Memory leak
- Authentication bypass
- Data corruption
- Intermittent failures
- Performance degradation

### 6. --full Flag Override

If `--full` provided, force COMPLEX route:

```
if --full:
  route = COMPLEX
  reason = "Forced by --full flag"
```

### 7. --turbo Mode Adjustment

In turbo mode, bias toward simpler routes:

```
if --turbo:
  if route == COMPLEX AND confidence >= 70%:
    route = QUICK
    reason = "Turbo mode: high-confidence hypothesis, simplified route"
```

## CONTEXT BOUNDARIES:

- This step expects: Ranked hypotheses from step-03
- This step produces: Routing decision with justification

## OUTPUT FORMAT:

```
## Routing Evaluation

### Criteria Assessment

| Criterion | Value | Score |
|-----------|-------|-------|
| Causes | {N} | {0/1/2} |
| LOC estimate | {N} | {0/1/2} |
| Files affected | {N} | {0/1/2} |
| Uncertainty | {N}% | {0/1/2} |

### Routing Decision

**Route**: {TRIVIAL | QUICK | COMPLEX}

**Justification**:
{reason for routing decision}

### Top Hypothesis
- **H1**: {title}
- **Confidence**: {N}%
- **Files**: {list}

{Route-specific message}
```

## ROUTE-SPECIFIC MESSAGES:

### TRIVIAL
```
Route: TRIVIAL

This appears to be a straightforward fix.
Proceeding with direct fix (no breakpoint).
```

### QUICK
```
Route: QUICK

Single-cause bug identified.
Proceeding with TDD cycle (Red-Green-Verify).
```

### COMPLEX
```
Route: COMPLEX

Multiple factors involved. Full investigation required.
Will generate solution scoring and present diagnostic breakpoint.
```

## NEXT STEP TRIGGER:

- If TRIVIAL → step-05-trivial.md
- If QUICK → step-06-quick.md
- If COMPLEX OR --full → step-07-complex.md
