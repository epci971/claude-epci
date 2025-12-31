---
description: >-
  Manage project memory and learning for EPCI. Initializes, displays status,
  resets, or exports the .project-memory/ directory. Includes learning subsystem
  for calibration, preferences, and pattern detection.
argument-hint: "status|init|reset|export|learn [status|reset|calibrate]"
allowed-tools: [Read, Write, Glob, Bash]
---

# EPCI Memory — Project Memory & Learning Management v2.0

## Overview

Manages the `.project-memory/` directory which stores:
- **Project context**: stack, conventions, patterns, feature history
- **Learning data**: calibration, preferences, recurring patterns

## Subcommands

| Command | Description |
|---------|-------------|
| `status` | Display project memory + learning summary |
| `init` | Initialize project memory with auto-detection |
| `reset` | Reset all memory (with confirmation) |
| `export` | Export all data as JSON |
| `learn status` | Display detailed learning statistics |
| `learn reset` | Reset learning data only (keep project context) |
| `learn calibrate` | Force recalibration from feature history |

---

## /memory status

Display combined project memory and learning state.

### Process

1. Check if `.project-memory/` exists
2. Load context, conventions, velocity, and learning data
3. Display unified summary

### Output

```
┌─────────────────────────────────────────────────────────────────────┐
│ PROJECT MEMORY STATUS                                               │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│ Location: .project-memory/                                          │
│                                                                     │
│ PROJECT                                                             │
│ ├── Name: {project_name}                                           │
│ ├── Stack: {stack}                                                 │
│ ├── Framework: {framework_version}                                 │
│ └── Initialized: {initialized_at}                                  │
│                                                                     │
│ METRICS                                                             │
│ ├── Features completed: {features_completed}                       │
│ ├── Last session: {last_session}                                   │
│ └── Velocity trend: {velocity_trend}                               │
│                                                                     │
│ CONVENTIONS                                                         │
│ ├── Entities: {naming.entities}                                    │
│ ├── Services: {naming.services}                                    │
│ └── Code style: {code_style}                                       │
│                                                                     │
│ PATTERNS DETECTED                                                   │
│ └── {patterns or "None detected"}                                  │
│                                                                     │
│ LEARNING (summary)                                                  │
│ ├── Calibration samples: {total_samples}                           │
│ ├── Overall accuracy: {overall_accuracy}                           │
│ └── Patterns tracked: {patterns_tracked}                           │
│                                                                     │
│ -> /memory learn status for detailed learning info                 │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## /memory init

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
       ├── calibration.json
       ├── preferences.json
       └── corrections.json
   ```
4. Initialize learning with defaults
5. Display detected values

### Output

```
┌─────────────────────────────────────────────────────────────────────┐
│ PROJECT MEMORY INITIALIZED                                          │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│ Created: .project-memory/                                           │
│                                                                     │
│ DETECTION RESULTS                                                   │
│ ├── Stack: {detected_stack} (confidence: {confidence}%)            │
│ ├── Framework: {framework} {version}                               │
│ ├── Language: {language} {version}                                 │
│ └── Code style: {code_style}                                       │
│                                                                     │
│ CONVENTIONS DETECTED                                                │
│ ├── Entities: {naming.entities}                                    │
│ ├── Services: {naming.services}                                    │
│ ├── Tests location: {structure.tests_location}                     │
│ └── Test suffix: {structure.test_suffix}                           │
│                                                                     │
│ PATTERNS DETECTED                                                   │
│ └── {patterns_list or "None detected"}                             │
│                                                                     │
│ LEARNING INITIALIZED                                                │
│ ├── Calibration: Ready (0 samples)                                 │
│ ├── Preferences: Empty                                             │
│ └── Patterns: Tracking enabled                                     │
│                                                                     │
│ You can manually adjust in:                                         │
│    .project-memory/conventions.json                                │
│    .project-memory/settings.json                                   │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## /memory reset

Reset all project memory with confirmation.

### Process

1. Check if `.project-memory/` exists
2. Ask for explicit confirmation
3. Create backup: `.project-memory-backup-{timestamp}/`
4. Remove `.project-memory/`
5. Confirm reset

### Confirmation Dialog

```
WARNING: This will delete ALL project memory data.

Current state:
- Features recorded: {count}
- Learning samples: {count}
- Initialized: {date}
- Last session: {date}

A backup will be created at: .project-memory-backup-{timestamp}/

Type "RESET" to confirm, or anything else to cancel:
```

### Output (after confirmation)

```
Project memory has been reset.
Backup created: .project-memory-backup-20251216-143022/

To reinitialize: /memory init
```

---

## /memory export

Export all memory and learning data as JSON.

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
  "learning": {
    "calibration": { ... },
    "preferences": { ... },
    "corrections": { ... }
  },
  "exported_at": "2025-12-16T14:30:00Z"
}
```

---

## /memory learn status

Display detailed learning statistics.

### Output

```
┌─────────────────────────────────────────────────────────────────────┐
│ EPCI LEARNING STATUS                                                │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│ CALIBRATION                                                         │
│ ├── Total samples: {total_samples}                                 │
│ ├── Overall accuracy: {overall_accuracy}                           │
│ ├── Trend: {trend}                                                 │
│ └── Last updated: {last_updated}                                   │
│                                                                     │
│ FACTORS BY COMPLEXITY                                               │
│ ├── TINY:     {factor}x ({samples} samples, {confidence} conf)    │
│ ├── SMALL:    {factor}x ({samples} samples, {confidence} conf)    │
│ ├── STANDARD: {factor}x ({samples} samples, {confidence} conf)    │
│ └── LARGE:    {factor}x ({samples} samples, {confidence} conf)    │
│                                                                     │
│ SUGGESTION LEARNING                                                 │
│ ├── Patterns tracked: {patterns_tracked}                          │
│ ├── Disabled patterns: {disabled_count}                            │
│ ├── Preferred patterns: {preferred_count}                          │
│ └── Learning enabled: {enabled}                                    │
│                                                                     │
│ RECURRING PATTERNS                                                  │
│ ├── Total corrections: {corrections_count}                         │
│ ├── Recurring (auto-suggest): {recurring_count}                    │
│ └── Top patterns:                                                  │
│     1. {pattern_1} ({acceptance_rate_1})                           │
│     2. {pattern_2} ({acceptance_rate_2})                           │
│     3. {pattern_3} ({acceptance_rate_3})                           │
│                                                                     │
│ INTERPRETATION                                                      │
│ • Factor > 1.0: Actual time exceeds estimates                       │
│ • Factor < 1.0: Estimates exceed actual time                        │
│ • High confidence: More reliable calibration                        │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### Interpretation Guide

| Factor | Meaning | Action |
|--------|---------|--------|
| 1.0 | Estimates are accurate | No adjustment needed |
| > 1.0 | Under-estimating | Multiply base estimate by factor |
| < 1.0 | Over-estimating | Multiply base estimate by factor |
| Low confidence | Few samples | Collect more data |

---

## /memory learn reset

Reset learning data only, keeping project context intact.

### Process

1. Check if learning data exists
2. Display current statistics
3. Ask for explicit confirmation
4. Create backup files
5. Reset calibration and preferences only

### Confirmation Dialog

```
WARNING: This will reset learning data only.
Project context, conventions, and history will be preserved.

Current learning state:
- Calibration samples: {count}
- Patterns tracked: {count}
- Corrections recorded: {count}
- Learning since: {date}

Backups will be created:
- learning/calibration.backup-{timestamp}.json
- learning/preferences.backup-{timestamp}.json
- learning/corrections.backup-{timestamp}.json

Type "RESET" to confirm, or anything else to cancel:
```

### Output (after confirmation)

```
Learning data has been reset.
Backups created in .project-memory/learning/

Project context preserved.
Run features with /epci to collect new calibration data.
```

---

## /memory learn calibrate

Force recalibration from feature history.

### Process

1. Load all completed feature history
2. Filter features with valid estimated/actual times
3. Reset calibration data
4. Replay all features through calibration algorithm
5. Display new calibration status

### Use Cases

- After importing feature history from another project
- After suspected calibration data corruption
- To recalculate with different alpha (weight) value

### Output

```
┌─────────────────────────────────────────────────────────────────────┐
│ RECALIBRATION COMPLETE                                              │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│ Features processed: {count}                                        │
│ Features with valid times: {valid_count}                           │
│                                                                     │
│ NEW CALIBRATION FACTORS                                             │
│ ├── TINY:     {factor}x ({samples} samples)                       │
│ ├── SMALL:    {factor}x ({samples} samples)                       │
│ ├── STANDARD: {factor}x ({samples} samples)                       │
│ └── LARGE:    {factor}x ({samples} samples)                       │
│                                                                     │
│ Overall accuracy: {accuracy}                                       │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Error Handling

| Error | Response |
|-------|----------|
| Memory not initialized | Suggest `/memory init` |
| Corrupted files | Warn and use defaults |
| Permission denied | Display error with path |
| Already initialized (init) | Ask for confirmation |
| No learning data | Show empty status, suggest running features |
| No feature history (calibrate) | Cannot recalibrate, show message |

---

## Integration with EPCI Workflow

Project memory is automatically used by:

| Command | Usage |
|---------|-------|
| `/brief` | Loads context for stack detection |
| `/epci` | Saves feature history after Phase 3 |
| `/epci` Phase 3 | Triggers calibration with feature times |
| Breakpoints | Displays velocity metrics |
| Suggestions | Records accept/reject feedback |
| Code review | Records corrections for pattern detection |
| Hooks | Receives memory context |

---

## Settings

Learning behavior can be configured in `.project-memory/settings.json`:

```json
{
  "learning": {
    "enabled": true,
    "calibration_alpha": 0.3,
    "suggestion_threshold": 0.3,
    "max_suggestions_per_breakpoint": 5,
    "recurrence_threshold": 3
  }
}
```

| Setting | Default | Description |
|---------|---------|-------------|
| `enabled` | `true` | Enable/disable learning |
| `calibration_alpha` | `0.3` | EMA smoothing factor (0-1) |
| `suggestion_threshold` | `0.3` | Min score to show suggestion |
| `max_suggestions_per_breakpoint` | `5` | Max suggestions at breakpoints |
| `recurrence_threshold` | `3` | Occurrences for auto-suggest |

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
| `learning/calibration.json` | Time estimation calibration |
| `learning/preferences.json` | Suggestion preferences |
| `learning/corrections.json` | Correction patterns |

---

## Privacy

EPCI Learning collects only:
- Time metrics (estimated vs actual)
- Pattern identifiers (not code content)
- User actions (accept/reject/ignore)

**Never stored:**
- Source code content
- File contents
- Personal information

All data is local to `.project-memory/` and can be exported/deleted at any time.
