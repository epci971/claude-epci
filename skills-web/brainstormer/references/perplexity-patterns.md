# Perplexity Research Patterns

## Overview

Cette référence définit les patterns de génération de prompts Perplexity pour enrichir les brainstormings avec des données actualisées et sourcées.

**Philosophie** : Exploiter les forces de chaque outil — Perplexity pour la recherche web actualisée, Claude pour l'analyse et la synthèse.

## Workflow Integration

```
Brief validé → HMW générées → 🔍 Recherches Perplexity → Résultats injectés → EMS initialisé
                                      │
                                      ▼
                              3-5 prompts optimisés
                              avec indicateur 🔍/🔬
```

## Research Mode Selection

### Critères de décision

| Critère | 🔍 Standard | 🔬 Deep Research |
|---------|-------------|------------------|
| Question factuelle simple | ✓ | - |
| Prix, dates, specs techniques | ✓ | - |
| Comparatif 2-3 options | ✓ | - |
| État de l'art complet | - | ✓ |
| Analyse multi-sources (5+) | - | ✓ |
| Sujet technique complexe | - | ✓ |
| Tendances sur période (6+ mois) | - | ✓ |
| Retours d'expérience détaillés | - | ✓ |
| Consensus scientifique/industriel | - | ✓ |
| Exploration d'un domaine inconnu | - | ✓ |

### Règle simplifiée

> **🔍 Standard** : Je cherche UNE information précise
> **🔬 Deep Research** : Je veux COMPRENDRE un sujet en profondeur

## Prompt Patterns par Type

### Technical

| Pattern | Mode | Template |
|---------|------|----------|
| État de l'art | 🔬 | `Quels sont les [technos/approches] les plus utilisés pour [use case] en [année] ? Critères : [liste]. Sources récentes uniquement.` |
| Comparatif | 🔍/🔬 | `Compare [A] vs [B] vs [C] pour [contexte spécifique]. Critères : [liste]. Format tableau si possible.` |
| Patterns/Anti-patterns | 🔬 | `Quels sont les patterns et anti-patterns reconnus pour [architecture/approche] ? Exemples concrets appréciés.` |
| REX Implémentation | 🔬 | `Retours d'expérience implémentation de [techno] en [contexte]. Pièges courants, solutions, métriques.` |
| API/SDK | 🔍 | `Quelles APIs/SDK existent pour [fonctionnalité] ? Comparatif : pricing, limites, qualité doc.` |

**Exemple Technical** :
```
Compare Apache Airflow vs Prefect vs Dagster pour orchestrer 
des pipelines ETL Django en production.
Critères : courbe d'apprentissage, intégration Django, 
monitoring, scalabilité, communauté.
Format tableau si possible.
```

### Business

| Pattern | Mode | Template |
|---------|------|----------|
| Benchmark marché | 🔬 | `Benchmark [secteur/métrique] en [région] pour [année]. Moyennes, leaders, tendances.` |
| Études de cas | 🔬 | `Études de cas [type de projet/transformation] dans [secteur]. Résultats chiffrés, facteurs de succès.` |
| Tendances | 🔬 | `Tendances [domaine] pour [horizon temporel]. Signaux faibles, prédictions analystes, impacts business.` |
| Modèles économiques | 🔍 | `Quels modèles économiques pour [type de produit/service] ? Exemples et métriques clés.` |
| Pricing | 🔍 | `Grille tarifaire [type de service] en [marché]. Fourchettes, facteurs de variation.` |

**Exemple Business** :
```
Études de cas de digitalisation de processus industriels 
dans le secteur agroalimentaire en France.
Résultats chiffrés, ROI, facteurs de succès et d'échec.
```

### Creative

| Pattern | Mode | Template |
|---------|------|----------|
| Inspirations | 🔍 | `Exemples innovants de [type de solution/design] pour [contexte]. Visuels ou descriptions détaillées.` |
| Références secteur | 🔬 | `Meilleures pratiques UX/UI pour [domaine]. Standards, conventions, innovations récentes.` |
| Contraintes domaine | 🔍 | `Contraintes réglementaires/techniques pour [type de produit] en [marché]. Points de vigilance.` |

**Exemple Creative** :
```
Meilleures pratiques UX pour les applications de suivi 
de production industrielle sur tablette.
Standards, conventions, innovations récentes.
```

### Analytical

| Pattern | Mode | Template |
|---------|------|----------|
| Données factuelles | 🔍 | `[Métrique spécifique] pour [entité/secteur] en [période]. Sources officielles privilégiées.` |
| Métriques secteur | 🔬 | `KPIs et benchmarks [secteur] en [année]. Définitions, moyennes, meilleures performances.` |
| Méthodologies | 🔬 | `Méthodologies éprouvées pour [type d'analyse/audit]. Étapes, outils, critères d'évaluation.` |

**Exemple Analytical** :
```
KPIs et benchmarks pour la performance des usines sucrières 
en 2024. Rendements, TCH, taux d'extraction, coûts.
Définitions standards et meilleures performances mondiales.
```

## Prompt Patterns par Template

### feature

| Focus | Recherches suggérées |
|-------|---------------------|
| APIs existantes | `APIs/SDK pour [fonctionnalité]. Pricing, limites, qualité.` |
| UX patterns | `Patterns UX pour [type de feature]. Conventions, exemples.` |
| Implémentations référence | `Comment [entreprise/produit] a implémenté [feature similaire] ?` |

### audit

| Focus | Recherches suggérées |
|-------|---------------------|
| Normes | `Normes et standards [domaine] en [année]. ISO, réglementations.` |
| Best practices | `Best practices [domaine] checklist. Points de contrôle essentiels.` |
| Outils d'audit | `Outils d'audit [domaine]. Comparatif, méthodologies.` |

### project

| Focus | Recherches suggérées |
|-------|---------------------|
| REX similaires | `Retours d'expérience projets [type] en [secteur]. Durées, budgets, pièges.` |
| Estimations | `Estimations typiques projet [type]. Fourchettes, facteurs de variation.` |
| Risques connus | `Risques fréquents projets [type]. Mitigation, signaux d'alerte.` |

### decision

| Focus | Recherches suggérées |
|-------|---------------------|
| Comparatifs | `Comparatif détaillé [option A] vs [option B]. Critères multiples.` |
| Trade-offs | `Trade-offs [choix technique/business]. Avantages, inconvénients, contextes.` |
| Critères décision | `Critères de décision pour [type de choix]. Frameworks, pondérations.` |

### problem

| Focus | Recherches suggérées |
|-------|---------------------|
| Causes documentées | `Causes fréquentes de [problème]. Diagnostic, indicateurs.` |
| Solutions éprouvées | `Solutions à [problème] en [contexte]. Efficacité, implémentation.` |
| Cas résolus | `Études de cas résolution [problème]. Avant/après, méthode.` |

### research

| Focus | Recherches suggérées |
|-------|---------------------|
| État de l'art | `État de l'art [domaine] en [année]. Publications, tendances.` |
| Acteurs clés | `Acteurs majeurs [domaine]. Entreprises, chercheurs, institutions.` |
| Controverses | `Débats et controverses [sujet]. Positions, arguments, consensus.` |

### strategy

| Focus | Recherches suggérées |
|-------|---------------------|
| Tendances long terme | `Tendances [secteur] horizon [3-5 ans]. Prédictions, scénarios.` |
| Mouvements concurrents | `Stratégies [concurrents/secteur]. Acquisitions, pivots, investissements.` |
| Signaux faibles | `Signaux faibles [domaine]. Innovations émergentes, disruptions potentielles.` |

## Output Format

### Format de génération (par Brainstormer)

```markdown
## 🔍 Recherches Perplexity

Avant de poursuivre l'exploration, effectue ces recherches pour enrichir notre contexte :

### R1 — [Catégorie] 🔍 Standard
```
[Prompt optimisé prêt à copier]
```

### R2 — [Catégorie] 🔬 Deep Research
```
[Prompt optimisé prêt à copier]
```

### R3 — [Catégorie] 🔍 Standard
```
[Prompt optimisé prêt à copier]
```

---
📋 **Instructions** :
1. Copie chaque prompt dans Perplexity (active Deep Research si indiqué 🔬)
2. Colle les résultats ici avec le format :
   ```
   ### Résultat R1
   [coller le résultat]
   
   ### Résultat R2
   [coller le résultat]
   ```
3. Tu peux faire toutes les recherches d'un coup ou sélectionner les plus pertinentes
4. Tape `skip` pour continuer sans recherches
```

### Format d'injection (par l'utilisateur)

```markdown
### Résultat R1
[Contenu copié depuis Perplexity]

### Résultat R2
[Contenu copié depuis Perplexity]

### Résultat R3
[Contenu copié depuis Perplexity]
```

## Quantity Guidelines

| Complexité sujet | Nombre de recherches |
|------------------|---------------------|
| Simple / Bien connu | 3 |
| Standard | 4 |
| Complexe / Nouveau domaine | 5 |

| Phase | Nombre de recherches |
|-------|---------------------|
| Initiale (après HMW) | 3-5 |
| Commande `research` en itération | 2-3 |

## Quality Criteria for Generated Prompts

### ✅ Bon prompt Perplexity

- Spécifique (pas vague)
- Contextualisé (secteur, année, région si pertinent)
- Orienté synthèse (pas juste une liste)
- Critères explicites si comparatif
- Longueur : 20-80 mots

### ❌ Mauvais prompt Perplexity

- Trop vague : "Parle-moi de l'IA"
- Trop large : "Tout sur le cloud computing"
- Sans contexte : "Meilleur framework"
- Opinion pure : "Quel est le meilleur langage ?"

## Integration with EMS

Les résultats Perplexity impactent l'EMS initial :

| Axe EMS | Impact des recherches |
|---------|----------------------|
| **Clarity** | +5-10 si les recherches clarifient le périmètre |
| **Depth** | +10-15 si état de l'art ou REX détaillés |
| **Coverage** | +5-10 si angles multiples couverts |
| **Decisions** | +5 si critères de décision fournis |
| **Actionability** | +5 si exemples concrets/implémentables |

## Skip Behavior

Si l'utilisateur tape `skip` ou `continue sans recherche` :
- Brainstormer continue normalement
- EMS initialisé aux valeurs baseline standard
- Mention dans le journal : "Recherches Perplexity : skipped"
- La commande `research` reste disponible pendant les itérations
