---
name: step-05-breakpoint-finish
description: Validate end of exploration before generation phase
prev_step: steps/step-04-iteration.md
next_step: steps/step-06-preview.md
conditional_next:
  - condition: "Continue iterating"
    step: steps/step-04-iteration.md
  - condition: "Save checkpoint"
    step: null
---

# Step 05: Breakpoint Finish

> Validate end of exploration before generation phase.

## Trigger

- User requested `finish` command
- EMS >= 70 and user accepted finalization
- Max iterations (10) reached
- `--quick` mode and iteration >= 3

## Inputs

| Input | Source | Required |
|-------|--------|----------|
| `ems` | Session state | Yes |
| `iteration` | Session state | Yes |
| `decisions[]` | Session state | Yes |
| `open_threads[]` | Session state | No |
| `brief_v0` | Session state | Yes |
| `hmw_questions` | Session state | No |
| `techniques_applied` | Session state | No |

## Reference Files

@../references/iteration-rules.md
@../references/ems-system.md

| Reference | Purpose |
|-----------|---------|
| iteration-rules.md | Minimum EMS thresholds (section #finalization-thresholds), Low EMS warning (section #low-ems-warning) |
| ems-system.md | Quality level messages (section #thresholds-and-messages) |

*(Breakpoint templates are inline in this file)*

## Protocol

### 0. Anti-Plan-Mode Checkpoint (MANDATORY)

🔴 AVANT de proceder :
- VERIFIE que tu n'es PAS en plan mode natif Claude Code
- L'output cible est `docs/briefs/{slug}/brief-{slug}-{date}.md`
- SI tu detectes une tendance a basculer en plan mode → STOP, continue le workflow brainstorm
- NE JAMAIS appeler EnterPlanMode — ce skill produit un BRIEF, pas un plan natif

### 1. Compile Exploration Summary

```markdown
## Exploration Summary

**Iterations**: {count}
**Final EMS**: {ems.global}/100
**Phase**: {DIVERGENT|CONVERGENT}

### EMS Breakdown
| Axis | Score | Status |
|------|-------|--------|
| Clarity | {score} | {Strong/Adequate/Weak} |
| Depth | {score} | {Strong/Adequate/Weak} |
| Coverage | {score} | {Strong/Adequate/Weak} |
| Decisions | {score} | {Strong/Adequate/Weak} |
| Actionability | {score} | {Strong/Adequate/Weak} |

### Key Decisions Made
1. {decision_1}
2. {decision_2}
...

### Open Threads (if any)
- {thread_1}
- {thread_2}
```

### 2. Check Minimum Quality

Apply low EMS warning thresholds from iteration-rules.md (section #low-ems-warning imported above):

```
IF ems.global < 60 AND NOT finish --force:
  BREAKPOINT: Low EMS warning

  Options:
    - Continue iterating
    - Force finish anyway
    - Save checkpoint
```

### 3. BREAKPOINT: Finish Validation (OBLIGATOIRE)

AFFICHE cette boîte:

┌─────────────────────────────────────────────────────────────────────┐
│ 🏁 FIN D'EXPLORATION                                                │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│ MÉTRIQUES                                                           │
│ • Itérations: {count}                                               │
│ • EMS final: {ems_global}/100                                       │
│ • Décisions prises: {decisions_count}                               │
│ • Threads ouverts: {open_threads_count}                             │
│ • Techniques utilisées: {techniques_count}                          │
│                                                                     │
│ RÉSUMÉ                                                              │
│ Décisions clés:                                                     │
│ • {decision_1}                                                      │
│ • {decision_2}                                                      │
│                                                                     │
│ Progression EMS: {initial} → {final} (+{delta})                     │
│ Évaluation qualité: {quality_assessment}                            │
│                                                                     │
├─────────────────────────────────────────────────────────────────────┤
│ SUGGESTIONS PROACTIVES                                              │
│ [P1] {open_threads_count} threads ouverts seront notés dans brief   │
│ [P2] EMS final {ems_global} — {quality_message}                     │
│ [P3] Preview montre le découpage avant validation                   │
├─────────────────────────────────────────────────────────────────────┤
│ ┌─ Options ──────────────────────────────────────────────────────┐ │
│ │  [A] Générer outputs (Recommended) — Créer brief et journal    │ │
│ │  [B] Preview d'abord — Voir découpage @planner                 │ │
│ │  [C] Continuer itérations — Explorer davantage                 │ │
│ │  [D] Sauvegarder checkpoint — Pause pour reprise               │ │
│ │  [?] Autre réponse...                                          │ │
│ └────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘

**Quality levels**: EXCELLENT (90-100), GOOD (70-89), ADEQUATE (50-69), LOW (<50)

Remplis les variables:
- `{count}`: Total iterations
- `{ems_global}`: Final EMS score
- `{decisions_count}`: Number of decisions
- `{open_threads_count}`: Open threads count
- `{techniques_count}`: Techniques used
- `{decision_1}`, `{decision_2}`: Key decisions
- `{initial}`, `{final}`, `{delta}`: EMS progression
- `{quality_assessment}`: `EXCELLENT`, `GOOD`, `ADEQUATE`, or `LOW`
- `{quality_message}`: Quality feedback message

APPELLE AskUserQuestion({
  questions: [{
    question: "Prêt à générer les outputs?",
    header: "Finish",
    multiSelect: false,
    options: [
      { label: "Générer outputs (Recommended)", description: "Créer brief et journal" },
      { label: "Preview d'abord", description: "Voir découpage @planner avant finalisation" },
      { label: "Continuer itérations", description: "Ajouter plus d'exploration" },
      { label: "Sauvegarder checkpoint", description: "Pause pour reprise ultérieure" }
    ]
  }]
})

⏸️ ATTENDS la réponse utilisateur avant de continuer.

### 4. Handle Open Threads

```
IF open_threads not empty:
  Display open threads summary

  Options:
    - Address now (return to iteration)
    - Note in brief (proceed)
    - Discard (remove from output)
```

### 5. Determine Output Mode

| Flag | Output Mode |
|------|-------------|
| `--quick` | Report only (no journal) |
| Default | Full (brief + journal) |

### 6. Prepare Generation Context

```json
{
  "generation_ready": true,
  "output_mode": "{full|quick}",
  "preview_requested": false,
  "final_ems": {ems},
  "final_decisions": [...],
  "open_threads_to_include": [...],
  "techniques_summary": [...]
}
```

## Outputs

| Output | Destination |
|--------|-------------|
| `generation_ready` | Session state |
| `output_mode` | Session state |
| `preview_requested` | Session state |
| Exploration summary | Session state |

## Next Step

| Condition | Next Step |
|-----------|-----------|
| Generate outputs | → `step-06-preview.md` |
| Preview first | → `step-06-preview.md` (with preview flag) |
| Continue iterating | → `step-04-iteration.md` |
| Save checkpoint | → Exit with session ID |

## Error Handling

| Error | Resolution |
|-------|------------|
| No decisions made | Warn, allow proceed |
| EMS < 40 | Strong warning, require --force |
| Session corrupted | Attempt recovery, offer restart |
