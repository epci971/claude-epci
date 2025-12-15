# Cahier des Charges — F06: Suggestions Proactives

> **Document**: CDC-F06-001
> **Version**: 1.0.0
> **Date**: 2025-12-15
> **Statut**: Validé
> **Feature ID**: F06
> **Version cible**: EPCI v3.5
> **Priorité**: P2

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

EPCI v3.0.0 est **réactif** : il répond aux demandes mais ne propose pas d'améliorations spontanément.

### 1.3 Glossaire Pertinent

| Terme | Définition |
|-------|------------|
| **Suggestion proactive** | Amélioration proposée spontanément par EPCI |
| **Pattern** | Motif de code récurrent détecté ou défini |
| **Technical debt** | Code nécessitant refactoring ou amélioration |
| **Project Memory** | Système de persistance du contexte (F04) |

---

## 2. Description de la Feature

### 2.1 Contexte et Justification

**Problème** : EPCI est purement réactif :
- N'identifie pas les opportunités d'amélioration
- Ne détecte pas les patterns réutilisables
- Ne prévient pas des problèmes potentiels
- N'apprend pas des erreurs passées

**Solution** : Système de suggestions proactives qui :
- Analyse le code pendant le workflow
- Détecte patterns, problèmes, opportunités
- Propose des améliorations avec actions concrètes
- Apprend des acceptations/rejets

### 2.2 Objectif

Faire d'EPCI un **partenaire de développement actif** qui :
1. **Anticipe** les problèmes avant qu'ils surviennent
2. **Propose** des améliorations pertinentes
3. **Apprend** des préférences de l'utilisateur
4. **S'adapte** au contexte du projet

---

## 3. Spécifications Fonctionnelles

### 3.1 Types de Suggestions

| Type | Déclencheur | Exemple |
|------|-------------|---------|
| **Pattern réutilisable** | Code similaire détecté | "Ce service ressemble à UserService, extraire un trait ?" |
| **Test manquant** | Coverage < seuil | "Aucun test pour la méthode `validate()` " |
| **Refactoring** | Dette technique | "Cette classe dépasse 500 lignes, découper ?" |
| **Sécurité** | Pattern risqué | "Input non validé détecté dans `processInput()` " |
| **Performance** | Anti-pattern | "N+1 query potentiel dans la boucle L.45" |

### 3.2 Affichage des Suggestions

```
┌─────────────────────────────────────────────────────────────────────┐
│ 💡 SUGGESTIONS PROACTIVES                                           │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  [P1] 🔒 Sécurité                                                  │
│  └── Le paramètre 'email' n'est pas validé dans register()         │
│      Suggestion: Ajouter Assert\Email                               │
│      [Appliquer] [Ignorer] [Ne plus suggérer]                      │
│                                                                     │
│  [P2] ♻️ Refactoring                                                │
│  └── Pattern Repository similaire à ProductRepository              │
│      Suggestion: Extraire AbstractCrudRepository                   │
│      [Voir détails] [Ignorer]                                      │
│                                                                     │
│  [P3] 🧪 Tests                                                      │
│  └── Méthode calculateDiscount() sans test                         │
│      Suggestion: Ajouter test unitaire                              │
│      [Générer test] [Ignorer]                                      │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### 3.3 Priorités des Suggestions

| Priorité | Type | Urgence | Action recommandée |
|----------|------|---------|-------------------|
| **P1** | Sécurité, bugs critiques | Immédiate | Traiter avant merge |
| **P2** | Qualité, maintenabilité | Normale | Traiter dans la feature |
| **P3** | Optimisation, style | Basse | Backlog optionnel |

### 3.4 Actions sur Suggestions

| Action | Effet | Apprentissage |
|--------|-------|---------------|
| **[Appliquer]** | EPCI applique la correction | +1 pour ce type |
| **[Voir détails]** | Affiche explication complète | Neutre |
| **[Ignorer]** | Skip cette suggestion | Neutre |
| **[Ne plus suggérer]** | Désactive ce type de suggestion | -∞ pour ce pattern |

### 3.5 Moments de Suggestion

| Phase | Suggestions possibles |
|-------|----------------------|
| **Phase 1 (Plan)** | Patterns réutilisables, architecture |
| **Phase 2 (Code)** | Sécurité, tests, refactoring, performance |
| **Phase 3 (Finalize)** | Documentation, changelog, cleanup |
| **Breakpoints** | Récapitulatif des suggestions en attente |

---

## 4. Exigences Techniques

### 4.1 Détection Patterns

| Exigence | Description | Priorité |
|----------|-------------|----------|
| [MUST] Détection similarité code | Identifier code similaire à l'existant | P1 |
| [MUST] Détection anti-patterns | N+1, God class, etc. | P1 |
| [MUST] Analyse sécurité basique | Inputs non validés, SQL injection | P1 |
| [SHOULD] Analyse coverage | Identifier méthodes sans tests | P2 |
| [SHOULD] Métriques complexité | Cyclomatic complexity, LOC | P2 |

### 4.2 Génération Suggestions

| Exigence | Description | Priorité |
|----------|-------------|----------|
| [MUST] Prioritisation | Trier par importance | P1 |
| [MUST] Actions concrètes | Proposer fix, pas juste signaler | P1 |
| [MUST] Explication | Expliquer pourquoi c'est suggéré | P1 |
| [SHOULD] Code preview | Montrer le diff proposé | P2 |

### 4.3 Apprentissage Préférences

| Exigence | Description | Priorité |
|----------|-------------|----------|
| [MUST] Tracking acceptations | Enregistrer choix utilisateur | P1 |
| [MUST] Adaptation | Ajuster priorités selon historique | P1 |
| [SHOULD] Désactivation pattern | "Ne plus suggérer" permanent | P2 |

---

## 5. Critères d'Acceptation

| ID | Critère | Méthode de vérification |
|----|---------|-------------------------|
| F06-AC1 | Suggestions pertinentes générées | Taux acceptation > 70% |
| F06-AC2 | Prioritisation correcte | P1 avant P2 avant P3 |
| F06-AC3 | Action "Ignorer" fonctionne | Ne revient pas dans la session |
| F06-AC4 | Apprentissage préférences | Suggestions adaptées après 10+ interactions |
| F06-AC5 | "Ne plus suggérer" respecté | Pattern désactivé définitivement |

---

## 6. Dépendances

### 6.1 Dépendances Entrantes (cette feature dépend de)

| Feature | Type | Description |
|---------|------|-------------|
| F04 Project Memory | **Forte** | Stockage patterns et préférences |
| F08 Apprentissage Continu | Forte | Modèle d'apprentissage |

### 6.2 Dépendances Sortantes (dépendent de cette feature)

| Feature | Type | Description |
|---------|------|-------------|
| F03 Breakpoints Enrichis | Forte | Affichage suggestions dans breakpoints |

---

## 7. Effort Estimé

| Tâche | Effort |
|-------|--------|
| Détection patterns | 8h |
| Génération suggestions | 6h |
| UI suggestions (breakpoints) | 4h |
| Apprentissage préférences | 4h |
| Tests | 2h |
| **Total** | **24h (3j)** |

---

## 8. Livrables

1. Module de détection patterns
2. Générateur de suggestions
3. Interface utilisateur (dans breakpoints)
4. Module d'apprentissage préférences
5. Documentation utilisateur
6. Tests unitaires et d'intégration

---

## 9. Catalogue de Détections

### 9.1 Sécurité (P1)

| Pattern | Détection | Suggestion |
|---------|-----------|------------|
| Input non validé | Paramètre utilisé sans Assert | Ajouter validation |
| SQL injection | Query string concaténée | Utiliser paramètres |
| XSS | Output non échappé | Échapper avec `htmlspecialchars` |
| CSRF | Formulaire sans token | Ajouter `csrf_token()` |
| Auth manquante | Controller sans `@IsGranted` | Ajouter contrôle accès |

### 9.2 Performance (P2)

| Pattern | Détection | Suggestion |
|---------|-----------|------------|
| N+1 query | Boucle avec query imbriquée | JOIN FETCH ou batch |
| Missing index | Query sur colonne non indexée | Ajouter index |
| Large payload | Response > 1MB | Paginer ou streamer |
| No cache | Query répétée identique | Ajouter cache |

### 9.3 Qualité (P2-P3)

| Pattern | Détection | Suggestion |
|---------|-----------|------------|
| God class | Classe > 500 LOC | Découper responsabilités |
| Long method | Méthode > 50 LOC | Extraire sous-méthodes |
| Magic numbers | Constantes en dur | Extraire constantes |
| Dead code | Code jamais atteint | Supprimer |
| Duplicate code | Blocs similaires > 20 LOC | Extraire méthode commune |

---

## 10. Algorithme de Scoring

```python
def calculate_suggestion_priority(suggestion: Suggestion) -> Priority:
    """
    Calcule la priorité d'une suggestion basée sur:
    - Type (sécurité > performance > qualité)
    - Impact (critique > modéré > mineur)
    - Historique utilisateur (préférences)
    """
    base_score = PRIORITY_WEIGHTS[suggestion.type]  # security=100, perf=70, quality=50

    # Ajuster selon impact
    impact_multiplier = {
        "critical": 1.5,
        "moderate": 1.0,
        "minor": 0.7
    }[suggestion.impact]

    # Ajuster selon préférences utilisateur
    user_preference = project_memory.get_preference_score(suggestion.pattern)
    preference_multiplier = 1.0 + (user_preference * 0.2)  # -1 à +1 → 0.8 à 1.2

    final_score = base_score * impact_multiplier * preference_multiplier

    if final_score >= 80:
        return Priority.P1
    elif final_score >= 50:
        return Priority.P2
    else:
        return Priority.P3
```

---

## 11. Hors Périmètre

- Suggestions automatiquement appliquées (toujours avec confirmation)
- Analyse statique complète (type SonarQube)
- Suggestions inter-projets (limité au projet courant)
- Apprentissage machine avancé (règles simples)

---

*Document généré depuis CDC-EPCI-UNIFIE-v4.md*
