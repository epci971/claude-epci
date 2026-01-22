# State Manager — API Reference

Complete API documentation for the state-manager core skill (EPCI v6.0).

## Feature Functions

### `createFeature(slug: string, spec: SpecOutput) -> FeatureState`

Initialize a new feature state with spec context.

**Parameters:**
- `slug`: Unique identifier for the feature (kebab-case, 3-50 chars)
- `spec`: Specification output from `/spec` containing PRD references

**Returns:** Initial FeatureState object

**Example:**
```typescript
const state = state_manager.createFeature("auth-oauth", {
  prd_json: "docs/specs/auth-oauth.prd.json",
  prd_md: "docs/specs/auth-oauth.md",
  complexity: "STANDARD",
  total_tasks: 6,
  estimated_minutes: 180
});
```

**Side Effects:**
- Creates `.claude/state/features/{slug}/` directory
- Creates `state.json` with initial state
- Creates empty `history.json`
- Creates `checkpoints/` directory
- Updates `.claude/state/features/index.json`

---

### `loadFeature(slug: string) -> FeatureState | null`

Load existing feature state.

**Parameters:**
- `slug`: Identifier of the feature to load

**Returns:** FeatureState object if exists, `null` otherwise

**Example:**
```typescript
const state = state_manager.loadFeature("auth-oauth");
if (state) {
  console.log(`Phase: ${state.lifecycle.current_phase}`);
  console.log(`Tasks remaining: ${state.execution.tasks.pending.length}`);
}
```

**Error Handling:**
- Returns `null` if feature doesn't exist
- Throws `STATE_CORRUPTED` on invalid JSON

---

### `updateFeature(slug: string, updates: Partial<FeatureState>) -> void`

Apply partial updates to feature state.

**Parameters:**
- `slug`: Feature identifier
- `updates`: Partial state object with fields to update

**Example:**
```typescript
// Update phase
state_manager.updateFeature("auth-oauth", {
  lifecycle: {
    current_phase: "implementation",
    last_update: new Date().toISOString(),
    last_updated_by: "/implement"
  }
});

// Mark task completed
state_manager.updateFeature("auth-oauth", {
  execution: {
    tasks: {
      completed: [...state.execution.tasks.completed, "US-001"],
      current: "US-002",
      pending: state.execution.tasks.pending.slice(1)
    }
  }
});
```

**Behavior:**
- Deep merges updates with existing state
- Auto-updates `lifecycle.last_update` timestamp
- Appends update action to history.json
- Updates index.json if status/phase changed

---

### `listFeatures(filter?: FeatureFilter) -> FeatureSummary[]`

List features with optional filtering.

**Parameters:**
- `filter`: Optional filter object
  - `status`: Filter by status (`in_progress`, `paused`, `completed`, `failed`)
  - `complexity`: Filter by complexity (`TINY`, `SMALL`, `STANDARD`, `LARGE`)

**Returns:** Array of FeatureSummary objects

**Example:**
```typescript
// All active features
const active = state_manager.listFeatures({ status: "in_progress" });

// All features
const all = state_manager.listFeatures();

active.forEach(f => {
  console.log(`${f.id}: ${f.current_phase} (${f.complexity})`);
});
```

**FeatureSummary Schema:**
```typescript
interface FeatureSummary {
  id: string;
  status: Status;
  current_phase: Phase;
  complexity: Complexity;
  branch?: string;
  created_at: string;
  last_update: string;
}
```

---

## Checkpoint Functions

### `createCheckpoint(slug: string, phase: Phase) -> Checkpoint`

Create a resumption checkpoint at current state.

**Parameters:**
- `slug`: Feature identifier
- `phase`: Current phase name for checkpoint naming

**Returns:** Checkpoint object with ID

**Example:**
```typescript
const checkpoint = state_manager.createCheckpoint("auth-oauth", "plan");
console.log(`Checkpoint: ${checkpoint.id}`);
// Output: "plan-20260122-100523"
```

**Checkpoint Schema:**
```typescript
interface Checkpoint {
  id: string;                    // "{phase}-{timestamp}"
  phase: Phase;                  // Phase when created
  timestamp: string;             // ISO8601
  git_ref?: string;              // Git commit SHA if available
  resumable: boolean;            // Always true for new checkpoints
  state_snapshot: FeatureState;  // Full state at checkpoint time
}
```

**Storage:** `.claude/state/features/{slug}/checkpoints/{id}.json`

---

### `listCheckpoints(slug: string) -> Checkpoint[]`

Get all checkpoints for a feature.

**Parameters:**
- `slug`: Feature identifier

**Returns:** Array of Checkpoint objects, sorted by timestamp (oldest first)

**Example:**
```typescript
const checkpoints = state_manager.listCheckpoints("auth-oauth");
checkpoints.forEach(cp => {
  console.log(`${cp.id} - ${cp.phase} (${cp.timestamp})`);
});
```

---

### `restoreCheckpoint(checkpointId: string) -> FeatureState`

Restore feature state from a checkpoint.

**Parameters:**
- `checkpointId`: Full checkpoint ID (e.g., "plan-20260122-100523")

**Returns:** Restored FeatureState

**Example:**
```typescript
// After a failed implementation attempt
const state = state_manager.restoreCheckpoint("plan-20260122-100523");
console.log(`Restored to phase: ${state.lifecycle.current_phase}`);
```

**Side Effects:**
- Overwrites current state.json with checkpoint state
- Appends "checkpoint_restored" to history.json
- Does NOT delete the checkpoint (can restore again)

---

## History Functions

### `appendHistory(slug: string, entry: HistoryEntry) -> void`

Log an action to feature history.

**Parameters:**
- `slug`: Feature identifier
- `entry`: History entry to append

**Example:**
```typescript
state_manager.appendHistory("auth-oauth", {
  action: "task_completed",
  task_id: "US-001",
  timestamp: new Date().toISOString(),
  details: { files_modified: ["src/auth/handler.ts"] }
});
```

**HistoryEntry Schema:**
```typescript
interface HistoryEntry {
  action: string;        // Action type identifier
  timestamp: string;     // ISO8601
  task_id?: string;      // Related task if applicable
  details?: object;      // Additional action-specific data
}
```

**Common Actions:**
- `feature_created`
- `phase_changed`
- `task_started`
- `task_completed`
- `task_failed`
- `checkpoint_created`
- `checkpoint_restored`
- `feature_completed`
- `improvement_added`

---

### `getHistory(slug: string) -> HistoryEntry[]`

Get complete action history for a feature.

**Parameters:**
- `slug`: Feature identifier

**Returns:** Array of HistoryEntry objects, chronologically ordered

**Example:**
```typescript
const history = state_manager.getHistory("auth-oauth");
const taskActions = history.filter(h => h.action.startsWith("task_"));
console.log(`Task events: ${taskActions.length}`);
```

---

## Session Functions

### `saveSession(sessionId: string, data: SessionData) -> void`

Persist a temporary session (brainstorm, debug).

**Parameters:**
- `sessionId`: Unique session identifier (format: `{type}-{timestamp}`)
- `data`: Session data object

**Example:**
```typescript
state_manager.saveSession("brainstorm-20260122-143052", {
  type: "brainstorm",
  started_at: "2026-01-22T14:30:52Z",
  input: "I want to add OAuth to my app",
  iterations: [
    { ems_score: 45, findings: [...] },
    { ems_score: 67, findings: [...] }
  ],
  output: { cdc_path: "docs/specs/auth-oauth-cdc.md" }
});
```

**Storage:** `.claude/state/sessions/{sessionId}.json`

---

### `loadSession(sessionId: string) -> SessionData | null`

Load a temporary session.

**Parameters:**
- `sessionId`: Session identifier

**Returns:** SessionData if exists, `null` otherwise

**Example:**
```typescript
const session = state_manager.loadSession("brainstorm-20260122-143052");
if (session) {
  console.log(`Session type: ${session.type}`);
  console.log(`Iterations: ${session.iterations.length}`);
}
```

---

### `cleanupSessions(maxAge?: number) -> number`

Remove stale sessions older than maxAge.

**Parameters:**
- `maxAge`: Maximum age in milliseconds (default: 7 days)

**Returns:** Number of sessions deleted

**Example:**
```typescript
// Clean sessions older than 24 hours
const deleted = state_manager.cleanupSessions(24 * 60 * 60 * 1000);
console.log(`Cleaned up ${deleted} stale sessions`);
```

---

## Index Functions

### `rebuildIndex() -> void`

Rebuild the feature index from individual state files.

**Use Case:** Recovery from corrupted index

**Example:**
```typescript
try {
  state_manager.listFeatures();
} catch (e) {
  if (e.code === "INDEX_CORRUPTED") {
    state_manager.rebuildIndex();
    console.log("Index rebuilt from feature directories");
  }
}
```

---

## Error Codes

| Code | Meaning | Recovery |
|------|---------|----------|
| `STATE_NOT_FOUND` | Feature state doesn't exist | Call `createFeature()` first |
| `STATE_CORRUPTED` | State JSON parse error | Restore from checkpoint |
| `INDEX_CORRUPTED` | Index file invalid | Call `rebuildIndex()` |
| `CHECKPOINT_NOT_FOUND` | Checkpoint doesn't exist | List checkpoints to find valid ID |
| `DISK_FULL` | Cannot write state | Free disk space |
| `CONCURRENT_MODIFY` | Race condition detected | Retry operation |
| `INVALID_SLUG` | Slug format invalid | Use kebab-case, 3-50 chars |
