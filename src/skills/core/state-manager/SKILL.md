---
name: state-manager
description: >-
  Manages feature state persistence across sessions for EPCI workflows.
  Tracks implementation progress, current phase, and resumption context.
  Use when: starting new feature (/implement), resuming paused work,
  saving checkpoints, or tracking multi-session implementations.
  Internal component for EPCI v6.0.
user-invocable: false
disable-model-invocation: false
allowed-tools: Read, Write, Glob
---

# State Manager

Internal component for feature state persistence across sessions.

## Overview

Enable resumable workflows by persisting:
- Current phase and step
- Files modified
- Pending tasks
- Context for resumption

## API

| Function | Description | Input | Output |
|----------|-------------|-------|--------|
| `init(feature_slug)` | Initialize new feature state | slug: string | State object |
| `load(feature_slug)` | Load existing state | slug: string | State object or null |
| `save(state)` | Persist current state | state: State | Success boolean |
| `update_phase(phase)` | Update current phase | phase: string | Updated state |
| `mark_complete()` | Mark feature as done | - | Final state |
| `create_checkpoint()` | Save resumption point | - | Checkpoint ID |

## State Schema

See `src/schemas/feature-state-v1.json` for full schema.

```json
{
  "feature_slug": "string",
  "created_at": "ISO8601",
  "updated_at": "ISO8601",
  "status": "in_progress | completed | paused | failed",
  "current_phase": "planning | implementation | finalization",
  "files_modified": ["string"],
  "context": {}
}
```

## Storage Location

States stored in `.epci/features/<slug>/state.json`

## Usage

Invoked automatically by skills when:
- `/implement` starts a new feature (creates state)
- `/quick` needs progress tracking (optional)
- `/improve` updates existing feature state
- Any skill needs to resume from checkpoint

## Implementation

```
state_manager.init("auth-oauth")
  → Creates .epci/features/auth-oauth/state.json
  → Returns initial state object

state_manager.update_phase("implementation")
  → Updates current_phase in state
  → Saves to disk

state_manager.create_checkpoint()
  → Saves current state to checkpoints/
  → Returns checkpoint ID for later resume
```

## Limitations

This component does NOT:
- Handle cross-project state sharing
- Provide real-time sync (file-based)
- Manage database connections
