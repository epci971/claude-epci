# Project Memory Integration

## Overview

The orchestrator integrates with `.project-memory/` for:
- Saving execution checkpoints (resume support)
- Recording feature history (velocity tracking)
- Updating orchestration metrics

## Checkpoint System

Checkpoints enable `--continue` flag functionality.

**Location**: `.project-memory/orchestration/checkpoint.json`

```json
{
  "orchestration_id": "orch-2026-01-09-221500",
  "source_dir": "./docs/specs/my-project/",
  "started_at": "2026-01-09T22:15:00Z",
  "current_spec": "S03",
  "completed": ["S01", "S02"],
  "failed": [],
  "skipped": [],
  "config": {
    "max_retries": 3,
    "auto_commit": true
  }
}
```

**Save checkpoint after each spec:**
```python
def save_checkpoint(state):
    path = ".project-memory/orchestration/checkpoint.json"
    atomic_write(path, state)
```

**Resume from checkpoint:**
```python
def resume_orchestration():
    checkpoint = load_checkpoint()
    completed = set(checkpoint['completed'])
    # Skip already completed specs
    for spec in specs:
        if spec.id in completed:
            continue
        execute_spec(spec)
```

## Feature History

Each completed spec is saved to feature history:

**Location**: `.project-memory/history/features/{spec-id}.json`

```json
{
  "slug": "s01-core",
  "title": "Core logic",
  "created_at": "2026-01-09T22:15:00Z",
  "completed_at": "2026-01-09T22:32:00Z",
  "complexity": "STANDARD",
  "actual_time": "17min",
  "estimated_time": "4h",
  "files_modified": ["src/core.py", "tests/test_core.py"],
  "commit_hash": "abc1234",
  "orchestration_id": "orch-2026-01-09-221500",
  "retries": 1
}
```

## Velocity Metrics

After orchestration completes, update velocity:

```python
def update_velocity(results):
    velocity = manager.load_velocity()

    for spec in results['succeeded']:
        complexity = spec['complexity']
        velocity['by_complexity'][complexity]['count'] += 1

    velocity['trend']['last_5_features'] = get_recent_features(5)
    manager.save_velocity(velocity)
```

## Cleanup

After successful orchestration:

```python
def cleanup():
    # Remove checkpoint (no longer needed)
    remove(".project-memory/orchestration/checkpoint.json")

    # Archive journal to history
    archive_journal(journal_path)
```
