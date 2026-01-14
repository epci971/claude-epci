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

# === Creation dossier worktrees si necessaire ===
mkdir -p "$WORKTREE_BASE"

# === Creation du worktree avec nouvelle branche ===
echo "Creation du worktree pour '$SLUG'..."
git worktree add -b "$BRANCH_NAME" "$WORKTREE_PATH" develop

# === Copie des fichiers .env si presents ===
SOURCE_DIR=$(git rev-parse --show-toplevel)
ENV_FILES_COPIED=()

for env_file in "$SOURCE_DIR"/.env "$SOURCE_DIR"/.env.* "$SOURCE_DIR"/.envrc; do
    if [ -f "$env_file" ]; then
        filename=$(basename "$env_file")
        cp "$env_file" "$WORKTREE_PATH/$filename"
        ENV_FILES_COPIED+=("$filename")
    fi
done

# === Message de succes ===
echo ""
echo "Worktree cree avec succes!"
echo "  Chemin:  $WORKTREE_PATH"
echo "  Branche: $BRANCH_NAME"

if [ ${#ENV_FILES_COPIED[@]} -gt 0 ]; then
    echo ""
    echo "Fichiers copies:"
    for f in "${ENV_FILES_COPIED[@]}"; do
        echo "  - $f"
    done
fi

echo ""
echo "Pour y acceder: cd $WORKTREE_PATH"
