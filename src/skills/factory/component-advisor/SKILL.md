---
name: component-advisor
description: >-
  Détection passive d'opportunités de création de composants EPCI. Identifie
  les patterns répétitifs qui pourraient devenir des skills, commandes ou
  subagents. Use when: analyse de workflow, détection de patterns récurrents.
  Not for: création active de composants (utiliser /epci:create).
---

# Component Advisor

## Overview

Skill passif qui détecte les opportunités de création de nouveaux composants
EPCI basé sur l'analyse des patterns d'utilisation.

## Détection automatique

### Indicateurs de nouveau Skill

| Signal | Score | Exemple |
|--------|-------|---------|
| Pattern répété 3+ fois | +3 | Même validation dans plusieurs commandes |
| Domaine technique non couvert | +2 | Nouvelle stack non supportée |
| Documentation fréquemment consultée | +2 | Recherches répétées sur même sujet |
| Copier-coller de guidelines | +1 | Mêmes conventions appliquées |

**Seuil de suggestion :** Score ≥ 4

### Indicateurs de nouvelle Commande

| Signal | Score | Exemple |
|--------|-------|---------|
| Séquence d'actions répétée | +3 | Même workflow manuel récurrent |
| Combinaison de skills fréquente | +2 | Toujours les mêmes skills ensemble |
| Process documenté mais non automatisé | +2 | Guide suivi manuellement |
| Demande utilisateur explicite | +3 | "J'aimerais une commande pour..." |

**Seuil de suggestion :** Score ≥ 4

### Indicateurs de nouveau Subagent

| Signal | Score | Exemple |
|--------|-------|---------|
| Validation spécialisée répétée | +3 | Check de sécurité spécifique |
| Review manuelle récurrente | +2 | Même checklist appliquée |
| Expertise domaine pointue | +2 | Connaissance spécialisée requise |
| Format de rapport standardisé | +1 | Même structure de rapport |

**Seuil de suggestion :** Score ≥ 4

## Format de suggestion

Quand un seuil est atteint :

```markdown
💡 **COMPONENT OPPORTUNITY DETECTED**

### Type suggéré : [Skill | Command | Subagent]

**Pattern identifié :**
[Description du pattern détecté]

**Occurrences :**
- [Occurrence 1]
- [Occurrence 2]
- [Occurrence 3]

**Bénéfices estimés :**
- [Bénéfice 1]
- [Bénéfice 2]

**Proposition :**
```
/epci:create [type] [suggested-name]
```

**Score de confiance :** [X/10]

---
*Suggestion automatique - Ignorer si non pertinent*
```

## Patterns surveillés

### Pour Skills

| Pattern | Domaine potentiel |
|---------|-------------------|
| Recherches répétées sur une techno | Nouveau skill stack |
| Conventions appliquées manuellement | Skill conventions |
| Best practices citées souvent | Skill patterns |
| Outils externes fréquemment utilisés | Skill intégration |

### Pour Commandes

| Pattern | Commande potentielle |
|---------|---------------------|
| Séquence d'outils répétée | Commande composite |
| Workflow multi-étapes manuel | Commande automatisation |
| Process avec breakpoints | Commande structurée |
| Action + validation + rapport | Commande workflow |

### Pour Subagents

| Pattern | Subagent potentiel |
|---------|-------------------|
| Validation récurrente | Validator agent |
| Analyse spécialisée | Analyzer agent |
| Review avec checklist | Reviewer agent |
| Génération formatée | Generator agent |

## Configuration

### Activer/Désactiver

Le component-advisor est passif par défaut.
Il observe et suggère sans interrompre le workflow.

### Seuils personnalisables

```yaml
component_advisor:
  skill_threshold: 4
  command_threshold: 4
  subagent_threshold: 4
  suggestion_frequency: "on_pattern_detected"  # ou "end_of_session"
```

## Exemples de détection

### Exemple 1 : Nouveau Skill détecté

```
💡 COMPONENT OPPORTUNITY: Skill

Pattern : Documentation Kubernetes consultée 5 fois
         Même structure de deployment appliquée 3 fois

Suggestion : /epci:create skill kubernetes-patterns

Bénéfices :
- Auto-détection projets K8s
- Patterns standardisés
- Réduction temps de recherche
```

### Exemple 2 : Nouvelle Commande détectée

```
💡 COMPONENT OPPORTUNITY: Command

Pattern : Séquence répétée
         1. Lint → 2. Test → 3. Build → 4. Deploy

Suggestion : /epci:create command ci-pipeline

Bénéfices :
- Automatisation du process
- Cohérence entre projets
- Gain de temps
```

### Exemple 3 : Nouveau Subagent détecté

```
💡 COMPONENT OPPORTUNITY: Subagent

Pattern : Checklist accessibilité appliquée 4 fois
         Même format de rapport généré

Suggestion : /epci:create agent a11y-auditor

Bénéfices :
- Audit automatique
- Rapport standardisé
- Pas d'oubli de critères
```

## Métriques

| Métrique | Description |
|----------|-------------|
| Patterns détectés | Nombre de patterns identifiés |
| Suggestions émises | Nombre de suggestions proposées |
| Suggestions acceptées | Composants effectivement créés |
| Taux d'adoption | % suggestions → composants |

## Limitations

- Détection basée sur la session courante
- Pas de mémoire entre sessions (sauf si contexte fourni)
- Suggestions indicatives, pas prescriptives
- Nécessite patterns répétés pour détecter
