# State Manager — Usage Examples

Practical examples of state-manager integration.

## Basic Workflow

### Starting a New Feature

```typescript
// 1. Initialize state
const state = state_manager.init("user-profile-edit");

// 2. Update context with task list
state.context.tasks = [
  { id: "US-001", title: "Add edit button", status: "pending" },
  { id: "US-002", title: "Create edit form", status: "pending" },
  { id: "US-003", title: "Save changes API", status: "pending" }
];
state_manager.save(state);

// 3. Begin implementation
state_manager.update_phase("implementation");
```

### Tracking Progress

```typescript
// Mark task as in progress
state.context.current_task = "US-001";
state.context.tasks[0].status = "in_progress";
state_manager.save(state);

// After completing task
state.context.tasks[0].status = "completed";
state.files_modified.push("src/components/UserProfile.tsx");
state_manager.save(state);
```

### Resuming Work

```typescript
// Load existing state
const state = state_manager.load("user-profile-edit");

if (state) {
  console.log(`Resuming: ${state.feature_slug}`);
  console.log(`Phase: ${state.current_phase}`);
  console.log(`Current task: ${state.context.current_task}`);

  // Find remaining tasks
  const remaining = state.context.tasks.filter(t => t.status !== "completed");
  console.log(`Tasks remaining: ${remaining.length}`);
}
```

---

## Checkpoint Usage

### Creating Checkpoints

```typescript
// Before a risky refactor
const checkpointId = state_manager.create_checkpoint();
console.log(`Checkpoint saved: ${checkpointId}`);

// Attempt risky operation
try {
  await performRiskyRefactor();
  // Success - checkpoint can be deleted
} catch (error) {
  // Failure - restore checkpoint
  state_manager.resume_checkpoint(checkpointId);
  console.log("Restored to checkpoint");
}
```

### End of Session

```typescript
// User wants to pause
state.status = "paused";
state.context.pause_reason = "User requested";
state.context.session_end = new Date().toISOString();
state_manager.save(state);
state_manager.create_checkpoint();

console.log("Session saved. Resume anytime with /implement --continue");
```

---

## Integration with Skills

### /implement Integration

```typescript
// At start of /implement
function startImplement(slug: string) {
  let state = state_manager.load(slug);

  if (!state) {
    // New feature
    state = state_manager.init(slug);
    state.context.started_by = "/implement";
  } else if (state.status === "paused") {
    // Resuming
    state.status = "in_progress";
    state_manager.save(state);
    console.log("Resuming paused feature...");
  }

  return state;
}
```

### /quick Integration

```typescript
// /quick uses lightweight state
function startQuick(description: string) {
  const slug = generateSlug(description);
  const state = state_manager.init(slug);

  // Minimal context for quick tasks
  state.context.quick_mode = true;
  state.context.description = description;

  // Skip planning phase for TINY
  state.current_phase = "implementation";

  return state_manager.save(state);
}
```

### /improve Integration

```typescript
// /improve updates existing feature state
function startImprove(existingSlug: string, improvement: string) {
  const state = state_manager.load(existingSlug);

  if (!state) {
    throw new Error(`Feature ${existingSlug} not found`);
  }

  // Create improvement branch in context
  state.context.improvements = state.context.improvements || [];
  state.context.improvements.push({
    description: improvement,
    started: new Date().toISOString(),
    status: "in_progress"
  });

  return state_manager.save(state);
}
```

---

## Error Handling

### Detecting Stale State

```typescript
const state = state_manager.load(slug);
const staleThreshold = 7 * 24 * 60 * 60 * 1000; // 7 days

if (state) {
  const lastUpdate = new Date(state.updated_at);
  const isStale = Date.now() - lastUpdate.getTime() > staleThreshold;

  if (isStale) {
    console.log("Warning: Feature state is stale");
    console.log("Options: resume, archive, or restart");
  }
}
```

### Recovering from Failure

```typescript
const state = state_manager.load(slug);

if (state?.status === "failed") {
  console.log(`Feature failed: ${state.context.last_error}`);

  // Option 1: Retry from last checkpoint
  const checkpoints = listCheckpoints(slug);
  if (checkpoints.length > 0) {
    const latest = checkpoints[checkpoints.length - 1];
    state_manager.resume_checkpoint(latest);
  }

  // Option 2: Reset to planning
  state.status = "in_progress";
  state.current_phase = "planning";
  state.context.retry_count = (state.context.retry_count || 0) + 1;
  state_manager.save(state);
}
```

---

## Multi-Feature Coordination

### Listing Active Features

```typescript
const features = state_manager.list_features();

console.log("Active features:");
features.forEach(slug => {
  const status = state_manager.get_status(slug);
  console.log(`  - ${slug}: ${status}`);
});
```

### Feature Dependencies

```typescript
// Feature B depends on Feature A
function checkDependencies(state: State) {
  const deps = state.context.dependencies || [];

  for (const depSlug of deps) {
    const depStatus = state_manager.get_status(depSlug);
    if (depStatus !== "completed") {
      console.log(`Blocked: waiting for ${depSlug}`);
      state.status = "paused";
      state.context.blocked_by = depSlug;
      state_manager.save(state);
      return false;
    }
  }

  return true;
}
```
