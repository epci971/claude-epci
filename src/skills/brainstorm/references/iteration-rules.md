# Iteration Rules

> Rules governing brainstorm iteration progression, phase transitions, and energy management.

## Phase Transitions

### Divergent → Convergent

| Condition | Action |
|-----------|--------|
| EMS >= 50 AND phase == DIVERGENT | Suggest Convergent phase |
| Coverage >= 60% AND 3+ iterations | Offer phase change |

When triggered:
```
BREAKPOINT: Suggest Convergent phase

IF user accepts:
  phase = "CONVERGENT"
  persona = "architecte" (default for convergent)
```

### Convergent Focus

In Convergent phase:
- Primary axes: **Decisions**, **Actionability**
- Push toward decisions
- Suggest decision frameworks (MoSCoW, Weighted Criteria)
- Insist on concrete actions

---

## Finalization Thresholds

### Standard Finish

| Condition | Action |
|-----------|--------|
| EMS >= 70 | Propose finish |
| Max iterations (10) | Force finish suggestion |
| `--quick` mode + iter >= 3 | Suggest finish |

### Finish Options

```
Options:
  - Continue (iterate more)
  - Preview (@planner)
  - Finalize (generate outputs)
```

### Low EMS Warning

| EMS Range | Warning Level |
|-----------|---------------|
| 60-69 | Soft warning (proceed allowed) |
| 50-59 | Strong warning (recommend continue) |
| < 50 | Very strong warning (require --force) |
| < 40 | Critical warning (require explicit --force) |

---

## Stagnation Detection

### Primary Triggers

| Condition | Detection |
|-----------|-----------|
| Delta < 3 for 2 consecutive iterations | Stagnation detected |
| Delta < 5 for 3 consecutive iterations | Alternative stagnation |
| Iteration >= 7 | Fatigue risk |

### Stagnation Response

```
BREAKPOINT: Energy checkpoint

Options:
  - Continue (push through)
  - Pause (save checkpoint for later)
  - Accelerate (finish with current EMS)
  - Pivot (change direction)
```

### Stagnation Message Template

```
⚠️ Stagnation Detected

EMS only progressed {delta_total} points over the last 2 iterations.

Options:
→ `dive [topic]` - Deep dive on specific point
→ `pivot` - Reorient toward emerging subject
→ `finish` - Synthesize current state
```

---

## Quick Mode Adjustments

When `--quick` flag is active:

| Setting | Quick Mode Value |
|---------|------------------|
| Max iterations | 3 |
| Questions per iteration | 2 (skip [Info] category) |
| Finish suggestion | At iteration 3 |
| Output mode | Report only (no journal) |
| Framing questions | 2 max (Target + Priority) |

### Quick Mode Triggers

```
IF --quick mode:
  → Limit to 2 questions
  → Skip [Info] category
  → Suggest finish at iteration >= 3
```

---

## Auto-Persona Switch

See [references/personas.md](./personas.md) for complete persona definitions.

### Quick Reference Triggers

| Trigger | Persona | Symbol |
|---------|---------|--------|
| Unsubstantiated certainty | Sparring | [!] |
| EMS stagnation | Pragmatique | [>] |
| Synthesis needed | Architecte | [#] |
| Open exploration | Maieuticien | [?] |

---

## Iteration Limits

| Limit | Value | Rationale |
|-------|-------|-----------|
| Max iterations | 10 | Prevent infinite loops |
| Max consecutive low-delta | 3 | Force intervention |
| Min EMS for finish | 40 | Quality baseline |
| Recommended finish EMS | 70+ | Good quality output |

---

## Loop Conditions Summary

| Condition | Action |
|-----------|--------|
| User continues | → Self-loop (step-04) |
| User finishes | → `step-05-breakpoint-finish.md` |
| EMS >= 70 + user accepts | → `step-05-breakpoint-finish.md` |
| Max iterations (10) | → `step-05-breakpoint-finish.md` |
| `checkpoint` command | → Save session, exit |
| `--quick` + iter >= 3 | → Suggest finish |

---

## Delta Interpretation

| Delta Range | Interpretation | Recommendation |
|-------------|----------------|----------------|
| +15 or more | Excellent progress | Continue exploration |
| +10 to +14 | Good progress | Continue or converge |
| +5 to +9 | Moderate progress | Consider technique change |
| +3 to +4 | Low progress | Suggest technique or pivot |
| < +3 | Stagnation | Intervention required |

---

*Iteration Rules v1.0 - EPCI Brainstorm v6.0*
