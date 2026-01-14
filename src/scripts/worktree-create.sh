#!/bin/bash
# worktree-create.sh — Cree un worktree isole pour une feature EPCI
set -e

# === Arguments ===
SLUG="$1"

# === Validation: Slug requis ===
if [ -z "$SLUG" ]; then
    echo "Usage: worktree-create.sh <slug>"
    echo "Erreur: Le slug est requis."
    exit 1
fi

# === Validation: Branche develop existe ===
if ! git rev-parse --verify develop >/dev/null 2>&1; then
    echo "Erreur: La branche 'develop' n'existe pas."
    echo "Creez-la d'abord avec: git checkout -b develop"
    exit 1
fi

# === Variables derivees ===
PROJECT_NAME=$(basename "$(git rev-parse --show-toplevel)")
WORKTREE_BASE="$HOME/worktrees/$PROJECT_NAME"
WORKTREE_PATH="$WORKTREE_BASE/$SLUG"
BRANCH_NAME="feature/$SLUG"

# === Validation: Worktree n'existe pas deja ===
if git worktree list | grep -q "$WORKTREE_PATH"; then
    echo "Erreur: Un worktree existe deja pour '$SLUG'."
    echo "Chemin: $WORKTREE_PATH"
    exit 1
fi
