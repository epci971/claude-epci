#!/bin/bash
# sync-epci-symlinks.sh - Synchronise les skills/agents EPCI vers ~/.claude/
# Usage: ./sync-epci-symlinks.sh [--dry-run]
#
# Ce script crée des symlinks individuels pour chaque skill et agent EPCI
# tout en préservant les skills/agents externes (non-EPCI).
#
# Solution temporaire pour contourner le bug Claude Code v2.1.x
# Voir: https://github.com/anthropics/claude-code/issues/17271

set -e

BUILD_DIR="/home/epci/apps/claude-epci/build/epci"
CLAUDE_SKILLS="$HOME/.claude/skills"
CLAUDE_AGENTS="$HOME/.claude/agents"
CLAUDE_PLUGINS="$HOME/.claude/plugins"

DRY_RUN=false
[[ "$1" == "--dry-run" ]] && DRY_RUN=true

log() { echo "  $1"; }
info() { echo "→ $1"; }

# Vérifier que le répertoire build existe
if [[ ! -d "$BUILD_DIR" ]]; then
    echo "❌ Erreur: Le répertoire build n'existe pas: $BUILD_DIR"
    echo "   Exécutez d'abord le script de build src → build"
    exit 1
fi

# Créer les dossiers si nécessaires
if ! $DRY_RUN; then
    mkdir -p "$CLAUDE_SKILLS" "$CLAUDE_AGENTS" "$CLAUDE_PLUGINS"
fi

info "Synchronisation des skills EPCI..."

# Scanner tous les dossiers skills contenant un SKILL.md
for skill_dir in "$BUILD_DIR/skills"/*; do
    [[ -d "$skill_dir" ]] || continue
    skill_name=$(basename "$skill_dir")
    target="$CLAUDE_SKILLS/$skill_name"

    # Vérifier si c'est un skill valide (contient SKILL.md directement ou dans un sous-dossier)
    if [[ -f "$skill_dir/SKILL.md" ]]; then
        # Skill simple (brainstorm, debug, etc.)
        if [[ -L "$target" ]]; then
            current=$(readlink "$target")
            if [[ "$current" == "$skill_dir" ]]; then
                log "✓ $skill_name (déjà synchronisé)"
            else
                log "↻ $skill_name (mise à jour du symlink)"
                $DRY_RUN || ln -sfn "$skill_dir" "$target"
            fi
        elif [[ -e "$target" ]]; then
            log "⚠ $skill_name (existe mais n'est pas un symlink EPCI - IGNORÉ)"
        else
            log "+ $skill_name"
            $DRY_RUN || ln -s "$skill_dir" "$target"
        fi
    else
        # Dossier conteneur (core, stack) - scanner les sous-dossiers
        for sub_skill in "$skill_dir"/*; do
            [[ -d "$sub_skill" && -f "$sub_skill/SKILL.md" ]] || continue
            sub_name=$(basename "$sub_skill")
            sub_target="$CLAUDE_SKILLS/$sub_name"

            if [[ -L "$sub_target" ]]; then
                current=$(readlink "$sub_target")
                if [[ "$current" == "$sub_skill" ]]; then
                    log "✓ $sub_name (déjà synchronisé)"
                else
                    log "↻ $sub_name (mise à jour)"
                    $DRY_RUN || ln -sfn "$sub_skill" "$sub_target"
                fi
            elif [[ -e "$sub_target" ]]; then
                log "⚠ $sub_name (existe - IGNORÉ)"
            else
                log "+ $sub_name"
                $DRY_RUN || ln -s "$sub_skill" "$sub_target"
            fi
        done
    fi
done

info "Synchronisation des agents EPCI..."

for agent_file in "$BUILD_DIR/agents"/*.md; do
    [[ -f "$agent_file" ]] || continue
    agent_name=$(basename "$agent_file")
    target="$CLAUDE_AGENTS/$agent_name"

    if [[ -L "$target" ]]; then
        current=$(readlink "$target")
        if [[ "$current" == "$agent_file" ]]; then
            log "✓ $agent_name (déjà synchronisé)"
        else
            log "↻ $agent_name (mise à jour)"
            $DRY_RUN || ln -sfn "$agent_file" "$target"
        fi
    elif [[ -e "$target" ]]; then
        log "⚠ $agent_name (existe - IGNORÉ)"
    else
        log "+ $agent_name"
        $DRY_RUN || ln -s "$agent_file" "$target"
    fi
done

info "Désactivation du plugin EPCI..."
if ! $DRY_RUN; then
    echo '{"version": 2, "plugins": {}}' > "$CLAUDE_PLUGINS/installed_plugins.json"
    log "✓ Plugin désactivé"
else
    log "(dry-run) Désactiverait le plugin"
fi

echo ""
info "Synchronisation terminée!"
echo "   Redémarrer Claude Code pour appliquer les changements."
