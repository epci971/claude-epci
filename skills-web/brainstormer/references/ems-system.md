# EMS — Exploration Maturity Score

> Complete specifications for the real-time exploration scoring system

---

## Overview

The EMS (Exploration Maturity Score) is a composite score from 0 to 100 that measures the maturity and quality of a brainstorming exploration in real-time. It evolves at each iteration based on 5 weighted axes.

**Purpose**:
- Provide objective measure of exploration progress
- Trigger contextual recommendations
- Guide decision to continue or finish
- Create engagement through visible progression

**Key characteristics**:
- Bidirectional evolution (can increase AND decrease)
- Displayed at end of every iteration
- Subjective evaluation by Claude based on explicit criteria
- No maximum delta per iteration (free evolution)

---

## The 5 Axes

### Formula

```
EMS = (Clarity × 0.25) + (Depth × 0.25) + (Coverage × 0.20) 
    + (Decisions × 0.20) + (Actionability × 0.10)
```

### Axis 1: Clarity (25%)

> *"Is the subject well defined and understood?"*

| Score | Level | Criteria |
|-------|-------|----------|
| 0-20 | 🔴 Vague | Subject unclear, no validated reformulation |
| 21-40 | 🟠 Emerging | Brief validated but gray areas remain |
| 41-60 | 🟡 Defined | Clear scope, constraints identified |
| 61-80 | 🟢 Precise | SMART objectives, clear success criteria |
| 81-100 | 🔵 Crystal | Shared vision, zero ambiguity |

**What increases it**:
- Validated reformulations
- Explicitly stated constraints
- Defined success criteria
- Scope clearly delineated (in/out)

**What decreases it**:
- Poorly framed pivot
- New ambiguities introduced
- Contradictions in requirements
- Scope creep without acknowledgment

---

### Axis 2: Depth (25%)

> *"Have we dug deep enough?"*

| Score | Level | Criteria |
|-------|-------|----------|
| 0-20 | 🔴 Surface | Basic questions, generic answers |
| 21-40 | 🟠 Exploratory | Some deepening, still superficial |
| 41-60 | 🟡 Substantial | Deep dives done, root causes explored |
| 61-80 | 🟢 Thorough | 5 Whys applied, frameworks used |
| 81-100 | 🔵 Expert | Non-obvious insights, original connections |

**What increases it**:
- Deep dives on specific topics
- Framework application (5 Whys, SWOT, etc.)
- Chained "why" questions
- Expert knowledge brought in
- Analogies from other domains

**What decreases it**:
- Staying at surface level
- Ignoring deepening suggestions
- Skipping over complex topics
- Accepting first answers without probing

---

### Axis 3: Coverage (20%)

> *"Have we explored all relevant angles?"*

| Score | Level | Criteria |
|-------|-------|----------|
| 0-20 | 🔴 Tunnel | Only one angle explored |
| 21-40 | 🟠 Partial | 2-3 perspectives, obvious gaps |
| 41-60 | 🟡 Adequate | Main perspectives covered |
| 61-80 | 🟢 Broad | Risks, alternatives, constraints all explored |
| 81-100 | 🔵 360° | Six Hats complete, no identifiable blind spots |

**What increases it**:
- Exploring alternatives
- Considering risks and downsides
- Changing perspectives (user, tech, business)
- Applying Six Hats or similar
- Addressing stakeholder viewpoints

**What decreases it**:
- Ignoring suggested angles
- Staying mono-perspective
- Dismissing alternatives without consideration
- Tunnel vision on preferred solution

---

### Axis 4: Decisions (20%)

> *"Have we made progress and decided?"*

| Score | Level | Criteria |
|-------|-------|----------|
| 0-20 | 🔴 Undecided | No decisions, everything remains open |
| 21-40 | 🟠 Hesitant | Some orientations, much uncertainty |
| 41-60 | 🟡 Progressive | Intermediate decisions made |
| 61-80 | 🟢 Determined | Key decisions locked, few open threads |
| 81-100 | 🔵 Resolved | All decisions made, clear arbitrations |

**What increases it**:
- Making explicit decisions
- Validating orientations
- Closing threads definitively
- Prioritizing options
- Choosing between alternatives

**What decreases it**:
- Reopening closed subjects
- Staying in indecision
- Avoiding commitment
- Endless deliberation without progress

---

### Axis 5: Actionability (10%)

> *"Can we act concretely after this brainstorm?"*

| Score | Level | Criteria |
|-------|-------|----------|
| 0-20 | 🔴 Abstract | Vague ideas, nothing actionable |
| 21-40 | 🟠 Conceptual | Directions but no concrete actions |
| 41-60 | 🟡 Outlined | Some actions identified |
| 61-80 | 🟢 Plannable | Clear actions with owners/timelines |
| 81-100 | 🔵 Executable | Complete action plan, ready to start |

**What increases it**:
- Defining concrete actions
- Assigning responsibilities
- Setting timelines
- Identifying next steps
- Creating actionable outputs

**What decreases it**:
- Staying theoretical
- Not concretizing insights
- Avoiding commitment to actions
- Vague "we should" without specifics

---

## Threshold Triggers

| EMS Range | Status | Message | Behavior |
|-----------|--------|---------|----------|
| 0-29 | 🌱 Beginner | "Exploration starting" | No finish suggestion |
| 30-59 | 🌿 Developing | "Exploration developing" | Normal mode |
| 60-89 | 🌳 Mature | "Exploration mature — `finish` available" | Soft finish suggestion |
| 90-100 | 🎯 Complete | "Exploration very complete — `finish` recommended" | Strong finish suggestion |

---

## Contextual Recommendations

### Detection Logic

```
AFTER EMS calculation:

FOR EACH axis:
  IF axis_score < 40:
    Mark as "critical" ⚠️
    Add targeted recommendation
  ELSE IF axis_score < 60:
    Mark as "needs improvement"
    Consider adding recommendation

LIMIT recommendations to 2 per iteration
PRIORITIZE by lowest score
```

### Recommendation Messages by Axis

| Axis | If < 40 | If 40-59 |
|------|---------|----------|
| **Clarity** | "Subject still unclear. Let's reformulate the core objective." | "Some gray areas remain. Should we clarify [specific point]?" |
| **Depth** | "Exploration superficial. Shall we do a deep dive or apply 5 Whys?" | "Good progress, but [topic] deserves more depth." |
| **Coverage** | "Tunnel vision detected. Let's explore risks or apply Six Hats." | "Main angles covered. Any stakeholder perspective missing?" |
| **Decisions** | "Many open points. Let's list and decide on [topic]." | "Making progress. Ready to lock [pending decision]?" |
| **Actionability** | "Still abstract. Let's define one concrete next action." | "Getting actionable. Who owns [identified action]?" |

### Display Format

```
💡 Recommendations:
   → [Primary recommendation for lowest axis]
   → [Secondary recommendation if another axis < 60]
```

---

## Stagnation Detection

### Logic

```
AFTER EMS calculation:

delta = current_ems - previous_ems

IF delta < 5:
  stagnation_count += 1
ELSE:
  stagnation_count = 0

IF stagnation_count >= 2:
  DISPLAY stagnation alert
  RESET stagnation_count = 0
```

### Alert Message

```
⚠️ Plateau detected — EMS score has stagnated for 2 iterations.

Suggestions:
→ Change angle (Six Hats framework?)
→ Deep dive on [weakest axis topic]
→ Consider a pivot if real subject has shifted
→ Move to `finish` if exploration is sufficient
```

---

## Coaching Mode

### Default: ON (Moderate level)

| Behavior | Description |
|----------|-------------|
| **Challenges** | 2-3 constructive challenges per iteration |
| **Framework push** | Proactively suggest relevant frameworks |
| **Weak axis focus** | Orient questions toward axes below 60 |
| **Light Devil's Advocate** | Challenge one assumption per iteration |
| **Proactive suggestions** | Offer frameworks even if not requested |

### Coaching Intensity Levels

| Level | Challenges | Framework Push | Devil's Advocate |
|-------|------------|----------------|------------------|
| Light | 1/iteration | On request | None |
| **Moderate** (default) | 2-3/iteration | Proactive | 1 challenge/iteration |
| Intense | Systematic | Very proactive | Constant |

### Disable

Use `--no-coaching` flag for neutral facilitation:
- Questions remain neutral
- No unsolicited challenges
- Frameworks only on request
- Pure facilitation mode

---

## Minimum Score for Finish

### Configuration

Use `--min-score [N]` flag to require minimum EMS before finish.

### Logic

```
IF min_score_finish IS SET AND command == "finish":
  IF current_ems < min_score_finish:
    DISPLAY warning:
    
    "⚠️ Current EMS: [X]/100 (configured threshold: [N])
    
    Axes to improve:
    - [Axis 1] ([score]/100): [suggestion]
    - [Axis 2] ([score]/100): [suggestion]
    
    Options:
    → `continue` — Continue exploration
    → `finish --force` — Generate report despite score"
    
    WAIT for user choice
  ELSE:
    PROCEED with finish
```

---

## Display Formats

### End of Iteration (Full Radar)

```
📊 EMS : 58/100 (+12) ███████████░░░░░░░░░ 

   Clarté       ████████████████░░░░ 78/100 (+5)
   Profondeur   ██████████░░░░░░░░░░ 52/100 (+18) ⚠️
   Couverture   ████████████░░░░░░░░ 62/100 (+8)
   Décisions    ██████░░░░░░░░░░░░░░ 35/100 (+15) ⚠️
   Actionnab.   ████░░░░░░░░░░░░░░░░ 22/100 (=) ⚠️

🌿 Exploration developing

💡 Recommendations:
   → Actionnability critical: Let's define a first concrete action.
   → Decisions lagging: 3 points remain open. Shall we decide on [X]?
```

### Quick Mode (Simplified)

```
📊 EMS : 58/100 (+12) ███████████░░░░░░░░░ 🌿

💡 Focus on: Decisions, Actionability
```

### Journal Evolution Graph

```
Score EMS
100 ┤                                        ┌──● Fin
 90 ┤ · · · · · · · · · · · · · · · · · · · ·│· · · 
 80 ┤                              ╭────────╯
 70 ┤                    ╭────────╯
 60 ┤ · · · · · · · · · ·│· · · · · · · · · · · · · 
 50 ┤          ╭────────╯
 40 ┤    ╭────╯
 30 ┤ · ·│· · · · · · · · · · · · · · · · · · · · · 
 20 ┤───╯
  0 ┼────┴─────┴─────┴─────┴─────┴─────┴
    Init  It.1  It.2  It.3  It.4  It.5
```

---

## Data Structure

### EMS State (for checkpoint)

```yaml
ems_state:
  version: "2.0"
  current_iteration: 4
  coaching_mode: true
  min_score_finish: null  # or integer
  stagnation_count: 0
  
  history:
    - iteration: 0  # Init (after brief validation)
      clarity: 40
      depth: 10
      coverage: 15
      decisions: 10
      actionability: 5
      total: 18
      delta: null
      
    - iteration: 1
      clarity: 60
      depth: 30
      coverage: 40
      decisions: 50
      actionability: 15
      total: 42
      delta: +24
      recommendations: ["Depth needs work", "Coverage partial"]
      
    # ... continues for each iteration
  
  current:
    clarity: 85
    depth: 78
    coverage: 72
    decisions: 80
    actionability: 65
    total: 78
    delta: +8
    weak_axes: ["actionability"]
    threshold_status: "mature"
```

---

## Evaluation Guidelines

### General Principles

1. **Holistic assessment**: Consider the entire conversation, not just last message
2. **Relative to topic complexity**: A simple topic reaches high scores faster
3. **User engagement matters**: Active participation increases scores
4. **Quality over quantity**: Depth beats breadth of discussion
5. **Decisions are progress**: Even "no" decisions count

### Scoring Consistency Tips

- Compare to previous iteration explicitly
- Note specific elements that changed the score
- Consider template expectations (audit needs more coverage, feature needs more actionability)
- Adjust for quick mode (simpler topics, faster progression expected)

### Edge Cases

| Situation | Handling |
|-----------|----------|
| Pivot mid-session | Reset relevant axes partially, preserve others |
| Deep dive | May increase Depth significantly, Coverage temporarily stable |
| User goes off-topic | Coverage may drop, Clarity may drop |
| Framework application | Usually boosts Depth and Coverage |
| Decisions reversed | Decisions axis drops |

---

## Integration Points

### With Bias Detection

If a bias is detected AND an axis is low, the recommendation can reference both:

```
💡 Recommendations:
   → Couverture faible + Confirmation bias detected: 
     We're focusing on supporting evidence. What would challenge our view?
```

### With Frameworks

Framework application typically impacts:
- **SWOT** → Coverage (+10-20), Decisions (+5-10)
- **5 Whys** → Depth (+15-25)
- **Six Hats** → Coverage (+15-25)
- **MoSCoW** → Decisions (+10-20), Actionability (+5-10)
- **Scoring** → Decisions (+10-15)

### With Session Length

| EMS at Iteration 5 | Suggested action |
|-------------------|------------------|
| < 40 | "Still early. Continue or reframe?" |
| 40-60 | "Making progress. A few more iterations?" |
| 60-80 | "Good maturity. Finish when ready." |
| > 80 | "Excellent! Consider finishing." |

---

## Limitations

- Subjective evaluation may vary
- Not designed for inter-session comparison
- Quick mode uses simplified display
- Cannot guarantee exploration quality (aids, not guarantees)
- User can always `finish --force` regardless of score

---

*EMS System v2.0 — Real-time exploration progress tracking*
