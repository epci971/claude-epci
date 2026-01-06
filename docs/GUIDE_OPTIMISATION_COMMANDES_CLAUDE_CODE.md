# Guide d'Optimisation des Commandes Claude Code

> **Objectif** : Transformer une commande monolithique (500+ lignes) en une architecture modulaire, performante et économe en tokens.

---

## Table des matières

1. [Principes fondamentaux](#1-principes-fondamentaux)
2. [Diagnostic d'une commande](#2-diagnostic-dune-commande)
3. [Stratégies de modularisation](#3-stratégies-de-modularisation)
4. [Architecture cible](#4-architecture-cible)
5. [Techniques d'optimisation](#5-techniques-doptimisation)
6. [Checklist de refactoring](#6-checklist-de-refactoring)
7. [Templates prêts à l'emploi](#7-templates-prêts-à-lemploi)
8. [Anti-patterns à éviter](#8-anti-patterns-à-éviter)

---

## 1. Principes fondamentaux

### 1.1 Le coût du contexte

| Élément | Impact contexte | Chargement |
|---------|-----------------|------------|
| Commande `.md` | **Immédiat** - chargé entièrement | Au lancement |
| Référence `@file` | **Différé** - chargé à l'invocation | À la demande |
| Skill `SKILL.md` | **Progressif** - metadata puis contenu | Selon besoin |
| Subagent | **Isolé** - contexte séparé | Délégation |

### 1.2 Règles d'or

```
┌─────────────────────────────────────────────────────────────────┐
│  RÈGLE 1: Commande < 200 lignes (idéal: 50-100 lignes)         │
│  RÈGLE 2: SKILL.md < 500 lignes                                 │
│  RÈGLE 3: Externaliser tout ce qui n'est pas essentiel         │
│  RÈGLE 4: Progressive disclosure > tout charger                 │
│  RÈGLE 5: Un fichier = une responsabilité                       │
└─────────────────────────────────────────────────────────────────┘
```

### 1.3 Formule d'optimisation

```
Tokens économisés = (Lignes externalisées × ~4 tokens/ligne) × Nombre d'invocations
```

Une commande de 1000 lignes invoquée 10 fois = ~40 000 tokens gaspillés si tout n'est pas utilisé à chaque fois.

---

## 2. Diagnostic d'une commande

### 2.1 Analyse de contenu

Avant toute optimisation, catégorise chaque section de ta commande :

| Catégorie | Description | Action recommandée |
|-----------|-------------|-------------------|
| **CORE** | Instructions essentielles, toujours nécessaires | Garder dans la commande |
| **REFERENCE** | Documentation, règles, standards | Externaliser en `@file` |
| **CONDITIONAL** | Utilisé selon le contexte | Convertir en Skill |
| **HEAVY** | Workflows complexes, multi-étapes | Déléguer à Subagent |
| **STATIC** | Templates, exemples, patterns | Fichiers séparés |
| **REDUNDANT** | Répétitions, verbosité | Supprimer/condenser |

### 2.2 Métriques cibles

```yaml
Commande optimale:
  lignes_totales: < 200
  lignes_instructions_core: < 50
  references_externes: 2-5 fichiers
  skills_associés: 0-2
  subagents: 0-1 (pour workflows complexes)
  
Signaux d'alerte:
  - Plus de 300 lignes → Refactoring obligatoire
  - Plus de 3 niveaux de headers → Structure trop complexe
  - Exemples > 30% du contenu → Externaliser
  - Répétitions de patterns → Factoriser
```

### 2.3 Script de diagnostic

Exécute cette analyse sur ta commande :

```bash
# Compter les lignes
wc -l .claude/commands/ma-commande.md

# Analyser la structure
grep -c "^#" .claude/commands/ma-commande.md      # Nombre de headers
grep -c "^\`\`\`" .claude/commands/ma-commande.md  # Blocs de code
grep -c "^-\|^\*\|^[0-9]\." .claude/commands/ma-commande.md  # Listes
```

---

## 3. Stratégies de modularisation

### 3.1 Stratégie 1: Références `@file` (Quick Win)

**Quand l'utiliser** : Données statiques, templates, règles qui ne changent pas

```markdown
# AVANT (dans la commande)
## Règles de codage
- Utiliser des noms explicites
- Pas de magic numbers
- ... (50 lignes de règles)

# APRÈS (commande)
Applique les règles définies dans @.claude/references/coding-rules.md
```

**Structure recommandée** :
```
.claude/
└── references/
    ├── coding-rules.md
    ├── security-patterns.md
    ├── naming-conventions.md
    └── templates/
        ├── component.template.md
        └── test.template.md
```

### 3.2 Stratégie 2: Conversion en Skill (Progressive Disclosure)

**Quand l'utiliser** : Workflows réutilisables, expertise domaine, documentation riche

**Principe** : Claude charge d'abord le nom/description, puis le SKILL.md complet si pertinent, puis les fichiers annexes à la demande.

```
.claude/skills/mon-domaine/
├── SKILL.md           # Vue d'ensemble (< 500 lignes)
├── DETAILED_RULES.md  # Règles complètes (chargé si besoin)
├── EXAMPLES.md        # Exemples (chargé si besoin)
├── PATTERNS.md        # Patterns avancés
└── scripts/
    └── validate.sh    # Scripts utilitaires
```

**Template SKILL.md** :
```yaml
---
name: mon-domaine-skill
description: |
  Expertise pour [domaine]. Utilisé quand [triggers].
  Cas d'usage: [liste courte].
---

# Mon Domaine Skill

## Quick Reference
[Instructions condensées - 20-30 lignes max]

## Workflow Standard
1. Étape 1
2. Étape 2
3. Étape 3

## Ressources
- Règles détaillées: [DETAILED_RULES.md](DETAILED_RULES.md)
- Exemples: [EXAMPLES.md](EXAMPLES.md)
- Patterns: [PATTERNS.md](PATTERNS.md)
```

### 3.3 Stratégie 3: Délégation Subagent

**Quand l'utiliser** : 
- Tâches qui nécessitent beaucoup de lecture de fichiers
- Workflows parallélisables
- Isolation de contexte nécessaire

```yaml
# .claude/agents/specialist/AGENT.md
---
name: specialist-agent
description: |
  Expert en [domaine]. Délègue-lui les tâches de [type].
  Invoque automatiquement pour: [triggers]
skills: mon-skill-1, mon-skill-2
model: inherit
tools: Read, Grep, Glob, Bash
---

Tu es un expert en [domaine].

## Ta mission
[Instructions détaillées - pas de limite stricte car contexte isolé]

## Process
1. Analyse
2. Traitement
3. Rapport synthétique au contexte principal
```

### 3.4 Stratégie 4: Architecture hybride

**Pour les commandes très complexes** (1000+ lignes originales) :

```
Commande (point d'entrée)
    │
    ├──→ @references (données statiques)
    │
    ├──→ Skill (progressive disclosure)
    │       ├── SKILL.md
    │       ├── RULES.md
    │       └── EXAMPLES.md
    │
    └──→ Subagent (tâches lourdes)
            └── AGENT.md (avec skills)
```

---

## 4. Architecture cible

### 4.1 Structure de fichiers recommandée

```
.claude/
├── commands/
│   └── ma-commande.md              # Point d'entrée (< 150 lignes)
│
├── references/
│   ├── coding-standards.md         # Standards de code
│   ├── security-rules.md           # Règles sécurité
│   ├── naming-conventions.md       # Conventions nommage
│   └── templates/
│       └── *.template.md           # Templates réutilisables
│
├── skills/
│   └── ma-commande-knowledge/
│       ├── SKILL.md                # Skill principal (< 500 lignes)
│       ├── DOMAIN_KNOWLEDGE.md     # Connaissance domaine
│       ├── ADVANCED_PATTERNS.md    # Patterns avancés
│       ├── EXAMPLES.md             # Exemples détaillés
│       └── scripts/
│           └── helpers.py          # Scripts utilitaires
│
└── agents/
    └── ma-commande-specialist/
        └── AGENT.md                # Agent spécialisé
```

### 4.2 Répartition du contenu

```
┌─────────────────────────────────────────────────────────────────┐
│                    COMMANDE (< 150 lignes)                      │
├─────────────────────────────────────────────────────────────────┤
│  • Frontmatter (description, allowed-tools)                     │
│  • Objectif principal (2-3 lignes)                              │
│  • Variables/Arguments ($ARGUMENTS, $1, $2)                     │
│  • Workflow high-level (étapes numérotées)                      │
│  • Références aux ressources externes                           │
│  • Output attendu                                               │
└─────────────────────────────────────────────────────────────────┘
                              │
          ┌───────────────────┼───────────────────┐
          ▼                   ▼                   ▼
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│   REFERENCES    │  │     SKILL       │  │    SUBAGENT     │
│   (@file)       │  │  (progressive)  │  │    (isolé)      │
├─────────────────┤  ├─────────────────┤  ├─────────────────┤
│ • Standards     │  │ • SKILL.md      │  │ • Tâches        │
│ • Templates     │  │ • RULES.md      │  │   complexes     │
│ • Conventions   │  │ • EXAMPLES.md   │  │ • Exploration   │
│ • Données       │  │ • PATTERNS.md   │  │ • Analyse       │
│   statiques     │  │ • scripts/      │  │   approfondie   │
└─────────────────┘  └─────────────────┘  └─────────────────┘
   Chargé quand        Chargé si            Contexte
   référencé           pertinent            séparé
```

---

## 5. Techniques d'optimisation

### 5.1 Condensation du texte

```markdown
# AVANT (verbeux)
## Instructions pour la revue de code
Quand tu fais une revue de code, tu dois t'assurer de vérifier 
plusieurs aspects importants. Premièrement, il faut regarder si 
le code respecte les conventions de nommage établies par l'équipe.
Deuxièmement, tu dois vérifier que les fonctions ne sont pas trop
longues et qu'elles font une seule chose...

# APRÈS (condensé)
## Code Review
Vérifie: naming conventions, fonction unique/courte, tests présents,
error handling, no magic numbers. Réfère-toi à @.claude/references/review-checklist.md
```

### 5.2 Utilisation efficace des listes

```markdown
# AVANT
- Premier point important à considérer
- Deuxième point important à considérer
- Troisième point important à considérer
- Quatrième point important à considérer
- Cinquième point important à considérer

# APRÈS
Points clés: A, B, C, D, E (détails dans @references/details.md)
```

### 5.3 Frontmatter optimisé

```yaml
---
# Essentiel
description: [Action] [cible] [contexte]. Trigger: [mots-clés].
allowed-tools: Read, Write, Bash(npm:*), Bash(git:*)

# Optionnel mais utile
argument-hint: <target> [--flag]
model: inherit
---
```

### 5.4 Instructions par référence

```markdown
# Pattern efficace
Applique le workflow de @.claude/skills/my-skill/SKILL.md pour $ARGUMENTS.

Si complexité > moyenne, délègue à @my-specialist-agent.

Output: format défini dans @.claude/references/output-format.md
```

### 5.5 Conditional loading avec Bash

```markdown
---
allowed-tools: Bash(cat:*), Read
---

# Context dynamique
Fichiers modifiés: !`git diff --name-only HEAD~1`
Branch actuelle: !`git branch --show-current`

Analyse uniquement les fichiers listés ci-dessus.
```

---

## 6. Checklist de refactoring

### Phase 1: Analyse (15 min)

- [ ] Compter les lignes totales
- [ ] Identifier les sections CORE vs REFERENCE vs CONDITIONAL vs HEAVY
- [ ] Lister les répétitions
- [ ] Identifier les exemples/templates extractibles
- [ ] Évaluer la complexité du workflow

### Phase 2: Extraction (30-60 min)

- [ ] Créer `.claude/references/` pour les données statiques
- [ ] Extraire les règles/standards en fichiers séparés
- [ ] Extraire les templates
- [ ] Extraire les exemples volumineux

### Phase 3: Skill (si nécessaire) (30 min)

- [ ] Créer `.claude/skills/[nom]/`
- [ ] Rédiger SKILL.md condensé (< 500 lignes)
- [ ] Distribuer le contenu dans fichiers annexes
- [ ] Ajouter les liens de référence dans SKILL.md

### Phase 4: Subagent (si nécessaire) (20 min)

- [ ] Identifier les tâches déléguables
- [ ] Créer `.claude/agents/[nom]/AGENT.md`
- [ ] Définir les skills accessibles au subagent
- [ ] Configurer les tools appropriés

### Phase 5: Commande finale (30 min)

- [ ] Réécrire la commande avec références
- [ ] Tester avec différents arguments
- [ ] Vérifier que tout se charge correctement
- [ ] Mesurer les tokens avant/après

### Phase 6: Validation

```bash
# Vérifier la nouvelle structure
tree .claude/

# Tester la commande
claude
> /ma-commande test-argument

# Vérifier le contexte utilisé
> /context
```

---

## 7. Templates prêts à l'emploi

### 7.1 Template de commande optimisée

```markdown
---
description: [Verbe] [cible] selon [méthode]. Triggers: [mots-clés].
allowed-tools: Read, Write, Grep, Glob
argument-hint: <target> [options]
---

# [Nom de la commande]

## Objectif
[1-2 phrases décrivant le but]

## Input
- Target: $ARGUMENTS (ou $1, $2 pour arguments positionnels)
- Context: !`git diff --name-only` (optionnel)

## Workflow
1. [Étape 1 - action concrète]
2. [Étape 2 - action concrète]
3. [Étape 3 - action concrète]

## Ressources
- Standards: @.claude/references/standards.md
- Patterns: @.claude/skills/[skill]/PATTERNS.md

## Output
[Format attendu - court]

## Notes
- Si complexité élevée → délègue à @[agent-name]
- Valide avec @.claude/skills/[skill]/scripts/validate.sh
```

### 7.2 Template SKILL.md

```yaml
---
name: [nom-du-skill]
description: |
  [Capacité principale]. Utilisé pour [cas d'usage].
  Triggers: [mots-clés qui activent ce skill].
allowed-tools: Read, Grep, Glob
---

# [Nom du Skill]

## Quick Start
[Instructions essentielles en 10-20 lignes]

## Workflow standard
1. [Étape 1]
2. [Étape 2]  
3. [Étape 3]

## Règles clés
[5-10 règles maximum, les autres dans RULES.md]

## Ressources détaillées
| Besoin | Fichier |
|--------|---------|
| Règles complètes | [RULES.md](RULES.md) |
| Exemples | [EXAMPLES.md](EXAMPLES.md) |
| Patterns avancés | [PATTERNS.md](PATTERNS.md) |
| Scripts | [scripts/](scripts/) |

## Troubleshooting
[3-5 problèmes courants avec solutions rapides]
```

### 7.3 Template AGENT.md

```yaml
---
name: [nom-agent]
description: |
  Expert [domaine]. Utilisé pour [tâches spécifiques].
  Délègue automatiquement quand: [conditions].
skills: skill-1, skill-2
model: inherit
tools: Read, Grep, Glob, Bash
---

# [Nom de l'Agent]

## Rôle
Tu es un expert en [domaine] spécialisé dans [spécialité].

## Mission
[Description de la mission principale]

## Process
1. **Analyse** : [description]
2. **Traitement** : [description]
3. **Rapport** : [format de sortie pour le contexte principal]

## Contraintes
- [Contrainte 1]
- [Contrainte 2]

## Output attendu
Retourne un rapport synthétique contenant:
- Résumé (3-5 lignes)
- Findings principaux
- Recommandations actionables
```

### 7.4 Template de fichier référence

```markdown
# [Titre du document de référence]

> **Usage**: Référencé par `@.claude/references/[filename].md`
> **Dernière màj**: [date]

## [Section 1]
[Contenu]

## [Section 2]
[Contenu]

---
*Ce fichier est chargé à la demande. Ne pas inclure d'instructions de workflow.*
```

---

## 8. Anti-patterns à éviter

### ❌ Anti-pattern 1: Tout dans la commande

```markdown
# MAUVAIS - Commande de 800 lignes
---
description: Fait tout
---
[800 lignes d'instructions, exemples, règles, templates...]
```

### ❌ Anti-pattern 2: Références circulaires

```markdown
# MAUVAIS - A référence B qui référence A
# file-a.md
Voir @file-b.md pour plus de détails

# file-b.md  
Voir @file-a.md pour le contexte
```

### ❌ Anti-pattern 3: Skills trop génériques

```yaml
# MAUVAIS
---
name: helper
description: Aide pour diverses tâches
---
```

```yaml
# BON
---
name: react-component-generator
description: |
  Génère des composants React avec TypeScript.
  Triggers: "créer composant", "nouveau component", "generate react"
---
```

### ❌ Anti-pattern 4: Subagent pour tâches simples

```markdown
# MAUVAIS - Subagent overkill
Délègue à @simple-task-agent pour renommer une variable
```

### ❌ Anti-pattern 5: Duplication de contenu

```markdown
# MAUVAIS - Mêmes règles dans plusieurs fichiers
# command.md
## Règles: [liste]

# skill/SKILL.md  
## Règles: [même liste]

# BON - Source unique
# references/rules.md
## Règles: [liste]

# command.md
Applique @.claude/references/rules.md

# skill/SKILL.md
Règles: voir [../references/rules.md](../references/rules.md)
```

### ❌ Anti-pattern 6: Instructions ambiguës

```markdown
# MAUVAIS
Fais une bonne analyse du code

# BON
Analyse le code pour: sécurité (OWASP top 10), performance (complexité O),
maintenabilité (couplage/cohésion). Output: tableau par catégorie.
```

---

## Annexe: Métriques de succès

### Avant optimisation
```
Commande: 1000 lignes
Tokens/invocation: ~4000
Temps de chargement: élevé
Contexte disponible: réduit
```

### Après optimisation
```
Commande: 100 lignes
Skill: 300 lignes (chargé si besoin)
References: 400 lignes (chargées à la demande)
Agent: 200 lignes (contexte isolé)

Tokens/invocation typique: ~800-1500
Tokens économisés: 60-80%
Contexte préservé: maximal
```

---

## Commande d'auto-optimisation

Utilise cette commande pour demander à Claude Code d'optimiser une commande existante :

```
Analyse et optimise la commande @.claude/commands/[ma-commande].md selon 
le guide @[ce-fichier].md.

1. Diagnostic: catégorise chaque section (CORE/REFERENCE/CONDITIONAL/HEAVY)
2. Propose une architecture cible avec structure de fichiers
3. Génère les fichiers optimisés
4. Valide que le comportement est préservé
```

---

*Guide v1.0 - Basé sur les best practices Anthropic et la documentation officielle Claude Code*
