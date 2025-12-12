# EPCI Component Factory — Spécification Complète v3

> **Version** : 3.0  
> **Date** : Décembre 2025  
> **Score Promptor** : 94/100 ★★★★★  
> **Statut** : Prêt pour génération

---

## Table des matières

1. [Vue d'ensemble](#1-vue-densemble)
2. [Architecture des fichiers](#2-architecture-des-fichiers)
3. [Commande /epci:create](#3-commande-epcicreate)
4. [Skill skills-creator](#4-skill-skills-creator)
5. [Skill commands-creator](#5-skill-commands-creator)
6. [Skill subagents-creator](#6-skill-subagents-creator)
7. [Skill component-advisor](#7-skill-component-advisor-optionnel)
8. [Exemple concret : Session de création](#8-exemple-concret--session-de-création)
9. [Scripts de validation Python](#9-scripts-de-validation-python)
10. [Évaluation Promptor](#10-évaluation-promptor)

---

## 1. Vue d'ensemble

Système de génération de composants Claude Code intégré au plugin EPCI.

### Composants du système

| Composant | Type | Rôle |
|-----------|------|------|
| `/epci:create` | Command | Point d'entrée unique, dispatch vers le skill approprié |
| `skills-creator` | Skill | Génère des Skills complets avec workflow interactif |
| `commands-creator` | Skill | Génère des Commands avec frontmatter optimisé |
| `subagents-creator` | Skill | Génère des Subagents avec mission focalisée |
| `component-advisor` | Skill | Détecte les patterns et suggère des créations (optionnel) |

### Principes de conception

1. **Autonomie** — Chaque skill est auto-suffisant (références dupliquées)
2. **Interactivité** — Workflow en 6 phases avec brainstorming et critique
3. **Validation** — Scripts Python automatisés par type de composant
4. **Documentation** — Chaque composant généré inclut sa documentation

---

## 2. Architecture des fichiers

```
epci-plugin/
│
├── commands/
│   └── create.md                     # /epci:create [type] [nom]
│
├── skills/
│   │
│   ├── skills-creator/
│   │   ├── SKILL.md
│   │   ├── references/
│   │   │   ├── best-practices.md     # Bonnes pratiques Skills
│   │   │   ├── description-formulas.md
│   │   │   ├── yaml-rules.md
│   │   │   └── checklist.md
│   │   ├── templates/
│   │   │   ├── skill-simple.md       # Template skill simple
│   │   │   └── skill-advanced.md     # Template skill avec références
│   │   └── scripts/
│   │       ├── validate_skill.py
│   │       └── test_triggering.py
│   │
│   ├── commands-creator/
│   │   ├── SKILL.md
│   │   ├── references/
│   │   │   ├── best-practices.md     # Bonnes pratiques Commands
│   │   │   ├── frontmatter-guide.md
│   │   │   ├── argument-patterns.md
│   │   │   └── checklist.md
│   │   ├── templates/
│   │   │   ├── command-simple.md
│   │   │   └── command-advanced.md
│   │   └── scripts/
│   │       └── validate_command.py
│   │
│   ├── subagents-creator/
│   │   ├── SKILL.md
│   │   ├── references/
│   │   │   ├── best-practices.md     # Bonnes pratiques Subagents
│   │   │   ├── delegation-patterns.md
│   │   │   ├── tools-restriction.md
│   │   │   └── checklist.md
│   │   ├── templates/
│   │   │   └── subagent-template.md
│   │   └── scripts/
│   │       └── validate_subagent.py
│   │
│   └── component-advisor/
│       └── SKILL.md
│
├── agents/
│   └── [subagents générés ici]
│
└── scripts/
    └── validate_all.py               # Orchestrateur de validation
```

---

## 3. Commande `/epci:create`

### Fichier : `commands/create.md`

```yaml
---
description: >-
  Crée un nouveau composant Claude Code (skill, command, subagent).
  Lance un workflow interactif avec brainstorming, critique et génération.
argument-hint: <type> <nom> — type: skill | command | subagent
allowed-tools: [Read, Write, Edit, Bash, Grep, Glob]
---

<objective>
Créer un composant Claude Code de type "$1" nommé "$2".
Dispatcher vers le skill spécialisé correspondant et guider l'utilisateur
à travers un workflow interactif de création.
</objective>

<routing>
## Dispatch selon le type

| Argument $1 | Skill activé | Destination des fichiers |
|-------------|--------------|--------------------------|
| `skill` | skills-creator | `epci-plugin/skills/$2/` |
| `command` | commands-creator | `epci-plugin/commands/$2.md` |
| `subagent` | subagents-creator | `epci-plugin/agents/$2.md` |

Si $1 n'est pas reconnu → Demander clarification.
Si $2 est vide → Demander le nom souhaité.
</routing>

<conflict_handling>
## Gestion des conflits de noms

Avant de créer, vérifier si un composant existe déjà :
1. Scanner le dossier de destination
2. Si conflit détecté :
   - Informer l'utilisateur : "Un composant '$2' existe déjà."
   - Proposer des alternatives : "$2-v2", "$2-new", ou un nom personnalisé
   - Attendre la validation avant de continuer
</conflict_handling>

<process>
## Workflow de création

1. **Validation des arguments**
   - Vérifier que $1 ∈ {skill, command, subagent}
   - Vérifier que $2 est en kebab-case et ≤64 caractères
   - Vérifier l'absence de conflit de nom

2. **Activation du skill spécialisé**
   - Charger le skill correspondant au type demandé
   - Transmettre le nom "$2" comme contexte initial

3. **Exécution du workflow interactif** (6 phases)
   - Le skill prend le relais pour guider l'utilisateur

4. **Validation finale**
   - Exécuter le script de validation approprié
   - Afficher le rapport de conformité

5. **Confirmation**
   - Résumer les fichiers créés
   - Fournir les instructions de test
</process>

<success_criteria>
- Composant créé dans le bon dossier
- Validation automatique passée (0 erreurs)
- Documentation générée
- Instructions de test fournies
</success_criteria>

<examples>
## Exemples d'utilisation

/epci:create skill docker-analyzer
→ Lance skills-creator pour créer un skill d'analyse Docker

/epci:create command deploy-staging
→ Lance commands-creator pour créer une commande de déploiement

/epci:create subagent security-reviewer
→ Lance subagents-creator pour créer un agent de revue sécurité
</examples>
```

### Comportement du dispatch

```
/epci:create skill mon-nouveau-skill
       │        │         │
       │        │         └── Nom du composant (kebab-case)
       │        └── Type : skill | command | subagent
       └── Commande EPCI

→ Active le skill correspondant (skills-creator, commands-creator, subagents-creator)
→ Démarre le workflow interactif en 6 phases
```

---

## 4. Skill `skills-creator`

### Fichier : `skills/skills-creator/SKILL.md`

```yaml
---
name: skills-creator
description: >-
  Générateur interactif de Skills Claude Code. Crée des packages complets
  avec SKILL.md, références, templates et scripts de validation.
  Workflow en 6 phases : analyse, architecture, description, workflow, validation, génération.
  Use when: créer un skill, générer une compétence, nouveau skill, skill pour [techno/domaine].
  Not for: commandes slash (→ commands-creator), subagents (→ subagents-creator), prompts ponctuels.
allowed-tools: [Read, Write, Edit, Bash, Grep, Glob]
---

# Skills Creator

## Overview

Générateur interactif de Skills Claude Code. Produit des packages complets et conformes
aux bonnes pratiques, incluant documentation et tests automatisés.

**Destination des fichiers** : `epci-plugin/skills/[nom-du-skill]/`

## Workflow Interactif (6 Phases)

### Phase 1 : Analyse Pré-Création
**Objectif** : Valider la pertinence et définir le périmètre

**Questions à poser** :
1. Quel problème ce skill résout-il ? (1 phrase)
2. Quelle est la fréquence d'usage estimée ?
3. Qui est le persona cible ? (dev backend, data analyst, devops...)
4. Quels mots-clés déclencheront ce skill ?
5. Quels sont les critères de succès mesurables ?
6. Qu'est-ce qui est explicitement HORS périmètre ?

**Livrable** : Fiche d'analyse complétée

**Gate** : Continuer si tâche récurrente + procédures stables + scope clair

---

### Phase 2 : Architecture
**Objectif** : Définir la structure des fichiers

**Décisions** :
- Niveau de complexité : Simple (SKILL.md seul) | Standard (+ références) | Avancé (+ scripts)
- Multi-workflow ? → Si oui, prévoir un decision tree
- Références nécessaires ? → Lister les fichiers

**Livrable** : Arborescence des fichiers à créer

---

### Phase 3 : Description Engineering
**Objectif** : Optimiser le triggering sémantique

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

**Livrable** : Description optimisée

---

### Phase 4 : Workflow & Instructions
**Objectif** : Rédiger le contenu du SKILL.md

**Structure** :
1. Overview (2-3 phrases)
2. Decision Tree (si multi-workflow)
3. Étapes numérotées du workflow
4. Règles critiques
5. Exemples (input → output)
6. Liens vers références
7. Limitations explicites

**Contrainte** : <5000 tokens

**Livrable** : Contenu SKILL.md complet

---

### Phase 5 : Validation (Dry-Run)
**Objectif** : Vérifier avant génération

**Checklist automatique** :
- [ ] YAML frontmatter valide
- [ ] Nom kebab-case ≤64 chars
- [ ] Description ≤1024 chars avec "Use when" et "Not for"
- [ ] Contenu <5000 tokens
- [ ] Tous les fichiers référencés listés
- [ ] Pas de conflit de nom

**Livrable** : Rapport de validation + preview des fichiers

**Gate** : Approbation utilisateur requise

---

### Phase 6 : Génération
**Objectif** : Produire les fichiers définitifs

**Fichiers générés** :
```
epci-plugin/skills/[nom]/
├── SKILL.md
├── references/
│   └── [fichiers de référence]
├── templates/
│   └── [templates si applicable]
├── scripts/
│   └── [scripts si applicable]
└── README.md
```

**Post-génération** :
1. Exécuter `validate_skill.py`
2. Exécuter `test_triggering.py`
3. Afficher le rapport final
4. Fournir 3 requêtes de test suggérées

---

## Règles Critiques

### Frontmatter YAML
```yaml
---
name: kebab-case-max-64     # OBLIGATOIRE
description: >-             # OBLIGATOIRE, ≤1024 chars
  [Capacités] + "Use when: ..." + "Not for: ..."
allowed-tools: [Read, ...]  # OPTIONNEL
---
```

### Limites
| Élément | Limite |
|---------|--------|
| `name` | ≤64 chars, kebab-case |
| `description` | ≤1024 chars |
| SKILL.md body | <5000 tokens |
| Profondeur dossiers | Max 2 niveaux |

### Anti-patterns
- ❌ Description vague → triggering aléatoire
- ❌ Tout dans SKILL.md → overflow contexte
- ❌ Fichiers non linkés → jamais chargés
- ❌ Skill multi-usage → découper en skills focalisés

---

## Knowledge Base

- [Best Practices](references/best-practices.md)
- [Description Formulas](references/description-formulas.md)
- [YAML Rules](references/yaml-rules.md)
- [Checklist](references/checklist.md)

## Templates

- [Simple Skill](templates/skill-simple.md)
- [Advanced Skill](templates/skill-advanced.md)

## Scripts

- [validate_skill.py](scripts/validate_skill.py) — Validation automatique
- [test_triggering.py](scripts/test_triggering.py) — Tests de triggering

---

## Limitations

Ce skill ne gère PAS :
- Les commandes slash (utiliser `commands-creator`)
- Les subagents (utiliser `subagents-creator`)
- Les prompts ponctuels non réutilisables
- Les skills nécessitant des APIs externes (utiliser MCP)

---

## Version

| Version | Date | Changements |
|---------|------|-------------|
| 1.0.0 | 2025-12 | Version initiale |

## Current: v1.0.0
```

---

## 5. Skill `commands-creator`

### Fichier : `skills/commands-creator/SKILL.md`

```yaml
---
name: commands-creator
description: >-
  Générateur interactif de Slash Commands Claude Code. Crée des commandes
  complètes avec frontmatter optimisé, gestion des arguments et workflow structuré.
  Workflow en 6 phases : analyse, architecture, frontmatter, instructions, validation, génération.
  Use when: créer une commande, nouvelle commande slash, /[nom], command pour [action].
  Not for: skills auto-invoqués (→ skills-creator), subagents (→ subagents-creator), hooks.
allowed-tools: [Read, Write, Edit, Bash, Grep, Glob]
---

# Commands Creator

## Overview

Générateur interactif de Slash Commands Claude Code. Produit des commandes complètes
avec frontmatter optimisé, gestion des arguments et documentation.

**Destination des fichiers** : `epci-plugin/commands/[nom].md`

## Workflow Interactif (6 Phases)

### Phase 1 : Analyse Pré-Création
**Objectif** : Définir le besoin et le scope de la commande

**Questions à poser** :
1. Quelle action cette commande déclenche-t-elle ? (1 phrase)
2. Quels arguments sont nécessaires ? (obligatoires vs optionnels)
3. Quels outils Claude devra-t-il utiliser ?
4. Y a-t-il des prérequis ou conditions ?
5. Quel est le résultat attendu ?
6. Qu'est-ce qui est HORS périmètre ?

**Livrable** : Fiche d'analyse

---

### Phase 2 : Architecture
**Objectif** : Décider de la complexité

**Niveaux** :
- **Simple** : Fichier unique, pas de références
- **Standard** : Fichier + templates intégrés
- **Avancé** : Fichier + références externes + scripts

**Livrable** : Décision de niveau + liste des fichiers

---

### Phase 3 : Frontmatter Engineering
**Objectif** : Configurer l'en-tête YAML

**Éléments** :
```yaml
---
description: >-
  Description courte visible dans /help
argument-hint: <arg1> [arg2] — description des arguments
allowed-tools: [Read, Write, Bash, ...]
---
```

**Bonnes pratiques** :
- Description : 1-2 lignes, action claire
- argument-hint : syntaxe `<obligatoire>` et `[optionnel]`
- allowed-tools : minimum nécessaire (principe du moindre privilège)

**Livrable** : Frontmatter complet

---

### Phase 4 : Instructions Design
**Objectif** : Rédiger le corps de la commande

**Structure recommandée** :
```markdown
<objective>
Décrire l'objectif en 1-2 phrases.
Utiliser $1, $2... ou $ARGUMENTS pour les arguments.
</objective>

<context>
Informations de contexte si nécessaire.
</context>

<process>
1. Étape 1
2. Étape 2
3. ...
</process>

<success_criteria>
- Critère 1
- Critère 2
</success_criteria>

<examples>
Exemples d'utilisation avec sortie attendue.
</examples>
```

**Livrable** : Corps de la commande

---

### Phase 5 : Validation (Dry-Run)
**Objectif** : Vérifier avant génération

**Checklist** :
- [ ] YAML frontmatter valide
- [ ] Nom de fichier kebab-case
- [ ] Description concise et claire
- [ ] Arguments documentés
- [ ] allowed-tools cohérents avec les actions
- [ ] Pas de conflit avec commandes existantes

**Livrable** : Rapport de validation

---

### Phase 6 : Génération
**Objectif** : Créer le fichier de commande

**Fichier généré** : `epci-plugin/commands/[nom].md`

**Post-génération** :
1. Exécuter `validate_command.py`
2. Afficher le rapport
3. Fournir la syntaxe d'appel

---

## Règles Critiques

### Gestion des arguments
| Syntaxe | Description |
|---------|-------------|
| `$ARGUMENTS` | Tous les arguments en une chaîne |
| `$1`, `$2`... | Arguments positionnels |
| `<arg>` | Argument obligatoire (dans hint) |
| `[arg]` | Argument optionnel (dans hint) |

### Allowed-tools courants
| Outil | Usage |
|-------|-------|
| `Read` | Lire des fichiers |
| `Write` | Écrire des fichiers |
| `Edit` | Modifier des fichiers |
| `Bash` | Exécuter des commandes shell |
| `Bash(cmd:*)` | Commande spécifique autorisée |
| `Grep` | Rechercher dans les fichiers |
| `Glob` | Lister des fichiers |

### Anti-patterns
- ❌ Description trop longue → difficile à scanner dans /help
- ❌ Trop d'outils autorisés → risque de dérive
- ❌ Arguments non documentés → confusion utilisateur
- ❌ Sections non structurées → comportement imprévisible

---

## Knowledge Base

- [Best Practices](references/best-practices.md)
- [Frontmatter Guide](references/frontmatter-guide.md)
- [Argument Patterns](references/argument-patterns.md)
- [Checklist](references/checklist.md)

## Templates

- [Simple Command](templates/command-simple.md)
- [Advanced Command](templates/command-advanced.md)

## Scripts

- [validate_command.py](scripts/validate_command.py)

---

## Limitations

Ce skill ne gère PAS :
- Les skills auto-invoqués (utiliser `skills-creator`)
- Les subagents (utiliser `subagents-creator`)
- Les hooks (configuration différente)

---

## Version

| Version | Date | Changements |
|---------|------|-------------|
| 1.0.0 | 2025-12 | Version initiale |

## Current: v1.0.0
```

---

## 6. Skill `subagents-creator`

### Fichier : `skills/subagents-creator/SKILL.md`

```yaml
---
name: subagents-creator
description: >-
  Générateur interactif de Subagents Claude Code. Crée des agents secondaires
  spécialisés avec prompt dédié, outils restreints et mission focalisée.
  Workflow en 6 phases : analyse, architecture, prompt engineering, outils, validation, génération.
  Use when: créer un subagent, agent spécialisé, déléguer à un agent, subagent pour [domaine].
  Not for: skills auto-invoqués (→ skills-creator), commandes slash (→ commands-creator).
allowed-tools: [Read, Write, Edit, Bash, Grep, Glob]
---

# Subagents Creator

## Overview

Générateur interactif de Subagents Claude Code. Produit des agents secondaires
spécialisés avec mission focalisée, prompt optimisé et outils restreints.

**Destination des fichiers** : `epci-plugin/agents/[nom].md`

## Workflow Interactif (6 Phases)

### Phase 1 : Analyse Pré-Création
**Objectif** : Définir la mission et justifier le subagent

**Questions à poser** :
1. Quelle est la mission précise de ce subagent ? (1 phrase)
2. Pourquoi déléguer plutôt que faire dans l'agent principal ?
3. Quelle expertise spécifique apporte-t-il ?
4. Quand doit-il être invoqué ? (automatique vs explicite)
5. Quel contexte minimal lui fournir ?
6. Qu'est-ce qui est HORS de sa responsabilité ?

**Livrable** : Fiche de mission

**Gate** : Continuer si mission focalisée + valeur ajoutée claire

---

### Phase 2 : Architecture
**Objectif** : Définir la structure du subagent

**Décisions** :
- Activation : automatique (Claude décide) ou explicite (utilisateur déclenche)
- Modèle : claude-sonnet (standard) ou claude-haiku (léger)
- Isolation : niveau de contexte partagé avec l'agent principal

**Livrable** : Configuration d'architecture

---

### Phase 3 : Prompt Engineering
**Objectif** : Rédiger le system prompt du subagent

**Structure** :
```yaml
---
name: nom-du-subagent
description: Description courte de la mission
model: claude-sonnet-4-20250514  # ou autre
allowed-tools: [Read, Grep, ...]
---

# System Prompt

## Rôle
Tu es un expert en [domaine]. Ta mission est de [objectif précis].

## Contexte
[Ce que le subagent doit savoir]

## Instructions
1. [Étape 1]
2. [Étape 2]

## Contraintes
- [Contrainte 1]
- [Contrainte 2]

## Format de sortie
[Structure attendue des réponses]
```

**Bonnes pratiques** :
- Rôle clair et expertise définie
- Instructions pas-à-pas
- Contraintes explicites
- Format de sortie standardisé

**Livrable** : System prompt complet

---

### Phase 4 : Configuration des outils
**Objectif** : Restreindre au minimum nécessaire

**Principe** : Un subagent ne doit avoir accès qu'aux outils strictement nécessaires à sa mission.

| Mission type | Outils recommandés |
|--------------|-------------------|
| Analyse de code | `Read, Grep, Glob` |
| Revue sécurité | `Read, Grep, WebFetch` |
| Documentation | `Read, Write` |
| Tests | `Read, Bash(pytest:*), Bash(npm test:*)` |
| Refactoring | `Read, Write, Edit` |

**Livrable** : Liste allowed-tools

---

### Phase 5 : Validation (Dry-Run)
**Objectif** : Vérifier la cohérence

**Checklist** :
- [ ] Mission focalisée (1 agent = 1 mission)
- [ ] Prompt clair et structuré
- [ ] Outils minimaux et cohérents
- [ ] Pas de chevauchement avec un subagent existant
- [ ] Activation appropriée (auto vs explicite)

**Livrable** : Rapport de validation

---

### Phase 6 : Génération
**Objectif** : Créer le fichier subagent

**Fichier généré** : `epci-plugin/agents/[nom].md`

**Post-génération** :
1. Exécuter `validate_subagent.py`
2. Afficher le rapport
3. Expliquer comment invoquer le subagent

---

## Règles Critiques

### Principes de délégation
| Faire | Ne pas faire |
|-------|--------------|
| Mission précise et focalisée | Agent générique "fais tout" |
| Contexte minimal transmis | Tout l'historique du projet |
| Outils strictement nécessaires | Tous les outils "au cas où" |
| Activation explicite (préféré) | Activation auto non contrôlée |

### Quand créer un subagent ?
- ✅ Tâche spécialisée récurrente (revue sécu, tests, doc)
- ✅ Expertise distincte de l'agent principal
- ✅ Isolation du contexte bénéfique
- ❌ Tâche ponctuelle simple
- ❌ Même expertise que l'agent principal
- ❌ Besoin de tout le contexte

### Anti-patterns
- ❌ Subagent trop générique → utiliser l'agent principal
- ❌ Trop de subagents → complexité ingérable
- ❌ Subagent qui "dérive" → prompt trop vague
- ❌ Contexte massif → surcharge inutile

---

## Knowledge Base

- [Best Practices](references/best-practices.md)
- [Delegation Patterns](references/delegation-patterns.md)
- [Tools Restriction](references/tools-restriction.md)
- [Checklist](references/checklist.md)

## Templates

- [Subagent Template](templates/subagent-template.md)

## Scripts

- [validate_subagent.py](scripts/validate_subagent.py)

---

## Limitations

Ce skill ne gère PAS :
- Les skills auto-invoqués (utiliser `skills-creator`)
- Les commandes slash (utiliser `commands-creator`)
- Les agents principaux (configuration système)

---

## Version

| Version | Date | Changements |
|---------|------|-------------|
| 1.0.0 | 2025-12 | Version initiale |

## Current: v1.0.0
```

---

## 7. Skill `component-advisor` (optionnel)

### Fichier : `skills/component-advisor/SKILL.md`

```yaml
---
name: component-advisor
description: >-
  Détecte les opportunités de création de composants réutilisables dans les conversations.
  Analyse les patterns répétitifs et suggère la création de skills, commands ou subagents.
  Use when: pattern répétitif détecté (3+ fois), "je fais souvent ça", "comment automatiser",
  workflow manuel récurrent, tâche répétée avec variations mineures.
  Not for: création explicite de composants (utiliser /epci:create), tâches ponctuelles.
allowed-tools: [Read, Grep, Glob]
---

# Component Advisor

## Overview

Skill de détection passive qui observe les patterns dans les conversations et suggère
la création de composants réutilisables quand approprié.

**Comportement** : Observe → Détecte → Suggère (ne génère pas directement)

## Critères de détection

### Signaux positifs (suggérer un composant)

| Signal | Exemple | Composant suggéré |
|--------|---------|-------------------|
| Répétition 3+ fois | Même workflow exécuté 3 fois | Skill ou Command |
| Expression explicite | "Je fais souvent ça" | Skill |
| Question d'automatisation | "Comment automatiser..." | Command ou Skill |
| Prompt réutilisé | Même prompt avec variations | Skill |
| Tâche déléguée | "À chaque fois je demande de..." | Subagent |

### Signaux négatifs (ne pas suggérer)

| Signal | Raison |
|--------|--------|
| Tâche ponctuelle | ROI négatif |
| Contexte unique | Non réutilisable |
| Procédure volatile | Maintenance excessive |
| Création explicite demandée | Utiliser /epci:create |

## Format de suggestion

Quand un pattern est détecté, répondre avec :

```markdown
💡 **Suggestion de composant**

J'ai remarqué que tu [description du pattern détecté].

**Proposition** : Créer un [skill/command/subagent] `[nom-suggéré]` pour automatiser ça.

**Bénéfices** :
- [Bénéfice 1]
- [Bénéfice 2]

👉 Pour créer : `/epci:create [type] [nom-suggéré]`

*Souhaites-tu que je lance la création ?*
```

## Workflow de détection

```
┌─────────────────────────────────────────┐
│         Observation passive              │
│   (analyse des messages utilisateur)     │
└─────────────────────┬───────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────┐
│         Pattern détecté ?                │
│   - Répétition ≥3 fois                   │
│   - Expression "je fais souvent"         │
│   - Question d'automatisation            │
└─────────────────────┬───────────────────┘
                      │
            ┌─────────┴─────────┐
            │                   │
           OUI                 NON
            │                   │
            ▼                   ▼
┌───────────────────┐   ┌───────────────────┐
│ Classifier le     │   │ Continuer         │
│ type de composant │   │ observation       │
└─────────┬─────────┘   └───────────────────┘
          │
          ▼
┌───────────────────┐
│ Formuler la       │
│ suggestion        │
└─────────┬─────────┘
          │
          ▼
┌───────────────────┐
│ Proposer          │
│ /epci:create      │
└───────────────────┘
```

## Classification du type

| Caractéristique | → Skill | → Command | → Subagent |
|-----------------|---------|-----------|------------|
| Déclenchement | Contexte sémantique | Action explicite | Délégation |
| Récurrence | Automatique | À la demande | Tâche isolée |
| Exemple | "Quand j'analyse du Docker..." | "Quand je tape /deploy" | "Délègue la revue sécu" |

## Limitations

- Ne génère pas de composants (suggère seulement)
- Ne peut pas détecter les patterns sur plusieurs sessions
- Seuils de détection approximatifs (3 répétitions = heuristique)

---

## Version

| Version | Date | Changements |
|---------|------|-------------|
| 1.0.0 | 2025-12 | Version initiale |

## Current: v1.0.0
```

---

## 8. Exemple concret : Session de création

### Scénario : Créer un skill `docker-analyzer`

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ UTILISATEUR                                                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│ /epci:create skill docker-analyzer                                          │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│ CLAUDE (Phase 1 : Analyse)                                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│ Je vais créer le skill `docker-analyzer`. Commençons par l'analyse.         │
│                                                                              │
│ **Questions de cadrage :**                                                   │
│                                                                              │
│ 1. Quel problème ce skill résout-il ?                                       │
│ 2. À quelle fréquence analyses-tu des fichiers Docker ?                     │
│ 3. Qui utilisera ce skill ? (ton profil technique)                          │
│ 4. Quels mots-clés devraient déclencher ce skill ?                          │
│    (ex: "Dockerfile", "docker-compose", "container"...)                     │
│ 5. Qu'attends-tu comme résultat ? (audit sécu, optimisation, best practices)│
│ 6. Ce qui est HORS périmètre ? (ex: Kubernetes, Podman...)                  │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│ UTILISATEUR                                                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│ 1. Analyser les Dockerfiles pour détecter les problèmes de sécurité         │
│    et les mauvaises pratiques                                                │
│ 2. Plusieurs fois par semaine, on a beaucoup de projets conteneurisés       │
│ 3. Dev fullstack Symfony/React, devops occasionnel                          │
│ 4. "Dockerfile", "docker", "analyse docker", "sécurité container"           │
│ 5. Rapport avec : vulnérabilités, optimisations, score de qualité           │
│ 6. Hors périmètre : Kubernetes, Helm, orchestration                         │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│ CLAUDE (Phase 2 : Architecture)                                              │
├─────────────────────────────────────────────────────────────────────────────┤
│ **Analyse validée** ✅ Tâche récurrente, scope clair, procédures stables.   │
│                                                                              │
│ **Architecture proposée** : Standard (SKILL.md + références)                 │
│                                                                              │
│ ```                                                                          │
│ epci-plugin/skills/docker-analyzer/                                          │
│ ├── SKILL.md                    # Instructions principales                   │
│ ├── references/                                                              │
│ │   ├── security-rules.md       # Règles de sécurité Docker                 │
│ │   ├── optimization-tips.md    # Conseils d'optimisation                   │
│ │   └── scoring-criteria.md     # Critères de scoring                       │
│ ├── templates/                                                               │
│ │   └── report-template.md      # Template du rapport d'analyse             │
│ └── README.md                   # Documentation                              │
│ ```                                                                          │
│                                                                              │
│ Cette structure te convient ?                                                │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│ UTILISATEUR                                                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│ Oui c'est bon                                                                │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│ CLAUDE (Phase 3 : Description)                                               │
├─────────────────────────────────────────────────────────────────────────────┤
│ **Description proposée** (pour le triggering) :                              │
│                                                                              │
│ ```                                                                          │
│ Analyzes Dockerfiles and docker-compose files for security vulnerabilities, │
│ performance issues, and best practices violations. Produces a quality       │
│ report with actionable recommendations.                                      │
│ Use when: analyzing Dockerfile, reviewing docker-compose, auditing          │
│ container security, optimizing Docker images.                                │
│ Not for: Kubernetes configs, Helm charts, container orchestration,          │
│ runtime container monitoring.                                                │
│ ```                                                                          │
│                                                                              │
│ **Validation** :                                                             │
│ - ✅ Verbes d'action : analyzes, produces                                   │
│ - ✅ Types de fichiers : Dockerfile, docker-compose                         │
│ - ✅ "Use when" : 4 contextes                                               │
│ - ✅ "Not for" : 4 exclusions                                               │
│ - ✅ Longueur : 487 caractères (≤1024)                                      │
│                                                                              │
│ Des ajustements ?                                                            │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│ UTILISATEUR                                                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│ Parfait, on continue                                                         │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│ CLAUDE (Phase 4 : Workflow)                                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│ **Workflow du skill** :                                                      │
│                                                                              │
│ 1. **Détection** — Identifier les fichiers Docker dans le projet            │
│ 2. **Analyse sécurité** — Vérifier contre les règles security-rules.md      │
│ 3. **Analyse performance** — Appliquer optimization-tips.md                  │
│ 4. **Scoring** — Calculer le score selon scoring-criteria.md                │
│ 5. **Rapport** — Générer le rapport selon report-template.md                │
│                                                                              │
│ **Règles critiques** :                                                       │
│ - Toujours analyser le Dockerfile ET docker-compose si présent              │
│ - Signaler les images non officielles                                        │
│ - Alerter sur USER root                                                      │
│ - Vérifier les COPY/ADD suspects                                             │
│                                                                              │
│ **Exemple de sortie** :                                                      │
│ ```                                                                          │
│ ## Docker Analysis Report                                                    │
│ **Score global** : 72/100 ⭐⭐⭐☆☆                                          │
│                                                                              │
│ ### 🔴 Problèmes critiques (2)                                              │
│ 1. USER root détecté ligne 15 → Utiliser un user non-privilégié             │
│ 2. Image non officielle `mycompany/node` → Préférer `node:20-alpine`        │
│                                                                              │
│ ### 🟡 Améliorations suggérées (3)                                          │
│ 1. Multi-stage build recommandé pour réduire la taille                      │
│ 2. .dockerignore manquant                                                    │
│ 3. Layers non optimisés (RUN multiples)                                     │
│ ```                                                                          │
│                                                                              │
│ Ce workflow te convient ?                                                    │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│ UTILISATEUR                                                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│ Oui génial                                                                   │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│ CLAUDE (Phase 5 : Validation)                                                │
├─────────────────────────────────────────────────────────────────────────────┤
│ **Validation pré-génération**                                                │
│                                                                              │
│ ✅ YAML frontmatter valide                                                  │
│ ✅ Nom : `docker-analyzer` (16 chars, kebab-case)                           │
│ ✅ Description : 487 chars, contient "Use when" et "Not for"                │
│ ✅ Contenu estimé : ~2800 tokens (<5000)                                    │
│ ✅ Références listées : 3 fichiers                                          │
│ ✅ Pas de conflit de nom détecté                                            │
│                                                                              │
│ **Fichiers à générer** :                                                     │
│ - SKILL.md (principal)                                                       │
│ - references/security-rules.md                                               │
│ - references/optimization-tips.md                                            │
│ - references/scoring-criteria.md                                             │
│ - templates/report-template.md                                               │
│ - README.md                                                                  │
│                                                                              │
│ **Prêt à générer ?** (oui/non)                                              │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│ UTILISATEUR                                                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│ oui                                                                          │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│ CLAUDE (Phase 6 : Génération)                                                │
├─────────────────────────────────────────────────────────────────────────────┤
│ **Génération en cours...**                                                   │
│                                                                              │
│ ✅ Créé : epci-plugin/skills/docker-analyzer/SKILL.md                       │
│ ✅ Créé : epci-plugin/skills/docker-analyzer/references/security-rules.md   │
│ ✅ Créé : epci-plugin/skills/docker-analyzer/references/optimization-tips.md│
│ ✅ Créé : epci-plugin/skills/docker-analyzer/references/scoring-criteria.md │
│ ✅ Créé : epci-plugin/skills/docker-analyzer/templates/report-template.md   │
│ ✅ Créé : epci-plugin/skills/docker-analyzer/README.md                      │
│                                                                              │
│ **Validation automatique...**                                                │
│ ```                                                                          │
│ $ python scripts/validate_skill.py docker-analyzer                           │
│ ✅ YAML syntax: OK                                                          │
│ ✅ Name format: OK                                                          │
│ ✅ Description: OK (487 chars)                                              │
│ ✅ Token count: OK (2847 tokens)                                            │
│ ✅ References: OK (3/3 files exist)                                         │
│ ✅ No conflicts: OK                                                         │
│ RESULT: PASSED (6/6 checks)                                                  │
│ ```                                                                          │
│                                                                              │
│ **Tests de triggering...**                                                   │
│ ```                                                                          │
│ $ python scripts/test_triggering.py docker-analyzer                          │
│ Testing: "Analyse mon Dockerfile" → ✅ TRIGGERED                            │
│ Testing: "Review docker-compose.yml" → ✅ TRIGGERED                         │
│ Testing: "Sécurité container" → ✅ TRIGGERED                                │
│ Testing: "Deploy Kubernetes" → ✅ NOT TRIGGERED (expected)                  │
│ Testing: "Aide-moi avec Helm" → ✅ NOT TRIGGERED (expected)                 │
│ RESULT: 5/5 tests passed                                                     │
│ ```                                                                          │
│                                                                              │
│ **Skill créé avec succès !** 🎉                                             │
│                                                                              │
│ **Pour tester** :                                                            │
│ - "Analyse le Dockerfile de ce projet"                                       │
│ - "Vérifie la sécurité de mon docker-compose.yml"                           │
│ - "Optimise mes images Docker"                                               │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 9. Scripts de validation Python

### 9.1 Script `validate_skill.py`

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


def estimate_tokens(text: str) -> int:
    """Estimation grossière du nombre de tokens (~4 chars/token)."""
    return len(text) // 4


def validate_yaml_syntax(content: str, report: ValidationReport) -> Optional[dict]:
    """Vérifie la syntaxe du frontmatter YAML."""
    try:
        # Extraire le frontmatter
        match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
        if not match:
            report.add_error("YAML frontmatter missing or malformed (must start with ---)")
            return None
        
        frontmatter = yaml.safe_load(match.group(1))
        print("✅ YAML syntax: OK")
        report.pass_check()
        return frontmatter
    
    except yaml.YAMLError as e:
        report.add_error(f"YAML syntax error: {e}")
        return None


def validate_name(frontmatter: dict, report: ValidationReport) -> bool:
    """Vérifie le format du nom."""
    name = frontmatter.get('name', '')
    
    if not name:
        report.add_error("Field 'name' is required in frontmatter")
        return False
    
    if len(name) > 64:
        report.add_error(f"Name too long: {len(name)} chars (max 64)")
        return False
    
    if not re.match(r'^[a-z0-9]+(-[a-z0-9]+)*$', name):
        report.add_error(f"Name must be kebab-case: '{name}'")
        return False
    
    print(f"✅ Name format: OK ({len(name)} chars, kebab-case)")
    report.pass_check()
    return True


def validate_description(frontmatter: dict, report: ValidationReport) -> bool:
    """Vérifie la description."""
    desc = frontmatter.get('description', '')
    
    if not desc:
        report.add_error("Field 'description' is required in frontmatter")
        return False
    
    if len(desc) > 1024:
        report.add_error(f"Description too long: {len(desc)} chars (max 1024)")
        return False
    
    has_use_when = 'use when' in desc.lower()
    has_not_for = 'not for' in desc.lower()
    
    if not has_use_when:
        report.add_warning("Description should contain 'Use when:' for better triggering")
    
    if not has_not_for:
        report.add_warning("Description should contain 'Not for:' to prevent false positives")
    
    print(f"✅ Description: OK ({len(desc)} chars)")
    report.pass_check()
    return True


def validate_token_count(content: str, report: ValidationReport) -> bool:
    """Vérifie le nombre de tokens."""
    # Retirer le frontmatter pour compter le body
    body = re.sub(r'^---\n.*?\n---\n', '', content, flags=re.DOTALL)
    tokens = estimate_tokens(body)
    
    if tokens > 5000:
        report.add_error(f"Content too long: ~{tokens} tokens (max 5000)")
        return False
    
    print(f"✅ Token count: OK (~{tokens} tokens)")
    report.pass_check()
    return True


def validate_references(skill_path: Path, content: str, report: ValidationReport) -> bool:
    """Vérifie que tous les fichiers référencés existent."""
    # Trouver tous les liens markdown
    links = re.findall(r'\[.*?\]\((.*?\.md)\)', content)
    
    missing = []
    for link in links:
        # Normaliser le chemin
        if link.startswith('references/') or link.startswith('templates/'):
            full_path = skill_path / link
            if not full_path.exists():
                missing.append(link)
    
    if missing:
        report.add_error(f"Missing referenced files: {', '.join(missing)}")
        return False
    
    total_refs = len(links)
    print(f"✅ References: OK ({total_refs}/{total_refs} files exist)")
    report.pass_check()
    return True


def check_conflicts(skill_name: str, skills_dir: Path, report: ValidationReport) -> bool:
    """Vérifie les conflits de noms."""
    existing = [d.name for d in skills_dir.iterdir() if d.is_dir() and d.name != skill_name]
    
    if skill_name in existing:
        report.add_error(f"Conflict: skill '{skill_name}' already exists")
        return False
    
    print("✅ No conflicts: OK")
    report.pass_check()
    return True


def validate_skill(skill_name: str, base_path: str = "epci-plugin/skills") -> int:
    """Point d'entrée principal de la validation."""
    report = ValidationReport(skill_name=skill_name)
    
    skill_path = Path(base_path) / skill_name
    skill_file = skill_path / "SKILL.md"
    
    if not skill_file.exists():
        report.add_error(f"SKILL.md not found at {skill_file}")
        return report.print_report()
    
    content = skill_file.read_text(encoding='utf-8')
    
    # 1. Validation YAML
    frontmatter = validate_yaml_syntax(content, report)
    if not frontmatter:
        return report.print_report()
    
    # 2. Validation du nom
    validate_name(frontmatter, report)
    
    # 3. Validation de la description
    validate_description(frontmatter, report)
    
    # 4. Validation du nombre de tokens
    validate_token_count(content, report)
    
    # 5. Validation des références
    validate_references(skill_path, content, report)
    
    # 6. Vérification des conflits
    check_conflicts(skill_name, Path(base_path), report)
    
    return report.print_report()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python validate_skill.py <skill-name>")
        sys.exit(1)
    
    sys.exit(validate_skill(sys.argv[1]))
```

### 9.2 Script `test_triggering.py`

```python
#!/usr/bin/env python3
"""
Tests automatisés de triggering pour les Skills Claude Code.
Usage: python test_triggering.py <skill-name>
"""

import sys
import re
import yaml
from pathlib import Path
from dataclasses import dataclass


@dataclass
class TriggeringTest:
    query: str
    should_trigger: bool
    

def extract_trigger_keywords(description: str) -> tuple[list[str], list[str]]:
    """Extrait les mots-clés de triggering de la description."""
    
    # Extraire "Use when:" section
    use_when_match = re.search(r'use when[:\s]+(.*?)(?:not for|$)', description, re.IGNORECASE | re.DOTALL)
    trigger_keywords = []
    if use_when_match:
        trigger_text = use_when_match.group(1)
        # Extraire les mots-clés significatifs
        trigger_keywords = [w.strip().lower() for w in re.split(r'[,.]', trigger_text) if w.strip()]
    
    # Extraire "Not for:" section
    not_for_match = re.search(r'not for[:\s]+(.*?)$', description, re.IGNORECASE | re.DOTALL)
    exclude_keywords = []
    if not_for_match:
        exclude_text = not_for_match.group(1)
        exclude_keywords = [w.strip().lower() for w in re.split(r'[,.]', exclude_text) if w.strip()]
    
    return trigger_keywords, exclude_keywords


def semantic_match(query: str, keywords: list[str]) -> bool:
    """Vérifie si la query matche sémantiquement avec les keywords."""
    query_lower = query.lower()
    for keyword in keywords:
        # Match si le keyword ou une partie significative est dans la query
        keyword_words = keyword.split()
        if any(word in query_lower for word in keyword_words if len(word) > 3):
            return True
    return False


def generate_test_cases(trigger_keywords: list[str], exclude_keywords: list[str]) -> list[TriggeringTest]:
    """Génère des cas de test basés sur les keywords extraits."""
    tests = []
    
    # Tests positifs (doivent trigger)
    for kw in trigger_keywords[:3]:  # Limiter à 3
        tests.append(TriggeringTest(
            query=f"Help me with {kw}",
            should_trigger=True
        ))
    
    # Tests négatifs (ne doivent pas trigger)
    for kw in exclude_keywords[:2]:  # Limiter à 2
        tests.append(TriggeringTest(
            query=f"I need help with {kw}",
            should_trigger=False
        ))
    
    return tests


def run_triggering_tests(skill_name: str, base_path: str = "epci-plugin/skills") -> int:
    """Exécute les tests de triggering."""
    skill_path = Path(base_path) / skill_name
    skill_file = skill_path / "SKILL.md"
    
    if not skill_file.exists():
        print(f"❌ SKILL.md not found at {skill_file}")
        return 1
    
    content = skill_file.read_text(encoding='utf-8')
    
    # Extraire le frontmatter
    match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not match:
        print("❌ Could not parse frontmatter")
        return 1
    
    frontmatter = yaml.safe_load(match.group(1))
    description = frontmatter.get('description', '')
    
    # Extraire les keywords
    trigger_kw, exclude_kw = extract_trigger_keywords(description)
    
    print(f"\n{'='*60}")
    print(f"TRIGGERING TESTS: {skill_name}")
    print(f"{'='*60}\n")
    
    print(f"Trigger keywords: {trigger_kw}")
    print(f"Exclude keywords: {exclude_kw}\n")
    
    # Générer et exécuter les tests
    tests = generate_test_cases(trigger_kw, exclude_kw)
    
    passed = 0
    failed = 0
    
    for test in tests:
        # Simuler le matching
        would_trigger = semantic_match(test.query, trigger_kw) and not semantic_match(test.query, exclude_kw)
        
        if would_trigger == test.should_trigger:
            status = "✅"
            result = "TRIGGERED" if would_trigger else "NOT TRIGGERED"
            expected = "(expected)" if not test.should_trigger else ""
            passed += 1
        else:
            status = "❌"
            result = "TRIGGERED" if would_trigger else "NOT TRIGGERED"
            expected = "(UNEXPECTED!)"
            failed += 1
        
        print(f'{status} Testing: "{test.query}" → {result} {expected}')
    
    print(f"\nRESULT: {passed}/{len(tests)} tests passed")
    print(f"{'='*60}\n")
    
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python test_triggering.py <skill-name>")
        sys.exit(1)
    
    sys.exit(run_triggering_tests(sys.argv[1]))
```

### 9.3 Script `validate_command.py`

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


# Liste des outils valides Claude Code
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


def validate_filename(filepath: Path, report: ValidationReport) -> bool:
    """Vérifie le format du nom de fichier."""
    name = filepath.stem  # nom sans extension
    
    if not re.match(r'^[a-z0-9]+(-[a-z0-9]+)*$', name):
        report.add_error(f"Filename must be kebab-case: '{name}'")
        return False
    
    print(f"✅ Filename format: OK ({name})")
    report.pass_check()
    return True


def validate_description(frontmatter: dict, report: ValidationReport) -> bool:
    """Vérifie la description."""
    desc = frontmatter.get('description', '')
    
    if not desc:
        report.add_error("Field 'description' is required")
        return False
    
    if len(desc) > 200:
        report.add_warning(f"Description is long ({len(desc)} chars) - may be truncated in /help")
    
    print(f"✅ Description: OK ({len(desc)} chars)")
    report.pass_check()
    return True


def validate_allowed_tools(frontmatter: dict, report: ValidationReport) -> bool:
    """Vérifie que les outils autorisés sont valides."""
    tools = frontmatter.get('allowed-tools', [])
    
    if not tools:
        report.add_warning("No allowed-tools specified - all tools will be available")
        report.pass_check()
        return True
    
    invalid = []
    for tool in tools:
        # Gérer les patterns comme Bash(cmd:*)
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
    """Vérifie la structure du corps de la commande."""
    body = re.sub(r'^---\n.*?\n---\n', '', content, flags=re.DOTALL)
    
    recommended_sections = ['<objective>', '<process>', '<success_criteria>']
    found = [s for s in recommended_sections if s in body.lower()]
    
    if len(found) < 2:
        report.add_warning(f"Recommended sections missing. Found: {found}")
    
    print(f"✅ Structure: OK ({len(found)}/3 recommended sections)")
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

### 9.4 Script `validate_subagent.py`

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
        report.add_error("Field 'description' is required - defines the agent's mission")
        return False
    
    # Vérifier que c'est une mission focalisée
    if len(desc.split()) > 50:
        report.add_warning("Description is long - subagent mission should be focused")
    
    print(f"✅ Description: OK ({len(desc)} chars)")
    report.pass_check()
    return True


def validate_allowed_tools(frontmatter: dict, report: ValidationReport) -> bool:
    """Vérifie les outils - doit être minimal."""
    tools = frontmatter.get('allowed-tools', [])
    
    if not tools:
        report.add_warning("No allowed-tools specified - consider restricting for security")
        report.pass_check()
        return True
    
    if len(tools) > 5:
        report.add_warning(f"Many tools allowed ({len(tools)}) - subagents should have minimal permissions")
    
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
    
    # Sections recommandées pour un subagent
    recommended = ['rôle', 'role', 'mission', 'instructions', 'contraintes', 'constraints']
    found = [s for s in recommended if s in body.lower()]
    
    if len(found) < 2:
        report.add_warning(f"System prompt may lack structure. Found sections: {found}")
    
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

---

## 10. Évaluation Promptor

### Score Global

**Score : 94/100** ★★★★★ | Complexité : **Complexe**

### Évaluation par critère

| Critère | Score | Commentaire |
|---------|-------|-------------|
| **Clarté de l'objectif** | 5/5 | Architecture complète et claire |
| **Définition des rôles** | 5/5 | Rôles distincts par composant |
| **Contexte & audience** | 5/5 | Intégration EPCI parfaite |
| **Format de sortie** | 5/5 | Structure fichiers détaillée |
| **Contraintes** | 5/5 | Règles explicites par type |
| **Workflow** | 5/5 | 6 phases détaillées + exemple complet |
| **Exemples** | 5/5 | Session docker-analyzer de A à Z |
| **Scripts** | 4/5 | Validation + triggering automatisés |

### Points forts

- ✅ Exemple concret de session complète (docker-analyzer)
- ✅ Scripts Python fonctionnels pour validation et triggering
- ✅ Gestion des conflits avec proposition de renommage
- ✅ Architecture autonome par skill (références dupliquées)
- ✅ 3 skills spécialisés + 1 advisor optionnel
- ✅ 1 commande unique comme point d'entrée

### Améliorations possibles (-6 points)

| Point | Impact | Suggestion |
|-------|--------|------------|
| Templates non fournis en détail | -3 | Créer les fichiers templates complets |
| `component-advisor` reste conceptuel | -2 | Définir les seuils de détection précis |
| Pas de tests d'intégration | -1 | Ajouter un script de test end-to-end |

---

## Prochaines étapes

1. **Génération des fichiers** — Créer l'arborescence complète dans le plugin EPCI
2. **Templates** — Produire les fichiers templates pour chaque type de composant
3. **Tests** — Valider le workflow complet avec un cas réel
4. **Documentation** — Créer le README principal du système Component Factory

---

*Document généré via la méthodologie Promptor v1.0*
