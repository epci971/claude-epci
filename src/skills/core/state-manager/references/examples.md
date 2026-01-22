# State Manager — Usage Examples

Practical examples of state-manager integration for EPCI v6.0.

## Basic Feature Workflow

### Starting a New Feature with /implement

```typescript
// 1. Create feature state with spec output
const state = state_manager.createFeature("user-profile-edit", {
  prd_json: "docs/specs/user-profile-edit.prd.json",
  prd_md: "docs/specs/user-profile-edit.md",
  complexity: "STANDARD",
  total_tasks: 4,
  estimated_minutes: 120
});

// State created at: .claude/state/features/user-profile-edit/state.json
// Index updated at: .claude/state/features/index.json

// 2. Begin implementation phase
state_manager.updateFeature("user-profile-edit", {
  lifecycle: {
    current_phase: "code",
    completed_phases: ["explore", "plan"],
    last_updated_by: "/implement"
  },
  execution: {
    tasks: {
      completed: [],
      current: "US-001",
      pending: ["US-002", "US-003", "US-004"],
      failed: []
    }
  }
});
```

### Tracking Task Progress

```typescript
// Load current state
const state = state_manager.loadFeature("user-profile-edit");

// Mark task as completed
state_manager.updateFeature("user-profile-edit", {
  execution: {
    tasks: {
      completed: [...state.execution.tasks.completed, "US-001"],
      current: "US-002",
      pending: state.execution.tasks.pending.slice(1)
    },
    iterations: state.execution.iterations + 1
  },
  artifacts: {
    modified_files: [
      ...state.artifacts.modified_files,
      "src/components/UserProfile.tsx"
    ]
  }
});

// Log to history
state_manager.appendHistory("user-profile-edit", {
  action: "task_completed",
  task_id: "US-001",
  timestamp: new Date().toISOString(),
  details: { files_modified: ["src/components/UserProfile.tsx"] }
});
```

### Completing a Feature

```typescript
// Mark feature as completed
state_manager.updateFeature("user-profile-edit", {
  lifecycle: {
    status: "completed",
    current_phase: "inspect",
    completed_phases: ["explore", "plan", "code", "inspect"],
    last_updated_by: "/implement"
  }
});

// Log completion
state_manager.appendHistory("user-profile-edit", {
  action: "feature_completed",
  timestamp: new Date().toISOString(),
  details: {
    total_tasks: 4,
    total_iterations: 18,
    files_modified: state.artifacts.modified_files.length
  }
});
```

---

## Checkpoint Management

### Creating Checkpoints

```typescript
// Before starting risky operation
const checkpoint = state_manager.createCheckpoint("user-profile-edit", "code");
console.log(`Checkpoint created: ${checkpoint.id}`);
// Output: "code-20260122-143052"

// Checkpoint saved to:
// .claude/state/features/user-profile-edit/checkpoints/code-20260122-143052.json
```

### Listing and Restoring Checkpoints

```typescript
// List all checkpoints for a feature
const checkpoints = state_manager.listCheckpoints("user-profile-edit");
checkpoints.forEach(cp => {
  console.log(`${cp.id} - Phase: ${cp.phase} - ${cp.timestamp}`);
});

// Restore from a checkpoint after failure
if (error) {
  const latestCheckpoint = checkpoints[checkpoints.length - 1];
  const restoredState = state_manager.restoreCheckpoint(latestCheckpoint.id);
  console.log(`Restored to phase: ${restoredState.lifecycle.current_phase}`);
}
```

### End of Work Session

```typescript
// User wants to pause work
state_manager.updateFeature("user-profile-edit", {
  lifecycle: {
    status: "paused",
    last_updated_by: "/implement"
  }
});

// Create checkpoint for easy resume
const checkpoint = state_manager.createCheckpoint("user-profile-edit", "code");

// Log pause
state_manager.appendHistory("user-profile-edit", {
  action: "feature_paused",
  timestamp: new Date().toISOString(),
  details: {
    checkpoint_id: checkpoint.id,
    reason: "user_request"
  }
});

console.log("Session saved. Resume with: /implement --continue user-profile-edit");
```

---

## Session Management (Brainstorm/Debug)

### Saving a Brainstorm Session

```typescript
// During /brainstorm workflow
state_manager.saveSession("brainstorm-20260122-100000", {
  type: "brainstorm",
  started_at: "2026-01-22T10:00:00Z",
  input: "I want to add OAuth authentication with Google and GitHub",

  iterations: [
    {
      iteration: 1,
      ems_score: 42,
      weak_axes: ["feasibility", "clarity"],
      hmw_questions: [
        "How might we handle multiple OAuth providers?",
        "How might we store tokens securely?"
      ]
    },
    {
      iteration: 2,
      ems_score: 67,
      weak_axes: ["feasibility"],
      refinements: ["Added token refresh strategy"]
    },
    {
      iteration: 3,
      ems_score: 85,
      weak_axes: [],
      convergence: true
    }
  ],

  output: {
    cdc_path: "docs/specs/auth-oauth-cdc.md",
    complexity: "STANDARD",
    recommended_next: "/spec @docs/specs/auth-oauth-cdc.md"
  }
});
```

### Saving a Debug Session

```typescript
// During /debug workflow
state_manager.saveSession("debug-20260122-143052", {
  type: "debug",
  started_at: "2026-01-22T14:30:52Z",
  input: "Login fails with 'Invalid token' error",

  investigation: {
    symptoms: ["Login form submits but returns 401"],
    hypotheses: [
      { description: "Token expired", probability: 0.6, tested: true, result: false },
      { description: "Token format wrong", probability: 0.3, tested: true, result: true }
    ],
    root_cause: "Base64 encoding missing in token generation"
  },

  output: {
    fix_applied: true,
    files_modified: ["src/auth/token.ts"],
    test_added: "tests/unit/token.test.ts",
    regression_passed: true
  }
});
```

### Loading and Cleaning Sessions

```typescript
// Resume a brainstorm session
const session = state_manager.loadSession("brainstorm-20260122-100000");
if (session) {
  console.log(`Resuming brainstorm: ${session.iterations.length} iterations done`);
  console.log(`Last EMS score: ${session.iterations.at(-1).ems_score}`);
}

// Cleanup old sessions (older than 24 hours)
const deleted = state_manager.cleanupSessions(24 * 60 * 60 * 1000);
console.log(`Cleaned up ${deleted} stale sessions`);
```

---

## Integration with Skills

### /implement Integration

```typescript
// At start of /implement
async function startImplement(slug: string, continueFlag: boolean) {
  let state = state_manager.loadFeature(slug);

  if (continueFlag && state) {
    // Resume existing feature
    if (state.lifecycle.status === "paused") {
      state_manager.updateFeature(slug, {
        lifecycle: { status: "in_progress" }
      });
      state_manager.appendHistory(slug, {
        action: "feature_resumed",
        timestamp: new Date().toISOString()
      });
      console.log(`Resuming ${slug} at phase: ${state.lifecycle.current_phase}`);
    }
    return state;
  }

  if (!state) {
    // Create new feature - need spec first
    throw new Error(`Run /spec first to create PRD for ${slug}`);
  }

  return state;
}
```

### /quick Integration

```typescript
// /quick uses minimal state (optional)
async function startQuick(description: string) {
  const slug = generateSlug(description);

  // Check if it's really quick (TINY/SMALL)
  const complexity = calculateComplexity(description);
  if (complexity === "STANDARD" || complexity === "LARGE") {
    console.log("Task too complex for /quick. Use /implement instead.");
    return null;
  }

  // Create minimal state
  const state = state_manager.createFeature(slug, {
    prd_json: null, // No formal PRD for quick tasks
    prd_md: null,
    complexity: complexity,
    total_tasks: 1,
    estimated_minutes: complexity === "TINY" ? 15 : 45
  });

  // Skip directly to code phase
  state_manager.updateFeature(slug, {
    lifecycle: {
      current_phase: "code",
      completed_phases: ["explore", "plan"], // Implicit for quick
      created_by: "/quick"
    }
  });

  return state;
}
```

### /improve Integration

```typescript
// /improve updates existing feature
async function startImprove(existingSlug: string, improvement: string) {
  const state = state_manager.loadFeature(existingSlug);

  if (!state) {
    throw new Error(`Feature ${existingSlug} not found`);
  }

  if (state.lifecycle.status !== "completed") {
    throw new Error(`Feature must be completed before improvements`);
  }

  // Add improvement to state
  state_manager.updateFeature(existingSlug, {
    improvements: [
      ...state.improvements,
      {
        description: improvement,
        started_at: new Date().toISOString(),
        completed_at: null,
        status: "in_progress"
      }
    ],
    lifecycle: {
      status: "in_progress", // Reopen feature
      last_updated_by: "/improve"
    }
  });

  state_manager.appendHistory(existingSlug, {
    action: "improvement_added",
    timestamp: new Date().toISOString(),
    details: { description: improvement }
  });

  return state_manager.loadFeature(existingSlug);
}
```

---

## Error Handling

### Handling Corrupted State

```typescript
try {
  const state = state_manager.loadFeature("my-feature");
} catch (error) {
  if (error.code === "STATE_CORRUPTED") {
    console.log("State file corrupted. Attempting recovery...");

    // Try to restore from latest checkpoint
    const checkpoints = state_manager.listCheckpoints("my-feature");
    if (checkpoints.length > 0) {
      const latest = checkpoints[checkpoints.length - 1];
      const recovered = state_manager.restoreCheckpoint(latest.id);
      console.log(`Recovered from checkpoint: ${latest.id}`);
    } else {
      console.log("No checkpoints available. Manual intervention needed.");
    }
  }
}
```

### Handling Corrupted Index

```typescript
try {
  const features = state_manager.listFeatures();
} catch (error) {
  if (error.code === "INDEX_CORRUPTED") {
    console.log("Index corrupted. Rebuilding from feature directories...");
    state_manager.rebuildIndex();
    const features = state_manager.listFeatures();
    console.log(`Index rebuilt with ${features.length} features`);
  }
}
```

### Detecting Stale Features

```typescript
const features = state_manager.listFeatures({ status: "in_progress" });
const staleThreshold = 7 * 24 * 60 * 60 * 1000; // 7 days

features.forEach(f => {
  const lastUpdate = new Date(f.last_update);
  const isStale = Date.now() - lastUpdate.getTime() > staleThreshold;

  if (isStale) {
    console.log(`Warning: ${f.id} is stale (last update: ${f.last_update})`);
    console.log("Options: resume with /implement --continue or archive");
  }
});
```

---

## Multi-Feature Coordination

### Listing All Features

```typescript
// All active features
const active = state_manager.listFeatures({ status: "in_progress" });
console.log("\nActive features:");
active.forEach(f => {
  console.log(`  ${f.id}: ${f.current_phase} (${f.complexity})`);
});

// All features by status
const all = state_manager.listFeatures();
const byStatus = {
  in_progress: all.filter(f => f.status === "in_progress"),
  paused: all.filter(f => f.status === "paused"),
  completed: all.filter(f => f.status === "completed"),
  failed: all.filter(f => f.status === "failed")
};

console.log(`\nFeature summary:`);
console.log(`  Active: ${byStatus.in_progress.length}`);
console.log(`  Paused: ${byStatus.paused.length}`);
console.log(`  Completed: ${byStatus.completed.length}`);
console.log(`  Failed: ${byStatus.failed.length}`);
```

### Feature Dashboard

```typescript
function showFeatureDashboard() {
  const features = state_manager.listFeatures();

  console.log("\n┌─────────────────────────────────────────────────────────┐");
  console.log("│                   FEATURE DASHBOARD                      │");
  console.log("├─────────────────────────────────────────────────────────┤");

  features.forEach(f => {
    const statusIcon = {
      in_progress: "🔄",
      paused: "⏸️",
      completed: "✅",
      failed: "❌"
    }[f.status];

    const phaseProgress = ["explore", "plan", "code", "inspect"]
      .map((p, i) => {
        if (f.current_phase === p) return "●";
        if (["explore", "plan", "code", "inspect"].indexOf(f.current_phase) > i) return "○";
        return "·";
      })
      .join("");

    console.log(`│ ${statusIcon} ${f.id.padEnd(25)} [${phaseProgress}] ${f.complexity.padEnd(8)} │`);
  });

  console.log("└─────────────────────────────────────────────────────────┘");
}
```

---

## Storage Layout Reference

```
.claude/state/
├── config.json                              # Global EPCI config
├── features/
│   ├── index.json                           # Central registry
│   │
│   ├── auth-oauth-google/
│   │   ├── state.json                       # Current state
│   │   ├── history.json                     # Action log
│   │   └── checkpoints/
│   │       ├── plan-20260122-110000.json
│   │       └── code-20260122-143052.json
│   │
│   └── user-profile-edit/
│       ├── state.json
│       ├── history.json
│       └── checkpoints/
│           └── plan-20260122-090000.json
│
└── sessions/
    ├── brainstorm-20260122-100000.json      # Temporary session
    └── debug-20260122-143052.json           # Temporary session
```
