#!/bin/bash
#
# worktree-finalize.sh - Remove a git worktree and optionally delete branch
#
# Usage: worktree-finalize.sh <feature-slug> [--force] [--delete-branch]
#
# Exit codes:
#   0 - Success
#   1 - Invalid arguments
#   2 - Worktree not found
#   3 - Uncommitted changes (without --force)
#   4 - Git command failed

set -euo pipefail

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

usage() {
    echo "Usage: $0 <feature-slug> [--force] [--delete-branch]"
    echo ""
    echo "Arguments:"
    echo "  feature-slug     Kebab-case feature identifier (required)"
    echo "  --force          Force removal even with uncommitted changes"
    echo "  --delete-branch  Delete the feature branch after removal"
    echo ""
    echo "Example:"
    echo "  $0 user-auth"
    echo "  $0 user-auth --force --delete-branch"
    exit 1
}

# Validate kebab-case
validate_kebab_case() {
    local slug="$1"
    if [[ ! "$slug" =~ ^[a-z][a-z0-9]*(-[a-z0-9]+)*$ ]]; then
        echo -e "${RED}ERROR: Feature slug must be kebab-case (e.g., 'my-feature')${NC}" >&2
        exit 1
    fi
}

# Check if inside a git repository
check_git_repo() {
    if ! git rev-parse --git-dir > /dev/null 2>&1; then
        echo -e "${RED}ERROR: Not inside a git repository${NC}" >&2
        exit 4
    fi
}

# Get repository root
get_repo_root() {
    git rev-parse --show-toplevel
}

# Check for uncommitted changes in worktree
check_uncommitted_changes() {
    local worktree_path="$1"
    if [[ -n "$(git -C "${worktree_path}" status --porcelain 2>/dev/null)" ]]; then
        return 0  # Has uncommitted changes
    fi
    return 1  # Clean
}

# Check if branch is merged to main
is_branch_merged() {
    local branch_name="$1"
    local main_branch="${2:-main}"

    # Check if main branch exists
    if ! git show-ref --verify --quiet "refs/heads/${main_branch}"; then
        main_branch="master"
        if ! git show-ref --verify --quiet "refs/heads/${main_branch}"; then
            return 1  # Can't determine, assume not merged
        fi
    fi

    if git branch --merged "${main_branch}" | grep -q "${branch_name}"; then
        return 0  # Is merged
    fi
    return 1  # Not merged
}

# Main
main() {
    local force=false
    local delete_branch=false
    local feature_slug=""

    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --force)
                force=true
                shift
                ;;
            --delete-branch)
                delete_branch=true
                shift
                ;;
            -*)
                echo -e "${RED}ERROR: Unknown option: $1${NC}" >&2
                usage
                ;;
            *)
                if [[ -z "$feature_slug" ]]; then
                    feature_slug="$1"
                else
                    echo -e "${RED}ERROR: Unexpected argument: $1${NC}" >&2
                    usage
                fi
                shift
                ;;
        esac
    done

    if [[ -z "$feature_slug" ]]; then
        usage
    fi

    # Validate
    validate_kebab_case "$feature_slug"
    check_git_repo

    local repo_root
    repo_root=$(get_repo_root)

    # Resolve absolute worktrees path
    local worktrees_dir="${repo_root}/../worktrees"
    if [[ -d "${worktrees_dir}" ]]; then
        worktrees_dir=$(cd "${worktrees_dir}" && pwd)
    fi

    local worktree_path="${worktrees_dir}/${feature_slug}"
    local branch_name="feature/${feature_slug}"

    # Check if worktree exists (using feature slug in path)
    if ! git worktree list | grep -q "/${feature_slug} "; then
        echo -e "${RED}ERROR: Worktree not found at ${worktree_path}${NC}" >&2
        exit 2
    fi

    # Get actual path from git worktree list
    worktree_path=$(git worktree list | grep "/${feature_slug} " | awk '{print $1}')

    # Check for uncommitted changes
    if check_uncommitted_changes "${worktree_path}"; then
        if [[ "$force" != true ]]; then
            echo -e "${YELLOW}WARNING: Worktree has uncommitted changes${NC}"
            echo "Changes in ${worktree_path}:"
            git -C "${worktree_path}" status --short
            echo ""
            echo -e "${RED}ERROR: Use --force to remove anyway${NC}" >&2
            exit 3
        else
            echo -e "${YELLOW}WARNING: Removing worktree with uncommitted changes${NC}"
        fi
    fi

    # Remove worktree
    if [[ "$force" == true ]]; then
        if ! git worktree remove --force "${worktree_path}"; then
            echo -e "${RED}ERROR: Failed to remove worktree${NC}" >&2
            exit 4
        fi
    else
        if ! git worktree remove "${worktree_path}"; then
            echo -e "${RED}ERROR: Failed to remove worktree${NC}" >&2
            exit 4
        fi
    fi

    echo -e "${GREEN}[OK] Worktree removed${NC}"

    # Prune worktrees
    git worktree prune

    # Handle branch deletion
    if [[ "$delete_branch" == true ]]; then
        if is_branch_merged "$branch_name"; then
            if git branch -d "${branch_name}" 2>/dev/null; then
                echo -e "${GREEN}[OK] Branch ${branch_name} deleted (was merged)${NC}"
            else
                echo -e "${YELLOW}WARNING: Could not delete branch ${branch_name}${NC}"
            fi
        else
            echo -e "${YELLOW}WARNING: Branch ${branch_name} is not merged to main${NC}"
            if [[ "$force" == true ]]; then
                if git branch -D "${branch_name}" 2>/dev/null; then
                    echo -e "${GREEN}[OK] Branch ${branch_name} force deleted${NC}"
                fi
            else
                echo "Use --force to delete unmerged branch"
            fi
        fi
    else
        echo "Branch ${branch_name} preserved"
    fi

    echo ""
    echo "Finalization complete."
}

main "$@"
