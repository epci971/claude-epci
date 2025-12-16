---
description: >-
  EPCI Component Factory. Creates new components (skills, commands,
  subagents) following EPCI standards. Dispatches to the appropriate
  creator skill.
argument-hint: skill|command|agent <name>
allowed-tools: [Read, Write, Glob, Bash]
---

# EPCI Create — Component Factory

## Overview

Dispatcher command to create new EPCI components.
Routes to the appropriate creator skill based on requested type.

## Usage

```
/epci:create <type> <name>
```

| Argument | Description | Examples |
|----------|-------------|----------|
| `type` | Component type | `skill`, `command`, `agent` |
| `name` | Component name (kebab-case) | `my-new-skill` |

## Routing

| Type | Invoked Skill | Output |
|------|---------------|--------|
| `skill` | `skills-creator` | `skills/<category>/<name>/SKILL.md` |
| `command` | `commands-creator` | `commands/<name>.md` |
| `agent` | `subagents-creator` | `agents/<name>.md` |

## Process

### 1. Argument Validation

```
If type missing → Error + usage
If name missing → Error + usage
If name not kebab-case → Error + expected format
If component exists → Error + suggestion
```

### 2. Routing to Creator Skill

```
switch (type):
    case "skill":
        → Invoke skill `skills-creator`
    case "command":
        → Invoke skill `commands-creator`
    case "agent":
        → Invoke skill `subagents-creator`
    default:
        → Error: unknown type
```

### 3. Interactive Phase (handled by skill)

The invoked creator skill guides the user through:
- Questions about the component
- Template generation
- Customization
- Validation
- Tests

## Examples

### Create a Skill

```
> /epci:create skill api-monitoring

→ Invokes skills-creator
→ Interactive questions about the skill
→ Generates skills/custom/api-monitoring/SKILL.md
→ Validates with validate_skill.py
→ Tests triggering
```

### Create a Command

```
> /epci:create command deploy

→ Invokes commands-creator
→ Questions about the command
→ Generates commands/deploy.md
→ Validates with validate_command.py
```

### Create a Subagent

```
> /epci:create agent perf-analyzer

→ Invokes subagents-creator
→ Questions about the subagent
→ Generates agents/perf-analyzer.md
→ Validates with validate_subagent.py
```

## Validation

After creation, the appropriate validation script is executed:

| Type | Script |
|------|--------|
| skill | `python scripts/validate_skill.py <path>` |
| command | `python scripts/validate_command.py <path>` |
| agent | `python scripts/validate_subagent.py <path>` |

## Naming Conventions

| Element | Convention | Example |
|---------|------------|---------|
| Name | kebab-case | `my-component` |
| Length | ≤ 64 characters | - |
| Characters | a-z, 0-9, - | - |

## Common Errors

### Invalid Type

```
❌ Type 'service' not recognized.

Supported types:
- skill    → Creates a new skill
- command  → Creates a new command
- agent    → Creates a new subagent

Usage: /epci:create <type> <name>
```

### Invalid Name

```
❌ Name 'MySkill' invalid.

Name must be kebab-case:
- Only lowercase, digits and hyphens
- No hyphen at start or end
- Maximum 64 characters

Correct example: my-skill
```

### Existing Component

```
❌ Skill 'api-monitoring' already exists.

Options:
1. Choose another name
2. Modify existing skill: skills/custom/api-monitoring/SKILL.md
3. Delete existing first
```

## Output

```
✅ **COMPONENT CREATED**

Type: [skill | command | agent]
Name: [name]
File: [path]

Validation: ✅ PASSED (X/Y checks)

Next steps:
1. Customize the content
2. Test the component
3. Document usage
```

## Factory Skills Tree

```
skills/factory/
├── skills-creator/
│   ├── SKILL.md
│   ├── references/
│   │   └── skill-anatomy.md
│   ├── templates/
│   │   ├── core-skill.md
│   │   └── stack-skill.md
│   └── scripts/
│       └── post-create.py
│
├── commands-creator/
│   ├── SKILL.md
│   ├── references/
│   │   └── command-anatomy.md
│   └── templates/
│       └── command-template.md
│
├── subagents-creator/
│   ├── SKILL.md
│   ├── references/
│   │   └── agent-anatomy.md
│   └── templates/
│       └── agent-template.md
│
└── component-advisor/
    └── SKILL.md
```

## Skills Loaded

- `component-advisor` (passive opportunity detection)
- `flags-system` (ensures new components are flags-aware)
- `[creator-skill]` (based on requested type)

## Flags Support

Components created by this command are automatically flags-aware:

- **Commands**: Include `argument-hint` with relevant flags
- **Skills**: Reference `flags-system` skill when applicable
- **Agents**: Receive active flags via `HookContext`
