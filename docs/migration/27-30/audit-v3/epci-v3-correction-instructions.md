# EPCI v3 — Instructions de Correction pour Claude Code

## OBJECTIF

Corriger et compléter l'implémentation EPCI v3 selon le cahier des charges.
Les fichiers sont dans le dossier du plugin EPCI.

---

## TÂCHE 1 : TRADUCTION FR → EN (CRITIQUE)

### Règles de traduction

1. **Conserver la structure YAML frontmatter**
2. **Traduire tout le texte** (titres, descriptions, commentaires, exemples)
3. **Garder les noms techniques** (kebab-case, noms de fichiers, noms de commandes)
4. **Conserver les emojis et symboles** (✅, ❌, 🔴, etc.)

### Exemple de transformation

```markdown
# AVANT (Français)
---
description: >-
  Point d'entrée EPCI. Analyse le brief brut, clarifie les ambiguïtés via
  questions itératives, évalue la complexité et route vers le workflow
  approprié.
---

# EPCI Brief — Point d'entrée

## Overview

Cette commande est le point d'entrée unique du workflow EPCI.

## Process

### Étape 1 : Analyse initiale

**Invoquer @Explore** (niveau medium) pour :
- Scanner la structure du projet
- Identifier les technologies utilisées
```

```markdown
# APRÈS (Anglais)
---
description: >-
  EPCI entry point. Analyzes raw brief, clarifies ambiguities through
  iterative questions, evaluates complexity and routes to appropriate
  workflow.
---

# EPCI Brief — Entry Point

## Overview

This command is the single entry point for the EPCI workflow.

## Process

### Step 1: Initial Analysis

**Invoke @Explore** (medium level) to:
- Scan project structure
- Identify technologies used
```

### Fichiers à traduire

Exécuter pour chaque fichier :

```
commands/epci-brief.md
commands/epci.md
commands/epci-quick.md
commands/epci-spike.md
commands/create.md
agents/plan-validator.md
agents/code-reviewer.md
agents/security-auditor.md
agents/qa-reviewer.md
agents/doc-generator.md
skills/core/epci-core/SKILL.md
skills/core/architecture-patterns/SKILL.md
skills/core/code-conventions/SKILL.md
skills/core/testing-strategy/SKILL.md
skills/core/git-workflow/SKILL.md
skills/stack/php-symfony/SKILL.md
skills/stack/javascript-react/SKILL.md
skills/stack/python-django/SKILL.md
skills/stack/java-springboot/SKILL.md
skills/factory/skills-creator/SKILL.md
skills/factory/commands-creator/SKILL.md
skills/factory/subagents-creator/SKILL.md
skills/factory/component-advisor/SKILL.md
```

---

## TÂCHE 2 : CRÉER FICHIERS REFERENCES (CRITIQUE)

### skills/factory/skills-creator/references/

#### best-practices.md

```markdown
# Skill Best Practices

## The 10 Golden Rules

1. **Kebab-case naming** — `my-skill` not `MySkill`
2. **Formulated description** — Always include "Use when:" + "Not for:"
3. **Single focus** — One skill = one domain
4. **Auto-detectable** — Clear trigger conditions
5. **Explicit exclusions** — Avoid false positives
6. **Content < 5000 tokens** — Fast loading
7. **Structured with headers** — Easy navigation
8. **Practical examples** — Code, tables, patterns
9. **Quick Reference section** — Fast lookup
10. **Anti-patterns section** — What to avoid

## Common Mistakes

| Mistake | Problem | Solution |
|---------|---------|----------|
| Vague description | Won't auto-trigger | Add specific "Use when" conditions |
| Too broad scope | Triggers too often | Narrow down with "Not for" |
| No examples | Hard to understand | Add code snippets |
| Missing Quick Reference | Slow lookup | Add summary table |

## Quality Checklist

- [ ] Name is kebab-case and ≤64 characters
- [ ] Description includes "Use when:" clause
- [ ] Description includes "Not for:" clause
- [ ] Description is ≤1024 characters
- [ ] Content has clear headers
- [ ] Content includes practical examples
- [ ] Content is < 5000 tokens
- [ ] Has Quick Reference section
```

#### description-formulas.md

```markdown
# Skill Description Formulas

## Required Structure

```
[Capability statement]. [Technologies/tools included].
Use when: [specific trigger conditions].
Not for: [explicit exclusions].
```

## Formula Patterns

### Pattern 1: Technology Skill

```
Patterns and conventions for [Tech/Framework]. Includes [tools, libraries].
Use when: developing with [tech], [detection file] detected.
Not for: [other techs], [other frameworks].
```

**Example:**
```
Patterns and conventions for PHP/Symfony. Includes Doctrine ORM, PHPUnit,
Twig, services and bundles. Use when: Symfony development, composer.json
with symfony detected. Not for: Laravel, plain PHP, other frameworks.
```

### Pattern 2: Concept Skill

```
[Domain] concepts and patterns. Covers [aspects].
Use when: [situations], [contexts].
Not for: [exclusions].
```

**Example:**
```
Software architecture patterns. Covers DDD, Clean Architecture,
CQRS, microservices patterns. Use when: evaluating complexity,
choosing architecture, structural refactoring. Not for: code conventions
(→ code-conventions), stack-specific patterns (→ stack skills).
```

### Pattern 3: Process Skill

```
[Process/Workflow] guidelines. Includes [components].
Use when: [phase], [activity].
Not for: [exclusions].
```

**Example:**
```
Git workflow and commit conventions. Includes branching strategy,
Conventional Commits, PR workflow. Use when: Phase 3 finalization,
committing, PR preparation. Not for: basic git commands.
```

## Length Guidelines

| Element | Min | Max | Ideal |
|---------|-----|-----|-------|
| Full description | 100 | 1024 | 200-400 |
| "Use when" clause | 20 | 200 | 50-100 |
| "Not for" clause | 10 | 100 | 30-50 |
```

#### yaml-rules.md

```markdown
# YAML Frontmatter Rules

## Required Fields

```yaml
---
name: skill-name          # Required: kebab-case, ≤64 chars
description: >-           # Required: ≤1024 chars, with formulas
  [description text]
---
```

## Optional Fields

```yaml
---
name: skill-name
description: >-
  [description]
allowed-tools: [Read, Write, Bash]  # Optional: restrict tools
---
```

## Validation Rules

### name
- Format: `^[a-z0-9]+(-[a-z0-9]+)*$`
- Length: 1-64 characters
- Examples: `epci-core`, `php-symfony`, `code-conventions`

### description
- Length: 1-1024 characters
- Must contain: "Use when:" (case-insensitive)
- Should contain: "Not for:" (case-insensitive)
- Use `>-` for multi-line (strips newlines)

### allowed-tools
- Type: Array of strings
- Valid values: Read, Write, Edit, Bash, Grep, Glob, Task, WebFetch, LS, MultiEdit
- Default: All tools allowed if omitted

## Common Errors

| Error | Cause | Fix |
|-------|-------|-----|
| YAML parse error | Bad indentation | Use 2-space indent |
| Invalid name | Uppercase or spaces | Use kebab-case |
| Description too long | >1024 chars | Shorten, use references |
| Missing Use when | No trigger conditions | Add explicit conditions |
```

#### checklist.md

```markdown
# Skill Validation Checklist

## Pre-Creation

- [ ] Identified clear use case
- [ ] Verified no existing skill covers this
- [ ] Defined trigger conditions
- [ ] Listed explicit exclusions
- [ ] Estimated content size (< 5000 tokens)

## Frontmatter

- [ ] name is kebab-case
- [ ] name is ≤64 characters
- [ ] description exists and is not empty
- [ ] description is ≤1024 characters
- [ ] description contains "Use when:"
- [ ] description contains "Not for:"
- [ ] YAML syntax is valid

## Content Structure

- [ ] Has Overview section
- [ ] Has at least one main content section
- [ ] Has Quick Reference or summary table
- [ ] Headers are properly nested (h2, h3, h4)
- [ ] Code examples are fenced and have language tags

## Quality

- [ ] Content is < 5000 tokens
- [ ] Examples are practical and runnable
- [ ] Anti-patterns are documented
- [ ] No duplicate information with other skills
- [ ] References exist if mentioned

## Testing

- [ ] validate_skill.py passes
- [ ] test_triggering.py passes
- [ ] Manual test with sample queries
```

### skills/factory/commands-creator/references/

#### best-practices.md

```markdown
# Command Best Practices

## Design Principles

1. **Single responsibility** — One command = one workflow
2. **Clear arguments** — Explicit, documented parameters
3. **Minimal tools** — Only required tools in allowed-tools
4. **Structured output** — Predictable result format
5. **Error handling** — Clear error messages

## Naming Conventions

| Element | Convention | Example |
|---------|------------|---------|
| File name | kebab-case.md | `epci-brief.md` |
| Command name | /prefix-name | `/epci-brief` |
| Subcommand | /prefix:action | `/epci:create` |
| Arguments | [required] --optional | `[type] --verbose` |

## Description Guidelines

- Start with action verb (infinitive)
- State the purpose clearly
- Mention key outputs
- Keep under 200 characters ideally

## Process Structure

1. **Input validation** — Check arguments first
2. **Analysis** — Understand context
3. **Execution** — Perform the task
4. **Output** — Present results clearly

## Common Mistakes

| Mistake | Impact | Solution |
|---------|--------|----------|
| Too many tools | Security risk | Minimize allowed-tools |
| No examples | Confusion | Add usage examples |
| Vague process | Inconsistent results | Detail each step |
| Missing error cases | Poor UX | Document error handling |
```

#### frontmatter-guide.md

```markdown
# Command Frontmatter Guide

## Required Fields

```yaml
---
description: >-
  [Action verb] [what it does]. [Context].
  [Output/result].
allowed-tools: [Tool1, Tool2]
---
```

## Optional Fields

```yaml
---
description: >-
  [description]
argument-hint: [arg1] [--flag]
allowed-tools: [Read, Write, Bash]
---
```

## Field Details

### description

Purpose: Explain what the command does
Format: Multi-line with `>-`
Length: 50-300 characters recommended

**Good example:**
```yaml
description: >-
  EPCI entry point. Analyzes raw brief, clarifies ambiguities through
  iterative questions, evaluates complexity and routes to appropriate
  workflow (/epci-quick, /epci, /epci-spike).
```

### argument-hint

Purpose: Show expected arguments in help
Format: `[required] [--optional] [<placeholder>]`

**Examples:**
```yaml
argument-hint: "[--large] [--continue]"
argument-hint: "skill|command|agent <name>"
argument-hint: "[duration] [question]"
```

### allowed-tools

Purpose: Restrict which tools the command can use
Format: Array of tool names

**Available tools:**
- `Read` — Read files
- `Write` — Create files
- `Edit` — Modify files
- `Bash` — Execute commands
- `Grep` — Search in files
- `Glob` — Find files by pattern
- `Task` — Invoke subagents
- `WebFetch` — HTTP requests
- `LS` — List directories
- `MultiEdit` — Batch edits

**Principle:** Include only necessary tools
```

#### argument-patterns.md

```markdown
# Command Argument Patterns

## Syntax

| Pattern | Meaning | Example |
|---------|---------|---------|
| `<arg>` | Required positional | `<name>` |
| `[arg]` | Optional positional | `[type]` |
| `--flag` | Boolean flag | `--verbose` |
| `--opt=value` | Option with value | `--timeout=30` |
| `arg1|arg2` | Choice | `skill|command|agent` |

## Common Patterns

### No arguments
```yaml
argument-hint: ""
# or omit entirely
```

### Single required argument
```yaml
argument-hint: "<name>"
```

### Optional flags
```yaml
argument-hint: "[--large] [--continue]"
```

### Mixed positional and flags
```yaml
argument-hint: "<type> <name> [--force]"
```

### Choice argument
```yaml
argument-hint: "skill|command|agent <name>"
```

## Accessing Arguments

In command body, arguments are available as:
- `$ARGUMENTS` — Full argument string
- `$1`, `$2`, etc. — Positional arguments
- Check for flags with string matching

## Validation

Always validate arguments at the start:

```markdown
### Step 1: Validate Arguments

```
If type missing → Error + usage
If name missing → Error + usage  
If name not kebab-case → Error + format
If component exists → Error + suggestion
```
```
```

#### checklist.md

```markdown
# Command Validation Checklist

## File Structure

- [ ] File is in commands/ directory
- [ ] File name is kebab-case.md
- [ ] File has YAML frontmatter

## Frontmatter

- [ ] description field exists
- [ ] description is clear and actionable
- [ ] allowed-tools is appropriate (not too broad)
- [ ] argument-hint present if command has arguments

## Content

- [ ] Has Overview section
- [ ] Has Arguments table (if applicable)
- [ ] Has Process section with clear steps
- [ ] Has Skills loaded section
- [ ] Has Subagents section (if applicable)
- [ ] Has Output section with examples
- [ ] Has Examples section

## Quality

- [ ] Steps are numbered and clear
- [ ] Error cases are documented
- [ ] Examples are realistic
- [ ] No placeholder content
```

### skills/factory/subagents-creator/references/

#### best-practices.md

```markdown
# Subagent Best Practices

## Core Principles

1. **Single mission** — One agent = one focused task
2. **Minimal tools** — Least privilege principle
3. **Clear output** — Structured, predictable format
4. **Defined scope** — Explicit boundaries

## Mission Design

### Good Missions

- "Validate implementation plan before Phase 2"
- "Review code quality and architecture"
- "Audit security vulnerabilities (OWASP)"
- "Generate documentation for changes"

### Bad Missions

- "Help with development" (too vague)
- "Check everything" (too broad)
- "Do multiple things" (not focused)

## Tool Selection

| Mission Type | Recommended Tools |
|--------------|-------------------|
| Analysis/Read | Read, Grep, Glob |
| Validation | Read, Grep |
| Generation | Read, Write |
| Execution | Read, Bash |

### Tools to Avoid Unless Necessary

- `Write` — If agent only reads/analyzes
- `Edit` — If agent doesn't modify files
- `Bash` — If no command execution needed
- `WebFetch` — If no external requests needed

## Output Structure

Always include:
1. **Summary** — 1-2 sentence overview
2. **Details** — Structured findings
3. **Verdict** — Clear decision (APPROVED, NEEDS_FIXES, etc.)
4. **Reasoning** — Justification for verdict

## Severity Levels

| Level | Symbol | Meaning | Action |
|-------|--------|---------|--------|
| Critical | 🔴 | Blocking issue | Must fix |
| Important | 🟠 | Significant issue | Should fix |
| Minor | 🟡 | Improvement | Nice to have |
```

#### delegation-patterns.md

```markdown
# Subagent Delegation Patterns

## Invocation Types

### Automatic (Conditional)

Agent is invoked automatically when conditions are met:

```markdown
## Invocation Conditions

Automatically invoked if:
- Files matching `**/auth/**` detected
- Keywords `password`, `secret`, `api_key` found
- More than 5 test files modified
```

### Explicit

Agent is invoked by user or command:

```markdown
## Invocation

Invoked by `/epci` command during Phase 2.
Can also be invoked manually: `@code-reviewer`
```

## Delegation Flow

```
Command
    │
    ├─► @agent-1 (always)
    │       │
    │       └─► Report
    │
    ├─► @agent-2 (if condition)
    │       │
    │       └─► Report
    │
    └─► Synthesize results
```

## Input/Output Contract

### Input

Define what the agent receives:
- Context (Feature Document, files, etc.)
- Specific instructions
- Scope limitations

### Output

Define what the agent produces:
- Report format (markdown)
- Verdict types (APPROVED, NEEDS_FIXES, etc.)
- Required sections

## Communication

### Agent to Command

```markdown
## Output

Report in this format:

### Summary
[Brief assessment]

### Findings
[Detailed issues]

### Verdict
**[APPROVED | NEEDS_FIXES]**
```

### Between Agents

Agents don't communicate directly.
Command orchestrates and passes context.
```

#### tools-restriction.md

```markdown
# Subagent Tools Restriction Guide

## Principle of Least Privilege

**Only grant tools necessary for the mission.**

## Tool Risk Assessment

| Tool | Risk Level | Use When |
|------|------------|----------|
| Read | Low | Always OK for analysis |
| Grep | Low | Searching in code |
| Glob | Low | Finding files |
| Bash | Medium | Running tests, linting |
| Write | Medium | Generating docs |
| Edit | High | Modifying code |
| WebFetch | Medium | External checks |
| Task | High | Calling other agents |

## Recommended Tool Sets

### Read-Only Analysis

```yaml
allowed-tools: [Read, Grep, Glob]
```

Use for: Validators, reviewers, auditors

### With Execution

```yaml
allowed-tools: [Read, Grep, Glob, Bash]
```

Use for: Agents that run tests or commands

### Generation

```yaml
allowed-tools: [Read, Write, Glob]
```

Use for: Documentation generators

### Full Access (Rare)

```yaml
allowed-tools: [Read, Write, Edit, Bash, Grep, Glob]
```

Use for: Complex agents with multiple responsibilities
**Warning:** Avoid if possible

## Warning Signs

| Sign | Problem | Solution |
|------|---------|----------|
| >5 tools | Too broad | Split into multiple agents |
| Write without need | Risk | Remove if not generating |
| Edit for reader | Overkill | Use Read only |
| All tools | No restriction | Review mission scope |

## Validation

When reviewing an agent's tools:

1. List each tool
2. Justify why it's needed
3. Remove if justification is weak
4. Test with minimal set
```

#### checklist.md

```markdown
# Subagent Validation Checklist

## Frontmatter

- [ ] name is kebab-case
- [ ] name is ≤64 characters
- [ ] description describes single mission
- [ ] model is specified (sonnet or haiku)
- [ ] allowed-tools is minimal (least privilege)

## Mission

- [ ] Mission is clearly stated
- [ ] Mission is single-focused (not multi-task)
- [ ] Scope is well-defined
- [ ] Exclusions are documented

## Invocation

- [ ] Conditions for invocation are clear
- [ ] Auto vs explicit is specified
- [ ] Parent command/context is documented

## Input/Output

- [ ] Expected input is documented
- [ ] Output format is specified
- [ ] Verdict types are defined
- [ ] Example output is provided

## Checklist Content

- [ ] Has categorized checklist items
- [ ] Items are verifiable (yes/no)
- [ ] Items are actionable

## Severity

- [ ] Severity levels are defined
- [ ] Each level has clear criteria
- [ ] Actions per level are specified

## Quality

- [ ] Content is < 2000 tokens
- [ ] No duplicate with other agents
- [ ] Tools are justified
```

---

## TÂCHE 3 : CRÉER FICHIERS TEMPLATES

### skills/factory/skills-creator/templates/

#### skill-simple.md

```markdown
---
name: [skill-name]
description: >-
  [Capability description]. Use when: [trigger conditions].
  Not for: [exclusions].
---

# [Skill Name]

## Overview

[2-3 sentences describing what this skill provides and when to use it.]

## Key Concepts

| Concept | Description |
|---------|-------------|
| [Concept 1] | [Brief explanation] |
| [Concept 2] | [Brief explanation] |
| [Concept 3] | [Brief explanation] |

## Patterns

### [Pattern 1 Name]

[Description of when and how to use this pattern]

```[language]
[Code example]
```

### [Pattern 2 Name]

[Description]

```[language]
[Code example]
```

## Quick Reference

| Situation | Recommendation |
|-----------|----------------|
| [Situation 1] | [What to do] |
| [Situation 2] | [What to do] |
| [Situation 3] | [What to do] |

## Anti-patterns

| Anti-pattern | Problem | Solution |
|--------------|---------|----------|
| [Bad practice] | [Why it's bad] | [Better approach] |
```

#### skill-advanced.md

```markdown
---
name: [skill-name]
description: >-
  [Capability description]. Includes [components].
  Use when: [trigger conditions]. Not for: [exclusions].
---

# [Skill Name]

## Overview

[Detailed description of the skill's purpose, scope, and value.]

## Auto-detection

Loaded automatically when:
- [Detection condition 1]
- [Detection condition 2]
- [Detection condition 3]

## Architecture

### Structure

```
[directory-structure]
```

### Conventions

| Element | Convention | Example |
|---------|------------|---------|
| [Element 1] | [Convention] | [Example] |
| [Element 2] | [Convention] | [Example] |

## Patterns

### [Pattern Category 1]

#### [Specific Pattern]

[Description]

```[language]
[Detailed code example]
```

### [Pattern Category 2]

[...]

## Testing

### [Test Type 1]

```[language]
[Test example]
```

### [Test Type 2]

```[language]
[Test example]
```

## Commands

```bash
# [Category 1]
[command 1]
[command 2]

# [Category 2]
[command 3]
```

## Best Practices

| Practice | Do | Don't |
|----------|-----|-------|
| [Practice 1] | [Good approach] | [Bad approach] |
| [Practice 2] | [Good approach] | [Bad approach] |

## Quick Reference

[Summary table or cheatsheet]

## References

- [Link to official docs]
- [Link to related resources]
```

### skills/factory/commands-creator/templates/

#### command-simple.md

```markdown
---
description: >-
  [Action verb] [what it does]. [Output/result].
allowed-tools: [Read, Write, Bash]
---

# [Command Name]

## Overview

[2-3 sentences describing command purpose]

## Process

### Step 1: [Name]

[Description]

### Step 2: [Name]

[Description]

### Step 3: [Name]

[Description]

## Output

```markdown
[Example output format]
```

## Examples

### Example: [Use Case]

```
> /[command]

[Expected result]
```
```

#### command-advanced.md

```markdown
---
description: >-
  [Detailed description of command purpose and behavior].
argument-hint: [args] [--flags]
allowed-tools: [Read, Write, Edit, Bash, Grep, Glob, Task]
---

# [Command Name]

## Overview

[Detailed description]

## Arguments

| Argument | Description | Required | Default |
|----------|-------------|----------|---------|
| `[arg]` | [Description] | Yes/No | [value] |
| `--flag` | [Description] | No | false |

## Process

### Step 1: [Name]

[Detailed description]

```
[Code or pseudo-code]
```

### Step 2: [Name]

[...]

## Skills Loaded

- `[skill-1]` — [Why loaded]
- `[skill-2]` — [Why loaded]

## Subagents Invoked

| Subagent | Condition | Role |
|----------|-----------|------|
| `@[agent]` | [When] | [What it does] |

## Output

[Description]

```markdown
[Example output]
```

## Examples

### Example 1: [Basic Use Case]

```
> /[command] [args]

[Result]
```

### Example 2: [Advanced Use Case]

```
> /[command] --flag [args]

[Result]
```

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| [Error 1] | [Cause] | [Fix] |

## See Also

- `/[related-command]` — [Relationship]
```

### skills/factory/subagents-creator/templates/

#### subagent-template.md

```markdown
---
name: [agent-name]
description: >-
  [Mission in 1-2 sentences]. [When invoked].
  [What it produces].
model: claude-sonnet-4-20250514
allowed-tools: [Read, Grep]
---

# [Agent Name] Agent

## Mission

[Clear description of the single mission this agent fulfills.]

## Invocation Conditions

Automatically invoked if:
- [Condition 1]
- [Condition 2]

OR manually invoked by:
- [Command/context]

## Input

- [Input 1] — [Description]
- [Input 2] — [Description]

## Checklist

### [Category 1]

- [ ] [Verifiable criterion 1]
- [ ] [Verifiable criterion 2]
- [ ] [Verifiable criterion 3]

### [Category 2]

- [ ] [Verifiable criterion 4]
- [ ] [Verifiable criterion 5]

## Severity Levels

| Level | Criteria | Action |
|-------|----------|--------|
| 🔴 Critical | [Definition] | Must fix |
| 🟠 Important | [Definition] | Should fix |
| 🟡 Minor | [Definition] | Nice to have |

## Output Format

```markdown
## [Report Title]

### Summary
[1-2 sentences]

### Findings

#### 🔴 Critical
1. **[Issue title]**
   - **Location**: [file:line]
   - **Issue**: [Description]
   - **Fix**: [Suggested solution]

### Verdict
**[APPROVED | NEEDS_FIXES | REJECTED]**

**Reasoning:** [Technical justification]
```

## Process

1. [Step 1]
2. [Step 2]
3. [Step 3]
```

---

## TÂCHE 4 : MODIFIER plugin.json

Remplacer le contenu de `.claude-plugin/plugin.json` par :

```json
{
  "name": "epci",
  "version": "3.0.0",
  "description": "EPCI (Explore → Plan → Code → Inspect) - Structured development workflow with full traceability",
  "author": {
    "name": "EPCI Team"
  },
  "license": "MIT",
  "commands": [
    {
      "name": "epci-brief",
      "file": "./commands/epci-brief.md",
      "description": "EPCI entry point - analyzes brief and routes to appropriate workflow"
    },
    {
      "name": "epci",
      "file": "./commands/epci.md",
      "description": "Complete 3-phase workflow for STANDARD and LARGE features"
    },
    {
      "name": "epci-quick",
      "file": "./commands/epci-quick.md",
      "description": "Condensed workflow for TINY and SMALL features"
    },
    {
      "name": "epci-spike",
      "file": "./commands/epci-spike.md",
      "description": "Time-boxed exploration for technical uncertainties"
    },
    {
      "name": "epci:create",
      "file": "./commands/create.md",
      "description": "Component Factory - creates skills, commands, or subagents"
    }
  ],
  "agents": [
    {
      "name": "plan-validator",
      "file": "./agents/plan-validator.md",
      "description": "Validates Phase 1 implementation plan"
    },
    {
      "name": "code-reviewer",
      "file": "./agents/code-reviewer.md",
      "description": "Reviews code quality by Phase 2"
    },
    {
      "name": "security-auditor",
      "file": "./agents/security-auditor.md",
      "description": "OWASP security audit (conditional)"
    },
    {
      "name": "qa-reviewer",
      "file": "./agents/qa-reviewer.md",
      "description": "Test strategy review (conditional)"
    },
    {
      "name": "doc-generator",
      "file": "./agents/doc-generator.md",
      "description": "Generates documentation in Phase 3"
    }
  ],
  "skills": [
    {
      "name": "epci-core",
      "path": "./skills/core/epci-core/",
      "description": "EPCI core concepts and workflow"
    },
    {
      "name": "architecture-patterns",
      "path": "./skills/core/architecture-patterns/",
      "description": "Software architecture patterns (DDD, Clean, CQRS)"
    },
    {
      "name": "code-conventions",
      "path": "./skills/core/code-conventions/",
      "description": "Generic code conventions and best practices"
    },
    {
      "name": "testing-strategy",
      "path": "./skills/core/testing-strategy/",
      "description": "Testing strategies (TDD, pyramide, mocking)"
    },
    {
      "name": "git-workflow",
      "path": "./skills/core/git-workflow/",
      "description": "Git workflow and Conventional Commits"
    },
    {
      "name": "php-symfony",
      "path": "./skills/stack/php-symfony/",
      "description": "PHP/Symfony patterns and conventions"
    },
    {
      "name": "javascript-react",
      "path": "./skills/stack/javascript-react/",
      "description": "JavaScript/React patterns and conventions"
    },
    {
      "name": "python-django",
      "path": "./skills/stack/python-django/",
      "description": "Python/Django patterns and conventions"
    },
    {
      "name": "java-springboot",
      "path": "./skills/stack/java-springboot/",
      "description": "Java/Spring Boot patterns and conventions"
    },
    {
      "name": "skills-creator",
      "path": "./skills/factory/skills-creator/",
      "description": "Guided skill creation with validation"
    },
    {
      "name": "commands-creator",
      "path": "./skills/factory/commands-creator/",
      "description": "Guided command creation with validation"
    },
    {
      "name": "subagents-creator",
      "path": "./skills/factory/subagents-creator/",
      "description": "Guided subagent creation with validation"
    },
    {
      "name": "component-advisor",
      "path": "./skills/factory/component-advisor/",
      "description": "Detects opportunities for new components"
    }
  ],
  "keywords": [
    "epci",
    "workflow",
    "development",
    "tdd",
    "code-review",
    "documentation",
    "planning",
    "validation"
  ]
}
```

---

## TÂCHE 5 : CORRIGER validate_all.py

Dans `scripts/validate_all.py`, modifier la fonction `get_project_root()` :

```python
def get_project_root() -> Path:
    """Find project root (contains commands/, agents/, skills/)."""
    current = Path(__file__).resolve().parent
    
    # Go up until we find the plugin structure
    while current != current.parent:
        if (current / "commands").exists() and (current / "agents").exists():
            return current
        current = current.parent
    
    # Fallback: parent of scripts/
    return Path(__file__).resolve().parent.parent
```

Et modifier `validate_all()` :

```python
def validate_all(verbose: bool = False) -> int:
    """Main entry point - validates all components."""
    project_root = get_project_root()
    
    # Use project root directly, not src/
    src_path = project_root  # Changed from: project_root / "src"
    scripts_path = project_root / "scripts"
    
    # ... rest of function
```

---

## TÂCHE 6 : SUPPRIMER OU DOCUMENTER hooks/

Option A : Supprimer le dossier vide
```bash
rmdir hooks/
```

Option B : Ajouter un README
```markdown
# Hooks

This directory is reserved for future hook implementations.

## Planned Hooks

- `pre-commit` — Validate before commit
- `post-phase` — Actions after each EPCI phase
```

---

## ORDRE D'EXÉCUTION RECOMMANDÉ

1. **Traduire tous les fichiers** (Tâche 1)
2. **Créer fichiers references/** (Tâche 2)
3. **Créer fichiers templates/** (Tâche 3)
4. **Modifier plugin.json** (Tâche 4)
5. **Corriger validate_all.py** (Tâche 5)
6. **Nettoyer hooks/** (Tâche 6)
7. **Exécuter validation** : `python scripts/validate_all.py --verbose`

---

## VALIDATION FINALE

Après toutes les corrections :

```bash
# Valider la structure
python scripts/validate_all.py --verbose

# Vérifier chaque skill individuellement
for skill in skills/core/*/; do python scripts/validate_skill.py "$skill"; done
for skill in skills/stack/*/; do python scripts/validate_skill.py "$skill"; done
for skill in skills/factory/*/; do python scripts/validate_skill.py "$skill"; done

# Vérifier les commandes
for cmd in commands/*.md; do python scripts/validate_command.py "$cmd"; done

# Vérifier les agents
for agent in agents/*.md; do python scripts/validate_subagent.py "$agent"; done
```

Critères de succès :
- [ ] Tous les scripts retournent exit code 0
- [ ] Aucun WARNING sur les fichiers manquants
- [ ] plugin.json liste les 13 skills
