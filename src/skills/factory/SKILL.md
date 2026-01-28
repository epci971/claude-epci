---
name: epci:factory
description: >-
  Creates production-ready Claude skills for EPCI v6.0 through guided 6-phase workflow.
  Generates complete skill packages: SKILL.md, steps/, references/.
  Supports user skills (user-invocable: true) and internal core skills (user-invocable: false).
  Default: generates skills with steps/ for multi-phase workflows.
  Use when: creating new skill, migrating prompts, improving existing skills, generating core components.
  Triggers: create skill, new skill, factory, generate component.
  Not for: one-time prompts, volatile procedures, runtime configuration.
user-invocable: true
argument-hint: "[skill-name] [--core] [--simple] [--audit] [--refactor]"
allowed-tools: Read, Write, Edit, Glob, Grep, AskUserQuestion
---

# Factory — Skill Generator

Create production-ready skills for EPCI v6.0 following best practices.

## Quick Start

```
/factory auth-handler              # User skill with steps (default)
/factory state-manager --core      # Internal core skill (no steps)
/factory tiny-helper --simple      # Simple skill (no steps)
/factory brainstorm --audit        # Audit existing skill for EPCI compliance
/factory debug --refactor          # Refactor existing skill (steps→references)
```

## MANDATORY EXECUTION RULES (READ FIRST):

- 🔴 NEVER skip the BREAKPOINT at validation (step-05)
- 🔴 NEVER generate skills without 12-point checklist pass
- 🔴 NEVER create vague descriptions (must have 3+ triggers)
- ✅ ALWAYS start with step-00-init.md
- ✅ ALWAYS follow next_step from each step
- ✅ ALWAYS use APEX style format for generated skills
- ✅ ALWAYS generate steps/ for standard mode (default)
- ⛔ FORBIDDEN generating skills with > 500 lines in SKILL.md
- 🔵 YOU ARE A METICULOUS SKILL ARCHITECT

## EXECUTION PROTOCOLS:

1. **Load** step-00-init.md
2. **Execute** current step protocols completely
3. **Present** breakpoints via breakpoint-system
4. **Evaluate** next step trigger conditions
5. **Proceed** to next_step

## CONTEXT BOUNDARIES:

- IN scope: Skill creation, skill migration, skill improvement
- OUT scope: Subagent creation (different workflow), schema creation, script creation

## Workflow Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    FACTORY 6-PHASE WORKFLOW                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Step 00: INIT                                                   │
│  └─ Parse args, detect mode (core/simple/standard)              │
│                                                                  │
│  Step 01: PRE-ANALYSIS                                          │
│  └─ Discovery questions, decision gate (proceed/stop)           │
│                                                                  │
│  Step 02: ARCHITECTURE                                          │
│  └─ Structure selection, tools, recommendations                 │
│                                                                  │
│  Step 03: DESCRIPTION                                           │
│  └─ Description engineering with formula                        │
│                                                                  │
│  Step 04: WORKFLOW                                              │
│  └─ Workflow design, steps definition, decision trees           │
│                                                                  │
│  Step 05: VALIDATION                                            │
│  └─ 12-point checklist, preview, BREAKPOINT                     │
│                                                                  │
│  Step 06: GENERATION                                            │
│  └─ Create files, update plugin.json, report                    │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Flags

| Flag | Default | Description |
|------|---------|-------------|
| `--core` | off | Core skill (user-invocable: false, no steps) |
| `--simple` | off | Simple skill (no steps/, for < 3 phases) |
| `--audit` | off | Audit existing skill for EPCI compliance |
| `--refactor` | off | Refactor existing skill (apply steps→references pattern) |

**Behavior by Mode:**

| Mode | Steps Generated | Location | user-invocable |
|------|-----------------|----------|----------------|
| Default | Yes | `skills/{name}/` | true |
| `--simple` | No | `skills/{name}/` | true |
| `--core` | No | `skills/core/{name}/` | false |
| `--audit` | N/A | Validates existing skill | N/A |
| `--refactor` | N/A | Refactors existing skill | N/A |

**Audit Mode** validates an existing skill against EPCI best practices:
- Phase 1: Structure (12-point checklist)
- Phase 2: Breakpoint compliance
- Phase 3: Core skills usage
- Phase 4: Stack skills detection
- Phase 5: Step chain validation

**Refactor Mode** applies the steps→references pattern to existing skills:
- Phase 1: Analysis (inventory, detect duplications, map extractions)
- Phase 2: Extraction Plan (new references, steps to modify)
- Phase 3: Execution (create references, update steps, consolidate)
- Phase 4: Validation (line counts, cross-links, metrics)

## Steps

| Step | Name | Description | Skippable |
|------|------|-------------|-----------|
| 00 | init | Parse args, mode detection | No |
| 01 | preanalysis | Discovery questions, decision gate | No |
| 02 | architecture | Structure selection, tools | No |
| 03 | description | Description engineering | No |
| 04 | workflow | Workflow design, steps definition | No |
| 05 | validation | 12-point checklist, BREAKPOINT | No |
| 06 | generation | Create files, report | No |

## Step Files

- [steps/step-00-init.md](steps/step-00-init.md) — Initialization
- [steps/step-01-preanalysis.md](steps/step-01-preanalysis.md) — Pre-Analysis
- [steps/step-02-architecture.md](steps/step-02-architecture.md) — Architecture
- [steps/step-03-description.md](steps/step-03-description.md) — Description
- [steps/step-04-workflow.md](steps/step-04-workflow.md) — Workflow
- [steps/step-05-validation.md](steps/step-05-validation.md) — Validation
- [steps/step-06-generation.md](steps/step-06-generation.md) — Generation
- [steps/step-07-refactor.md](steps/step-07-refactor.md) — Refactoring (--refactor mode)

## Reference Files

- [references/apex-style-guide.md](references/apex-style-guide.md) — APEX style formatting
- [references/best-practices-synthesis.md](references/best-practices-synthesis.md) — Core best practices
- [references/checklist-validation.md](references/checklist-validation.md) — 12-point validation
- [references/description-formulas.md](references/description-formulas.md) — Description patterns
- [references/yaml-rules.md](references/yaml-rules.md) — Frontmatter syntax
- [references/skill-templates.md](references/skill-templates.md) — APEX templates
- [references/agents-catalog.md](references/agents-catalog.md) — Agent recommendations
- [references/stacks-catalog.md](references/stacks-catalog.md) — Stack detection
- [references/skill-refactoring-prompt.md](references/skill-refactoring-prompt.md) — Refactoring workflow
- [references/refactoring-checklist.md](references/refactoring-checklist.md) — Post-refactoring validation
- [references/refactoring-formats.md](references/refactoring-formats.md) — Refactoring display templates

## Templates (for generated steps)

- [templates/step-init-template.md](templates/step-init-template.md) — Init step template
- [templates/step-generic-template.md](templates/step-generic-template.md) — Generic step template
- [templates/step-finish-template.md](templates/step-finish-template.md) — Finish step template

## Shared Components Used

- `epci:breakpoint-system` — Validation approval (step-05)
- `epci:complexity-calculator` — Sizing determination
- `epci:clarification-engine` — Gap analysis on description (optional)
- `epci:project-memory` — Store generated skill metadata

## Subagents

| Agent | Model | Trigger |
|-------|-------|---------|
| `@Explore` | - | Always at init (background) |

## Generated Skill Structure

**Default (with steps):**
```
skills/{name}/
├── SKILL.md                    # Router (~200 lines)
├── steps/
│   ├── step-00-init.md
│   ├── step-01-{phase1}.md
│   ├── step-02-{phase2}.md
│   └── step-99-finish.md
└── references/
    └── {domain}.md
```

**Simple (--simple) or Core (--core):**
```
skills/{name}/
└── SKILL.md                    # Complete skill
```

## Description Formula

```
DESCRIPTION = [CAPABILITIES] + [USE CASES] + [TRIGGERS] + [BOUNDARIES]
```

**Rules:**
- Length: 50-150 words (< 1024 chars)
- Trigger words: 3-5 natural phrases
- Specificity: No generic terms ("helper", "utility")
- Action verbs: Start with what it does

## 12-Point Checklist (Summary)

| # | Check | Required |
|---|-------|----------|
| 1 | Name is kebab-case | Yes |
| 2 | Name <= 64 chars | Yes |
| 3 | Description is specific | Yes |
| 4 | Description < 1024 chars | Yes |
| 5 | 3+ trigger words | Yes |
| 6 | SKILL.md < 500 lines | Yes |
| 7 | Referenced files exist | Yes |
| 8 | Tools are appropriate | Yes |
| 9 | Steps numbered | Yes |
| 10 | Examples included | Recommended |
| 11 | Error handling defined | Recommended |
| 12 | Limitations documented | Recommended |

See [references/checklist-validation.md](references/checklist-validation.md) for details.

## Anti-Patterns

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| Vague description | Won't trigger | Use formula with triggers |
| Everything in SKILL.md | Context overflow | Use steps/ structure |
| No examples | Users confused | Add input/output examples |
| Multi-purpose | Hard to trigger | Split into focused skills |

## INVOCATION PROTOCOL (CRITICAL)

Les syntaxes `@skill:epci:xxx` et `@agent:xxx` dans les step files sont **DOCUMENTAIRES SEULEMENT**.
Claude interprète les blocs de code comme des exemples, pas comme des instructions d'exécution.

**Pour invoquer réellement:**

| Type | Syntaxe documentaire | Invocation réelle |
|------|---------------------|-------------------|
| Breakpoints | `@skill:epci:breakpoint-system` | Section impérative + AskUserQuestion explicite |
| Agents | `@agent:Explore` | `Task({ subagent_type: "Explore", ... })` |
| Core skills | `@skill:epci:project-memory` | `Read(".claude/state/...")` pour fichiers d'état |

**Règle pour auteurs de step files:**
- Utiliser le format impératif direct (pas dans bloc de code)
- Afficher les boîtes ASCII hors bloc exécutable
- Appeler AskUserQuestion explicitement
- Ajouter `⏸️ ATTENDS la réponse` après chaque breakpoint

## Refactoring Mode

The `--refactor` flag enables automated refactoring of existing skills to follow the steps→references pattern.

### When to Use

- Steps exceeding 200 lines
- Duplicated content across steps
- Inline ASCII boxes > 10 lines
- Inline schemas > 5 fields
- Missing "Reference Files Used" tables

### Workflow

```
/factory {skill-name} --refactor
```

Routes to `step-07-refactor.md` which executes:

1. **Analysis**: Inventory files, detect violations, map extractions
2. **Plan**: Define new references, identify steps to modify
3. **Execute**: Create references, update steps, consolidate
4. **Validate**: Check line counts, cross-links, run audit

### Extraction Thresholds

| Content Type | Threshold | Target Reference |
|--------------|-----------|------------------|
| ASCII box | > 10 lines | `breakpoint-formats.md` |
| JSON schema | > 5 fields | `{domain}-schema.md` |
| Lookup table | > 10 rows | `{domain}-tables.md` |
| Business rules | > 3 rules | `{domain}-rules.md` |
| Output template | > 20 lines | `{domain}-templates.md` |

### Priority Queue

| Skill | Priority | Critical Issue |
|-------|----------|----------------|
| debug | P1 | step-07-complex.md (277 lines) |
| refactor | P1 | step-07-report.md (229 lines) |
| implement | P2 | step-04-review.md (201 lines) |
| quick | P3 | step-03-code.md (238 lines) |

See [references/skill-refactoring-prompt.md](references/skill-refactoring-prompt.md) for the complete workflow.

## Limitations

This skill does NOT:
- Create subagents (different workflow)
- Modify existing skills (use edit manually)
- Generate tests automatically
- Create schemas or scripts
