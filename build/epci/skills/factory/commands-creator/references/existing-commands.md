# Existing Commands Reference

Reference catalog of all existing EPCI commands for consistency and inspiration.

## Commands Overview (6)

### /brief
- **Purpose**: Entry point - analyzes brief, evaluates complexity, routes to workflow
- **Arguments**: None (receives raw brief)
- **Output**: Structured functional brief + routing recommendation
- **Tools**: Read, Glob, Grep, Bash, Task
- **Invokes**: @Explore (medium)

### /epci
- **Purpose**: Full 3-phase workflow for STANDARD/LARGE features
- **Arguments**: `[--large]` `[--continue]`
- **Output**: Complete Feature Document
- **Tools**: Read, Write, Edit, Bash, Grep, Glob, Task
- **Phases**:
  1. Analysis → @Plan, @plan-validator
  2. Code → @code-reviewer, @security-auditor*, @qa-reviewer*
  3. Finalize → @doc-generator

### /quick
- **Purpose**: Condensed workflow for TINY/SMALL features
- **Arguments**: None
- **Output**: Implemented code (no Feature Document)
- **Tools**: Read, Write, Edit, Bash, Grep, Glob, Task
- **Modes**: TINY (<50 LOC), SMALL (<200 LOC)

### /brainstorm
- **Purpose**: Feature discovery and technical exploration (includes spike command)
- **Arguments**: `[topic]` or `spike [duration] [question]`
- **Output**: Structured brief or Spike Report with GO/NO-GO verdict
- **Tools**: Read, Glob, Grep, Bash, Task, WebFetch

### /epci:create
- **Purpose**: Component Factory dispatcher
- **Arguments**: `skill|command|agent <name>`
- **Output**: New component created and validated
- **Tools**: Read, Write, Glob, Bash
- **Routes to**: skills-creator, commands-creator, subagents-creator

## Frontmatter Patterns

### Standard Command
```yaml
---
description: >-
  [Action in infinitive]. [Context]. [Result].
argument-hint: [args] [--flags]
allowed-tools: [Tool1, Tool2, ...]
---
```

### Workflow Command
```yaml
---
description: >-
  [Multi-phase workflow description]. [Purpose].
  [When to use vs alternatives].
argument-hint: [--modifier] [--continue]
allowed-tools: [Read, Write, Edit, Bash, Grep, Glob, Task]
---
```

## Structural Patterns

### Standard Sections
1. **Overview** — What the command does
2. **Arguments** — Table with argument/flag details
3. **Process** — Numbered steps with descriptions
4. **Loaded Skills** — Skills activated by command
5. **Invoked Subagents** — Subagents called and when
6. **Output** — Expected output format
7. **Examples** — Usage examples

### Process Patterns

#### Single-Pass Command
```markdown
## Process
1. Input validation
2. Main operation
3. Output generation
```

#### Multi-Phase Command
```markdown
## Process
### Phase 1: [Name]
[Description]
**BREAKPOINT**: User confirmation

### Phase 2: [Name]
[Description]
**BREAKPOINT**: User confirmation

### Phase 3: [Name]
[Description]
```

## Tool Recommendations

| Command Type | Recommended Tools |
|--------------|-------------------|
| Read-only analysis | Read, Grep, Glob |
| Code generation | Read, Write, Edit, Bash |
| Full workflow | Read, Write, Edit, Bash, Grep, Glob, Task |
| Exploration | Read, Glob, Grep, Bash, Task, WebFetch |

## Description Best Practices

### Good Patterns
- Start with infinitive verb
- Include context of use
- Mention output/result
- Keep under 200 chars

### Examples
```
✅ "Analyze the brief, evaluate complexity and route to appropriate workflow."
✅ "Execute full EPCI 3-phase workflow for STANDARD/LARGE features."
❌ "This command is used to analyze things." (vague)
❌ "The brief analyzer." (no verb, no context)
```
