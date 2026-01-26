# APEX Style Integration — EPCI v6

> **Date**: 2026-01-26
> **Version**: 6.0.3
> **Objectif**: Standardiser le format des skills EPCI avec le style APEX

---

## Vue d'Ensemble

Le style APEX apporte un format plus directif et scannable pour les skills :
- **Rules-first** avec icones standardisees
- **Structure steps** pour workflows multi-phases
- **Moins de prose**, plus de listes et tables

---

## 1. Conventions de Formatage APEX

### 1.1 Icones Standardisees

| Icone | Keyword | Signification | Usage |
|-------|---------|---------------|-------|
| :red_circle: | NEVER | Actions strictement interdites | Hard rule, violation = echec |
| :white_check_mark: | ALWAYS | Actions obligatoires | Hard rule, must execute |
| :no_entry: | FORBIDDEN | Blocage dur | Error if violated |
| :large_blue_circle: | POSTURE | Mindset/attitude a adopter | Soft guidance |
| :thought_balloon: | FOCUS | Ce sur quoi se concentrer | Mental directive |
| :warning: | WARNING | Attention particuliere | Caution flag |
| :pause_button: | BREAKPOINT | Point d'arret utilisateur | User decision required |

### 1.2 Structure Obligatoire de Section

```markdown
## MANDATORY EXECUTION RULES (READ FIRST):

- :red_circle: NEVER [action interdite critique]
- :red_circle: NEVER [autre interdiction]
- :white_check_mark: ALWAYS [obligation]
- :white_check_mark: ALWAYS [autre obligation]
- :large_blue_circle: [directive de posture/mindset]
- :thought_balloon: [focus mental]
- :no_entry: FORBIDDEN [hard block]

## EXECUTION PROTOCOLS:

1. [Action 1]
2. [Action 2]
3. [Action 3]

## CONTEXT BOUNDARIES:

- IN scope: [what's included]
- OUT scope: [what's excluded]

## OUTPUT FORMAT:

[Expected output specification]
```

---

## 2. Structure Steps pour Workflows

### 2.1 Quand Utiliser les Steps

| Skill | Steps ? | Raison |
|-------|---------|--------|
| `/factory` | Non (mais genere steps) | Workflow lineaire simple |
| `/brainstorm` | **Oui** | Phases distinctes (diverge, evaluate, converge) |
| `/spec` | **Oui** | Phases distinctes (analyze, decompose, generate) |
| `/implement` | **Oui** | 4+ phases avec conditionnels |
| `/quick` | Non | Trop simple |
| `/debug` | **Oui** | Phases distinctes (hypotheses, investigate, fix) |
| `/improve` | **Oui** | Phases distinctes (impact, plan, implement) |
| `/refactor` | **Oui** | Phases distinctes (analyze, plan, execute) |

### 2.2 Structure Repertoire Steps

```
skills/{name}/
├── SKILL.md                    # Entry point, routing
├── steps/
│   ├── step-00-init.md         # Initialisation
│   ├── step-01-{phase}.md      # Phase 1
│   ├── step-02-{phase}.md      # Phase 2
│   ├── step-0Xb-{variant}.md   # Branche conditionnelle
│   └── step-99-finish.md       # Finalisation
├── references/
│   └── {domain}.md
└── templates/
    └── {output}.md
```

### 2.3 Frontmatter de Step

```yaml
---
name: step-XX-{name}
description: {description courte}
prev_step: steps/step-XX-prev.md
next_step: steps/step-XX-next.md
conditional_next:
  - condition: "{expression}"
    step: steps/step-XXb-variant.md
---
```

### 2.4 Template de Step

```markdown
---
name: step-XX-{name}
description: {description}
prev_step: steps/step-XX-{prev}.md
next_step: steps/step-XX-{next}.md
---

# Step XX: {Name}

## MANDATORY EXECUTION RULES (READ FIRST):

- :red_circle: NEVER [rule 1]
- :white_check_mark: ALWAYS [rule 2]
- :no_entry: FORBIDDEN [rule 3]

## EXECUTION PROTOCOLS:

1. [Protocol 1]
2. [Protocol 2]
3. [Protocol 3]

## CONTEXT BOUNDARIES:

- [Boundary 1]
- [Boundary 2]

## OUTPUT FORMAT:

[Expected output format]

## BREAKPOINT (if applicable):

┌─────────────────────────────────────────────────────────────────────┐
│ :pause_button: BREAKPOINT — {Title}                                             │
├─────────────────────────────────────────────────────────────────────┤
│ [Context summary]                                                   │
│                                                                     │
│ ┌─ Options ──────────────────────────────────────────────────────┐ │
│ │  1. {Option 1} (Recommended)                                   │ │
│ │  2. {Option 2}                                                 │ │
│ │  3. {Option 3}                                                 │ │
│ │  4. [Free response]                                            │ │
│ └────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘

## NEXT STEP TRIGGER:

When [condition], proceed to `next_step`.
```

---

## 3. Mapping APEX → EPCI

### 3.1 Equivalences Structurelles

| APEX | EPCI v6 | Notes |
|------|---------|-------|
| `workflow/steps/` | `steps/` | Meme structure |
| `phase-XX-*.md` | `step-XX-*.md` | Renommage semantique |
| `CORE.md` | `SKILL.md` | Entry point |
| `conditional_phases` | `conditional_next` | Meme concept |

### 3.2 Equivalences Formatage

| APEX Pattern | EPCI Equivalent |
|--------------|-----------------|
| `## MANDATORY EXECUTION RULES` | Identique |
| `## EXECUTION PROTOCOLS` | Identique |
| `## CONTEXT BOUNDARIES` | Identique |
| `:red_circle: NEVER` | Identique |
| `:white_check_mark: ALWAYS` | Identique |
| `:no_entry: FORBIDDEN` | Identique |

---

## 4. Guide de Conversion Skills Existants

### 4.1 Checklist Conversion

- [ ] Identifier les sections en prose
- [ ] Extraire les regles implicites → `:red_circle: NEVER` / `:white_check_mark: ALWAYS`
- [ ] Convertir workflow en steps numerotes
- [ ] Ajouter `MANDATORY EXECUTION RULES` en debut
- [ ] Ajouter `CONTEXT BOUNDARIES` explicites
- [ ] Supprimer les paragraphes explicatifs redondants

### 4.2 Exemple Avant/Apres

**AVANT (style v5):**
```markdown
## Workflow

This skill helps you implement features. First, you should explore
the codebase to understand the existing patterns. Make sure not to
modify any files during this exploration phase. After exploration,
create a plan and validate it with the user.

### Phase 1: Exploration
Read the relevant files...
```

**APRES (style APEX):**
```markdown
## MANDATORY EXECUTION RULES (READ FIRST):

- :red_circle: NEVER modify files during exploration
- :white_check_mark: ALWAYS explore codebase before planning
- :white_check_mark: ALWAYS validate plan with user via breakpoint

## EXECUTION PROTOCOLS:

1. **Explore** codebase (read-only)
2. **Plan** implementation approach
3. **Validate** plan with breakpoint
4. **Implement** with TDD

## CONTEXT BOUNDARIES:

- IN scope: Feature implementation following EPCI phases
- OUT scope: Bug fixes (use /debug), refactoring (use /refactor)
```

---

## 5. Factory Integration

### 5.1 Nouveau Flag `--workflow`

```bash
/factory my-skill --workflow   # Genere structure avec steps/
/factory my-skill              # Genere structure simple (SKILL.md only)
```

### 5.2 Structure Generee avec `--workflow`

```
skills/{name}/
├── SKILL.md                    # Router vers steps/
├── steps/
│   ├── step-00-init.md
│   ├── step-01-{phase1}.md
│   └── step-99-finish.md
└── references/
```

### 5.3 Validation Style APEX

Factory valide automatiquement :
- Presence de `MANDATORY EXECUTION RULES`
- Utilisation des icones standardisees
- Structure steps si `--workflow`
- Absence de prose documentaire

---

## 6. Implementation Timeline

| Composant | Status | Notes |
|-----------|--------|-------|
| `/factory` + `--workflow` | En cours | Ajout flag + templates |
| `/implement` avec steps | En cours | 10 step files |
| `/brainstorm` avec steps | Planifie | Phase 2 |
| `/spec` avec steps | Planifie | Phase 2 |
| `/debug` avec steps | Planifie | Phase 2 |
| `/improve` avec steps | Planifie | Phase 2 |
| `/refactor` avec steps | Planifie | Phase 2 |

---

## 7. References

- [apex-style-guide.md](../../../src/skills/factory/references/apex-style-guide.md) — Guide complet du style APEX
- [skill-templates.md](../../../src/skills/factory/references/skill-templates.md) — Templates de skills
- [epci-v6-implementation-plan.md](epci-v6-implementation-plan.md) — Plan d'implementation v6
