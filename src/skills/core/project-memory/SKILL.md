---
name: project-memory
description: >-
  Maintains project context, history, and learnings across sessions.
  Provides persistent memory for patterns, preferences, and past decisions.
  Use when: recalling past implementations, applying project conventions,
  calibrating estimates, or accessing user preferences.
  Internal component for EPCI v6.0.
user-invocable: false
disable-model-invocation: false
allowed-tools: Read, Write, Glob
---

# Project Memory

Internal component for project context and history across sessions.

## Overview

Persistent memory for:
- Past implementations and their outcomes
- User preferences and choices
- Project coding patterns
- Similar problems solved before
- Velocity and estimation metrics

## API

| Function | Description | Input | Output |
|----------|-------------|-------|--------|
| `init(project_root)` | Initialize memory | path | Memory instance |
| `recall(query)` | Search past context | query string | Relevant memories |
| `store(type, data)` | Save new memory | type, data | Success boolean |
| `get_patterns()` | Project patterns | - | Pattern list |
| `get_velocity()` | Estimation metrics | - | Velocity data |
| `get_preferences()` | User preferences | - | Preferences object |

## Memory Types

| Type | Contents | Example |
|------|----------|---------|
| `features` | Completed feature history | auth-oauth implementation |
| `patterns` | Code patterns used | API response format |
| `preferences` | User choices | prefers TDD, uses Tailwind |
| `bugs` | Past bugs and fixes | OAuth redirect issue |
| `velocity` | Time estimates accuracy | SMALL tasks avg 1.5h |

## Storage Structure

```
.epci/
├── memory/
│   ├── features/
│   │   └── {slug}.json       # Feature implementation history
│   ├── patterns.json         # Detected code patterns
│   ├── preferences.json      # User preferences
│   ├── bugs.json             # Bug fix history
│   └── velocity.json         # Estimation calibration
└── features/
    └── <slug>/
        └── state.json        # Active feature state
```

## Usage

Invoked automatically by all skills for context:

```
# Called at session start
memory = project_memory.init("/path/to/project")

# Recall similar past work
similar = memory.recall("authentication feature")
# Returns: [{ slug: "auth-basic", patterns: [...], duration: "2h" }]

# Get project coding patterns
patterns = memory.get_patterns()
# Returns: { api_style: "REST", error_format: "...", ... }

# Store new learning
memory.store("patterns", { new_pattern: "..." })

# Check estimation accuracy
velocity = memory.get_velocity()
# Returns: { small_avg: 1.5, small_accuracy: 0.85, ... }
```

## Velocity Calibration

Tracks estimation accuracy over time:

```json
{
  "tiny": { "estimated_avg": 30, "actual_avg": 25, "accuracy": 0.83 },
  "small": { "estimated_avg": 120, "actual_avg": 135, "accuracy": 0.89 },
  "standard": { "estimated_avg": 480, "actual_avg": 520, "accuracy": 0.92 },
  "large": { "estimated_avg": 1440, "actual_avg": 1600, "accuracy": 0.90 }
}
```

## Pattern Detection

Automatically detects and stores:

| Pattern | Detection Method |
|---------|------------------|
| API style | Analyze existing endpoints |
| Error handling | Grep error patterns |
| Naming conventions | File and variable analysis |
| Test structure | Analyze test files |
| Component patterns | UI component analysis |

## Preference Learning

Tracks user choices:

```json
{
  "workflow": {
    "tdd_preference": "guided",
    "breakpoint_frequency": "high",
    "verbosity": "concise"
  },
  "technical": {
    "preferred_test_framework": "vitest",
    "css_approach": "tailwind",
    "api_style": "rest"
  }
}
```

## Limitations

This component does NOT:
- Sync across machines (local file-based)
- Store sensitive credentials
- Replace version control history
