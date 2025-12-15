# Cahier des Charges — F11: Wave Orchestration

> **Document**: CDC-F11-001
> **Version**: 1.0.0
> **Date**: 2025-12-15
> **Statut**: Validé
> **Feature ID**: F11
> **Version cible**: EPCI v4.0
> **Priorité**: P2
> **Source**: Analyse WD Framework v2.0 [NEW]

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

Les features LARGE sont traitées de manière **monolithique**. Risque de perte de contexte sur les longues exécutions.

### 1.3 Glossaire Pertinent

| Terme | Définition |
|-------|------------|
| **Wave** | Vague d'exécution dans une orchestration multi-étapes |
| **Progressive** | Stratégie itérative avec validation entre vagues |
| **Systematic** | Stratégie d'analyse complète avant exécution |
| **Context accumulation** | Chaque vague hérite du contexte des précédentes |

---

## 2. Description de la Feature

### 2.1 Contexte et Justification

**Source** : Analyse comparative WD Framework v2.0

**Problème** : L'exécution monolithique des features LARGE :
- Perd le fil sur les longues exécutions
- Ne permet pas de validation intermédiaire
- Accumule les erreurs sans correction
- Sous-utilise le contexte acquis

**Solution** : Découpage en "vagues" avec :
- Accumulation progressive du contexte
- Validation optionnelle entre vagues
- Stratégies adaptées (progressive vs systematic)
- Amélioration qualité de 30-50%

### 2.2 Objectif

Améliorer la qualité des features LARGE de **30-50%** via un découpage intelligent en vagues avec accumulation de contexte.

---

## 3. Concept Wave

### 3.1 Comparaison Sans/Avec Wave

```
┌─────────────────────────────────────────────────────────────────────┐
│                    WAVE ORCHESTRATION                               │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  SANS WAVE (actuel --large)                                        │
│  ════════════════════════════════════════════════════════►         │
│  Exécution monolithique, risque de perdre le fil                   │
│                                                                     │
│  AVEC WAVE (--wave)                                                │
│                                                                     │
│  ┌─────────┐     ┌─────────┐     ┌─────────┐     ┌─────────┐      │
│  │ Vague 1 │ ──► │ Vague 2 │ ──► │ Vague 3 │ ──► │ Vague 4 │      │
│  │ Analyse │     │  Core   │     │ Périph. │     │  Tests  │      │
│  │ + Fonda.│     │         │     │         │     │ + Docs  │      │
│  └────┬────┘     └────┬────┘     └────┬────┘     └────┬────┘      │
│       │               │               │               │            │
│       ▼               ▼               ▼               ▼            │
│   Contexte        Contexte        Contexte        Contexte         │
│   initial         enrichi         complet          final           │
│                                                                     │
│  Breakpoint optionnel entre chaque vague (si --safe)               │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### 3.2 Stratégies

| Stratégie | Description | Cas d'usage |
|-----------|-------------|-------------|
| **progressive** | Vague par vague avec validation | Incertitude, besoin feedback fréquent |
| **systematic** | Analyse complète d'abord, puis exécution groupée | Feature bien définie, confiance élevée |

---

## 4. Découpage Automatique

### 4.1 Exemple de Découpage

**Feature** : "Système de notifications multi-canal"
**Complexité** : LARGE (score: 0.82)
**Stratégie** : progressive

```
┌─────────────────────────────────────────────────────────────────────┐
│ VAGUE 1 — Fondations                                               │
├─────────────────────────────────────────────────────────────────────┤
│ ├── Entité Notification                                            │
│ ├── NotificationRepository                                         │
│ ├── NotificationService (base)                                     │
│ └── Tests unitaires fondations                                     │
│                                                                     │
│ Contexte acquis: Structure données, interfaces de base             │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│ VAGUE 2 — Canaux                                                   │
├─────────────────────────────────────────────────────────────────────┤
│ ├── NotificationChannelInterface                                   │
│ ├── EmailNotificationChannel                                       │
│ ├── PushNotificationChannel                                        │
│ ├── InAppNotificationChannel                                       │
│ └── Tests unitaires canaux                                         │
│                                                                     │
│ Contexte enrichi: Patterns canal, templates                        │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│ VAGUE 3 — Orchestration                                            │
├─────────────────────────────────────────────────────────────────────┤
│ ├── NotificationDispatcher                                         │
│ ├── Integration Symfony Messenger                                  │
│ ├── Retry logic + Dead letter                                      │
│ └── Tests intégration                                              │
│                                                                     │
│ Contexte complet: Flow complet, edge cases                         │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│ VAGUE 4 — Finalisation                                             │
├─────────────────────────────────────────────────────────────────────┤
│ ├── Tests E2E                                                      │
│ ├── Documentation API                                              │
│ ├── Migration script                                               │
│ └── Feature Document §3-§4                                         │
│                                                                     │
│ Contexte final: Prêt pour review                                   │
└─────────────────────────────────────────────────────────────────────┘
```

### 4.2 Algorithme de Découpage

```python
def plan_waves(feature: Feature, strategy: str) -> List[Wave]:
    """
    Découpe une feature en vagues selon la stratégie.
    """
    tasks = feature.planned_tasks
    waves = []

    if strategy == "progressive":
        # Découpage par couche architecturale
        waves = [
            Wave("Fondations", filter_tasks(tasks, ["entity", "repository", "base"])),
            Wave("Core Logic", filter_tasks(tasks, ["service", "handler", "logic"])),
            Wave("Integration", filter_tasks(tasks, ["controller", "api", "integration"])),
            Wave("Finalization", filter_tasks(tasks, ["test", "doc", "migration"]))
        ]
    elif strategy == "systematic":
        # Analyse complète d'abord
        analysis_wave = Wave("Analysis", [AnalyzeAllTask()])
        execution_waves = chunk_by_dependency(tasks)
        waves = [analysis_wave] + execution_waves

    # Filtrer vagues vides
    return [w for w in waves if w.tasks]
```

### 4.3 Accumulation de Contexte

Chaque vague hérite et enrichit le contexte :

```python
@dataclass
class WaveContext:
    wave_number: int
    files_created: List[str]
    files_modified: List[str]
    patterns_used: List[str]
    tests_status: Dict[str, str]
    issues_found: List[Issue]
    decisions_made: List[Decision]

def execute_wave(wave: Wave, previous_context: WaveContext) -> WaveContext:
    """
    Exécute une vague avec le contexte des vagues précédentes.
    """
    # Le contexte précédent est passé à Claude
    # Claude peut référencer les fichiers créés, patterns utilisés, etc.
    ...
```

---

## 5. Intégration avec Flags

### 5.1 Activation

```bash
# Activation explicite
/epci --wave --wave-strategy progressive

# Activation implicite (LARGE + think-hard)
/epci --think-hard   # Si LARGE détecté → --wave auto

# Forcer sans wave même si LARGE
/epci --think-hard --no-wave
```

### 5.2 Breakpoints Entre Vagues

Avec `--safe`, breakpoint entre chaque vague :

```
┌─────────────────────────────────────────────────────────────────────┐
│ ⏸️  BREAKPOINT WAVE 2/4 — Core Logic Complete                       │
├─────────────────────────────────────────────────────────────────────┤
│ 📊 Vague 2: 8/8 tâches | Tests: 15 ✅ | Coverage: 78%              │
│ 🔄 Contexte: 12 fichiers créés, pattern Service Layer              │
│ 📋 Prochaine vague: Integration (6 tâches)                         │
├─────────────────────────────────────────────────────────────────────┤
│ [Continuer Wave 3] [Revoir Wave 2] [Voir contexte] [Annuler]       │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 6. Critères d'Acceptation

| ID | Critère | Méthode de vérification |
|----|---------|-------------------------|
| F11-AC1 | Découpage automatique | Test feature LARGE |
| F11-AC2 | 2 stratégies fonctionnelles | Test progressive et systematic |
| F11-AC3 | Contexte accumulé | Vague N voit résultats N-1 |
| F11-AC4 | Breakpoints entre vagues (si --safe) | Test mode safe |
| F11-AC5 | Intégration F07 Orchestration | Agents par vague |

---

## 7. Dépendances

### 7.1 Dépendances Entrantes (cette feature dépend de)

| Feature | Type | Description |
|---------|------|-------------|
| F07 Orchestration | **Forte** | Wave utilise l'orchestrator |
| F10 Flags | Forte | `--wave*` flags |

### 7.2 Dépendances Sortantes (dépendent de cette feature)

| Feature | Type | Description |
|---------|------|-------------|
| Aucune | — | Feature terminale |

---

## 8. Effort Estimé

| Tâche | Effort |
|-------|--------|
| Wave planner | 8h |
| Stratégie progressive | 4h |
| Stratégie systematic | 4h |
| Accumulation contexte | 6h |
| Intégration orchestrator | 6h |
| Tests | 4h |
| **Total** | **32h (4j)** |

---

## 9. Livrables

1. Module Wave Planner
2. Stratégie Progressive
3. Stratégie Systematic
4. Module d'accumulation de contexte
5. Intégration avec Orchestrator (F07)
6. Documentation utilisateur
7. Tests unitaires et d'intégration

---

## 10. Métriques de Succès

| Métrique | Sans Wave | Avec Wave | Amélioration |
|----------|-----------|-----------|--------------|
| Qualité code LARGE | Baseline | +30-50% | Mesure revue |
| Erreurs accumulées | X | X/2 | 50% réduction |
| Temps correction | Baseline | -20% | Détection plus tôt |
| Satisfaction utilisateur | 3.5/5 | 4.2/5 | +20% |

---

## 11. Hors Périmètre

- Waves parallèles (toujours séquentielles)
- Persistence cross-session des waves
- Rollback automatique de vague
- Customisation du nombre de vagues

---

*Document généré depuis CDC-EPCI-UNIFIE-v4.md*
