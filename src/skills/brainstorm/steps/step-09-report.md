---
name: step-09-report
description: Calculate routing, execute hook, display completion summary
prev_step: steps/step-08-generate.md
next_step: null
---

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

Évalue le brief selon ces critères pour déterminer la complexité:

| Critère | TINY | SMALL | STANDARD | LARGE |
|---------|------|-------|----------|-------|
| Fichiers impactés | 1 | 2-3 | 4-10 | 10+ |
| Durée estimée | <1h | 1-2h | 2-8h | >8h |
| Dépendances | 0 | 1-2 | 3-5 | 6+ |
| Tests requis | Unitaires simples | Unitaires | Int. + Unit. | E2E + Int. + Unit. |

Calcul du score:
```
score_fichiers = map_files_to_score(estimated_files)
score_duree = map_duration_to_score(estimated_duration)
score_deps = map_deps_to_score(dependencies_count)

complexity = weighted_average([
  (score_fichiers, 0.4),
  (score_duree, 0.35),
  (score_deps, 0.25)
])

SI complexity < 25 → TINY
SI complexity < 50 → SMALL
SI complexity < 75 → STANDARD
SINON → LARGE
```

Routing rules:
| Complexity | Routing | Reason |
|------------|---------|--------|
| TINY | `/quick` | Single file, < 1h |
| SMALL | `/quick` | Few files, < 2h |
| STANDARD | `/implement` | Multiple files, requires planning |
| LARGE | `/implement` | Multi-phase, architectural |

### 2. Log Session Completion

```python
# Log session completion data (hooks system not yet implemented)
session_data = {
  "event": "brainstorm-complete",
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

# Note: Hook system (src/hooks/runner.py) not yet implemented
# Data is stored in session state and index.json instead
```

### 3. Store Metrics in Project State (SI DISPONIBLE)

Sauvegarder les métriques pour référence future:

```
SI le dossier `.claude/state/features/` existe:
  Read(".claude/state/features/index.json")

  Ajouter entrée pour cette session (format compatible avec implement):
  {
    "id": "{slug}",
    "status": "brainstorm-complete",
    "current_phase": "brainstorm",
    "complexity": "{complexity_estimate}",
    "branch": null,
    "created_at": "{session_start_timestamp}",
    "last_update": "{ISO8601}",
    "summary": "{brief_summary_1_sentence}",
    "modified_files": ["{brief_path}", "{journal_path}"],
    "test_count": 0,
    "brainstorm_data": {
      "ems_final": {ems.global},
      "iterations": {iteration},
      "techniques": {techniques_applied},
      "duration_minutes": {duration_minutes}
    }
  }

  Write(".claude/state/features/index.json", updated_index)

SINON:
  → Skip metrics storage
  → Log: "project-memory unavailable, skipping metrics storage"
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

### Suggested Next Steps (Manual)

> ℹ️ **Brainstorm is complete.** The commands below are **suggestions only**.
> No implementation will start until you explicitly run one of these commands.

**Complexity**: {complexity_estimate}
**Suggested workflow**: `{routing}`

```bash
# Option 1: Generate specifications first
/spec docs/briefs/{slug}/brief-{slug}-{date}.md

# Option 2: Direct implementation (if TINY/SMALL)
/quick "{summary}" @{brief_path}

# Option 3: Full implementation (if STANDARD/LARGE)
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
  "suggested_routing": {
    "complexity": "{level}",
    "suggested_skill": "{/quick|/implement}",
    "note": "User must explicitly invoke next skill"
  }
}
```

## Outputs

| Output | Destination |
|--------|-------------|
| Session data | Session state (logged, hooks not yet implemented) |
| Metrics | `.claude/state/features/index.json` |
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
