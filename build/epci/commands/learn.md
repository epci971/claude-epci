---
description: >-
  Manage EPCI continuous learning system. Displays calibration status,
  resets learning data, exports for analysis, or forces recalibration.
  Use 'status' for overview, 'reset' to clear data, 'export' for backup.
argument-hint: "status|reset|export|calibrate"
allowed-tools: [Read, Write, Glob, Bash]
---

# EPCI Learn — Continuous Learning Management

## Overview

Manages the EPCI continuous learning system which:
- Calibrates time estimations based on actual performance
- Tracks suggestion acceptance/rejection patterns
- Detects recurring issues for proactive suggestions

## Subcommands

| Command | Description |
|---------|-------------|
| `status` | Display current learning state and statistics |
| `reset` | Clear learning data (with confirmation) |
| `export` | Export all learning data as JSON |
| `calibrate` | Force recalibration from feature history |

---

## /learn status

Display the current state of the learning system.

### Process

1. Check if `.project-memory/` exists
2. Load calibration and preference data
3. Display comprehensive status

### Output

```
┌─────────────────────────────────────────────────────────────────────┐
│ 📚 EPCI LEARNING STATUS                                             │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│ 📊 CALIBRATION                                                      │
│ ├── Total samples: {total_samples}                                 │
│ ├── Overall accuracy: {overall_accuracy}                           │
│ ├── Trend: {trend}                                                 │
│ └── Last updated: {last_updated}                                   │
│                                                                     │
│ 📈 FACTORS BY COMPLEXITY                                            │
│ ├── TINY:     {factor}x ({samples} samples, {confidence} conf)    │
│ ├── SMALL:    {factor}x ({samples} samples, {confidence} conf)    │
│ ├── STANDARD: {factor}x ({samples} samples, {confidence} conf)    │
│ └── LARGE:    {factor}x ({samples} samples, {confidence} conf)    │
│                                                                     │
│ 🎯 SUGGESTION LEARNING                                              │
│ ├── Patterns tracked: {patterns_tracked}                          │
│ ├── Disabled patterns: {disabled_count}                            │
│ ├── Preferred patterns: {preferred_count}                          │
│ └── Learning enabled: {enabled}                                    │
│                                                                     │
│ 🔄 RECURRING PATTERNS                                               │
│ ├── Total corrections: {corrections_count}                         │
│ ├── Recurring (auto-suggest): {recurring_count}                    │
│ └── Top patterns:                                                  │
│     1. {pattern_1} ({acceptance_rate_1})                           │
│     2. {pattern_2} ({acceptance_rate_2})                           │
│     3. {pattern_3} ({acceptance_rate_3})                           │
│                                                                     │
│ 💡 INTERPRETATION                                                   │
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

## /learn reset

Reset learning data with confirmation.

### Process

1. Check if learning data exists
2. Display current statistics
3. Ask for explicit confirmation
4. Create backup files
5. Reset calibration and preferences

### Confirmation Dialog

```
⚠️  WARNING: This will delete all learning data.

Current state:
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
✅ Learning data has been reset.
📦 Backups created:
   - calibration.backup-20251218-143022.json
   - preferences.backup-20251218-143022.json
   - corrections.backup-20251218-143022.json

To start fresh: Run some features with `/epci` to collect new data.
```

---

## /learn export

Export all learning data as JSON.

### Process

1. Load all learning files
2. Aggregate into single JSON
3. Output to stdout

### Output Format

```json
{
  "calibration": {
    "version": "1.0.0",
    "factors": {
      "TINY": { "factor": 0.95, "samples": 5, "confidence": 1.0 },
      "SMALL": { "factor": 1.1, "samples": 8, "confidence": 1.0 },
      "STANDARD": { "factor": 1.25, "samples": 3, "confidence": 0.79 },
      "LARGE": { "factor": 1.4, "samples": 1, "confidence": 0.50 }
    },
    "global": {
      "total_samples": 17,
      "overall_accuracy": 0.78,
      "trend": "improving"
    },
    "history": [ ... ]
  },
  "preferences": {
    "suggestion_feedback": {
      "test-coverage": { "accepted": 5, "rejected": 1, "acceptance_rate": 0.83 },
      "n1-query": { "accepted": 2, "rejected": 3, "acceptance_rate": 0.40 }
    },
    "disabled_suggestions": ["code-style-nitpick"],
    "preferred_patterns": ["repository-pattern"]
  },
  "corrections": {
    "corrections": [ ... ],
    "patterns": {
      "input-validation": { "occurrences": 4, "auto_suggest": true }
    }
  },
  "exported_at": "2025-12-18T14:30:00Z"
}
```

### Usage

```bash
# Display in terminal
/learn export

# Save to file (user copies output)
# Or redirect in shell: claude-code "/learn export" > learning-backup.json
```

---

## /learn calibrate

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
│ 🔄 RECALIBRATION COMPLETE                                           │
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
| No learning data | Show empty status, suggest running features |
| Corrupted files | Warn and use defaults, suggest reset |
| No feature history | Cannot recalibrate, show message |

---

## Integration with EPCI Workflow

Learning data is automatically updated by:

| Trigger | Action |
|---------|--------|
| `/epci` Phase 3 completion | Trigger calibration with feature times |
| Suggestion accepted | Record positive feedback |
| Suggestion rejected | Record negative feedback |
| "Never suggest" clicked | Add to disabled list |
| Code review correction | Record for pattern detection |

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
