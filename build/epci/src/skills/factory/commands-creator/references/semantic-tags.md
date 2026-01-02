# Semantic Tags - Command Content Structure

> Standardized sections and semantic markers for command documentation

---

## Core Section Tags

### Required Sections

| Section | Purpose | Content |
|---------|---------|---------|
| `## Overview` | Command summary | 2-3 sentences describing purpose |
| `## Process` | Execution steps | Numbered workflow steps |
| `## Output` | Expected result | Format and examples |

### Optional Sections

| Section | Purpose | When to Include |
|---------|---------|-----------------|
| `## Arguments` | Parameter documentation | If command has arguments |
| `## Loaded Skills` | Skill dependencies | If skills are auto-loaded |
| `## Invoked Subagents` | Agent orchestration | If subagents are used |
| `## Examples` | Usage examples | Always recommended |
| `## Common Errors` | Troubleshooting | For complex commands |
| `## See Also` | Related commands | For command families |

---

## Semantic Markers

### Process Flow Markers

| Marker | Usage | Example |
|--------|-------|---------|
| `### Step N:` | Numbered step | `### Step 1: Initialize` |
| `### Phase N:` | Major phase | `### Phase 1: Analysis` |
| `**BREAKPOINT**` | User confirmation | Pause before destructive action |
| `**CHECKPOINT**` | Validation point | Verify before continuing |

### Conditional Markers

```markdown
### Step 3: Review (conditional)
**Condition**: Only if `--review` flag is set or changes > 10 files

[Step content]
```

### Decision Trees

```markdown
## Quick Decision

```
Input received?
      │
  ┌───┴───┐
  ▼       ▼
Valid?  Invalid?
  │       │
  ▼       ▼
Process  Error
```
```

---

## Section Templates

### Overview Template

```markdown
## Overview

[Command name] [action verb] [target] for [purpose].
[Main use case in one sentence].
[Key differentiator or constraint].
```

### Arguments Template

```markdown
## Arguments

| Argument | Description | Required | Default |
|----------|-------------|----------|---------|
| `<target>` | File or directory to process | Yes | - |
| `[--flag]` | Enable feature X | No | false |
| `[--option=value]` | Set option Y | No | "default" |
```

### Process Template

```markdown
## Process

### Step 1: Initialization
[What happens first, prerequisites]

### Step 2: Analysis
[Core processing logic]

### Step 3: Generation
[Output creation]

### Step 4: Validation
[Quality checks before completion]
```

### Output Template

```markdown
## Output

**Format**: [markdown/json/files]

```markdown
✅ **COMMAND COMPLETED**

[Summary of what was done]

Results:
- [Result 1]
- [Result 2]

Next steps:
1. [Suggested action]
```
```

---

## Skill Integration Tags

### Loading Pattern

```markdown
## Loaded Skills

| Skill | Condition | Purpose |
|-------|-----------|---------|
| `epci-core` | Always | Workflow concepts |
| `testing-strategy` | If tests involved | Test patterns |
| `[stack]-[framework]` | Auto-detected | Stack patterns |
```

### Invocation Pattern

```markdown
## Invoked Subagents

| Subagent | When | Role |
|----------|------|------|
| `@Explore` | Phase 1 | Codebase analysis |
| `@code-reviewer` | Phase 2 | Quality review |
| `@doc-generator` | Phase 3 | Documentation |
```

---

## Example Section Patterns

### Basic Example

```markdown
## Examples

### Example 1: Simple usage

```
> /command target

[Expected output]
```
```

### Complex Example with Context

```markdown
## Examples

### Example 1: React component creation

**Context**: Creating a new button component in a React project

```
> /command create-component Button --type=functional

Creating component: Button
Type: Functional component
Location: src/components/Button/

✅ Created:
- src/components/Button/Button.tsx
- src/components/Button/Button.test.tsx
- src/components/Button/Button.module.css
- src/components/Button/index.ts
```
```

---

## Error Documentation Pattern

```markdown
## Common Errors

| Error | Cause | Solution |
|-------|-------|----------|
| `FILE_NOT_FOUND` | Target doesn't exist | Check path spelling |
| `PERMISSION_DENIED` | No write access | Check file permissions |
| `VALIDATION_FAILED` | Invalid input | Review argument format |
```

---

## Cross-Reference Pattern

```markdown
## See Also

| Command | Relationship |
|---------|--------------|
| `/related-command` | Does X instead of Y |
| `/parent-command` | Higher-level workflow |
| `/helper-command` | Utility for this command |
```

---

## Best Practices

### Section Ordering

```markdown
1. ## Overview          (always first)
2. ## Arguments         (if applicable)
3. ## Process           (main content)
4. ## Loaded Skills     (if applicable)
5. ## Invoked Subagents (if applicable)
6. ## Output            (expected result)
7. ## Examples          (usage examples)
8. ## Common Errors     (troubleshooting)
9. ## See Also          (references)
```

### Semantic Consistency

| Do | Avoid |
|----|-------|
| Use standard section names | Invent new section names |
| Follow template structure | Mix different structures |
| Include all required sections | Skip Overview or Process |
| Use tables for structured data | Long prose for references |
| Numbered steps in Process | Bullet points for workflow |

---

## Quick Reference Card

```
+------------------------------------------+
|         COMMAND STRUCTURE                 |
+------------------------------------------+
| ## Overview         <- 2-3 sentences      |
| ## Arguments        <- Table format       |
| ## Process          <- Numbered steps     |
|   ### Step 1:                             |
|   ### Step 2:                             |
| ## Loaded Skills    <- Table: skill/why   |
| ## Invoked Subagents <- Table: who/when   |
| ## Output           <- Format + example   |
| ## Examples         <- Real usage         |
| ## Common Errors    <- Troubleshooting    |
| ## See Also         <- Related commands   |
+------------------------------------------+
```
