# Frameworks d'Analyse

## Overview

Outils methodologiques a appliquer selon le contexte de l'exploration.
Detection automatique basee sur les signaux de la conversation.

## MoSCoW — Priorisation

### Declencheur
- "Quelles priorites ?"
- "Qu'est-ce qui est essentiel ?"
- Multiple features a trier

### Application

| Categorie | Definition | Critere |
|-----------|------------|---------|
| **Must** | Indispensable | Bloquant si absent |
| **Should** | Important | Forte valeur ajoutee |
| **Could** | Souhaitable | Nice to have |
| **Won't** | Exclu (v1) | Hors scope explicite |

### Format Output

```
Priorisation MoSCoW

Must (non negociable):
- [Feature 1]
- [Feature 2]

Should (important):
- [Feature 3]

Could (si temps):
- [Feature 4]

Won't (v1):
- [Feature 5]
```

---

## 5 Whys — Analyse Causale

### Declencheur
- Besoin flou ou symptome plutot que cause
- "Pourquoi" demande plusieurs fois
- Probleme recurrent

### Application

Creuser iterativement :
1. Pourquoi [probleme initial] ?
2. Pourquoi [reponse 1] ?
3. Pourquoi [reponse 2] ?
4. Pourquoi [reponse 3] ?
5. Pourquoi [reponse 4] ? -> Cause racine

### Format Output

```
Analyse 5 Whys

Probleme: [enonce initial]

1. Pourquoi ? -> [reponse]
2. Pourquoi ? -> [reponse]
3. Pourquoi ? -> [reponse]
4. Pourquoi ? -> [reponse]
5. Pourquoi ? -> [cause racine]

Cause racine identifiee: [conclusion]
```

---

## SWOT — Analyse Strategique

### Declencheur
- Comparaison d'approches
- Evaluation d'une option technique
- Decision architecture

### Application

| Dimension | Question |
|-----------|----------|
| **Strengths** | Quels avantages de cette approche ? |
| **Weaknesses** | Quelles limites ou risques ? |
| **Opportunities** | Quels benefices futurs ? |
| **Threats** | Quels dangers ou obstacles ? |

### Format Output

```
Analyse SWOT — [Option]

+-----------------+-----------------+
| FORCES          | FAIBLESSES      |
+-----------------+-----------------+
| - [force 1]     | - [faiblesse 1] |
| - [force 2]     | - [faiblesse 2] |
+-----------------+-----------------+
| OPPORTUNITES    | MENACES         |
+-----------------+-----------------+
| - [opport. 1]   | - [menace 1]    |
| - [opport. 2]   | - [menace 2]    |
+-----------------+-----------------+
```

---

## Scoring — Matrice de Decision

### Declencheur
- Plusieurs options a comparer
- Criteres multiples
- Besoin de justifier un choix

### Application

1. Lister les options
2. Definir les criteres (3-5 max)
3. Ponderer les criteres
4. Noter chaque option (1-5)
5. Calculer les scores

### Format Output

```
Matrice de Decision

Criteres: Complexite (30%), Performance (25%),
          Maintenabilite (25%), Cout (20%)

| Option    | Compl. | Perf. | Maint. | Cout | TOTAL |
|-----------|--------|-------|--------|------|-------|
| Option A  | 4      | 5     | 3      | 4    | 4.05  |
| Option B  | 3      | 4     | 5      | 3    | 3.80  |
| Option C  | 5      | 3     | 4      | 5    | 4.20  |

Recommandation: Option C (score 4.20)
```

---

## Pre-mortem — Anticipation des Risques

### Declencheur
- Commande `premortem`
- Projet a risque identifie
- Avant decision finale importante

### Persona
Active automatiquement 🥊 Sparring

### Application

1. **Projection** : "Nous sommes dans 3 mois. L'implementation a echoue."
2. **Identification** : Lister toutes les causes possibles d'echec
3. **Scoring** : Probabilite x Impact (1-3 chaque, score max 9)
4. **Mitigation** : Definir action preventive pour causes majeures (score >= 6)
5. **Signaux** : Identifier alertes a surveiller

### Scoring

| Niveau | Probabilite | Impact |
|--------|-------------|--------|
| 🟢 Faible | 1 | 1 |
| 🟡 Moyenne | 2 | 2 |
| 🔴 Haute/Critique | 3 | 3 |

Score = Probabilite x Impact (max 9)

### Format Output

```
⚰️ Pre-mortem : [Feature]

Projection: Nous sommes dans 3 mois. L'implementation a echoue.

| # | Cause | Proba | Impact | Score |
|---|-------|-------|--------|-------|
| 1 | [Cause technique 1] | 🔴 Haute | 🔴 Critique | 9 |
| 2 | [Cause technique 2] | 🟡 Moyenne | 🔴 Critique | 6 |
| 3 | [Cause technique 3] | 🟡 Moyenne | 🟡 Modere | 4 |

Mitigations preventives:
| Cause | Action | Qui | Quand |
|-------|--------|-----|-------|
| [Cause 1] | [Action preventive] | Dev | Sprint 1 |
| [Cause 2] | [Action preventive] | Dev | Sprint 1 |

Signaux d'alerte:
- 🚨 [Signal 1] → [Action corrective]
- 🚨 [Signal 2] → [Action corrective]
```

### Integration

Les mitigations identifiees alimentent :
- Section "Risques" du Feature Document EPCI
- Estimation de contingence
- Section "Risques" dans Propositor

---

## Quand Appliquer

| Situation | Framework |
|-----------|-----------|
| Trop de features, besoin de trier | MoSCoW |
| Probleme flou, symptome vs cause | 5 Whys |
| Evaluer une approche technique | SWOT |
| Comparer plusieurs solutions | Scoring |
| Anticiper les risques, projet important | Pre-mortem |
| Aucun signal clair | Continuer questions |

## Anti-patterns

- **Ne pas forcer** un framework si non pertinent
- **Ne pas combiner** plusieurs frameworks en une iteration
- **Ne pas bloquer** l'exploration pour appliquer un framework
