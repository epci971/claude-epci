# Feature Document — F02: Système de Hooks

> **Feature ID**: F02
> **Version cible**: EPCI v3.1
> **Date**: 2025-12-15
> **Statut**: En cours

---

## §1 — Brief Fonctionnel

### Contexte

Le dossier `hooks/` existe dans la structure EPCI mais est **vide**. Les utilisateurs n'ont actuellement aucun moyen d'exécuter des actions automatiques à des points précis du workflow `/epci`. Cette feature transforme ce dossier vide en un système fonctionnel permettant d'injecter des scripts personnalisés à 7 points du workflow.

### Objectif

Permettre aux utilisateurs de :
1. Exécuter des scripts custom avant/après chaque phase
2. Logger des métriques ou notifier des systèmes externes
3. Intégrer des outils de qualité (linters, formatters) automatiquement
4. Personnaliser le workflow sans modifier le core EPCI

### Stack Détectée

| Composant | Technologie |
|-----------|-------------|
| Plugin | Claude Code Plugin v3.0 (Markdown + YAML frontmatter) |
| Runner | Python 3 (scripts dans `src/scripts/`) |
| Hooks | Python (.py), Bash (.sh), Node.js (.js) |
| Config | JSON (project-memory/settings.json) |

### Critères d'Acceptation

- [ ] **AC1**: runner.py exécute les hooks correctement
- [ ] **AC2**: 7 points de hook disponibles (pre/post-phase-1/2/3, on-breakpoint)
- [ ] **AC3**: Timeout respecté (configurable, défaut 30s)
- [ ] **AC4**: Contexte JSON passé correctement aux hooks via stdin
- [ ] **AC5**: Mode dégradé si hook échoue (continue avec warning si `fail_on_error: false`)

### Contraintes

- Langages supportés : Python, Bash, Node.js (via shebang)
- Timeout : défaut 30s, max 5 min
- Isolation : chaque hook dans subprocess isolé
- Communication : JSON via stdin, JSON en retour
- Compatibilité : non-breaking avec workflow `/epci` existant

### Hors Périmètre

- Interface graphique pour gérer les hooks
- Marketplace de hooks communautaires
- Hooks asynchrones avec queue
- Hooks distribués sur plusieurs machines

---

## §2 — Plan d'Implémentation

### Fichiers Impactés

| Fichier | Action | Risque | Description |
|---------|--------|--------|-------------|
| `src/hooks/runner.py` | Créer | Moyen | Moteur d'exécution des hooks (~150 LOC) |
| `src/hooks/README.md` | Créer | Faible | Documentation utilisateur |
| `src/hooks/examples/pre-phase-2-lint.sh` | Créer | Faible | Exemple hook linter |
| `src/hooks/examples/post-phase-3-notify.py` | Créer | Faible | Exemple hook notification |
| `src/hooks/examples/on-breakpoint-log.sh` | Créer | Faible | Exemple hook logging |
| `src/hooks/active/.gitkeep` | Créer | Faible | Placeholder pour hooks actifs |
| `src/commands/epci.md` | Modifier | Moyen | Intégration 7 points de hook |
| `CLAUDE.md` | Modifier | Faible | Documentation hooks |

### Tâches

#### Phase A: Infrastructure Core (runner.py)

1. [ ] **Créer structure runner.py avec dataclasses** (10 min)
   - Fichier: `src/hooks/runner.py`
   - Dataclasses: `HookConfig`, `HookContext`, `HookResult`
   - Pattern: suivre `validate_all.py`

2. [ ] **Implémenter découverte de hooks** (10 min)
   - Fichier: `src/hooks/runner.py`
   - Fonction: `discover_hooks(hooks_dir, hook_type)`
   - Scanner `hooks/active/` pour scripts actifs

3. [ ] **Implémenter exécution hook + timeout** (15 min)
   - Fichier: `src/hooks/runner.py`
   - Fonction: `execute_hook(path, context, config)`
   - Subprocess avec timeout configurable

4. [ ] **Implémenter dispatcher et CLI** (10 min)
   - Fichier: `src/hooks/runner.py`
   - Fonction: `run_hooks(hook_type, context)`
   - CLI pour tests manuels

#### Phase B: Exemples

5. [ ] **Créer exemple pre-phase-2-lint.sh** (5 min)
   - Fichier: `src/hooks/examples/pre-phase-2-lint.sh`
   - Script Bash exécutant linter

6. [ ] **Créer exemple post-phase-3-notify.py** (5 min)
   - Fichier: `src/hooks/examples/post-phase-3-notify.py`
   - Script Python notification template

7. [ ] **Créer exemple on-breakpoint-log.sh** (5 min)
   - Fichier: `src/hooks/examples/on-breakpoint-log.sh`
   - Script Bash logging contexte

#### Phase C: Intégration epci.md

8. [ ] **Ajouter invocations hooks dans epci.md** (15 min)
   - Fichier: `src/commands/epci.md`
   - 7 points: pre/post-phase-1/2/3 + on-breakpoint

#### Phase D: Documentation

9. [ ] **Créer hooks/README.md** (10 min)
   - Fichier: `src/hooks/README.md`
   - Guide utilisateur complet

10. [ ] **Mettre à jour CLAUDE.md** (5 min)
    - Fichier: `CLAUDE.md`
    - Section hooks dans documentation développeur

### Risques

| Risque | Probabilité | Impact | Mitigation |
|--------|-------------|--------|------------|
| Subprocess blocking | Moyenne | Élevé | Timeout strict (30s défaut) |
| JSON malformé retourné | Moyenne | Moyen | Try/except + mode dégradé |
| Sécurité hooks malveillants | Faible | Élevé | Documentation + avertissements |
| Complexité intégration epci.md | Faible | Moyen | Instructions minimales, références README |

### Architecture runner.py

```
┌─────────────────────────────────────────────────────────────────┐
│                         runner.py                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Dataclasses:                                                    │
│  ├── HookConfig (enabled, timeout, fail_on_error)               │
│  ├── HookContext (phase, feature_slug, files, timestamp)        │
│  └── HookResult (status, message, duration_ms)                  │
│                                                                  │
│  Core Functions:                                                 │
│  ├── discover_hooks(hooks_dir, hook_type) → List[Path]          │
│  ├── execute_hook(path, context, config) → HookResult           │
│  └── run_hooks(hook_type, context_dict) → List[HookResult]      │
│                                                                  │
│  CLI:                                                            │
│  └── main() → argparse interface for testing                    │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Points d'Intégration epci.md

| Point | Emplacement | Hook Type |
|-------|-------------|-----------|
| Début Phase 1 | Après ligne 46 | `pre-phase-1` |
| Fin Phase 1 | Avant BP1 (ligne 107) | `post-phase-1` |
| Début Phase 2 | Après ligne 156 | `pre-phase-2` |
| Fin Phase 2 | Avant BP2 (ligne 224) | `post-phase-2` |
| Début Phase 3 | Après ligne 275 | `pre-phase-3` |
| Fin Phase 3 | Après ligne 335 | `post-phase-3` |
| Breakpoints | BP1 et BP2 | `on-breakpoint` |

### Validation

- **@plan-validator**: APPROVED
  - Completeness: ✅ Tous les AC couverts
  - Consistency: ✅ Dépendances logiques
  - Feasibility: ✅ Estimations réalistes
  - Quality: ✅ Risques mitigés

---

## §3 — Implémentation

### Progression

- [x] Tâche 1 — Créer runner.py avec dataclasses
- [x] Tâche 2 — Implémenter découverte hooks
- [x] Tâche 3 — Implémenter exécution + timeout
- [x] Tâche 4 — Implémenter dispatcher et CLI
- [x] Tâche 5 — Créer exemple pre-phase-2-lint.sh
- [x] Tâche 6 — Créer exemple post-phase-3-notify.py
- [x] Tâche 7 — Créer exemple on-breakpoint-log.sh
- [x] Tâche 8 — Intégrer hooks dans epci.md
- [x] Tâche 9 — Créer hooks/README.md
- [x] Tâche 10 — Mettre à jour CLAUDE.md

### Fichiers Créés

| Fichier | LOC | Description |
|---------|-----|-------------|
| `src/hooks/runner.py` | ~350 | Moteur d'exécution des hooks |
| `src/hooks/README.md` | ~300 | Documentation utilisateur |
| `src/hooks/examples/pre-phase-2-lint.sh` | ~60 | Exemple linter (Bash) |
| `src/hooks/examples/post-phase-3-notify.py` | ~80 | Exemple notification (Python) |
| `src/hooks/examples/on-breakpoint-log.sh` | ~35 | Exemple logging (Bash) |
| `src/hooks/active/.gitkeep` | 4 | Placeholder |

### Fichiers Modifiés

| Fichier | Modifications |
|---------|---------------|
| `src/commands/epci.md` | +50 LOC — Section Hooks Integration + 7 points d'invocation |
| `CLAUDE.md` | +60 LOC — Section 3.6 Système de Hooks + structure |

### Tests

```bash
# Test du runner CLI
python src/hooks/runner.py --list
# Hook types disponibles, répertoires affichés

# Test exécution hook
echo '{"phase": "phase-2"}' | ./src/hooks/examples/pre-phase-2-lint.sh
# {"status": "success", "message": "No linter configured"}
```

### Déviations

| Tâche | Déviation | Justification |
|-------|-----------|---------------|
| - | Aucune déviation | Implémentation conforme au plan |

### Reviews

- **@code-reviewer**: APPROVED_WITH_FIXES
  - Issues corrigées:
    - ✅ CRLF → LF (tous les fichiers)
    - ✅ Shebang security (ajout `_get_safe_interpreter`)
    - ✅ Explicit bash interpreter pour `.sh`
  - Points positifs:
    - Architecture robuste avec dataclasses
    - Gestion complète des erreurs (timeout, permissions, JSON)
    - Sécurité subprocess (pas de `shell=True`)

---

## §4 — Finalisation

### Commit

```
feat(hooks): add extensible hook system for EPCI workflow

- Add hooks/runner.py with subprocess execution, timeout, JSON I/O
- Add 3 example hooks: linter, notification, logging
- Add safe interpreter whitelist for shebang security
- Integrate 7 hook points in /epci command (pre/post phases, breakpoints)
- Add comprehensive hooks/README.md documentation
- Update CLAUDE.md with hooks system documentation

Implements F02: Système de Hooks for EPCI v3.1

Refs: docs/features/f02-systeme-hooks.md
```

### Documentation

- **CHANGELOG.md**: Entrée F02 ajoutée sous [Unreleased]
- **CLAUDE.md**: Section 3.6 "Système de Hooks" ajoutée
- **hooks/README.md**: Documentation utilisateur complète

### Fichiers Créés

| Fichier | Description |
|---------|-------------|
| `src/hooks/runner.py` | Moteur d'exécution (~400 LOC) |
| `src/hooks/README.md` | Documentation utilisateur |
| `src/hooks/examples/pre-phase-2-lint.sh` | Exemple linter |
| `src/hooks/examples/post-phase-3-notify.py` | Exemple notification |
| `src/hooks/examples/on-breakpoint-log.sh` | Exemple logging |
| `src/hooks/active/.gitkeep` | Placeholder |
| `docs/features/f02-systeme-hooks.md` | Feature Document |

### Fichiers Modifiés

| Fichier | Modifications |
|---------|---------------|
| `src/commands/epci.md` | +50 LOC (Hooks Integration + 7 points) |
| `CLAUDE.md` | +60 LOC (Section 3.6 + structure) |
| `CHANGELOG.md` | Entrée F02 |

### Validation Finale

- [x] Phase 1: Plan validé par @plan-validator
- [x] Phase 2: Code implémenté et reviewé par @code-reviewer
- [x] Phase 3: Documentation complète, CHANGELOG mis à jour
- [x] Tests: CLI runner fonctionnel
- [x] Critères d'acceptation: AC1-AC5 satisfaits
