# Feature Brief — EPCI v5 Improvements

> **Slug**: `epci-v5-improvements`
> **Category**: LARGE
> **Date**: 2024-12-31
> **Source**: Audit de coherence workflow v4.4

---

## Context

Suite a un audit complet du workflow EPCI v4.4.0, plusieurs problemes de coherence et lacunes fonctionnelles ont ete identifies. Ce brief decrit les ameliorations necessaires pour la version 5.0.

### Score Actuel du Workflow

| Metrique | Score |
|----------|-------|
| Structure interne | 85/100 |
| Documentation | 65/100 |
| Execution runtime | 60/100 |
| **Global** | **70/100** |

**Objectif v5** : Atteindre 85/100 global

---

## Problemes Identifies

### P1 — Hooks Non Automatiques (Critique)

**Symptome** : La memoire projet n'est jamais mise a jour malgre les features completees.

**Cause** : Les hooks `post-phase-3` sont documentes dans les fichiers markdown mais dependent de Claude pour les executer manuellement. Claude peut oublier ou ignorer ces instructions.

**Impact** :
- `.project-memory/history/features/` reste vide
- Metriques de velocite incorrectes
- `/memory` retourne des donnees obsoletes
- Calibration temps impossible

**Solution Proposee** :
1. Creer un wrapper Python qui force l'execution des hooks
2. Ajouter verification en fin de workflow
3. Alerter si hook non execute

### P2 — Documentation Desynchronisee (Importante)

**Symptome** : CLAUDE.md declare 6 agents, il y en a 9.

**Cause** : Ajout des agents `@clarifier`, `@planner`, `@implementer` pour les modes turbo/quick sans mise a jour de la documentation.

**Impact** :
- Confusion utilisateur
- Incoherence interne (epci-core skill aussi desynchronise)

**Solution** :
1. Mettre a jour CLAUDE.md section 5 (Subagents)
2. Mettre a jour epci-core skill
3. Creer AGENTS_MATRIX.md

### P3 — Absence de State Machine (Importante)

**Symptome** : Impossible de reprendre un workflow interrompu.

**Cause** : Pas d'etat persistant du workflow.

**Impact** :
- Si erreur Phase 2, tout recommencer
- Pas de rollback possible
- Pas de visibilite sur l'etat courant

**Solution** :
1. Creer `.epci-state.json` pour tracker l'etat
2. Ajouter `--resume` et `--rollback` flags
3. Persister checkpoints a chaque phase

### P4 — Validation Prerequis Absente (Moyenne)

**Symptome** : `/epci` peut etre lance sans Feature Document.

**Cause** : Pas de verification au debut des commandes.

**Impact** :
- Erreurs cryptiques en cours de workflow
- Perte de temps

**Solution** :
1. Ajouter validation prerequis en debut de chaque commande
2. Messages d'erreur clairs avec next step

### P5 — Fragmentation Skills (Moyenne)

**Symptome** : 23 skills rendent la maintenance difficile.

**Cause** : Decoupage trop granulaire.

**Impact** :
- Difficulte a comprendre le systeme
- Duplication de concepts
- Maintenance couteuse

**Solution** :
1. Fusionner skills similaires (13 core → 5-6)
2. Creer SKILLS_MATRIX.md pour documentation

---

## Specifications Fonctionnelles

### F1 — State Machine Workflow

**Fichier** : `.epci-state.json` (racine projet)

```json
{
  "version": "1.0",
  "workflow": "epci|quick|brainstorm",
  "feature_slug": "user-auth",
  "started_at": "2024-12-31T10:00:00Z",
  "current_phase": "phase-2",
  "checkpoints": {
    "brief": {"status": "completed", "at": "..."},
    "phase1": {"status": "completed", "at": "...", "verdict": "APPROVED"},
    "phase2": {"status": "in_progress", "started_at": "..."},
    "phase3": {"status": "pending"}
  },
  "context": {
    "complexity": "STANDARD",
    "files_planned": 5,
    "flags": ["--think-hard"]
  }
}
```

**Comportements** :
- Cree au debut de `/brief`
- Mis a jour a chaque breakpoint
- Lu au debut de chaque commande pour validation
- Supprime apres `/commit` reussi

**Flags** :
- `--resume` : Reprend depuis dernier checkpoint
- `--rollback <checkpoint>` : Annule jusqu'au checkpoint specifie
- `--status` : Affiche etat courant

### F2 — Hook Execution Garantie

**Mecanisme** : Wrapper Python execute avant affichage completion

```python
# src/hooks/ensure_execution.py
def ensure_post_phase_hooks(phase: str, context: dict) -> bool:
    """Force execution des hooks post-phase."""
    result = run_hooks(f"post-{phase}", context)
    if not result.success:
        warn(f"Hook post-{phase} failed: {result.message}")
    return result.success
```

**Integration** :
- Appele automatiquement en fin de phase
- Log si hook echoue
- Alerte utilisateur si memoire non mise a jour

### F3 — Validation Prerequis

**Par commande** :

| Commande | Prerequis | Verification |
|----------|-----------|--------------|
| `/epci` | Feature Document §1 existe | `docs/features/{slug}.md` |
| `/commit` | `.epci-commit-context.json` existe | Fichier present |
| `/epci --resume` | `.epci-state.json` existe | Fichier + status valide |

**Message erreur type** :
```
Prerequis manquant: Feature Document non trouve.

Attendu: docs/features/{slug}.md avec §1 complete

Action: Lancez /brief d'abord pour creer le Feature Document.
```

### F4 — Documentation Matrices

**AGENTS_MATRIX.md** :
```markdown
| Agent | Model | Invoque par | Phase | Conditionnel |
|-------|-------|-------------|-------|--------------|
| @plan-validator | opus | /epci | P1→BP1 | Non |
| @planner | sonnet | /epci --turbo, /quick | P1 | Turbo only |
| ...
```

**SKILLS_MATRIX.md** :
```markdown
| Skill | Categorie | Commandes | Agents | Auto-load |
|-------|-----------|-----------|--------|-----------|
| epci-core | core | /brief, /epci, /quick | tous | Toujours |
| ...
```

---

## Criteres d'Acceptation

### AC1 — State Machine
- [ ] `.epci-state.json` cree au debut de /brief
- [ ] Etat mis a jour a chaque breakpoint
- [ ] `--resume` reprend correctement
- [ ] `--status` affiche etat lisible

### AC2 — Hooks Automatiques
- [ ] Hook post-phase-3 execute automatiquement
- [ ] `.project-memory/history/features/` contient les features
- [ ] Alerte si hook echoue

### AC3 — Validation Prerequis
- [ ] `/epci` refuse sans Feature Document
- [ ] Message erreur clair avec action
- [ ] `/commit` refuse sans context file

### AC4 — Documentation
- [ ] CLAUDE.md mentionne 9 agents
- [ ] AGENTS_MATRIX.md cree
- [ ] SKILLS_MATRIX.md cree
- [ ] epci-core skill mis a jour

### AC5 — Score Qualite
- [ ] Audit workflow >= 80/100
- [ ] Aucun point faible "Critique"

---

## Plan d'Implementation

### Wave 1 — Documentation (Quick wins)

| Tache | Fichier | Effort |
|-------|---------|--------|
| Mettre a jour CLAUDE.md | CLAUDE.md | 30min |
| Mettre a jour README.md | README.md | 15min |
| Mettre a jour epci-core | src/skills/core/epci-core/SKILL.md | 15min |
| Creer AGENTS_MATRIX.md | docs/AGENTS_MATRIX.md | 30min |
| Creer SKILLS_MATRIX.md | docs/SKILLS_MATRIX.md | 30min |

### Wave 2 — State Machine

| Tache | Fichier | Effort |
|-------|---------|--------|
| Creer module state | src/workflow/state.py | 2h |
| Integrer dans /brief | src/commands/brief.md | 1h |
| Integrer dans /epci | src/commands/epci.md | 1h |
| Ajouter --resume, --rollback | src/settings/flags.md | 30min |

### Wave 3 — Hooks Automatiques

| Tache | Fichier | Effort |
|-------|---------|--------|
| Creer ensure_execution.py | src/hooks/ensure_execution.py | 1h |
| Integrer fin Phase 3 | src/commands/epci.md | 30min |
| Integrer fin /quick | src/commands/quick.md | 30min |
| Tests hooks | tests/test_hooks.py | 1h |

### Wave 4 — Validation Prerequis

| Tache | Fichier | Effort |
|-------|---------|--------|
| Module validation | src/workflow/validation.py | 1h |
| Integrer /epci | src/commands/epci.md | 30min |
| Integrer /commit | src/commands/commit.md | 30min |

---

## Risques

| Risque | Probabilite | Impact | Mitigation |
|--------|-------------|--------|------------|
| Breaking change workflows existants | Moyenne | Haut | Migration guide, deprecation warnings |
| State file corruption | Faible | Moyen | Validation JSON, backup avant write |
| Overhead performance | Faible | Faible | State minimal, lazy loading |

---

## Metriques de Succes

| KPI | Avant | Objectif | Mesure |
|-----|-------|----------|--------|
| Score coherence global | 70/100 | 85/100 | Audit prompt |
| Features enregistrees | 0% | 100% | count history/ |
| Reprises workflow | Impossible | Fonctionnel | Test --resume |
| Doc accuracy | 65/100 | 95/100 | Audit prompt |

---

## Notes

- Cette feature est LARGE car elle touche le coeur du workflow
- Implementer en 4 waves pour limiter les risques
- Chaque wave doit passer les tests avant la suivante
- Prevoir migration guide pour utilisateurs existants
