# Cognitive Bias Detection

> Patterns, thresholds, and alerts for common thinking traps during brainstorming

---

## Overview

Brainstormer monitors for cognitive biases during iterations. When detected, it provides **soft alerts** — non-intrusive mentions to prompt reflection, not blocks or judgments.

**Alert format**:
```
💭 Bias check: [Bias name] — [Brief explanation]. [Gentle question to reflect]
```

**Core principle**: Alerts are aids for better thinking, not accusations or obstacles.

---

## Alert Thresholds & Rules

### Global Thresholds

| Rule | Value | Rationale |
|------|-------|-----------|
| Minimum iterations before first alert | 3 | Allow warmup, build rapport |
| Maximum alerts per bias type | 1 per session | Avoid nagging |
| Maximum total alerts per session | 3 | Don't overwhelm |
| Pattern matches required to trigger | 2+ | Reduce false positives |
| Cooldown between alerts | 2 iterations | Space out alerts |

### Alert Decision Flow

```
Pattern detected?
       │
       ▼
   ┌───────────────────────┐
   │ Iteration ≥ 3?        │──No──→ Don't alert, log for later
   └───────────────────────┘
       │Yes
       ▼
   ┌───────────────────────┐
   │ This bias already     │──Yes─→ Don't alert (1 per type max)
   │ alerted this session? │
   └───────────────────────┘
       │No
       ▼
   ┌───────────────────────┐
   │ Total alerts < 3?     │──No──→ Don't alert (session limit)
   └───────────────────────┘
       │Yes
       ▼
   ┌───────────────────────┐
   │ Last alert ≥ 2        │──No──→ Don't alert (cooldown)
   │ iterations ago?       │
   └───────────────────────┘
       │Yes
       ▼
   ┌───────────────────────┐
   │ Pattern count ≥ 2?    │──No──→ Don't alert (insufficient evidence)
   └───────────────────────┘
       │Yes
       ▼
     ALERT
```

---

## Detectable Biases

### 1. Confirmation Bias

**Definition**: Seeking information that confirms existing beliefs while ignoring contradictory evidence.

**Detection patterns** (need 2+ to trigger):
| Pattern | Signal Strength |
|---------|-----------------|
| User dismisses contradictory sources without engagement | High |
| Selectively quoting only supporting evidence | High |
| "I knew it" or "See, I was right" reactions | Medium |
| Requesting searches biased toward expected results | Medium |
| Ignoring or minimizing opposing viewpoints | Medium |
| Cherry-picking data points | High |

**Alert example**:
> 💭 Bias check: Confirmation bias — We seem to be focusing on sources that support our initial hypothesis. What evidence might challenge this view?

**Mitigation questions**:
- "What evidence would prove this wrong?"
- "Who would disagree with this, and why?"
- "What are we NOT seeing?"
- "If we had to argue the opposite, what would we say?"

---

### 2. Sunk Cost Fallacy

**Definition**: Continuing a course of action because of past investment, not future value.

**Detection patterns** (need 2+ to trigger):
| Pattern | Signal Strength |
|---------|-----------------|
| "We've already spent X on this" as justification | High |
| "We can't abandon it now after all this work" | High |
| Reluctance to pivot despite new information | Medium |
| Emotional attachment to previous decisions | Medium |
| Comparing against past investment rather than future value | High |
| "It would be a waste to stop now" | High |

**Alert example**:
> 💭 Bias check: Sunk cost — Past investment seems to be influencing our evaluation. If we were starting fresh today with no prior investment, would we make the same choice?

**Mitigation questions**:
- "Ignoring what we've spent, what's the best path forward?"
- "If a new team took over tomorrow, what would they decide?"
- "What would we advise a friend in this exact situation?"

---

### 3. Anchoring Bias

**Definition**: Over-relying on the first piece of information encountered.

**Detection patterns** (need 2+ to trigger):
| Pattern | Signal Strength |
|---------|-----------------|
| First number mentioned becomes persistent reference | High |
| Initial solution dominates despite exploring alternatives | Medium |
| Adjustments from initial estimate are small (<20%) | Medium |
| "The first estimate was X, so..." framing | High |
| Difficulty considering values far from initial anchor | High |
| Returning to initial idea after exploring others | Medium |

**Alert example**:
> 💭 Bias check: Anchoring — The initial estimate of [X] seems to be anchoring our thinking. Could we try building an estimate from completely different assumptions?

**Mitigation questions**:
- "What if we started with a completely different number?"
- "Can we estimate this from multiple independent angles?"
- "What would someone with no context guess?"

---

### 4. Availability Heuristic

**Definition**: Overweighting easily recalled examples (recent, vivid, emotional).

**Detection patterns** (need 2+ to trigger):
| Pattern | Signal Strength |
|---------|-----------------|
| Recent event dominates reasoning disproportionately | High |
| Vivid anecdote outweighs statistical evidence | High |
| "Remember when X happened?" as primary evidence | Medium |
| Personal experience treated as universal truth | Medium |
| News stories influencing probability estimates | Medium |
| Emotional examples given more weight than data | High |

**Alert example**:
> 💭 Bias check: Availability heuristic — That recent incident is vivid in memory. Is it representative of the typical case, or might it be an outlier?

**Mitigation questions**:
- "Is this example typical or exceptional?"
- "What does the broader data show?"
- "Are we generalizing from too few cases?"

---

### 5. Overconfidence Bias

**Definition**: Excessive certainty in one's knowledge or predictions.

**Detection patterns** (need 2+ to trigger):
| Pattern | Signal Strength |
|---------|-----------------|
| Extreme certainty language ("definitely", "100%", "guaranteed") | High |
| Very narrow confidence intervals | High |
| Dismissing uncertainty or downplaying risks | Medium |
| "This will obviously work" without evidence | High |
| Ignoring base rates or historical failure rates | Medium |
| No consideration of alternative outcomes | Medium |

**Alert example**:
> 💭 Bias check: Overconfidence — We seem very certain about this outcome. What's our confidence based on, and what could make us wrong?

**Mitigation questions**:
- "What's our track record on similar predictions?"
- "What's the base rate of success for this type of thing?"
- "If we're wrong, how would we know?"
- "What would a skeptic say?"

---

### 6. Groupthink

**Definition**: Prioritizing consensus over critical evaluation.

**Detection patterns** (need 2+ to trigger):
| Pattern | Signal Strength |
|---------|-----------------|
| Quick agreement without substantive debate | High |
| "Everyone agrees" without exploring individual views | Medium |
| Suppression or dismissal of dissenting thoughts | High |
| Assuming silence equals agreement | Medium |
| "Let's not rock the boat" sentiment | High |
| Pressure toward unanimity | High |

**Alert example**:
> 💭 Bias check: Potential groupthink — We've reached agreement quite quickly. Should we deliberately argue the opposite position to stress-test our reasoning?

**Mitigation questions**:
- "What would a devil's advocate say?"
- "Are there concerns we're not voicing?"
- "What if we had to defend the opposite view?"

---

### 7. Status Quo Bias

**Definition**: Preference for the current state, resistance to change.

**Detection patterns** (need 2+ to trigger):
| Pattern | Signal Strength |
|---------|-----------------|
| "It's always been done this way" as justification | High |
| Change seen as inherently risky without analysis | Medium |
| Asymmetric evaluation (change = risk, status quo = safe) | High |
| "Why fix what isn't broken?" without examining if it's actually working | Medium |
| Undervaluing improvement potential | Medium |
| Requiring higher evidence for change than for staying | High |

**Alert example**:
> 💭 Bias check: Status quo bias — The current approach feels comfortable, but are we fairly evaluating alternatives? What are the hidden costs of NOT changing?

**Mitigation questions**:
- "What if we had to start from zero today?"
- "What are the hidden costs of the current state?"
- "What would a competitor do?"
- "In 5 years, will we regret not changing?"

---

### 8. Planning Fallacy

**Definition**: Underestimating time, costs, and risks; overestimating benefits.

**Detection patterns** (need 2+ to trigger):
| Pattern | Signal Strength |
|---------|-----------------|
| Optimistic timelines without buffer or contingency | High |
| "Best case" treated as expected case | High |
| Historical overruns on similar projects ignored | High |
| "This time will be different" without explaining why | High |
| Ignoring complexity, dependencies, or unknowns | Medium |
| No consideration of what could delay things | Medium |

**Alert example**:
> 💭 Bias check: Planning fallacy — This estimate seems optimistic. Based on similar past projects, what's a realistic timeline including unexpected delays?

**Mitigation questions**:
- "How long did similar projects actually take?"
- "What could cause delays that we're not accounting for?"
- "What's our buffer for unknowns?"
- "What would a pessimistic estimate look like?"

---

## Alert Behavior

### Alert Tone Guidelines

| Do | Don't |
|----|-------|
| "I notice..." | "You're being biased..." |
| "Should we consider..." | "You must..." |
| "This might be worth examining..." | "This is wrong..." |
| Offer mitigation question | Just criticize |
| One sentence + one question | Long explanation |

### User Response Handling

After a bias alert, user can:

| Response | Brainstormer Behavior |
|----------|----------------------|
| Acknowledges and adjusts | Note in journal, continue |
| Explains why not applicable | Accept explanation, note in journal, don't re-alert |
| Requests Devil's Advocate mode | Activate challenge mode for deeper exploration |
| Ignores alert | Don't repeat for this bias, continue normally |
| Seems annoyed | Acknowledge, reduce future alerts, note preference |

### Devil's Advocate Integration

When `--challenge` mode is active:
- **Actively seek** bias patterns to exploit in challenges
- **Present counter-arguments** based on detected biases
- **Force consideration** of opposite viewpoints
- **Use bias detection** to structure pointed questions

**Example in challenge mode**:
> "You seem anchored on the €50k budget. Let's stress-test: What if the true cost is €150k — would this still be worth doing? What if it's only €15k — what would that change about our approach?"

---

## Bias Logging

All bias-related events are logged in the exploration journal:

```markdown
## Bias Detection Log

| Iteration | Bias Type | Patterns Detected | Alert Sent | User Response |
|-----------|-----------|-------------------|------------|---------------|
| 4 | Anchoring | Initial estimate reference (×2) | Yes | Acknowledged, re-estimated |
| 6 | Sunk cost | "Already invested" (×1) | No | Below threshold |
| 7 | Confirmation | Dismissed contrary source (×2) | Yes | Explained context |
```

---

## Limitations

Brainstormer's bias detection does NOT:
- Diagnose psychological conditions
- Claim certainty about bias presence (always "might be", "seems like")
- Override user judgment or refuse to proceed
- Repeatedly alert about the same bias
- Use bias detection to block or slow down the session
- Guarantee bias-free outcomes (alerts are aids, not guarantees)

Bias alerts are **tools for reflection**, helping users think more clearly — not accusations or obstacles.
