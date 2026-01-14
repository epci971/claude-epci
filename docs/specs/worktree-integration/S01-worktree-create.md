# S01 — Script worktree-create.sh

| Metadata | Value |
|----------|-------|
| **Spec ID** | S01 |
| **Parent PRD** | worktree-integration |
| **Effort** | 2 jours |
| **Priority** | P1 (Must-have) |
| **Dependencies** | - |
| **Status** | Pending |

---

## Objectif

Creer le script `worktree-create.sh` permettant d'isoler une feature dans un worktree Git dedie.

## User Story Source

**US1 — Creer un worktree**

**En tant que** developpeur EPCI,
**Je veux** creer un worktree isole pour une feature,
**Afin de** travailler sans impacter les autres branches.

---

## Scope

### Fichiers a creer

| Fichier | Action | Description |
|---------|--------|-------------|
| `src/scripts/worktree-create.sh` | Create | Script principal de creation worktree |

### Hors scope

- Scripts finalize et abort (S02)
- Integration avec /brief, /epci, /quick (S03)

---

## Acceptance Criteria

- [ ] **AC1**: Given je suis sur le repo EPCI, When je lance `./src/scripts/worktree-create.sh mon-slug`, Then un worktree est cree dans `~/worktrees/{projet}/mon-slug/`
- [ ] **AC2**: Given le worktree est cree, When je verifie, Then une branche `feature/mon-slug` existe depuis `develop`
- [ ] **AC3**: Given des fichiers .env existent, When le worktree est cree, Then ils sont copies dans le worktree
- [ ] **AC4**: Given un worktree existe deja pour ce slug, When je relance le script, Then erreur + message "worktree existe deja"
- [ ] **AC5**: Given la branche develop n'existe pas, When je lance le script, Then erreur + message "branche develop requise"
- [ ] **AC6**: Given le dossier ~/worktrees/ n'existe pas, When je lance le script, Then il est cree automatiquement

---

## Tasks

- [ ] T1: Creer le fichier `src/scripts/worktree-create.sh` avec shebang bash
- [ ] T2: Implementer la validation des arguments (slug requis)
- [ ] T3: Implementer la detection du nom du projet (basename du repo)
- [ ] T4: Implementer la verification de la branche develop
- [ ] T5: Implementer la verification worktree existant
- [ ] T6: Implementer la creation du dossier `~/worktrees/{projet}/`
- [ ] T7: Implementer `git worktree add` avec branche `feature/{slug}`
- [ ] T8: Implementer la copie des fichiers .env/.envrc si presents
- [ ] T9: Ajouter les messages de succes/erreur en francais
- [ ] T10: Rendre le script executable (chmod +x)
- [ ] T11: Tester manuellement les cas nominaux et edge cases

---

## Technical Notes

### Structure du script

```bash
#!/bin/bash
# worktree-create.sh — Cree un worktree isole pour une feature EPCI
set -e

SLUG="$1"
PROJECT_NAME=$(basename "$(git rev-parse --show-toplevel)")
WORKTREE_BASE="$HOME/worktrees/$PROJECT_NAME"
WORKTREE_PATH="$WORKTREE_BASE/$SLUG"
BRANCH_NAME="feature/$SLUG"

# Validations...
# Creation...
# Copie .env...
# Message succes...
```

### Commandes Git cles

```bash
# Verifier branche develop existe
git rev-parse --verify develop

# Verifier worktree n'existe pas
git worktree list | grep -q "$WORKTREE_PATH" && exit 1

# Creer worktree
git worktree add -b "$BRANCH_NAME" "$WORKTREE_PATH" develop
```

### Messages d'erreur

| Situation | Message |
|-----------|---------|
| Slug manquant | "Usage: worktree-create.sh <slug>" |
| Develop inexistant | "Erreur: La branche 'develop' n'existe pas. Creez-la d'abord." |
| Worktree existe | "Erreur: Un worktree existe deja pour '{slug}'." |

---

## Definition of Done

- [ ] Script cree et executable
- [ ] Tous les AC valides manuellement
- [ ] Messages d'erreur clairs en francais
- [ ] Compatible Linux/macOS (POSIX)
