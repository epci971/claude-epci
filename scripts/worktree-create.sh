#!/bin/bash
#
# worktree-create.sh - Create a git worktree for a feature
#
# Usage: worktree-create.sh <feature-slug> [base-branch]
#
# Exit codes:
#   0 - Success
#   1 - Invalid arguments
#   2 - Worktree already exists
#   3 - Uncommitted changes in current repo (unused in create)
#   4 - Git command failed

set -euo pipefail

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

usage() {
    echo "Usage: $0 <feature-slug> [base-branch]"
    echo ""
    echo "Arguments:"
    echo "  feature-slug    Kebab-case feature identifier (required)"
    echo "  base-branch     Base branch to create from (default: main)"
    echo ""
    echo "Example:"
    echo "  $0 user-auth"
    echo "  $0 user-auth develop"
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

# Main
main() {
    # Parse arguments
    if [[ $# -lt 1 ]]; then
        usage
    fi

    local feature_slug="$1"
    local base_branch="${2:-}"

    # Auto-detect default branch if not specified
    if [[ -z "$base_branch" ]]; then
        if git show-ref --verify --quiet "refs/heads/main"; then
            base_branch="main"
        elif git show-ref --verify --quiet "refs/heads/master"; then
            base_branch="master"
        elif git show-ref --verify --quiet "refs/remotes/origin/main"; then
            base_branch="origin/main"
        elif git show-ref --verify --quiet "refs/remotes/origin/master"; then
            base_branch="origin/master"
        else
            echo -e "${RED}ERROR: Could not detect default branch (main or master)${NC}" >&2
            exit 4
        fi
    fi

    # Validate
    validate_kebab_case "$feature_slug"
    check_git_repo

    local repo_root
    repo_root=$(get_repo_root)

    # Create worktrees directory if needed and resolve absolute path
    local worktrees_dir="${repo_root}/../worktrees"
    mkdir -p "${worktrees_dir}"
    worktrees_dir=$(cd "${worktrees_dir}" && pwd)

    local worktree_path="${worktrees_dir}/${feature_slug}"
    local branch_name="feature/${feature_slug}"

    # Check if worktree already exists (using feature slug in path)
    if git worktree list | grep -q "/${feature_slug} "; then
        echo -e "${RED}ERROR: Worktree already exists at ${worktree_path}${NC}" >&2
        exit 2
    fi

    # Check if branch already exists
    if git show-ref --verify --quiet "refs/heads/${branch_name}"; then
        echo -e "${YELLOW}WARNING: Branch ${branch_name} already exists, will use existing branch${NC}"
        # Create worktree using existing branch
        if ! git worktree add "${worktree_path}" "${branch_name}"; then
            echo -e "${RED}ERROR: Failed to create worktree${NC}" >&2
            exit 4
        fi
    else
        # Check if base branch exists
        if ! git show-ref --verify --quiet "refs/heads/${base_branch}"; then
            # Try remote
            if ! git show-ref --verify --quiet "refs/remotes/origin/${base_branch}"; then
                echo -e "${RED}ERROR: Base branch '${base_branch}' does not exist${NC}" >&2
                exit 4
            fi
            base_branch="origin/${base_branch}"
        fi

        # Create worktree with new branch
        if ! git worktree add -b "${branch_name}" "${worktree_path}" "${base_branch}"; then
            echo -e "${RED}ERROR: Failed to create worktree${NC}" >&2
            exit 4
        fi
    fi

    echo -e "${GREEN}[OK] Worktree created successfully${NC}"
    echo ""
    echo "Details:"
    echo "  Path:   ${worktree_path}"
    echo "  Branch: ${branch_name}"
    echo ""
    echo "To work in the worktree:"
    echo "  cd ${worktree_path}"
}

main "$@"
