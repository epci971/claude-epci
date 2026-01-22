# Hooks Reference

> Hook system for extending EPCI workflows.

## Hook Execution

```bash
python3 hooks/runner.py <hook-type> --context '{...}'
```

## Available Hooks

| Hook | Trigger Point | Commands |
|------|--------------|----------|
| `pre-brief` | Before /brief exploration | brief |
| `post-brief` | After complexity evaluation | brief |
| `pre-phase-1` | Before Phase 1 | epci |
| `post-phase-1` | After plan validation | epci |
| `pre-phase-2` | Before coding | epci |
| `post-phase-2` | After code review | epci |
| `post-phase-3` | After completion | epci, quick |
| `on-breakpoint` | At each breakpoint | epci |
| `pre-agent` | Before agent runs | epci |
| `post-agent` | After agent completes | epci |
| `pre-debug` | Before debug | debug |
| `post-diagnostic` | After diagnostic | debug |
| `post-debug` | After debug complete | debug |
| `pre-commit` | Before commit | commit |
| `post-commit` | After commit | commit |

## Context Schema

```json
{
  "phase": "<phase-name>",
  "feature_slug": "<slug>",
  "complexity": "<TINY|SMALL|STANDARD|LARGE>",
  "files_modified": ["<files>"],
  "actual_time": "<duration>",
  "commit_status": "<committed|pending>"
}
```

## Mandatory Hook: post-phase-3

**⚠️ CRITICAL:** Must execute after /epci and /quick to save history.

```bash
python3 hooks/runner.py post-phase-3 --context '{
  "phase": "phase-3",
  "feature_slug": "<slug>",
  "complexity": "<complexity>",
  "files_modified": ["<files>"],
  "estimated_time": "<estimated>",
  "actual_time": "<actual>",
  "commit_hash": "<hash or null>",
  "commit_status": "<committed|pending|cancelled>"
}'
```

**Effects:**
- Saves to `.project-memory/history/features/`
- Updates velocity metrics
- Enables calibration

## Skip Hooks

Use `--no-hooks` flag to disable all hook execution.

## Error Handling

- Default: `fail_on_error: false` — workflow continues with warning
- Hook errors logged but don't block workflow
