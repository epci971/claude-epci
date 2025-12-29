# EPCI Plugin — Claude Code Development Assistant

> **Version** : 3.2.0
> **Date** : Décembre 2024
> **Audience** : Développeurs du plugin EPCI

---

## 1. Project Overview

### 1.1 Qu'est-ce qu'EPCI ?

EPCI (Explore → Plan → Code → Inspect) est un plugin Claude Code qui structure le développement logiciel en phases distinctes avec validation à chaque étape.

### 1.2 Philosophie v3

| Principe | Description |
|----------|-------------|
| **Simplicité** | 5 commandes principales (vs 12 en v2.7) |
| **Modularité** | Exploitation des primitives natives Claude Code (Skills, Subagents) |
| **Traçabilité** | Feature Document comme fil rouge de chaque développement |
| **Extensibilité** | Component Factory pour créer de nouveaux composants |

### 1.3 Évolution depuis v2.7

| Aspect | v2.7 | v3.0 | v3.2 |
|--------|------|------|------|
| Commandes | 12 fichiers | 5 fichiers | 5 fichiers |
| Point d'entrée | Multiple (micro, soft, 0-briefing...) | Unique (`epci-brief`) | Unique (`epci-brief`) |
| Subagents custom | 0 | 5 | 5 |
| Skills | 0 | 19 | 20+ |
| Personas | Custom | Déprécié | **F09 Auto-activation** |
| Routing | 5 niveaux (TINY→LARGE + pré-stages) | 3 workflows (quick, full, spike) | 3 workflows + personas |
| Auto-extension | Non | Component Factory | Component Factory |

### 1.4 Nouveautés v3.2 (F09)

- **Système de Personas** : 6 modes de pensée globaux avec auto-activation
- **Scoring algorithmique** : Détection automatique based on keywords + files + stack
- **Integration `/epci-brief`** : Step 5 - Persona Detection dans le workflow
- **6 Personas** : Architect, Frontend, Backend, Security, QA, Doc
- **Flags `--persona-X`** : Activation manuelle possible
- **Breakpoint display** : Personas actifs/suggérés dans FLAGS line

---

## 2. Repository Structure

```
tools-claude-code-epci/
├── CLAUDE.md                    # Ce fichier - doc développeur
│
├── archive/                     # Versions dépréciées
│   └── v2.7/                   # Archivage build/commands/
│
├── build/                       # Production v2.7 (référence)
│   └── commands/               # 12 commandes v2.7
│       ├── epci-workflow-guide-v2.7.md
│       ├── epci-0-briefing-v2.7.md
│       ├── epci-1-analyse-v2.7.md
│       ├── epci-2-code-v2.7.md
│       ├── epci-3-finalize-v2_7.md
│       ├── epci-micro-v2.7.md
│       ├── epci-soft-v2.7.md
│       ├── epci-spike-v2.7.md
│       ├── epci-hotfix-v2.7.md
│       ├── epci-discover-v2.7.md
│       ├── epci-flags-v2.7.md
│       └── epci-personas-v2.7.md
│
├── docs/                        # Documentation & spécifications
│   ├── epci-v3-complete-specification.md    # Spec complète v3.0
│   ├── epci-component-factory-spec-v3.md    # Spec Component Factory
│   ├── Guide_Bonnes_Pratiques_Claude_Code_EPCI.md  # Best practices (FR)
│   ├── guide-claude-skills.md               # Guide Skills (EN)
│   ├── plan-implementation-v3.md            # Plan migration
│   └── migration/                           # Guides migration
│       ├── v2.7-reference.md
│       ├── breaking-changes.md
│       └── upgrade-guide.md
│
└── src/                         # Implémentation v3.0
    ├── .claude-plugin/
    │   └── plugin.json          # Manifeste plugin
    │
    ├── agents/                  # 5 subagents custom
    │   ├── code-reviewer.md
    │   ├── doc-generator.md
    │   ├── plan-validator.md
    │   ├── qa-reviewer.md
    │   └── security-auditor.md
    │
    ├── commands/                # 5 commandes
    │   ├── create.md           # /epci:create - Component Factory
    │   ├── epci-brief.md       # Point d'entrée + routing
    │   ├── epci-quick.md       # Workflow TINY/SMALL
    │   ├── epci-spike.md       # Exploration time-boxed
    │   └── epci.md             # Workflow complet 3 phases
    │
    ├── hooks/                   # Système de hooks (v3.1)
    │   ├── README.md           # Documentation utilisateur
    │   ├── runner.py           # Moteur d'exécution
    │   ├── examples/           # Exemples de hooks
    │   └── active/             # Hooks actifs (symlinks)
    │
    ├── scripts/                 # Validation
    │   ├── validate_all.py     # Orchestrateur
    │   ├── validate_command.py
    │   ├── validate_flags.py   # Validation système flags (v3.1)
    │   ├── validate_skill.py
    │   ├── validate_subagent.py
    │   └── test_triggering.py
    │
    ├── settings/                # Configuration (v3.1)
    │   └── flags.md            # Documentation flags universels
    │
    └── skills/                  # 20+ skills
        ├── core/               # Skills fondamentaux (6)
        │   ├── architecture-patterns/SKILL.md
        │   ├── code-conventions/SKILL.md
        │   ├── epci-core/SKILL.md
        │   ├── flags-system/SKILL.md  # Système flags universels (v3.1)
        │   ├── git-workflow/SKILL.md
        │   └── testing-strategy/SKILL.md
        │
        ├── stack/              # Skills par technologie (4)
        │   ├── java-springboot/SKILL.md
        │   ├── javascript-react/SKILL.md
        │   ├── php-symfony/SKILL.md
        │   └── python-django/SKILL.md
        │
        ├── personas/           # Personas système (1)
        │   ├── SKILL.md
        │   └── references/
        │       ├── architect.md
        │       ├── frontend.md
        │       ├── backend.md
        │       ├── security.md
        │       ├── qa.md
        │       └── doc.md
        │
        └── factory/            # Component Factory (4)
            ├── commands-creator/
            │   ├── SKILL.md
            │   ├── references/
            │   ├── templates/
            │   └── scripts/
            ├── component-advisor/SKILL.md
            ├── skills-creator/
            │   ├── SKILL.md
            │   ├── references/
            │   ├── templates/
            │   └── scripts/
            └── subagents-creator/
                ├── SKILL.md
                ├── references/
                ├── templates/
                └── scripts/
```

### 2.1 Rôle de chaque dossier

| Dossier | Rôle | État |
|---------|------|------|
| `archive/` | Versions historiques dépréciées | Vide (prêt pour v2.7) |
| `build/` | Version en production | v2.7 (12 commandes) |
| `docs/` | Spécifications, guides, migration | Complet |
| `src/` | Implémentation v3.0 | En développement |

---

## 3. Core Concepts

### 3.1 Workflow EPCI (4 phases)

```
Explore → Plan → Code → Inspect
```

| Phase | Objectif | Output |
|-------|----------|--------|
| **Explore** | Comprendre le codebase, identifier patterns | Analyse contextuelle |
| **Plan** | Concevoir la stratégie d'implémentation | Plan technique validé |
| **Code** | Implémenter avec TDD | Code + tests |
| **Inspect** | Vérifier, documenter, finaliser | Feature Document complet |

### 3.2 Routing par complexité

```
                ┌──────────────────┐
                │   Brief brut     │
                └────────┬─────────┘
                         │
                         ▼
        ┌────────────────────────────────┐
        │         /epci-brief            │
        │  • Load Project Memory (1x)    │
        │  • @Explore (thorough)         │
        │  • Clarification               │
        │  • Évaluation complexité       │
        │  • Génération output + Memory  │
        └────────────────┬───────────────┘
                         │
       ┌─────────────────┼─────────────────┐
       │                 │                 │
       ▼                 ▼                 ▼
┌─────────────┐   ┌─────────────┐   ┌─────────────┐
│ TINY/SMALL  │   │ STD/LARGE   │   │   SPIKE     │
│ Brief inline│   │Feature Doc  │   │ Brief inline│
│ /epci-quick │   │   /epci     │   │ /epci-spike │
└─────────────┘   └─────────────┘   └─────────────┘
```

**Note :** `/epci-brief` effectue l'exploration complète et génère :
- Brief inline pour TINY/SMALL (pas de fichier)
- Feature Document avec §1 rempli pour STANDARD/LARGE

**Memory Pattern (v3.2+):** Project Memory is loaded **once** in `/epci-brief` and passed downstream:
- Via "Memory Summary" section in Feature Document §1 (STANDARD/LARGE)
- Via "Memory Summary" section in inline brief (TINY/SMALL)
- `/epci` and `/epci-quick` read memory from context, not from disk

| Catégorie | Critères | Workflow | Durée |
|-----------|----------|----------|-------|
| **TINY** | 1 fichier, < 50 LOC, aucun risque | `/epci-quick` | < 15 min |
| **SMALL** | 2-3 fichiers, < 200 LOC, risque faible | `/epci-quick` | 15-60 min |
| **STANDARD** | 4-10 fichiers, tests requis | `/epci` (3 phases) | 1-4 h |
| **LARGE** | 10+ fichiers, architecture complexe | `/epci --large` | 4+ h |
| **SPIKE** | Exploration, incertitude technique | `/epci-spike` | Time-boxé |

### 3.3 Feature Document Pattern

Chaque feature STANDARD/LARGE génère un Feature Document unique :

```
docs/features/<slug>.md
```

**Cycle de vie (v3.2) :**

| Section | Créé par | Contenu |
|---------|----------|---------|
| §1 | `/epci-brief` | Brief fonctionnel, stack, critères, Memory Summary |
| §2 | `/epci` Phase 1 | Plan d'implémentation, fichiers impactés, tâches, risques |
| §3 | `/epci` Phases 2-3 | Implémentation, tests, reviews, commits, documentation |

> **Note (v3.2):** §3 et §4 fusionnés. Le tableau des fichiers est maintenant uniquement dans §2.

**Structure :**

```markdown
# Feature Document — [Titre]

## §1 — Brief Fonctionnel
[Créé par /epci-brief avec exploration complète]
- Contexte, stack détecté
- Critères d'acceptation, contraintes, hors scope
- Memory Summary (chargé une fois)

## §2 — Plan d'Implémentation
[Généré par /epci Phase 1]
- Fichiers impactés (tableau unique)
- Tâches atomiques, validation @plan-validator

## §3 — Implementation & Finalization
[Mis à jour par /epci Phases 2-3]
- Progress, tests, reviews (Phase 2)
- Commit message, documentation, PR ready (Phase 3)
```

### 3.4 Modèle Subagent

#### Subagents Natifs Claude Code

| Subagent | Model | Mode | Usage EPCI |
|----------|-------|------|------------|
| **@Explore** | Haiku | Read-only | Analyse codebase (invoqué par `/epci-brief`) |
| **General-purpose** | Sonnet | Read+Write | Implémentation |

**Note :** `@Plan` n'est plus utilisé — l'exploration est centralisée dans `/epci-brief`.

#### Subagents Custom EPCI

| Subagent | Rôle | Invoqué par |
|----------|------|-------------|
| **@plan-validator** | Valide le plan avant Phase 2 | `/epci` Phase 1 |
| **@code-reviewer** | Revue qualité code | `/epci` Phase 2, `/epci-quick` |
| **@security-auditor** | Audit sécurité OWASP | `/epci` Phase 2 (conditionnel) |
| **@qa-reviewer** | Revue tests et couverture | `/epci` Phase 2 (conditionnel) |
| **@doc-generator** | Génération documentation | `/epci` Phase 3 |

### 3.5 Système Skills

#### Skills Core (5)

| Skill | Rôle | Chargé par |
|-------|------|------------|
| `epci-core` | Concepts workflow, Feature Document | Toutes commandes |
| `architecture-patterns` | Design patterns, SOLID, DDD | `/epci-brief`, `/epci` Phase 1 |
| `code-conventions` | Naming, formatting, structure | `/epci-quick`, `/epci` Phase 2 |
| `testing-strategy` | TDD, coverage, mocking | `/epci` Phase 2 |
| `git-workflow` | Conventional Commits, branching | `/epci` Phase 3 |

#### Skills Stack (4) — Auto-détectés

| Skill | Détection | Patterns |
|-------|-----------|----------|
| `php-symfony` | `composer.json` | Bundles, Services, Doctrine |
| `javascript-react` | `package.json` + react | Hooks, Components, State |
| `python-django` | `requirements.txt` / `pyproject.toml` | Models, Views, DRF |
| `java-springboot` | `pom.xml` / `build.gradle` | Annotations, Beans, JPA |

#### Skills Factory (4)

| Skill | Rôle | Invoqué par |
|-------|------|-------------|
| `skills-creator` | Création interactive de skills | `/epci:create skill` |
| `commands-creator` | Création de commandes | `/epci:create command` |
| `subagents-creator` | Création de subagents | `/epci:create agent` |
| `component-advisor` | Détection opportunités création | Passif (auto) |

### 3.6 Système de Hooks (v3.1+)

Le système de hooks permet d'exécuter des scripts personnalisés à des points précis du workflow EPCI.

#### Points de Hook (v3.2)

| Hook Type | Déclencheur | Usage |
|-----------|-------------|-------|
| `pre-brief` | Avant exploration /epci-brief | Charger config externe, valider environnement |
| `post-brief` | Après évaluation complexité | Notifier début feature, créer tickets |
| `pre-phase-1` | Avant Phase 1 | Charger contexte, vérifier prérequis |
| `post-phase-1` | Après validation plan | Notifier équipe, mettre à jour tickets |
| `pre-phase-2` | Avant Phase 2 | Exécuter linters, setup environnement |
| `post-phase-2` | Après code review | Tests additionnels, coverage |
| `post-phase-3` | Après finalisation | Déployer, notifier, métriques |
| `on-breakpoint` | À chaque breakpoint | Logging, collecte métriques |

> **Note:** `pre-phase-3` supprimé en v3.2 (redondant avec `post-phase-2`).

#### Structure des Fichiers

```
hooks/
├── README.md           # Documentation utilisateur
├── runner.py           # Moteur d'exécution (~300 LOC)
├── examples/           # Exemples de hooks
│   ├── pre-phase-2-lint.sh
│   ├── post-phase-3-notify.py
│   └── on-breakpoint-log.sh
└── active/             # Hooks actifs (symlinks vers examples/)
```

#### Format d'un Hook

Les hooks reçoivent un contexte JSON via stdin et retournent un résultat JSON:

```python
#!/usr/bin/env python3
import sys, json
context = json.loads(sys.stdin.read())
# Logic here
print(json.dumps({"status": "success", "message": "Hook completed"}))
```

#### Configuration

| Paramètre | Défaut | Description |
|-----------|--------|-------------|
| `enabled` | `true` | Activer/désactiver les hooks |
| `timeout_seconds` | `30` | Timeout par hook |
| `fail_on_error` | `false` | Stopper le workflow si erreur |

Voir `hooks/README.md` pour la documentation complète.

### 3.7 Système de Flags Universels (v3.1+)

Le système de flags permet un contrôle fin du comportement des workflows EPCI.

#### Catégories de Flags

| Catégorie | Flags | Usage |
|-----------|-------|-------|
| **Thinking** | `--think`, `--think-hard`, `--ultrathink` | Profondeur d'analyse |
| **Compression** | `--uc`, `--verbose` | Gestion tokens |
| **Workflow** | `--safe`, `--no-hooks` | Contrôle exécution |
| **Persona** | `--persona-architect`, `--persona-frontend`, etc. | Modes de pensée globaux (v3.2) |
| **Wave** | `--wave`, `--wave-strategy` | Orchestration multi-vagues |
| **Legacy** | `--large`, `--continue` | Rétrocompatibilité |

#### Auto-Activation

Les flags peuvent être auto-activés selon le contexte:

| Condition | Seuil | Flag |
|-----------|-------|------|
| Fichiers impactés | 3-10 | `--think` |
| Fichiers impactés | >10 | `--think-hard` |
| Context window | >75% | `--uc` |
| Fichiers sensibles | auth, security, payment | `--safe` |
| Complexité | >0.7 | `--wave` |

#### Règles de Précédence

1. Flags explicites > Auto-activation
2. `--ultrathink` > `--think-hard` > `--think`
3. `--verbose` explicit > `--uc` auto

#### Migration depuis v3.0

| v3.0 | v3.1 équivalent |
|------|-----------------|
| `--large` | `--think-hard --wave` |

Voir `src/settings/flags.md` pour la documentation complète.

### 3.8 Système de Personas (v3.2+)

Le système de personas définit des **modes de pensée globaux** qui influencent l'ensemble du workflow EPCI.

#### 6 Personas Workflow

| Persona | Icon | Focus | Flag |
|---------|------|-------|------|
| **Architect** | 🏗️ | System thinking, patterns, scalability | `--persona-architect` |
| **Frontend** | 🎨 | UI/UX, accessibility, Core Web Vitals | `--persona-frontend` |
| **Backend** | ⚙️ | APIs, data integrity, reliability | `--persona-backend` |
| **Security** | 🔒 | Threat modeling, OWASP, compliance | `--persona-security` |
| **QA** | 🧪 | Tests, edge cases, coverage | `--persona-qa` |
| **Doc** | 📝 | Documentation, clarity, examples | `--persona-doc` |

#### Auto-Activation

```
Score = (keywords × 0.4) + (files × 0.4) + (stack × 0.2)
```

| Score | Action |
|-------|--------|
| > 0.6 | Auto-activate persona |
| 0.4-0.6 | Suggest to user at breakpoint |
| < 0.4 | No activation |

#### Personas vs Subagents vs Brainstormer

| Aspect | Persona (F09) | Subagent | Brainstormer |
|--------|---------------|----------|--------------|
| **Scope** | Entire workflow | Validation point | `/brainstorm` only |
| **Timing** | During generation | After generation | Facilitation sessions |
| **Role** | Thinking mode | Verification | Facilitation style |
| **Count** | 6 workflow personas | 5 custom | 3 facilitation personas |

**No Conflict**: They operate at different levels without interference.

#### Integration dans `/epci-brief`

Step 5: Persona Detection (nouveau en v3.2)
1. Calcul du score pour les 6 personas via algorithme
2. Auto-activation si score > 0.6
3. Suggestion si score 0.4-0.6
4. Affichage dans la ligne FLAGS du breakpoint

#### Exemple

```bash
# Brief: "Add user authentication endpoint with JWT"
# → --persona-backend (auto: 0.65) + --persona-security (auto: 0.61)

┌─────────────────────────────────────────────────────────────────────┐
│ FLAGS: --think-hard (auto) | --persona-backend (auto: 0.65)        │
│        --persona-security (suggested: 0.61)                        │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 4. Component Reference

### 4.1 Commands (5)

#### `/epci-brief` — Point d'entrée

```yaml
---
description: >-
  Point d'entrée EPCI - Exploration complète, clarification,
  évaluation complexité et génération du brief/Feature Document.
allowed-tools: [Read, Glob, Grep, Bash, Task, Write]
---
```

**Workflow :**
1. Réception brief brut
2. Invocation `@Explore` (thorough) — exploration complète
3. Boucle clarification (max 3 itérations)
4. Évaluation complexité
5. **Détection personas** (v3.2) — scoring et auto-activation
6. Génération output selon catégorie
7. Routage vers `/epci-quick`, `/epci`, ou `/epci-spike`

**Output :**
- TINY/SMALL → Brief inline structuré
- STANDARD/LARGE → Feature Document créé (`docs/features/<slug>.md`) avec §1 rempli

#### `/epci` — Workflow complet

```yaml
---
description: >-
  Workflow EPCI complet en 3 phases pour features STANDARD et LARGE.
argument-hint: [--large] [--continue]
allowed-tools: [Read, Write, Edit, Bash, Grep, Glob, Task]
---
```

**Phases :**

| Phase | Subagents | Skills | Thinking |
|-------|-----------|--------|----------|
| 1 - Planification | @plan-validator | epci-core, architecture-patterns | `think hard` |
| 2 - Code | @code-reviewer, @security-auditor*, @qa-reviewer* | testing-strategy, code-conventions | `think` |
| 3 - Finalize | @doc-generator | git-workflow | `think` |

*= conditionnel

**Note :** Phase 1 lit le §1 du Feature Document (créé par `/epci-brief`) et passe directement à la planification.

**BREAKPOINTS :** Confirmation utilisateur entre chaque phase

#### `/epci-quick` — Workflow condensé

```yaml
---
description: >-
  Workflow EPCI condensé pour features TINY et SMALL.
  Single-pass sans Feature Document formel.
allowed-tools: [Read, Write, Edit, Bash, Grep, Glob, Task]
---
```

**Modes :**
- **TINY** : < 50 LOC, 1 fichier, pas de tests
- **SMALL** : < 200 LOC, 2-3 fichiers, tests optionnels

#### `/epci-spike` — Exploration

```yaml
---
description: >-
  Exploration time-boxée pour incertitudes techniques.
  Génère un Spike Report (pas un Feature Document).
argument-hint: [durée] [question]
allowed-tools: [Read, Glob, Grep, Bash, Task, WebFetch]
---
```

**Output :** Spike Report avec verdict GO/NO-GO/MORE_RESEARCH

#### `/epci:create` — Component Factory

```yaml
---
description: >-
  Dispatcher Component Factory pour créer skills, commands, ou subagents.
argument-hint: skill|command|agent <name>
allowed-tools: [Read, Write, Glob, Bash]
---
```

**Routing :**
- `skill` → Invoque `skills-creator`
- `command` → Invoque `commands-creator`
- `agent` → Invoque `subagents-creator`

### 4.2 Custom Subagents (5)

#### @plan-validator

```yaml
---
name: plan-validator
description: Valide le plan d'implémentation avant Phase 2
allowed-tools: [Read, Grep]
---
```

**Critères validation :**
- Tâches atomiques (2-15 min)
- Dépendances ordonnées
- Tests prévus pour chaque tâche
- Risques identifiés et mitigés

**Verdict :** `APPROVED` | `NEEDS_REVISION`

#### @code-reviewer

```yaml
---
name: code-reviewer
description: Revue de code orientée qualité et maintenabilité
allowed-tools: [Read, Grep, Glob]
---
```

**Checklist :**
- SOLID principles
- DRY, KISS, YAGNI
- Naming conventions
- Error handling
- Test coverage

#### @security-auditor

```yaml
---
name: security-auditor
description: Audit sécurité OWASP Top 10
allowed-tools: [Read, Grep]
---
```

**Invocation conditionnelle :** Fichiers auth, API, input handling

**Checklist :** Injection, XSS, CSRF, Auth bypass, Data exposure

#### @qa-reviewer

```yaml
---
name: qa-reviewer
description: Revue qualité des tests et couverture
allowed-tools: [Read, Grep, Bash]
---
```

**Invocation conditionnelle :** STANDARD/LARGE avec tests complexes

**Checklist :** Coverage, edge cases, mocking, assertions

#### @doc-generator

```yaml
---
name: doc-generator
description: Génération documentation technique
allowed-tools: [Read, Write, Glob]
---
```

**Outputs :**
- README updates
- API documentation
- CHANGELOG entries
- Inline documentation

### 4.3 Skills Catalog

#### Core Skills (6)

| Skill | Fichier | Description |
|-------|---------|-------------|
| epci-core | `skills/core/epci-core/SKILL.md` | Workflow EPCI, Feature Document, phases |
| architecture-patterns | `skills/core/architecture-patterns/SKILL.md` | SOLID, DDD, Clean Architecture |
| code-conventions | `skills/core/code-conventions/SKILL.md` | Naming, formatting, structure |
| flags-system | `skills/core/flags-system/SKILL.md` | Flags universels, auto-activation, précédence (v3.1) |
| testing-strategy | `skills/core/testing-strategy/SKILL.md` | TDD, BDD, coverage, mocking |
| git-workflow | `skills/core/git-workflow/SKILL.md` | Conventional Commits, branching |

#### Personas Skills (1)

| Skill | Fichier | Description |
|-------|---------|-------------|
| personas | `skills/personas/SKILL.md` | 6 workflow personas with auto-activation (v3.2) |

#### Stack Skills

| Skill | Fichier | Auto-détection |
|-------|---------|----------------|
| php-symfony | `skills/stack/php-symfony/SKILL.md` | `composer.json` |
| javascript-react | `skills/stack/javascript-react/SKILL.md` | `package.json` + react |
| python-django | `skills/stack/python-django/SKILL.md` | `requirements.txt` |
| java-springboot | `skills/stack/java-springboot/SKILL.md` | `pom.xml` |

#### Factory Skills

| Skill | Fichier | Contenu |
|-------|---------|---------|
| skills-creator | `skills/factory/skills-creator/` | SKILL.md + references/ + templates/ + scripts/ |
| commands-creator | `skills/factory/commands-creator/` | SKILL.md + references/ + templates/ + scripts/ |
| subagents-creator | `skills/factory/subagents-creator/` | SKILL.md + references/ + templates/ + scripts/ |
| component-advisor | `skills/factory/component-advisor/SKILL.md` | Détection passive |

---

## 5. Architecture Patterns

### 5.1 Dispatch et Routing

```
User Request
    │
    ▼
/epci-brief (ALWAYS FIRST)
    │
    ├─► Complexity = TINY/SMALL  ──► /epci-quick
    │
    ├─► Complexity = STANDARD    ──► /epci
    │
    ├─► Complexity = LARGE       ──► /epci --large
    │
    └─► Uncertainty = HIGH       ──► /epci-spike
```

### 5.2 Invocation Subagents

```markdown
# Dans une commande ou skill

**Invoquer subagent natif :**
@Explore avec niveau "medium" pour analyser le codebase

**Invoquer subagent custom :**
@code-reviewer avec le code implémenté
```

**Syntaxe invocation :**
- Natifs : `@Explore`, `@Plan`
- Customs : `@plan-validator`, `@code-reviewer`, etc.

### 5.3 Auto-loading Skills

Les skills sont chargés automatiquement par matching sémantique :

```yaml
# SKILL.md
---
name: php-symfony
description: >-
  Guides PHP/Symfony development with best practices.
  Auto-invoke when composer.json detected or Symfony mentioned.
  Do NOT load for Laravel or plain PHP projects.
---
```

**Formule description :**
```
[Capacité] + [Auto-invoke WHEN...] + [Do NOT load for...]
```

### 5.4 Cycle de vie Feature Document (v3.2)

```
┌─────────────────────────────────────────────────────────┐
│                    Feature Document                      │
│                 docs/features/<slug>.md                  │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  /epci-brief ──────► §1 Brief Fonctionnel               │
│                      + Memory Summary (chargé 1x)        │
│                                                          │
│  /epci Phase 1 ────► §2 Plan d'Implémentation           │
│       │              + Fichiers impactés (tableau)       │
│       │              + Validation @plan-validator        │
│       │                                                  │
│       ▼ BREAKPOINT                                       │
│                                                          │
│  /epci Phase 2 ────► §3 Implementation & Finalization   │
│       │              + Progress, tests, reviews          │
│       │                                                  │
│       ▼ BREAKPOINT                                       │
│                                                          │
│  /epci Phase 3 ────► §3 (append)                        │
│                      + Commit, docs, PR ready            │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

---

## 6. Development Guidelines

### 6.1 Conventions de nommage

| Élément | Convention | Exemple |
|---------|------------|---------|
| Commandes | kebab-case, `.md` | `epci-brief.md` |
| Subagents | kebab-case, `.md` | `code-reviewer.md` |
| Skills | kebab-case (dossier) | `php-symfony/SKILL.md` |
| Scripts | snake_case, `.py` | `validate_skill.py` |
| Feature Documents | kebab-case | `add-user-auth.md` |

### 6.2 Standards YAML Frontmatter

#### Commandes

```yaml
---
description: >-
  Action courte en infinitif (~50-100 mots max).
  Inclure contexte d'usage et cas exclus.
argument-hint: [param1] [--flag]
allowed-tools: [Read, Write, Edit, Bash, Grep, Glob, Task]
---
```

#### Subagents

```yaml
---
name: kebab-case-name
description: Rôle spécialisé en 1-2 phrases
model: claude-sonnet  # optionnel
allowed-tools: [Read, Grep]  # minimal
---
```

#### Skills

```yaml
---
name: kebab-case-name
description: >-
  [Capacité]. Auto-invoke when [conditions].
  Do NOT load for [exclusions].
allowed-tools: [Read, Write]  # optionnel
---
```

### 6.3 Limites tokens

| Composant | Limite | Raison |
|-----------|--------|--------|
| Commandes | < 5000 tokens | Performance chargement |
| Skills (SKILL.md) | < 5000 tokens | Auto-loading rapide |
| Subagents | < 2000 tokens | Focus mission |
| Descriptions | ≤ 1024 chars | Matching sémantique |

### 6.4 Validation obligatoire

Avant tout merge, exécuter :

```bash
# Valider un skill
python src/scripts/validate_skill.py src/skills/core/epci-core/

# Valider une commande
python src/scripts/validate_command.py src/commands/epci-brief.md

# Valider un subagent
python src/scripts/validate_subagent.py src/agents/code-reviewer.md

# Valider tout
python src/scripts/validate_all.py
```

**Critères validation :**
- YAML frontmatter valide
- Nom ≤ 64 caractères, kebab-case
- Description présente et formule correcte
- Tokens dans les limites
- Structure fichiers correcte

---

## 7. Migration Notes (v2.7 → v3.0)

### 7.1 Mapping fonctionnalités

| v2.7 | v3.0 | Notes |
|------|------|-------|
| `epci-discover` | `epci-brief` | Clarification intégrée |
| `epci-0-briefing` | `epci-brief` | Point d'entrée unifié |
| `epci-micro` | `epci-quick` (TINY) | Mode simplifié |
| `epci-soft` | `epci-quick` (SMALL) | Tests optionnels |
| `epci-1-analyse` | `epci` Phase 1 | + @Plan, @plan-validator |
| `epci-2-code` | `epci` Phase 2 | + subagents review |
| `epci-3-finalize` | `epci` Phase 3 | + @doc-generator |
| `epci-spike` | `epci-spike` | Simplifié |
| `epci-hotfix` | `epci-quick` urgent | Déprécié |
| `epci-flags` | Flags natifs Claude | Déprécié |
| `epci-personas` | `/epci --persona-X` (v3.2) | Réimplémenté avec auto-activation |

### 7.2 Fonctionnalités dépréciées

| Feature v2.7 | Alternative v3.0 |
|--------------|------------------|
| Système de flags custom | Utiliser flags natifs Claude Code |
| Système de personas custom | Système personas EPCI v3.2 avec auto-activation |
| Routing 5 niveaux | Routing simplifié 3 workflows |
| epci-hotfix | `/epci-quick` avec mention urgence |
| Pre-stages (discover) | Intégré dans `/epci-brief` |

### 7.3 Breaking changes

1. **Point d'entrée unique** : Toujours commencer par `/epci-brief`
2. **Feature Document obligatoire** : STANDARD/LARGE uniquement
3. **Subagents automatiques** : Invocation conditionnelle intégrée
4. **Skills auto-loaded** : Plus de chargement manuel

---

## 8. Testing & Validation

### 8.1 Scripts validation

| Script | Cible | Validation |
|--------|-------|------------|
| `validate_skill.py` | Skills | YAML, nom, description, tokens, structure |
| `validate_command.py` | Commands | YAML, frontmatter, structure |
| `validate_subagent.py` | Subagents | YAML, mission focus, tools |
| `test_triggering.py` | Skills | Tests matching sémantique |
| `validate_all.py` | Tout | Orchestrateur global |

### 8.2 Matrice de tests

| Scénario | Commande | Validation |
|----------|----------|------------|
| TINY feature | `/epci-brief` → `/epci-quick` | 1 fichier, < 50 LOC |
| SMALL feature | `/epci-brief` → `/epci-quick` | 2-3 fichiers, tests optionnels |
| STANDARD feature | `/epci-brief` → `/epci` | Feature Document complet |
| LARGE feature | `/epci-brief` → `/epci --large` | Tous subagents invoqués |
| Spike | `/epci-brief` → `/epci-spike` | Spike Report généré |
| Component creation | `/epci:create skill test` | Skill validé et testé |

### 8.3 Quality gates

- [ ] Tous scripts validation passent (exit code 0)
- [ ] Feature Documents bien formés
- [ ] Subagents invoqués appropriément
- [ ] Skills auto-loaded correctement
- [ ] BREAKPOINTS respectés

---

## 9. Contributing

### 9.1 Créer un nouveau composant

```bash
# Utiliser le Component Factory
/epci:create skill mon-nouveau-skill
/epci:create command ma-nouvelle-commande
/epci:create agent mon-nouvel-agent
```

### 9.2 Workflow de contribution

1. **Analyser** : Identifier le besoin
2. **Créer** : Utiliser `/epci:create` pour le squelette
3. **Implémenter** : Suivre le workflow 6 phases du factory skill
4. **Valider** : Exécuter scripts validation
5. **Tester** : Tests triggering + tests fonctionnels
6. **Documenter** : Mettre à jour ce CLAUDE.md si nécessaire
7. **Soumettre** : PR avec checklist complète

### 9.3 Checklist PR

- [ ] Validation scripts passent
- [ ] Tests triggering passent (skills)
- [ ] Documentation à jour
- [ ] Pas de secrets en dur
- [ ] `allowed-tools` restrictif
- [ ] Descriptions suivent la formule
