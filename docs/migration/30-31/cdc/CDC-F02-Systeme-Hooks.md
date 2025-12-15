# Cahier des Charges — F02: Système de Hooks

> **Document**: CDC-F02-001
> **Version**: 1.0.0
> **Date**: 2025-12-15
> **Statut**: Validé
> **Feature ID**: F02
> **Version cible**: EPCI v3.1
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

Le plugin EPCI v3.0.0 est opérationnel avec **23 composants validés** :
- 5 commandes
- 5 subagents
- 13 skills

### 1.3 Glossaire Pertinent

| Terme | Définition |
|-------|------------|
| **Hook** | Script exécuté automatiquement à un point précis du workflow EPCI |
| **Breakpoint** | Point de pause nécessitant confirmation utilisateur |
| **Phase** | Étape du workflow EPCI (Phase 1: Plan, Phase 2: Code, Phase 3: Finalize) |

---

## 2. Description de la Feature

### 2.1 Contexte et Justification

Le dossier `hooks/` existe dans la structure EPCI mais est **vide**. Les utilisateurs n'ont actuellement **aucun moyen** d'exécuter des actions automatiques à des points précis du workflow.

**Problème** : Pas d'extensibilité du workflow sans modifier le code source.

**Solution** : Système de hooks permettant d'injecter des scripts custom à 7 points du workflow.

### 2.2 Objectif

Permettre aux utilisateurs de :
1. Exécuter des scripts custom avant/après chaque phase
2. Logger des métriques ou notifier des systèmes externes
3. Intégrer des outils de qualité (linters, formatters) automatiquement
4. Personnaliser le workflow sans modifier le core EPCI

---

## 3. Spécifications Fonctionnelles

### 3.1 Types de Hooks

| Hook | Déclencheur | Cas d'usage |
|------|-------------|-------------|
| `pre-phase-1` | Avant Phase 1 (Planning) | Vérifier prérequis, charger contexte |
| `post-phase-1` | Après Phase 1 | Notifier équipe, créer ticket |
| `pre-phase-2` | Avant Phase 2 (Code) | Setup environnement, linters |
| `post-phase-2` | Après Phase 2 | Run tests supplémentaires, coverage |
| `pre-phase-3` | Avant Phase 3 (Finalize) | Vérifier tests passent |
| `post-phase-3` | Après Phase 3 | Déployer, notifier |
| `on-breakpoint` | À chaque breakpoint | Logging, métriques |

### 3.2 Structure des Fichiers

```
hooks/
├── README.md                    # Documentation
├── runner.py                    # Exécuteur de hooks
├── examples/
│   ├── pre-phase-2-lint.sh     # Exemple linter
│   ├── post-phase-3-notify.py  # Exemple notification
│   └── on-breakpoint-log.sh    # Exemple logging
└── active/                      # Hooks actifs (symlinks)
```

### 3.3 Format d'un Hook

```python
#!/usr/bin/env python3
"""
Hook: post-phase-2
Description: Run additional quality checks after implementation
"""

import sys
import json

def main(context: dict) -> dict:
    """
    Args:
        context: {
            "phase": "phase-2",
            "feature_slug": "user-preferences",
            "files_modified": [...],
            "test_results": {...}
        }

    Returns:
        {"status": "success|warning|error", "message": "..."}
    """
    # Hook logic here
    return {"status": "success", "message": "Quality checks passed"}

if __name__ == "__main__":
    context = json.loads(sys.stdin.read())
    result = main(context)
    print(json.dumps(result))
```

### 3.4 Configuration

```json
// project-memory/settings.json
{
  "hooks": {
    "enabled": true,
    "timeout_seconds": 30,
    "fail_on_error": false,
    "active": [
      "pre-phase-2-lint",
      "post-phase-3-notify"
    ]
  }
}
```

### 3.5 Contexte Passé aux Hooks

| Champ | Type | Description |
|-------|------|-------------|
| `phase` | string | Phase courante (phase-1, phase-2, phase-3) |
| `feature_slug` | string | Slug de la feature en cours |
| `files_modified` | array | Liste des fichiers modifiés |
| `test_results` | object | Résultats des tests (si disponibles) |
| `breakpoint_type` | string | Type de breakpoint (pour on-breakpoint) |
| `timestamp` | string | ISO 8601 timestamp |

---

## 4. Exigences Techniques

### 4.1 Runner de Hooks (`runner.py`)

| Exigence | Description | Priorité |
|----------|-------------|----------|
| [MUST] Découverte auto | Scanner `hooks/active/` pour hooks actifs | P1 |
| [MUST] Exécution isolée | Chaque hook dans subprocess | P1 |
| [MUST] Timeout | Respecter `timeout_seconds` configurable | P1 |
| [MUST] Passage contexte | JSON via stdin | P1 |
| [MUST] Capture output | Capturer stdout/stderr | P1 |
| [SHOULD] Logging | Logger exécution et résultats | P2 |
| [SHOULD] Parallélisation | Option pour hooks parallèles | P2 |

### 4.2 Gestion des Erreurs

| Situation | Comportement si `fail_on_error: false` | Comportement si `fail_on_error: true` |
|-----------|----------------------------------------|---------------------------------------|
| Hook timeout | Warning, continue workflow | Stop workflow, afficher erreur |
| Hook exit code ≠ 0 | Warning, continue workflow | Stop workflow, afficher erreur |
| Hook non trouvé | Warning, skip | Warning, skip |
| JSON invalide retourné | Warning, continue | Stop workflow |

### 4.3 Langages Supportés

| Langage | Extension | Shebang requis |
|---------|-----------|----------------|
| Python | `.py` | `#!/usr/bin/env python3` |
| Bash | `.sh` | `#!/bin/bash` |
| Node.js | `.js` | `#!/usr/bin/env node` |

---

## 5. Critères d'Acceptation

| ID | Critère | Méthode de vérification |
|----|---------|-------------------------|
| F02-AC1 | runner.py exécute hooks | Test manuel avec hook de debug |
| F02-AC2 | 7 points de hook disponibles | Documentation + tests |
| F02-AC3 | Timeout respecté | Test avec hook `sleep 60` et timeout 5s |
| F02-AC4 | Contexte passé correctement | Test avec hook qui log le contexte |
| F02-AC5 | Mode dégradé si hook échoue | Test avec hook qui `exit 1` |

---

## 6. Dépendances

### 6.1 Dépendances Entrantes (cette feature dépend de)

| Feature | Type | Description |
|---------|------|-------------|
| Aucune | — | Feature indépendante |

### 6.2 Dépendances Sortantes (dépendent de cette feature)

| Feature | Type | Description |
|---------|------|-------------|
| F03 Breakpoints Enrichis | Faible | Hook `on-breakpoint` enrichit les breakpoints |
| F07 Orchestration Multi-Agents | Forte | Les hooks s'intègrent dans l'orchestration |

---

## 7. Effort Estimé

| Tâche | Effort |
|-------|--------|
| runner.py (core) | 6h |
| Documentation README.md | 2h |
| 3 exemples hooks | 3h |
| Intégration workflow EPCI | 4h |
| Tests | 3h |
| **Total** | **18h (2.5j)** |

---

## 8. Livrables

1. `hooks/runner.py` — Exécuteur de hooks
2. `hooks/README.md` — Documentation utilisateur
3. `hooks/examples/pre-phase-2-lint.sh` — Exemple linter
4. `hooks/examples/post-phase-3-notify.py` — Exemple notification
5. `hooks/examples/on-breakpoint-log.sh` — Exemple logging
6. `hooks/active/` — Dossier pour hooks actifs (symlinks)

---

## 9. Exemples d'Usage

### 9.1 Hook Linter Pre-Phase-2

```bash
#!/bin/bash
# hooks/examples/pre-phase-2-lint.sh
# Description: Run ESLint/Prettier before coding phase

echo "Running linters..."
npm run lint:fix 2>&1

if [ $? -eq 0 ]; then
    echo '{"status": "success", "message": "Linting passed"}'
else
    echo '{"status": "warning", "message": "Linting had issues, please review"}'
fi
```

### 9.2 Hook Notification Post-Phase-3

```python
#!/usr/bin/env python3
# hooks/examples/post-phase-3-notify.py
# Description: Send Slack notification when feature is complete

import sys
import json
import requests

def main(context):
    feature = context.get("feature_slug", "unknown")
    message = f"✅ Feature `{feature}` completed!"

    # Envoyer à Slack (exemple)
    # requests.post(SLACK_WEBHOOK, json={"text": message})

    return {"status": "success", "message": f"Notified: {feature}"}

if __name__ == "__main__":
    ctx = json.loads(sys.stdin.read())
    print(json.dumps(main(ctx)))
```

---

## 10. Hors Périmètre

- Interface graphique pour gérer les hooks
- Marketplace de hooks communautaires
- Hooks asynchrones avec queue
- Hooks distribués sur plusieurs machines

---

*Document généré depuis CDC-EPCI-UNIFIE-v4.md*
