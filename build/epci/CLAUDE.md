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
| User Skills (8) | User-facing commands | Direct user interaction |
| Core Skills (6) | Internal components | Reusable logic, auto-triggered |
| Schemas | JSON schemas | Data validation |
| Scripts | Utilities | Validation, helpers |

---

## 2. User Skills (8)

User-invocable commands via `/epci:<skill-name>`.

| Skill | Purpose | Triggers |
|-------|---------|----------|
| `/brainstorm` | Idea exploration and refinement | vague idea, unclear requirements |
| `/spec` | Create specifications (PRD/CDC) | write spec, document feature |
| `/implement` | Full implementation workflow | build feature, implement |
| `/quick` | Fast implementation for small tasks | quick fix, small change |
| `/debug` | Structured debugging | fix bug, investigate error |
| `/improve` | Enhance existing code | optimize, improve performance |
| `/refactor` | Code restructuring | refactor, restructure |
| `/factory` | Create new plugin components | create skill, create component |

---

## 3. Core Skills (6)

Internal skills used by user skills. Not directly user-invocable (`user-invocable: false`).
Claude triggers these automatically based on context.

| Core Skill | Purpose | Used By |
|------------|---------|---------|
| `state-manager` | Feature state persistence | implement, quick, improve |
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
│   └── plugin.json              # Manifest with 14 skills (8 user + 6 core)
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
│   ├── improve/
│   │   └── SKILL.md
│   ├── refactor/
│   │   └── SKILL.md
│   ├── factory/
│   │   ├── SKILL.md
│   │   └── references/
│   │
│   └── core/                    # Internal core skills
│       ├── state-manager/
│       │   └── SKILL.md
│       ├── breakpoint-system/
│       │   └── SKILL.md
│       ├── complexity-calculator/
│       │   └── SKILL.md
│       ├── clarification-engine/
│       │   └── SKILL.md
│       ├── tdd-enforcer/
│       │   └── SKILL.md
│       └── project-memory/
│           └── SKILL.md
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
