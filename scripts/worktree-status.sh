#!/bin/bash
#
# worktree-status.sh - Check status of a git worktree
#
# Usage: worktree-status.sh <feature-slug>
#
# Output: JSON object with worktree status
#   {"exists": true, "path": "...", "branch": "...", "clean": true/false}
#   {"exists": false}
#
# Exit codes:
#   0 - Success (always, output indicates existence)
#   1 - Invalid arguments

set -euo pipefail

usage() {
    echo "Usage: $0 <feature-slug>" >&2
    echo "" >&2
    echo "Output: JSON with worktree status" >&2
    echo '  {"exists": true, "path": "...", "branch": "...", "clean": true}' >&2
    echo '  {"exists": false}' >&2
    exit 1
}

# Validate kebab-case
validate_kebab_case() {
    local slug="$1"
    if [[ ! "$slug" =~ ^[a-z][a-z0-9]*(-[a-z0-9]+)*$ ]]; then
        echo '{"error": "invalid_slug", "message": "Feature slug must be kebab-case"}'
        exit 1
    fi
}

# Get repository root
get_repo_root() {
    git rev-parse --show-toplevel 2>/dev/null
}

# Escape string for JSON
json_escape() {
    printf '%s' "$1" | sed 's/\\/\\\\/g; s/"/\\"/g; s/\n/\\n/g'
}

# Main
main() {
    if [[ $# -lt 1 ]]; then
        usage
    fi

    local feature_slug="$1"

    # Validate
    validate_kebab_case "$feature_slug"

    local repo_root
    repo_root=$(get_repo_root)

    if [[ -z "$repo_root" ]]; then
        echo '{"error": "not_git_repo", "message": "Not inside a git repository"}'
        exit 0
    fi

    local worktree_path="${repo_root}/../worktrees/${feature_slug}"
    local branch_name="feature/${feature_slug}"

    # Resolve to absolute path for comparison (read-only, no side effects)
    local abs_worktree_path
    local worktrees_parent="${repo_root}/.."
    if [[ -d "${worktrees_parent}/worktrees" ]]; then
        abs_worktree_path=$(cd "${worktrees_parent}/worktrees" && pwd)/"${feature_slug}"
    else
        # Worktrees directory doesn't exist yet, construct expected path
        abs_worktree_path=$(cd "${worktrees_parent}" && pwd)/worktrees/"${feature_slug}"
    fi

    # Check if worktree exists in git worktree list
    if ! git worktree list | grep -q "${feature_slug}"; then
        # Also check if directory exists but not registered
        if [[ -d "${abs_worktree_path}" ]]; then
            echo "{\"exists\": false, \"orphan_directory\": true, \"path\": \"${abs_worktree_path}\"}"
        else
            echo '{"exists": false}'
        fi
        exit 0
    fi

    # Worktree exists, get details
    local current_branch=""
    local is_clean=true

    # Get current branch in worktree
    if [[ -d "${abs_worktree_path}" ]]; then
        current_branch=$(git -C "${abs_worktree_path}" branch --show-current 2>/dev/null || echo "")

        # Check if clean
        if [[ -n "$(git -C "${abs_worktree_path}" status --porcelain 2>/dev/null)" ]]; then
            is_clean=false
        fi
    fi

    # Build JSON output
    local path_escaped
    local branch_escaped
    path_escaped=$(json_escape "${abs_worktree_path}")
    branch_escaped=$(json_escape "${current_branch}")

    echo "{\"exists\": true, \"path\": \"${path_escaped}\", \"branch\": \"${branch_escaped}\", \"clean\": ${is_clean}}"
}

main "$@"
