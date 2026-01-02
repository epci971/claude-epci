---
description: >-
  {{action_infinitive}}. {{context}}.
  {{expected_result}}.
argument-hint: {{arguments}} {{flags}}
allowed-tools: [Read, Write, Edit, Bash, Grep, Glob, Task]
---

# {{Command Name}}

## Overview

{{description_2_3_sentences}}

## Arguments

| Argument | Description | Required | Default |
|----------|-------------|----------|---------|
| `{{arg1}}` | {{description1}} | {{yes_no}} | {{default1}} |
| `--{{flag1}}` | {{flag_description1}} | No | {{default2}} |
| `--{{flag2}}` | {{flag_description2}} | No | {{default3}} |

## Process

### 1. {{Step Name}}

{{step_description}}

**Skills loaded**: `{{skill1}}`, `{{skill2}}`

### 2. {{Step Name}}

{{step_description}}

**Subagent invoked**: `@{{subagent}}` — {{subagent_role}}

### 3. {{Step Name}}

{{step_description}}

## Loaded Skills

| Skill | Phase | Purpose |
|-------|-------|---------|
| `{{skill1}}` | {{phase}} | {{purpose1}} |
| `{{skill2}}` | {{phase}} | {{purpose2}} |

## Invoked Subagents

| Subagent | Condition | Role |
|----------|-----------|------|
| `@{{subagent1}}` | {{condition1}} | {{role1}} |
| `@{{subagent2}}` | {{condition2}} | {{role2}} |

## Output

{{output_description}}

```markdown
{{output_format_example}}
```

## Examples

### Example 1: {{Use Case}}

```
> /{{command}} {{args}}

{{expected_result}}
```

### Example 2: {{Use Case with Flag}}

```
> /{{command}} --{{flag}} {{args}}

{{expected_result}}
```

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| {{error1}} | {{cause1}} | {{solution1}} |
| {{error2}} | {{cause2}} | {{solution2}} |

## See Also

- `/{{related_command1}}` — {{relationship1}}
- `/{{related_command2}}` — {{relationship2}}
