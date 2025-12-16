---
name: project-memory
description: >-
  Manages project memory persistence for EPCI workflows. Provides context
  about project stack, conventions, feature history, and velocity metrics.
  Use when: accessing project context, saving feature history, loading conventions.
  Not for: creating new components (use /epci:create), spike explorations.
---

# Project Memory Skill

## Overview

Project memory provides persistent storage for EPCI workflow data across sessions.
Data is stored in `.project-memory/` at the project root.

## Capabilities

### 1. Project Context

Access project metadata and stack information:

```python
# Context includes:
- project.name          # Project name
- project.stack         # Technology stack (php-symfony, javascript-react, etc.)
- project.framework_version
- project.language_version
- epci.features_completed
- epci.last_session
```

### 2. Conventions

Load project-specific conventions:

```python
# Naming conventions
- naming.entities       # PascalCase, camelCase, snake_case
- naming.services       # {Name}Service pattern
- naming.controllers    # {Domain}Controller pattern

# Structure conventions
- structure.src_location    # src/, app/, lib/
- structure.tests_location  # tests/, __tests__/
- structure.test_suffix     # Test, .test, _test

# Code style
- code_style.indent         # spaces, tabs
- code_style.indent_size    # 2, 4
- code_style.max_line_length
```

### 3. Feature History

Track completed features:

```python
# Each feature records:
- slug, title, complexity
- files_modified, loc_added, loc_removed
- tests_created, test_coverage
- estimated_time, actual_time
- agents_used, issues_found
- commit_hash, branch
```

### 4. Velocity Metrics

Access development velocity:

```python
# Metrics include:
- total_features
- avg_time_by_complexity (TINY, SMALL, STANDARD, LARGE)
- estimation_accuracy
- velocity_trend (improving, stable, declining)
```

## Usage in EPCI Workflow

### During /epci-brief

Load project context to:
- Know the stack before exploration
- Apply correct conventions
- Reference past similar features

### During /epci Phase 2

Use conventions to:
- Name new files correctly
- Place tests in right location
- Follow code style

### After /epci Phase 3

Save feature history:
- Record completion metrics
- Update velocity data
- Track agents used

## Memory Structure

```
.project-memory/
├── context.json        # Project metadata
├── conventions.json    # Naming & style rules
├── settings.json       # EPCI configuration
├── history/
│   ├── features/       # Feature completion records
│   └── decisions/      # Architecture decisions
├── patterns/
│   ├── detected.json   # Auto-detected patterns
│   └── custom.json     # User-defined patterns
├── metrics/
│   ├── velocity.json   # Development speed metrics
│   └── quality.json    # Code quality metrics
└── learning/
    ├── corrections.json    # Applied corrections
    └── preferences.json    # User preferences
```

## Commands

| Command | Description |
|---------|-------------|
| `/epci-memory init` | Initialize memory with auto-detection |
| `/epci-memory status` | Display current state |
| `/epci-memory reset` | Clear memory (with backup) |
| `/epci-memory export` | Export as JSON |

## Auto-Detection

On initialization, the system detects:

| Detection | Sources |
|-----------|---------|
| Stack | composer.json, package.json, requirements.txt, pom.xml |
| Framework version | Lock files, config files |
| Naming conventions | Existing file names in entity/service dirs |
| Test patterns | Test file locations and naming |
| Code style | .eslintrc, .prettierrc, phpcs.xml, etc. |
| Architecture patterns | Directory structure, class names |

## Best Practices

1. **Initialize early** — Run `/epci-memory init` at project start
2. **Let it learn** — Complete features to build velocity history
3. **Review conventions** — Check detected conventions match your intent
4. **Export before major changes** — Backup with `/epci-memory export`

## Integration Points

- **HookContext** includes `project_memory` field
- **Breakpoints** display velocity metrics
- **Feature Documents** reference memory data
