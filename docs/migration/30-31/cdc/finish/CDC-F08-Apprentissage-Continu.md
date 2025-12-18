# Cahier des Charges — F08: Apprentissage Continu

> **Document**: CDC-F08-001
> **Version**: 1.0.0
> **Date**: 2025-12-15
> **Statut**: Validé
> **Feature ID**: F08
> **Version cible**: EPCI v4.0
> **Priorité**: P1

---

## 1. Contexte Global EPCI

### 1.1 Philosophie EPCI v4.0

```
┌─────────────────────────────────────────────────────────────────────┐
│                        PHILOSOPHIE EPCI                             │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  🎯 SIMPLICITÉ        — 5 commandes ciblées, pas 22                │
│  📋 TRAÇABILITÉ       — Feature Document pour chaque feature        │
│  ⏸️  BREAKPOINTS       — L'humain valide entre les phases           │
│  🔄 TDD               — Red → Green → Refactor systématique         │
│  🧩 MODULARITÉ        — Skills, Agents, Commands séparés            │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### 1.2 État Actuel (Baseline v3.0.0)

EPCI v3.0.0 **ne s'améliore pas avec l'usage**. Chaque session est indépendante, sans apprentissage.

### 1.3 Glossaire Pertinent

| Terme | Définition |
|-------|------------|
| **Learning Loop** | Boucle d'apprentissage continu (mesure → analyse → adapte → améliore) |
| **Vélocité** | Vitesse de développement mesurée |
| **Calibration** | Ajustement des modèles d'estimation |
| **Project Memory** | Système de persistance du contexte (F04) |

---

## 2. Description de la Feature

### 2.1 Contexte et Justification

**Problème** : EPCI ne s'améliore pas avec l'usage :
- Estimations toujours basées sur des heuristiques fixes
- Mêmes erreurs répétées
- Suggestions génériques sans adaptation
- Pas de calibration des prédictions

**Solution** : Système d'apprentissage continu qui :
- Collecte des métriques à chaque workflow
- Analyse les patterns de succès/échec
- Calibre les estimations avec les données réelles
- Améliore les suggestions basées sur le feedback

### 2.2 Objectif

Créer une **boucle d'amélioration continue** où EPCI devient plus précis et pertinent avec chaque feature développée.

---

## 3. Spécifications Fonctionnelles

### 3.1 Boucle d'Apprentissage

```
┌─────────────────────────────────────────────────────────────────────┐
│                    LEARNING LOOP                                    │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│    ┌───────────┐     ┌───────────┐     ┌───────────┐              │
│    │  MESURE   │ ──► │  ANALYSE  │ ──► │  ADAPTE   │              │
│    └───────────┘     └───────────┘     └───────────┘              │
│         │                                     │                     │
│         │                                     │                     │
│         └─────────────────────────────────────┘                    │
│                         │                                           │
│                         ▼                                           │
│                  ┌─────────────┐                                   │
│                  │   AMÉLIORE  │                                   │
│                  └─────────────┘                                   │
│                                                                     │
│  MESURE: Temps réel, estimé, déviations, erreurs                   │
│  ANALYSE: Patterns, corrélations, causes                           │
│  ADAPTE: Ajuste modèles, seuils, suggestions                       │
│  AMÉLIORE: Prochaine estimation plus précise                       │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### 3.2 Métriques Collectées

| Métrique | Usage | Stockage |
|----------|-------|----------|
| **Temps estimé vs réel** | Calibrer estimations | `metrics/velocity.json` |
| **Suggestions acceptées/rejetées** | Améliorer pertinence | `learning/preferences.json` |
| **Erreurs récurrentes** | Prévenir proactivement | `learning/corrections.json` |
| **Patterns de correction** | Suggérer automatiquement | `patterns/detected.json` |
| **Vélocité par type** | Affiner scoring complexité | `metrics/velocity.json` |

### 3.3 Structure des Données d'Apprentissage

```json
// project-memory/learning/corrections.json
{
  "corrections": [
    {
      "id": "corr-001",
      "timestamp": "2025-01-18T14:30:00Z",
      "feature_slug": "user-preferences",
      "type": "security",
      "original_code": "...",
      "corrected_code": "...",
      "reason": "Input validation manquante",
      "pattern_id": "sec-input-validation",
      "agent": "@security-auditor"
    }
  ],
  "patterns": {
    "sec-input-validation": {
      "occurrences": 3,
      "auto_suggest": true,
      "last_seen": "2025-01-18T14:30:00Z"
    }
  }
}
```

```json
// project-memory/learning/preferences.json
{
  "suggestion_feedback": {
    "pattern-extraction": {
      "accepted": 5,
      "rejected": 1,
      "acceptance_rate": 0.83
    },
    "test-generation": {
      "accepted": 8,
      "rejected": 0,
      "acceptance_rate": 1.0
    },
    "n1-query-fix": {
      "accepted": 2,
      "rejected": 3,
      "acceptance_rate": 0.4
    }
  },
  "disabled_suggestions": ["code-style-nitpick"],
  "preferred_patterns": ["repository-pattern", "service-layer"]
}
```

### 3.4 Algorithmes d'Apprentissage

#### Calibration des Estimations

```python
def calibrate_estimation(complexity: str, estimated: float, actual: float):
    """
    Ajuste le modèle d'estimation basé sur les données réelles.

    Uses exponential moving average:
    new_factor = alpha * (actual/estimated) + (1-alpha) * old_factor
    """
    alpha = 0.3  # Poids des nouvelles données
    historical = load_calibration_data(complexity)

    ratio = actual / estimated
    new_factor = alpha * ratio + (1 - alpha) * historical.calibration_factor

    save_calibration_data(complexity, {
        "calibration_factor": new_factor,
        "samples": historical.samples + 1,
        "last_updated": datetime.now()
    })
```

#### Scoring de Suggestion

```python
def calculate_suggestion_score(pattern: str) -> float:
    """
    Calcule le score d'une suggestion basé sur l'historique.

    Score = acceptance_rate * recency_factor * relevance_factor
    """
    prefs = load_preferences()

    if pattern in prefs.disabled_suggestions:
        return 0.0

    feedback = prefs.suggestion_feedback.get(pattern, {})
    acceptance_rate = feedback.get("acceptance_rate", 0.5)  # 50% par défaut

    recency = calculate_recency_factor(feedback.get("last_seen"))
    relevance = calculate_relevance_factor(pattern, current_context)

    return acceptance_rate * recency * relevance
```

### 3.5 Commande `/epci-learn`

```yaml
---
description: Interact with EPCI learning system
argument-hint: "[status|reset|export|calibrate]"
---

# Usage

/epci-learn status      # Affiche état apprentissage
/epci-learn reset       # Réinitialise données apprentissage
/epci-learn export      # Exporte données en JSON
/epci-learn calibrate   # Force recalibration manuelle
/epci-learn feedback    # Interface feedback utilisateur
```

---

## 4. Exigences Techniques

### 4.1 Collecte Métriques

| Exigence | Description | Priorité |
|----------|-------------|----------|
| [MUST] Auto-collecte | Collecter à chaque fin de workflow | P1 |
| [MUST] Timestamps | Horodater toutes les métriques | P1 |
| [MUST] Non-intrusif | Ne pas impacter performance workflow | P1 |
| [SHOULD] Granularité | Métriques par phase, pas juste globales | P2 |

### 4.2 Analyse et Apprentissage

| Exigence | Description | Priorité |
|----------|-------------|----------|
| [MUST] Calibration estimations | Ajuster avec EMA | P1 |
| [MUST] Scoring suggestions | Calculer pertinence | P1 |
| [MUST] Détection patterns | Identifier erreurs récurrentes | P1 |
| [SHOULD] Seuils adaptatifs | Ajuster seuils de complexité | P2 |

### 4.3 Stockage

| Exigence | Description | Priorité |
|----------|-------------|----------|
| [MUST] JSON files | Format lisible et portable | P1 |
| [MUST] Versionning | Schéma versionné | P1 |
| [SHOULD] Pruning | Supprimer données anciennes (> 6 mois) | P2 |
| [SHOULD] Backup | Sauvegarder avant reset | P2 |

---

## 5. Critères d'Acceptation

| ID | Critère | Méthode de vérification |
|----|---------|-------------------------|
| F08-AC1 | Métriques collectées automatiquement | Fichiers `learning/` après workflow |
| F08-AC2 | Estimations améliorées | Variance estimations diminue sur 10+ features |
| F08-AC3 | Suggestions pertinentes | Taux acceptation augmente |
| F08-AC4 | Commande `/epci-learn` fonctionnelle | Test manuel |
| F08-AC5 | Reset avec confirmation | Test `/epci-learn reset` |

---

## 6. Dépendances

### 6.1 Dépendances Entrantes (cette feature dépend de)

| Feature | Type | Description |
|---------|------|-------------|
| F04 Project Memory | **Forte** | Stockage des données d'apprentissage |
| F05 Clarification | Faible | Feedback sur pertinence questions |
| F06 Suggestions | Forte | Feedback sur suggestions |
| F09 Personas | Forte | Apprentissage par persona |

### 6.2 Dépendances Sortantes (dépendent de cette feature)

| Feature | Type | Description |
|---------|------|-------------|
| F03 Breakpoints | Faible | Métriques dans breakpoints |
| F05 Clarification | Faible | Questions améliorées |
| F06 Suggestions | Forte | Suggestions améliorées |

---

## 7. Effort Estimé

| Tâche | Effort |
|-------|--------|
| Collecte métriques | 8h |
| Analyse patterns | 10h |
| Modèle apprentissage (calibration, scoring) | 10h |
| Commande /epci-learn | 4h |
| Tests | 3h |
| **Total** | **35h (4.5j)** |

---

## 8. Livrables

1. Module de collecte de métriques
2. Module d'analyse de patterns
3. Algorithmes de calibration
4. Commande `/epci-learn`
5. Schémas JSON pour données d'apprentissage
6. Documentation utilisateur
7. Tests unitaires et d'intégration

---

## 9. Métriques de Succès

| Métrique | Baseline | Cible après 20 features |
|----------|----------|-------------------------|
| Précision estimations | ±40% | ±15% |
| Taux acceptation suggestions | 50% | 75% |
| Erreurs récurrentes détectées | 0% | 80% |
| Satisfaction utilisateur | N/A | 4.2/5 |

---

## 10. Privacy et Éthique

| Préoccupation | Mesure |
|---------------|--------|
| **Données sensibles** | Ne jamais stocker contenu du code, seulement métriques |
| **Opt-out** | Possibilité de désactiver l'apprentissage |
| **Transparence** | Afficher ce qui est collecté dans `/epci-learn status` |
| **Portabilité** | Export complet des données utilisateur |

---

## 11. Hors Périmètre

- Machine Learning avancé (réseaux de neurones)
- Apprentissage inter-projets (limité au projet courant)
- Apprentissage en temps réel (batch après workflow)
- Partage de modèles entre utilisateurs

---

*Document généré depuis CDC-EPCI-UNIFIE-v4.md*
