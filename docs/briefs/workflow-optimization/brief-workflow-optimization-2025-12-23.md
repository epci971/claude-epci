# Brief Fonctionnel — Optimisation Workflow EPCI v3.2

> **Slug**: `workflow-optimization-v32`
> **Date**: 2025-12-23
> **Source**: Brainstorming session
> **EMS Final**: 92/100

---

## Contexte

Le workflow EPCI v3.0/v3.1 présente plusieurs axes d'optimisation identifiés lors d'un brainstorming approfondi :
- Chargement mémoire redondant (3x par workflow)
- Hooks manquants sur epci-brief
- Hook pre-phase-3 redondant
- Feature Document avec sections redondantes
- Flags inutilisés (--fast, --dry-run)
- Skills dupliqués (project-memory vs project-memory-loader)

Ce brief regroupe toutes les optimisations validées pour la v3.2.

---

## Optimisations Validées

### 1. Mémoire — Chargement Unique

**Problème**: `.project-memory/` chargé 3 fois (epci-brief, epci, epci-quick)

**Solution**:
- Charger uniquement dans `/epci-brief`
- Passer le summary via Feature Document §1 (STANDARD/LARGE)
- Passer le summary via brief inline (TINY/SMALL)

**Fichiers impactés**:
- `src/commands/epci-brief.md` — Ajouter memory summary dans output
- `src/commands/epci.md` — Lire memory depuis §1 au lieu de recharger
- `src/commands/epci-quick.md` — Lire memory depuis brief inline

**Gain**: -30-60 sec par workflow

---

### 2. Breakpoint epci-quick

**Problème**: Pas de breakpoint avant commit dans epci-quick

**Solution**: Ajouter breakpoint pre-commit identique à /epci Phase 3

**Fichiers impactés**:
- `src/commands/epci-quick.md` — Ajouter section BREAKPOINT PRE-COMMIT

**Statut**: DÉJÀ IMPLÉMENTÉ (vérifié dans le fichier)

---

### 3. Hooks — Restructuration

**Actions**:

| Action | Hook | Raison |
|--------|------|--------|
| **Supprimer** | `pre-phase-3` | Redondant avec post-phase-2 |
| **Ajouter** | `pre-brief` | Charger config externe avant exploration |
| **Ajouter** | `post-brief` | Notifier début feature, créer tickets |
| **Garder** | `on-breakpoint` | Logging fin de workflow |

**Fichiers impactés**:
- `src/hooks/README.md` — MAJ documentation
- `src/hooks/runner.py` — Ajouter pre-brief, post-brief
- `src/commands/epci-brief.md` — Invoquer nouveaux hooks
- `src/commands/epci.md` — Supprimer invocation pre-phase-3

**Nouveau schéma**:
```
epci-brief: pre-brief → [explore] → post-brief
epci P1:    pre-phase-1 → [plan] → post-phase-1
epci P2:    pre-phase-2 → [code] → post-phase-2
epci P3:    pre-commit → [commit] → post-commit → post-phase-3 → on-breakpoint
```

---

### 4. Feature Document — Restructuration

**Actions**:

| Action | Détail |
|--------|--------|
| **Fusionner** | §3 (Implémentation) + §4 (Finalisation) → §3 unique |
| **Supprimer** | Tableau fichiers dans §1 (garder uniquement dans §2) |
| **Ajouter** | Memory Summary dans §1 |

**Nouvelle structure**:
```markdown
## §1 — Brief Fonctionnel
- Contexte
- Stack Détecté
- Critères d'Acceptation
- Contraintes
- Hors Scope
- Évaluation + Flags
- Memory Summary (NOUVEAU)

## §2 — Plan d'Implémentation
- Fichiers Impactés (tableau UNIQUE)
- Tâches
- Risques
- Validation

## §3 — Implémentation & Finalisation (FUSIONNÉ)
- Progress
- Tests
- Reviews
- Déviations
- Commit Message
- Documentation
- PR Ready
```

**Fichiers impactés**:
- `src/commands/epci-brief.md` — MAJ template §1
- `src/commands/epci.md` — MAJ templates §2 et §3
- `CLAUDE.md` — MAJ documentation structure

---

### 5. Flags — Nettoyage

**Actions**:

| Action | Flag | Raison |
|--------|------|--------|
| **Supprimer** | `--fast` | Jamais utilisé, risqué |
| **Supprimer** | `--dry-run` | Jamais utilisé |
| **Ajouter** | `--no-hooks` | Désactiver tous les hooks |

**Inventaire final (9 flags)**:
```
Thinking:    --think, --think-hard, --ultrathink
Compression: --uc, --verbose
Workflow:    --safe, --no-hooks
Wave:        --wave, --wave-strategy
Legacy:      --large, --continue
```

**Fichiers impactés**:
- `src/settings/flags.md` — MAJ documentation
- `src/commands/epci.md` — Supprimer références --fast, --dry-run
- `src/commands/epci-quick.md` — Supprimer références --fast
- `src/skills/core/flags-system/SKILL.md` — MAJ si existe

---

### 6. Skills — Consolidation

**Actions**:

| Action | Détail |
|--------|--------|
| **Fusionner** | `project-memory` + `project-memory-loader` → `project-memory` |
| **Implémenter** | Cache skills session |
| **Implémenter** | Lazy-load skills |

**Fichiers impactés**:
- `src/skills/core/project-memory/SKILL.md` — Intégrer loader
- `src/skills/core/project-memory-loader/` — Supprimer (fusionné)
- Toutes les commandes — MAJ références skill

**Résultat**: 20 skills (au lieu de 21)

---

## Découpage en Features

| Feature | Contenu | Catégorie | Priorité |
|---------|---------|-----------|----------|
| **F-Memory-Single-Load** | Mémoire 1x, memory summary dans §1/brief | SMALL | HIGH |
| **F-Hooks-Restructure** | pre/post-brief, supprimer pre-phase-3 | SMALL | MEDIUM |
| **F-Feature-Doc-V2** | Fusion §3+§4, supprimer tableau §1 | SMALL | MEDIUM |
| **F-Flags-Cleanup** | Supprimer fast/dry-run, ajouter no-hooks | TINY | LOW |
| **F-Skills-Consolidate** | Fusion project-memory, cache, lazy-load | STANDARD | LOW |

---

## Critères d'Acceptation Globaux

- [ ] Mémoire chargée 1 seule fois par workflow
- [ ] Hooks pre-brief et post-brief fonctionnels
- [ ] Hook pre-phase-3 supprimé sans régression
- [ ] Feature Document §3 contient implémentation + finalisation
- [ ] Flags --fast et --dry-run supprimés
- [ ] Flag --no-hooks fonctionnel
- [ ] Skills project-memory fusionnés
- [ ] Aucune régression sur workflows existants

---

## Hors Scope

- Exploration différenciée (quick vs thorough selon complexité pré-évaluée)
- Refonte complète du routing
- Nouveaux flags (--quiet, --interactive)
- Dashboard métriques temps réel

---

## Commandes Suggérées

```bash
# Implémenter par ordre de priorité
/epci-brief F-Memory-Single-Load
/epci-brief F-Hooks-Restructure
/epci-brief F-Feature-Doc-V2
/epci-brief F-Flags-Cleanup
/epci-brief F-Skills-Consolidate
```

---

*Brief généré par /brainstorm — Session du 2025-12-23*
