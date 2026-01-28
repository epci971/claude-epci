# Best Practices Synthesis

> Condensed from Claude Code Best Practices (January 2026)

## 1. Structure Limits

| Element | Limit | Notes |
|---------|-------|-------|
| `name` | ≤ 64 chars | kebab-case, lowercase |
| `description` | ≤ 1024 chars | 50-150 words optimal |
| SKILL.md body | < 500 lines | Use progressive disclosure beyond |
| Token estimate | < 5000 tokens | For context efficiency |

## 2. Description Formula

```
[CAPABILITIES] + [USE CASES] + [TRIGGERS] + [BOUNDARIES]
```

**Example:**
```yaml
description: >-
  Generates API documentation from source code.
  Extracts endpoints, parameters, and responses.
  Use when: documenting REST APIs, creating OpenAPI specs.
  Triggers: API docs, document endpoints.
  Not for: internal code comments.
```

## 3. Frontmatter Fields

### Required
- `name` — Unique identifier (kebab-case)
- `description` — What it does + when to use

### Common Optional
| Field | Default | Values |
|-------|---------|--------|
| `user-invocable` | `true` | `true` / `false` |
| `disable-model-invocation` | `false` | `true` / `false` |
| `allowed-tools` | inherit | `Read, Write, Bash, etc.` |
| `argument-hint` | none | `"[param]"` |

### Advanced Optional
| Field | Default | Values |
|-------|---------|--------|
| `model` | inherit | `sonnet` / `haiku` / `opus` |
| `context` | none | `fork` (isolated subagent) |
| `agent` | `general-purpose` | `Explore` / `Plan` |

## 4. Progressive Disclosure

Structure for large skills:

```
Level 1: Frontmatter (~100 tokens) — always loaded
Level 2: SKILL.md body (<5000 tokens) — on trigger
Level 3: references/ (variable) — on demand via links
```

**Rule**: Keep SKILL.md < 300 lines, put details in references/

## 5. Triggering Best Practices

### Do
- Include 3-5 natural trigger phrases
- Use action verbs ("Generates", "Analyzes")
- Specify concrete use cases
- Define clear boundaries

### Don't
- Use vague terms ("helper", "utility")
- Make description too short
- Skip trigger words
- Create multi-purpose skills

## 6. Internal Skills (Core)

For skills that Claude invokes automatically:

```yaml
user-invocable: false
disable-model-invocation: false  # Allow Claude to invoke
```

**Description pattern:**
```yaml
description: >-
  [What it does]. Internal component for EPCI v6.0.
  Use when: [specific conditions].
  Not for: direct user invocation.
```

## 7. Progressive Disclosure Pattern

| Level | File | Content | Lines |
|-------|------|---------|-------|
| 1 | SKILL.md | Overview, links to steps/references | ~200 |
| 2 | steps/*.md | Declarative procedures | 50-150 each |
| 3 | references/*.md | Schemas, templates, tables | Variable |

### 7.1 Content Location Matrix

| Content Type | Location | Threshold |
|--------------|----------|-----------|
| Procedure (WHAT to do) | steps/ | Always |
| ASCII templates | references/ | > 10 lines |
| JSON schemas | references/ | > 5 fields |
| Lookup tables | references/ | > 10 rows |
| Business rules | references/ | > 3 rules |
| Breakpoint formats | references/ | Always centralize |
| AskUserQuestion options | references/ | If reused across steps |
| Output templates | references/ | > 20 lines |

### 7.2 Extraction Thresholds (Refactoring)

Explicit thresholds for `--refactor` mode:

| Content | Threshold | Target Reference | Example |
|---------|-----------|------------------|---------|
| ASCII box | > 10 lines | `breakpoint-formats.md` | Phase output boxes |
| JSON schema | > 5 fields | `{domain}-schema.md` | State structure |
| Lookup table | > 10 rows | `{domain}-tables.md` | Scoring criteria |
| Business rules | > 3 rules | `{domain}-rules.md` | Validation rules |
| Output template | > 20 lines | `{domain}-templates.md` | Report formats |
| **Step file** | > 200 lines | **Must refactor** | Extract to refs |

**Step Size Targets:**
| Metric | Violation | Warning | Target |
|--------|-----------|---------|--------|
| Step lines | > 200 | > 150 | < 150 |
| SKILL.md | > 500 | > 400 | < 300 |

### Decision Tree

```
1. Is it a FORMAT (visual display)?
   → references/ (breakpoint-formats.md pattern)

2. Is it a RULE/THRESHOLD?
   → references/ if reused, inline if unique to step

3. Is it ORCHESTRATION (IF/FOR/Task)?
   → steps/ (this is procedural logic)

4. Is it DATA (schema, lookup table)?
   → references/

5. Is it > 20 lines of inline content?
   → Extract to references/
```

### Rules

**DO**:
- Link from step to reference: `See [references/file.md](../references/file.md)`
- Keep step descriptions under 50 words per action
- Maintain single source of truth in references/
- Add "Reference Files Used" table in each step

**DO NOT**:
- Duplicate schemas in steps/
- Embed full templates in steps/
- Copy reference tables into procedures
- Inline ASCII boxes > 10 lines

### Step Content Guidelines

Steps should be **declarative** (WHAT to do), not **definitional** (data/schema).

| Content Type | Location | Example |
|--------------|----------|---------|
| Procedure | steps/ | "Apply template from references/X" |
| Template | references/ | Full markdown template |
| Schema | references/ | JSON/YAML structure |
| Table > 10 rows | references/ | Scoring criteria, rules |
| Breakpoint format | references/ | ASCII box with variables |

---

## 8. Anti-Patterns Summary

| Anti-Pattern | Problem | Fix |
|--------------|---------|-----|
| Vague description | Random triggering | Use formula |
| Everything in SKILL.md | Context overflow | Progressive disclosure |
| Unlinked references | Never loaded | Link from SKILL.md |
| Multi-purpose skills | Hard to trigger | Split into focused |
| No examples | User confusion | Add input/output |
| Generic names | Collisions | Use specific names |
| Duplicated content | Maintenance burden | Single source in references/ |

## 9. Core Skills Integration

EPCI v6 provides 6 core skills for composable functionality. Document usage in generated skills.

### Core Skills Catalog

| Core Skill | Purpose | API Functions |
|------------|---------|---------------|
| `breakpoint-system` | Interactive decision points | `present()`, `wait_approval()` |
| `complexity-calculator` | Scope estimation | `calculate()`, `route()` |
| `clarification-engine` | Smart questions | `analyze_gaps()`, `generate_questions()` |
| `state-manager` | Feature state tracking | `init()`, `update()`, `get()` |
| `tdd-enforcer` | TDD workflow | `start_cycle()`, `validate_phase()` |
| `project-memory` | Project context | `recall()`, `store_feature()` |

### When to Use Core Skills

| Skill Type | Required | Recommended | Optional |
|------------|----------|-------------|----------|
| Exploration | breakpoint | clarification | memory |
| Specification | breakpoint, complexity | clarification | memory |
| Implementation | breakpoint, state, tdd | complexity | memory |
| Transformation | breakpoint, state | — | memory |

### Reference Syntax

In generated skills, reference core skills:

```markdown
## Core Skills Integration

| Core Skill | Purpose in This Skill |
|------------|----------------------|
| `@skill:epci:breakpoint-system` | Phase transitions |
| `@skill:epci:state-manager` | Progress tracking |
```

---

## 10. Task Tool Integration (MANDATORY)

### 🔴 Rule: Subagent Delegation

Skills with multi-phase workflows MUST document Task tool usage for:
- Phase delegation (planning, review, security audit)
- Context isolation (preserve main thread)
- Model optimization (Sonnet for execution, Opus for validation)

### Required Documentation

In SKILL.md "Shared Components Used" section:
```markdown
## Subagent Delegation

| Phase | Agent | Invocation |
|-------|-------|------------|
| Plan | @planner | `Task(subagent_type: "planner")` |
| Plan Validation | @plan-validator | `Task(subagent_type: "plan-validator")` |
| Review | @code-reviewer | `Task(subagent_type: "code-reviewer")` |
| Security | @security-auditor | `Task(subagent_type: "security-auditor")` |
```

### Exception: Implementation Phase

Implementation phase MUST NOT be delegated:
- @implementer cannot access stack skills (via Skill tool)
- Main thread required for technology-specific patterns

### Validation

Audit script (Phase 6) checks:
- Complex workflows (4+ steps) document Task usage
- Each delegated phase shows explicit Task invocation

---

## 11. Quality Checklist (Quick)

Before committing:
- [ ] Name unique and kebab-case
- [ ] Description < 1024 chars with triggers
- [ ] SKILL.md < 500 lines
- [ ] All references linked
- [ ] Examples included
- [ ] Core skills documented (if used)
- [ ] Task tool documented for delegated phases
- [ ] Tested with `/skill-name`

---

## 12. Native vs Custom Agents

### Native Agents (Use When Generic)

Claude Code provides built-in agents optimized for specific tasks:

| Agent | Identifier | Model | Best For |
|-------|------------|-------|----------|
| Explore | `Explore` | Haiku | Codebase exploration, file discovery |
| Plan | `Plan` | Inherits | Research for planning phase |
| General-purpose | `general-purpose` | Inherits | Complex multi-step autonomous tasks |

**Characteristics:**
- `Explore`: Read-only (Read, Glob, Grep), fast Haiku model, perfect for exploration phases
- `Plan`: Context isolation for safe research
- `general-purpose`: Full tool access for complex operations

### Custom Agents (Use When EPCI-Specific)

| Agent | Purpose | Why Custom |
|-------|---------|------------|
| `@planner` | EPCI task decomposition | Specific output format required |
| `@plan-validator` | CQNT validation checklist | Domain-specific rules |
| `@code-reviewer` | EPCI review criteria | Custom checklist |
| `@security-auditor` | OWASP with EPCI reporting | Structured security format |

### Decision Matrix

| Situation | Use Native | Use Custom |
|-----------|------------|------------|
| Generic file search | `Explore` | — |
| Research for planning | `Plan` | — |
| Complex autonomous task | `general-purpose` | — |
| EPCI-formatted plan | — | `@planner` |
| Plan with CQNT validation | — | `@plan-validator` |
| Code review with EPCI checklist | — | `@code-reviewer` |
| Security audit with OWASP | — | `@security-auditor` |

### Invocation Example

```typescript
// Native agent (generic exploration)
Task({
  subagent_type: "Explore",
  prompt: `Find files related to authentication...`
})

// Custom agent (EPCI-specific validation)
Task({
  subagent_type: "plan-validator",
  prompt: `Validate plan against CQNT criteria...`
})
