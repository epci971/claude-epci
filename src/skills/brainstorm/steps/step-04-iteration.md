---
name: step-04-iteration
description: Main exploration loop with EMS tracking, persona switching, and techniques
prev_step: steps/step-03-breakpoint-framing.md
next_step: steps/step-05-breakpoint-finish.md
conditional_next:
  - condition: "Continue iteration"
    step: steps/step-04-iteration.md
  - condition: "Checkpoint saved"
    step: null
---

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

## Reference Files

@../references/iteration-rules.md
@../references/ems-system.md
@../references/personas.md

| Reference | Purpose |
|-----------|---------|
| iteration-rules.md | Phase transitions, stagnation, thresholds |
| ems-system.md | EMS calculation and anchors |
| personas.md | Auto-switch rules |

*(Breakpoint templates are inline in this file)*

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

LANCE Task({
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

ATTENDS le résultat avant de continuer. Update EMS history in session state.

### 3. Check Auto-Switch Persona

Check auto-switch conditions from personas.md (section #auto-switch-rules imported above).

If triggered, update `session.active_persona` and signal switch at message start.

### 4. Check Technique Suggestion

```
IF weak_axes not empty AND no_recent_technique:
  LANCE l'agent technique-advisor:

  LANCE Task({
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

AFFICHE cette boîte:

┌─────────────────────────────────────────────────────────────────────┐
│ 📊 STATUT ITÉRATION {iteration}                                     │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│ EMS GLOBAL: {score}/100 ({delta})                                   │
│                                                                     │
│ AXES EMS                                                            │
│ ┌─────────────────────────────────────────────────────────────────┐ │
│ │ Clarté        [{bar_clarity}] {clarity}/100                     │ │
│ │ Profondeur    [{bar_depth}] {depth}/100                         │ │
│ │ Couverture    [{bar_coverage}] {coverage}/100                   │ │
│ │ Décisions     [{bar_decisions}] {decisions}/100                 │ │
│ │ Actionnabilité[{bar_actionability}] {actionability}/100         │ │
│ └─────────────────────────────────────────────────────────────────┘ │
│                                                                     │
│ Phase: {phase} | Persona: {persona}                                 │
│ Itération: {iteration}/10 | Technique suggérée: {technique}         │
│ Axes faibles: {weak_axes}                                           │
│                                                                     │
├─────────────────────────────────────────────────────────────────────┤
│ SUGGESTIONS PROACTIVES                                              │
│ [P1] Focus sur {weak_axis} — actuellement le plus bas               │
│ [P2] Essaie {technique} pour débloquer {axis}                       │
│ [P3] Considère sauvegarder checkpoint si pause                      │
├─────────────────────────────────────────────────────────────────────┤
│ ┌─ Options ──────────────────────────────────────────────────────┐ │
│ │  [A] Continuer (Recommended) — Répondre et itérer              │ │
│ │  [B] Dive [sujet] — Approfondir un point                       │ │
│ │  [C] Pivoter — Réorienter                                      │ │
│ │  [D] Finir — Générer les outputs maintenant                    │ │
│ │  [?] Autre réponse...                                          │ │
│ └────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘

**Progress bar format**: `[████████░░] 80/100` (█ = filled, ░ = empty)

Remplis les variables:
- `{iteration}`: Current iteration number
- `{score}`: EMS global score
- `{delta}`: Change from previous (e.g., `+12`)
- `{clarity}`, `{depth}`, `{coverage}`, `{decisions}`, `{actionability}`: Axis scores from ems-evaluator
- `{bar_*}`: Progress bars (10 chars each)
- `{phase}`: `DIVERGENT` or `CONVERGENT`
- `{persona}`: Active persona (e.g., `architecte`)
- `{technique}`: Suggested technique or `-`
- `{weak_axes}`: Axes with score < 50

APPELLE AskUserQuestion({
  questions: [{
    question: "Comment voulez-vous continuer?",
    header: "EMS {score}",
    multiSelect: false,
    options: [
      { label: "Continuer (Recommended)", description: "Répondre aux questions et itérer" },
      { label: "Dive [sujet]", description: "Approfondir un point spécifique" },
      { label: "Pivoter", description: "Réorienter vers un sujet émergent" },
      { label: "Finir", description: "Générer les outputs maintenant" }
    ]
  }]
})

⏸️ ATTENDS la réponse utilisateur avant de continuer.

### 7. Check Phase Transition

Apply rules from iteration-rules.md (section #divergent--convergent imported above).

```
IF ems.global >= 50 AND phase == "DIVERGENT":
  BREAKPOINT: Suggest Convergent phase
  IF user accepts: phase = "CONVERGENT", persona = "architecte"
```

### 8. Check Finalization

Apply thresholds from iteration-rules.md (section #finalization-thresholds imported above).

```
IF ems.global >= 70:
  BREAKPOINT: Propose finish with Preview/@planner/Finalize options
```

### 9. Check Energy (Stagnation/Fatigue)

Apply detection from iteration-rules.md (section #stagnation-detection imported above).

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

Apply quick mode adjustments from iteration-rules.md (section #quick-mode-adjustments imported above) if `--quick` flag active.

## Loop Conditions

See iteration-rules.md (section #loop-conditions-summary imported above) for complete table.

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
