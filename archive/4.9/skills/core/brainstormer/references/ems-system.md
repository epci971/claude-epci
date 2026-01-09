# EMS — Exploration Maturity Score

## Overview

Score composite sur 100 mesurant la maturite de l'exploration.
Calcule sur 5 axes ponderes. Version 2.0 avec ancres objectives.

## Les 5 Axes

| Axe | Poids | Description | Indicateurs |
|-----|-------|-------------|-------------|
| **Clarte** | 25% | Precision du besoin | Ambiguites resolues, reformulation validee |
| **Profondeur** | 20% | Niveau de detail | Specs detaillees, edge cases identifies |
| **Couverture** | 20% | Exhaustivite | Tous aspects couverts, rien oublie |
| **Decisions** | 20% | Choix actes | Decisions prises vs en suspens |
| **Actionnabilite** | 15% | Pret pour action | Assez de details pour implementer |

## Calcul

```
EMS = (Clarte x 0.25) + (Profondeur x 0.20) + (Couverture x 0.20)
    + (Decisions x 0.20) + (Actionnabilite x 0.15)
```

Chaque axe est note de 0 a 100.

## Ancres Objectives

Criteres observables pour un scoring plus coherent.

| Score | Clarte | Profondeur | Decisions |
|-------|--------|------------|-----------|
| **20** | Sujet enonce, non reformule | Questions surface uniquement | Tout reste ouvert |
| **40** | Brief valide + scope defini | 1 chaine "pourquoi" (2+ niveaux) | 1-2 orientations prises |
| **60** | + Contraintes (>=2) identifiees | Framework applique OU deep dive | Choix cles verrouilles |
| **80** | + Criteres d'acceptation | Insights non-evidents | Priorisation etablie |
| **100** | Zero ambiguite sur le "quoi" | Cause racine identifiee + validee | Tous threads fermes |

**Couverture** :
- 20: Une seule perspective
- 40: 2-3 angles explores
- 60: Risques adresses OU alternatives comparees
- 80: Multi-stakeholders OU >=3 alternatives avec criteres
- 100: Aucun angle mort identifiable

**Actionnabilite** :
- 20: Idees vagues, aucune action concrete
- 40: "Il faudrait..." sans qui/quand
- 60: Actions identifiees avec owner OU timeline
- 80: Actions + owner + timeline + dependances
- 100: Plan d'action complet, pret a executer

## Recommandations Phase-Aware

Les recommandations s'adaptent a la phase actuelle.

| Phase | Focus Principal | Comportement |
|-------|-----------------|--------------|
| 🔀 Divergent | Couverture, Profondeur | Ne pas pousser les Decisions (normal qu'elles soient basses) |
| 🎯 Convergent | Decisions, Actionnabilite | Pousser vers les decisions, suggerer frameworks de decision |

**En phase Divergente** :
```
Recommandations :
→ Couverture a 45% : Explorons d'autres angles (stakeholders ? risques ?)
→ Profondeur a 38% : Un deep dive enrichirait l'exploration
```

**En phase Convergente** :
```
Recommandations :
→ Decisions a 52% : 3 points restent ouverts, tranchons
→ Actionnabilite a 40% : Definissons des actions concretes avec owners
```

## Echelle de Maturite

| Score | Niveau | Emoji | Signification |
|-------|--------|-------|---------------|
| 0-30 | Germination | seed | Exploration initiale, beaucoup d'inconnues |
| 31-50 | Developpement | seedling | Contours se precisent, questions cles identifiees |
| 51-70 | Mature | tree | Vision claire, details a affiner |
| 71-85 | Tres Complete | target | Pret pour implementation, finish recommande |
| 86-100 | Exceptionnelle | trophy | Exhaustif, documentation de reference |

## Affichage Compact (CLI)

```
Iteration 3 | EMS: 58/100 (+12) [##########..........] seedling
```

- 20 caracteres pour la barre
- Delta depuis derniere iteration
- Emoji de niveau

## Affichage Detaille (sur `status`)

```
EMS : 58/100 [##########..........] seedling

   Clarte       [#################...] 85/100
   Profondeur   [##########..........] 52/100
   Couverture   [##########..........] 55/100
   Decisions    [###########.........] 58/100
   Actionnab.   [######..............] 32/100

Recommandation: Actionnabilite faible, detailler les specs techniques
```

## Evolution Typique

| Phase | EMS attendu | Actions |
|-------|-------------|---------|
| Init | 20-25 | Contexte etabli, premieres questions |
| Iteration 1 | 35-45 | Cadrage initial fait |
| Iteration 2 | 50-60 | Approfondissement |
| Iteration 3 | 65-75 | Maturite atteinte |
| Finish | 70+ | Brief generable |

## Criteres par Axe

### Clarte (25%)
- [ ] Besoin reformule et valide
- [ ] Objectif principal clair
- [ ] Perimetre defini
- [ ] Utilisateurs cibles identifies

### Profondeur (20%)
- [ ] Specs fonctionnelles detaillees
- [ ] Edge cases identifies
- [ ] Contraintes techniques listees
- [ ] Dependances mappees

### Couverture (20%)
- [ ] Tous les aspects fonctionnels couverts
- [ ] Impacts techniques identifies
- [ ] Hors scope explicite
- [ ] Questions de securite/perf adressees

### Decisions (20%)
- [ ] Choix technologiques actes
- [ ] Approche architecturale decidee
- [ ] Priorites etablies
- [ ] Compromis documentes

### Actionnabilite (15%)
- [ ] Assez de details pour estimer
- [ ] Criteres d'acceptation definis
- [ ] Premiere etape claire
- [ ] Risques identifies
