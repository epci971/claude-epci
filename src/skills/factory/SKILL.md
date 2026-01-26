---
name: factory
description: >-
  Creates production-ready Claude skills for EPCI v6.0 through guided 6-phase workflow.
  Generates complete skill packages: SKILL.md, references/, templates/.
  Supports user skills (user-invocable: true) and internal core skills (user-invocable: false).
  Use when creating new skill, migrating prompts, improving existing skills, or generating core components.
  Not for one-time prompts, volatile procedures, or runtime configuration.
user-invocable: true
argument-hint: "[skill-name] [--core] [--workflow]"
allowed-tools: Read, Write, Edit, Glob, Grep, AskUserQuestion
---

# Factory — Skill Generator

Create production-ready skills for EPCI v6.0 following best practices.

## Quick Start

```
/factory auth-handler              # Create user skill
/factory state-manager --core      # Create internal core skill
/factory implement-v2 --workflow   # Create skill with steps/ structure
```

---

## MANDATORY WRITING RULES — Style APEX

### Format Obligatoire

Tous les skills generes DOIVENT utiliser le format APEX :

- :red_circle: NEVER ecrire de longs paragraphes explicatifs
- :red_circle: NEVER melanger regles et workflow dans une meme section
- :white_check_mark: ALWAYS commencer par "MANDATORY EXECUTION RULES (READ FIRST):"
- :white_check_mark: ALWAYS utiliser les icones standardisees
- :white_check_mark: ALWAYS separer RULES → PROTOCOLS → BOUNDARIES
- :no_entry: FORBIDDEN prose documentaire (style ancien)

### Structure Obligatoire de Chaque Skill/Step

1. **MANDATORY EXECUTION RULES (READ FIRST):**
   - :red_circle: NEVER rules (max 5)
   - :white_check_mark: ALWAYS rules (max 5)
   - :no_entry: FORBIDDEN rules (if applicable)
   - :large_blue_circle: POSTURE rules (if applicable)
   - :thought_balloon: FOCUS rules (if applicable)

2. **EXECUTION PROTOCOLS:**
   - Liste numerotee des actions
   - Format: `1. **{Verb}** {description}`

3. **CONTEXT BOUNDARIES:**
   - IN scope: ce qui est inclus
   - OUT scope: ce qui est exclu

4. **OUTPUT FORMAT:** (si applicable)

5. **BREAKPOINT:** (si applicable)

6. **NEXT STEP TRIGGER:** (si workflow avec steps)

### Table des Icones

| Icone | Keyword | Usage |
|-------|---------|-------|
| :red_circle: | NEVER | Actions interdites critiques |
| :white_check_mark: | ALWAYS | Actions obligatoires |
| :no_entry: | FORBIDDEN | Blocage dur |
| :large_blue_circle: | POSTURE | Mindset/attitude |
| :thought_balloon: | FOCUS | Concentration mentale |
| :warning: | WARNING | Attention particuliere |
| :pause_button: | BREAKPOINT | Point d'arret utilisateur |

See [references/apex-style-guide.md](references/apex-style-guide.md) for complete style guide.

---

## Modes

| Flag | Mode | Output Location | user-invocable |
|------|------|-----------------|----------------|
| (none) | User skill | `skills/{name}/SKILL.md` | `true` |
| `--core` | Core skill | `skills/core/{name}/SKILL.md` | `false` |
| `--workflow` | Skill with steps | `skills/{name}/` + `steps/` | `true` |

---

## Mode Workflow (--workflow)

Genere une structure avec steps separes pour les skills multi-phases.

### Quand Utiliser

- :white_check_mark: Workflows avec 3+ phases distinctes
- :white_check_mark: Besoin de branches conditionnelles
- :white_check_mark: Breakpoints a chaque phase
- :red_circle: NEVER pour skills simples (< 3 phases)

### Structure Generee

```
skills/{name}/
├── SKILL.md                    # Router vers steps/
├── steps/
│   ├── step-00-init.md         # Initialisation
│   ├── step-01-{phase1}.md     # Phase 1
│   ├── step-02-{phase2}.md     # Phase 2
│   ├── step-0Xb-{variant}.md   # Branche conditionnelle (optionnel)
│   └── step-99-finish.md       # Finalisation
└── references/
    └── {domain}.md
```

### SKILL.md Router Template

Le SKILL.md principal agit comme router :

```markdown
## MANDATORY EXECUTION RULES (READ FIRST):

- :red_circle: NEVER execute steps out of order
- :white_check_mark: ALWAYS start with step-00-init.md
- :white_check_mark: ALWAYS follow next_step from each step

## EXECUTION PROTOCOLS:

1. **Load** step-00-init.md
2. **Execute** current step protocols
3. **Evaluate** next step trigger
4. **Proceed** to next_step or conditional_next

## CONTEXT BOUNDARIES:

- IN scope: {skill scope}
- OUT scope: {exclusions}
```

### Step Template

Chaque step suit ce format :

```markdown
---
name: step-XX-{name}
description: {short description}
prev_step: steps/step-XX-{prev}.md
next_step: steps/step-XX-{next}.md
conditional_next:
  - condition: "{expression}"
    step: steps/step-XXb-{variant}.md
---

# Step XX: {Name}

## MANDATORY EXECUTION RULES (READ FIRST):

- :red_circle: NEVER {rule}
- :white_check_mark: ALWAYS {rule}

## EXECUTION PROTOCOLS:

1. **{Verb}** {action}

## NEXT STEP TRIGGER:

When {condition}, proceed to `next_step`.
```

---

## Workflow Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    FACTORY 6-PHASE WORKFLOW                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Phase 1: PRE-ANALYSIS                                          │
│  └─ Questions: purpose, triggers, scope, frequency              │
│     └─ Decision Gate: proceed / stop (one-off prompt)           │
│                                                                  │
│  Phase 2: ARCHITECTURE                                          │
│  └─ Structure: Simple / Standard / Advanced                     │
│  └─ Define files and references needed                          │
│                                                                  │
│  Phase 3: DESCRIPTION ENGINEERING                               │
│  └─ Craft description for optimal triggering                    │
│  └─ Apply formula: CAPABILITIES + USE CASES + TRIGGERS          │
│  └─ Validate: < 1024 chars                                      │
│                                                                  │
│  Phase 4: WORKFLOW DESIGN                                       │
│  └─ Define numbered steps                                       │
│  └─ Create decision tree (if multi-path)                        │
│  └─ Add input/output examples                                   │
│                                                                  │
│  Phase 5: VALIDATION (Dry-Run)                                  │
│  └─ 12-point checklist                                          │
│  └─ Preview structure + SKILL.md                                │
│  └─ BREAKPOINT: User approval                                   │
│                                                                  │
│  Phase 6: GENERATION                                            │
│  └─ Create all files                                            │
│  └─ Update plugin.json if needed                                │
│  └─ Conformity report                                           │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Phase 1: Pre-Analysis

### Discovery Questions

Ask these questions to understand the skill need:

1. **Purpose**: What problem does this skill solve?
2. **Frequency**: How often will this be used? (daily/weekly/rare)
3. **Triggers**: What phrases would invoke this skill?
4. **Scope**: What's in scope? What's explicitly out of scope?
5. **Persona**: Who uses this skill? (all users / specific role)

### Decision Gate

**PROCEED** if:
- Used more than once
- Has clear triggers
- Solves repeatable problem

**STOP** if:
- One-time task → use conversation directly
- Volatile procedure → document elsewhere
- Runtime config → use settings/env

---

## Phase 2: Architecture

### Structure Options

| Structure | When to Use | Files |
|-----------|-------------|-------|
| **Simple** | Single workflow, < 200 lines | `SKILL.md` only |
| **Standard** | Multi-step, references needed | `SKILL.md` + `references/` |
| **Advanced** | Templates, scripts, multi-workflow | Full structure |

### File Structure Templates

**Simple:**
```
skills/{name}/
└── SKILL.md
```

**Standard:**
```
skills/{name}/
├── SKILL.md
└── references/
    ├── checklist.md
    └── examples.md
```

**Advanced:**
```
skills/{name}/
├── SKILL.md
├── references/
│   ├── detailed-guide.md
│   └── examples.md
├── templates/
│   └── output-template.md
└── scripts/
    └── helper.py
```

### Tools Selection

Choose allowed-tools based on skill needs:

| Need | Tools |
|------|-------|
| Read-only analysis | `Read, Glob, Grep` |
| File modifications | `Read, Write, Edit` |
| User interaction | `AskUserQuestion` |
| Command execution | `Bash` |
| Exploration | `Read, Glob, Grep` + `agent: Explore` |

---

## Phase 3: Description Engineering

### Formula

```
DESCRIPTION = [CAPABILITIES] + [USE CASES] + [TRIGGERS] + [BOUNDARIES]
```

### Components

| Component | Purpose | Example |
|-----------|---------|---------|
| CAPABILITIES | What it does | "Generates API documentation" |
| USE CASES | When to use | "Use when documenting endpoints" |
| TRIGGERS | Natural phrases | "Trigger: API docs, document API" |
| BOUNDARIES | What it doesn't do | "Not for: internal docs" |

### Examples

**Good Description:**
```yaml
description: >-
  Generates comprehensive API documentation from code.
  Extracts endpoints, parameters, responses, and examples.
  Use when: documenting REST APIs, creating OpenAPI specs,
  updating endpoint docs. Triggers: API docs, document API,
  endpoint documentation. Not for: internal code docs.
```

**Bad Description:**
```yaml
description: "Documentation helper"  # Too vague, won't trigger
```

### Validation Rules

- **Length**: 50-150 words (< 1024 characters)
- **Trigger words**: Include 3-5 natural phrases
- **Specificity**: Avoid generic terms ("helper", "utility")
- **Action verbs**: Start with what it does

See [references/description-formulas.md](references/description-formulas.md) for patterns.

---

## Phase 4: Workflow Design

### Numbered Steps

Every skill needs clear, numbered steps:

```markdown
## Workflow

1. **Analyze** input requirements
2. **Validate** preconditions
3. **Execute** main logic
4. **Verify** results
5. **Report** outcome
```

### Decision Trees

For multi-path skills:

```markdown
## Decision Tree

IF input is file path:
  → Read and analyze file
  → Generate documentation
ELSE IF input is directory:
  → Scan all files
  → Generate index + per-file docs
ELSE:
  → Ask for clarification
```

### Input/Output Examples

Always include:

```markdown
## Examples

### Input
```
/doc-generator src/api/users.ts
```

### Output
```markdown
# Users API

## GET /users
Returns list of users...
```
```

---

## Phase 5: Validation (Dry-Run + Automated Script)

### 12-Point Checklist

Before generation, verify:

| # | Check | Required |
|---|-------|----------|
| 1 | `name` is unique and kebab-case | Yes |
| 2 | `name` length ≤ 64 characters | Yes |
| 3 | `description` is specific (not vague) | Yes |
| 4 | `description` length < 1024 chars | Yes |
| 5 | Description has trigger words | Yes |
| 6 | SKILL.md body < 500 lines | Yes |
| 7 | All referenced files exist | Yes |
| 8 | `allowed-tools` is appropriate | Yes |
| 9 | Workflow steps are numbered | Yes |
| 10 | Examples included | Recommended |
| 11 | Error handling defined | Recommended |
| 12 | Limitations documented | Recommended |

See [references/checklist-validation.md](references/checklist-validation.md) for details.

### Automated Validation

Run the validation script on the preview structure:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/factory/scripts/validate_skill_output.py <skill_path>
```

Options:
- Default mode: All checks are blocking
- `--permissive`: Recommended checks become warnings only

### Preview

Show user:
1. File structure to create
2. SKILL.md preview (first 50 lines)
3. **Automated validation report** (from script)

### BREAKPOINT

```
┌─────────────────────────────────────────────────────────────────┐
│ [VALIDATION] Skill Ready for Generation                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│ Skill: {name}                                                   │
│ Type: {user | core}                                             │
│ Structure: {simple | standard | advanced}                       │
│                                                                  │
│ Files to create:                                                │
│ • skills/{path}/{name}/SKILL.md                                 │
│ • skills/{path}/{name}/references/...                           │
│                                                                  │
│ Validation: ✅ PASS (12/12) or ❌ FAIL (N issues)               │
│                                                                  │
├─────────────────────────────────────────────────────────────────┤
│ [A] Generate  [B] Modify  [C] Cancel                            │
└─────────────────────────────────────────────────────────────────┘
```

---

## Phase 6: Generation

### Actions

1. **Create directory structure**
2. **Write SKILL.md** with full content
3. **Write reference files** if needed
4. **Update plugin.json** (add skill path)
5. **Run post-generation validation**:
   ```bash
   python3 ${CLAUDE_PLUGIN_ROOT}/skills/factory/scripts/validate_skill_output.py <generated_skill_path>
   ```
6. **Generate conformity report**

### Conformity Report

```markdown
## Generation Complete

✅ Created: skills/{name}/SKILL.md
✅ Created: skills/{name}/references/checklist.md
✅ Updated: .claude-plugin/plugin.json
✅ Validation: PASS (12/12 checks)

### Skill Summary
- Name: {name}
- Type: {user | core}
- Lines: {count}
- References: {count}

### Next Steps
1. Test with: /{name} [args]
2. Verify auto-triggering works
3. Add to documentation if public
```

---

## Reference Files

- [apex-style-guide.md](references/apex-style-guide.md) — APEX style formatting rules
- [best-practices-synthesis.md](references/best-practices-synthesis.md) — Core best practices
- [checklist-validation.md](references/checklist-validation.md) — 12-point validation
- [description-formulas.md](references/description-formulas.md) — Description patterns
- [yaml-rules.md](references/yaml-rules.md) — Frontmatter syntax
- [skill-templates.md](references/skill-templates.md) — User, core, and workflow templates

---

## Anti-Patterns

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| Vague description | Won't trigger correctly | Use formula with triggers |
| Everything in SKILL.md | Context overflow | Use progressive disclosure |
| No examples | Users confused | Add input/output examples |
| Generic name | Conflicts possible | Use specific, unique names |
| Multi-purpose | Hard to trigger | Split into focused skills |

---

## Limitations

This skill does NOT:
- Create subagents (different workflow)
- Modify existing skills (use edit manually)
- Generate tests automatically
