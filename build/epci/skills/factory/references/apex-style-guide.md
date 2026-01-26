# APEX Style Guide

> Reference complete pour le style APEX dans les skills EPCI v6.

---

## 1. Icones Standardisees

### Table de Reference

| Icone | Keyword | Usage | Exemple |
|-------|---------|-------|---------|
| 🔴 | NEVER | Action interdite critique | `🔴 NEVER modify files during exploration` |
| ✅ | ALWAYS | Action obligatoire | `✅ ALWAYS validate plan with user` |
| ⛔ | FORBIDDEN | Blocage dur (error si viole) | `⛔ FORBIDDEN skip TDD for STANDARD+ tasks` |
| 🔵 | POSTURE | Mindset/attitude | `🔵 YOU ARE A SKEPTICAL REVIEWER` |
| 💭 | FOCUS | Concentration mentale | `💭 FOCUS on test coverage first` |
| ⚠️ | WARNING | Attention particuliere | `⚠️ WARNING security implications` |
| ⏸️ | BREAKPOINT | Point d'arret utilisateur | `⏸️ BREAKPOINT — Plan Validation` |

### Regles d'Utilisation

1. **🔴 NEVER** — Reserve aux interdictions critiques (max 5 par skill)
2. **✅ ALWAYS** — Reserve aux obligations fondamentales (max 5 par skill)
3. **⛔ FORBIDDEN** — Violations qui doivent stopper l'execution
4. **🔵 POSTURE** — Pour les attitudes de travail
5. **💭 FOCUS** — Pour orienter l'attention
6. **⚠️ WARNING** — Pour les risques a considerer
7. **⏸️ BREAKPOINT** — Uniquement pour les points de decision utilisateur

---

## 2. Structure de Skill APEX

### 2.1 Sections Obligatoires

```markdown
## MANDATORY EXECUTION RULES (READ FIRST):

- 🔴 NEVER [rule 1]
- 🔴 NEVER [rule 2]
- ✅ ALWAYS [rule 3]
- ✅ ALWAYS [rule 4]
- 🔵 [posture]
- 💭 [focus]
- ⛔ FORBIDDEN [hard block]

## EXECUTION PROTOCOLS:

1. **{Verb}** {description}
2. **{Verb}** {description}
3. **{Verb}** {description}

## CONTEXT BOUNDARIES:

- IN scope: {what's included}
- OUT scope: {what's excluded}
```

### 2.2 Sections Optionnelles

```markdown
## OUTPUT FORMAT:

{Specification du format de sortie}

## ERROR HANDLING:

| Error | Cause | Resolution |
|-------|-------|------------|
| {error} | {cause} | {fix} |

## BREAKPOINT:

┌─────────────────────────────────────────────────────────────────────┐
│ ⏸️ BREAKPOINT — {Title}                                             │
├─────────────────────────────────────────────────────────────────────┤
│ {Context}                                                           │
│ ┌─ Options ──────────────────────────────────────────────────────┐ │
│ │  1. {Option 1} (Recommended)                                   │ │
│ │  2. {Option 2}                                                 │ │
│ └────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘

## NEXT STEP TRIGGER:

When {condition}, proceed to `{next_step}`.
```

---

## 3. Exemples Avant/Apres

### Exemple 1: Workflow d'Exploration

**AVANT (style prose):**
```markdown
## Phase 1: Exploration

During this phase, you should carefully examine the codebase to
understand the existing patterns. It's important not to make any
changes to the files while you're exploring, as this could cause
issues. Make sure to identify all relevant files and note any
patterns that should be followed.
```

**APRES (style APEX):**
```markdown
## MANDATORY EXECUTION RULES (READ FIRST):

- 🔴 NEVER modify files during exploration
- 🔴 NEVER skip pattern identification
- ✅ ALWAYS use read-only tools (Read, Glob, Grep)
- ✅ ALWAYS document identified patterns

## EXECUTION PROTOCOLS:

1. **Identify** relevant files with Glob
2. **Analyze** existing patterns in code
3. **Document** patterns for implementation phase
```

### Exemple 2: Code Review

**AVANT (style prose):**
```markdown
## Code Review

When reviewing code, try to be thorough and look for potential issues.
Consider security implications and make sure tests are adequate.
Don't just approve without careful analysis.
```

**APRES (style APEX):**
```markdown
## MANDATORY EXECUTION RULES (READ FIRST):

- 🔴 NEVER auto-approve without analysis
- 🔴 NEVER skip security check
- ✅ ALWAYS verify test coverage
- ✅ ALWAYS check for OWASP top 10
- 🔵 YOU ARE A SKEPTICAL REVIEWER, not a defender
- 💭 FOCUS on edge cases and failure modes

## EXECUTION PROTOCOLS:

1. **Verify** test coverage meets threshold
2. **Scan** for security vulnerabilities
3. **Review** edge case handling
4. **Report** findings with severity
```

---

## 4. Anti-Patterns

### 4.1 A Eviter

| Anti-Pattern | Probleme | Solution |
|--------------|----------|----------|
| Longs paragraphes | Difficile a scanner | Convertir en listes |
| Regles implicites | Facile a manquer | Expliciter avec icones |
| Trop de 🔴 | Dilue l'importance | Max 5 NEVER par skill |
| ⛔ pour tout | Trop restrictif | Reserve aux violations critiques |
| Pas de CONTEXT BOUNDARIES | Scope ambigu | Toujours definir IN/OUT |
| Prose dans PROTOCOLS | Verbeux | Actions numerotees courtes |

### 4.2 Exemples d'Anti-Patterns

**MAUVAIS — Trop de prose:**
```markdown
## Mandatory Rules

You should always make sure to read the files before modifying them.
This is really important because you need to understand what you're
changing. Also, never forget to run the tests.
```

**BON — Format APEX:**
```markdown
## MANDATORY EXECUTION RULES (READ FIRST):

- 🔴 NEVER modify files without reading first
- ✅ ALWAYS run tests after changes
```

**MAUVAIS — Trop de NEVER:**
```markdown
- 🔴 NEVER do X
- 🔴 NEVER do Y
- 🔴 NEVER do Z
- 🔴 NEVER do A
- 🔴 NEVER do B
- 🔴 NEVER do C
- 🔴 NEVER do D
- 🔴 NEVER do E
```

**BON — Prioriser les critiques:**
```markdown
- 🔴 NEVER do X (security critical)
- 🔴 NEVER do Y (data integrity)
- ⚠️ WARNING avoid Z when possible
- ⚠️ WARNING consider alternatives to A
```

---

## 5. Checklist Validation Style

### Pour Skills Simples

- [ ] `MANDATORY EXECUTION RULES` en premiere section
- [ ] Max 5 `🔴 NEVER` rules
- [ ] Max 5 `✅ ALWAYS` rules
- [ ] `EXECUTION PROTOCOLS` avec actions numerotees
- [ ] `CONTEXT BOUNDARIES` avec IN/OUT explicites
- [ ] Pas de paragraphes > 3 lignes
- [ ] Verbes d'action en debut de protocole

### Pour Skills avec Steps

- [ ] Tout ci-dessus, plus:
- [ ] Chaque step a son propre `MANDATORY EXECUTION RULES`
- [ ] Frontmatter avec `prev_step`/`next_step`
- [ ] `NEXT STEP TRIGGER` explicite
- [ ] Breakpoints aux points de decision

---

## 6. Templates Rapides

### Template Minimal

```markdown
## MANDATORY EXECUTION RULES (READ FIRST):

- 🔴 NEVER {critical prohibition}
- ✅ ALWAYS {critical requirement}

## EXECUTION PROTOCOLS:

1. **{Verb}** {action}
2. **{Verb}** {action}

## CONTEXT BOUNDARIES:

- IN scope: {included}
- OUT scope: {excluded}
```

### Template Step

```markdown
---
name: step-XX-{name}
description: {short description}
prev_step: steps/step-XX-{prev}.md
next_step: steps/step-XX-{next}.md
---

# Step XX: {Name}

## MANDATORY EXECUTION RULES (READ FIRST):

- 🔴 NEVER {rule}
- ✅ ALWAYS {rule}

## EXECUTION PROTOCOLS:

1. **{Verb}** {action}

## NEXT STEP TRIGGER:

When {condition}, proceed to `{next_step}`.
```

---

## 7. Integration Factory

Factory applique automatiquement ces regles lors de la generation:

1. **Validation pre-generation** — Verifie structure APEX
2. **Injection templates** — Utilise templates style APEX
3. **Post-validation** — Verifie conformite icones

Voir [skill-templates.md](skill-templates.md) pour les templates complets.
