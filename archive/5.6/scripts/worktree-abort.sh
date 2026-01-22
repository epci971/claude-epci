#!/bin/bash
# worktree-abort.sh — Supprime un worktree sans merger
set -e

# === Argument ou detection automatique ===
SLUG="${1:-}"

# Detecter le repo principal et le nom du projet
MAIN_REPO=$(git worktree list | head -1 | awk '{print $1}')
PROJECT_NAME=$(basename "$MAIN_REPO")

# Si pas d'argument, detecter depuis le worktree courant
if [ -z "$SLUG" ]; then
    CURRENT_BRANCH=$(git branch --show-current 2>/dev/null || echo "")

    if [[ "$CURRENT_BRANCH" =~ ^feature/ ]]; then
        SLUG=${CURRENT_BRANCH#feature/}
        echo "Detection automatique du slug: $SLUG"
    else
        echo "Erreur: Pas de slug fourni et impossible de le detecter."
        echo "Usage: worktree-abort.sh [slug]"
        echo ""
        echo "Exemples:"
        echo "  worktree-abort.sh mon-feature    # Depuis n'importe ou"
        echo "  worktree-abort.sh                # Depuis le worktree a supprimer"
        exit 1
    fi
fi

# === Verification que le worktree existe ===
WORKTREE_PATH="$HOME/worktrees/$PROJECT_NAME/$SLUG"

if ! git worktree list | grep -q "$WORKTREE_PATH"; then
    echo "Erreur: Worktree '$SLUG' introuvable."
    echo "Chemin attendu: $WORKTREE_PATH"
    echo ""
    echo "Worktrees existants:"
    git worktree list
    exit 1
fi

echo "Abandon du worktree '$SLUG'..."
echo "  Chemin: $WORKTREE_PATH"
echo "  Branche: feature/$SLUG"
echo ""

# === Cleanup force worktree ===
echo "Suppression du worktree (force)..."
cd "$MAIN_REPO"
git worktree remove --force "$WORKTREE_PATH" 2>/dev/null || true

# === Cleanup branche ===
echo "Suppression de la branche feature/$SLUG..."
git branch -D "feature/$SLUG" 2>/dev/null || true

# === Message de confirmation ===
echo ""
echo "========================================"
echo "Worktree '$SLUG' abandonne avec succes!"
echo "========================================"
echo ""
echo "Resume:"
echo "  - Worktree supprime: $WORKTREE_PATH"
echo "  - Branche feature/$SLUG supprimee"
echo ""
echo "Note: Aucune modification n'a ete mergee dans develop."
