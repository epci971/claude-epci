# EMS - Exploration Maturity Score

> Scoring system to measure exploration maturity for brainstorm sessions.

## Overview

The EMS (Exploration Maturity Score) is a composite indicator measuring brainstorm progression toward an actionable result. Calculated at each iteration end and displayed as a radar.

## The 5 Axes

| Axis | Weight | Key Question |
|------|--------|--------------|
| **Clarity** | 25% | Is the subject well defined and understood? |
| **Depth** | 25% | Have we dug deep enough? |
| **Coverage** | 20% | Have we explored all relevant angles? |
| **Decisions** | 20% | Have we made progress and decided? |
| **Actionability** | 10% | Can we act concretely after this? |

### Formula

```
EMS = (Clarity x 0.25) + (Depth x 0.25) + (Coverage x 0.20)
    + (Decisions x 0.20) + (Actionability x 0.10)
```

## Objective Anchors

Each axis has **observable criteria** for consistent scoring.

### Clarity (25%)

| Score | Observable Anchor |
|-------|-------------------|
| **20** | Topic stated but not reformulated or validated |
| **40** | Brief validated with in/out scope defined |
| **60** | + Constraints identified (>=2) + success criteria defined |
| **80** | + SMART objectives + stakeholders identified |
| **100** | Zero open questions on the "what" - crystalline definition |

**Progression Signals**:
- User validates reformulation -> +20
- Explicit constraints mentioned -> +10 per constraint (max 2)
- Success criteria defined -> +10
- Stakeholders listed -> +10

### Depth (25%)

| Score | Observable Anchor |
|-------|-------------------|
| **20** | Surface questions only (what, who, when) |
| **40** | At least one "why" chain (2+ levels) |
| **60** | Framework applied OR deep dive completed |
| **80** | Non-obvious insights + cross-domain connections |
| **100** | Root cause identified + validated + implications traced |

**Progression Signals**:
- First "why" explored -> +20
- Second level "why" -> +15
- Framework applied (5 Whys, Fishbone...) -> +15
- Relevant analogy from another domain -> +10
- Root cause explicitly named -> +15

### Coverage (20%)

| Score | Observable Anchor |
|-------|-------------------|
| **20** | Single perspective explored |
| **40** | 2-3 different angles explored |
| **60** | Risks explicitly addressed OR alternatives compared |
| **80** | Complete Six Hats OR >=3 alternatives with criteria OR multi-stakeholders |
| **100** | No identifiable blind spots - exhaustive exploration |

**Progression Signals**:
- New angle explored -> +15 per angle (max 3)
- Risks section addressed -> +15
- Alternative compared -> +10 per alternative (max 2)
- Stakeholder perspective added -> +10

### Decisions (20%)

| Score | Observable Anchor |
|-------|-------------------|
| **20** | Everything remains open, no orientation |
| **40** | 1-2 orientations taken but reversible |
| **60** | Key decisions locked with rationale |
| **80** | Trade-offs made + prioritization established |
| **100** | All scope decisions made, threads closed |

**Progression Signals**:
- First orientation taken -> +20
- Explicit decision with justification -> +15 per decision
- Prioritization established (MoSCoW, scoring...) -> +15
- Thread explicitly closed -> +10 per thread

### Actionability (10%)

| Score | Observable Anchor |
|-------|-------------------|
| **20** | Vague ideas, no concrete action |
| **40** | "We should..." but no who/when |
| **60** | Actions identified with owner OR timeline |
| **80** | Actions + owner + timeline + dependencies |
| **100** | Complete action plan, ready to execute |

**Progression Signals**:
- First concrete action named -> +20
- Owner assigned -> +15
- Timeline defined -> +15
- Dependencies identified -> +10
- Quick win identified -> +10

## Phase Integration

Recommendations adapt to current phase.

### In Divergent Phase

**Primary Focus**: Coverage, Depth

**Typical Recommendations**:
```
Recommendations (divergent phase):
  -> Coverage at 45%: Let's explore other angles (stakeholders? risks?)
  -> Depth at 38%: A deep dive would enrich the exploration
```

**Behavior**:
- Don't push Decisions (normal to be low)
- Encourage broad exploration
- Suggest exploration frameworks (Six Hats, Starbursting)

### In Convergent Phase

**Primary Focus**: Decisions, Actionability

**Typical Recommendations**:
```
Recommendations (convergent phase):
  -> Decisions at 52%: 3 points remain open, let's decide
  -> Actionability at 40%: Let's define concrete actions with owners
```

**Behavior**:
- Push toward decisions
- Suggest decision frameworks (MoSCoW, Weighted Criteria)
- Insist on concrete actions

### Phase Change Suggestion

When Coverage reaches 60%+ and in Divergent for 3+ iterations:

```
Phase Suggestion

Exploration seems mature (Coverage: 72%, Depth: 68%).
We could switch to Convergent mode to start deciding.

-> `converge` - Switch to decision mode
-> `continue` - Stay in open exploration
```

## Display Format

### Standard Format (end of iteration)

```
EMS: 68/100 (+12) [================....]

   Clarity      [================....] 78/100 (+8)
   Depth        [==============......] 65/100 (+15) ^
   Coverage     [================....] 72/100 (+10)
   Decisions    [==========..........] 52/100 (+5) !
   Actionab.    [========............] 45/100 (+8)

Exploration in development

Recommendations:
  -> Decisions weak: 3 key points remain to decide
  -> Actionability: Let's start defining concrete actions
```

### Quick Mode Format (simplified)

```
EMS: 68/100 (+12) [in development]
```

### Indicator Legend

| Indicator | Meaning |
|-----------|---------|
| ^ | Notable progression (+10 or more) |
| ! | Weak axis (< 50) |
| * | Strong axis (>= 80) |
| X | Critical axis (< 30) |

## Thresholds and Messages

| EMS Range | Status | Icon | Message |
|-----------|--------|------|---------|
| 0-29 | Beginning | [seed] | "Exploration starting - let's continue" |
| 30-59 | Development | [sprout] | "Exploration in development" |
| 60-89 | Mature | [tree] | "Exploration mature - `finish` available" |
| 90-100 | Complete | [target] | "Exploration very complete - `finish` recommended" |

### Contextual Messages

**Stagnation detected** (< 5 pts over 2 iterations):
```
Stagnation Detected

EMS only progressed [X] points over the last 2 iterations.

Options:
-> `dive [topic]` - Deep dive on specific point
-> `pivot` - Reorient toward emerging subject
-> `finish` - Synthesize current state
```

**Minimum score not reached** (with `--min-score`):
```
Minimum Score Not Reached

Current EMS: 58/100 | Required minimum: 70/100

Axes to improve:
- Decisions: 45/100 (need: +25)
- Actionability: 38/100 (need: +20)

Options:
-> `continue` - Continue exploration
-> `finish --force` - Generate report despite score
```

## Initialization

EMS starts at **0** and is initialized after brief validation.

### Initial Scores Based on Clarity

| Clarity Score | Initial EMS Clarity | Other Axes |
|---------------|---------------------|------------|
| >= 0.8 | 60 | 25 each |
| 0.6 - 0.79 | 45 | 20 each |
| 0.4 - 0.59 | 30 | 20 each |
| < 0.4 | 20 | 15 each |

### Initialization Bonuses

| Condition | Bonus |
|-----------|-------|
| Brief validated | Clarity: +20 |
| Sources analyzed | Depth: +10, Coverage: +10 |
| History found | Clarity: +10 |
| HMW generated | Coverage: +5 |

### Example Initialization

```
Input clarity: 0.7 (medium)
→ Initial Clarity: 45
→ After brief validated: 45 + 20 = 65
→ After HMW generated: Coverage += 5

Starting EMS:
- Clarity: 65
- Depth: 20
- Coverage: 25
- Decisions: 20
- Actionability: 20
- Global: 65×0.25 + 20×0.25 + 25×0.20 + 20×0.20 + 20×0.10 = 32.25 ≈ 32
```

### Progression Triggers

EMS recalculation occurs when:

| Trigger | Action |
|---------|--------|
| User response integrated | Full recalculation |
| Decision made explicit | +15-20 Decisions axis |
| Technique applied | Context-dependent bonus |
| Thread closed | +10 Decisions axis |
| Deep dive completed | +15-20 Depth axis |
| New angle explored | +10-15 Coverage axis |

### Delta Interpretation

| Delta | Interpretation | Typical Cause |
|-------|----------------|---------------|
| +20 or more | Major breakthrough | Framework applied, key insight |
| +15 to +19 | Excellent progress | Multiple good answers |
| +10 to +14 | Good progress | Solid iteration |
| +5 to +9 | Moderate progress | Standard answers |
| +3 to +4 | Low progress | Minimal new info |
| < +3 | Stagnation | Repeat questions, user fatigue |
| Negative | Regression | Scope expansion, lost clarity |

## EMS in Checkpoints

Checkpoint saves complete state:

```yaml
ems_state:
  global: 68
  clarity: 78
  depth: 65
  coverage: 72
  decisions: 52
  actionability: 45
  history:
    - iteration: 1
      score: 32
      delta: +32
    - iteration: 2
      score: 48
      delta: +16
    - iteration: 3
      score: 68
      delta: +20
```

## EMS in Final Report

The report includes:

1. **Final score** with visual radar
2. **Progression graph** (ASCII art)
3. **Axis analysis** weak/strong
4. **Success criteria verification**

### Progression Graph

```
EMS Score
100 |                                    *--- 78 (End)
 80 | . . . . . . . . . . . . . . . .+--+ . .
 60 | . . . . . . . . . . . . . .+--+ . . . .
 48 |                      +----+
 40 | . . . . . . . . .+--+ . . . . . . . . .
 32 |            +----+
 20 |      +----+
  0 +-----+-----+-----+-----+-----+-----+-----
    Init  It.1  It.2  It.3  It.4  It.5  End
```

## Best Practices

### To improve Clarity
- Reformulate and validate
- Explicitly define scope (in/out)
- List constraints
- Define success criteria

### To improve Depth
- Apply 5 Whys
- Do a deep dive on a key point
- Look for analogies in other domains
- Identify root cause

### To improve Coverage
- Apply Six Hats
- List risks
- Explore alternatives
- Consider different stakeholders

### To improve Decisions
- Apply MoSCoW
- Use weighted scoring
- Explicitly close threads
- Document rationales

### To improve Actionability
- Define concrete actions
- Assign owners
- Set deadlines
- Identify quick wins

## System Limits

- EMS is an **indicator**, not absolute truth
- Anchors are **guides**, not rigid rules
- High EMS doesn't guarantee good brainstorming (form vs substance)
- Low EMS may be appropriate for preliminary exploration
- The system doesn't capture idea **quality**, only process **maturity**

---

*EMS System v3.0 - EPCI Brainstorm v6.0*
