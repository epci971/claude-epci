---
name: {{stack}}-{{framework}}
description: >-
  Patterns and conventions for {{Stack}}/{{Framework}}. Includes {{tools}}.
  Use when: {{stack}} development, {{detection_file}} detected.
  Not for: {{other_stacks}}.
---

# {{Stack}}/{{Framework}} Development Patterns

## Overview

Patterns and conventions for modern {{Framework}} development.

## Auto-detection

Automatically loaded if detection of:
- `{{config_file}}` containing `{{package_name}}`
- Files `{{marker_files}}`
- Structure `{{directory_patterns}}`

## {{Framework}} Architecture

### Standard Structure

```
project/
├── {{dir1}}/
│   ├── {{subdir1}}/
│   └── {{subdir2}}/
├── {{dir2}}/
│   └── {{subdir3}}/
├── {{config_file}}
└── README.md
```

### Naming Conventions

| Element | Convention | Example |
|---------|------------|---------|
| {{element1}} | {{convention1}} | `{{example1}}` |
| {{element2}} | {{convention2}} | `{{example2}}` |
| {{element3}} | {{convention3}} | `{{example3}}` |

## {{Main Pattern 1}}

### {{SubPattern}}

```{{language}}
{{code_example}}
```

## {{Main Pattern 2}}

### {{SubPattern}}

```{{language}}
{{code_example}}
```

## Testing Patterns

### Unit Test

```{{language}}
{{test_example}}
```

### Integration Test

```{{language}}
{{integration_test_example}}
```

## Useful Commands

```bash
# Development
{{dev_command}}

# Testing
{{test_command}}

# Build
{{build_command}}
```

## Best Practices

| Practice | Do | Avoid |
|----------|-----|-------|
| {{practice1}} | {{do1}} | {{avoid1}} |
| {{practice2}} | {{do2}} | {{avoid2}} |
| {{practice3}} | {{do3}} | {{avoid3}} |
