# State Manager — Schemas

Complete JSON schemas for EPCI v6.0 state management.

## FeatureState Schema

Full feature state object stored in `.claude/state/features/{slug}/state.json`.

```json
{
  "$schema": "https://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["feature_id", "version", "lifecycle", "spec", "execution", "artifacts"],
  "properties": {
    "feature_id": {
      "type": "string",
      "pattern": "^[a-z0-9-]{3,50}$",
      "description": "Unique kebab-case identifier"
    },
    "version": {
      "type": "integer",
      "const": 1,
      "description": "Schema version for migrations"
    },

    "lifecycle": {
      "type": "object",
      "required": ["status", "current_phase", "created_at", "last_update", "created_by"],
      "properties": {
        "status": {
          "type": "string",
          "enum": ["in_progress", "paused", "completed", "failed"]
        },
        "current_phase": {
          "type": "string",
          "enum": ["explore", "plan", "code", "inspect"]
        },
        "completed_phases": {
          "type": "array",
          "items": { "type": "string" }
        },
        "created_at": {
          "type": "string",
          "format": "date-time"
        },
        "last_update": {
          "type": "string",
          "format": "date-time"
        },
        "created_by": {
          "type": "string",
          "description": "Skill that created the feature"
        },
        "last_updated_by": {
          "type": "string",
          "description": "Skill that last updated"
        }
      }
    },

    "spec": {
      "type": "object",
      "properties": {
        "prd_json": { "type": "string" },
        "prd_md": { "type": "string" },
        "complexity": {
          "type": "string",
          "enum": ["TINY", "SMALL", "STANDARD", "LARGE"]
        },
        "total_tasks": { "type": "integer" },
        "estimated_minutes": { "type": "integer" }
      }
    },

    "execution": {
      "type": "object",
      "properties": {
        "tasks": {
          "type": "object",
          "properties": {
            "completed": { "type": "array", "items": { "type": "string" } },
            "current": { "type": ["string", "null"] },
            "pending": { "type": "array", "items": { "type": "string" } },
            "failed": { "type": "array", "items": { "type": "string" } }
          }
        },
        "iterations": { "type": "integer" },
        "last_error": { "type": ["string", "null"] }
      }
    },

    "artifacts": {
      "type": "object",
      "properties": {
        "feature_doc": { "type": "string" },
        "test_files": { "type": "array", "items": { "type": "string" } },
        "modified_files": { "type": "array", "items": { "type": "string" } }
      }
    },

    "checkpoints": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "id": { "type": "string" },
          "phase": { "type": "string" },
          "timestamp": { "type": "string", "format": "date-time" },
          "git_ref": { "type": "string" },
          "resumable": { "type": "boolean" }
        }
      }
    },

    "improvements": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "description": { "type": "string" },
          "started_at": { "type": "string", "format": "date-time" },
          "completed_at": { "type": ["string", "null"], "format": "date-time" },
          "status": { "type": "string" }
        }
      }
    }
  }
}
```

---

## Index Schema

Central feature registry at `.claude/state/features/index.json`.

```json
{
  "$schema": "https://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["version", "last_update", "features"],
  "properties": {
    "version": {
      "type": "string",
      "const": "1.0"
    },
    "last_update": {
      "type": "string",
      "format": "date-time"
    },
    "features": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["id", "status", "current_phase", "created_at"],
        "properties": {
          "id": { "type": "string" },
          "status": {
            "type": "string",
            "enum": ["in_progress", "paused", "completed", "failed"]
          },
          "current_phase": {
            "type": "string",
            "enum": ["explore", "plan", "code", "inspect"]
          },
          "complexity": {
            "type": "string",
            "enum": ["TINY", "SMALL", "STANDARD", "LARGE"]
          },
          "branch": { "type": "string" },
          "created_at": { "type": "string", "format": "date-time" },
          "last_update": { "type": "string", "format": "date-time" }
        }
      }
    }
  }
}
```

---

## History Schema

Action history log at `.claude/state/features/{slug}/history.json`.

```json
{
  "$schema": "https://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["feature_id", "entries"],
  "properties": {
    "feature_id": { "type": "string" },
    "entries": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["action", "timestamp"],
        "properties": {
          "action": {
            "type": "string",
            "enum": [
              "feature_created",
              "phase_changed",
              "task_started",
              "task_completed",
              "task_failed",
              "checkpoint_created",
              "checkpoint_restored",
              "feature_paused",
              "feature_resumed",
              "feature_completed",
              "feature_failed",
              "improvement_added"
            ]
          },
          "timestamp": { "type": "string", "format": "date-time" },
          "task_id": { "type": "string" },
          "details": { "type": "object" }
        }
      }
    }
  }
}
```

---

## Checkpoint Schema

Checkpoint file at `.claude/state/features/{slug}/checkpoints/{id}.json`.

```json
{
  "$schema": "https://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["id", "phase", "timestamp", "resumable", "state_snapshot"],
  "properties": {
    "id": {
      "type": "string",
      "pattern": "^[a-z]+-[0-9]{8}-[0-9]{6}$",
      "description": "Format: {phase}-{YYYYMMDD}-{HHmmss}"
    },
    "phase": {
      "type": "string",
      "enum": ["explore", "plan", "code", "inspect"]
    },
    "timestamp": {
      "type": "string",
      "format": "date-time"
    },
    "git_ref": {
      "type": "string",
      "description": "Git commit SHA at checkpoint time"
    },
    "resumable": {
      "type": "boolean",
      "default": true
    },
    "state_snapshot": {
      "$ref": "#/definitions/FeatureState",
      "description": "Complete state at checkpoint time"
    }
  }
}
```

---

## Session Schema

Temporary session at `.claude/state/sessions/{id}.json`.

```json
{
  "$schema": "https://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["id", "type", "started_at"],
  "properties": {
    "id": {
      "type": "string",
      "pattern": "^(brainstorm|debug)-[0-9]{8}-[0-9]{6}$"
    },
    "type": {
      "type": "string",
      "enum": ["brainstorm", "debug"]
    },
    "started_at": {
      "type": "string",
      "format": "date-time"
    },
    "ended_at": {
      "type": ["string", "null"],
      "format": "date-time"
    },
    "input": {
      "type": "string",
      "description": "Original user input"
    },
    "iterations": {
      "type": "array",
      "description": "Session iteration data"
    },
    "output": {
      "type": "object",
      "description": "Session output (CDC path, fix details, etc.)"
    }
  }
}
```

---

## Config Schema

Global EPCI configuration at `.claude/state/config.json`.

```json
{
  "$schema": "https://json-schema.org/draft-07/schema#",
  "type": "object",
  "properties": {
    "version": {
      "type": "string",
      "const": "6.0"
    },
    "project_id": {
      "type": "string",
      "description": "Unique project identifier"
    },
    "settings": {
      "type": "object",
      "properties": {
        "auto_checkpoint": {
          "type": "boolean",
          "default": true,
          "description": "Create checkpoint at each phase end"
        },
        "session_cleanup_days": {
          "type": "integer",
          "default": 7,
          "description": "Days before session cleanup"
        },
        "max_checkpoints_per_feature": {
          "type": "integer",
          "default": 10,
          "description": "Maximum checkpoints to keep"
        }
      }
    },
    "created_at": {
      "type": "string",
      "format": "date-time"
    }
  }
}
```

---

## Status Transitions

```
                    ┌──────────────┐
                    │   (start)    │
                    └──────┬───────┘
                           │
                           ▼
                    ┌──────────────┐
        ┌──────────▶│ in_progress  │◀──────────┐
        │           └──────┬───────┘           │
        │                  │                   │
        │      ┌───────────┼───────────┐       │
        │      │           │           │       │
        │      ▼           ▼           ▼       │
        │ ┌────────┐ ┌───────────┐ ┌────────┐  │
        │ │ paused │ │ completed │ │ failed │  │
        │ └────┬───┘ └───────────┘ └────┬───┘  │
        │      │      (terminal)        │      │
        └──────┘                        └──────┘
        (resume)                        (retry)
```

---

## Phase Transitions

```
explore ──▶ plan ──▶ code ──▶ inspect ──▶ (done)
    │         │        │          │
    │         │        │          │
    └─────────┴────────┴──────────┘
            (rollback on failure)
```

---

## Example Files

### state.json

```json
{
  "feature_id": "auth-oauth-google",
  "version": 1,

  "lifecycle": {
    "status": "in_progress",
    "current_phase": "code",
    "completed_phases": ["explore", "plan"],
    "created_at": "2026-01-22T10:00:00Z",
    "last_update": "2026-01-22T14:30:00Z",
    "created_by": "/implement",
    "last_updated_by": "/implement"
  },

  "spec": {
    "prd_json": "docs/specs/auth-oauth-google.prd.json",
    "prd_md": "docs/specs/auth-oauth-google.md",
    "complexity": "STANDARD",
    "total_tasks": 6,
    "estimated_minutes": 180
  },

  "execution": {
    "tasks": {
      "completed": ["US-001", "US-002"],
      "current": "US-003",
      "pending": ["US-004", "US-005", "US-006"],
      "failed": []
    },
    "iterations": 12,
    "last_error": null
  },

  "artifacts": {
    "feature_doc": "docs/features/auth-oauth-google.md",
    "test_files": ["tests/integration/oauth.test.ts"],
    "modified_files": ["src/auth/oauth.ts", "src/auth/types.ts"]
  },

  "checkpoints": [
    {
      "id": "plan-20260122-110000",
      "phase": "plan",
      "timestamp": "2026-01-22T11:00:00Z",
      "git_ref": "abc123",
      "resumable": true
    }
  ],

  "improvements": []
}
```

### index.json

```json
{
  "version": "1.0",
  "last_update": "2026-01-22T15:00:00Z",
  "features": [
    {
      "id": "auth-oauth-google",
      "status": "in_progress",
      "current_phase": "code",
      "complexity": "STANDARD",
      "branch": "feature/auth-oauth-google",
      "created_at": "2026-01-20T10:00:00Z",
      "last_update": "2026-01-22T14:30:00Z"
    },
    {
      "id": "user-profile-edit",
      "status": "completed",
      "current_phase": "inspect",
      "complexity": "SMALL",
      "branch": "feature/user-profile-edit",
      "created_at": "2026-01-15T09:00:00Z",
      "last_update": "2026-01-16T16:00:00Z"
    }
  ]
}
```

### history.json

```json
{
  "feature_id": "auth-oauth-google",
  "entries": [
    {
      "action": "feature_created",
      "timestamp": "2026-01-22T10:00:00Z",
      "details": { "created_by": "/implement", "complexity": "STANDARD" }
    },
    {
      "action": "phase_changed",
      "timestamp": "2026-01-22T10:30:00Z",
      "details": { "from": "explore", "to": "plan" }
    },
    {
      "action": "checkpoint_created",
      "timestamp": "2026-01-22T11:00:00Z",
      "details": { "checkpoint_id": "plan-20260122-110000" }
    },
    {
      "action": "phase_changed",
      "timestamp": "2026-01-22T11:15:00Z",
      "details": { "from": "plan", "to": "code" }
    },
    {
      "action": "task_completed",
      "timestamp": "2026-01-22T12:00:00Z",
      "task_id": "US-001",
      "details": { "files_modified": ["src/auth/oauth.ts"] }
    },
    {
      "action": "task_completed",
      "timestamp": "2026-01-22T13:30:00Z",
      "task_id": "US-002",
      "details": { "files_modified": ["src/auth/types.ts"] }
    }
  ]
}
```
