---
paths:
  - src/agents/**/*.md
  - src/skills/**/*.md
  - "!src/**/references/**"
  - "!src/**/templates/**"
---

# Plugin Content Conventions

> Conventions pour le contenu Markdown du plugin (skills, agents).

## 🔴 CRITICAL

1. **Frontmatter YAML obligatoire**: Chaque fichier doit commencer par `---`
2. **Name unique**: Le champ `name` doit etre unique dans sa categorie
3. **Description <= 1024 chars**: Limite Claude Code pour descriptions
4. **Pas de duplication**: Ne pas repeter les references dans le SKILL.md principal

## 🟡 CONVENTIONS

### Naming fichiers

| Type | Convention | Exemple |
|------|------------|---------|
| Agents | `kebab-case.md` | `code-reviewer.md` |
| Skills | `dossier/SKILL.md` | `epci-core/SKILL.md` |

### Frontmatter par type

**Skill:**
```yaml
---
name: rules-generator
description: >-
  Generates .claude/rules/ structure for projects. Performs 3-level detection
  (stack, architecture, conventions) and creates CLAUDE.md + rules files.
  Use when: /epci:rules command invoked, project needs conventions setup.
  Not for: Manual rule editing, linter configuration, IDE settings.
---
```

**Agent:**
```yaml
---
name: code-reviewer
description: >-
  Reviews code quality, patterns, and standards compliance.
  Returns structured feedback with severity levels.
model: opus
allowed-tools: [Read, Grep, Glob]
---
```

### Limites Tokens

| Type | Limite | Raison |
|------|--------|--------|
| Skills | < 5000 | Performance |
| Agents | < 2000 | Focus |
| Descriptions | <= 1024 chars | Claude Code limit |

### Structure Skills

```
skill-name/
├── SKILL.md           # Definition principale (< 5000 tokens)
├── references/        # Details techniques (optionnel)
│   ├── patterns.md
│   └── examples.md
└── templates/         # Templates generables (optionnel)
```

## 🟢 PREFERENCES

- Utiliser references/ pour details techniques longs
- Tables pour quick reference
- Exemples avec Correct/Incorrect
- Emojis pour severity: 🔴 CRITICAL, 🟡 CONVENTIONS, 🟢 PREFERENCES

## Quick Reference

| Element | Limite |
|---------|--------|
| name | unique, kebab-case |
| description | <= 1024 chars, `>-` pour multiline |
| model (agents) | opus, sonnet, haiku |
| allowed-tools | Array valide |

## Common Patterns

| Pattern | Usage |
|---------|-------|
| `>-` YAML | Description multiline sans newlines |
| references/ | Split contenu technique |
| templates/ | Fichiers generables |
| Use when/Not for | Clarifier scope du skill |

## Anti-patterns

| Anti-pattern | Probleme | Alternative |
|--------------|----------|-------------|
| Skill monolithique | Depasse tokens | Split en references/ |
| Description trop courte | Contexte insuffisant | 2-3 phrases avec Use when |
| Duplication references | Maintenance difficile | Liens vers references/ |
| name avec espaces | Invalide | kebab-case uniquement |

## Examples

### Correct - Skill bien structure

```markdown
---
name: debugging-strategy
description: >-
  Strategie de debug structuree avec scoring hypotheses et arbre de pensee.
  Use when: Bug complexe, comportement inattendu, erreur difficile a reproduire.
  Not for: Erreurs evidentes, typos, bugs triviaux.
---

# Debugging Strategy

## Overview
[Contenu concis]

## Actions
[Reference vers references/thought-tree.md pour details]
```

### Incorrect - Skill trop long

```markdown
---
name: mega-skill
description: Does everything
---

# Mega Skill

[5000+ lignes de contenu...]
```
