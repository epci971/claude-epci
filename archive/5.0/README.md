# EPCI Plugin v5.0.0

> **E**xplore → **P**lan → **C**ode → **I**nspect

Workflow structuré pour le développement assisté par IA avec traçabilité complète, mémoire projet persistante, apprentissage continu et orchestration batch.

---

## Table des matières

- [Quick Start](#quick-start)
- [Workflow EPCI](#workflow-epci)
- [Commandes](#commandes)
- [Routing par Complexité](#routing-par-complexité)
- [Orchestration Batch](#orchestration-batch)
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
/brief "Ajouter une fonctionnalité d'authentification OAuth2"

# 2. Le plugin évalue la complexité et recommande un workflow
# 3. Suivez le workflow recommandé
```

### Workflow Typique

```
Utilisateur: /brief "Ajouter un endpoint API pour les utilisateurs"

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

├── §1 Brief Fonctionnel      ← /brief
├── §2 Plan d'Implémentation  ← /epci Phase 1
├── §3 Rapport d'Implémentation ← /epci Phase 2
└── §4 Finalisation           ← /epci Phase 3
```

---

## Commandes

### Vue d'ensemble (12 commandes)

| Commande | Description | Quand l'utiliser |
|----------|-------------|------------------|
| `/brief` | Point d'entrée universel | Toujours commencer ici |
| `/epci` | Workflow complet 3 phases | Features STANDARD et LARGE |
| `/quick` | Workflow condensé | Features TINY et SMALL |
| `/brainstorm` | Feature discovery v4.9 | Idée vague, incertitude |
| `/decompose` | Décomposition PRD/briefs | Gros projets > 5 jours |
| `/orchestrate` | Exécution batch specs | Overnight automation |
| `/debug` | Diagnostic structuré | Bug fixing |
| `/commit` | Finalisation git EPCI | Après /epci ou /quick |
| `/memory` | Gestion mémoire + learning | Init, export, calibrate |
| `/rules` | Génération .claude/rules/ | Conventions projet |
| `/promptor` | Voice-to-brief + Notion | Dictée vocale |
| `/create` | Factory de composants | Créer skills/commands/agents |

### `/brief` — Point d'entrée

```bash
/brief "Description de votre besoin"
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

### `/quick` — Workflow Condensé

```bash
/quick
```

| Mode | Fichiers | LOC | Tests | Durée |
|------|----------|-----|-------|-------|
| **TINY** | 1 | < 50 | Non requis | < 15 min |
| **SMALL** | 2-3 | < 200 | Optionnels | 15-60 min |

**Exemples TINY :** Typos, fixes de config, petits ajustements
**Exemples SMALL :** Petites features, refactoring local

### `/brainstorm` — Feature Discovery & Exploration

```bash
/brainstorm "Nouvelle feature d'export CSV"
/brainstorm spike 1h "Est-ce que GraphQL est viable pour notre API?"
```

**Output :** Brief structuré ou Spike Report avec verdict (GO/NO-GO/MORE_RESEARCH).

### `/epci:create` — Component Factory

```bash
/epci:create skill mon-nouveau-skill
/epci:create command ma-nouvelle-commande
/epci:create agent mon-nouvel-agent
```

Crée des composants EPCI avec validation automatique.

### `/decompose` — Décomposition PRD/Briefs

```bash
/decompose mon-prd.md --output specs/
/decompose brief.md --min-days 2 --max-days 5
```

Décompose un PRD ou brief brainstorm en sous-specs exécutables :
- **Auto-détection format** : PRD (Phases/Steps) ou Brief (User Stories)
- Génération INDEX.md compatible `/orchestrate`
- Validation via `@decompose-validator`
- Export au format markdown structuré

**Chaîne complète** : `/brainstorm` → `/decompose` → `/orchestrate`

### `/orchestrate` — Exécution Batch

```bash
/orchestrate ./docs/specs/my-project/           # Exécution standard
/orchestrate ./specs/ --dry-run                 # Voir le plan sans exécuter
/orchestrate ./specs/ --continue                # Reprendre après interruption
/orchestrate ./specs/ --skip S03,S05            # Ignorer certaines specs
```

Orchestre l'exécution automatique de multiples specs :
- **DAG-based** : Gestion des dépendances entre specs
- **Priority sorting** : Effort croissant + priority override (1-99)
- **Auto-retry** : Jusqu'à 3 tentatives par spec
- **Dual journaling** : MD (humain) + JSON (outils)
- **Timeout proportionnel** : TINY=15m, SMALL=30m, STD=1h, LARGE=2h

**Use case** : Lancer avant la nuit, revenir le matin avec toutes les features implémentées.

### `/memory` — Gestion Mémoire Projet

```bash
/memory init           # Initialiser la mémoire projet
/memory status         # Voir l'état actuel
/memory export         # Exporter la configuration
/memory reset          # Réinitialiser
/memory learn status   # État de l'apprentissage
/memory learn calibrate # Calibrer les estimations
```

Gère la mémoire persistante du projet (conventions, préférences, historique) et le système d'apprentissage.

---

## Routing par Complexité

```
                    Brief Utilisateur
                           │
                           ▼
                    ┌─────────────┐
                    │ /brief │
                    │ (Évaluation)│
                    └──────┬──────┘
                           │
        ┌──────────────────┴──────────────────┐
        │                                     │
        ▼                                     ▼
   ┌─────────┐                          ┌──────────┐
   │  TINY   │                          │ STANDARD │
   │  SMALL  │                          │  LARGE   │
   └────┬────┘                          └────┬─────┘
        │                                    │
        ▼                                    ▼
  ┌───────────┐                       ┌───────────┐
  │  /quick   │                       │   /epci   │
  └───────────┘                       └───────────┘
```

### Critères de Complexité

| Catégorie | Fichiers | LOC | Risque | Tests | Workflow |
|-----------|----------|-----|--------|-------|----------|
| **TINY** | 1 | < 50 | Aucun | Non | `/quick` |
| **SMALL** | 2-3 | < 200 | Faible | Optionnels | `/quick` |
| **STANDARD** | 4-10 | Variable | Modéré | Requis | `/epci` |
| **LARGE** | 10+ | Variable | Élevé | Complets | `/epci --large` |

---

## Orchestration Batch

Pour les gros projets avec multiples specs, la chaîne complète est :

```
┌─────────────────────────────────────────────────────────────────┐
│            CHAÎNE COMPLÈTE POUR GROS PROJETS                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   ┌─────────────┐    ┌─────────────┐    ┌─────────────┐         │
│   │ /brainstorm │ →  │ /decompose  │ →  │ /orchestrate│         │
│   └─────────────┘    └─────────────┘    └─────────────┘         │
│         │                  │                  │                  │
│         ▼                  ▼                  ▼                  │
│   Brief EMS 85+      INDEX.md +         Exécution auto          │
│   (User Stories)     S01...SNN.md       (overnight)             │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Formats Compatibles

| Source | Format | Cible |
|--------|--------|-------|
| `/brainstorm` | Brief avec User Stories | `/decompose` |
| `/decompose` | INDEX.md + specs | `/orchestrate` |
| PRD manuel | Phases/Steps | `/decompose` |

### INDEX.md Format (decompose → orchestrate)

```markdown
| ID | Title | Effort | Priority | Dependencies | Status |
|----|-------|--------|----------|--------------|--------|
| S01 | Core logic | 2j | - | - | Pending |
| S02 | UI components | 1j | 1 | - | Pending |
| S03 | Integration | 3j | - | S01, S02 | Pending |
```

---

## Subagents

### Agents Natifs Claude Code

| Agent | Modèle | Mode | Usage EPCI |
|-------|--------|------|------------|
| `@Explore` | Haiku | Read-only | Analyse codebase |
| `@Plan` | Sonnet | Research | Recherche avant plan |

### Agents Custom EPCI (15)

#### Core Agents (7)

| Agent | Model | Mission | Invoqué par |
|-------|-------|---------|-------------|
| `@plan-validator` | opus | Valide le plan avant Phase 2 | `/epci` Phase 1 |
| `@code-reviewer` | opus | Revue qualité et maintenabilité | `/epci` Phase 2, `/debug` |
| `@security-auditor` | opus | Audit OWASP Top 10 | `/epci` Phase 2 (conditionnel) |
| `@qa-reviewer` | sonnet | Revue tests et couverture | `/epci` Phase 2 (conditionnel) |
| `@doc-generator` | sonnet | Génération documentation | `/epci` Phase 3 |
| `@decompose-validator` | opus | Valide la décomposition | `/decompose` |
| `@rules-validator` | opus | Valide .claude/rules/ | `/rules` |

#### Turbo/Quick Agents (3)

| Agent | Model | Mission | Invoqué par |
|-------|-------|---------|-------------|
| `@clarifier` | haiku | Questions clarification rapides | `/brief --turbo`, `/brainstorm --turbo` |
| `@planner` | sonnet | Planification rapide | `/epci --turbo`, `/quick`, `/brainstorm` |
| `@implementer` | sonnet | Implémentation TDD rapide | `/epci --turbo`, `/quick` |

#### Brainstorm Agents (5)

| Agent | Model | Mission | Invoqué par |
|-------|-------|---------|-------------|
| `@ems-evaluator` | haiku | Calcul EMS 5 axes | `/brainstorm` (chaque itération) |
| `@technique-advisor` | haiku | Auto-sélection techniques | `/brainstorm` (si axe < 50) |
| `@party-orchestrator` | sonnet | Orchestration multi-persona | `/brainstorm` (commande `party`) |
| `@expert-panel` | sonnet | Panel 5 experts dev | `/brainstorm` (commande `panel`) |
| `@rule-clarifier` | haiku | Clarification règles métier | `/brainstorm` |

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

### Core Skills (16)

Skills fondamentaux chargés selon le contexte du workflow.

| Skill | Domaine | Chargé par |
|-------|---------|------------|
| `epci-core` | Concepts EPCI, Feature Document, Breakpoints | Toutes commandes |
| `architecture-patterns` | SOLID, DDD, Clean Architecture | `/brief`, Phase 1 |
| `code-conventions` | Naming, structure, DRY/KISS | Phase 2 |
| `testing-strategy` | TDD, coverage, mocking | Phase 2 |
| `git-workflow` | Conventional Commits, branching | Phase 3 |
| `breakpoint-metrics` | Scoring complexité, estimation temps | Breakpoints enrichis |
| `flags-system` | Flags universels, auto-activation | Toutes commandes |
| `project-memory` | Contexte et chargement mémoire projet | `/memory`, workflows |
| `learning-optimizer` | Optimisation apprentissage | `/memory learn` |
| `proactive-suggestions` | Suggestions proactives IA | Phase 2, breakpoints |
| `clarification-intelligente` | Clarification intelligente | `/brief` |
| `brainstormer` | Feature discovery v4.9 | `/brainstorm` |
| `debugging-strategy` | Diagnostic structuré | `/debug` |
| `rules-generator` | Génération .claude/rules/ | `/rules` |
| `input-clarifier` | Clarification inputs utilisateur | `/brainstorm` |
| `orchestrator-batch` | Orchestration batch specs | `/orchestrate` |

### Stack Skills (5)

Skills auto-détectés selon le projet.

| Skill | Détection | Patterns |
|-------|-----------|----------|
| `php-symfony` | `composer.json` + symfony | Doctrine, Services, Messenger |
| `javascript-react` | `package.json` + react | Hooks, Components, State |
| `python-django` | `requirements.txt` + django | Models, DRF, Services |
| `java-springboot` | `pom.xml` + spring-boot | JPA, Controllers, Services |
| `frontend-editor` | Fichiers frontend (CSS, UI) | Tailwind, SCSS, Responsive |

### Factory Skills (4)

Skills pour la création de nouveaux composants.

| Skill | Rôle | Invoqué par |
|-------|------|-------------|
| `skills-creator` | Création de skills | `/create skill` |
| `commands-creator` | Création de commandes | `/create command` |
| `subagents-creator` | Création d'agents | `/create agent` |
| `component-advisor` | Détection d'opportunités | Passif (auto) |

### Autres Skills (3)

| Skill | Rôle | Invoqué par |
|-------|------|-------------|
| `mcp` | Intégration MCP servers | Auto (Context7, Magic, etc.) |
| `personas` | Système personas adaptatifs | `/brainstorm`, auto |
| `promptor` | Voice-to-brief + Notion | `/promptor` |

---

## Scripts de Validation

### Validation Individuelle

```bash
# Valider un skill
python scripts/validate_skill.py skills/core/epci-core/

# Valider une commande
python scripts/validate_command.py commands/brief.md

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
/memory init      # Créer .project-memory/ dans le projet
/memory status    # Afficher l'état de la mémoire
/memory export    # Exporter en JSON
/memory reset     # Réinitialiser
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
│   └── plugin.json              # Manifeste v5.0.0
│
├── commands/                    # 12 commandes
│   ├── brief.md                 # Point d'entrée + routing
│   ├── epci.md                  # Workflow complet 3 phases
│   ├── quick.md                 # Workflow condensé TINY/SMALL
│   ├── brainstorm.md            # Feature discovery v4.9
│   ├── decompose.md             # Décomposition PRD/briefs
│   ├── orchestrate.md           # Orchestration batch specs
│   ├── debug.md                 # Diagnostic structuré
│   ├── commit.md                # Finalisation git EPCI
│   ├── memory.md                # Gestion mémoire + learning
│   ├── rules.md                 # Génération .claude/rules/
│   ├── promptor.md              # Voice-to-brief + Notion
│   └── create.md                # Factory dispatcher
│
├── agents/                      # 15 subagents custom
│   ├── plan-validator.md        # Core
│   ├── code-reviewer.md
│   ├── security-auditor.md
│   ├── qa-reviewer.md
│   ├── doc-generator.md
│   ├── decompose-validator.md
│   ├── rules-validator.md
│   ├── clarifier.md             # Turbo
│   ├── planner.md
│   ├── implementer.md
│   ├── ems-evaluator.md         # Brainstorm
│   ├── technique-advisor.md
│   ├── party-orchestrator.md
│   ├── expert-panel.md
│   └── rule-clarifier.md
│
├── skills/                      # 28 skills
│   ├── core/                    # 16 skills fondamentaux
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
│   │   ├── clarification-intelligente/
│   │   ├── brainstormer/
│   │   ├── debugging-strategy/
│   │   ├── rules-generator/
│   │   ├── input-clarifier/
│   │   └── orchestrator-batch/
│   │
│   ├── stack/                   # 5 skills auto-détectés
│   │   ├── php-symfony/
│   │   ├── javascript-react/
│   │   ├── python-django/
│   │   ├── java-springboot/
│   │   └── frontend-editor/
│   │
│   ├── factory/                 # 4 skills de création
│   │   ├── skills-creator/
│   │   ├── commands-creator/
│   │   ├── subagents-creator/
│   │   └── component-advisor/
│   │
│   ├── mcp/                     # MCP integration
│   ├── personas/                # Système personas
│   └── promptor/                # Voice-to-brief
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
| Commandes | kebab-case, `.md` | `brief.md` |
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

### v5.0.0 (Janvier 2026) — Current

**Nouvelle commande majeure :**
- `/orchestrate` — Orchestration batch de specs avec DAG, priority sorting, auto-retry, dual journaling

**Compatibilité chaîne complète :**
- `/brainstorm` → `/decompose` → `/orchestrate`
- `/decompose` accepte maintenant les briefs brainstorm (User Stories)
- INDEX.md format unifié compatible `/orchestrate`

**Nouveau skill :**
- `orchestrator-batch` — Logique d'orchestration batch (6 références)

**Améliorations `/decompose` :**
- Auto-détection format PRD vs Brief brainstorm
- Mapping User Stories → Specs (Complexité S/M/L → jours)
- INDEX.md avec colonnes Priority et Status
- Nouveau edge case EC6 pour briefs

**Totaux v5.0.0 :**
- 12 commandes
- 15 subagents
- 28 skills

---

### v4.9 (Janvier 2026)

**Brainstorm v4.9 :**
- Finalization Checkpoint obligatoire à EMS >= 85
- 3 nouveaux agents : `@expert-panel`, `@party-orchestrator`, `@rule-clarifier`
- Nouveau skill : `input-clarifier`

### v4.8 (Janvier 2026)

**Brainstorm v4.8 :**
- Auto-sélection techniques basée sur axes EMS faibles
- Mix de techniques si 2+ axes faibles
- Preview @planner/@security en phase Convergent

### v4.4

- Fusion `/learn` → `/memory` (subcommand `learn`)
- Ajout `/commit` pour finalisation git EPCI
- 3 nouveaux agents turbo : `@clarifier`, `@planner`, `@implementer`

### v3.8 (Décembre 2024)

**Nouvelles commandes :**
- `/decompose` — Décomposition de features en tâches
- `/memory` — Gestion mémoire projet

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
| Point d'entrée | Multiple | Unique (`/brief`) |
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
| `/epci-discover` | `/brief` |
| `/epci-0-briefing` | `/brief` |
| `/epci-micro` | `/quick` (TINY) |
| `/epci-soft` | `/quick` (SMALL) |
| `/epci-1-analyse` | `/epci` Phase 1 |
| `/epci-2-code` | `/epci` Phase 2 |
| `/epci-3-finalize` | `/epci` Phase 3 |
| `/epci-hotfix` | `/quick` + urgence |

---

## Ressources

- **CLAUDE.md** — Documentation développeur complète (racine du projet)
- **docs/features/** — Feature Documents générés
- **docs/spikes/** — Spike Reports

---

## Licence

MIT - EPCI Team
