# Skill Templates

Ready-to-use templates for creating user and core skills.

## User Skill Templates

### Template: Simple User Skill

For single-purpose skills under 200 lines.

```yaml
---
name: {skill-name}
description: >-
  {ACTION VERB}s {OBJECT} for {PURPOSE}.
  {ADDITIONAL CAPABILITY}.
  Use when: {SCENARIO 1}, {SCENARIO 2}.
  Triggers: {KEYWORD 1}, {KEYWORD 2}, {KEYWORD 3}.
  Not for: {EXCLUSION}.
user-invocable: true
disable-model-invocation: false
argument-hint: "[{param}]"
allowed-tools: {TOOLS}
---

# {Skill Name}

{One-line description of what this skill does.}

## Quick Start

```
/{skill-name} {example-arg}
```

## Workflow

1. **{Step 1 verb}** {description}
2. **{Step 2 verb}** {description}
3. **{Step 3 verb}** {description}

## Examples

### Input
```
/{skill-name} {example}
```

### Output
```
{Expected output format}
```

## Limitations

This skill does NOT:
- {Limitation 1}
- {Limitation 2}
```

---

### Template: Standard User Skill

For multi-step skills with references.

```yaml
---
name: {skill-name}
description: >-
  {ACTION VERB}s {OBJECT} for {PURPOSE}.
  {ADDITIONAL CAPABILITY}.
  Use when: {SCENARIO 1}, {SCENARIO 2}.
  Triggers: {KEYWORD 1}, {KEYWORD 2}, {KEYWORD 3}.
  Not for: {EXCLUSION}.
user-invocable: true
disable-model-invocation: false
argument-hint: "[{param}]"
allowed-tools: {TOOLS}
---

# {Skill Name}

{One-line description.}

## Quick Start

```
/{skill-name} {example}
```

## Modes

| Mode | Description | Flag |
|------|-------------|------|
| Default | {default behavior} | - |
| {Mode 2} | {description} | `--{flag}` |

## Workflow

### Phase 1: {Phase Name}

1. **{Step}** {description}
2. **{Step}** {description}

### Phase 2: {Phase Name}

1. **{Step}** {description}
2. **{Step}** {description}

## Decision Tree

```
IF {condition}:
  → {action 1}
ELSE IF {condition}:
  → {action 2}
ELSE:
  → {default action}
```

## Examples

### Example 1: {Scenario}

**Input:**
```
/{skill-name} {args}
```

**Output:**
```
{result}
```

## Reference Files

- [detailed-guide.md](references/detailed-guide.md) — Full documentation
- [examples.md](references/examples.md) — More examples

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| {Error 1} | {cause} | {fix} |
| {Error 2} | {cause} | {fix} |

## Limitations

This skill does NOT:
- {Limitation 1}
- {Limitation 2}
- {Limitation 3}
```

---

### Template: Interactive User Skill

For skills with user prompts.

```yaml
---
name: {skill-name}
description: >-
  {INTERACTIVE DESCRIPTION}.
  Guides through {PROCESS} with questions.
  Use when: {SCENARIO}.
  Triggers: {KEYWORDS}.
user-invocable: true
allowed-tools: Read, Write, AskUserQuestion
---

# {Skill Name}

Interactive skill that guides you through {process}.

## Workflow

### Step 1: Gather Information

Ask user:
1. {Question 1}
2. {Question 2}

### Step 2: Process

Based on answers:
- If {condition} → {action}
- If {condition} → {action}

### Step 3: Generate Output

Create {output} based on collected information.

## Breakpoints

```
┌─────────────────────────────────────────┐
│ [{TYPE}] {Title}                        │
├─────────────────────────────────────────┤
│ {Content}                               │
├─────────────────────────────────────────┤
│ [A] {Option 1}  [B] {Option 2}          │
└─────────────────────────────────────────┘
```

## Example Session

**User:** `/{skill-name}`

**Skill:** "What is your target?"
- [A] Option 1
- [B] Option 2

**User selects:** A

**Skill:** Generates output...
```

---

## Core Skill Templates

### Template: Core Component

For internal skills (user-invocable: false).

```yaml
---
name: {component-name}
description: >-
  {CAPABILITY DESCRIPTION}. Internal component for EPCI v6.0.
  Use when: {internal trigger conditions}.
  Not for: direct user invocation.
user-invocable: false
disable-model-invocation: false
allowed-tools: {TOOLS}
---

# {Component Name}

Internal component for {purpose}.

## Overview

{2-3 sentences explaining the component's role}

## API

| Function | Description | Input | Output |
|----------|-------------|-------|--------|
| `{function1}()` | {description} | {input} | {output} |
| `{function2}()` | {description} | {input} | {output} |
| `{function3}()` | {description} | {input} | {output} |

## Usage

Invoked automatically by skills when {conditions}:

```
# Example invocation
{component}.{function}({params})
# Returns: {result}
```

## Data Schema

```json
{
  "field1": "type",
  "field2": "type",
  "field3": {
    "nested": "type"
  }
}
```

## Implementation

```
{Step-by-step behavior description}
```

## Limitations

This component does NOT:
- {Limitation 1}
- {Limitation 2}
```

---

### Template: State Component

For components managing persistent state.

```yaml
---
name: {state-component}
description: >-
  Manages {STATE TYPE} across sessions for EPCI workflows.
  Use when: {state operations needed}.
  Internal component for EPCI v6.0.
user-invocable: false
disable-model-invocation: false
allowed-tools: Read, Write, Glob
---

# {State Component}

Manages {state type} persistence.

## Storage Location

```
.epci/{location}/
├── {file1}.json
└── {file2}.json
```

## API

| Function | Description | Returns |
|----------|-------------|---------|
| `init()` | Initialize state | State object |
| `load(id)` | Load existing | State or null |
| `save(state)` | Persist | Boolean |
| `update(partial)` | Partial update | Updated state |

## Schema

```json
{
  "$schema": "...",
  "id": "string",
  "created_at": "ISO8601",
  "updated_at": "ISO8601",
  "data": {}
}
```

## Usage

```
state = component.init()
state = component.load("id")
component.save(state)
```
```

---

## File Structure Examples

### Simple Structure
```
skills/{name}/
└── SKILL.md
```

### Standard Structure
```
skills/{name}/
├── SKILL.md
└── references/
    ├── guide.md
    └── examples.md
```

### Advanced Structure
```
skills/{name}/
├── SKILL.md
├── references/
│   ├── detailed-guide.md
│   ├── checklist.md
│   └── examples.md
├── templates/
│   └── output.md
└── scripts/
    └── helper.py
```

### Core Structure
```
skills/core/{name}/
└── SKILL.md
```

---

## Checklist Before Using Template

- [ ] Choose appropriate template for skill type
- [ ] Replace all `{placeholders}`
- [ ] Verify description follows formula
- [ ] Add specific examples
- [ ] Define clear limitations
- [ ] Remove unused sections
