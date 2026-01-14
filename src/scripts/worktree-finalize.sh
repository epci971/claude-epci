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
echo ""

# === Merge dans develop ===
echo "Merge de $CURRENT_BRANCH dans develop..."
cd "$MAIN_REPO"

# Checkout develop
if ! git checkout develop 2>/dev/null; then
    echo "Erreur: Impossible de checkout la branche develop."
    exit 1
fi

# Merge avec --no-ff pour conserver l'historique
if ! git merge --no-ff "$CURRENT_BRANCH" -m "Merge $CURRENT_BRANCH into develop"; then
    echo ""
    echo "Erreur: Conflit lors du merge."
    echo "Resolvez manuellement:"
    echo "  cd $MAIN_REPO"
    echo "  git status  # voir les fichiers en conflit"
    echo "  # Editez les fichiers, puis:"
    echo "  git add ."
    echo "  git commit"
    echo ""
    echo "  # OU pour annuler le merge:"
    echo "  git merge --abort"
    exit 1
fi

echo "Merge reussi!"
echo ""

# === Cleanup worktree ===
echo "Suppression du worktree..."
if ! git worktree remove "$WORKTREE_PATH"; then
    echo "Erreur: Impossible de supprimer le worktree."
    echo "Essayez manuellement: git worktree remove --force $WORKTREE_PATH"
    exit 1
fi

# === Cleanup branche ===
echo "Suppression de la branche $CURRENT_BRANCH..."
if ! git branch -d "$CURRENT_BRANCH"; then
    echo "Warning: Impossible de supprimer la branche $CURRENT_BRANCH."
    echo "Elle peut etre supprimee manuellement: git branch -D $CURRENT_BRANCH"
fi

# === Message de succes ===
echo ""
echo "========================================"
echo "Feature '$SLUG' finalisee avec succes!"
echo "========================================"
echo ""
echo "Resume:"
echo "  - Branche $CURRENT_BRANCH mergee dans develop"
echo "  - Worktree supprime: $WORKTREE_PATH"
echo "  - Branche $CURRENT_BRANCH supprimee"
echo ""
echo "Vous etes maintenant sur la branche develop dans $MAIN_REPO"
