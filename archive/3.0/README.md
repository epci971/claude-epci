# EPCI Plugin v3.0

> **E**xplore → **P**lan → **C**ode → **I**nspect

Workflow structuré pour le développement assisté par IA avec traçabilité complète.

---

## Table des matières

- [Quick Start](#quick-start)
- [Workflow EPCI](#workflow-epci)
- [Commandes](#commandes)
- [Routing par Complexité](#routing-par-complexité)
- [Subagents](#subagents)
- [Skills](#skills)
- [Scripts de Validation](#scripts-de-validation)
- [Architecture](#architecture)
- [Extension du Plugin](#extension-du-plugin)
- [Changelog v2.7 → v3.0](#changelog-v27--v30)

---

## Quick Start

### Installation

```bash
# Installation projet (recommandé)
cp -r src/ votre-projet/.claude/

# OU installation globale
cp -r src/ ~/.claude/
```

### Premier Usage

```bash
# 1. Décrivez votre besoin
/epci-brief "Ajouter une fonctionnalité d'authentification OAuth2"

# 2. Le plugin évalue la complexité et recommande un workflow
# 3. Suivez le workflow recommandé
```

### Workflow Typique

```
Utilisateur: /epci-brief "Ajouter un endpoint API pour les utilisateurs"

Claude: Analyse du brief...
        Complexité: STANDARD
        Recommandation: /epci

Utilisateur: /epci

Claude: Phase 1 - Analyse et Planning...
        [BREAKPOINT] Plan validé, continuer?

Utilisateur: Oui

Claude: Phase 2 - Implémentation TDD...
        [BREAKPOINT] Code reviewé, continuer?

Utilisateur: Oui

Claude: Phase 3 - Finalisation...
        Feature Document: docs/features/add-users-api.md
```

---

## Workflow EPCI

### Les 4 Phases

```
┌─────────────────────────────────────────────────────────────────┐
│                        WORKFLOW EPCI                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐ │
│   │ EXPLORE  │ →  │   PLAN   │ →  │   CODE   │ →  │ INSPECT  │ │
│   └──────────┘    └──────────┘    └──────────┘    └──────────┘ │
│        │               │               │               │        │
│        ▼               ▼               ▼               ▼        │
│   Comprendre      Concevoir       Implémenter     Vérifier      │
│   le codebase     la solution     avec TDD        et finaliser  │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

| Phase | Objectif | Output |
|-------|----------|--------|
| **Explore** | Comprendre le codebase et les patterns existants | Analyse contextuelle |
| **Plan** | Concevoir la stratégie d'implémentation | Plan technique validé |
| **Code** | Implémenter avec TDD (Red → Green → Refactor) | Code + tests |
| **Inspect** | Vérifier, documenter, finaliser | Feature Document complet |

### Feature Document

Chaque feature STANDARD/LARGE génère un document de traçabilité :

```
docs/features/<feature-slug>.md

├── §1 Brief Fonctionnel      ← /epci-brief
├── §2 Plan d'Implémentation  ← /epci Phase 1
├── §3 Rapport d'Implémentation ← /epci Phase 2
└── §4 Finalisation           ← /epci Phase 3
```

---

## Commandes

### Vue d'ensemble

| Commande | Description | Quand l'utiliser |
|----------|-------------|------------------|
| `/epci-brief` | Point d'entrée universel | Toujours commencer ici |
| `/epci` | Workflow complet 3 phases | Features STANDARD et LARGE |
| `/epci-quick` | Workflow condensé | Features TINY et SMALL |
| `/epci-spike` | Exploration time-boxée | Incertitude technique |
| `/epci:create` | Factory de composants | Créer skills/commands/agents |

### `/epci-brief` — Point d'entrée

```bash
/epci-brief "Description de votre besoin"
```

**Processus :**
1. Analyse du brief via `@Explore`
2. Clarification itérative (max 3 tours)
3. Évaluation de la complexité
4. Recommandation du workflow approprié

**Output :** Brief fonctionnel structuré avec recommandation

### `/epci` — Workflow Complet

```bash
/epci              # Mode standard
/epci --large      # Mode large (tous les subagents)
/epci --continue   # Reprendre une phase interrompue
```

**Phase 1 — Analyse et Planning**
- Thinking : `think hard`
- Skills : `epci-core`, `architecture-patterns`, stack auto-détecté
- Agents : `@Plan`, `@plan-validator`
- Output : §2 Plan d'Implémentation
- **BREAKPOINT** : Confirmation utilisateur

**Phase 2 — Implémentation TDD**
- Thinking : `think`
- Skills : `testing-strategy`, `code-conventions`, stack auto-détecté
- Agents : `@code-reviewer` (toujours), `@security-auditor` (conditionnel), `@qa-reviewer` (conditionnel)
- Output : §3 Rapport d'Implémentation
- **BREAKPOINT** : Confirmation utilisateur

**Phase 3 — Finalisation**
- Thinking : `think`
- Skills : `git-workflow`
- Agent : `@doc-generator`
- Output : §4 Finalisation (commits, docs, PR)

### `/epci-quick` — Workflow Condensé

```bash
/epci-quick
```

| Mode | Fichiers | LOC | Tests | Durée |
|------|----------|-----|-------|-------|
| **TINY** | 1 | < 50 | Non requis | < 15 min |
| **SMALL** | 2-3 | < 200 | Optionnels | 15-60 min |

**Exemples TINY :** Typos, fixes de config, petits ajustements
**Exemples SMALL :** Petites features, refactoring local

### `/epci-spike` — Exploration

```bash
/epci-spike 1h "Est-ce que GraphQL est viable pour notre API?"
/epci-spike 30min "Comment intégrer ce SDK externe?"
```

**Output :** Spike Report avec verdict :
- **GO** : Approche recommandée, effort estimé
- **NO-GO** : Raison, alternatives suggérées
- **MORE_RESEARCH** : Questions restantes

### `/epci:create` — Component Factory

```bash
/epci:create skill mon-nouveau-skill
/epci:create command ma-nouvelle-commande
/epci:create agent mon-nouvel-agent
```

Crée des composants EPCI avec validation automatique.

---

## Routing par Complexité

```
                    Brief Utilisateur
                           │
                           ▼
                    ┌─────────────┐
                    │ /epci-brief │
                    │ (Évaluation)│
                    └──────┬──────┘
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
        ▼                  ▼                  ▼
   ┌─────────┐       ┌──────────┐       ┌─────────┐
   │  TINY   │       │ STANDARD │       │  SPIKE  │
   │  SMALL  │       │  LARGE   │       │         │
   └────┬────┘       └────┬─────┘       └────┬────┘
        │                 │                  │
        ▼                 ▼                  ▼
  ┌───────────┐    ┌───────────┐      ┌───────────┐
  │/epci-quick│    │   /epci   │      │/epci-spike│
  └───────────┘    └───────────┘      └───────────┘
```

### Critères de Complexité

| Catégorie | Fichiers | LOC | Risque | Tests | Workflow |
|-----------|----------|-----|--------|-------|----------|
| **TINY** | 1 | < 50 | Aucun | Non | `/epci-quick` |
| **SMALL** | 2-3 | < 200 | Faible | Optionnels | `/epci-quick` |
| **STANDARD** | 4-10 | Variable | Modéré | Requis | `/epci` |
| **LARGE** | 10+ | Variable | Élevé | Complets | `/epci --large` |
| **SPIKE** | - | - | Incertain | - | `/epci-spike` |

---

## Subagents

### Agents Natifs Claude Code

| Agent | Modèle | Mode | Usage EPCI |
|-------|--------|------|------------|
| `@Explore` | Haiku | Read-only | Analyse codebase |
| `@Plan` | Sonnet | Research | Recherche avant plan |

### Agents Custom EPCI

| Agent | Mission | Invocation | Tools |
|-------|---------|------------|-------|
| `@plan-validator` | Valide le plan avant Phase 2 | Phase 1 | Read, Grep |
| `@code-reviewer` | Revue qualité et maintenabilité | Phase 2 | Read, Grep, Glob |
| `@security-auditor` | Audit OWASP Top 10 | Phase 2 (conditionnel) | Read, Grep |
| `@qa-reviewer` | Revue tests et couverture | Phase 2 (conditionnel) | Read, Grep, Bash |
| `@doc-generator` | Génération documentation | Phase 3 | Read, Write, Glob |

### Invocation Conditionnelle

**`@security-auditor`** activé si :
- Fichiers dans `**/auth/**`, `**/security/**`, `**/api/**`
- Mots-clés : password, secret, jwt, oauth, encrypt

**`@qa-reviewer`** activé si :
- Plus de 5 fichiers de test
- Tests d'intégration ou E2E
- Mocking complexe détecté

### Verdicts

| Verdict | Signification |
|---------|---------------|
| `APPROVED` | Aucun problème |
| `APPROVED_WITH_NOTES` | Issues mineures |
| `NEEDS_REVISION` | Corrections requises |
| `REJECTED` | Problèmes critiques |

---

## Skills

### Core Skills (5)

Skills fondamentaux chargés selon le contexte du workflow.

| Skill | Domaine | Chargé par |
|-------|---------|------------|
| `epci-core` | Concepts EPCI, Feature Document | Toutes commandes |
| `architecture-patterns` | SOLID, DDD, Clean Architecture | `/epci-brief`, Phase 1 |
| `code-conventions` | Naming, structure, DRY/KISS | Phase 2 |
| `testing-strategy` | TDD, coverage, mocking | Phase 2 |
| `git-workflow` | Conventional Commits, branching | Phase 3 |

### Stack Skills (4)

Skills auto-détectés selon le projet.

| Skill | Détection | Patterns |
|-------|-----------|----------|
| `php-symfony` | `composer.json` + symfony | Doctrine, Services, Messenger |
| `javascript-react` | `package.json` + react | Hooks, Components, State |
| `python-django` | `requirements.txt` + django | Models, DRF, Services |
| `java-springboot` | `pom.xml` + spring-boot | JPA, Controllers, Services |

### Factory Skills (4)

Skills pour la création de nouveaux composants.

| Skill | Rôle | Invoqué par |
|-------|------|-------------|
| `skills-creator` | Création de skills | `/epci:create skill` |
| `commands-creator` | Création de commandes | `/epci:create command` |
| `subagents-creator` | Création d'agents | `/epci:create agent` |
| `component-advisor` | Détection d'opportunités | Passif (auto) |

---

## Scripts de Validation

### Validation Individuelle

```bash
# Valider un skill
python scripts/validate_skill.py skills/core/epci-core/

# Valider une commande
python scripts/validate_command.py commands/epci-brief.md

# Valider un subagent
python scripts/validate_subagent.py agents/code-reviewer.md
```

### Validation Globale

```bash
# Valider tous les composants
python scripts/validate_all.py

# Mode verbose
python scripts/validate_all.py --verbose
```

### Test de Triggering

```bash
# Tester l'auto-activation d'un skill
python scripts/test_triggering.py skills/stack/python-django/

# Tester tous les skills
python scripts/test_triggering.py
```

### Critères de Validation

| Composant | Critères |
|-----------|----------|
| **Skill** | YAML valide, nom kebab-case ≤64 chars, description ≤1024 chars, < 5000 tokens |
| **Command** | YAML valide, description présente, allowed-tools valides |
| **Subagent** | YAML valide, nom kebab-case, tools restrictifs, < 2000 tokens |

---

## Architecture

### Structure des Dossiers

```
src/
├── .claude-plugin/
│   └── plugin.json              # Manifeste v3.0.0
│
├── commands/                    # 5 commandes
│   ├── epci-brief.md           # Point d'entrée
│   ├── epci.md                 # Workflow complet
│   ├── epci-quick.md           # Workflow condensé
│   ├── epci-spike.md           # Exploration
│   └── create.md               # Factory dispatcher
│
├── agents/                      # 5 subagents custom
│   ├── plan-validator.md
│   ├── code-reviewer.md
│   ├── security-auditor.md
│   ├── qa-reviewer.md
│   └── doc-generator.md
│
├── skills/                      # 13 skills
│   ├── core/                   # 5 skills fondamentaux
│   │   ├── epci-core/
│   │   ├── architecture-patterns/
│   │   ├── code-conventions/
│   │   ├── testing-strategy/
│   │   └── git-workflow/
│   │
│   ├── stack/                  # 4 skills auto-détectés
│   │   ├── php-symfony/
│   │   ├── javascript-react/
│   │   ├── python-django/
│   │   └── java-springboot/
│   │
│   └── factory/                # 4 skills de création
│       ├── skills-creator/
│       ├── commands-creator/
│       ├── subagents-creator/
│       └── component-advisor/
│
├── scripts/                     # Validation Python
│   ├── validate_skill.py
│   ├── validate_command.py
│   ├── validate_subagent.py
│   ├── validate_all.py
│   └── test_triggering.py
│
└── hooks/                       # Réservé pour hooks custom
```

### Conventions de Nommage

| Élément | Convention | Exemple |
|---------|------------|---------|
| Commandes | kebab-case, `.md` | `epci-brief.md` |
| Subagents | kebab-case, `.md` | `code-reviewer.md` |
| Skills | kebab-case (dossier) | `python-django/SKILL.md` |
| Scripts | snake_case, `.py` | `validate_skill.py` |
| Feature Docs | kebab-case | `add-user-auth.md` |

### Format des Fichiers

**Commandes et Subagents :**
```yaml
---
description: >-
  Description de l'action...
argument-hint: [args] [--flags]
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, Task
---

# Contenu Markdown
```

**Skills :**
```yaml
---
name: skill-name
description: >-
  Capacité. Use when: conditions.
  Not for: exclusions.
allowed-tools: Read, Grep
---

# Contenu Markdown
```

---

## Extension du Plugin

### Créer un Nouveau Skill

```bash
/epci:create skill mon-nouveau-skill
```

Le skill `skills-creator` guide la création en 6 phases :
1. **Qualification** — Définir le domaine et les triggers
2. **Definition** — Écrire le frontmatter YAML
3. **Content** — Structurer le contenu
4. **References** — Ajouter des fichiers annexes (optionnel)
5. **Validation** — Vérifier avec le script
6. **Triggering** — Tester l'auto-activation

### Créer une Nouvelle Commande

```bash
/epci:create command ma-nouvelle-commande
```

### Créer un Nouvel Agent

```bash
/epci:create agent mon-nouvel-agent
```

**Principe clé : Least Privilege**
- Donner uniquement les tools nécessaires
- Préférer Read-only (Read, Grep, Glob)
- Éviter Write/Edit/Bash sauf si indispensable

---

## Changelog v2.7 → v3.0

### Simplification

| Aspect | v2.7 | v3.0 |
|--------|------|------|
| Commandes | 12 fichiers | 5 fichiers |
| Point d'entrée | Multiple | Unique (`/epci-brief`) |
| Routing | 5 niveaux + pré-stages | 3 workflows |

### Nouveautés v3.0

- **5 Subagents Custom** : plan-validator, code-reviewer, security-auditor, qa-reviewer, doc-generator
- **13 Skills Modulaires** : Core, Stack, Factory
- **Component Factory** : `/epci:create` pour auto-extension
- **Feature Document** : Traçabilité complète par feature
- **Validation Automatique** : Scripts Python pour chaque composant

### Migration depuis v2.7

| Commande v2.7 | Équivalent v3.0 |
|---------------|-----------------|
| `/epci-discover` | `/epci-brief` |
| `/epci-0-briefing` | `/epci-brief` |
| `/epci-micro` | `/epci-quick` (TINY) |
| `/epci-soft` | `/epci-quick` (SMALL) |
| `/epci-1-analyse` | `/epci` Phase 1 |
| `/epci-2-code` | `/epci` Phase 2 |
| `/epci-3-finalize` | `/epci` Phase 3 |
| `/epci-hotfix` | `/epci-quick` + urgence |

---

## Ressources

- **CLAUDE.md** — Documentation développeur complète (racine du projet)
- **docs/features/** — Feature Documents générés
- **docs/spikes/** — Spike Reports

---

## Licence

MIT - EPCI Team
