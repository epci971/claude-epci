---
name: project-memory
description: >-
  Comprehensive Project Memory management for EPCI workflows. Loads context
  at workflow start, persists feature history, and provides conventions/patterns
  for consistent code generation. Auto-invoke at start of /epci-brief, /epci,
  /epci-quick, /epci-spike, /epci-decompose.
allowed-tools: [Read, Glob, Write]
---

# Project Memory Skill

## Overview

Project Memory provides persistent storage and context loading for EPCI workflows.
Data is stored in `.project-memory/` at the project root and is automatically
loaded at the start of each EPCI command.

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

## When to Load

**Always load at the start of:**
- `/epci-brief` — Before exploration
- `/epci` — Before each phase
- `/epci-quick` — Before implementation
- `/epci-spike` — Before exploration
- `/epci-decompose` — Before analysis

## Loading Process

### Step 1: Check for Project Memory

```
Check if `.project-memory/` directory exists in project root.
```

**If not found:** Continue without context. At workflow end, suggest:
```
💡 No Project Memory detected. Run `/epci-memory init` to enable
   learning, conventions, and velocity tracking.
```

### Step 2: Load Required Files

Load the following files in order:

#### 2.1 Context — `.project-memory/context.json`

**Extract:**
```json
{
  "project.name": "Project identifier",
  "project.stack": "Tech stack (e.g., 'python-django', 'php-symfony')",
  "project.framework_version": "Framework version",
  "team.code_style": "Code style preference"
}
```

**Usage:**
- Auto-detect appropriate stack skill
- Set framework-specific defaults
- Apply code style preferences

#### 2.2 Conventions — `.project-memory/conventions.json`

**Extract:**
```json
{
  "naming": {
    "files": "kebab-case | snake_case | PascalCase",
    "classes": "PascalCase",
    "functions": "camelCase | snake_case",
    "variables": "camelCase | snake_case",
    "constants": "UPPER_SNAKE_CASE"
  },
  "structure": {
    "source_dir": "src/",
    "tests_dir": "tests/",
    "docs_dir": "docs/"
  },
  "code_style": {
    "max_line_length": 120,
    "indent": "spaces | tabs",
    "indent_size": 4
  }
}
```

**Usage:**
- Apply naming conventions to all generated code
- Place files in correct directories
- Format code according to style rules

#### 2.3 Settings — `.project-memory/settings.json`

**Extract:**
```json
{
  "flags": {
    "default_thinking": "think | think-hard | ultrathink",
    "auto_safe_for_sensitive": true
  },
  "hooks": {
    "enabled": true,
    "fail_on_error": false
  },
  "breakpoints": {
    "require_confirmation": true
  }
}
```

**Usage:**
- Apply default flags if not explicitly set
- Configure hook behavior
- Set breakpoint behavior

#### 2.4 Patterns — `.project-memory/patterns/detected.json`

**Extract:**
```json
{
  "patterns": [
    {
      "id": "repository-pattern",
      "confidence": 0.95,
      "files": ["src/Repository/*.php"]
    }
  ]
}
```

**Usage:**
- Suggest consistent architectural patterns
- Guide file placement decisions
- Inform refactoring strategies

### Step 3: Load Optional Files (if exist)

#### 3.1 Velocity — `.project-memory/metrics/velocity.json`

**Extract:**
```json
{
  "summary": {
    "total_features": 15,
    "avg_completion_time": "2h 30m"
  },
  "trend": {
    "velocity_trend": "improving | stable | declining"
  },
  "by_complexity": {
    "TINY": {"count": 5, "avg_time": "10m"},
    "SMALL": {"count": 6, "avg_time": "45m"},
    "STANDARD": {"count": 3, "avg_time": "3h"},
    "LARGE": {"count": 1, "avg_time": "8h"}
  }
}
```

**Usage:**
- Calibrate time estimates
- Identify complexity patterns
- Track improvement trends

#### 3.2 Feature History — `.project-memory/history/features/*.json`

**Scan for:** Similar features by keywords

**Usage:**
- Suggest reuse of patterns from similar features
- Avoid repeating past mistakes
- Leverage proven solutions

#### 3.3 Learning Preferences — `.project-memory/learning/preferences.json`

**Usage:**
- Avoid suggesting disabled patterns
- Follow user's preferred approaches
- Respect past decisions

## Context Application Matrix

| Loaded Data | Where Applied |
|-------------|---------------|
| `conventions.naming` | All generated code, file names |
| `conventions.structure` | File placement, imports |
| `conventions.code_style` | Code formatting |
| `patterns.detected` | Architecture suggestions |
| `settings.flags` | Default flag values |
| `velocity.by_complexity` | Time estimates |
| `history.similar` | "Similar feature X used Y" suggestions |
| `learning.disabled` | Filter out rejected patterns |

## Memory Status Display

At workflow start, display loaded context summary:

```
📚 PROJECT MEMORY LOADED
├── Project: {project.name} ({project.stack})
├── Conventions: {naming.files} files, {naming.functions} functions
├── Patterns: {patterns.count} detected
├── History: {features.count} features completed
└── Velocity: {trend} trend, avg {avg_time} per feature
```

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

## Error Handling

| Condition | Action |
|-----------|--------|
| File missing | Skip with debug log, continue |
| Invalid JSON | Warn user, skip file, continue |
| Empty directory | Suggest `/epci-memory init` |
| Partial data | Use available data, log gaps |

## Integration Points

- **HookContext** includes `project_memory` field
- **Breakpoints** display velocity metrics
- **Feature Documents** reference memory data
- **Reading** context → This skill (auto-loaded)
- **Writing** context → `post-phase-3-memory-update.py` hook
- **Breakpoint context** → `on-breakpoint-memory-context.py` hook

## Best Practices

1. **Initialize early** — Run `/epci-memory init` at project start
2. **Let it learn** — Complete features to build velocity history
3. **Review conventions** — Check detected conventions match your intent
4. **Export before major changes** — Backup with `/epci-memory export`

## Performance Notes

- Load only required files for the current phase
- Cache loaded context for duration of workflow
- Avoid re-reading unchanged files within same session
