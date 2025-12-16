# Cahier des Charges — F04: Project Memory

> **Document**: CDC-F04-001
> **Version**: 1.0.0
> **Date**: 2025-12-15
> **Statut**: Validé
> **Feature ID**: F04
> **Version cible**: EPCI v3.5
> **Priorité**: P1 (CRITIQUE)

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

EPCI v3.0.0 **n'a pas de mémoire entre sessions**. Chaque nouvelle session repart de zéro sans contexte projet.

### 1.3 Glossaire Pertinent

| Terme | Définition |
|-------|------------|
| **Project Memory** | Système de persistance du contexte projet entre sessions |
| **Feature History** | Historique des features développées avec EPCI |
| **Patterns** | Patterns de code détectés ou définis manuellement |
| **Conventions** | Règles de code spécifiques au projet |

---

## 2. Description de la Feature

### 2.1 Contexte et Justification

**Problème critique** : Chaque session Claude Code avec EPCI repart de zéro :
- Pas de mémoire des features passées
- Pas de connaissance des conventions projet
- Pas d'apprentissage des préférences utilisateur
- Redécouverte systématique du contexte

**Solution** : Système de persistance `project-memory/` stockant :
- Contexte projet global
- Historique des features
- Patterns détectés/définis
- Métriques de vélocité
- Données d'apprentissage

### 2.2 Objectif

Permettre à EPCI de :
1. **Se souvenir** du contexte projet entre sessions
2. **Apprendre** des features passées
3. **S'adapter** aux conventions du projet
4. **Améliorer** ses suggestions avec le temps

---

## 3. Spécifications Fonctionnelles

### 3.1 Structure des Fichiers

```
project-memory/
├── context.json              # Contexte projet global
├── conventions.json          # Conventions détectées/définies
├── settings.json             # Configuration EPCI pour ce projet
├── history/
│   ├── features/             # Historique features
│   │   ├── user-auth.json
│   │   └── user-preferences.json
│   └── decisions/            # Décisions architecturales
├── patterns/
│   ├── detected.json         # Patterns auto-détectés
│   └── custom.json           # Patterns définis par user
├── metrics/
│   ├── velocity.json         # Métriques de vélocité
│   └── quality.json          # Métriques qualité
└── learning/
    ├── corrections.json      # Corrections appliquées
    └── preferences.json      # Préférences utilisateur
```

### 3.2 Fichier `context.json`

```json
{
  "project": {
    "name": "my-symfony-app",
    "stack": "php-symfony",
    "detected_at": "2025-01-15T10:00:00Z",
    "framework_version": "7.0",
    "php_version": "8.3"
  },
  "team": {
    "primary_developer": "Édouard",
    "code_style": "PSR-12"
  },
  "integrations": {
    "github": {
      "enabled": true,
      "repository": "owner/repo",
      "branch_pattern": "feature/{slug}"
    },
    "notion": {
      "enabled": true,
      "workspace_id": "xxx",
      "features_database": "yyy"
    }
  },
  "epci": {
    "version": "4.0.0",
    "features_completed": 15,
    "last_session": "2025-01-20T14:30:00Z"
  }
}
```

### 3.3 Fichier `conventions.json`

```json
{
  "naming": {
    "entities": "PascalCase",
    "services": "{Name}Service",
    "repositories": "{Entity}Repository",
    "controllers": "{Domain}Controller"
  },
  "structure": {
    "tests_location": "tests/",
    "test_suffix": "Test.php",
    "feature_tests_pattern": "Feature/{Domain}/{Name}Test.php"
  },
  "code_style": {
    "max_line_length": 120,
    "indent": "spaces",
    "indent_size": 4
  }
}
```

### 3.4 Fichier Feature History

```json
// history/features/user-preferences.json
{
  "slug": "user-preferences",
  "title": "User Preferences Management",
  "created_at": "2025-01-18T09:00:00Z",
  "completed_at": "2025-01-18T14:30:00Z",
  "complexity": "STANDARD",
  "complexity_score": 0.58,
  "files_modified": [
    "src/Entity/UserPreferences.php",
    "src/Repository/UserPreferencesRepository.php",
    "src/Service/UserPreferencesService.php",
    "src/Controller/Api/UserPreferencesController.php"
  ],
  "tests_created": 12,
  "estimated_time": "2h30",
  "actual_time": "2h45",
  "agents_used": ["plan-validator", "code-reviewer"],
  "issues_found": 0,
  "related_features": ["user-auth"]
}
```

### 3.5 Commande `/epci-memory`

```yaml
---
description: Manage project memory
argument-hint: "[status|init|reset|export]"
---

# Usage

/epci-memory status      # Affiche état mémoire
/epci-memory init        # Initialise mémoire projet
/epci-memory reset       # Réinitialise (avec confirmation)
/epci-memory export      # Exporte en JSON
```

---

## 4. Exigences Techniques

### 4.1 Initialisation

| Exigence | Description | Priorité |
|----------|-------------|----------|
| [MUST] Auto-détection stack | Détecter framework, langage, versions | P1 |
| [MUST] Création structure | Créer tous les fichiers/dossiers | P1 |
| [MUST] Valeurs par défaut | Initialiser avec défauts sensés | P1 |
| [SHOULD] Migration | Supporter upgrade de versions | P2 |

### 4.2 Chargement

| Exigence | Description | Priorité |
|----------|-------------|----------|
| [MUST] Auto-load | Charger au démarrage si existe | P1 |
| [MUST] Validation | Valider JSON avant chargement | P1 |
| [MUST] Mode dégradé | Fonctionner si fichiers corrompus | P1 |
| [SHOULD] Lazy loading | Charger à la demande pour gros projets | P2 |

### 4.3 Sauvegarde

| Exigence | Description | Priorité |
|----------|-------------|----------|
| [MUST] Auto-save features | Sauver après chaque feature | P1 |
| [MUST] Atomic writes | Éviter corruption fichiers | P1 |
| [SHOULD] Backup | Garder version précédente | P2 |

### 4.4 Sécurité

| Exigence | Description | Priorité |
|----------|-------------|----------|
| [MUST] Pas de secrets | Ne jamais stocker tokens/passwords | P1 |
| [MUST] Gitignore | Ajouter au .gitignore si sensible | P1 |
| [SHOULD] Sanitization | Nettoyer données avant stockage | P2 |

---

## 5. Critères d'Acceptation

| ID | Critère | Méthode de vérification |
|----|---------|-------------------------|
| F04-AC1 | Structure créée à l'init | `ls project-memory/` |
| F04-AC2 | Context chargé au démarrage | Logs de démarrage |
| F04-AC3 | Historique features sauvé | Après workflow complet |
| F04-AC4 | Export fonctionnel | `/epci-memory export` |
| F04-AC5 | Reset avec confirmation | `/epci-memory reset` |

---

## 6. Dépendances

### 6.1 Dépendances Entrantes (cette feature dépend de)

| Feature | Type | Description |
|---------|------|-------------|
| Aucune | — | Feature fondamentale indépendante |

### 6.2 Dépendances Sortantes (dépendent de cette feature)

| Feature | Type | Description |
|---------|------|-------------|
| F05 Clarification Intelligente | **Forte** | Utilise historique pour questions contextuelles |
| F06 Suggestions Proactives | **Forte** | Utilise patterns pour suggestions |
| F08 Apprentissage Continu | **Forte** | Stocke données d'apprentissage |
| F03 Breakpoints Enrichis | Faible | Métriques historiques |
| INT-01 GitHub | Faible | Config intégration |
| INT-02 Notion | **Forte** | Config et sync |

⚠️ **F04 est une dépendance critique** : 6 features en dépendent directement.

---

## 7. Effort Estimé

| Tâche | Effort |
|-------|--------|
| Structure données (schemas JSON) | 6h |
| Commande /epci-memory | 4h |
| Chargement automatique | 6h |
| Sauvegarde features | 6h |
| Détection patterns | 8h |
| Tests | 4h |
| **Total** | **34h (4.5j)** |

---

## 8. Livrables

1. `project-memory/` — Structure complète
2. `/epci-memory` — Commande de gestion
3. Module de chargement automatique
4. Module de sauvegarde features
5. Module de détection patterns
6. Documentation utilisateur
7. Tests unitaires et d'intégration

---

## 9. Schemas JSON Détaillés

### 9.1 Schema `settings.json`

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "properties": {
    "hooks": {
      "type": "object",
      "properties": {
        "enabled": { "type": "boolean", "default": true },
        "timeout_seconds": { "type": "integer", "default": 30 },
        "fail_on_error": { "type": "boolean", "default": false },
        "active": { "type": "array", "items": { "type": "string" } }
      }
    },
    "breakpoints": {
      "type": "object",
      "properties": {
        "show_metrics": { "type": "boolean", "default": true },
        "show_preview": { "type": "boolean", "default": true },
        "auto_continue_tiny": { "type": "boolean", "default": false }
      }
    },
    "integrations": {
      "type": "object",
      "properties": {
        "github": { "$ref": "#/definitions/github_config" },
        "notion": { "$ref": "#/definitions/notion_config" }
      }
    }
  }
}
```

### 9.2 Schema `velocity.json`

```json
{
  "summary": {
    "total_features": 15,
    "avg_time_standard": "2h15",
    "avg_time_small": "45m",
    "accuracy_estimation": 0.87
  },
  "by_complexity": {
    "TINY": { "count": 5, "avg_time": "12m" },
    "SMALL": { "count": 6, "avg_time": "48m" },
    "STANDARD": { "count": 4, "avg_time": "2h20" }
  },
  "trend": {
    "last_5_features": [
      { "slug": "user-preferences", "estimated": "2h30", "actual": "2h45" },
      { "slug": "notifications", "estimated": "3h", "actual": "2h50" }
    ]
  }
}
```

---

## 10. Hors Périmètre

- Synchronisation cloud de la mémoire projet
- Partage de mémoire entre développeurs (mode équipe)
- Interface graphique pour explorer la mémoire
- Backup automatique sur service externe
- Chiffrement des données

---

*Document généré depuis CDC-EPCI-UNIFIE-v4.md*
