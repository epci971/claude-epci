# Hooks Integration

## Overview

The orchestrator supports hooks at key lifecycle points for
custom automation, notifications, and integrations.

## Hook Points

| Hook | Trigger | Typical Use |
|------|---------|-------------|
| `pre-orchestrate` | Before execution loop | Validate env, notify start |
| `post-spec` | After each spec | Update tracker, progress |
| `post-orchestrate` | After all specs | Notify, deploy, report |

## Hook Context

### pre-orchestrate

```json
{
  "hook_type": "pre-orchestrate",
  "orchestration_id": "orch-2026-01-09-221500",
  "source_dir": "./docs/specs/my-project/",
  "specs_count": 5,
  "specs": ["S01", "S02", "S03", "S04", "S05"],
  "config": {
    "max_retries": 3,
    "auto_commit": true
  }
}
```

### post-spec

```json
{
  "hook_type": "post-spec",
  "orchestration_id": "orch-2026-01-09-221500",
  "spec_id": "S01",
  "spec_title": "Core logic",
  "status": "success",
  "duration_sec": 1020,
  "retries": 1,
  "commit_sha": "abc1234",
  "routing": "epci",
  "complexity": "STANDARD"
}
```

### post-orchestrate

```json
{
  "hook_type": "post-orchestrate",
  "orchestration_id": "orch-2026-01-09-221500",
  "completed_at": "2026-01-09T23:10:00Z",
  "summary": {
    "total_specs": 5,
    "succeeded": 3,
    "failed": 1,
    "skipped": 1,
    "total_duration_sec": 3300,
    "commits": ["abc1234", "def5678", "ghi9012"]
  },
  "journal_path": "./docs/specs/my-project/orchestration-journal.md",
  "report_path": "./docs/specs/my-project/orchestration-report.md"
}
```

## Invocation

Hooks are invoked using the standard hook runner:

```bash
python3 src/hooks/runner.py post-spec --context '{
  "hook_type": "post-spec",
  "spec_id": "S01",
  "status": "success",
  ...
}'
```

## Example Hooks

### Slack Notification (post-orchestrate)

```python
# hooks/active/post-orchestrate-slack.py
import json
import requests

def run(context):
    summary = context['summary']
    message = f"Orchestration complete: {summary['succeeded']}/{summary['total_specs']} specs"

    requests.post(SLACK_WEBHOOK, json={
        "text": message,
        "attachments": [
            {"color": "good" if summary['failed'] == 0 else "warning"}
        ]
    })
```

### Progress Tracker (post-spec)

```python
# hooks/active/post-spec-tracker.py
def run(context):
    # Update external tracker (Jira, Linear, etc.)
    update_ticket(
        ticket_id=context['spec_id'],
        status='Done' if context['status'] == 'success' else 'Failed'
    )
```

## Disabling Hooks

```bash
# Run without any hooks
/orchestrate ./specs/ --no-hooks
```
