# State Manager — State Schema

Full schema documentation for feature state objects.

## State Object

```json
{
  "$schema": "https://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["feature_slug", "created_at", "updated_at", "status", "current_phase"],
  "properties": {
    "feature_slug": {
      "type": "string",
      "pattern": "^[a-z0-9-]+$",
      "description": "Unique kebab-case identifier"
    },
    "created_at": {
      "type": "string",
      "format": "date-time",
      "description": "ISO8601 creation timestamp"
    },
    "updated_at": {
      "type": "string",
      "format": "date-time",
      "description": "ISO8601 last update timestamp"
    },
    "status": {
      "type": "string",
      "enum": ["in_progress", "completed", "paused", "failed"],
      "description": "Current feature status"
    },
    "current_phase": {
      "type": "string",
      "enum": ["planning", "implementation", "finalization"],
      "description": "Current workflow phase"
    },
    "files_modified": {
      "type": "array",
      "items": { "type": "string" },
      "description": "List of files modified during implementation"
    },
    "context": {
      "type": "object",
      "description": "Arbitrary context for resumption"
    }
  }
}
```

---

## Status Values

| Status | Meaning | Transitions To |
|--------|---------|----------------|
| `in_progress` | Actively being worked on | `completed`, `paused`, `failed` |
| `paused` | Temporarily stopped | `in_progress`, `failed` |
| `completed` | Successfully finished | (terminal) |
| `failed` | Encountered blocking error | `in_progress` (retry) |

---

## Phase Values

| Phase | Description | Typical Duration |
|-------|-------------|------------------|
| `planning` | Analysis, design, task breakdown | 10-30% of total |
| `implementation` | Writing code, tests | 50-70% of total |
| `finalization` | Documentation, review, commit | 10-20% of total |

---

## Context Object

The `context` field stores arbitrary data for resumption. Common patterns:

### Implementation Context

```json
{
  "context": {
    "current_task": "US-003",
    "tasks_completed": ["US-001", "US-002"],
    "tasks_remaining": ["US-003", "US-004"],
    "last_file": "src/auth/handler.ts",
    "tdd_phase": "GREEN"
  }
}
```

### Error Context

```json
{
  "context": {
    "last_error": "Test timeout",
    "error_file": "tests/auth.test.ts",
    "retry_count": 2,
    "blocked_since": "2026-01-22T10:00:00Z"
  }
}
```

### Checkpoint Context

```json
{
  "context": {
    "checkpoint_reason": "user_request",
    "session_duration": 3600,
    "tokens_used": 45000
  }
}
```

---

## Storage Layout

```
.epci/
├── features/
│   └── {slug}/
│       ├── state.json           # Current state
│       ├── feature-doc.md       # Feature documentation
│       └── checkpoints/
│           ├── 20260122-100523.json
│           └── 20260122-143012.json
│
├── history/
│   └── {slug}/
│       └── final-state.json     # Archived completed state
│
└── config.json                  # Global EPCI configuration
```

---

## Validation Rules

1. **slug format**: Must be kebab-case, 3-50 characters
2. **timestamps**: Must be valid ISO8601 with timezone
3. **files_modified**: Must be relative paths from project root
4. **context size**: Should stay under 10KB for performance

---

## Migration

When schema changes:

1. Check `schema_version` field (default: 1)
2. Run migration function if needed
3. Update `schema_version` after migration

```json
{
  "schema_version": 1,
  "feature_slug": "...",
  ...
}
```
