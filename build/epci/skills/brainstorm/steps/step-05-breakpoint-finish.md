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

```
IF ems.global < 60 AND NOT finish --force:
  BREAKPOINT: Low EMS warning

  "EMS is {score}/100, below recommended minimum (60).
   Brief quality may be affected."

  Options:
    - Continue iterating
    - Force finish anyway
    - Save checkpoint
```

### 3. BREAKPOINT: Finish Validation

```typescript
@skill:breakpoint-system
  type: plan-review
  title: "Finish Exploration"
  data: {
    metrics: {
      iterations: {count},
      ems_final: {ems.global},
      decisions_count: {decisions.length},
      open_threads: {open_threads.length},
      techniques_used: {techniques_applied.length}
    },
    summary: {
      key_decisions: [...],
      open_threads: [...],
      ems_progression: "{initial} -> {final} (+{delta})"
    },
    quality_assessment: "{EXCELLENT|GOOD|ADEQUATE|LOW}"
  }
  ask: {
    question: "Ready to generate outputs?",
    header: "Finish",
    options: [
      {label: "Generate outputs (Recommended)", description: "Create brief and journal"},
      {label: "Preview first", description: "See @planner breakdown before finalizing"},
      {label: "Continue iterating", description: "Add more exploration"},
      {label: "Save checkpoint", description: "Pause for later resumption"}
    ]
  }
  suggestions: [
    {pattern: "open_threads", text: "{count} open threads will be noted in brief", priority: "P1"},
    {pattern: "ems", text: "Final EMS {score} - {quality_assessment}", priority: "P2"},
    {pattern: "preview", text: "Preview shows implementation breakdown before commit", priority: "P3"}
  ]
```

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
