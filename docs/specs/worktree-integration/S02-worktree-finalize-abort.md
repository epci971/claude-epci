# S02 — Scripts finalize & abort

| Metadata | Value |
|----------|-------|
| **Spec ID** | S02 |
| **Parent PRD** | worktree-integration |
| **Effort** | 3 jours |
| **Priority** | P1 (Must-have) |
| **Dependencies** | S01 |
| **Status** | Pending |

---

## Objectif

Creer les scripts `worktree-finalize.sh` et `worktree-abort.sh` pour terminer ou abandonner proprement un worktree.

## User Stories Sources

### US2 — Finaliser un worktree

**En tant que** developpeur EPCI,
**Je veux** merger automatiquement mon worktree dans develop,
**Afin de** integrer ma feature sans manipulation Git complexe.

### US3 — Abandonner un worktree

**En tant que** developpeur EPCI,
**Je veux** supprimer un worktree sans merger,
**Afin de** annuler proprement une feature abandonnee.

---

## Scope

### Fichiers a creer

| Fichier | Action | Description |
|---------|--------|-------------|
| `src/scripts/worktree-finalize.sh` | Create | Script merge + cleanup |
| `src/scripts/worktree-abort.sh` | Create | Script cleanup sans merge |

### Hors scope

- Integration automatique avec /epci et /quick (S03)
- Script worktree-create.sh (S01)

---

## Acceptance Criteria

### worktree-finalize.sh

- [ ] **AC1**: Given je suis dans un worktree, When je lance `worktree-finalize.sh`, Then le worktree est merge dans develop
- [ ] **AC2**: Given le merge reussit, When finalize termine, Then le worktree est supprime
- [ ] **AC3**: Given un conflit existe, When finalize echoue, Then un message clair indique comment resoudre manuellement
- [ ] **AC4**: Given des fichiers non commites existent, When je lance finalize, Then erreur + message "commiter d'abord"

### worktree-abort.sh

- [ ] **AC5**: Given j'ai un worktree actif, When je lance `worktree-abort.sh [slug]`, Then le worktree est supprime
- [ ] **AC6**: Given j'ai une branche feature/{slug}, When abort termine, Then la branche est supprimee
- [ ] **AC7**: Given le slug n'existe pas, When je lance abort, Then erreur + message "worktree introuvable"

---

## Tasks

### worktree-finalize.sh

- [ ] T1: Creer le fichier `src/scripts/worktree-finalize.sh` avec shebang bash
- [ ] T2: Detecter automatiquement le slug depuis le worktree courant
- [ ] T3: Verifier qu'on est bien dans un worktree (pas le repo principal)
- [ ] T4: Verifier qu'il n'y a pas de fichiers non commites
- [ ] T5: Checkout develop dans le repo principal
- [ ] T6: Merge de la branche feature/{slug} dans develop
- [ ] T7: Gerer les conflits avec message d'erreur explicite
- [ ] T8: Supprimer le worktree avec `git worktree remove`
- [ ] T9: Supprimer la branche feature/{slug}
- [ ] T10: Afficher message de succes avec resume

### worktree-abort.sh

- [ ] T11: Creer le fichier `src/scripts/worktree-abort.sh` avec shebang bash
- [ ] T12: Accepter le slug en argument OU le detecter depuis le worktree courant
- [ ] T13: Verifier que le worktree existe
- [ ] T14: Supprimer le worktree avec `git worktree remove --force`
- [ ] T15: Supprimer la branche feature/{slug}
- [ ] T16: Afficher message de confirmation

### Tests

- [ ] T17: Tester finalize en cas nominal (merge clean)
- [ ] T18: Tester finalize avec conflit (message d'erreur)
- [ ] T19: Tester abort depuis le worktree
- [ ] T20: Tester abort depuis le repo principal avec slug

---

## Technical Notes

### worktree-finalize.sh — Structure

```bash
#!/bin/bash
# worktree-finalize.sh — Merge et supprime le worktree courant
set -e

# Detection contexte
WORKTREE_PATH=$(pwd)
MAIN_REPO=$(git worktree list | head -1 | awk '{print $1}')
CURRENT_BRANCH=$(git branch --show-current)
SLUG=${CURRENT_BRANCH#feature/}

# Validations
# - Est-on dans un worktree ?
# - Fichiers non commites ?

# Merge
cd "$MAIN_REPO"
git checkout develop
git merge --no-ff "$CURRENT_BRANCH" -m "Merge feature/$SLUG into develop"

# Cleanup
git worktree remove "$WORKTREE_PATH"
git branch -d "$CURRENT_BRANCH"

echo "Feature '$SLUG' mergee et worktree supprime."
```

### worktree-abort.sh — Structure

```bash
#!/bin/bash
# worktree-abort.sh — Supprime un worktree sans merger
set -e

SLUG="${1:-}"

# Si pas d'argument, detecter depuis worktree courant
if [ -z "$SLUG" ]; then
    CURRENT_BRANCH=$(git branch --show-current)
    SLUG=${CURRENT_BRANCH#feature/}
fi

# Trouver le worktree
PROJECT_NAME=$(basename "$(git rev-parse --show-toplevel)")
WORKTREE_PATH="$HOME/worktrees/$PROJECT_NAME/$SLUG"

# Cleanup force
git worktree remove --force "$WORKTREE_PATH" 2>/dev/null || true
git branch -D "feature/$SLUG" 2>/dev/null || true

echo "Worktree '$SLUG' abandonne et supprime."
```

### Messages d'erreur

| Situation | Message |
|-----------|---------|
| Pas dans un worktree | "Erreur: Vous n'etes pas dans un worktree." |
| Fichiers non commites | "Erreur: Des fichiers ne sont pas commites. Commitez ou stash d'abord." |
| Conflit merge | "Erreur: Conflit lors du merge. Resolvez manuellement:\n  cd {main_repo}\n  git merge --abort\n  # OU resoudre puis git commit" |
| Worktree introuvable | "Erreur: Worktree '{slug}' introuvable." |

---

## Definition of Done

- [ ] Les deux scripts crees et executables
- [ ] Tous les AC valides manuellement
- [ ] Messages d'erreur clairs en francais
- [ ] Gestion des conflits avec instructions
- [ ] Compatible Linux/macOS (POSIX)
