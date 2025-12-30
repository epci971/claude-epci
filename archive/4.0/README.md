# EPCI Plugin v3.9.5

> **E**xplore → **P**lan → **C**ode → **I**nspect

Workflow structuré pour le développement assisté par IA avec traçabilité complète, mémoire projet persistante et apprentissage continu.

---

## Table des matières

- [Quick Start](#quick-start)
- [Workflow EPCI](#workflow-epci)
- [Commandes](#commandes)
- [Routing par Complexité](#routing-par-complexité)
- [Subagents](#subagents)
- [Skills](#skills)
- [Project Memory](#project-memory)
- [Système de Hooks](#système-de-hooks)
- [Système de Flags](#système-de-flags)
- [Scripts de Validation](#scripts-de-validation)
- [Architecture](#architecture)
- [Extension du Plugin](#extension-du-plugin)
- [Changelog](#changelog)

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
| `/epci-decompose` | Décomposition de features | Planification tâches complexes |
| `/epci-memory` | Gestion mémoire projet | Initialiser, exporter, réinitialiser |
| `/epci-learn` | Apprentissage projet | Analyser patterns et calibrer |
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
- **BREAKPOINT ENRICHI** : Tableau de bord décisionnel avec métriques, verdicts agents, preview Phase 2

**Phase 2 — Implémentation TDD**
- Thinking : `think`
- Skills : `testing-strategy`, `code-conventions`, stack auto-détecté
- Agents : `@code-reviewer` (toujours), `@security-auditor` (conditionnel), `@qa-reviewer` (conditionnel)
- Output : §3 Rapport d'Implémentation
- **BREAKPOINT ENRICHI** : Tableau de bord décisionnel avec métriques, verdicts agents, preview Phase 3

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

### `/epci-decompose` — Décomposition de Features

```bash
/epci-decompose feature.md --output tasks/ --think hard
/epci-decompose --min-days 2 --max-days 5
```

Décompose une feature complexe en tâches atomiques :
- Analyse du Feature Document ou brief
- Génération de tâches avec estimations
- Validation via `@decompose-validator`
- Export au format markdown structuré

### `/epci-memory` — Gestion Mémoire Projet

```bash
/epci-memory init       # Initialiser la mémoire projet
/epci-memory status     # Voir l'état actuel
/epci-memory export     # Exporter la configuration
/epci-memory reset      # Réinitialiser
```

Gère la mémoire persistante du projet (conventions, préférences, historique).

### `/epci-learn` — Apprentissage Projet

```bash
/epci-learn status      # État de l'apprentissage
/epci-learn calibrate   # Calibrer les estimations
/epci-learn export      # Exporter les patterns appris
/epci-learn reset       # Réinitialiser l'apprentissage
```

Analyse les patterns du projet et optimise les suggestions futures.

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

### Agents Custom EPCI (6)

| Agent | Mission | Invocation | Tools |
|-------|---------|------------|-------|
| `@plan-validator` | Valide le plan avant Phase 2 | Phase 1 | Read, Grep |
| `@code-reviewer` | Revue qualité et maintenabilité | Phase 2 | Read, Grep, Glob |
| `@security-auditor` | Audit OWASP Top 10 | Phase 2 (conditionnel) | Read, Grep |
| `@qa-reviewer` | Revue tests et couverture | Phase 2 (conditionnel) | Read, Grep, Bash |
| `@doc-generator` | Génération documentation | Phase 3 | Read, Write, Glob |
| `@decompose-validator` | Valide la décomposition des tâches | `/epci-decompose` | Read, Grep |

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

### Breakpoints Enrichis

À partir de la v3.1, les breakpoints du workflow `/epci` affichent un tableau de bord décisionnel complet :

```
┌─────────────────────────────────────────────────────────────────┐
│                    🔄 EPCI BREAKPOINT — PHASE 1→2               │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  📊 MÉTRIQUES                                                    │
│  ├─ Complexité    : 6.2/10 (STANDARD)                          │
│  ├─ Fichiers      : 7 impactés, 3 nouveaux                     │
│  ├─ Temps estimé  : ~3h 15min                                   │
│  └─ Risque        : MOYEN (auth + API externe)                  │
│                                                                  │
│  ✅ AGENTS VERDICTS                                             │
│  ├─ @plan-validator    : APPROVED                               │
│  └─ @Plan              : APPROVED_WITH_NOTES                    │
│                                                                  │
│  🎯 PREVIEW PHASE 2 (Implémentation TDD)                       │
│  ├─ 1. Créer User entity avec validation                       │
│  ├─ 2. Tests unitaires UserService                             │
│  ├─ 3. Endpoint POST /api/users                                │
│  ├─ 4. Tests intégration API                                   │
│  └─ 5. Validation sécurité JWT...                              │
│                                                                  │
│  🤔 OPTIONS                                                     │
│  ├─ [C] Continuer la Phase 2                                   │
│  ├─ [R] Réviser le plan (retour Phase 1)                       │
│  ├─ [P] Pause (sauvegarder l'état)                             │
│  └─ [A] Abandon (nettoyer et sortir)                           │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘

Votre choix ? [C/R/P/A] :
```

**Composants des Breakpoints Enrichis :**

| Élément | Description |
|---------|-------------|
| **Métriques** | Scoring complexité, estimation temps, analyse risque |
| **Verdicts Agents** | Status des subagents avec codes couleur |
| **Preview** | Aperçu des 3-5 premières tâches de la phase suivante |
| **Options** | Choix interactifs documentés |

**Skills associés :**
- `breakpoint-metrics` : Calcul scoring et estimation temps
- `epci-core` : Format et documentation des breakpoints

---

## Skills

### Core Skills (12)

Skills fondamentaux chargés selon le contexte du workflow.

| Skill | Domaine | Chargé par |
|-------|---------|------------|
| `epci-core` | Concepts EPCI, Feature Document, Breakpoints | Toutes commandes |
| `architecture-patterns` | SOLID, DDD, Clean Architecture | `/epci-brief`, Phase 1 |
| `code-conventions` | Naming, structure, DRY/KISS | Phase 2 |
| `testing-strategy` | TDD, coverage, mocking | Phase 2 |
| `git-workflow` | Conventional Commits, branching | Phase 3 |
| `breakpoint-metrics` | Scoring complexité, estimation temps | Breakpoints enrichis |
| `flags-system` | Flags universels, auto-activation | Toutes commandes |
| `project-memory` | Contexte et chargement mémoire projet | `/epci-memory`, workflows |
| `learning-optimizer` | Optimisation apprentissage | `/epci-learn` |
| `proactive-suggestions` | Suggestions proactives IA | Phase 2, breakpoints |
| `clarification-intelligente` | Clarification intelligente | `/epci-brief` |

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

## Project Memory

Le système de mémoire projet permet de persister le contexte entre les sessions.

### Composants

```
project-memory/
├── manager.py              # Gestion centrale de la mémoire
├── detector.py             # Détection de patterns
├── learning_analyzer.py    # Analyse d'apprentissage
├── calibration.py          # Calibration des estimations
├── suggestion_engine.py    # Génération de suggestions
├── clarification_analyzer.py  # Analyse des clarifications
├── question_generator.py   # Génération de questions
├── similarity_matcher.py   # Matching de patterns
├── schemas/                # Schémas JSON (8 fichiers)
├── templates/              # Templates par défaut (4 fichiers)
├── patterns/               # Catalogue de patterns
└── tests/                  # Tests unitaires (8 fichiers)
```

### Données Persistées

| Type | Description | Fichier |
|------|-------------|---------|
| **Contexte** | Stack, architecture, conventions | `context.json` |
| **Conventions** | Règles de nommage, patterns | `conventions.json` |
| **Préférences** | Choix utilisateur récurrents | `preferences.json` |
| **Corrections** | Corrections appliquées | `corrections.json` |
| **Vélocité** | Métriques de productivité | `velocity.json` |
| **Historique** | Features développées | `feature-history.json` |

### Commandes

```bash
/epci-memory init      # Créer .epci-memory/ dans le projet
/epci-memory status    # Afficher l'état de la mémoire
/epci-memory export    # Exporter en JSON
/epci-memory reset     # Réinitialiser
```

---

## Système de Hooks

Les hooks permettent d'exécuter des scripts personnalisés à des points clés du workflow.

### Points de Hook

| Hook | Déclencheur | Usage |
|------|-------------|-------|
| `pre-phase-1` | Avant Phase 1 | Charger contexte, vérifier prérequis |
| `post-phase-1` | Après validation plan | Notifier équipe, créer tickets |
| `pre-phase-2` | Avant Phase 2 | Linters, setup environnement |
| `post-phase-2` | Après code review | Tests additionnels, coverage |
| `pre-phase-3` | Avant Phase 3 | Vérifier tests passent |
| `post-phase-3` | Après finalisation | Déployer, notifier |
| `on-breakpoint` | À chaque breakpoint | Logging, métriques |

### Structure

```
hooks/
├── README.md           # Documentation
├── runner.py           # Moteur d'exécution
├── examples/           # Exemples de hooks (6)
│   ├── pre-phase-2-lint.sh
│   ├── post-phase-3-notify.py
│   ├── post-phase-3-memory-update.py
│   ├── on-breakpoint-memory-context.py
│   ├── on-breakpoint-log.sh
│   └── post-phase-2-suggestions.py
└── active/             # Hooks actifs (symlinks)
```

### Création d'un Hook

```python
#!/usr/bin/env python3
import sys, json

# Recevoir le contexte
context = json.loads(sys.stdin.read())

# Traitement
result = {"status": "success", "message": "Hook exécuté"}

# Retourner le résultat
print(json.dumps(result))
```

---

## Système de Flags

Les flags universels contrôlent le comportement des workflows EPCI.

### Catégories

| Catégorie | Flags | Description |
|-----------|-------|-------------|
| **Thinking** | `--think`, `--think-hard`, `--ultrathink` | Profondeur d'analyse |
| **Compression** | `--uc`, `--verbose` | Gestion des tokens |
| **Workflow** | `--safe`, `--no-hooks` | Contrôle exécution |
| **Wave** | `--wave`, `--wave-strategy` | Orchestration multi-vagues |
| **Legacy** | `--large`, `--continue` | Rétrocompatibilité |

### Auto-Activation

Les flags peuvent être activés automatiquement selon le contexte :

| Condition | Seuil | Flag activé |
|-----------|-------|-------------|
| Fichiers impactés | 3-10 | `--think` |
| Fichiers impactés | >10 | `--think-hard` |
| Context window | >75% | `--uc` |
| Fichiers sensibles | auth, security, payment | `--safe` |
| Complexité | >0.7 | `--wave` |

### Précédence

1. Flags explicites > Auto-activation
2. `--ultrathink` > `--think-hard` > `--think`

---

## Architecture

### Structure des Dossiers

```
src/
├── .claude-plugin/
│   └── plugin.json              # Manifeste v3.8.3
│
├── commands/                    # 8 commandes
│   ├── epci-brief.md           # Point d'entrée + routing
│   ├── epci.md                 # Workflow complet 3 phases
│   ├── epci-quick.md           # Workflow condensé TINY/SMALL
│   ├── epci-spike.md           # Exploration time-boxée
│   ├── epci-decompose.md       # Décomposition de features
│   ├── epci-memory.md          # Gestion mémoire projet
│   ├── epci-learn.md           # Apprentissage projet
│   └── create.md               # Factory dispatcher
│
├── agents/                      # 6 subagents custom
│   ├── plan-validator.md
│   ├── code-reviewer.md
│   ├── security-auditor.md
│   ├── qa-reviewer.md
│   ├── doc-generator.md
│   └── decompose-validator.md  # Validation décomposition
│
├── skills/                      # 20 skills
│   ├── core/                   # 12 skills fondamentaux
│   │   ├── epci-core/
│   │   ├── architecture-patterns/
│   │   ├── code-conventions/
│   │   ├── testing-strategy/
│   │   ├── git-workflow/
│   │   ├── breakpoint-metrics/
│   │   ├── flags-system/
│   │   ├── project-memory/
│   │   ├── learning-optimizer/
│   │   ├── proactive-suggestions/
│   │   └── clarification-intelligente/
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
├── scripts/                     # 7 scripts de validation
│   ├── validate_all.py         # Orchestrateur
│   ├── validate_skill.py
│   ├── validate_command.py
│   ├── validate_subagent.py
│   ├── validate_flags.py       # Validation système flags
│   ├── validate_memory.py      # Validation mémoire
│   └── test_triggering.py
│
├── settings/                    # Configuration
│   └── flags.md                # Documentation flags universels
│
├── hooks/                       # Système de hooks
│   ├── README.md               # Documentation
│   ├── runner.py               # Moteur d'exécution
│   ├── examples/               # Exemples (6 hooks)
│   └── active/                 # Hooks actifs (symlinks)
│
└── project-memory/              # Backend mémoire projet
    ├── manager.py              # Gestion centrale
    ├── detector.py             # Détection patterns
    ├── learning_analyzer.py    # Analyse apprentissage
    ├── calibration.py          # Calibration estimations
    ├── suggestion_engine.py    # Suggestions
    ├── clarification_analyzer.py
    ├── question_generator.py
    ├── similarity_matcher.py
    ├── schemas/                # 8 schémas JSON
    ├── templates/              # 4 templates
    ├── patterns/               # Catalogue patterns
    └── tests/                  # 8 tests unitaires
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

## Changelog

### v3.8 (Décembre 2024) — Current

**Nouvelles commandes :**
- `/epci-decompose` — Décomposition de features en tâches
- `/epci-memory` — Gestion mémoire projet
- `/epci-learn` — Apprentissage et calibration

**Nouvel agent :**
- `@decompose-validator` — Validation des décompositions

**Nouveaux skills core :**
- `learning-optimizer` — Optimisation apprentissage
- `proactive-suggestions` — Suggestions proactives IA
- `clarification-intelligente` — Clarification intelligente

**Améliorations :**
- Intégration project-memory dans tous les workflows
- Breakpoints enrichis avec métriques
- Instructions de séquence et étapes obligatoires

### v3.7 — Hooks & Memory Backend

**Système de hooks :**
- Moteur d'exécution (`runner.py`)
- 7 points de hook (pre/post phases, on-breakpoint)
- 6 exemples de hooks

**Project Memory backend :**
- 11 modules Python
- 8 schémas JSON
- 8 tests unitaires

### v3.6 — Project Memory

**Nouveau système :**
- Mémoire projet persistante
- Skills `project-memory` et `flags-system`
- Détection de patterns
- Calibration des estimations

### v3.1 — Flags universels

**Système de flags :**
- Catégories : Thinking, Compression, Workflow, Wave
- Auto-activation selon contexte
- Règles de précédence

**Breakpoints enrichis :**
- Tableau de bord décisionnel
- Métriques et verdicts agents
- Preview phase suivante

### v3.0 — Refonte majeure

**Simplification :**

| Aspect | v2.7 | v3.0 |
|--------|------|------|
| Commandes | 12 fichiers | 5 fichiers |
| Point d'entrée | Multiple | Unique (`/epci-brief`) |
| Routing | 5 niveaux | 3 workflows |

**Nouveautés :**
- 5 Subagents Custom
- 13 Skills Modulaires
- Component Factory
- Feature Document
- Validation Automatique

### Migration depuis v2.7

| Commande v2.7 | Équivalent actuel |
|---------------|-------------------|
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
