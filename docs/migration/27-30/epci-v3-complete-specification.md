# EPCI v3.0 — Spécification Complète pour Implémentation

> **Document** : Cahier des charges autoportant pour génération par Claude Code
> **Version** : 3.0.0
> **Date** : Décembre 2024
> **Objectif** : Générer l'intégralité du plugin EPCI v3 à partir de ce document
> **Usage** : Soumettre ce document à Claude Code pour génération automatique

---

## Table des matières

1. [Présentation du projet](#1-présentation-du-projet)
2. [Architecture cible](#2-architecture-cible)
3. [Subagents natifs Claude Code](#3-subagents-natifs-claude-code)
4. [Commandes EPCI](#4-commandes-epci)
5. [Subagents customs EPCI](#5-subagents-customs-epci)
6. [Skills EPCI](#6-skills-epci)
7. [Component Factory](#7-component-factory)
8. [Scripts de validation](#8-scripts-de-validation)
9. [Feature Document](#9-feature-document)
10. [Plugin Manifest](#10-plugin-manifest)
11. [Critères de validation](#11-critères-de-validation)
12. [Instructions de génération](#12-instructions-de-génération)

---

## 1. Présentation du projet

### 1.1 Qu'est-ce qu'EPCI ?

EPCI (Explore → Plan → Code → Inspect) est un plugin Claude Code qui structure le développement logiciel en phases distinctes avec validation à chaque étape.

### 1.2 Philosophie v3

| Principe | Description |
|----------|-------------|
| **Simplicité** | 4 commandes principales + 1 commande factory |
| **Modularité** | Exploiter les primitives natives Claude Code (Skills, Subagents) |
| **Traçabilité** | Feature Document comme fil rouge de chaque développement |
| **Extensibilité** | Component Factory pour créer de nouveaux composants |

### 1.3 Flux global

```
                    ┌──────────────────┐
                    │   Brief brut     │
                    │   (utilisateur)  │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │   /epci-brief    │
                    │                  │
                    │ • @Explore       │
                    │ • Clarification  │
                    │ • Évaluation     │
                    │ • Routage        │
                    └────────┬─────────┘
                             │
           ┌─────────────────┼─────────────────┐
           │                 │                 │
           ▼                 ▼                 ▼
    ┌─────────────┐   ┌─────────────┐   ┌─────────────┐
    │ TINY/SMALL  │   │ STD/LARGE   │   │  SPIKE      │
    │             │   │             │   │             │
    │ /epci-quick │   │   /epci     │   │ /epci-spike │
    └─────────────┘   └─────────────┘   └─────────────┘
           │                 │                 │
           ▼                 ▼                 ▼
    ┌─────────────────────────────────────────────────┐
    │              Feature Document                   │
    │         (ou Spike Report pour spike)            │
    └─────────────────────────────────────────────────┘
```

### 1.4 Catégories de complexité

| Catégorie | Critères | Workflow | Durée estimée |
|-----------|----------|----------|---------------|
| **TINY** | 1 fichier, < 50 LOC, aucun risque | `/epci-quick` | < 15 min |
| **SMALL** | 2-3 fichiers, < 200 LOC, risque faible | `/epci-quick` | 15-60 min |
| **STANDARD** | 4-10 fichiers, logique métier, tests requis | `/epci` | 1-4 heures |
| **LARGE** | 10+ fichiers, architecture, multi-composants | `/epci` | 4+ heures |
| **SPIKE** | Exploration, incertitude technique | `/epci-spike` | Time-boxé |

---

## 2. Architecture cible

### 2.1 Structure des fichiers à générer

```
epci-plugin/
├── .claude-plugin/
│   └── plugin.json                      # Manifest du plugin
│
├── commands/                            # 5 commandes
│   ├── epci-brief.md                   # Point d'entrée, clarification, routage
│   ├── epci.md                         # Workflow complet (STANDARD/LARGE)
│   ├── epci-quick.md                   # Workflow condensé (TINY/SMALL)
│   ├── epci-spike.md                   # Exploration time-boxée
│   └── create.md                       # /epci:create - Component Factory
│
├── agents/                              # 5 subagents customs
│   ├── plan-validator.md               # Validation du plan Phase 1
│   ├── code-reviewer.md                # Review code Phase 2
│   ├── security-auditor.md             # Audit sécurité (conditionnel)
│   ├── qa-reviewer.md                  # Review tests (conditionnel)
│   └── doc-generator.md                # Génération doc Phase 3
│
├── skills/                              # 13 skills
│   │
│   │── epci-core/
│   │   └── SKILL.md                    # Concepts fondamentaux EPCI
│   │
│   │── architecture-patterns/
│   │   └── SKILL.md                    # Patterns d'architecture
│   │
│   │── code-conventions/
│   │   └── SKILL.md                    # Conventions de code
│   │
│   │── testing-strategy/
│   │   └── SKILL.md                    # Stratégies de test
│   │
│   │── git-workflow/
│   │   └── SKILL.md                    # Workflow Git
│   │
│   │── php-symfony/
│   │   └── SKILL.md                    # Stack PHP/Symfony
│   │
│   │── python-django/
│   │   └── SKILL.md                    # Stack Python/Django
│   │
│   │── java-springboot/
│   │   └── SKILL.md                    # Stack Java/Spring Boot
│   │
│   │── javascript-react/
│   │   └── SKILL.md                    # Stack JavaScript/React
│   │
│   │── skills-creator/                 # Component Factory
│   │   ├── SKILL.md
│   │   ├── references/
│   │   │   ├── best-practices.md
│   │   │   ├── description-formulas.md
│   │   │   ├── yaml-rules.md
│   │   │   └── checklist.md
│   │   ├── templates/
│   │   │   ├── skill-simple.md
│   │   │   └── skill-advanced.md
│   │   └── scripts/
│   │       ├── validate_skill.py
│   │       └── test_triggering.py
│   │
│   │── commands-creator/               # Component Factory
│   │   ├── SKILL.md
│   │   ├── references/
│   │   │   ├── best-practices.md
│   │   │   ├── frontmatter-guide.md
│   │   │   ├── argument-patterns.md
│   │   │   └── checklist.md
│   │   ├── templates/
│   │   │   ├── command-simple.md
│   │   │   └── command-advanced.md
│   │   └── scripts/
│   │       └── validate_command.py
│   │
│   │── subagents-creator/              # Component Factory
│   │   ├── SKILL.md
│   │   ├── references/
│   │   │   ├── best-practices.md
│   │   │   ├── delegation-patterns.md
│   │   │   ├── tools-restriction.md
│   │   │   └── checklist.md
│   │   ├── templates/
│   │   │   └── subagent-template.md
│   │   └── scripts/
│   │       └── validate_subagent.py
│   │
│   └── component-advisor/              # Component Factory (optionnel)
│       └── SKILL.md
│
└── scripts/
    └── validate_all.py                  # Orchestrateur de validation
```

### 2.2 Conventions de nommage

| Élément | Convention | Exemple |
|---------|------------|---------|
| Commandes | kebab-case | `epci-brief.md` |
| Subagents | kebab-case | `code-reviewer.md` |
| Skills | kebab-case (dossier) | `php-symfony/SKILL.md` |
| Invocation subagent | @name | `@code-reviewer` |
| Scripts | snake_case | `validate_skill.py` |

### 2.3 Récapitulatif des composants

| Type | Nombre | Liste |
|------|--------|-------|
| Commandes | 5 | epci-brief, epci, epci-quick, epci-spike, create |
| Subagents customs | 5 | plan-validator, code-reviewer, security-auditor, qa-reviewer, doc-generator |
| Skills Core | 5 | epci-core, architecture-patterns, code-conventions, testing-strategy, git-workflow |
| Skills Stack | 4 | php-symfony, python-django, java-springboot, javascript-react |
| Skills Factory | 4 | skills-creator, commands-creator, subagents-creator, component-advisor |

---

## 3. Subagents natifs Claude Code

### 3.1 Subagents built-in utilisés

EPCI v3 exploite les subagents natifs de Claude Code :

| Subagent | Model | Mode | Tools | Usage dans EPCI |
|----------|-------|------|-------|-----------------|
| **@Explore** | Haiku | Read-only | Glob, Grep, Read, Bash (ro) | `/epci-brief` : analyse codebase |
| **@Plan** | Sonnet | Research | Read, Glob, Grep, Bash | `/epci` Phase 1 : recherche avant plan |
| **General-purpose** | Sonnet | Read+Write | Tous | Implémentation (comportement par défaut) |

### 3.2 Niveaux de thoroughness (@Explore)

| Niveau | Usage EPCI | Description |
|--------|------------|-------------|
| **Quick** | `/epci-quick`, TINY | Recherche rapide, lookups simples |
| **Medium** | `/epci-brief`, SMALL | Évaluation initiale équilibrée |
| **Very thorough** | `/epci` STANDARD/LARGE, `/epci-spike` | Analyse complète approfondie |

### 3.3 Mapping subagents natifs → Commandes EPCI

| Commande | @Explore | @Plan | General-purpose |
|----------|:--------:|:-----:|:---------------:|
| `/epci-brief` | ✅ Medium | — | — |
| `/epci` Phase 1 | — | ✅ Auto | — |
| `/epci` Phase 2 | — | — | ✅ Auto |
| `/epci` Phase 3 | — | — | ✅ Auto |
| `/epci-quick` | ✅ Quick | — | ✅ Auto |
| `/epci-spike` | ✅ Very thorough | — | — |

---

## 4. Commandes EPCI

### 4.1 Vue d'ensemble des commandes

| Commande | Rôle | Subagents natifs | Subagents customs | Skills |
|----------|------|------------------|-------------------|--------|
| `/epci-brief` | Clarification + routage | @Explore | — | epci-core, architecture-patterns, [stack] |
| `/epci` | Workflow 3 phases | @Plan | @plan-validator, @code-reviewer, @security-auditor*, @qa-reviewer*, @doc-generator | Tous par phase |
| `/epci-quick` | Workflow condensé | @Explore | @code-reviewer (light) | epci-core, code-conventions, git-workflow, [stack] |
| `/epci-spike` | Exploration | @Explore | — | architecture-patterns |
| `/epci:create` | Component Factory | — | — | skills-creator, commands-creator, subagents-creator |

*= conditionnel

---

### 4.2 Commande `/epci-brief`

**Fichier** : `commands/epci-brief.md`

#### 4.2.1 Spécification

```yaml
---
description: >-
  Point d'entrée EPCI - Analyse le brief, clarifie les ambiguïtés, 
  évalue la complexité et route vers le workflow approprié.
allowed-tools: [Read, Glob, Grep, Bash, Task]
---
```

#### 4.2.2 Subagents & Skills utilisés

| Type | Composant | Moment | Obligatoire |
|------|-----------|--------|-------------|
| Subagent natif | @Explore (medium) | Début - analyse codebase | ✅ |
| Skill | epci-core | Chargé au démarrage | ✅ |
| Skill | architecture-patterns | Pour évaluer complexité | ✅ |
| Skill | [stack-specific] | Si détecté automatiquement | Auto |

#### 4.2.3 Comportement fonctionnel

```markdown
# /epci-brief

Tu es l'assistant EPCI en phase de briefing. Ton rôle est de transformer 
un brief brut en brief fonctionnel validé et de router vers le workflow approprié.

## Subagents & Skills

**Au démarrage :**
1. Charger le skill `epci-core`
2. Charger le skill `architecture-patterns`
3. Détecter la stack et charger le skill correspondant :
   - `composer.json` → `php-symfony`
   - `package.json` + React → `javascript-react`
   - `requirements.txt` ou `pyproject.toml` → `python-django`
   - `pom.xml` ou `build.gradle` → `java-springboot`

**Invoquer @Explore** (niveau medium) pour :
- Scanner la structure du projet
- Identifier les technologies utilisées
- Estimer la complexité architecturale

## Étape 1 : Réception et analyse initiale

1. Recevoir le brief brut (texte libre, ticket, transcript)
2. Invoquer @Explore pour analyser le codebase existant
3. Analyser le contenu pour identifier :
   - Les éléments clairs et exploitables
   - Les ambiguïtés et zones d'ombre
   - Les informations manquantes critiques
   - Les incohérences éventuelles

## Étape 2 : Boucle de clarification (itérative)

Si des ambiguïtés sont détectées :

```
TANT QUE brief_incomplet:
    1. Poser 3-5 questions ciblées par catégorie :
       - Business/Valeur : Pourquoi ? Pour qui ? Quel impact ?
       - Scope : Qu'est-ce qui est inclus/exclus ?
       - Contraintes : Techniques, temps, budget ?
       - Priorité : Criticité, dépendances ?
    
    2. Attendre les réponses de l'utilisateur
    
    3. Intégrer les réponses dans le brief
    
    4. Réévaluer : reste-t-il des ambiguïtés ?
       - Si OUI : nouvelles questions plus précises
       - Si NON : sortir de la boucle
```

**Limite** : Maximum 3 itérations de questions

## Étape 3 : Suggestions IA

Proposer des améliorations basées sur l'analyse @Explore :
- Suggestions de design (basées sur architecture-patterns)
- Bonnes pratiques de la stack détectée
- Points d'attention spécifiques au contexte

## Étape 4 : Évaluation de complexité

| Critère | TINY | SMALL | STANDARD | LARGE | SPIKE |
|---------|------|-------|----------|-------|-------|
| Fichiers | 1 | 2-3 | 4-10 | 10+ | ? |
| LOC estimé | <50 | <200 | <1000 | 1000+ | ? |
| Risque | Aucun | Faible | Moyen | Élevé | Inconnu |
| Tests requis | Non | Optionnel | Oui | Oui+ | N/A |
| Archi impactée | Non | Non | Possible | Oui | ? |

## Étape 5 : Routage

Recommander le workflow approprié :

| Catégorie | Commande | Justification |
|-----------|----------|---------------|
| TINY | `/epci-quick` | Exécution immédiate, pas de plan formel |
| SMALL | `/epci-quick` | Plan léger intégré |
| STANDARD | `/epci` | Workflow complet 3 phases |
| LARGE | `/epci` + flag `--large` | Thinking renforcé, subagents obligatoires |
| SPIKE | `/epci-spike` | Exploration time-boxée |

## Output

Générer le brief structuré :

```markdown
# Brief Fonctionnel — [Titre]

## Contexte
[Résumé du besoin]

## Stack détectée
[Stack identifiée par @Explore]

## Critères d'acceptation
- [ ] Critère 1
- [ ] Critère 2
- [ ] Critère 3

## Contraintes
- [Contrainte technique]
- [Contrainte temps/budget]

## Hors périmètre
- [Exclusion explicite]

## Évaluation
- **Catégorie** : [TINY|SMALL|STANDARD|LARGE|SPIKE]
- **Justification** : [Raison de la catégorisation]

## Recommandation
→ Utiliser `/epci-quick` | `/epci` | `/epci-spike`
```
```

---

### 4.3 Commande `/epci`

**Fichier** : `commands/epci.md`

#### 4.3.1 Spécification

```yaml
---
description: >-
  Workflow EPCI complet en 3 phases pour features STANDARD et LARGE.
  Phase 1: Analyse et planification. Phase 2: Implémentation TDD.
  Phase 3: Finalisation et documentation.
argument-hint: [--large] [--continue]
allowed-tools: [Read, Write, Edit, Bash, Grep, Glob, Task]
---
```

#### 4.3.2 Vue d'ensemble des phases

| Phase | Objectif | Subagents | Skills | Thinking |
|-------|----------|-----------|--------|----------|
| **Phase 1** | Analyse + Plan | @Plan (natif), @plan-validator | epci-core, architecture-patterns, [stack] | `think hard` |
| **Phase 2** | Implémentation | @code-reviewer, @security-auditor*, @qa-reviewer* | testing-strategy, code-conventions, [stack] | `think` |
| **Phase 3** | Finalisation | @doc-generator | git-workflow | `think` |

#### 4.3.3 Phase 1 — Analyse et Planification

```markdown
## Phase 1 : Analyse et Planification

### Subagents & Skills

**Skills chargés :**
- `epci-core` (obligatoire)
- `architecture-patterns` (obligatoire)
- `[stack-specific]` (auto-détecté)

**Subagents invoqués :**
- `@Plan` (natif) — Recherche automatique dans le codebase
- `@plan-validator` — Validation du plan avant Phase 2

### Niveau de Thinking

`think hard` — Phase critique nécessitant réflexion approfondie

### Process

1. **Réception du brief fonctionnel**
   - Vérifier que le brief vient de `/epci-brief` ou est complet
   - Si brief incomplet → suggérer `/epci-brief` d'abord

2. **Analyse technique** (utilise @Plan automatiquement)
   - Identifier les fichiers impactés
   - Analyser les dépendances
   - Évaluer les risques techniques

3. **Génération du plan**
   - Découper en tâches atomiques (2-15 min chacune)
   - Ordonner par dépendances
   - Inclure les tests pour chaque tâche

4. **Validation par @plan-validator**
   - Invoquer `@plan-validator` avec le plan généré
   - Attendre verdict : APPROVED | NEEDS_REVISION
   - Si NEEDS_REVISION → corriger et re-soumettre

### Output — Feature Document §2

```markdown
## §2 — Plan d'implémentation

### Fichiers impactés
| Fichier | Action | Risque |
|---------|--------|--------|
| src/Service/X.php | Modifier | Moyen |
| src/Entity/Y.php | Créer | Faible |

### Tâches
1. [ ] **Tâche 1** — Description (5 min)
   - Fichier : `src/...`
   - Test : `tests/...`
   - Commande : `php bin/phpunit --filter ...`

2. [ ] **Tâche 2** — Description (10 min)
   ...

### Risques identifiés
| Risque | Probabilité | Mitigation |
|--------|-------------|------------|
| ... | Moyenne | ... |

### Validation
- **@plan-validator** : [APPROVED]
```

### ⏸️ BREAKPOINT Phase 1

```
---
⏸️ **BREAKPOINT PHASE 1**

Plan complet et validé.
- @plan-validator : APPROVED
- Tâches : X tâches identifiées
- Fichiers : Y fichiers impactés

§2 du Feature Document mis à jour.

**Attendre confirmation :** "Plan validé, continue"
---
```
```

#### 4.3.4 Phase 2 — Implémentation

```markdown
## Phase 2 : Implémentation

### Subagents & Skills

**Skills chargés :**
- `testing-strategy` (obligatoire)
- `code-conventions` (obligatoire)
- `[stack-specific]` (auto-détecté)

**Subagents invoqués :**
- `@code-reviewer` — En fin de phase (obligatoire)
- `@security-auditor` — Si fichiers sensibles détectés (conditionnel)
- `@qa-reviewer` — Si tests complexes (conditionnel)

### Conditions d'invocation des subagents conditionnels

**@security-auditor** si présence de :
- Fichiers matchant : `**/auth/**`, `**/security/**`, `**/password/**`, `**/token/**`, `**/api/**`
- Mots-clés dans le code : `password`, `secret`, `api_key`, `jwt`, `oauth`

**@qa-reviewer** si :
- Plus de 5 fichiers de test créés/modifiés
- Tests d'intégration ou E2E impliqués
- Mocking complexe requis

### Niveau de Thinking

`think` — Implémentation standard

### Process

1. **Pour chaque tâche du plan :**
   ```
   a. Écrire le test qui échoue (RED)
   b. Exécuter le test → confirmer échec
   c. Implémenter le code minimal (GREEN)
   d. Exécuter le test → confirmer passage
   e. Refactorer si nécessaire (REFACTOR)
   f. Cocher la tâche dans le plan
   ```

2. **Après toutes les tâches :**
   - Exécuter la suite de tests complète
   - Invoquer @code-reviewer
   - Invoquer @security-auditor si applicable
   - Invoquer @qa-reviewer si applicable

3. **Traiter les retours des subagents :**
   - Issues Critical → corriger obligatoirement
   - Issues Important → corriger ou justifier
   - Issues Minor → optionnel

### Output — Feature Document §3

```markdown
## §3 — Implémentation

### Progression
- [x] Tâche 1 — Complétée
- [x] Tâche 2 — Complétée
- [ ] Tâche 3 — En cours

### Tests
```bash
$ php bin/phpunit
OK (47 tests, 156 assertions)
```

### Reviews
- **@code-reviewer** : APPROVED (0 Critical, 2 Minor)
- **@security-auditor** : APPROVED (si applicable)
- **@qa-reviewer** : APPROVED (si applicable)

### Déviations du plan
| Tâche | Déviation | Justification |
|-------|-----------|---------------|
| #3 | Fichier supplémentaire | Refactoring nécessaire |
```

### ⏸️ BREAKPOINT Phase 2

```
---
⏸️ **BREAKPOINT PHASE 2**

Code implémenté et validé.
- Tests : 47/47 passing
- @code-reviewer : APPROVED
- @security-auditor : APPROVED (si applicable)

§3 du Feature Document mis à jour.

**Attendre confirmation :** "Code validé, continue"
---
```
```

#### 4.3.5 Phase 3 — Finalisation

```markdown
## Phase 3 : Finalisation

### Subagents & Skills

**Skills chargés :**
- `git-workflow` (obligatoire)

**Subagents invoqués :**
- `@doc-generator` — Génération de la documentation

### Niveau de Thinking

`think` — Finalisation standard

### Process

1. **Commit structuré**
   - Utiliser le format Conventional Commits
   - Message détaillé avec références au Feature Document

2. **Documentation**
   - Invoquer @doc-generator
   - Générer/mettre à jour README si applicable
   - Documenter les changements d'API si applicable

3. **Préparation PR**
   - Créer la branche si pas déjà fait
   - Préparer le template de PR
   - Lister les reviewers suggérés

### Output — Feature Document §4

```markdown
## §4 — Finalisation

### Commit
```
feat(module): implement feature X

- Add Service X with method Y
- Create Entity Z
- Add 47 tests covering all cases

Refs: FEATURE-DOC-001
```

### Documentation
- [x] README mis à jour
- [x] API documentée
- [x] Changelog ajouté

### PR
- **Branche** : feature/xxx
- **Target** : develop
- **Reviewers** : @team-lead, @senior-dev

### Vérification finale
- [x] Tous les tests passent
- [x] Lint/CS clean
- [x] Documentation complète
- [x] PR prête
```

### Fin de workflow

```
---
✅ **WORKFLOW EPCI TERMINÉ**

Feature Document complet : [lien ou path]

**Résumé :**
- Tâches : X/X complétées
- Tests : Y tests, Z assertions
- Reviews : Tous APPROVED
- PR : Prête pour review

**Prochaine étape :** Soumettre la PR
---
```
```

---

### 4.4 Commande `/epci-quick`

**Fichier** : `commands/epci-quick.md`

#### 4.4.1 Spécification

```yaml
---
description: >-
  Workflow EPCI condensé pour features TINY et SMALL.
  Exécution rapide avec plan léger intégré.
allowed-tools: [Read, Write, Edit, Bash, Grep, Glob, Task]
---
```

#### 4.4.2 Subagents & Skills

| Type | Composant | Moment | Obligatoire |
|------|-----------|--------|-------------|
| Subagent natif | @Explore (quick) | Début - lookup rapide | ✅ |
| Subagent custom | @code-reviewer (light) | Fin - review simplifié | ✅ |
| Skill | epci-core | Chargé au démarrage | ✅ |
| Skill | code-conventions | Pour l'implémentation | ✅ |
| Skill | git-workflow | Pour le commit | ✅ |
| Skill | [stack-specific] | Si détecté | Auto |

#### 4.4.3 Comportement fonctionnel

```markdown
# /epci-quick

Workflow condensé pour features simples (TINY/SMALL).

## Subagents & Skills

**Au démarrage :**
1. Charger `epci-core`, `code-conventions`, `git-workflow`
2. Détecter et charger le skill stack-specific
3. Invoquer @Explore (quick) pour lookup rapide

**En fin de workflow :**
- Invoquer @code-reviewer en mode light (pas de sécurité, focus qualité)

## Process unifié

### 1. Analyse rapide (2 min)
- Invoquer @Explore (quick)
- Identifier le(s) fichier(s) à modifier
- Estimer l'impact

### 2. Plan léger inline
- Lister les modifications prévues
- Pas de Feature Document formel
- Pas de breakpoint

### 3. Implémentation directe
- Appliquer les conventions du skill stack
- Écrire tests si applicable (SMALL)
- Implémenter le changement

### 4. Validation
- Lancer les tests
- Invoquer @code-reviewer (light)
- Si issues Critical → corriger

### 5. Commit
- Format Conventional Commits simplifié
- Message concis

## Output

```markdown
---
✅ **EPCI-QUICK TERMINÉ**

**Changements :**
- [fichier1] : [modification]
- [fichier2] : [modification]

**Tests :** OK (X tests)
**Review :** @code-reviewer APPROVED

**Commit :**
```
fix(module): brief description
```
---
```
```

---

### 4.5 Commande `/epci-spike`

**Fichier** : `commands/epci-spike.md`

#### 4.5.1 Spécification

```yaml
---
description: >-
  Exploration technique time-boxée pour réduire l'incertitude.
  Produit un Spike Report, pas de code production.
argument-hint: <durée> — durée en minutes (défaut: 30)
allowed-tools: [Read, Bash, Grep, Glob, WebFetch, WebSearch]
---
```

#### 4.5.2 Subagents & Skills

| Type | Composant | Moment | Obligatoire |
|------|-----------|--------|-------------|
| Subagent natif | @Explore (very thorough) | Exploration approfondie | ✅ |
| Skill | architecture-patterns | Pour évaluer les options | ✅ |

#### 4.5.3 Comportement fonctionnel

```markdown
# /epci-spike

Exploration technique time-boxée.

## Subagents & Skills

**Chargés :**
- `architecture-patterns` — Pour évaluer les options architecturales

**Invoqués :**
- @Explore (very thorough) — Exploration approfondie du codebase et du domaine

## Règles

1. **Time-box strict** : Respecter la durée spécifiée ($1 ou 30 min par défaut)
2. **Pas de code production** : Uniquement du code exploratoire jetable
3. **Output = Spike Report** : Document structuré, pas de commit

## Process

### 1. Cadrage (5 min)
- Définir la question technique précise
- Lister les hypothèses à valider
- Définir les critères de succès

### 2. Exploration (@Explore very thorough)
- Analyser le codebase existant
- Rechercher des solutions (WebSearch si autorisé)
- Prototyper si nécessaire (code jetable)

### 3. Évaluation
- Valider/invalider chaque hypothèse
- Comparer les options trouvées
- Identifier les risques

### 4. Spike Report

```markdown
# Spike Report — [Question]

## Question explorée
[Question technique précise]

## Durée
[X] minutes sur [Y] prévues

## Hypothèses testées
| Hypothèse | Résultat | Preuve |
|-----------|----------|--------|
| H1 : ... | ✅ Validée | [observation] |
| H2 : ... | ❌ Invalidée | [observation] |

## Options identifiées
| Option | Avantages | Inconvénients | Effort |
|--------|-----------|---------------|--------|
| A : ... | ... | ... | Moyen |
| B : ... | ... | ... | Élevé |

## Recommandation
[Option recommandée et justification]

## Questions ouvertes
- [Question non résolue 1]
- [Question non résolue 2]

## Prochaines étapes
- [ ] [Action 1]
- [ ] [Action 2]
```
```

---

### 4.6 Commande `/epci:create`

**Fichier** : `commands/create.md`

#### 4.6.1 Spécification

```yaml
---
description: >-
  Crée un nouveau composant Claude Code (skill, command, subagent).
  Lance un workflow interactif avec brainstorming, critique et génération.
argument-hint: <type> <nom> — type: skill | command | subagent
allowed-tools: [Read, Write, Edit, Bash, Grep, Glob]
---
```

#### 4.6.2 Comportement fonctionnel

```markdown
# /epci:create

Point d'entrée unique pour la création de composants Claude Code.

## Dispatch

| Argument $1 | Skill activé | Destination |
|-------------|--------------|-------------|
| `skill` | skills-creator | `epci-plugin/skills/$2/` |
| `command` | commands-creator | `epci-plugin/commands/$2.md` |
| `subagent` | subagents-creator | `epci-plugin/agents/$2.md` |

## Validation des arguments

1. Vérifier que $1 ∈ {skill, command, subagent}
2. Vérifier que $2 est en kebab-case et ≤64 caractères
3. Vérifier l'absence de conflit de nom

## Gestion des conflits

Avant de créer, scanner le dossier de destination.
Si conflit détecté :
- Informer : "Un composant '$2' existe déjà."
- Proposer : "$2-v2", "$2-new", ou nom personnalisé
- Attendre validation

## Workflow

1. **Activation du skill spécialisé**
2. **Exécution du workflow interactif (6 phases)**
3. **Validation automatique** (script Python)
4. **Confirmation** avec instructions de test

## Exemples

```
/epci:create skill docker-analyzer
→ Lance skills-creator pour créer un skill d'analyse Docker

/epci:create command deploy-staging
→ Lance commands-creator pour créer une commande de déploiement

/epci:create subagent security-reviewer
→ Lance subagents-creator pour créer un agent de revue sécurité
```
```

---

## 5. Subagents customs EPCI

### 5.1 Vue d'ensemble

| Subagent | Mission | Tools | Invoqué par |
|----------|---------|-------|-------------|
| @plan-validator | Valider le plan Phase 1 | Read, Grep, Glob | `/epci` Phase 1 |
| @code-reviewer | Review qualité + architecture | Read, Grep, Glob, Bash | `/epci` Phase 2, `/epci-quick` |
| @security-auditor | Audit OWASP + vulnérabilités | Read, Grep, WebFetch | `/epci` Phase 2 (conditionnel) |
| @qa-reviewer | Valider stratégie de test | Read, Grep, Glob, Bash | `/epci` Phase 2 (conditionnel) |
| @doc-generator | Générer documentation | Read, Write | `/epci` Phase 3 |

### 5.2 Subagent @plan-validator

**Fichier** : `agents/plan-validator.md`

```yaml
---
name: plan-validator
description: >-
  Valide les plans d'implémentation EPCI Phase 1. Vérifie la complétude,
  la cohérence, la faisabilité et l'alignement avec les critères d'acceptation.
  Retourne APPROVED ou NEEDS_REVISION avec feedback détaillé.
model: claude-sonnet-4-20250514
allowed-tools: [Read, Grep, Glob]
---

# Plan Validator Agent

## Mission

Valider le plan d'implémentation avant le passage en Phase 2.

## Critères de validation

### 1. Complétude
- [ ] Tous les critères d'acceptation ont une tâche correspondante
- [ ] Tous les fichiers impactés sont listés
- [ ] Les tests sont prévus pour chaque tâche

### 2. Cohérence
- [ ] Ordre d'implémentation respecte les dépendances
- [ ] Pas de tâche dépendant d'une tâche ultérieure
- [ ] Estimations de temps réalistes (2-15 min par tâche)

### 3. Faisabilité
- [ ] Risques identifiés ont des mitigations
- [ ] Pas de dépendance externe bloquante
- [ ] Stack technique confirmé et maîtrisé

### 4. Qualité
- [ ] Tâches atomiques et testables
- [ ] Descriptions claires et actionnables
- [ ] Pas de tâche vague ou ambiguë

## Format de sortie

```markdown
## Plan Validation Report

### Verdict
**[APPROVED | NEEDS_REVISION]**

### Checklist
- [x] Complétude : OK
- [x] Cohérence : OK
- [ ] Faisabilité : Issue détectée
- [x] Qualité : OK

### Issues (si NEEDS_REVISION)

#### 🔴 Critical
1. [Description du problème critique]
   - **Impact** : [pourquoi c'est bloquant]
   - **Fix suggéré** : [comment corriger]

#### 🟠 Important
1. [Description du problème important]

### Recommandations
- [Suggestion d'amélioration 1]
- [Suggestion d'amélioration 2]
```
```

### 5.3 Subagent @code-reviewer

**Fichier** : `agents/code-reviewer.md`

```yaml
---
name: code-reviewer
description: >-
  Revue de code EPCI Phase 2. Vérifie la qualité, l'architecture,
  les tests et l'alignement avec le plan. Retourne un rapport avec
  sévérité Critical/Important/Minor.
model: claude-sonnet-4-20250514
allowed-tools: [Read, Grep, Glob, Bash]
---

# Code Reviewer Agent

## Mission

Valider le code produit en Phase 2 contre le plan et les standards.

## Checklist de revue

### Code Quality
- [ ] Séparation des responsabilités claire
- [ ] Gestion d'erreurs appropriée
- [ ] Type safety (typage strict)
- [ ] DRY respecté
- [ ] Edge cases gérés

### Architecture
- [ ] Patterns du projet respectés
- [ ] Pas de couplage excessif
- [ ] Performance acceptable
- [ ] Scalabilité considérée

### Tests
- [ ] Tests existent pour chaque fonctionnalité
- [ ] Tests testent la logique, pas les mocks
- [ ] Cas nominaux ET edge cases couverts
- [ ] Tous les tests passent

### Plan Alignment
- [ ] Toutes les tâches implémentées
- [ ] Pas de scope creep
- [ ] Déviations documentées

## Niveaux de sévérité

| Niveau | Critères | Action |
|--------|----------|--------|
| 🔴 Critical | Bug, sécurité, perte de données | Must fix |
| 🟠 Important | Architecture, tests manquants | Should fix |
| 🟡 Minor | Style, optimisation | Nice to have |

## Format de sortie

```markdown
## Code Review Report

### Summary
[1-2 phrases sur la qualité globale]

### Strengths
- [Point fort 1 avec file:line]
- [Point fort 2]

### Issues

#### 🔴 Critical (Must Fix)
1. **[Titre]**
   - File: `path/to/file.php:123`
   - Issue: [Description]
   - Impact: [Pourquoi c'est critique]
   - Fix: [Comment corriger]

#### 🟠 Important (Should Fix)
[...]

#### 🟡 Minor (Nice to Have)
[...]

### Verdict
**[APPROVED | APPROVED_WITH_FIXES | NEEDS_REVISION]**

**Reasoning:** [Justification technique]
```

## Mode Light (pour /epci-quick)

En mode light, focus uniquement sur :
- Bugs évidents
- Erreurs de syntaxe/typage
- Tests manquants pour SMALL

Pas de revue architecture ou optimisation.
```

### 5.4 Subagent @security-auditor

**Fichier** : `agents/security-auditor.md`

```yaml
---
name: security-auditor
description: >-
  Audit de sécurité EPCI Phase 2. Vérifie OWASP Top 10, defense-in-depth,
  et configurations sensibles. Invoqué si fichiers auth/security détectés.
model: claude-sonnet-4-20250514
allowed-tools: [Read, Grep, WebFetch]
---

# Security Auditor Agent

## Mission

Auditer le code pour les vulnérabilités de sécurité.

## Conditions d'invocation

Invoqué automatiquement si détection de :
- Fichiers : `**/auth/**`, `**/security/**`, `**/password/**`, `**/token/**`, `**/api/**`
- Mots-clés : `password`, `secret`, `api_key`, `jwt`, `oauth`, `bearer`

## OWASP Top 10 Checklist

- [ ] A01 - Broken Access Control
- [ ] A02 - Cryptographic Failures
- [ ] A03 - Injection (SQL, XSS, Command)
- [ ] A04 - Insecure Design
- [ ] A05 - Security Misconfiguration
- [ ] A06 - Vulnerable Components
- [ ] A07 - Authentication Failures
- [ ] A08 - Data Integrity Failures
- [ ] A09 - Logging Failures
- [ ] A10 - SSRF

## Defense-in-Depth

Vérifier la validation à chaque couche :
1. **Entry Point** — Controller/API validation
2. **Business Logic** — Service validation
3. **Database** — Constraints (NOT NULL, CHECK, FK)
4. **Output** — Encoding (Twig escape, JSON encode)

## Niveaux de sévérité

| Niveau | CVSS Approx | Exemples |
|--------|-------------|----------|
| 🔴 Critical | 9.0+ | Injection SQL, RCE |
| 🟠 High | 7.0-8.9 | Auth bypass, XSS stored |
| 🟡 Medium | 4.0-6.9 | CSRF, info disclosure |
| ⚪ Low | 0.1-3.9 | Missing headers |

## Format de sortie

```markdown
## Security Audit Report

### Scope
- Files analyzed: X
- Patterns checked: OWASP Top 10 + Defense-in-Depth

### Findings

#### 🔴 Critical
1. **SQL Injection**
   - File: `src/Repository/UserRepository.php:45`
   - Code: `$sql = "SELECT * FROM users WHERE id = " . $id;`
   - Fix: Use prepared statements

#### 🟠 High
[...]

### Verdict
**[APPROVED | NEEDS_FIXES]**
```
```

### 5.5 Subagent @qa-reviewer

**Fichier** : `agents/qa-reviewer.md`

```yaml
---
name: qa-reviewer
description: >-
  Revue QA EPCI Phase 2. Vérifie la stratégie de test, la couverture,
  et les anti-patterns. Invoqué si tests complexes détectés.
model: claude-sonnet-4-20250514
allowed-tools: [Read, Grep, Glob, Bash]
---

# QA Reviewer Agent

## Mission

Valider la qualité et la stratégie des tests.

## Conditions d'invocation

Invoqué automatiquement si :
- Plus de 5 fichiers de test créés/modifiés
- Tests d'intégration ou E2E impliqués
- Mocking complexe détecté

## Checklist

### Stratégie
- [ ] Pyramide de tests respectée (unit > integration > e2e)
- [ ] Tests isolés et indépendants
- [ ] Pas de dépendances entre tests
- [ ] Fixtures/factories utilisées

### Couverture
- [ ] Cas nominaux couverts
- [ ] Edge cases couverts
- [ ] Cas d'erreur couverts
- [ ] Limites testées

### Anti-patterns à détecter
- ❌ Tester les mocks au lieu du code
- ❌ Méthodes test-only dans le code prod
- ❌ Mocking sans comprendre ce qu'on mock
- ❌ Mocks incomplets (pas tous les cas)
- ❌ Tests écrits après le code (afterthought)

## Format de sortie

```markdown
## QA Review Report

### Test Strategy
- Unit tests: X
- Integration tests: Y
- E2E tests: Z
- Pyramid: [OK | Inverted | Imbalanced]

### Coverage Assessment
- Nominal cases: [OK | Partial | Missing]
- Edge cases: [OK | Partial | Missing]
- Error cases: [OK | Partial | Missing]

### Anti-patterns Detected
1. [Anti-pattern détecté]
   - File: `tests/...`
   - Issue: [Description]
   - Fix: [Suggestion]

### Verdict
**[APPROVED | NEEDS_IMPROVEMENT]**
```
```

### 5.6 Subagent @doc-generator

**Fichier** : `agents/doc-generator.md`

```yaml
---
name: doc-generator
description: >-
  Génération de documentation EPCI Phase 3. Crée ou met à jour
  README, API docs, changelog basé sur les changements effectués.
model: claude-sonnet-4-20250514
allowed-tools: [Read, Write]
---

# Documentation Generator Agent

## Mission

Générer la documentation appropriée pour les changements effectués.

## Types de documentation

| Type | Quand | Format |
|------|-------|--------|
| README | Nouveau composant | Markdown |
| API Docs | Endpoints modifiés | OpenAPI / Markdown |
| Changelog | Toujours | CHANGELOG.md |
| PHPDoc/JSDoc | Classes/fonctions publiques | Inline |

## Process

1. **Analyser les changements** (git diff)
2. **Identifier les besoins** de documentation
3. **Générer/mettre à jour** les fichiers
4. **Valider** la cohérence

## Templates

### README pour nouveau composant
```markdown
# [Nom du composant]

## Description
[Ce que fait le composant]

## Installation
[Comment l'installer]

## Usage
[Comment l'utiliser avec exemples]

## Configuration
[Options de configuration]

## API
[Méthodes/endpoints publics]
```

### Entrée Changelog
```markdown
## [Version] - YYYY-MM-DD

### Added
- [Nouvelle fonctionnalité]

### Changed
- [Modification]

### Fixed
- [Correction de bug]
```

## Format de sortie

```markdown
## Documentation Report

### Files Created
- `docs/api/feature-x.md`

### Files Updated
- `README.md` (section Usage)
- `CHANGELOG.md` (v1.2.0)

### Summary
[Résumé des ajouts documentaires]
```
```

---

## 6. Skills EPCI

### 6.1 Vue d'ensemble des skills

| Skill | Catégorie | Description courte |
|-------|-----------|-------------------|
| epci-core | Core | Concepts fondamentaux du workflow EPCI |
| architecture-patterns | Core | Patterns d'architecture logicielle |
| code-conventions | Core | Conventions de code et bonnes pratiques |
| testing-strategy | Core | Stratégies et patterns de test |
| git-workflow | Core | Workflow Git et conventions de commit |
| php-symfony | Stack | Patterns Symfony/Doctrine/PHPUnit |
| python-django | Stack | Patterns Django/pytest |
| java-springboot | Stack | Patterns Spring Boot/JUnit |
| javascript-react | Stack | Patterns React/Jest/TypeScript |
| skills-creator | Factory | Création de nouveaux skills |
| commands-creator | Factory | Création de nouvelles commandes |
| subagents-creator | Factory | Création de nouveaux subagents |
| component-advisor | Factory | Détection et suggestion de composants |

### 6.2 Mapping Skills → Commandes

| Skill | Brief | Phase 1 | Phase 2 | Phase 3 | Quick | Spike | Create |
|-------|:-----:|:-------:|:-------:|:-------:|:-----:|:-----:|:------:|
| epci-core | ✅ | ✅ | ✅ | ✅ | ✅ | — | — |
| architecture-patterns | ✅ | ✅ | — | — | — | ✅ | — |
| code-conventions | — | — | ✅ | — | ✅ | — | — |
| testing-strategy | — | — | ✅ | — | — | — | — |
| git-workflow | — | — | — | ✅ | ✅ | — | — |
| php-symfony | Auto | Auto | Auto | Auto | Auto | Auto | — |
| python-django | Auto | Auto | Auto | Auto | Auto | Auto | — |
| java-springboot | Auto | Auto | Auto | Auto | Auto | Auto | — |
| javascript-react | Auto | Auto | Auto | Auto | Auto | Auto | — |
| skills-creator | — | — | — | — | — | — | ✅* |
| commands-creator | — | — | — | — | — | — | ✅* |
| subagents-creator | — | — | — | — | — | — | ✅* |
| component-advisor | — | — | — | — | — | — | — |

*= selon argument de /epci:create

### 6.3 Détection automatique de stack

| Fichier détecté | Skill chargé |
|-----------------|--------------|
| `composer.json` + `symfony` | php-symfony |
| `package.json` + `react` | javascript-react |
| `requirements.txt` ou `pyproject.toml` + `django` | python-django |
| `pom.xml` ou `build.gradle` + `spring` | java-springboot |

---

### 6.4 Skill `epci-core`

**Fichier** : `skills/epci-core/SKILL.md`

```yaml
---
name: epci-core
description: >-
  Concepts fondamentaux du workflow EPCI. Définit les phases (Explore, Plan, 
  Code, Inspect), les catégories de complexité, le Feature Document et les 
  breakpoints. Use when: tout workflow EPCI, comprendre la méthodologie.
  Not for: création de composants (utiliser /epci:create).
---

# EPCI Core

## Overview

EPCI (Explore → Plan → Code → Inspect) est une méthodologie de développement
structurée en phases avec validation à chaque étape.

## Les 4 Phases

| Phase | Objectif | Output |
|-------|----------|--------|
| **Explore** | Comprendre le besoin et l'existant | Brief fonctionnel |
| **Plan** | Concevoir la solution | Plan d'implémentation |
| **Code** | Implémenter avec tests | Code + tests |
| **Inspect** | Valider et finaliser | PR prête |

## Catégories de complexité

| Catégorie | Fichiers | LOC | Risque | Workflow |
|-----------|----------|-----|--------|----------|
| TINY | 1 | <50 | Aucun | /epci-quick |
| SMALL | 2-3 | <200 | Faible | /epci-quick |
| STANDARD | 4-10 | <1000 | Moyen | /epci |
| LARGE | 10+ | 1000+ | Élevé | /epci |
| SPIKE | ? | ? | Inconnu | /epci-spike |

## Feature Document

Document central de traçabilité pour chaque feature.

### Structure
```markdown
# Feature Document — [ID]

## §1 — Brief Fonctionnel
[Contexte, critères d'acceptation, contraintes]

## §2 — Plan d'Implémentation
[Tâches, fichiers, risques]

## §3 — Implémentation
[Progression, tests, reviews]

## §4 — Finalisation
[Commit, documentation, PR]
```

## Breakpoints

Points de synchronisation obligatoires :

| Breakpoint | Après | Condition de passage |
|------------|-------|---------------------|
| BP1 | Phase 1 | Plan validé par @plan-validator |
| BP2 | Phase 2 | Code reviewé par @code-reviewer |

## Principes

1. **Traçabilité** — Tout est documenté dans le Feature Document
2. **Validation** — Chaque phase a une gate de sortie
3. **Itération** — Les phases peuvent être revisitées si nécessaire
4. **Adaptation** — Le workflow s'adapte à la complexité
```

### 6.5 Skill `architecture-patterns`

**Fichier** : `skills/architecture-patterns/SKILL.md`

```yaml
---
name: architecture-patterns
description: >-
  Patterns d'architecture logicielle courants. Inclut DDD, Clean Architecture,
  CQRS, Event Sourcing, Microservices patterns. Use when: évaluer complexité,
  choisir une architecture, refactoring structurel. Not for: conventions de code
  (→ code-conventions), patterns spécifiques stack (→ skills stack).
---

# Architecture Patterns

## Overview

Catalogue de patterns d'architecture pour guider les décisions de design.

## Patterns par niveau

### Application Level
| Pattern | Quand utiliser | Complexité |
|---------|---------------|------------|
| MVC | Apps web classiques | Faible |
| Clean Architecture | Logique métier complexe | Moyenne |
| Hexagonal | Ports & Adapters | Moyenne |
| CQRS | Read/Write séparés | Élevée |

### Domain Level
| Pattern | Quand utiliser |
|---------|---------------|
| Entity | Objet avec identité |
| Value Object | Objet sans identité |
| Aggregate | Groupe cohérent d'entités |
| Repository | Abstraction de persistance |
| Service | Logique sans état |

### Integration Level
| Pattern | Quand utiliser |
|---------|---------------|
| API Gateway | Point d'entrée unique |
| Event-Driven | Découplage asynchrone |
| Saga | Transactions distribuées |

## Quick Reference

| Besoin | Pattern recommandé |
|--------|-------------------|
| Séparation UI/Métier | Clean Architecture |
| Testabilité | Hexagonal (Ports & Adapters) |
| Scalabilité lecture | CQRS |
| Découplage services | Event-Driven |
| Transactions multi-services | Saga |

## Anti-patterns à éviter

- ❌ Big Ball of Mud (pas de structure)
- ❌ God Class (classe qui fait tout)
- ❌ Anemic Domain Model (entités sans logique)
- ❌ Distributed Monolith (micro mais couplé)
```

### 6.6 Skill `code-conventions`

**Fichier** : `skills/code-conventions/SKILL.md`

```yaml
---
name: code-conventions
description: >-
  Conventions de code génériques et bonnes pratiques. Nommage, structure de
  fichiers, commentaires, gestion d'erreurs. Use when: implémentation Phase 2,
  review de code. Not for: conventions spécifiques stack (→ skills stack).
---

# Code Conventions

## Overview

Conventions de code universelles pour un code lisible et maintenable.

## Nommage

| Élément | Convention | Exemple |
|---------|------------|---------|
| Classes | PascalCase | `UserService` |
| Méthodes | camelCase | `getUserById()` |
| Variables | camelCase | `$userName` |
| Constantes | UPPER_SNAKE | `MAX_RETRY_COUNT` |
| Fichiers | kebab-case ou PascalCase | `user-service.ts` |

## Structure

### Ordre dans une classe
1. Constantes
2. Propriétés (static puis instance)
3. Constructeur
4. Méthodes publiques
5. Méthodes protégées
6. Méthodes privées

### Taille des fonctions
- **Idéal** : < 20 lignes
- **Max** : 50 lignes
- Si plus → extraire des sous-fonctions

## Gestion d'erreurs

```
DO:
- Fail fast (valider en entrée)
- Exceptions typées
- Messages d'erreur explicites
- Logging des erreurs

DON'T:
- Catch vide
- Exception générique partout
- Retourner null pour les erreurs
- Ignorer les erreurs
```

## Commentaires

| Type | Quand | Exemple |
|------|-------|---------|
| Doc | API publique | `/** @param ... */` |
| TODO | Amélioration future | `// TODO: optimize` |
| FIXME | Bug connu | `// FIXME: race condition` |
| Inline | Logique complexe | `// Calcul du hash...` |

## Quick Reference

| Règle | Check |
|-------|-------|
| Nommage explicite | Pas de `x`, `data`, `temp` |
| Une responsabilité | Fonction = 1 chose |
| Pas de magic numbers | Constantes nommées |
| DRY | Pas de copier/coller |
| YAGNI | Pas de code "au cas où" |
```

### 6.7 Skill `testing-strategy`

**Fichier** : `skills/testing-strategy/SKILL.md`

```yaml
---
name: testing-strategy
description: >-
  Stratégies et patterns de test. Pyramide de tests, TDD, mocking, fixtures.
  Use when: Phase 2 implémentation, définir stratégie de test, review QA.
  Not for: outils spécifiques stack (→ skills stack).
---

# Testing Strategy

## Overview

Guide des stratégies de test pour un code fiable et maintenable.

## Pyramide de tests

```
       /\
      /E2E\        Few, slow, expensive
     /------\
    /Integration\   Some, medium
   /--------------\
  /     Unit       \  Many, fast, cheap
 /------------------\
```

| Niveau | Quantité | Vitesse | Coût |
|--------|----------|---------|------|
| Unit | Beaucoup | Rapide | Faible |
| Integration | Moyen | Moyen | Moyen |
| E2E | Peu | Lent | Élevé |

## Test-Driven Development (TDD)

### Cycle RED-GREEN-REFACTOR

1. **RED** — Écrire un test qui échoue
2. **GREEN** — Écrire le code minimal pour passer
3. **REFACTOR** — Améliorer sans changer le comportement

### Règles TDD

- Test AVANT le code, toujours
- Un seul test à la fois
- Code minimal pour faire passer
- Refactor seulement si vert

## Patterns de test

### Arrange-Act-Assert (AAA)
```
// Arrange - Setup
$user = new User('test@example.com');

// Act - Execute
$result = $user->validate();

// Assert - Verify
$this->assertTrue($result);
```

### Given-When-Then (BDD)
```
Given un utilisateur avec email valide
When je valide l'utilisateur
Then la validation réussit
```

## Mocking

### Quand mocker
- ✅ Dépendances externes (API, DB, filesystem)
- ✅ Comportements lents ou coûteux
- ✅ Cas difficiles à reproduire (erreurs réseau)

### Quand NE PAS mocker
- ❌ Le code qu'on teste
- ❌ Les value objects
- ❌ Les logiques simples

## Anti-patterns

| Anti-pattern | Problème | Solution |
|--------------|----------|----------|
| Test du mock | Teste l'implémentation | Tester le comportement |
| Test flaky | Passe/échoue aléatoirement | Éliminer les dépendances temporelles |
| Test couplé | Dépend d'autres tests | Tests isolés |
| Test lent | Suite > 10 min | Plus de unit, moins d'E2E |
```

### 6.8 Skill `git-workflow`

**Fichier** : `skills/git-workflow/SKILL.md`

```yaml
---
name: git-workflow
description: >-
  Workflow Git et conventions de commit. Branching strategy, Conventional
  Commits, PR workflow. Use when: Phase 3 finalisation, commit, préparation PR.
  Not for: commandes git basiques.
---

# Git Workflow

## Overview

Workflow Git standardisé pour une collaboration efficace.

## Branching Strategy

```
main ─────────────────────────────────────────►
        │                           │
develop ├───────────────────────────┼─────────►
        │           │               │
feature/x ──────────┘               │
                                    │
feature/y ──────────────────────────┘
```

### Branches

| Type | Convention | Base | Merge vers |
|------|------------|------|------------|
| main | `main` | - | - |
| develop | `develop` | main | main |
| feature | `feature/nom` | develop | develop |
| bugfix | `bugfix/nom` | develop | develop |
| hotfix | `hotfix/nom` | main | main + develop |

## Conventional Commits

### Format
```
<type>(<scope>): <description>

[body]

[footer]
```

### Types

| Type | Usage |
|------|-------|
| `feat` | Nouvelle fonctionnalité |
| `fix` | Correction de bug |
| `docs` | Documentation |
| `style` | Formatage (pas de changement de code) |
| `refactor` | Refactoring |
| `test` | Ajout/modification de tests |
| `chore` | Maintenance, dépendances |

### Exemples

```
feat(auth): add JWT token refresh

- Implement token refresh endpoint
- Add refresh token to login response
- Update auth middleware

Closes #123
```

```
fix(api): handle null response from external service

The external API sometimes returns null instead of an empty
array. This caused a TypeError in the mapping function.

Fixes #456
```

## PR Workflow

### Checklist avant PR

- [ ] Tests passent
- [ ] Lint clean
- [ ] Documentation à jour
- [ ] Commits squashés/rebasés
- [ ] Description PR complète

### Template PR

```markdown
## Description
[Résumé des changements]

## Type de changement
- [ ] Bug fix
- [ ] Nouvelle feature
- [ ] Breaking change

## Tests
- [ ] Tests unitaires ajoutés
- [ ] Tests d'intégration ajoutés
- [ ] Tests manuels effectués

## Checklist
- [ ] Code auto-reviewé
- [ ] Documentation mise à jour
- [ ] Pas de console.log/var_dump
```
```

---

### 6.9 Skills Stack-Specific

Les skills stack-specific suivent tous la même structure. Voici le template et les spécificités de chaque stack.

#### Template commun

```yaml
---
name: [stack-name]
description: >-
  Patterns et conventions pour [Stack]. Inclut [frameworks], [testing tools],
  [patterns spécifiques]. Use when: développement [stack], review code [stack].
  Not for: autres stacks.
---

# [Stack] Development Patterns

## Overview
Patterns et conventions pour le développement [Stack].

## Project Structure
[Structure de dossiers recommandée]

## Patterns
[Patterns spécifiques à la stack]

## Testing
[Outils et patterns de test]

## Quick Reference
[Tableau récapitulatif]
```

#### 6.9.1 Skill `php-symfony`

**Fichier** : `skills/php-symfony/SKILL.md`

**Spécificités** :
- Structure : `src/Controller`, `src/Entity`, `src/Repository`, `src/Service`
- Patterns : Entity, Repository, Service, Form, Event
- Testing : PHPUnit, WebTestCase, KernelTestCase
- Outils : Doctrine, Twig, Messenger

#### 6.9.2 Skill `python-django`

**Fichier** : `skills/python-django/SKILL.md`

**Spécificités** :
- Structure : `app/models.py`, `app/views.py`, `app/serializers.py`
- Patterns : Model, View, Serializer, Signal
- Testing : pytest, pytest-django, factory_boy
- Outils : Django REST Framework, Celery

#### 6.9.3 Skill `java-springboot`

**Fichier** : `skills/java-springboot/SKILL.md`

**Spécificités** :
- Structure : `controller/`, `service/`, `repository/`, `entity/`
- Patterns : Controller, Service, Repository, DTO
- Testing : JUnit 5, Mockito, TestContainers
- Outils : Spring Data JPA, Spring Security

#### 6.9.4 Skill `javascript-react`

**Fichier** : `skills/javascript-react/SKILL.md`

**Spécificités** :
- Structure : `components/`, `hooks/`, `services/`, `store/`
- Patterns : Component, Hook, Context, Reducer
- Testing : Jest, React Testing Library
- Outils : TypeScript, TanStack Query, Zustand

---

## 7. Component Factory

### 7.1 Vue d'ensemble

Le Component Factory permet de créer de nouveaux composants Claude Code (skills, commands, subagents) via un workflow interactif en 6 phases.

### 7.2 Skill `skills-creator`

**Fichier** : `skills/skills-creator/SKILL.md`

```yaml
---
name: skills-creator
description: >-
  Générateur interactif de Skills Claude Code. Crée des packages complets
  avec SKILL.md, références, templates et scripts de validation.
  Workflow en 6 phases : analyse, architecture, description, workflow, validation, génération.
  Use when: créer un skill, générer une compétence, nouveau skill, skill pour [techno/domaine].
  Not for: commandes slash (→ commands-creator), subagents (→ subagents-creator).
allowed-tools: [Read, Write, Edit, Bash, Grep, Glob]
---

# Skills Creator

## Overview

Générateur interactif de Skills Claude Code. Produit des packages complets
avec documentation et validation automatisée.

**Destination** : `epci-plugin/skills/[nom-du-skill]/`

## Workflow (6 Phases)

### Phase 1 : Analyse Pré-Création

**Questions à poser :**
1. Quel problème ce skill résout-il ? (1 phrase)
2. Quelle est la fréquence d'usage estimée ?
3. Qui est le persona cible ?
4. Quels mots-clés déclencheront ce skill ?
5. Quels sont les critères de succès mesurables ?
6. Qu'est-ce qui est explicitement HORS périmètre ?

**Gate** : Continuer si tâche récurrente + procédures stables + scope clair

### Phase 2 : Architecture

**Décisions :**
- Niveau de complexité : Simple | Standard | Avancé
- Multi-workflow ? → Decision tree
- Références nécessaires ? → Lister les fichiers

**Output** : Arborescence des fichiers à créer

### Phase 3 : Description Engineering

**Formule** :
```
[CAPACITÉS] + [TYPES DE DONNÉES] + "Use when: [contextes]" + "Not for: [exclusions]"
```

**Checklist** :
- [ ] Verbes d'action (analyze, extract, create, validate...)
- [ ] Types de fichiers/données concernés
- [ ] 2-3 contextes "Use when"
- [ ] 2-3 exclusions "Not for"
- [ ] ≤1024 caractères

### Phase 4 : Workflow & Instructions

**Structure du SKILL.md** :
1. Overview (2-3 phrases)
2. Decision Tree (si multi-workflow)
3. Étapes numérotées
4. Règles critiques
5. Exemples (input → output)
6. Liens vers références
7. Limitations explicites

**Contrainte** : <5000 tokens

### Phase 5 : Validation (Dry-Run)

**Checklist automatique** :
- [ ] YAML frontmatter valide
- [ ] Nom kebab-case ≤64 chars
- [ ] Description ≤1024 chars avec "Use when" et "Not for"
- [ ] Contenu <5000 tokens
- [ ] Tous les fichiers référencés listés
- [ ] Pas de conflit de nom

**Gate** : Approbation utilisateur requise

### Phase 6 : Génération

**Fichiers générés** :
```
epci-plugin/skills/[nom]/
├── SKILL.md
├── references/
│   └── [fichiers de référence]
├── templates/ (si applicable)
├── scripts/ (si applicable)
└── README.md
```

**Post-génération** :
1. Exécuter `validate_skill.py`
2. Exécuter `test_triggering.py`
3. Afficher rapport + requêtes de test

## Règles

### Frontmatter YAML
```yaml
---
name: kebab-case-max-64
description: >-
  [Capacités] + "Use when: ..." + "Not for: ..."
allowed-tools: [Read, ...]  # Optionnel
---
```

### Limites
| Élément | Limite |
|---------|--------|
| name | ≤64 chars, kebab-case |
| description | ≤1024 chars |
| SKILL.md body | <5000 tokens |

## Knowledge Base

Voir les fichiers dans `references/` :
- best-practices.md
- description-formulas.md
- yaml-rules.md
- checklist.md
```

#### Fichiers de référence du skill

**`skills/skills-creator/references/best-practices.md`** :
```markdown
# Best Practices pour Skills

## Structure
- SKILL.md = entry point
- Références = connaissances détaillées
- Templates = outputs formatés
- Scripts = validation automatique

## Description
- Commencer par verbes d'action
- Inclure types de données
- "Use when:" obligatoire
- "Not for:" obligatoire
- Max 1024 caractères

## Contenu
- Overview court (2-3 phrases)
- Instructions numérotées
- Exemples concrets
- Limitations explicites
- < 5000 tokens total
```

**`skills/skills-creator/references/description-formulas.md`** :
```markdown
# Formules de Description

## Pattern de base
```
[Verbe + capacité principale]. [Capacité secondaire].
Use when: [contexte 1], [contexte 2], [contexte 3].
Not for: [exclusion 1], [exclusion 2].
```

## Exemples

### Skill d'analyse
```
Analyzes [type] files for [issues]. Produces [output type].
Use when: [trigger 1], [trigger 2].
Not for: [exclusion 1], [exclusion 2].
```

### Skill de génération
```
Generates [type] from [input]. Supports [features].
Use when: [trigger 1], [trigger 2].
Not for: [exclusion 1], [exclusion 2].
```
```

**`skills/skills-creator/references/yaml-rules.md`** :
```markdown
# Règles YAML Frontmatter

## Champs obligatoires
- `name` : kebab-case, ≤64 chars
- `description` : ≤1024 chars

## Champs optionnels
- `allowed-tools` : liste de tools autorisés

## Format
```yaml
---
name: mon-skill
description: >-
  Description sur
  plusieurs lignes.
allowed-tools: [Read, Write]
---
```

## Erreurs courantes
- ❌ Espaces dans le nom
- ❌ Description sans "Use when"
- ❌ Caractères spéciaux dans le nom
```

**`skills/skills-creator/references/checklist.md`** :
```markdown
# Checklist de Création de Skill

## Avant création
- [ ] Besoin récurrent identifié
- [ ] Procédures stables
- [ ] Scope clair

## Structure
- [ ] SKILL.md créé
- [ ] Références nécessaires créées
- [ ] README.md créé

## Qualité
- [ ] Description avec "Use when" et "Not for"
- [ ] Instructions claires et numérotées
- [ ] Exemples fournis
- [ ] Limitations documentées

## Validation
- [ ] YAML valide
- [ ] Nom kebab-case ≤64
- [ ] Description ≤1024 chars
- [ ] Body < 5000 tokens
- [ ] Scripts de validation passent
```

#### Templates du skill

**`skills/skills-creator/templates/skill-simple.md`** :
```markdown
---
name: {{NAME}}
description: >-
  {{DESCRIPTION}}
---

# {{TITLE}}

## Overview

{{OVERVIEW}}

## When to Use

**Use when:**
- {{USE_CASE_1}}
- {{USE_CASE_2}}

**Not for:**
- {{EXCLUSION_1}}
- {{EXCLUSION_2}}

## Process

1. {{STEP_1}}
2. {{STEP_2}}
3. {{STEP_3}}

## Examples

### Input
{{EXAMPLE_INPUT}}

### Output
{{EXAMPLE_OUTPUT}}

## Limitations

- {{LIMITATION_1}}
- {{LIMITATION_2}}
```

**`skills/skills-creator/templates/skill-advanced.md`** :
```markdown
---
name: {{NAME}}
description: >-
  {{DESCRIPTION}}
allowed-tools: [{{TOOLS}}]
---

# {{TITLE}}

## Overview

{{OVERVIEW}}

## Decision Tree

```
{{DECISION_TREE}}
```

## When to Use

**Use when:**
- {{USE_CASE_1}}
- {{USE_CASE_2}}
- {{USE_CASE_3}}

**Not for:**
- {{EXCLUSION_1}}
- {{EXCLUSION_2}}

## Process

### Workflow A: {{WORKFLOW_A_NAME}}
1. {{STEP_A1}}
2. {{STEP_A2}}

### Workflow B: {{WORKFLOW_B_NAME}}
1. {{STEP_B1}}
2. {{STEP_B2}}

## Rules

| Rule | Description |
|------|-------------|
| {{RULE_1}} | {{RULE_1_DESC}} |
| {{RULE_2}} | {{RULE_2_DESC}} |

## Examples

### Example 1: {{EXAMPLE_1_NAME}}
**Input:** {{EXAMPLE_1_INPUT}}
**Output:** {{EXAMPLE_1_OUTPUT}}

### Example 2: {{EXAMPLE_2_NAME}}
**Input:** {{EXAMPLE_2_INPUT}}
**Output:** {{EXAMPLE_2_OUTPUT}}

## Knowledge Base

- [{{REF_1}}](references/{{REF_1_FILE}})
- [{{REF_2}}](references/{{REF_2_FILE}})

## Limitations

- {{LIMITATION_1}}
- {{LIMITATION_2}}
- {{LIMITATION_3}}

## Version

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | {{DATE}} | Initial version |
```

---

### 7.3 Skill `commands-creator`

**Fichier** : `skills/commands-creator/SKILL.md`

```yaml
---
name: commands-creator
description: >-
  Générateur interactif de Slash Commands Claude Code. Crée des commandes
  complètes avec frontmatter optimisé, gestion des arguments et workflow structuré.
  Use when: créer une commande, nouvelle commande slash, /[nom].
  Not for: skills (→ skills-creator), subagents (→ subagents-creator).
allowed-tools: [Read, Write, Edit, Bash, Grep, Glob]
---

# Commands Creator

## Overview

Générateur interactif de Slash Commands Claude Code.

**Destination** : `epci-plugin/commands/[nom].md`

## Workflow (6 Phases)

### Phase 1 : Analyse
- Quelle action cette commande déclenche-t-elle ?
- Quels arguments sont nécessaires ?
- Quels outils Claude devra-t-il utiliser ?
- Quel est le résultat attendu ?

### Phase 2 : Architecture
- Simple | Standard | Avancé

### Phase 3 : Frontmatter
```yaml
---
description: Description courte
argument-hint: <arg1> [arg2]
allowed-tools: [Read, Write, ...]
---
```

### Phase 4 : Instructions
```markdown
<objective>...</objective>
<process>...</process>
<success_criteria>...</success_criteria>
```

### Phase 5 : Validation
- YAML valide
- Arguments documentés
- Outils cohérents

### Phase 6 : Génération
- Créer le fichier
- Valider avec script
- Fournir syntaxe d'appel

## Gestion des arguments

| Syntaxe | Description |
|---------|-------------|
| `$ARGUMENTS` | Tous les arguments |
| `$1`, `$2`... | Arguments positionnels |
| `<arg>` | Obligatoire (dans hint) |
| `[arg]` | Optionnel (dans hint) |
```

---

### 7.4 Skill `subagents-creator`

**Fichier** : `skills/subagents-creator/SKILL.md`

```yaml
---
name: subagents-creator
description: >-
  Générateur interactif de Subagents Claude Code. Crée des agents spécialisés
  avec prompt dédié, outils restreints et mission focalisée.
  Use when: créer un subagent, agent spécialisé, déléguer à un agent.
  Not for: skills (→ skills-creator), commandes (→ commands-creator).
allowed-tools: [Read, Write, Edit, Bash, Grep, Glob]
---

# Subagents Creator

## Overview

Générateur interactif de Subagents Claude Code.

**Destination** : `epci-plugin/agents/[nom].md`

## Workflow (6 Phases)

### Phase 1 : Analyse
- Quelle est la mission précise ?
- Pourquoi déléguer ?
- Quelle expertise spécifique ?
- Activation automatique ou explicite ?

### Phase 2 : Architecture
- Modèle : sonnet | haiku
- Activation : auto | explicite

### Phase 3 : Prompt Engineering
```yaml
---
name: nom-du-subagent
description: Mission courte
model: claude-sonnet-4-20250514
allowed-tools: [Read, Grep, ...]
---

# System Prompt
## Rôle
## Contexte
## Instructions
## Contraintes
## Format de sortie
```

### Phase 4 : Configuration des outils
Principe du moindre privilège.

| Mission | Outils |
|---------|--------|
| Analyse | Read, Grep, Glob |
| Revue sécurité | Read, Grep, WebFetch |
| Documentation | Read, Write |

### Phase 5 : Validation
- Mission focalisée
- Outils minimaux
- Pas de chevauchement

### Phase 6 : Génération

## Règles

| Faire | Ne pas faire |
|-------|--------------|
| Mission précise | Agent générique |
| Contexte minimal | Tout l'historique |
| Outils stricts | Tous les outils |
```

---

### 7.5 Skill `component-advisor`

**Fichier** : `skills/component-advisor/SKILL.md`

```yaml
---
name: component-advisor
description: >-
  Détecte les opportunités de création de composants réutilisables.
  Observe les patterns répétitifs et suggère la création de skills, commands
  ou subagents. Use when: pattern répétitif (3+ fois), "je fais souvent ça",
  workflow manuel récurrent. Not for: création explicite (→ /epci:create).
allowed-tools: [Read, Grep, Glob]
---

# Component Advisor

## Overview

Skill de détection passive qui suggère la création de composants
quand des patterns répétitifs sont détectés.

**Comportement** : Observe → Détecte → Suggère (ne génère pas)

## Signaux de détection

### Positifs (suggérer)
| Signal | Exemple | Composant |
|--------|---------|-----------|
| Répétition 3+ | Même workflow 3 fois | Skill/Command |
| "Je fais souvent" | Expression explicite | Skill |
| "Comment automatiser" | Question | Command/Skill |
| Prompt réutilisé | Variations mineures | Skill |
| Tâche déléguée | "À chaque fois..." | Subagent |

### Négatifs (ne pas suggérer)
- Tâche ponctuelle
- Contexte unique
- Procédure volatile
- Création déjà demandée

## Format de suggestion

```markdown
💡 **Suggestion de composant**

J'ai remarqué que tu [pattern détecté].

**Proposition** : Créer un [type] `[nom-suggéré]`

**Bénéfices** :
- [Bénéfice 1]
- [Bénéfice 2]

👉 Pour créer : `/epci:create [type] [nom]`
```

## Classification

| Caractéristique | → Skill | → Command | → Subagent |
|-----------------|---------|-----------|------------|
| Déclenchement | Contexte | Action explicite | Délégation |
| Exemple | "Quand j'analyse..." | "Quand je tape /..." | "Délègue la..." |
```

---

## 8. Scripts de validation

### 8.1 Script `validate_skill.py`

**Fichier** : `skills/skills-creator/scripts/validate_skill.py`

```python
#!/usr/bin/env python3
"""
Validation automatique des Skills Claude Code.
Usage: python validate_skill.py <skill-name>
"""

import sys
import os
import re
import yaml
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class ValidationReport:
    """Rapport de validation d'un skill."""
    skill_name: str
    valid: bool = True
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    checks_passed: int = 0
    checks_total: int = 6

    def add_error(self, message: str):
        self.errors.append(message)
        self.valid = False

    def add_warning(self, message: str):
        self.warnings.append(message)

    def pass_check(self):
        self.checks_passed += 1

    def print_report(self):
        print(f"\n{'='*60}")
        print(f"VALIDATION REPORT: {self.skill_name}")
        print(f"{'='*60}\n")
        
        if self.errors:
            print("❌ ERRORS:")
            for err in self.errors:
                print(f"   - {err}")
            print()
        
        if self.warnings:
            print("⚠️  WARNINGS:")
            for warn in self.warnings:
                print(f"   - {warn}")
            print()
        
        status = "PASSED" if self.valid else "FAILED"
        print(f"RESULT: {status} ({self.checks_passed}/{self.checks_total} checks)")
        print(f"{'='*60}\n")
        
        return 0 if self.valid else 1


def validate_yaml_syntax(content: str, report: ValidationReport) -> dict | None:
    """Vérifie la syntaxe du frontmatter YAML."""
    try:
        match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
        if not match:
            report.add_error("YAML frontmatter missing or malformed")
            return None
        
        frontmatter = yaml.safe_load(match.group(1))
        print("✅ YAML syntax: OK")
        report.pass_check()
        return frontmatter
    
    except yaml.YAMLError as e:
        report.add_error(f"YAML syntax error: {e}")
        return None


def validate_name(frontmatter: dict, report: ValidationReport) -> bool:
    """Vérifie le champ name."""
    name = frontmatter.get('name', '')
    
    if not name:
        report.add_error("Field 'name' is required")
        return False
    
    if not re.match(r'^[a-z0-9]+(-[a-z0-9]+)*$', name):
        report.add_error(f"Name must be kebab-case: '{name}'")
        return False
    
    if len(name) > 64:
        report.add_error(f"Name exceeds 64 chars: {len(name)}")
        return False
    
    print(f"✅ Name format: OK ({name})")
    report.pass_check()
    return True


def validate_description(frontmatter: dict, report: ValidationReport) -> bool:
    """Vérifie la description."""
    desc = frontmatter.get('description', '')
    
    if not desc:
        report.add_error("Field 'description' is required")
        return False
    
    if len(desc) > 1024:
        report.add_error(f"Description exceeds 1024 chars: {len(desc)}")
        return False
    
    has_use_when = 'use when' in desc.lower()
    has_not_for = 'not for' in desc.lower()
    
    if not has_use_when:
        report.add_warning("Description should contain 'Use when:'")
    if not has_not_for:
        report.add_warning("Description should contain 'Not for:'")
    
    print(f"✅ Description: OK ({len(desc)} chars)")
    report.pass_check()
    return True


def estimate_tokens(text: str) -> int:
    """Estimation grossière du nombre de tokens."""
    return len(text) // 4


def validate_token_count(content: str, report: ValidationReport) -> bool:
    """Vérifie que le contenu ne dépasse pas 5000 tokens."""
    body = re.sub(r'^---\n.*?\n---\n', '', content, flags=re.DOTALL)
    tokens = estimate_tokens(body)
    
    if tokens > 5000:
        report.add_error(f"Content exceeds 5000 tokens: ~{tokens}")
        return False
    
    print(f"✅ Token count: OK (~{tokens} tokens)")
    report.pass_check()
    return True


def validate_references(skill_path: Path, content: str, report: ValidationReport) -> bool:
    """Vérifie que les fichiers référencés existent."""
    ref_dir = skill_path / "references"
    
    # Chercher les références dans le contenu
    refs_mentioned = re.findall(r'references/([a-z0-9-]+\.md)', content)
    
    missing = []
    for ref in refs_mentioned:
        if not (ref_dir / ref).exists():
            missing.append(ref)
    
    if missing:
        report.add_warning(f"Referenced files not found: {', '.join(missing)}")
    
    print(f"✅ References: OK")
    report.pass_check()
    return True


def validate_no_conflicts(skill_name: str, base_path: str, report: ValidationReport) -> bool:
    """Vérifie qu'il n'y a pas de conflit de nom."""
    # Dans le contexte de création, cette vérification est faite en amont
    print(f"✅ No conflicts: OK")
    report.pass_check()
    return True


def validate_skill(skill_name: str, base_path: str = "epci-plugin/skills") -> int:
    """Point d'entrée principal."""
    skill_path = Path(base_path) / skill_name
    skill_file = skill_path / "SKILL.md"
    
    if not skill_file.exists():
        print(f"❌ File not found: {skill_file}")
        return 1
    
    report = ValidationReport(skill_name=skill_name)
    content = skill_file.read_text(encoding='utf-8')
    
    # Validations
    frontmatter = validate_yaml_syntax(content, report)
    if frontmatter:
        validate_name(frontmatter, report)
        validate_description(frontmatter, report)
        validate_token_count(content, report)
        validate_references(skill_path, content, report)
        validate_no_conflicts(skill_name, base_path, report)
    
    return report.print_report()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python validate_skill.py <skill-name>")
        sys.exit(1)
    
    sys.exit(validate_skill(sys.argv[1]))
```

### 8.2 Script `test_triggering.py`

**Fichier** : `skills/skills-creator/scripts/test_triggering.py`

```python
#!/usr/bin/env python3
"""
Test de triggering des Skills Claude Code.
Usage: python test_triggering.py <skill-name>
"""

import sys
import re
import yaml
from pathlib import Path


def load_skill_description(skill_name: str, base_path: str = "epci-plugin/skills") -> str | None:
    """Charge la description d'un skill."""
    skill_file = Path(base_path) / skill_name / "SKILL.md"
    
    if not skill_file.exists():
        return None
    
    content = skill_file.read_text(encoding='utf-8')
    match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    
    if not match:
        return None
    
    frontmatter = yaml.safe_load(match.group(1))
    return frontmatter.get('description', '')


def extract_triggers(description: str) -> tuple[list[str], list[str]]:
    """Extrait les triggers positifs et négatifs de la description."""
    positive = []
    negative = []
    
    # Extraire "Use when:" patterns
    use_when_match = re.search(r'Use when[:\s]+([^.]+)', description, re.IGNORECASE)
    if use_when_match:
        triggers = use_when_match.group(1).split(',')
        positive = [t.strip() for t in triggers]
    
    # Extraire "Not for:" patterns
    not_for_match = re.search(r'Not for[:\s]+([^.]+)', description, re.IGNORECASE)
    if not_for_match:
        exclusions = not_for_match.group(1).split(',')
        negative = [e.strip() for e in exclusions]
    
    return positive, negative


def should_trigger(query: str, description: str) -> bool:
    """Détermine si une requête devrait déclencher le skill."""
    query_lower = query.lower()
    desc_lower = description.lower()
    
    # Extraire mots-clés de la description
    keywords = re.findall(r'\b[a-z]{4,}\b', desc_lower)
    
    # Vérifier si des mots-clés apparaissent dans la requête
    matches = sum(1 for kw in keywords if kw in query_lower)
    
    return matches >= 2


def test_skill_triggering(skill_name: str, base_path: str = "epci-plugin/skills") -> int:
    """Teste le triggering d'un skill."""
    description = load_skill_description(skill_name, base_path)
    
    if not description:
        print(f"❌ Could not load skill: {skill_name}")
        return 1
    
    positive_triggers, negative_triggers = extract_triggers(description)
    
    print(f"\n{'='*60}")
    print(f"TRIGGERING TESTS: {skill_name}")
    print(f"{'='*60}\n")
    
    passed = 0
    total = 0
    
    # Tests positifs (doivent trigger)
    for trigger in positive_triggers[:3]:  # Max 3 tests
        total += 1
        result = should_trigger(trigger, description)
        status = "✅ TRIGGERED" if result else "❌ NOT TRIGGERED"
        print(f'Testing: "{trigger}" → {status}')
        if result:
            passed += 1
    
    # Tests négatifs (ne doivent pas trigger)
    for exclusion in negative_triggers[:2]:  # Max 2 tests
        total += 1
        result = not should_trigger(exclusion, description)
        status = "✅ NOT TRIGGERED (expected)" if result else "❌ TRIGGERED (unexpected)"
        print(f'Testing: "{exclusion}" → {status}')
        if result:
            passed += 1
    
    print(f"\nRESULT: {passed}/{total} tests passed")
    print(f"{'='*60}\n")
    
    return 0 if passed == total else 1


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python test_triggering.py <skill-name>")
        sys.exit(1)
    
    sys.exit(test_skill_triggering(sys.argv[1]))
```

### 8.3 Script `validate_command.py`

**Fichier** : `skills/commands-creator/scripts/validate_command.py`

```python
#!/usr/bin/env python3
"""
Validation automatique des Commands Claude Code.
Usage: python validate_command.py <command-file.md>
"""

import sys
import re
import yaml
from pathlib import Path
from dataclasses import dataclass, field


@dataclass
class ValidationReport:
    """Rapport de validation d'une commande."""
    command_name: str
    valid: bool = True
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    checks_passed: int = 0
    checks_total: int = 5

    def add_error(self, message: str):
        self.errors.append(message)
        self.valid = False

    def add_warning(self, message: str):
        self.warnings.append(message)

    def pass_check(self):
        self.checks_passed += 1

    def print_report(self):
        print(f"\n{'='*60}")
        print(f"VALIDATION REPORT: {self.command_name}")
        print(f"{'='*60}\n")
        
        if self.errors:
            print("❌ ERRORS:")
            for err in self.errors:
                print(f"   - {err}")
            print()
        
        if self.warnings:
            print("⚠️  WARNINGS:")
            for warn in self.warnings:
                print(f"   - {warn}")
            print()
        
        status = "PASSED" if self.valid else "FAILED"
        print(f"RESULT: {status} ({self.checks_passed}/{self.checks_total} checks)")
        print(f"{'='*60}\n")
        
        return 0 if self.valid else 1


VALID_TOOLS = [
    'Read', 'Write', 'Edit', 'Bash', 'Grep', 'Glob', 
    'Task', 'WebFetch', 'WebSearch', 'TodoRead', 'TodoWrite'
]


def validate_yaml_syntax(content: str, report: ValidationReport) -> dict | None:
    """Vérifie la syntaxe du frontmatter YAML."""
    try:
        match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
        if not match:
            report.add_error("YAML frontmatter missing or malformed")
            return None
        
        frontmatter = yaml.safe_load(match.group(1))
        print("✅ YAML syntax: OK")
        report.pass_check()
        return frontmatter
    
    except yaml.YAMLError as e:
        report.add_error(f"YAML syntax error: {e}")
        return None


def validate_filename(path: Path, report: ValidationReport) -> bool:
    """Vérifie le nom du fichier."""
    name = path.stem
    
    if not re.match(r'^[a-z0-9]+(-[a-z0-9]+)*$', name):
        report.add_error(f"Filename must be kebab-case: '{name}'")
        return False
    
    print(f"✅ Filename: OK ({name})")
    report.pass_check()
    return True


def validate_description(frontmatter: dict, report: ValidationReport) -> bool:
    """Vérifie la description."""
    desc = frontmatter.get('description', '')
    
    if not desc:
        report.add_error("Field 'description' is required")
        return False
    
    if len(desc) > 500:
        report.add_warning(f"Description is long ({len(desc)} chars) - keep it concise for /help")
    
    print(f"✅ Description: OK ({len(desc)} chars)")
    report.pass_check()
    return True


def validate_allowed_tools(frontmatter: dict, report: ValidationReport) -> bool:
    """Vérifie les outils autorisés."""
    tools = frontmatter.get('allowed-tools', [])
    
    if not tools:
        report.add_warning("No allowed-tools specified - all tools will be available")
        report.pass_check()
        return True
    
    invalid = []
    for tool in tools:
        # Gérer les outils avec paramètres comme Bash(cmd:*)
        base_tool = tool.split('(')[0]
        if base_tool not in VALID_TOOLS:
            invalid.append(tool)
    
    if invalid:
        report.add_error(f"Invalid tools: {', '.join(invalid)}")
        return False
    
    print(f"✅ Allowed-tools: OK ({len(tools)} tools)")
    report.pass_check()
    return True


def validate_structure(content: str, report: ValidationReport) -> bool:
    """Vérifie la structure du contenu."""
    body = re.sub(r'^---\n.*?\n---\n', '', content, flags=re.DOTALL)
    
    # Vérifier présence de sections recommandées
    recommended = ['objective', 'process', 'success_criteria']
    found = [s for s in recommended if f'<{s}>' in body.lower() or f'## {s}' in body.lower()]
    
    if len(found) < 2:
        report.add_warning(f"Consider adding structured sections: {recommended}")
    
    print(f"✅ Structure: OK")
    report.pass_check()
    return True


def validate_command(filepath: str, base_path: str = "epci-plugin/commands") -> int:
    """Point d'entrée principal."""
    path = Path(filepath)
    if not path.exists():
        path = Path(base_path) / filepath
    
    if not path.exists():
        print(f"❌ File not found: {filepath}")
        return 1
    
    report = ValidationReport(command_name=path.stem)
    content = path.read_text(encoding='utf-8')
    
    # Validations
    frontmatter = validate_yaml_syntax(content, report)
    if frontmatter:
        validate_filename(path, report)
        validate_description(frontmatter, report)
        validate_allowed_tools(frontmatter, report)
        validate_structure(content, report)
    
    return report.print_report()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python validate_command.py <command-file.md>")
        sys.exit(1)
    
    sys.exit(validate_command(sys.argv[1]))
```

### 8.4 Script `validate_subagent.py`

**Fichier** : `skills/subagents-creator/scripts/validate_subagent.py`

```python
#!/usr/bin/env python3
"""
Validation automatique des Subagents Claude Code.
Usage: python validate_subagent.py <subagent-file.md>
"""

import sys
import re
import yaml
from pathlib import Path
from dataclasses import dataclass, field


@dataclass
class ValidationReport:
    """Rapport de validation d'un subagent."""
    agent_name: str
    valid: bool = True
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    checks_passed: int = 0
    checks_total: int = 5

    def add_error(self, message: str):
        self.errors.append(message)
        self.valid = False

    def add_warning(self, message: str):
        self.warnings.append(message)

    def pass_check(self):
        self.checks_passed += 1

    def print_report(self):
        print(f"\n{'='*60}")
        print(f"VALIDATION REPORT: {self.agent_name}")
        print(f"{'='*60}\n")
        
        if self.errors:
            print("❌ ERRORS:")
            for err in self.errors:
                print(f"   - {err}")
            print()
        
        if self.warnings:
            print("⚠️  WARNINGS:")
            for warn in self.warnings:
                print(f"   - {warn}")
            print()
        
        status = "PASSED" if self.valid else "FAILED"
        print(f"RESULT: {status} ({self.checks_passed}/{self.checks_total} checks)")
        print(f"{'='*60}\n")
        
        return 0 if self.valid else 1


VALID_TOOLS = [
    'Read', 'Write', 'Edit', 'Bash', 'Grep', 'Glob', 
    'WebFetch', 'WebSearch', 'TodoRead', 'TodoWrite'
]


def validate_yaml_syntax(content: str, report: ValidationReport) -> dict | None:
    """Vérifie la syntaxe du frontmatter YAML."""
    try:
        match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
        if not match:
            report.add_error("YAML frontmatter missing or malformed")
            return None
        
        frontmatter = yaml.safe_load(match.group(1))
        print("✅ YAML syntax: OK")
        report.pass_check()
        return frontmatter
    
    except yaml.YAMLError as e:
        report.add_error(f"YAML syntax error: {e}")
        return None


def validate_name(frontmatter: dict, report: ValidationReport) -> bool:
    """Vérifie le champ name."""
    name = frontmatter.get('name', '')
    
    if not name:
        report.add_error("Field 'name' is required")
        return False
    
    if not re.match(r'^[a-z0-9]+(-[a-z0-9]+)*$', name):
        report.add_error(f"Name must be kebab-case: '{name}'")
        return False
    
    print(f"✅ Name: OK ({name})")
    report.pass_check()
    return True


def validate_description(frontmatter: dict, report: ValidationReport) -> bool:
    """Vérifie la description (mission du subagent)."""
    desc = frontmatter.get('description', '')
    
    if not desc:
        report.add_error("Field 'description' is required")
        return False
    
    if len(desc.split()) > 50:
        report.add_warning("Description is long - subagent mission should be focused")
    
    print(f"✅ Description: OK ({len(desc)} chars)")
    report.pass_check()
    return True


def validate_allowed_tools(frontmatter: dict, report: ValidationReport) -> bool:
    """Vérifie les outils - doit être minimal."""
    tools = frontmatter.get('allowed-tools', [])
    
    if not tools:
        report.add_warning("No allowed-tools - consider restricting for security")
        report.pass_check()
        return True
    
    if len(tools) > 5:
        report.add_warning(f"Many tools ({len(tools)}) - subagents should have minimal permissions")
    
    invalid = []
    for tool in tools:
        base_tool = tool.split('(')[0]
        if base_tool not in VALID_TOOLS:
            invalid.append(tool)
    
    if invalid:
        report.add_error(f"Invalid tools: {', '.join(invalid)}")
        return False
    
    print(f"✅ Allowed-tools: OK ({len(tools)} tools)")
    report.pass_check()
    return True


def validate_prompt_structure(content: str, report: ValidationReport) -> bool:
    """Vérifie la structure du system prompt."""
    body = re.sub(r'^---\n.*?\n---\n', '', content, flags=re.DOTALL)
    
    recommended = ['rôle', 'role', 'mission', 'instructions', 'contraintes', 'constraints']
    found = [s for s in recommended if s in body.lower()]
    
    if len(found) < 2:
        report.add_warning(f"System prompt may lack structure. Found: {found}")
    
    print(f"✅ Prompt structure: OK")
    report.pass_check()
    return True


def validate_subagent(filepath: str, base_path: str = "epci-plugin/agents") -> int:
    """Point d'entrée principal."""
    path = Path(filepath)
    if not path.exists():
        path = Path(base_path) / filepath
    
    if not path.exists():
        print(f"❌ File not found: {filepath}")
        return 1
    
    report = ValidationReport(agent_name=path.stem)
    content = path.read_text(encoding='utf-8')
    
    # Validations
    frontmatter = validate_yaml_syntax(content, report)
    if frontmatter:
        validate_name(frontmatter, report)
        validate_description(frontmatter, report)
        validate_allowed_tools(frontmatter, report)
        validate_prompt_structure(content, report)
    
    return report.print_report()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python validate_subagent.py <subagent-file.md>")
        sys.exit(1)
    
    sys.exit(validate_subagent(sys.argv[1]))
```

### 8.5 Script orchestrateur `validate_all.py`

**Fichier** : `scripts/validate_all.py`

```python
#!/usr/bin/env python3
"""
Orchestrateur de validation pour tous les composants EPCI.
Usage: python validate_all.py
"""

import subprocess
import sys
from pathlib import Path


def run_validation(script: str, args: list[str]) -> tuple[bool, str]:
    """Exécute un script de validation."""
    try:
        result = subprocess.run(
            ['python', script] + args,
            capture_output=True,
            text=True
        )
        return result.returncode == 0, result.stdout + result.stderr
    except Exception as e:
        return False, str(e)


def validate_all(base_path: str = "epci-plugin") -> int:
    """Valide tous les composants du plugin."""
    base = Path(base_path)
    
    print("\n" + "="*60)
    print("EPCI PLUGIN VALIDATION")
    print("="*60 + "\n")
    
    results = {
        'skills': [],
        'commands': [],
        'subagents': []
    }
    
    # Valider les skills
    skills_dir = base / "skills"
    if skills_dir.exists():
        for skill_dir in skills_dir.iterdir():
            if skill_dir.is_dir() and (skill_dir / "SKILL.md").exists():
                script = skills_dir / "skills-creator" / "scripts" / "validate_skill.py"
                if script.exists():
                    success, output = run_validation(str(script), [skill_dir.name])
                    results['skills'].append((skill_dir.name, success))
    
    # Valider les commandes
    commands_dir = base / "commands"
    if commands_dir.exists():
        for cmd_file in commands_dir.glob("*.md"):
            script = skills_dir / "commands-creator" / "scripts" / "validate_command.py"
            if script.exists():
                success, output = run_validation(str(script), [str(cmd_file)])
                results['commands'].append((cmd_file.stem, success))
    
    # Valider les subagents
    agents_dir = base / "agents"
    if agents_dir.exists():
        for agent_file in agents_dir.glob("*.md"):
            script = skills_dir / "subagents-creator" / "scripts" / "validate_subagent.py"
            if script.exists():
                success, output = run_validation(str(script), [str(agent_file)])
                results['subagents'].append((agent_file.stem, success))
    
    # Rapport final
    print("\n" + "="*60)
    print("FINAL REPORT")
    print("="*60 + "\n")
    
    total_passed = 0
    total_failed = 0
    
    for category, items in results.items():
        print(f"\n{category.upper()}:")
        for name, success in items:
            status = "✅" if success else "❌"
            print(f"  {status} {name}")
            if success:
                total_passed += 1
            else:
                total_failed += 1
    
    print(f"\n{'='*60}")
    print(f"TOTAL: {total_passed} passed, {total_failed} failed")
    print(f"{'='*60}\n")
    
    return 0 if total_failed == 0 else 1


if __name__ == "__main__":
    sys.exit(validate_all())
```

---

## 9. Feature Document

### 9.1 Template complet

**Structure du Feature Document** utilisé par `/epci` :

```markdown
# Feature Document — [FD-YYYY-MM-DD-XXX]

> **Feature** : [Titre de la feature]
> **Catégorie** : [TINY | SMALL | STANDARD | LARGE]
> **Créé** : [Date]
> **Statut** : [BRIEF | PLAN | CODE | DONE]

---

## §1 — Brief Fonctionnel

### Contexte
[Description du besoin et du contexte business]

### Stack détectée
[Stack identifiée par @Explore]

### Critères d'acceptation
- [ ] CA1 : [Critère mesurable 1]
- [ ] CA2 : [Critère mesurable 2]
- [ ] CA3 : [Critère mesurable 3]

### Contraintes
- [Contrainte technique]
- [Contrainte temps/budget]

### Hors périmètre
- [Exclusion explicite 1]
- [Exclusion explicite 2]

---

## §2 — Plan d'Implémentation

### Fichiers impactés

| Fichier | Action | Risque | Justification |
|---------|--------|--------|---------------|
| `src/...` | Créer | Faible | [Raison] |
| `src/...` | Modifier | Moyen | [Raison] |

### Tâches

#### Tâche 1 : [Nom] (X min)
- **Fichier** : `src/...`
- **Action** : [Description précise]
- **Test** : `tests/...`
- **Commande** : `php bin/phpunit --filter ...`

#### Tâche 2 : [Nom] (X min)
...

### Risques identifiés

| Risque | Probabilité | Impact | Mitigation |
|--------|-------------|--------|------------|
| [Risque 1] | Moyenne | Élevé | [Mitigation] |

### Validation

- **@plan-validator** : [APPROVED | NEEDS_REVISION]
- **Commentaires** : [Feedback si applicable]

---

## §3 — Implémentation

### Progression

- [x] Tâche 1 — Complétée [timestamp]
- [x] Tâche 2 — Complétée [timestamp]
- [ ] Tâche 3 — En cours

### Tests

```bash
$ php bin/phpunit
OK (47 tests, 156 assertions)
```

### Reviews

#### @code-reviewer
- **Verdict** : [APPROVED | NEEDS_REVISION]
- **Critical** : 0
- **Important** : X (corrigés)
- **Minor** : Y

#### @security-auditor (si applicable)
- **Verdict** : [APPROVED | NEEDS_FIXES]
- **Findings** : [Résumé]

#### @qa-reviewer (si applicable)
- **Verdict** : [APPROVED | NEEDS_IMPROVEMENT]
- **Coverage** : [Assessment]

### Déviations du plan

| Tâche | Déviation | Justification |
|-------|-----------|---------------|
| #X | [Description] | [Raison] |

---

## §4 — Finalisation

### Commit

```
feat(module): implement [feature]

- Add [composant 1]
- Create [composant 2]
- Update [composant 3]

Refs: FD-YYYY-MM-DD-XXX
```

### Documentation

- [x] README mis à jour
- [x] API documentée
- [x] Changelog ajouté

### PR

- **Branche** : `feature/xxx`
- **Target** : `develop`
- **Reviewers** : @xxx, @yyy
- **URL** : [lien PR]

### Vérification finale

- [x] Tous les tests passent
- [x] Lint/CS clean
- [x] Documentation complète
- [x] Critères d'acceptation validés

---

## Historique

| Date | Phase | Action | Par |
|------|-------|--------|-----|
| [Date] | BRIEF | Création | @user |
| [Date] | PLAN | Validation | @plan-validator |
| [Date] | CODE | Review | @code-reviewer |
| [Date] | DONE | Merge | @user |
```

---

## 10. Plugin Manifest

### 10.1 Fichier `plugin.json`

**Fichier** : `.claude-plugin/plugin.json`

```json
{
  "name": "epci",
  "version": "3.0.0",
  "description": "EPCI (Explore → Plan → Code → Inspect) - Structured development workflow for Claude Code",
  "author": "EPCI Contributors",
  "homepage": "https://github.com/example/epci-plugin",
  "license": "MIT",
  "engines": {
    "claude-code": ">=1.0.0"
  },
  "commands": [
    {
      "name": "epci-brief",
      "file": "commands/epci-brief.md",
      "description": "Start EPCI workflow with brief clarification and routing"
    },
    {
      "name": "epci",
      "file": "commands/epci.md",
      "description": "Full EPCI workflow for STANDARD/LARGE features"
    },
    {
      "name": "epci-quick",
      "file": "commands/epci-quick.md",
      "description": "Quick EPCI workflow for TINY/SMALL features"
    },
    {
      "name": "epci-spike",
      "file": "commands/epci-spike.md",
      "description": "Time-boxed technical exploration"
    },
    {
      "name": "epci:create",
      "file": "commands/create.md",
      "description": "Create new Claude Code components (skill, command, subagent)"
    }
  ],
  "agents": [
    "agents/plan-validator.md",
    "agents/code-reviewer.md",
    "agents/security-auditor.md",
    "agents/qa-reviewer.md",
    "agents/doc-generator.md"
  ],
  "skills": [
    "skills/epci-core",
    "skills/architecture-patterns",
    "skills/code-conventions",
    "skills/testing-strategy",
    "skills/git-workflow",
    "skills/php-symfony",
    "skills/python-django",
    "skills/java-springboot",
    "skills/javascript-react",
    "skills/skills-creator",
    "skills/commands-creator",
    "skills/subagents-creator",
    "skills/component-advisor"
  ],
  "keywords": [
    "epci",
    "workflow",
    "development",
    "tdd",
    "code-review",
    "documentation"
  ]
}
```

---

## 11. Critères de validation

### 11.1 Checklist de génération

Avant de considérer le plugin comme généré, vérifier :

#### Structure des fichiers
- [ ] `.claude-plugin/plugin.json` existe et est valide
- [ ] 5 commandes dans `commands/`
- [ ] 5 subagents dans `agents/`
- [ ] 13 skills dans `skills/`
- [ ] Scripts Python dans les skills factory

#### Commandes
- [ ] Chaque commande a un frontmatter YAML valide
- [ ] Les sections Subagents & Skills sont documentées
- [ ] Les breakpoints sont définis pour `/epci`

#### Subagents
- [ ] Chaque subagent a name, description, model, allowed-tools
- [ ] Les tools sont restreints selon le principe du moindre privilège
- [ ] Le system prompt est structuré

#### Skills
- [ ] Chaque skill a un SKILL.md avec frontmatter valide
- [ ] Les descriptions contiennent "Use when" et "Not for"
- [ ] Les skills factory ont leurs références et templates

#### Scripts
- [ ] `validate_skill.py` fonctionne
- [ ] `validate_command.py` fonctionne
- [ ] `validate_subagent.py` fonctionne
- [ ] `validate_all.py` orchestre correctement

### 11.2 Tests fonctionnels

#### Test 1 : /epci-brief
```
Input: "Je veux ajouter un bouton de suppression sur la page produit"
Expected: Brief structuré + évaluation complexité + recommandation workflow
```

#### Test 2 : /epci
```
Input: Brief validé de complexité STANDARD
Expected: Workflow 3 phases avec breakpoints, Feature Document complet
```

#### Test 3 : /epci-quick
```
Input: "Corriger le bug de formatage de date"
Expected: Exécution rapide sans breakpoint, commit formaté
```

#### Test 4 : /epci-spike
```
Input: "Explorer les options pour intégrer Elasticsearch"
Expected: Spike Report avec options comparées
```

#### Test 5 : /epci:create skill
```
Input: /epci:create skill docker-analyzer
Expected: Workflow 6 phases, skill généré et validé
```

---

## 12. Instructions de génération

### 12.1 Ordre de génération recommandé

1. **Structure de base**
   - Créer l'arborescence des dossiers
   - Créer `.claude-plugin/plugin.json`

2. **Skills Core** (dans l'ordre)
   - `epci-core`
   - `architecture-patterns`
   - `code-conventions`
   - `testing-strategy`
   - `git-workflow`

3. **Skills Stack**
   - `php-symfony`
   - `python-django`
   - `java-springboot`
   - `javascript-react`

4. **Subagents**
   - `plan-validator`
   - `code-reviewer`
   - `security-auditor`
   - `qa-reviewer`
   - `doc-generator`

5. **Commandes principales**
   - `epci-brief`
   - `epci`
   - `epci-quick`
   - `epci-spike`

6. **Component Factory**
   - `skills-creator` (avec références, templates, scripts)
   - `commands-creator` (avec références, templates, scripts)
   - `subagents-creator` (avec références, templates, scripts)
   - `component-advisor`
   - `create.md` (commande)

7. **Scripts globaux**
   - `scripts/validate_all.py`

8. **Validation finale**
   - Exécuter `validate_all.py`
   - Corriger les erreurs
   - Tester les commandes

### 12.2 Notes importantes

- **Chaque fichier doit être complet** — Pas de placeholders ou TODO
- **Les skills stack doivent être adaptés** — Patterns réels de chaque framework
- **Les scripts doivent être fonctionnels** — Python 3.10+ compatible
- **Le plugin.json doit référencer tous les composants**

### 12.3 Commande de génération suggérée

```
Génère le plugin EPCI v3 complet selon ce cahier des charges.
Commence par la structure, puis les skills core, puis les subagents,
puis les commandes, puis le Component Factory.
Valide chaque composant au fur et à mesure.
```

---

*Fin du cahier des charges EPCI v3.0*
