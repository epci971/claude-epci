---
description: >-
  Exploration time-boxée pour incertitudes techniques. Génère un Spike Report
  avec verdict GO/NO-GO/MORE_RESEARCH. Pas de code production, focus sur
  l'apprentissage et la réduction d'incertitude.
argument-hint: "[durée] [question]"
allowed-tools: [Read, Glob, Grep, Bash, Task, WebFetch]
---

# EPCI Spike — Exploration Time-boxée

## Overview

Un spike est une exploration limitée dans le temps pour réduire l'incertitude technique.
**Objectif : Apprendre, pas produire du code.**

## Arguments

| Argument | Description | Défaut |
|----------|-------------|--------|
| `durée` | Temps maximum (ex: 30min, 1h, 2h) | 1h |
| `question` | Question technique à résoudre | Obligatoire |

## Quand utiliser un spike

- Nouvelle technologie ou framework inconnu
- Faisabilité incertaine
- Plusieurs approches possibles sans préférence claire
- Intégration avec système externe non documenté
- Performance ou scalabilité à valider

## Process

### 1. Cadrage (5 min)

Définir clairement :
- **Question** : Quelle incertitude veut-on lever ?
- **Critères de succès** : Comment saurons-nous que c'est faisable ?
- **Time-box** : Durée maximale stricte
- **Scope** : Ce qui est inclus/exclus de l'exploration

```markdown
## Spike Setup

**Question :** [Question technique précise]

**Critères de succès :**
- [ ] Critère 1 (mesurable)
- [ ] Critère 2 (mesurable)

**Time-box :** [Durée]

**Scope :**
- ✅ Inclus : [Ce qu'on explore]
- ❌ Exclus : [Ce qu'on n'explore pas]
```

### 2. Exploration

**Invoquer @Explore** (niveau thorough) pour :
- Rechercher des solutions existantes
- Analyser des exemples de code
- Identifier les patterns applicables

**Activités typiques :**
- Lire la documentation
- Créer des prototypes jetables
- Tester des hypothèses
- Évaluer des alternatives

**Règles :**
- ⏱️ Respecter strictement le time-box
- 🗑️ Le code produit est jetable (pas de qualité production)
- 📝 Documenter les découvertes au fur et à mesure
- 🎯 Rester focalisé sur la question initiale

### 3. Synthèse (10 min)

À la fin du time-box, synthétiser :
- Ce qui a été appris
- Ce qui fonctionne / ne fonctionne pas
- Les risques identifiés
- La recommandation

## Output : Spike Report

```markdown
# Spike Report — [Titre]

## Question
[La question technique explorée]

## Résumé exécutif
[2-3 phrases sur la conclusion principale]

## Exploration menée

### Approches testées
| Approche | Résultat | Notes |
|----------|----------|-------|
| [Approche 1] | ✅ Fonctionne | [Détails] |
| [Approche 2] | ❌ Échoue | [Raison] |
| [Approche 3] | ⚠️ Partiel | [Limitations] |

### Code prototype
```[lang]
// Code jetable - NE PAS utiliser en production
[snippet démontrant le concept]
```

### Découvertes
1. [Découverte importante 1]
2. [Découverte importante 2]
3. [Découverte importante 3]

### Risques identifiés
| Risque | Probabilité | Impact | Mitigation |
|--------|-------------|--------|------------|
| [Risque 1] | Haute | Élevé | [Solution] |
| [Risque 2] | Moyenne | Moyen | [Solution] |

## Ressources consultées
- [Lien 1] - [Ce qu'on en a tiré]
- [Lien 2] - [Ce qu'on en a tiré]

## Verdict

### [GO | NO-GO | MORE_RESEARCH]

**Justification :**
[Explication du verdict]

### Si GO
- **Approche recommandée :** [Approche à suivre]
- **Effort estimé :** [SMALL | STANDARD | LARGE]
- **Prochaine étape :** Lancer `/epci-brief` avec ces informations

### Si NO-GO
- **Raison :** [Pourquoi ce n'est pas faisable]
- **Alternatives suggérées :** [Autres options à considérer]

### Si MORE_RESEARCH
- **Questions restantes :** [Ce qu'il faut encore explorer]
- **Spike suivant suggéré :** [Nouveau spike proposé]

## Temps passé
- Time-box prévu : [Durée]
- Temps réel : [Durée]
```

## Exemples de spikes

### Spike : Intégration API externe

```
Question : L'API de paiement X peut-elle gérer nos volumes ?
Time-box : 2h

Exploration :
- Lecture documentation API
- Test des endpoints en sandbox
- Mesure des temps de réponse
- Calcul des coûts

Verdict : GO
- L'API supporte 1000 req/s (notre besoin : 100)
- Pricing acceptable
- SDK PHP disponible
```

### Spike : Nouvelle techno

```
Question : GraphQL est-il adapté pour notre API ?
Time-box : 4h

Exploration :
- Setup serveur GraphQL
- Implémentation query basique
- Comparaison avec REST actuel
- Évaluation courbe d'apprentissage

Verdict : NO-GO
- Courbe d'apprentissage trop élevée pour l'équipe
- Bénéfices insuffisants pour notre cas d'usage
- Recommandation : Rester sur REST
```

## Skills chargés

- `architecture-patterns` (évaluation approches)
- `[stack-skill]` (auto-détecté)

## Différences avec autres workflows

| Aspect | /epci-spike | /epci | /epci-quick |
|--------|-------------|-------|-------------|
| Objectif | Apprendre | Produire | Produire |
| Code | Jetable | Production | Production |
| Output | Spike Report | Feature Doc | Commit |
| Tests | Non | Oui | Optionnel |
| Time-box | Strict | Flexible | Flexible |

## Post-spike

Après un spike GO :
1. Créer un brief avec les informations du spike
2. Lancer `/epci-brief` pour le workflow normal
3. Référencer le Spike Report dans le Feature Document

```
📊 **SPIKE COMPLETE**

Spike Report généré : docs/spikes/<spike-slug>.md
Verdict : [GO | NO-GO | MORE_RESEARCH]

Prochaine étape : [Action recommandée]
```
