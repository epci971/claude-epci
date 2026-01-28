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

## Reference Files Used

| Reference | Purpose |
|-----------|---------|
| [breakpoint-formats.md](../references/breakpoint-formats.md#finish-validation-box) | Finish validation ASCII box template |
| [iteration-rules.md](../references/iteration-rules.md#finalization-thresholds) | Minimum EMS thresholds |
| [ems-system.md](../references/ems-system.md#thresholds-and-messages) | Quality level messages |

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

Apply [low EMS warning thresholds](../references/iteration-rules.md#low-ems-warning):

```
IF ems.global < 60 AND NOT finish --force:
  BREAKPOINT: Low EMS warning

  Options:
    - Continue iterating
    - Force finish anyway
    - Save checkpoint
```

### 3. BREAKPOINT: Finish Validation (OBLIGATOIRE)

AFFICHE le format Finish Validation depuis [references/breakpoint-formats.md](../references/breakpoint-formats.md#finish-validation-box).

Remplis les variables:
- `{count}`, `{ems.global}`, `{decisions.length}`, `{open_threads.length}`
- Key decisions list
- `{initial}` → `{final}` (+`{delta}`)
- Quality assessment from [ems-system.md](../references/ems-system.md#thresholds-and-messages)

APPELLE AskUserQuestion avec les options depuis la référence.

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
