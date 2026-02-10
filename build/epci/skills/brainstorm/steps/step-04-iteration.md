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

### 1.5 Extract and Persist Decisions

🔴 **OBLIGATOIRE**: Extraire les décisions des réponses utilisateur et les persister.

```
# Decision markers to detect
DECISION_MARKERS = [
  "decided", "choosing", "going with", "let's do", "we'll use",
  "the approach will be", "I'm choosing", "definitely", "yes, that works"
]

FOR each response in user_responses:
  IF contains_decision_markers(response):
    # Load current session
    session = JSON.parse(Read(session_path))

    # Create decision record
    decision = {
      "id": "D{len(session.decisions) + 1:03d}",
      "text": extract_decision_text(response),
      "iteration": current_iteration,
      "ems_at_time": ems.global,
      "rationale": extract_rationale(response),
      "confidence": assess_confidence(response),  # high/medium/low
      "timestamp": NOW()
    }

    session.decisions.append(decision)
    session.timestamps.last_update = NOW()

    # Persist session
    Write(session_path, JSON.stringify(session, indent=2))

    # Append to incremental decisions file
    append_to_decisions_file(decision, session)

# Check for thread closures
FOR each thread in session.open_threads:
  IF response closes thread:
    thread.status = "closed"
    thread.closed_at_iteration = current_iteration
    # Update decisions file with closed thread
```

**Helper: append_to_decisions_file**

```
def append_to_decisions_file(decision, session):
  decisions_dir = "docs/briefs/{slug}/"
  decisions_path = "{decisions_dir}decisions-{slug}.md"

  # Create directory if needed
  IF NOT directory_exists(decisions_dir):
    Bash("mkdir -p {decisions_dir}")

  IF NOT file_exists(decisions_path):
    # Create file with header (see references/decisions-format.md)
    header = """# Decisions - {session.context.idea_raw}

> Incremental decisions log - Session `{session.session_id}`
> Started: {session.timestamps.created_at}

---

## Summary

| Metric | Value |
|--------|-------|
| **Total decisions** | 0 |
| **Current EMS** | {ems.global}/100 |
| **Current iteration** | {iteration} |
| **Last updated** | {NOW()} |

---

## Decisions Log

---

## Open Threads

| ID | Thread | Opened | Priority | Status | Notes |
|----|--------|--------|----------|--------|-------|

---

*Last updated: {NOW()}*
*Resume with: `/brainstorm --continue {slug}-{timestamp}`*
"""
    Write(decisions_path, header)

  # Read current content
  content = Read(decisions_path)

  # Update summary section
  content = update_summary(content, len(session.decisions), ems.global, iteration)

  # Insert decision entry before "## Open Threads"
  entry = """
### D{decision.id}: {decision.text[:50]}...

| Attribute | Value |
|-----------|-------|
| **Iteration** | {decision.iteration} |
| **EMS at time** | {decision.ems_at_time}/100 |
| **Confidence** | {decision.confidence} |
| **Timestamp** | {decision.timestamp} |

**Decision**: {decision.text}

**Rationale**: {decision.rationale}

---
"""
  content = insert_before_section(content, "## Open Threads", entry)

  # Update timestamp
  content = update_last_updated(content, NOW())

  Write(decisions_path, content)
```

**Confidence Assessment**:

| Confidence | Trigger Words |
|------------|---------------|
| **High** | "definitely", "absolutely", "we must", "decided", "going with" |
| **Medium** | "probably", "likely", "should", "let's try" |
| **Low** | "maybe", "perhaps", "could", "might consider" |

### 2. Recalcul EMS (OBLIGATOIRE - NE PAS SAUTER)

🔴 **CRITIQUE**: Tu DOIS appeler l'agent ems-evaluator à CHAQUE itération.
⛔ **NE PAS** simuler le score manuellement.
⛔ **NE PAS** sauter cette étape.
⛔ **NE PAS** continuer sans le résultat.

**EXÉCUTE IMMÉDIATEMENT**:

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

⏸️ **ATTENDS le résultat avant de continuer.**

**Après réception du résultat EMS**:

```python
# Mise à jour obligatoire de l'historique
ems.history.append({
  "iteration": current_iteration,
  "global": result.global,
  "scores": result.scores,
  "delta": result.delta
})
ems.scores = result.scores
ems.global = result.global
ems.delta = result.delta
ems.weak_axes = result.weak_axes
ems.strong_axes = result.strong_axes
```

### 2.1 Vérification État EMS (OBLIGATOIRE)

**AVANT de continuer**, vérifie:

| Check | Condition | Action si manquant |
|-------|-----------|-------------------|
| `ems.history` | Contient l'itération précédente | ⛔ STOP - Recalcule via ems-evaluator |
| `ems.scores` | 5 axes remplis (clarity, depth, coverage, decisions, actionability) | ⛔ STOP - Recalcule |
| `ems.delta` | Calculé vs itération N-1 | ⛔ STOP - Recalcule |
| `ems.global` | Entre 0-100 | ⛔ STOP - Résultat invalide |

🔴 **SI vérification échoue**: STOP et appelle ems-evaluator AVANT de continuer.

### 2.2 Persist Session State (OBLIGATOIRE)

🔴 **CRITIQUE**: Après CHAQUE recalcul EMS, SAUVEGARDE la session pour éviter toute perte.

```
# Load current session
session = JSON.parse(Read(session_path))

# Update EMS data
session.ems.history.append({
  "iteration": current_iteration,
  "global": ems.global,
  "scores": ems.scores,
  "delta": ems.delta,
  "timestamp": NOW()
})
session.ems.global = ems.global
session.ems.axes = ems.scores

# Update iteration and timestamps
session.iteration = current_iteration
session.timestamps.last_update = NOW()
session.status = "active"

# Update phase and persona if changed
session.phase = phase
session.persona = persona

# Append persona change to history if switched
IF persona != previous_persona:
  session.persona_history.append({
    "persona": persona,
    "iteration": current_iteration,
    "trigger": switch_trigger
  })

# Persist to disk
Write(session_path, JSON.stringify(session, indent=2))

# Log confirmation
DISPLAY: "Session saved (EMS: {ems.global}, iteration {current_iteration})"
```

🔴 **SI Write échoue**: Retry once, then continue with warning.

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

### 10.5 Handle Checkpoint Command

Si l'utilisateur tape `checkpoint`:

```
IF user_input == "checkpoint":
  # Load and update session
  session = JSON.parse(Read(session_path))
  session.status = "paused"
  session.timestamps.last_update = NOW()

  # Persist final state
  Write(session_path, JSON.stringify(session, indent=2))

  # Update decisions file with pause note
  IF file_exists(decisions_path):
    content = Read(decisions_path)
    content = update_last_updated(content, NOW())
    content = append_note(content, "Session paused at iteration {iteration}")
    Write(decisions_path, content)

  # Display checkpoint confirmation
  DISPLAY:
  ┌─────────────────────────────────────────────────────────────────────┐
  │ ✅ CHECKPOINT SAVED                                                  │
  ├─────────────────────────────────────────────────────────────────────┤
  │                                                                     │
  │ Session ID: {session.session_id}                                    │
  │ Current EMS: {session.ems.global}/100                               │
  │ Iteration: {session.iteration}                                      │
  │ Decisions: {len(session.decisions)}                                 │
  │ Open threads: {len(session.open_threads)}                           │
  │                                                                     │
  │ Files saved:                                                        │
  │   • .claude/state/sessions/{session_id}.json                        │
  │   • docs/briefs/{slug}/decisions-{slug}.md                          │
  │                                                                     │
  ├─────────────────────────────────────────────────────────────────────┤
  │ Resume with:                                                        │
  │   /brainstorm --continue {slug}-{timestamp}                         │
  └─────────────────────────────────────────────────────────────────────┘

  → Exit session (no next step)
```

### 10.6 Handle Status Command

Si l'utilisateur tape `status`:

```
IF user_input == "status":
  # Load session
  session = JSON.parse(Read(session_path))

  DISPLAY complete state:
  - Session ID
  - EMS history graph
  - All decisions made
  - Open threads
  - Persona history
  - Files created

  → Continue iteration (no state change)
```

## Loop Conditions

See iteration-rules.md (section #loop-conditions-summary imported above) for complete table.

| Condition | Action |
|-----------|--------|
| User continues | → Self-loop (step-04) |
| User finishes | → `step-05-breakpoint-finish.md` |

## Outputs

| Output | Destination |
|--------|-------------|
| Session JSON (updated) | `.claude/state/sessions/{session_id}.json` |
| Decisions file (incremental) | `docs/briefs/{slug}/decisions-{slug}.md` |
| Updated `ems` | Session state + JSON |
| Updated `phase` | Session state + JSON |
| Updated `persona` | Session state + JSON |
| `decisions[]` | Session state + JSON + decisions.md |
| `open_threads[]` | Session state + JSON + decisions.md |
| `techniques_applied[]` | Session state + JSON |
| `persona_history[]` | Session state + JSON |

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
