---
name: skills-creator
description: >-
  Guided creation of new Claude Code Skills. 6-phase workflow with templates,
  validation and triggering tests. Use when: /epci:create skill invoked.
  Not for: modifying existing skills, other components.
---

# Skills Creator

## Overview

Guides new skill creation with automatic validation.

## 6-Phase Workflow

### Phase 1: Qualification

Questions to define the skill:

1. **Domain**: What technical domain does this skill cover?
2. **Trigger**: When should this skill be auto-invoked?
3. **Exclusions**: When should it NOT be invoked?
4. **Category**: core | stack | factory | custom?
5. **Tools**: What tools are needed?

### Phase 2: Definition

Define frontmatter elements:

```yaml
---
name: [kebab-case, ≤64 chars]
description: >-
  [Capability]. [Auto-invoke when: conditions].
  [Not for: exclusions].
allowed-tools: [Read, Write, ...]  # If needed
---
```

**Required description formula:**
```
[What the skill does]. Use when: [activation conditions].
Not for: [clear exclusions].
```

### Phase 3: Content

Generate skill content:

```markdown
# [Skill Name]

## Overview
[Description in 2-3 sentences]

## [Main Section 1]
[Structured content with tables, code, examples]

## [Main Section 2]
[...]

## Quick Reference
[Cheatsheet, checklist, quick reference table]

## Common Patterns
[Frequent patterns, practical examples]

## Anti-patterns
[What to avoid]
```

**Constraints:**
- < 5000 tokens
- Structure with headers
- Tables for references
- Code examples if applicable

### Phase 4: References (optional)

If the skill needs references:

```
skills/<category>/<name>/
├── SKILL.md
└── references/
    ├── reference-1.md
    └── reference-2.md
```

### Phase 5: Validation

Run validation script:

```bash
python src/scripts/validate_skill.py src/skills/<category>/<name>/
```

**Criteria:**
- [ ] Valid YAML frontmatter
- [ ] Kebab-case name ≤ 64 chars
- [ ] Description with "Use when:" and "Not for:"
- [ ] Description ≤ 1024 chars
- [ ] Content < 5000 tokens
- [ ] References exist if mentioned

### Phase 6: Triggering Test

Test auto-invocation:

```bash
python src/scripts/test_triggering.py src/skills/<category>/<name>/
```

**Automatic tests:**
- Requests that MUST trigger → verified
- Requests that must NOT trigger → verified

## Templates

### Core Skill Template

```markdown
---
name: [name]
description: >-
  [Generic capability]. Use when: [general contexts].
  Not for: [exclusions].
---

# [Name] Skill

## Overview
[Description]

## Concepts
[Fundamental concepts]

## Patterns
[Applicable patterns]

## Quick Reference
[Reference table]
```

### Stack Skill Template

```markdown
---
name: [stack]-[framework]
description: >-
  Patterns and conventions for [Stack/Framework]. Includes [tools].
  Use when: [stack] development, [detection file] detected.
  Not for: [other stacks/frameworks].
---

# [Stack] Development Patterns

## Overview
[Description]

## Auto-detection
[How the skill is detected]

## Architecture
[Recommended structure]

## Patterns
[Specific patterns]

## Testing
[Test patterns]

## Commands
[Useful commands]
```

## Description Examples

### Good ✅

```
Microservices architecture patterns. Includes service mesh,
circuit breaker, saga patterns. Use when: microservices design,
distributed architecture. Not for: monoliths, simple applications.
```

### Bad ❌

```
A skill for microservices.
```
(Missing "Use when:" and "Not for:")

## Output

```markdown
✅ **SKILL CREATED**

Skill: [name]
Category: [category]
File: src/skills/[category]/[name]/SKILL.md

Validation: ✅ PASSED (6/6 checks)
Triggering: ✅ PASSED (X/Y tests)

Next steps:
1. Customize content
2. Add references if needed
3. Test with real requests
```

## Design Rules

### The 10 Golden Rules

1. **Kebab-case name** — `my-skill` not `MySkill`
2. **Formulated description** — "Use when:" + "Not for:"
3. **Single focus** — One skill = one domain
4. **Auto-detectable** — Clear trigger conditions
5. **Explicit exclusions** — Avoid false positives
6. **Content < 5000 tokens** — Fast loading
7. **Structure with headers** — Easy navigation
8. **Practical examples** — Code, tables, patterns
9. **Quick Reference** — Fast lookup
10. **Anti-patterns** — What to avoid
