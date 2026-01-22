# State Manager — API Reference

Detailed API documentation for the state-manager core skill.

## Functions

### `init(feature_slug: string) -> State`

Initialize a new feature state.

**Parameters:**
- `feature_slug`: Unique identifier for the feature (kebab-case)

**Returns:** Initial State object

**Example:**
```typescript
const state = state_manager.init("auth-oauth");
// Creates: .epci/features/auth-oauth/state.json
// Returns: {
//   feature_slug: "auth-oauth",
//   created_at: "2026-01-22T10:00:00Z",
//   updated_at: "2026-01-22T10:00:00Z",
//   status: "in_progress",
//   current_phase: "planning",
//   files_modified: [],
//   context: {}
// }
```

**Side Effects:**
- Creates `.epci/features/{slug}/` directory
- Creates `state.json` file

---

### `load(feature_slug: string) -> State | null`

Load existing feature state.

**Parameters:**
- `feature_slug`: Identifier of the feature to load

**Returns:** State object if exists, `null` otherwise

**Example:**
```typescript
const state = state_manager.load("auth-oauth");
if (state) {
  console.log(`Current phase: ${state.current_phase}`);
}
```

**Error Handling:**
- Returns `null` if feature doesn't exist
- Throws on corrupted JSON

---

### `save(state: State) -> boolean`

Persist current state to disk.

**Parameters:**
- `state`: Complete State object to save

**Returns:** `true` on success, `false` on failure

**Example:**
```typescript
state.context.last_error = "Connection timeout";
const saved = state_manager.save(state);
```

**Behavior:**
- Overwrites existing state file
- Updates `updated_at` timestamp automatically
- Creates backup in `.epci/features/{slug}/backups/`

---

### `update_phase(phase: Phase) -> State`

Update the current implementation phase.

**Parameters:**
- `phase`: One of `"planning"`, `"implementation"`, `"finalization"`

**Returns:** Updated State object

**Example:**
```typescript
state_manager.update_phase("implementation");
// State now shows current_phase: "implementation"
```

**Phase Transitions:**
```
planning → implementation → finalization
    ↑                            │
    └────── (reset on error) ────┘
```

---

### `mark_complete() -> State`

Mark feature as completed.

**Returns:** Final State object with `status: "completed"`

**Example:**
```typescript
const final = state_manager.mark_complete();
// Moves state to .epci/history/auth-oauth/
```

**Side Effects:**
- Changes status to `"completed"`
- Archives state to `.epci/history/`
- Updates project-memory velocity metrics

---

### `create_checkpoint() -> string`

Create a resumption checkpoint.

**Returns:** Checkpoint ID (timestamp-based)

**Example:**
```typescript
const checkpointId = state_manager.create_checkpoint();
// Returns: "20260122-100523"
// Creates: .epci/features/auth-oauth/checkpoints/20260122-100523.json
```

**Use Cases:**
- Before risky operations
- End of work session
- Before asking for user input

---

### `resume_checkpoint(checkpoint_id: string) -> State`

Resume from a saved checkpoint.

**Parameters:**
- `checkpoint_id`: ID returned from `create_checkpoint()`

**Returns:** State as it was at checkpoint time

**Example:**
```typescript
const state = state_manager.resume_checkpoint("20260122-100523");
```

---

## Helper Functions

### `list_features() -> string[]`

List all active features (not completed).

**Returns:** Array of feature slugs

### `get_status(slug: string) -> Status`

Get current status without loading full state.

**Returns:** Status string: `"in_progress"`, `"paused"`, `"completed"`, `"failed"`

### `cleanup_orphaned()`

Remove states for features with no recent activity (> 30 days).

---

## Error Codes

| Code | Meaning | Recovery |
|------|---------|----------|
| `STATE_NOT_FOUND` | Feature state doesn't exist | Call `init()` first |
| `STATE_CORRUPTED` | JSON parse error | Restore from checkpoint |
| `DISK_FULL` | Cannot write state | Free disk space |
| `CONCURRENT_MODIFY` | Race condition detected | Retry operation |
