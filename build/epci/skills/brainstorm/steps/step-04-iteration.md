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

## Reference Files Used

| Reference | Purpose |
|-----------|---------|
| [breakpoint-formats.md](../references/breakpoint-formats.md#ems-status-box) | EMS status ASCII box template |
| [iteration-rules.md](../references/iteration-rules.md) | Phase transitions, stagnation, thresholds |
| [ems-system.md](../references/ems-system.md) | EMS calculation and anchors |
| [personas.md](../references/personas.md) | Auto-switch rules |

## Protocol

### 1. Integrate User Responses

```
FOR each response from previous iteration:
  - Extract key information
  - Categorize: decision, insight, constraint, open_thread
  - Update session context
  - Mark addressed questions
```

### 2. Recalculate EMS via Agent ems-evaluator

LANCE l'agent ems-evaluator pour recalculer le score:

```
Task({
  subagent_type: "ems-evaluator",
  model: "haiku",
  prompt: "Calcule l'EMS pour cette session brainstorm.
    État session: {current_state}
    Réponses utilisateur: {user_responses}
    Itération: {current_iteration}
    EMS précédent: {ems}

    Retourne JSON:
    {
      scores: { clarity, depth, coverage, decisions, actionability },
      global: weighted_score,
      delta: change_from_previous,
      weak_axes: [axes avec score < 50],
      strong_axes: [axes avec score >= 70]
    }"
})
```

ATTENDS le résultat avant de continuer. Update EMS history in session state.

### 3. Check Auto-Switch Persona

Check auto-switch conditions from [references/personas.md](../references/personas.md#auto-switch-rules).

If triggered, update `session.active_persona` and signal switch at message start.

### 4. Check Technique Suggestion

```
IF weak_axes not empty AND no_recent_technique:
  LANCE l'agent technique-advisor:

  Task({
    subagent_type: "technique-advisor",
    model: "haiku",
    prompt: "Suggère technique adaptée aux axes faibles: {weak_axes}"
  })

  ATTENDS le résultat.
  BREAKPOINT: Suggérer technique (affiche recommandation)
```

### 5. Check Targeted Perplexity Research

```
IF iter >= 2 AND ems.global < 50 AND weak_axes:
  Generate targeted prompts for weak axes
  BREAKPOINT: Offer targeted research
```

### 6. BREAKPOINT: EMS Status (OBLIGATOIRE)

AFFICHE le format EMS Status depuis [references/breakpoint-formats.md](../references/breakpoint-formats.md#ems-status-box).

Remplis les variables:
- `{iteration}`, `{score}`, `{delta}`
- `{clarity}`, `{depth}`, `{coverage}`, `{decisions}`, `{actionability}`
- `{phase}`, `{persona}`, `{weak_axes}`
- Suggestions P1/P2/P3 basées sur weak_axes

APPELLE AskUserQuestion avec les options depuis la référence.

⏸️ ATTENDS la réponse utilisateur avant de continuer.

### 7. Check Phase Transition

Apply rules from [references/iteration-rules.md](../references/iteration-rules.md#divergent--convergent).

```
IF ems.global >= 50 AND phase == "DIVERGENT":
  BREAKPOINT: Suggest Convergent phase
  IF user accepts: phase = "CONVERGENT", persona = "architecte"
```

### 8. Check Finalization

Apply thresholds from [references/iteration-rules.md](../references/iteration-rules.md#finalization-thresholds).

```
IF ems.global >= 70:
  BREAKPOINT: Propose finish with Preview/@planner/Finalize options
```

### 9. Check Energy (Stagnation/Fatigue)

Apply detection from [references/iteration-rules.md](../references/iteration-rules.md#stagnation-detection).

```
IF stagnation_detected OR iter >= 7:
  BREAKPOINT: Energy checkpoint
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

Apply [quick mode adjustments](../references/iteration-rules.md#quick-mode-adjustments) if `--quick` flag active.

## Loop Conditions

See [references/iteration-rules.md](../references/iteration-rules.md#loop-conditions-summary) for complete table.

| Condition | Action |
|-----------|--------|
| User continues | → Self-loop (step-04) |
| User finishes | → `step-05-breakpoint-finish.md` |

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
