# Step 09: Report

> Calculate routing, execute hook, display completion summary.

## Trigger

- Previous step: `step-08-generate.md` completed
- Files written to disk

## Inputs

| Input | Source | Required |
|-------|--------|----------|
| `output_files` | From step-08 | Yes |
| `ems` | Session state | Yes |
| `complexity_estimate` | From step-06 | Yes |
| `slug` | From step-08 | Yes |
| `iteration` | Session state | Yes |
| `techniques_applied` | Session state | No |
| `session_id` | Session state | Yes |

## Protocol

### 1. Calculate Complexity Routing

```python
@skill:complexity-calculator
  input: {
    brief: brief_final,
    ems: ems,
    codebase_context: codebase_analysis
  }
  output: {
    complexity: "TINY|SMALL|STANDARD|LARGE",
    routing: "/quick|/implement",
    confidence: 0.85,
    factors: [...]
  }
```

Routing rules:
| Complexity | Routing | Reason |
|------------|---------|--------|
| TINY | `/quick` | Single file, < 1h |
| SMALL | `/quick` | Few files, < 2h |
| STANDARD | `/implement` | Multiple files, requires planning |
| LARGE | `/implement` | Multi-phase, architectural |

### 2. Execute Hook: post-brainstorm

```python
hook_data = {
  "hook": "post-brainstorm",
  "timestamp": datetime.now().isoformat(),
  "data": {
    "feature_slug": slug,
    "ems_score": ems["global"],
    "ems_axes": ems["axes"],
    "iterations": iteration,
    "duration_minutes": calculate_duration(),
    "phase_final": phase,
    "techniques_applied": techniques_applied,
    "personas_used": unique_personas_used(),
    "template": template,
    "output_files": output_files
  }
}

# Execute hook
Bash("python src/hooks/runner.py post-brainstorm --context '{json}'")
```

### 3. Store Metrics in project-memory

```python
@skill:project-memory
  store_feature_metrics(
    slug=slug,
    ems_final=ems["global"],
    iterations=iteration,
    techniques=techniques_applied,
    duration=duration_minutes
  )
```

### 4. Clean Up Session

```python
IF session completed successfully:
  # Archive session file
  mv .claude/state/sessions/brainstorm-{slug}-{ts}.json \
     .claude/state/archive/brainstorm-{slug}-{ts}.json

  # Or mark as completed
  session["status"] = "completed"
```

### 5. Display Completion Summary

```markdown
## Brainstorm Complete

### Session Summary
| Metric | Value |
|--------|-------|
| **Session ID** | {session_id} |
| **Iterations** | {count} |
| **Duration** | {minutes} min |
| **Final EMS** | {ems.global}/100 |

### EMS Radar
```
      Clarity
         {score}
          /\
         /  \
Actionability --- Depth
  {score}    {score}
         \  /
          \/
   Decisions --- Coverage
     {score}     {score}
```

### Generated Files
- `{brief_path}`
- `{journal_path}` (if not --quick)

### Recommended Next Steps

**Complexity**: {complexity_estimate}
**Recommended workflow**: `{routing}`

```bash
# Option 1: Generate specifications
/spec docs/briefs/{slug}/brief-{slug}-{date}.md

# Option 2: Direct implementation (if TINY/SMALL)
/quick "{summary}" @{brief_path}

# Option 3: Full implementation
/implement {slug} @{brief_path}
```

### Quick Commands
- Resume this session: `/brainstorm --continue {session_id}`
- View brief: `cat {brief_path}`
- View journal: `cat {journal_path}`
```

### 6. Final State

```json
{
  "status": "completed",
  "completion_time": "{timestamp}",
  "output_files": [...],
  "routing": {
    "complexity": "{level}",
    "recommended_skill": "{/quick|/implement}",
    "next_command": "/spec {brief_path}"
  }
}
```

## Outputs

| Output | Destination |
|--------|-------------|
| Hook execution | `src/hooks/runner.py` |
| Metrics | `project-memory` |
| Session archive | `.claude/state/archive/` |
| Completion summary | User display |

## Next Step

→ **Session Complete**

Suggested user actions:
1. `/spec {brief_path}` - Generate technical specs
2. `/quick "{summary}"` - Quick implementation (TINY/SMALL)
3. `/implement {slug}` - Full implementation (STANDARD/LARGE)

## Error Handling

| Error | Resolution |
|-------|------------|
| Hook execution fails | Log warning, continue |
| project-memory unavailable | Skip metrics storage |
| Archive fails | Leave session in place |
