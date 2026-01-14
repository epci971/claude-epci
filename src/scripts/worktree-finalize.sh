#!/bin/bash
# worktree-finalize.sh — Merge et supprime le worktree courant
set -e

# === Detection contexte ===
WORKTREE_PATH=$(pwd)
MAIN_REPO=$(git worktree list | head -1 | awk '{print $1}')
CURRENT_BRANCH=$(git branch --show-current)

# === Validation: Est-on dans un worktree ? ===
if [ "$WORKTREE_PATH" = "$MAIN_REPO" ]; then
    echo "Erreur: Vous n'etes pas dans un worktree."
    echo "Ce script doit etre execute depuis un worktree, pas depuis le repo principal."
    exit 1
fi

# === Validation: Branche feature/* ? ===
if [[ ! "$CURRENT_BRANCH" =~ ^feature/ ]]; then
    echo "Erreur: Vous n'etes pas sur une branche feature/*."
    echo "Branche actuelle: $CURRENT_BRANCH"
    exit 1
fi

# === Extraction slug depuis branche ===
SLUG=${CURRENT_BRANCH#feature/}

# === Validation: Fichiers non commites ? ===
if [ -n "$(git status --porcelain)" ]; then
    echo "Erreur: Des fichiers ne sont pas commites."
    echo "Commitez ou stash d'abord avant de finaliser."
    echo ""
    echo "Fichiers en attente:"
    git status --short
    exit 1
fi

echo "Detection contexte:"
echo "  Worktree: $WORKTREE_PATH"
echo "  Repo principal: $MAIN_REPO"
echo "  Branche: $CURRENT_BRANCH"
echo "  Slug: $SLUG"
