---
name: commands-creator
description: >-
  Guided creation of new Claude Code commands. Workflow with templates,
  frontmatter validation and structure. Use when: /epci:create command invoked.
  Not for: modifying existing commands, skills or subagents.
---

# Commands Creator

## Overview

Guides new command creation with automatic validation.

## Workflow

### Phase 1: Qualification

Questions to define the command:

1. **Objective**: What does this command do?
2. **Arguments**: What arguments does it accept?
3. **Tools**: What tools are needed?
4. **Output**: What is the expected result?
5. **Integrations**: What skills/subagents does it use?

### Phase 2: Frontmatter Definition

```yaml
---
description: >-
  [Action in infinitive]. [Usage context]. [Expected result].
  [Constraints or limitations if any].
argument-hint: [arg1] [arg2] [--flag]
allowed-tools: [Read, Write, Edit, Bash, Grep, Glob, Task]
---
```

### Phase 3: Content Structure

```markdown
# [Command Name]

## Overview
[Description in 2-3 sentences]

## Arguments
| Argument | Description | Default |
|----------|-------------|---------|
| `arg1` | Description | - |
| `--flag` | Description | false |

## Process
### Step 1: [Name]
[Detailed description]

### Step 2: [Name]
[Detailed description]

## Loaded Skills
- `skill-1` (reason)
- `skill-2` (reason)

## Invoked Subagents
- `@subagent-1` — Role

## Output
[Expected output format]

## Examples
[Usage examples]
```

### Phase 4: Validation

```bash
python src/scripts/validate_command.py src/commands/[name].md
```

**Criteria:**
- [ ] .md file exists
- [ ] Valid YAML frontmatter
- [ ] Description present and clear
- [ ] Valid allowed-tools
- [ ] Structure with headers

## Template

```markdown
---
description: >-
  [Main action of the command]. [Usage context].
  [What the command produces as result].
argument-hint: [arguments-and-flags]
allowed-tools: [Read, Write, Edit, Bash, Grep, Glob, Task]
---

# [Command Name]

## Overview

[Command description in 2-3 sentences. Include main use case
and type of project/context where it's useful.]

## Arguments

| Argument | Description | Required | Default |
|----------|-------------|----------|---------|
| `[arg]` | Description | Yes/No | - |
| `--[flag]` | Description | No | false |

## Process

### 1. [First step]

[Step description]

```
[Code or pseudo-code if applicable]
```

### 2. [Second step]

[Step description]

### 3. [Third step]

[Step description]

## Loaded Skills

- `[skill-1]` — [Loading reason]
- `[skill-2]` — [Loading reason]

## Invoked Subagents

| Subagent | Condition | Role |
|----------|-----------|------|
| `@[name]` | [When] | [What it does] |

## Output

[Output format description]

```markdown
[Output example]
```

## Examples

### Example 1: [Use case]

```
> /[command] [arguments]

[Expected result]
```

### Example 2: [Another case]

```
> /[command] --[flag] [arguments]

[Expected result]
```

## Common Errors

| Error | Cause | Solution |
|-------|-------|----------|
| [Error 1] | [Cause] | [Solution] |

## See Also

- `/[related-command]` — [Relationship]
```

## Best Practices

### Description

| Do | Avoid |
|----|-------|
| Infinitive verb | Passive form |
| Concise (< 200 chars) | Too long description |
| Clear context | Technical jargon |

### Arguments

| Do | Avoid |
|----|-------|
| Explicit names | Cryptic abbreviations |
| Default values | All required |
| Complete documentation | Args without description |

### Process

| Do | Avoid |
|----|-------|
| Numbered steps | Confusing flow |
| Clear conditions | Implicit logic |
| Concrete examples | Abstract descriptions |

## Output

```markdown
✅ **COMMAND CREATED**

Command: [name]
File: src/commands/[name].md

Validation: ✅ PASSED (5/5 checks)

Next steps:
1. Customize the process
2. Add examples
3. Test the command
```

## Available Tools

| Tool | Usage |
|------|-------|
| `Read` | File reading |
| `Write` | File creation |
| `Edit` | File modification |
| `Bash` | Shell commands |
| `Grep` | Code search |
| `Glob` | File pattern matching |
| `Task` | Subagent invocation |
| `WebFetch` | HTTP requests |
| `TodoRead/Write` | Task management |
