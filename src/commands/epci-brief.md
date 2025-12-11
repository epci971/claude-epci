---
description: >-
  Point d'entrée EPCI. Analyse le brief brut, clarifie les ambiguïtés via
  questions itératives, évalue la complexité et route vers le workflow
  approprié (/epci-quick, /epci, /epci-spike).
allowed-tools: [Read, Glob, Grep, Bash, Task]
---

# EPCI Brief — Point d'entrée

## Overview

Cette commande est le point d'entrée unique du workflow EPCI.
Elle transforme un brief brut en brief structuré et oriente vers le workflow approprié.

## Process

### Étape 1 : Analyse initiale

**Invoquer @Explore** (niveau medium) pour :
- Scanner la structure du projet
- Identifier les technologies utilisées
- Estimer la complexité architecturale

Analyser le brief pour identifier :
- Les éléments clairs et exploitables
- Les ambiguïtés et zones d'ombre
- Les informations manquantes critiques
- Les incohérences éventuelles

### Étape 2 : Boucle de clarification

Si des ambiguïtés sont détectées, poser des questions ciblées (max 3 itérations) :

| Catégorie | Questions types |
|-----------|-----------------|
| **Business/Valeur** | Pourquoi ? Pour qui ? Quel impact métier ? |
| **Scope** | Qu'est-ce qui est inclus/exclus ? Quelles limites ? |
| **Contraintes** | Techniques ? Temps ? Budget ? Dépendances ? |
| **Priorité** | Criticité ? Deadline ? Bloquant pour quoi ? |

**Règles :**
- Maximum 5 questions par itération
- Maximum 3 itérations de clarification
- Prioriser les questions bloquantes

### Étape 3 : Suggestions IA

Proposer des améliorations basées sur l'analyse @Explore :
- Suggestions de design (basées sur architecture-patterns)
- Bonnes pratiques de la stack détectée
- Points d'attention spécifiques au contexte
- Risques potentiels identifiés

### Étape 4 : Évaluation de complexité

| Critère | TINY | SMALL | STANDARD | LARGE | SPIKE |
|---------|------|-------|----------|-------|-------|
| Fichiers | 1 | 2-3 | 4-10 | 10+ | ? |
| LOC estimé | <50 | <200 | <1000 | 1000+ | ? |
| Risque | Aucun | Faible | Moyen | Élevé | Inconnu |
| Tests requis | Non | Optionnel | Oui | Oui+ | N/A |
| Archi impactée | Non | Non | Possible | Oui | ? |

### Étape 5 : Routage

| Catégorie | Commande | Justification |
|-----------|----------|---------------|
| TINY | `/epci-quick` | Exécution immédiate, pas de plan formel |
| SMALL | `/epci-quick` | Plan léger intégré |
| STANDARD | `/epci` | Workflow complet 3 phases |
| LARGE | `/epci --large` | Thinking renforcé, tous subagents |
| SPIKE | `/epci-spike` | Exploration time-boxée |

## Output

Générer le brief structuré :

```markdown
# Brief Fonctionnel — [Titre]

## Contexte
[Résumé du besoin en 2-3 phrases]

## Stack détectée
[Stack identifiée par @Explore : framework, langage, versions]

## Critères d'acceptation
- [ ] Critère 1 (mesurable)
- [ ] Critère 2 (mesurable)
- [ ] Critère 3 (mesurable)

## Contraintes
- [Contrainte technique identifiée]
- [Contrainte temps/budget si applicable]

## Hors périmètre
- [Exclusion explicite 1]
- [Exclusion explicite 2]

## Évaluation
- **Catégorie** : [TINY|SMALL|STANDARD|LARGE|SPIKE]
- **Fichiers estimés** : X
- **LOC estimés** : ~Y
- **Risque** : [Aucun|Faible|Moyen|Élevé|Inconnu]
- **Justification** : [Raison de la catégorisation]

## Recommandation
→ Utiliser `/epci-quick` | `/epci` | `/epci --large` | `/epci-spike`
```

## Skills chargés

- `epci-core` (concepts EPCI)
- `architecture-patterns` (évaluation complexité)
- `[stack-skill]` (auto-détecté selon projet)

## Transition

Après génération du brief :
1. Présenter le brief structuré à l'utilisateur
2. Attendre confirmation avant de router
3. Proposer de lancer la commande recommandée

```
---
📋 **BRIEF COMPLET**

Brief fonctionnel généré et validé.
Catégorie : [CATEGORY]
Workflow recommandé : [COMMAND]

**Prochaine étape :** Lancer `[COMMAND]` ?
---
```
