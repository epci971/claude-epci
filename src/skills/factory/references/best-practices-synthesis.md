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

## 7. Anti-Patterns Summary

| Anti-Pattern | Problem | Fix |
|--------------|---------|-----|
| Vague description | Random triggering | Use formula |
| Everything in SKILL.md | Context overflow | Progressive disclosure |
| Unlinked references | Never loaded | Link from SKILL.md |
| Multi-purpose skills | Hard to trigger | Split into focused |
| No examples | User confusion | Add input/output |
| Generic names | Collisions | Use specific names |

## 8. Core Skills Integration

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

## 9. Task Tool Integration (MANDATORY)

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

## 10. Quality Checklist (Quick)

Before committing:
- [ ] Name unique and kebab-case
- [ ] Description < 1024 chars with triggers
- [ ] SKILL.md < 500 lines
- [ ] All references linked
- [ ] Examples included
- [ ] Core skills documented (if used)
- [ ] Task tool documented for delegated phases
- [ ] Tested with `/skill-name`
