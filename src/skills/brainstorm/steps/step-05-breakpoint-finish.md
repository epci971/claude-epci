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

@../references/breakpoint-formats.md
@../references/iteration-rules.md
@../references/ems-system.md

| Reference | Purpose |
|-----------|---------|
| breakpoint-formats.md | Finish validation box (section #finish-validation-box) |
| iteration-rules.md | Minimum EMS thresholds (section #finalization-thresholds), Low EMS warning (section #low-ems-warning) |
| ems-system.md | Quality level messages (section #thresholds-and-messages) |

## Protocol

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

AFFICHE la boîte Finish Validation (section #finish-validation-box du fichier breakpoint-formats.md importé ci-dessus).

Remplis les variables:
- `{count}`, `{ems.global}`, `{decisions.length}`, `{open_threads.length}` depuis session state
- Key decisions list
- `{initial}` → `{final}` (+`{delta}`) depuis EMS history
- Quality assessment depuis ems-system.md (section #thresholds-and-messages imported above)

APPELLE AskUserQuestion:
```json
{
  "question": "Prêt à générer les outputs?",
  "header": "Finish",
  "multiSelect": false,
  "options": [
    { "label": "Générer outputs (Recommended)", "description": "Créer brief et journal" },
    { "label": "Preview d'abord", "description": "Voir découpage @planner avant finalisation" },
    { "label": "Continuer itérations", "description": "Ajouter plus d'exploration" },
    { "label": "Sauvegarder checkpoint", "description": "Pause pour reprise ultérieure" }
  ]
}
```

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
