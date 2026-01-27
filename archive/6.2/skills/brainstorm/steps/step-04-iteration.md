# Step 04: Iteration

> Main exploration loop with EMS tracking, persona switching, and techniques.

## Trigger

- Previous step: `step-03-breakpoint-framing.md` completed
- Or: Self-loop from previous iteration
- Or: Resume from `--continue` flag

## Inputs

| Input | Source | Required |
|-------|--------|----------|
| `iteration` | Session state | Yes |
| `ems` | Session state | Yes |
| `phase` | Session state | Yes |
| `persona` | Session state | Yes |
| `user_responses` | Previous iteration | No |
| `--quick` flag | From step-00 | No |

## Protocol

### 1. Integrate User Responses

```
FOR each response from previous iteration:
  - Extract key information
  - Categorize: decision, insight, constraint, open_thread
  - Update session context
  - Mark addressed questions
```

### 2. Recalculate EMS via @ems-evaluator

```python
@agent:ems-evaluator (Haiku)
  input: {
    session_state: current_state,
    responses: user_responses,
    iteration: current_iteration,
    previous_ems: ems
  }
  output: {
    scores: { clarity, depth, coverage, decisions, actionability },
    global: weighted_score,
    delta: change_from_previous,
    weak_axes: [axes with score < 50],
    strong_axes: [axes with score >= 70]
  }
```

Update EMS history:
```json
{
  "ems": {
    "global": 52,
    "axes": {...},
    "history": [
      {"iteration": 1, "global": 35, "delta": 15},
      {"iteration": 2, "global": 52, "delta": 17}
    ]
  }
}
```

### 3. Check Auto-Switch Persona

| Condition | Switch To | Signal |
|-----------|-----------|--------|
| Unsubstantiated certainty ("obviously", "definitely") | Sparring [!] | "[!] [Challenge] Wait - you said 'obviously'..." |
| EMS stagnation (< 5 pts x 2 iter) | Pragmatique [>] | "[>] [Action] We're stuck. Let's make a decision." |
| iter >= 6 without decisions | Pragmatique [>] | "[>] [Action] Time to converge." |
| Synthesis needed (coverage high, decisions low) | Architecte [#] | "[#] [Structure] Let's organize what we have." |
| Open exploration (low clarity) | Maieuticien [?] | "[?] [Exploration] Tell me more about..." |
| Manual override via `mode` command | Requested | "[X] [Mode] Switching as requested." |

### 4. Check Technique Suggestion

```python
IF weak_axes not empty AND no_recent_technique:
  @agent:technique-advisor (Haiku)
    input: {
      weak_axes: [...],
      template: current_template,
      iteration: current_iteration
    }
    output: {
      technique: "5-whys",
      description: "...",
      how_to_apply: "..."
    }

  BREAKPOINT: Suggest technique
```

### 5. Check Targeted Perplexity Research

```
IF iter >= 2 AND ems.global < 50 AND weak_axes:
  Generate targeted prompts for weak axes:

  FOR axis in weak_axes:
    prompt = generate_perplexity_prompt(axis, brief)

  BREAKPOINT: Offer targeted research
```

### 6. BREAKPOINT: EMS Status

```typescript
@skill:epci:breakpoint-system
  type: ems-status
  title: "Iteration {iteration} Status"
  data: {
    ems: {
      global: {score},
      axes: {
        clarity: {score},
        depth: {score},
        coverage: {score},
        decisions: {score},
        actionability: {score}
      },
      delta: {change},
      weak_axes: [...],
      history: [...]
    },
    phase: "{DIVERGENT|CONVERGENT}",
    persona: "{current_persona}",
    iteration: {n},
    max_iterations: 10,
    technique_suggested: "{technique or null}",
    persona_switch: "{new_persona or null}"
  }
  ask: {
    question: "How would you like to continue?",
    header: "EMS {score}",
    options: [
      {label: "Continue", description: "Answer questions and iterate"},
      {label: "Dive [topic]", description: "Deep dive on specific point"},
      {label: "Pivot", description: "Reorient toward emerging subject"},
      {label: "Finish", description: "Generate outputs now"}
    ]
  }
  suggestions: [
    {pattern: "weak", text: "Focus on {weak_axis} - currently lowest", priority: "P1"},
    {pattern: "technique", text: "Try {technique} to unblock {axis}", priority: "P2"},
    {pattern: "checkpoint", text: "Consider saving checkpoint if pausing", priority: "P3"}
  ]
```

### 7. Check Phase Transition (EMS = 50)

```
IF ems.global >= 50 AND phase == "DIVERGENT":
  BREAKPOINT: Suggest Convergent phase

  IF user accepts:
    phase = "CONVERGENT"
    persona = "architecte" (default for convergent)
```

### 8. Check Finalization (EMS >= 70)

```
IF ems.global >= 70:
  BREAKPOINT: Propose finish

  Options:
    - Continue (iterate more)
    - Preview (@planner)
    - Finalize (generate outputs)
```

### 9. Check Energy (Stagnation/Fatigue)

```
IF (delta < 3 for 2 consecutive iterations) OR (iter >= 7):
  BREAKPOINT: Energy checkpoint

  Options:
    - Continue (push through)
    - Pause (save checkpoint for later)
    - Accelerate (finish with current EMS)
    - Pivot (change direction)
```

### 10. Generate Iteration Questions (3 max)

Based on weak axes and current phase:

```markdown
## Questions (Iteration {n})

**[Critical]** {question targeting weakest axis}
-> Suggestion: {hint}

**[Important]** {question for second weak axis}
-> Suggestion: {hint}

**[Info]** {exploratory question}
-> Suggestion: {hint}
```

```
IF --quick mode:
  → Limit to 2 questions
  → Skip [Info] category
```

## Loop Conditions

| Condition | Action |
|-----------|--------|
| User continues | → Self-loop (step-04) |
| User finishes | → `step-05-breakpoint-finish.md` |
| EMS >= 70 + user accepts | → `step-05-breakpoint-finish.md` |
| Max iterations (10) | → `step-05-breakpoint-finish.md` |
| `checkpoint` command | → Save session, exit |
| `--quick` + iter >= 3 | → Suggest finish |

## Outputs

| Output | Destination |
|--------|-------------|
| Updated `ems` | Session state |
| Updated `phase` | Session state |
| Updated `persona` | Session state |
| `decisions[]` | Session state |
| `open_threads[]` | Session state |
| `techniques_applied[]` | Session state |

## Next Step

| Condition | Next Step |
|-----------|-----------|
| Continue iteration | → `step-04-iteration.md` (self) |
| Finish requested | → `step-05-breakpoint-finish.md` |
| Checkpoint saved | → Exit with session ID |

## Error Handling

| Error | Resolution |
|-------|------------|
| @ems-evaluator failure | Manual estimation, continue |
| @technique-advisor unavailable | Suggest default (Six Hats) |
| EMS stagnation (3 iter < 3 pts) | Force technique or pivot |
