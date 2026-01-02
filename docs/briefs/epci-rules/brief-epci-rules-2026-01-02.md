# Feature Brief — EPCI Rules Generator

> **Slug**: `epci-rules`
> **Date**: 2026-01-02
> **Complexité estimée**: STANDARD (4-10 fichiers, tests requis)
> **EMS Final**: 92/100

---

## 1. Objectif Fonctionnel

Créer une commande `/epci:rules` qui analyse automatiquement un projet pour générer une structure `.claude/rules/` optimisée. Cette commande maintient la cohérence entre le fichier `CLAUDE.md` (vision fonctionnelle/projet) et les rules (conventions techniques par stack).

### Problème résolu

- Absence de conventions documentées dans les projets
- Incohérence entre le code et les bonnes pratiques
- Temps perdu à redécouvrir les patterns à chaque session
- Drift entre conventions déclarées et code réel

### Valeur ajoutée

- Génération automatique basée sur l'analyse du codebase (Niveau 3)
- Templates issus des skills stack existants (source unique de vérité)
- Validation via agent dédié (@rules-validator)
- Traçabilité via hook post-rules-init

---

## 2. Architecture Cible

### 2.1 Composants à créer

| Composant | Fichier | Modèle | Rôle |
|-----------|---------|--------|------|
| **Command** | `src/commands/rules.md` | — | Orchestration des 4 actions |
| **Skill** | `src/skills/core/rules-generator/SKILL.md` | — | Logique génération + détection Niveau 3 |
| **Agent** | `src/agents/rules-validator.md` | opus | Validation syntaxe, cohérence, complétude, qualité |
| **Script** | `src/scripts/validate_rules.py` | — | Validation technique Python |
| **Hook** | `src/hooks/active/post-rules-init.py` | — | Sauvegarde project-memory |

### 2.2 Extensions des skills stack existants

Ajouter un dossier `rules-templates/` dans chaque skill stack:

```
src/skills/stack/
├── php-symfony/
│   ├── SKILL.md
│   ├── references/
│   └── rules-templates/          # NOUVEAU
│       ├── backend-symfony.md
│       ├── testing-phpunit.md
│       └── security-symfony.md
├── python-django/
│   ├── SKILL.md
│   ├── references/
│   └── rules-templates/          # NOUVEAU
│       ├── backend-django.md
│       ├── testing-pytest.md
│       └── api-drf.md
├── javascript-react/
│   ├── SKILL.md
│   ├── references/
│   └── rules-templates/          # NOUVEAU
│       ├── frontend-react.md
│       ├── state-management.md
│       └── testing-vitest.md
├── java-springboot/
│   ├── SKILL.md
│   ├── references/
│   └── rules-templates/          # NOUVEAU
│       ├── backend-spring.md
│       ├── testing-junit.md
│       └── security-spring.md
└── frontend-editor/
    ├── SKILL.md
    ├── references/
    └── rules-templates/          # NOUVEAU
        ├── styling-tailwind.md
        └── accessibility.md
```

### 2.3 Structure générée dans les projets cibles

```
project/
├── backend/                      # Django ou Symfony
├── frontend/                     # React + Tailwind
├── .claude/
│   ├── CLAUDE.md                 # Vision fonctionnelle (>50 lignes)
│   └── rules/
│       ├── _global/
│       │   ├── quality.md
│       │   ├── git-workflow.md
│       │   └── commands.md
│       ├── backend/
│       │   └── {django|symfony}.md   # Avec paths: backend/**/*.py
│       ├── frontend/
│       │   ├── react.md              # Avec paths: frontend/**/*.tsx
│       │   └── tailwind.md           # Avec paths: frontend/**/*.css
│       ├── testing/
│       │   └── {pytest|phpunit|vitest}.md
│       └── domain/
│           └── glossary.md
└── .project-memory/              # Mis à jour par hook
```

---

## 3. Spécifications Techniques

### 3.1 Détection Niveau 3

La commande effectue une analyse en 3 niveaux:

| Niveau | Analyse | Méthode |
|--------|---------|---------|
| **1. Stack** | Frameworks détectés | composer.json, package.json, requirements.txt, pom.xml |
| **2. Architecture** | Patterns structurels | Analyse dossiers (backend/, frontend/, src/, apps/) |
| **3. Conventions** | Nommage, patterns récurrents | Analyse AST léger (classes, fonctions, imports) |

### 3.2 Format CLAUDE.md enrichi

```markdown
# {Nom du Projet}

## Description

{Brief fonctionnel du projet en 3-5 phrases. Objectif métier principal,
utilisateurs cibles, valeur délivrée.}

## Architecture

- **Pattern**: {MVC | DDD | Clean Architecture | Hexagonal}
- **Structure**: Monorepo avec backend/ et frontend/ séparés
- **Backend**: {Description du backend et ses responsabilités}
- **Frontend**: {Description du frontend et son rôle}

## Stack Technique

| Couche | Technologie | Version | Notes |
|--------|-------------|---------|-------|
| Backend | {Django/Symfony} | {x.x} | {notes} |
| Frontend | React | {x.x} | Islands architecture |
| Styling | Tailwind CSS | {x.x} | Design tokens custom |
| Database | {PostgreSQL/MySQL} | {x.x} | |
| Cache | {Redis} | {x.x} | Si applicable |
| Queue | {Celery/Messenger} | {x.x} | Si applicable |

## Décisions Architecturales

| Décision | Choix | Rationale |
|----------|-------|-----------|
| State management | Zustand | Léger, adapté aux islands |
| API | REST + DRF/API Platform | Standard, bien outillé |
| Auth | {JWT/Session} | {Raison} |

## Commandes Essentielles

```bash
# Développement
{cmd_dev_backend}      # Lancer le backend
{cmd_dev_frontend}     # Lancer le frontend

# Tests
{cmd_test}             # Lancer tous les tests

# Qualité
{cmd_lint}             # Linting
{cmd_format}           # Formatting
```

## Conventions

Les conventions techniques détaillées sont dans `.claude/rules/`:

| Domaine | Fichier | Scope |
|---------|---------|-------|
| Backend | `rules/backend/{framework}.md` | `backend/**/*` |
| Frontend | `rules/frontend/react.md` | `frontend/**/*.tsx` |
| Styling | `rules/frontend/tailwind.md` | `frontend/**/*.css` |
| Tests | `rules/testing/*.md` | `**/tests/**/*` |
| Qualité | `rules/_global/quality.md` | Tout le projet |

## Équipe & Contacts

- **Tech Lead**: {nom}
- **Repository**: {url}
- **Documentation**: {url}
```

### 3.3 Format des fichiers rules

```markdown
---
paths:
  - backend/**/*.py
  - "!backend/**/migrations/**"
---

# {Framework} Rules

> Conventions pour le développement {framework} dans ce projet.

## 🔴 CRITICAL (Ne jamais violer)

1. **{Règle absolue 1}**: {Explication}
2. **{Règle absolue 2}**: {Explication}

## 🟡 CONVENTIONS (Standard du projet)

- {Convention 1}: {détail}
- {Convention 2}: {détail}

## 🟢 PRÉFÉRENCES (Quand applicable)

- {Préférence 1}
- {Préférence 2}

## Quick Reference

| Task | Pattern |
|------|---------|
| {Tâche 1} | {Pattern} |
| {Tâche 2} | {Pattern} |

## Common Patterns

| Pattern | Implementation | Benefit |
|---------|----------------|---------|
| {Pattern 1} | {Code/description} | {Avantage} |

## Anti-patterns

| Anti-pattern | Problem | Alternative |
|--------------|---------|-------------|
| {Anti-pattern 1} | {Problème} | {Solution} |

## Examples

### Correct

```{lang}
// Exemple de code correct
```

### Incorrect

```{lang}
// Exemple à éviter
```
```

### 3.4 Paths patterns pour frontend-editor

**CRITIQUE**: Les paths doivent matcher correctement pour l'auto-activation.

```yaml
# rules/frontend/tailwind.md
---
paths:
  - frontend/**/*.css
  - frontend/**/*.scss
  - frontend/tailwind.config.*
  - "!frontend/node_modules/**"
---

# rules/frontend/react.md
---
paths:
  - frontend/**/*.tsx
  - frontend/**/*.jsx
  - frontend/**/*.ts
  - "!frontend/**/*.test.ts"
  - "!frontend/**/*.test.tsx"
  - "!frontend/node_modules/**"
---
```

### 3.5 Extraction depuis les skills (marqueurs inline)

Dans chaque skill stack, ajouter des marqueurs pour identifier les sections à extraire:

```markdown
<!-- RULE:backend/{framework}.md:CRITICAL -->
## Thin Controller Pattern
...
<!-- /RULE -->

<!-- RULE:backend/{framework}.md:CONVENTIONS -->
### Naming Conventions
...
<!-- /RULE -->

<!-- RULE:backend/{framework}.md:PATTERNS -->
## Common Patterns
...
<!-- /RULE -->
```

---

## 4. Actions de la Commande

### 4.1 `init` (P1 - Prioritaire)

```
/epci:rules init [--force] [--dry-run]
```

**Workflow:**
1. Détection Niveau 3 du projet
2. Identification des skills stack applicables
3. Génération de CLAUDE.md (vision fonctionnelle)
4. Génération de .claude/rules/ (conventions techniques)
5. Invocation @rules-validator
6. Exécution hook post-rules-init
7. Affichage rapport

**Flags:**
- `--force`: Écraser les fichiers existants sans confirmation
- `--dry-run`: Afficher ce qui serait généré sans créer les fichiers

### 4.2 `validate` (P1 - Prioritaire)

```
/epci:rules validate [--fix]
```

**Workflow:**
1. Lire les rules existantes
2. Analyser le code actuel
3. Détecter le drift (violations des rules)
4. Générer rapport avec localisation
5. Optionnel: proposer corrections

**Output:**
```
⚠️ Drift détecté (3 violations):

1. rules/backend/django.md:12 — "Services in services/"
   → apps/lots/views.py:45 contient logique métier

2. rules/frontend/react.md:8 — "Jamais any"
   → frontend/src/utils/helpers.ts:12 utilise 'any'

3. rules/frontend/tailwind.md:5 — "Pas de styles inline"
   → frontend/src/components/Card.tsx:23 utilise style={}

Actions: [fix] [ignore] [update-rules]
```

### 4.3 `update` (P2)

```
/epci:rules update
```

**Workflow:**
1. Analyser les nouveaux patterns dans le code
2. Comparer avec les rules existantes
3. Proposer des ajouts/modifications
4. Demander confirmation
5. Appliquer les changements

### 4.4 `sync` (P3 - Différé v1.1)

```
/epci:rules sync
```

**Workflow:**
1. Détecter les linters existants (.eslintrc, phpstan.neon, ruff.toml)
2. Parser leurs règles
3. Importer dans le format rules
4. Éviter la duplication

---

## 5. Agent @rules-validator

### 5.1 Spécification

```yaml
name: rules-validator
description: >-
  Validates generated .claude/rules/ structure. Checks YAML frontmatter syntax,
  paths patterns validity, alignment with codebase, completeness for detected
  stacks, and quality (sections present, examples included). Returns APPROVED,
  NEEDS_REVISION, or REJECTED with detailed report.
model: opus
allowed-tools: [Read, Glob, Grep]
```

### 5.2 Critères de validation

| Catégorie | Checks |
|-----------|--------|
| **Syntaxe** | YAML frontmatter valide, paths patterns corrects, markdown bien formé |
| **Cohérence** | Rules alignées avec le code, pas de références à des fichiers inexistants |
| **Complétude** | Toutes les stacks détectées ont leurs rules, sections obligatoires présentes |
| **Qualité** | Sections 🔴/🟡/🟢 présentes, Quick Reference, Patterns, Anti-patterns, Examples |

### 5.3 Format de sortie

```markdown
## Rules Validation Report

### Verdict
[APPROVED | NEEDS_REVISION | REJECTED]

### Summary
- Files validated: X
- Issues found: Y (Z critical)

### Issues

#### 🔴 Critical
- [file:line] {description}

#### 🟡 Warning
- [file:line] {description}

#### 🟢 Suggestion
- [file:line] {description}

### Recommendations
1. {Recommandation 1}
2. {Recommandation 2}
```

---

## 6. Hook post-rules-init

### 6.1 Spécification

```python
# src/hooks/active/post-rules-init.py

"""
Hook exécuté après /epci:rules init
Sauvegarde la configuration générée dans .project-memory/
"""

def run(context: dict) -> None:
    """
    context = {
        "action": "init",
        "stacks_detected": ["python-django", "javascript-react", "frontend-editor"],
        "files_created": [".claude/CLAUDE.md", ".claude/rules/..."],
        "validation_verdict": "APPROVED",
        "timestamp": "2026-01-02T14:30:00Z"
    }
    """
    # Sauvegarder dans .project-memory/rules-history.json
    # Mettre à jour .project-memory/context.json avec stacks
    pass
```

---

## 7. Exploration Summary

### 7.1 Codebase analysé

- **Structure**: EPCI v4.4 avec 10 commands, 24 skills, 9 agents
- **Skills stack existants**: 5 (php-symfony, python-django, javascript-react, java-springboot, frontend-editor)
- **Patterns de validation**: Scripts Python dans src/scripts/
- **Factory system**: src/skills/factory/ pour création de composants

### 7.2 Fichiers candidats

| Action | Fichier |
|--------|---------|
| Créer | `src/commands/rules.md` |
| Créer | `src/skills/core/rules-generator/SKILL.md` |
| Créer | `src/skills/core/rules-generator/references/*.md` |
| Créer | `src/agents/rules-validator.md` |
| Créer | `src/scripts/validate_rules.py` |
| Créer | `src/hooks/active/post-rules-init.py` |
| Modifier | `src/skills/stack/*/` (ajouter rules-templates/) |
| Modifier | `src/commands/brief.md` (auto-suggestion si .claude/ absent) |

### 7.3 Dépendances

- **Skills requis**: project-memory (stack detection), code-conventions
- **Subagents**: @rules-validator (nouveau)
- **Hooks**: post-rules-init (nouveau)
- **Scripts**: validate_rules.py (nouveau)

---

## 8. Critères d'acceptation

- [ ] `/epci:rules init` génère CLAUDE.md + rules/ pour un projet Django+React+Tailwind
- [ ] `/epci:rules validate` détecte le drift entre code et rules
- [ ] Les paths patterns s'auto-activent correctement (frontend-editor inclus)
- [ ] @rules-validator valide la structure générée
- [ ] Hook post-rules-init sauvegarde dans .project-memory/
- [ ] Script validate_rules.py passe pour les rules générées
- [ ] Documentation mise à jour (CLAUDE.md principal)

---

## 9. Prochaines étapes

1. **Lancer `/epci:brief`** avec ce brief pour affiner les fichiers impactés
2. **Phase 1 (Plan)**: Détailler l'implémentation de chaque composant
3. **Phase 2 (Code)**: Implémenter dans l'ordre:
   - Skill rules-generator (logique de base)
   - Templates dans skills stack
   - Command rules.md
   - Agent @rules-validator
   - Script validate_rules.py
   - Hook post-rules-init
4. **Phase 3 (Inspect)**: Tests + documentation

---

*Brief généré par /brainstorm — EMS 92/100*
