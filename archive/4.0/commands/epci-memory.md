---
description: >-
  Manage project memory for EPCI. Initializes, displays status, resets, or
  exports the .project-memory/ directory in the current project.
  Use 'init' to set up memory, 'status' for current state, 'export' for backup.
argument-hint: "status|init|reset|export"
allowed-tools: [Read, Write, Glob, Bash]
---

# EPCI Memory — Project Memory Management

## Overview

Manages the `.project-memory/` directory in the current project.
This directory stores project context, conventions, feature history, and metrics.

## Subcommands

| Command | Description |
|---------|-------------|
| `status` | Display current memory state and statistics |
| `init` | Initialize project memory with auto-detection |
| `reset` | Clear project memory (with confirmation) |
| `export` | Export all memory data as JSON |

---

## /epci-memory status

Display the current state of project memory.

### Process

1. Check if `.project-memory/` exists
2. Load context, conventions, and velocity
3. Display summary

### Output

```
┌─────────────────────────────────────────────────────────────────────┐
│ 📦 PROJECT MEMORY STATUS                                            │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│ 📂 Location: .project-memory/                                       │
│                                                                     │
│ 🔧 PROJECT                                                          │
│ ├── Name: {project_name}                                           │
│ ├── Stack: {stack}                                                 │
│ ├── Framework: {framework_version}                                 │
│ └── Initialized: {initialized_at}                                  │
│                                                                     │
│ 📊 METRICS                                                          │
│ ├── Features completed: {features_completed}                       │
│ ├── Last session: {last_session}                                   │
│ └── Velocity trend: {velocity_trend}                               │
│                                                                     │
│ 📋 CONVENTIONS                                                      │
│ ├── Entities: {naming.entities}                                    │
│ ├── Services: {naming.services}                                    │
│ └── Code style: {code_style}                                       │
│                                                                     │
│ 🏗️  PATTERNS DETECTED                                               │
│ └── {patterns or "None detected"}                                  │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## /epci-memory init

Initialize project memory with auto-detection.

### Process

1. Check if `.project-memory/` already exists
   - If exists → Ask for confirmation to reinitialize
2. Run project detector:
   - Detect stack (PHP/Symfony, React, Django, etc.)
   - Detect conventions (naming, structure, code style)
   - Detect architecture patterns
3. Create directory structure:
   ```
   .project-memory/
   ├── context.json
   ├── conventions.json
   ├── settings.json
   ├── history/
   │   ├── features/
   │   └── decisions/
   ├── patterns/
   │   ├── detected.json
   │   └── custom.json
   ├── metrics/
   │   ├── velocity.json
   │   └── quality.json
   └── learning/
       ├── corrections.json
       └── preferences.json
   ```
4. Display detected values

### Output

```
┌─────────────────────────────────────────────────────────────────────┐
│ ✅ PROJECT MEMORY INITIALIZED                                        │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│ 📂 Created: .project-memory/                                        │
│                                                                     │
│ 🔍 DETECTION RESULTS                                                │
│ ├── Stack: {detected_stack} (confidence: {confidence}%)            │
│ ├── Framework: {framework} {version}                               │
│ ├── Language: {language} {version}                                 │
│ └── Code style: {code_style}                                       │
│                                                                     │
│ 📋 CONVENTIONS DETECTED                                             │
│ ├── Entities: {naming.entities}                                    │
│ ├── Services: {naming.services}                                    │
│ ├── Tests location: {structure.tests_location}                     │
│ └── Test suffix: {structure.test_suffix}                           │
│                                                                     │
│ 🏗️  PATTERNS DETECTED                                               │
│ └── {patterns_list or "None detected"}                             │
│                                                                     │
│ 💡 You can manually adjust conventions in:                          │
│    .project-memory/conventions.json                                │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## /epci-memory reset

Reset project memory with confirmation.

### Process

1. Check if `.project-memory/` exists
2. Ask for explicit confirmation
3. Create backup: `.project-memory-backup-{timestamp}/`
4. Remove `.project-memory/`
5. Confirm reset

### Confirmation Dialog

```
⚠️  WARNING: This will delete all project memory data.

Current state:
- Features recorded: {count}
- Initialized: {date}
- Last session: {date}

A backup will be created at: .project-memory-backup-{timestamp}/

Type "RESET" to confirm, or anything else to cancel:
```

### Output (after confirmation)

```
✅ Project memory has been reset.
📦 Backup created: .project-memory-backup-20251216-143022/

To reinitialize: /epci-memory init
```

---

## /epci-memory export

Export all memory data as JSON.

### Process

1. Load all memory files
2. Aggregate into single JSON
3. Output to stdout or file

### Output Format

```json
{
  "context": { ... },
  "conventions": { ... },
  "settings": { ... },
  "velocity": { ... },
  "features": {
    "feature-slug-1": { ... },
    "feature-slug-2": { ... }
  },
  "patterns": {
    "detected": [ ... ],
    "custom": [ ... ]
  },
  "exported_at": "2025-12-16T14:30:00Z"
}
```

### Usage

```bash
# Display in terminal
/epci-memory export

# Save to file (user copies output)
/epci-memory export > memory-backup.json
```

---

## Error Handling

| Error | Response |
|-------|----------|
| Memory not initialized | Suggest `/epci-memory init` |
| Corrupted files | Warn and use defaults |
| Permission denied | Display error with path |
| Already initialized (init) | Ask for confirmation |

---

## Integration with EPCI Workflow

Project memory is automatically used by:

| Command | Usage |
|---------|-------|
| `/epci-brief` | Loads context for stack detection |
| `/epci` | Saves feature history after Phase 3 |
| Breakpoints | Displays velocity metrics |
| Hooks | Receives memory context |

---

## Files Reference

| File | Purpose |
|------|---------|
| `context.json` | Project metadata, stack, team info |
| `conventions.json` | Naming, structure, code style rules |
| `settings.json` | EPCI configuration for this project |
| `history/features/*.json` | Feature development history |
| `history/decisions/*.json` | Architectural decisions |
| `patterns/detected.json` | Auto-detected patterns |
| `patterns/custom.json` | User-defined patterns |
| `metrics/velocity.json` | Development velocity metrics |
| `metrics/quality.json` | Code quality metrics |
| `learning/corrections.json` | Applied corrections history |
| `learning/preferences.json` | User preferences |
