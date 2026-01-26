# EPCI Plugin v6.0

> **Version**: 6.0.0 | **Date**: January 2026

---

## 1. Overview

EPCI v6 is a streamlined AI-assisted development workflow plugin for Claude Code.

**Key Changes from v5:**
- 23 skills → 8 user-facing skills + 6 core skills
- Internal components now as skills (user-invocable: false)
- Simplified architecture with clear separation

### Architecture

| Layer | Components | Purpose |
|-------|------------|---------|
| User Skills (7) | User-facing commands | Direct user interaction |
| Core Skills (6) | Internal components | Reusable logic, auto-triggered |
| Schemas | JSON schemas | Data validation |
| Scripts | Utilities | Validation, helpers |

---

## 2. User Skills (7)

User-invocable commands via `/epci:<skill-name>`.

| Skill | Purpose | Triggers |
|-------|---------|----------|
| `/brainstorm` | Idea exploration and refinement | vague idea, unclear requirements |
| `/spec` | Create specifications (PRD/CDC) | write spec, document feature |
| `/implement` | Full implementation workflow | build feature, implement |
| `/quick` | Fast implementation for small tasks | quick fix, small change |
| `/debug` | Structured debugging | fix bug, investigate error |
| `/refactor` | Code restructuring | refactor, restructure |
| `/factory` | Create new plugin components | create skill, create component |

---

## 3. Core Skills (6)

Internal skills used by user skills. Not directly user-invocable (`user-invocable: false`).
Claude triggers these automatically based on context.

| Core Skill | Purpose | Used By |
|------------|---------|---------|
| `state-manager` | Feature state persistence | implement, quick |
| `breakpoint-system` | Interactive breakpoints | All skills |
| `complexity-calculator` | Scope estimation & routing | brainstorm, spec, implement, quick |
| `clarification-engine` | Smart clarification questions | brainstorm, spec, debug |
| `tdd-enforcer` | TDD workflow enforcement | implement, quick, debug |
| `project-memory` | Project context and history | All skills |

---

## 4. Directory Structure

```
src/
├── .claude-plugin/
│   └── plugin.json              # Manifest with 19 skills (8 user + 6 core + 5 stack)
├── CLAUDE.md                    # This file
│
├── skills/                      # All skills
│   ├── brainstorm/              # User skills
│   │   ├── SKILL.md
│   │   └── references/
│   ├── spec/
│   │   ├── SKILL.md
│   │   ├── references/
│   │   └── templates/
│   ├── implement/
│   │   └── SKILL.md
│   ├── quick/
│   │   └── SKILL.md
│   ├── debug/
│   │   └── SKILL.md
│   ├── refactor/
│   │   └── SKILL.md
│   ├── factory/
│   │   ├── SKILL.md
│   │   └── references/
│   │
│   ├── core/                    # Internal core skills
│   │   ├── state-manager/
│   │   ├── breakpoint-system/
│   │   ├── complexity-calculator/
│   │   ├── clarification-engine/
│   │   ├── tdd-enforcer/
│   │   └── project-memory/
│   │
│   └── stack/                   # Technology-specific skills
│       ├── python-django/
│       │   ├── SKILL.md
│       │   ├── references/
│       │   └── rules-templates/
│       ├── javascript-react/
│       ├── java-springboot/
│       ├── php-symfony/
│       └── frontend-editor/
│
├── agents/                      # Specialized subagents (16)
│   ├── plan-validator.md
│   ├── code-reviewer.md
│   ├── security-auditor.md
│   ├── qa-reviewer.md
│   ├── decompose-validator.md
│   ├── doc-generator.md
│   ├── implementer.md
│   ├── planner.md
│   ├── expert-panel.md
│   ├── party-orchestrator.md
│   ├── ems-evaluator.md
│   ├── technique-advisor.md
│   ├── clarifier.md
│   ├── rules-validator.md
│   ├── rule-clarifier.md
│   └── statusline-setup.md
│
├── schemas/                     # JSON schemas
│   ├── prd-v2.json
│   ├── ralph-index-v1.json
│   ├── feature-state-v1.json
│   └── feature-index-v1.json
│
└── scripts/                     # Utilities
    └── validate.py
```

---

## 5. Workflow Overview

### Primary Flow

```
Idea → /brainstorm → /spec → /implement → Done
         ↓            ↓          ↓
     Clarify      Document    Build+Test
```

### Quick Path (Small Tasks)

```
Clear requirement → /quick → Done
                      ↓
                Build+Test
```

### Debug Path

```
Bug report → /debug → Investigation → Fix → Done
```

---

## 6. Development Guidelines

### Conventions

| Element | Convention | Example |
|---------|------------|---------|
| User Skills | lowercase, hyphenated | `brainstorm`, `quick` |
| Core Skills | lowercase, hyphenated | `state-manager` |
| Schemas | kebab-case-v{n}.json | `feature-state-v1.json` |

### Limits

| Element | Limit |
|---------|-------|
| SKILL.md body | < 500 lines |
| Description | ≤ 1024 chars (50-150 words optimal) |

### Breakpoint Usage (MANDATORY)

All user-invocable skills MUST use `@skill:breakpoint-system` for interactive breakpoints.

**Rules:**
- NEVER create manual ASCII boxes for interactive breakpoints in step files
- ALWAYS invoke `@skill:breakpoint-system` with appropriate type
- ALWAYS document breakpoint types in SKILL.md "Breakpoints" section

**Supported types:** `validation`, `analysis`, `plan-review`, `phase-transition`, `decomposition`, `diagnostic`, `ems-status`, `info-only`

**Example invocation:**
```typescript
@skill:breakpoint-system
  type: plan-review
  title: "Plan Validation"
  data: { /* type-specific structure per breakpoint-system schema */ }
  ask: { question, header, options }
  suggestions: [ /* P1/P2/P3 proactive suggestions */ ]
```

**Note:** ASCII boxes for informative displays (summaries, TDD cycle status) that don't require user input remain in manual format.

### Validation

```bash
python src/scripts/validate.py
```

---

## 7. Quick Reference

### Invoke a Skill

```
/epci:brainstorm "your idea"
/epci:quick "small task"
/epci:implement feature-slug
```

### Create Skills

```
/epci:factory my-skill              # Create user skill
/epci:factory my-component --core   # Create core skill
```

---

## 8. Migration from v5

v5 content archived in `archive/v5/`. Key changes:

- Commands + Skills → unified Skills
- Subagents → integrated or removed
- Shared components → Core skills (skills/core/)

See `docs/migration/` for detailed migration guides.

---

## 9. Stack Skills (5)

Technology-specific patterns and conventions. Located in `src/skills/stack/`.

| Stack | Target | Auto-detect |
|-------|--------|-------------|
| `python-django` | Django/DRF backend | `manage.py`, django in requirements |
| `javascript-react` | React islands/SPA | react in package.json, `.tsx` files |
| `java-springboot` | Spring Boot backend | spring-boot in pom.xml/build.gradle |
| `php-symfony` | Symfony 7/8 backend | symfony in composer.json, `bin/console` |
| `frontend-editor` | Tailwind/a11y styling | `tailwind.config.*` |

Each stack skill provides:
- `references/` — Architecture, testing, security patterns
- `rules-templates/` — Pre-built .claude/rules/ templates

---

## 10. Agents (16)

Specialized subagents for specific tasks. Located in `src/agents/`.

| Category | Agents | Purpose |
|----------|--------|---------|
| **Validators** | plan-validator, code-reviewer, rules-validator, decompose-validator | Quality gates |
| **Reviewers** | security-auditor, qa-reviewer | Specialized review |
| **Executors** | implementer, planner, doc-generator | Task execution |
| **Brainstorm** | expert-panel, party-orchestrator, ems-evaluator, technique-advisor, clarifier | Exploration |
| **Utilities** | rule-clarifier, statusline-setup | Support |

### Agent Model Mapping

| Model | Agents |
|-------|--------|
| **Opus** | plan-validator, code-reviewer, security-auditor, decompose-validator, rules-validator |
| **Sonnet** | qa-reviewer, doc-generator, implementer, planner, expert-panel, party-orchestrator |
| **Haiku** | ems-evaluator, technique-advisor, clarifier, rule-clarifier, statusline-setup |
