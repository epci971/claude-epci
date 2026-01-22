# Command Template

Template for generating command files from skills.

## When to Create a Command

Create a command file only when:
- The skill has `user-invocable: true`
- The skill is intended to be invoked via `/epci:{name}`

Core skills (`--core` flag) do NOT get command files.

---

## Template Structure

```yaml
---
description: "{shortened_description}"
argument-hint: "{argument_hint}"
allowed-tools: "{allowed_tools}"
disable-model-invocation: true
---

Invoke the epci:{name} skill and follow it exactly as presented to you
```

---

## Field Mapping

| Command Field | Source | Transformation |
|---------------|--------|----------------|
| `description` | SKILL.md `description` | Shorten to max 150 chars, remove "Trigger words:" |
| `argument-hint` | SKILL.md `argument-hint` | Copy as-is |
| `allowed-tools` | SKILL.md `allowed-tools` | Copy as-is (optional) |
| `disable-model-invocation` | Fixed | Always `true` |

---

## Description Shortening Rules

1. **Max length**: 150 characters
2. **Remove suffix**: Strip "Trigger words: ..." and everything after
3. **Keep first sentence(s)**: Preserve the core capability description
4. **No trailing period**: Remove if present

### Examples

**Input (from SKILL.md):**
```yaml
description: >
  Transform vague ideas into structured specifications through guided exploration.
  Uses iterative refinement with EMS scoring to progressively clarify requirements.
  Trigger words: brainstorm, explore idea, clarify requirements, vague concept.
```

**Output (for command.md):**
```yaml
description: "Transform vague ideas into structured specifications through guided exploration. Use for idea exploration, requirement clarification."
```

---

## Generation Steps

1. **Read skill frontmatter**: Extract `description`, `argument-hint`, `allowed-tools`

2. **Shorten description**:
   ```python
   # Pseudo-code
   desc = skill_description
   desc = desc.split("Trigger words:")[0].strip()  # Remove trigger suffix
   if len(desc) > 150:
       desc = desc[:147] + "..."
   ```

3. **Build frontmatter**:
   ```yaml
   ---
   description: "{shortened_desc}"
   argument-hint: "{skill_argument_hint}"
   allowed-tools: "{skill_allowed_tools}"  # Only if present in skill
   disable-model-invocation: true
   ---
   ```

4. **Add body**:
   ```
   Invoke the epci:{name} skill and follow it exactly as presented to you
   ```

5. **Write to**: `commands/{name}.md`

---

## Validation

After creating the command, run:

```bash
python3 src/scripts/validate.py
```

This verifies:
- `argument-hint` matches between skill and command
- `allowed-tools` matches between skill and command (if present)

---

## Examples

### Example 1: Simple skill (no allowed-tools)

**Skill (quick/SKILL.md):**
```yaml
name: quick
description: >
  Fast implementation for TINY and SMALL tasks. Single-phase execution
  with optional TDD. Ideal for bug fixes, small features, and quick changes.
  Trigger words: quick fix, small change, tiny feature, fast implementation.
user-invocable: true
argument-hint: "<task> [@plan-path]"
```

**Generated command (commands/quick.md):**
```yaml
---
description: "Fast implementation for TINY and SMALL tasks. Single-phase execution with TDD. Use for quick fixes and small changes."
argument-hint: "<task> [@plan-path]"
disable-model-invocation: true
---

Invoke the epci:quick skill and follow it exactly as presented to you
```

### Example 2: Skill with allowed-tools

**Skill (factory/SKILL.md):**
```yaml
name: factory
description: >
  Creates production-ready Claude skills for EPCI v6.0 through guided 6-phase workflow.
  Generates complete skill packages: SKILL.md, references/, templates/.
user-invocable: true
argument-hint: "[skill-name] [--core]"
allowed-tools: Read, Write, Edit, Glob, Grep, AskUserQuestion
```

**Generated command (commands/factory.md):**
```yaml
---
description: "Create new skills for EPCI plugin through guided 6-phase workflow. Use when creating skill, component, or extending the plugin."
argument-hint: "[skill-name] [--core]"
allowed-tools: "Read, Write, Edit, Glob, Grep, AskUserQuestion"
disable-model-invocation: true
---

Invoke the epci:factory skill and follow it exactly as presented to you
```
