# Automatisation du Cycle Feature Complet avec Git Worktrees et GitHub CLI

## Table des Matières

1. [Vue d'ensemble](#vue-densemble)
2. [Architecture et Conventions](#architecture-et-conventions)
3. [Scripts Production-Ready](#scripts-production-ready)
4. [GitHub Actions Workflow](#github-actions-workflow)
5. [Gestion des Worktrees](#gestion-des-worktrees)
6. [Patterns Avancés](#patterns-avancés)
7. [Troubleshooting](#troubleshooting)

---

## Vue d'ensemble

Ce guide couvre l'automatisation complète du cycle de développement feature :

1. **Création** : worktree + branche automatiques avec naming convention
2. **Contexte** : exécution de commandes/scripts dans le worktree
3. **Commits** : assistés ou automatiques via hooks
4. **Push** : envoi de la branche au remote
5. **PR** : création automatique avec template via `gh pr create`
6. **Cleanup** : détection de merge et suppression du worktree

### Avantages de cette approche

- **Isolation** : chaque feature dans un répertoire séparé
- **Parallélisation** : plusieurs features simultanément sans changements de branche
- **Sécurité** : l'historique git principal reste propre
- **Automation** : réduction des tâches manuelles répétitives
- **CI/CD** : intégration avec GitHub Actions pour cleanup automatique

---

## Architecture et Conventions

### Naming Convention

```
Branch:   feature/TICKET-short-description
Worktree: ../worktrees/TICKET
Example:  feature/PROJ-123-user-authentication
          ../worktrees/PROJ-123
```

### Extraction du TICKET

```bash
# From: feature/PROJ-123-user-auth
# Extract: PROJ-123

BRANCH_NAME="feature/PROJ-123-user-auth"
TICKET=$(echo "$BRANCH_NAME" | sed -E 's|feature/([A-Z]+-[0-9]+).*|\1|')
echo "$TICKET"  # Output: PROJ-123
```

### Structure de répertoires

```
my-project/
├── .git/
├── src/
├── .github/
│   └── workflows/
│       ├── cleanup-worktree.yml
│       └── pr-template.md
├── scripts/
│   ├── create-feature.sh
│   ├── create-pr.sh
│   └── manage-worktrees.sh
└── worktrees/
    ├── PROJ-123/
    ├── PROJ-124/
    └── PROJ-125/
```

---

## Scripts Production-Ready

### 1. Script de Création de Feature

**`scripts/create-feature.sh`**

```bash
#!/bin/bash
set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
MAIN_REPO="$(pwd)"
WORKTREES_DIR="${MAIN_REPO}/worktrees"
DEFAULT_BASE_BRANCH="${1:-main}"

# Functions
log_error() {
    echo -e "${RED}❌ ERROR: $1${NC}" >&2
}

log_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

log_info() {
    echo -e "${YELLOW}ℹ️  $1${NC}"
}

validate_ticket() {
    local ticket="$1"
    # Validate format: PROJ-123 or TICKET-123
    if [[ ! "$ticket" =~ ^[A-Z]+-[0-9]+$ ]]; then
        log_error "Invalid ticket format. Expected: PROJ-123, got: $ticket"
        return 1
    fi
    return 0
}

validate_description() {
    local desc="$1"
    if [[ ! "$desc" =~ ^[a-z0-9\-]+$ ]]; then
        log_error "Invalid description. Use only lowercase, numbers, and hyphens"
        return 1
    fi
    return 0
}

check_worktree_exists() {
    local ticket="$1"
    if [[ -d "${WORKTREES_DIR}/${ticket}" ]]; then
        log_error "Worktree for $ticket already exists"
        return 1
    fi
    return 0
}

create_feature() {
    local ticket="$1"
    local description="$2"
    local base_branch="${3:-${DEFAULT_BASE_BRANCH}}"
    
    # Validate inputs
    validate_ticket "$ticket" || return 1
    validate_description "$description" || return 1
    check_worktree_exists "$ticket" || return 1
    
    # Construct branch name
    local branch_name="feature/${ticket}-${description}"
    
    log_info "Creating feature branch: $branch_name"
    log_info "Base branch: $base_branch"
    log_info "Worktree path: ${WORKTREES_DIR}/${ticket}"
    
    # Ensure base branch is up-to-date
    log_info "Fetching latest changes from remote..."
    git fetch origin "$base_branch" || {
        log_error "Failed to fetch $base_branch from origin"
        return 1
    }
    
    # Create worktree with new branch
    log_info "Creating worktree..."
    mkdir -p "$WORKTREES_DIR"
    
    if git worktree add \
        --detach \
        "${WORKTREES_DIR}/${ticket}" \
        "origin/${base_branch}"; then
        
        # Now create the branch in the worktree
        (
            cd "${WORKTREES_DIR}/${ticket}"
            git checkout -b "$branch_name" || {
                log_error "Failed to create branch $branch_name"
                cd "$MAIN_REPO"
                git worktree remove "${WORKTREES_DIR}/${ticket}"
                return 1
            }
        ) || return 1
        
    else
        log_error "Failed to create worktree"
        return 1
    fi
    
    log_success "Feature created successfully!"
    log_info "To start working:"
    echo ""
    echo "  cd ${WORKTREES_DIR}/${ticket}"
    echo "  # ... make changes ..."
    echo "  git add ."
    echo "  git commit -m 'feat: your message'"
    echo "  sh ${MAIN_REPO}/scripts/create-pr.sh $ticket"
    echo ""
}

# Main
if [[ $# -lt 2 ]]; then
    echo "Usage: $0 <TICKET> <description> [base-branch]"
    echo ""
    echo "Examples:"
    echo "  $0 PROJ-123 user-authentication"
    echo "  $0 PROJ-124 fix-login-bug develop"
    exit 1
fi

create_feature "$@"
```

**Utilisation:**

```bash
cd my-project
sh scripts/create-feature.sh PROJ-123 user-authentication
# Crée: worktrees/PROJ-123 + branche feature/PROJ-123-user-authentication

cd worktrees/PROJ-123
# ... faire des modifications ...
git add .
git commit -m "feat: add user login form"
```

---

### 2. Script de Création de PR Automatique

**`scripts/create-pr.sh`**

```bash
#!/bin/bash
set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

MAIN_REPO="$(git rev-parse --show-toplevel)"
WORKTREES_DIR="${MAIN_REPO}/worktrees"
PR_TEMPLATE="${MAIN_REPO}/.github/pr-template.md"
DEFAULT_BASE_BRANCH="main"

log_error() {
    echo -e "${RED}❌ ERROR: $1${NC}" >&2
}

log_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

log_info() {
    echo -e "${YELLOW}ℹ️  $1${NC}"
}

log_debug() {
    echo -e "${BLUE}ℹ️  DEBUG: $1${NC}"
}

extract_ticket_from_branch() {
    local branch="$1"
    # From: feature/PROJ-123-description → PROJ-123
    echo "$branch" | sed -E 's|.*/([A-Z]+-[0-9]+).*|\1|'
}

get_current_branch() {
    git rev-parse --abbrev-ref HEAD
}

validate_branch_format() {
    local branch="$1"
    if [[ ! "$branch" =~ ^feature/[A-Z]+-[0-9]+- ]]; then
        log_error "Branch must follow format: feature/TICKET-description"
        log_error "Current branch: $branch"
        return 1
    fi
    return 0
}

check_branch_pushed() {
    local branch="$1"
    if ! git ls-remote --heads origin "$branch" | grep -q "$branch"; then
        log_error "Branch not found on remote. Please push first:"
        log_error "  git push -u origin $branch"
        return 1
    fi
    return 0
}

count_commits() {
    local base_branch="${1:-${DEFAULT_BASE_BRANCH}}"
    git rev-list --count "origin/${base_branch}..HEAD"
}

generate_pr_body() {
    local ticket="$1"
    local base_branch="${2:-${DEFAULT_BASE_BRANCH}}"
    
    if [[ -f "$PR_TEMPLATE" ]]; then
        log_info "Using PR template from: $PR_TEMPLATE"
        cat "$PR_TEMPLATE" | sed "s|{TICKET}|${ticket}|g"
    else
        # Default template
        cat << EOF
## 🎯 Objective
Resolves #${ticket}

## 📝 Description
<!-- Describe your changes here -->

## 🔄 Related Issue
Closes #${ticket}

## 📋 Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex logic
- [ ] Tests added/updated
- [ ] No breaking changes

## 🧪 Testing
<!-- Describe testing performed -->

## 📸 Screenshots (if applicable)
<!-- Add screenshots for UI changes -->
EOF
    fi
}

create_pr() {
    local base_branch="${1:-${DEFAULT_BASE_BRANCH}}"
    local draft_mode="${2:-false}"
    
    # Get current branch
    local current_branch
    current_branch=$(get_current_branch)
    
    # Validate branch format
    validate_branch_format "$current_branch" || return 1
    
    # Check if branch is pushed
    log_info "Checking if branch is pushed to remote..."
    check_branch_pushed "$current_branch" || return 1
    
    # Extract ticket ID
    local ticket
    ticket=$(extract_ticket_from_branch "$current_branch")
    
    # Extract description from branch name
    local description
    description=$(echo "$current_branch" | sed -E 's|feature/[A-Z]+-[0-9]+-(.*)|\1|' | tr '-' ' ')
    
    log_info "Creating PR for: $current_branch"
    log_info "Ticket: $ticket"
    log_info "Description: $description"
    
    # Generate PR title
    local pr_title="${ticket}: ${description}"
    
    # Generate PR body
    local pr_body
    pr_body=$(generate_pr_body "$ticket" "$base_branch")
    
    # Create temporary file for body
    local body_file
    body_file=$(mktemp)
    echo "$pr_body" > "$body_file"
    
    log_info "PR Title: $pr_title"
    log_debug "PR Body file: $body_file"
    
    # Count commits for info
    local commit_count
    commit_count=$(count_commits "$base_branch")
    log_info "Commits since $base_branch: $commit_count"
    
    # Build gh pr create command
    local gh_args=(
        "pr"
        "create"
        "--title" "$pr_title"
        "--body-file" "$body_file"
        "--base" "$base_branch"
        "--head" "$current_branch"
    )
    
    if [[ "$draft_mode" == "true" ]]; then
        gh_args+=("--draft")
        log_info "Creating as DRAFT"
    fi
    
    # Create PR
    log_info "Creating PR via GitHub CLI..."
    if gh "${gh_args[@]}"; then
        log_success "PR created successfully!"
        
        # Get PR info
        local pr_number
        pr_number=$(gh pr view --json number -q .number 2>/dev/null || echo "unknown")
        log_success "PR #${pr_number}: $pr_title"
        
        # Get PR URL
        local pr_url
        pr_url=$(gh pr view --json url -q .url 2>/dev/null || echo "")
        if [[ -n "$pr_url" ]]; then
            log_info "View PR: $pr_url"
        fi
    else
        log_error "Failed to create PR"
        rm -f "$body_file"
        return 1
    fi
    
    # Cleanup
    rm -f "$body_file"
}

# Main
case "${1:-}" in
    --draft)
        create_pr "${2:-${DEFAULT_BASE_BRANCH}}" "true"
        ;;
    *)
        create_pr "${1:-${DEFAULT_BASE_BRANCH}}"
        ;;
esac
```

**Utilisation:**

```bash
cd worktrees/PROJ-123
git add .
git commit -m "feat: add login form"
git push -u origin feature/PROJ-123-user-authentication

# Create PR (interactive mode with template)
sh ../../scripts/create-pr.sh

# Create PR as draft
sh ../../scripts/create-pr.sh --draft

# Create PR against different base branch
sh ../../scripts/create-pr.sh develop
```

---

### 3. Script de Gestion des Worktrees

**`scripts/manage-worktrees.sh`**

```bash
#!/bin/bash
set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

MAIN_REPO="$(git rev-parse --show-toplevel)"
WORKTREES_DIR="${MAIN_REPO}/worktrees"

log_error() {
    echo -e "${RED}❌ ERROR: $1${NC}" >&2
}

log_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

log_info() {
    echo -e "${YELLOW}ℹ️  $1${NC}"
}

log_header() {
    echo -e "${BLUE}═══ $1 ═══${NC}"
}

# List all active worktrees with status
list_worktrees() {
    log_header "Active Worktrees"
    
    if [[ ! -d "$WORKTREES_DIR" ]]; then
        log_info "No worktrees directory found"
        return 0
    fi
    
    local count=0
    
    git worktree list --porcelain | while IFS= read -r line; do
        if [[ $line =~ ^worktree ]]; then
            local path="${line#worktree }"
            local ticket=$(basename "$path")
            
            # Skip if not in our worktrees directory
            if [[ ! "$path" =~ ${WORKTREES_DIR} ]]; then
                continue
            fi
            
            count=$((count + 1))
            
            # Get branch info
            (
                cd "$path" 2>/dev/null || return
                local branch
                branch=$(git rev-parse --abbrev-ref HEAD)
                local commit
                commit=$(git rev-parse --short HEAD)
                local status
                status=$(git status --short | wc -l)
                
                printf "%3d. %-15s %s (%d changes)\n" \
                    "$count" "$ticket" "$branch [$commit]" "$status"
            )
        fi
    done
    
    if [[ $count -eq 0 ]]; then
        log_info "No active worktrees"
    else
        echo ""
        log_info "Total: $count worktree(s)"
    fi
}

# Show detailed status of a specific worktree
show_worktree_status() {
    local ticket="$1"
    local worktree_path="${WORKTREES_DIR}/${ticket}"
    
    if [[ ! -d "$worktree_path" ]]; then
        log_error "Worktree not found: $ticket"
        return 1
    fi
    
    log_header "Worktree: $ticket"
    
    (
        cd "$worktree_path"
        
        echo "Path: $(pwd)"
        echo "Branch: $(git rev-parse --abbrev-ref HEAD)"
        echo "Commit: $(git rev-parse HEAD)"
        echo ""
        
        log_header "Status"
        git status --short || true
        echo ""
        
        log_header "Unpushed Commits"
        git log --oneline -n 5 "origin/main..HEAD" 2>/dev/null || \
            git log --oneline -n 5 "origin/develop..HEAD" 2>/dev/null || \
            echo "No unpushed commits"
    )
}

# Remove a worktree
remove_worktree() {
    local ticket="$1"
    local worktree_path="${WORKTREES_DIR}/${ticket}"
    
    if [[ ! -d "$worktree_path" ]]; then
        log_error "Worktree not found: $ticket"
        return 1
    fi
    
    log_info "Checking for unsaved changes in $ticket..."
    (
        cd "$worktree_path"
        if [[ -n $(git status --short) ]]; then
            log_error "Unsaved changes detected. Stash or commit first:"
            git status --short
            return 1
        fi
    ) || return 1
    
    log_info "Removing worktree: $ticket"
    if git worktree remove "$worktree_path"; then
        log_success "Worktree removed: $ticket"
    else
        log_error "Failed to remove worktree: $ticket"
        return 1
    fi
}

# Cleanup orphaned worktrees (metadata only)
cleanup_orphaned() {
    log_header "Cleaning up orphaned worktrees"
    
    if git worktree prune --verbose; then
        log_success "Cleanup completed"
    else
        log_error "Cleanup failed"
        return 1
    fi
}

# Fetch updates for all worktrees
fetch_all() {
    log_header "Fetching updates for all worktrees"
    
    git worktree list --porcelain | while IFS= read -r line; do
        if [[ $line =~ ^worktree ]]; then
            local path="${line#worktree }"
            if [[ ! "$path" =~ ${WORKTREES_DIR} ]]; then
                continue
            fi
            
            local ticket=$(basename "$path")
            (
                cd "$path"
                log_info "Fetching in $ticket..."
                git fetch origin
            ) || log_error "Fetch failed in $ticket"
        fi
    done
}

# Main command routing
case "${1:-help}" in
    list)
        list_worktrees
        ;;
    status)
        if [[ -z "${2:-}" ]]; then
            log_error "Usage: $0 status <TICKET>"
            exit 1
        fi
        show_worktree_status "$2"
        ;;
    remove)
        if [[ -z "${2:-}" ]]; then
            log_error "Usage: $0 remove <TICKET>"
            exit 1
        fi
        remove_worktree "$2"
        ;;
    cleanup)
        cleanup_orphaned
        ;;
    fetch)
        fetch_all
        ;;
    *)
        echo "Git Worktree Manager"
        echo ""
        echo "Usage: $0 <command> [args]"
        echo ""
        echo "Commands:"
        echo "  list                    - List all active worktrees"
        echo "  status <TICKET>         - Show detailed status of a worktree"
        echo "  remove <TICKET>         - Remove a worktree"
        echo "  cleanup                 - Clean orphaned worktree metadata"
        echo "  fetch                   - Fetch updates in all worktrees"
        echo ""
        echo "Examples:"
        echo "  $0 list"
        echo "  $0 status PROJ-123"
        echo "  $0 remove PROJ-123"
        exit 1
        ;;
esac
```

**Utilisation:**

```bash
# Lister tous les worktrees actifs
sh scripts/manage-worktrees.sh list

# Voir le statut d'un worktree spécifique
sh scripts/manage-worktrees.sh status PROJ-123

# Supprimer un worktree
sh scripts/manage-worktrees.sh remove PROJ-123

# Nettoyer les métadonnées orphelines
sh scripts/manage-worktrees.sh cleanup

# Fetch updates dans tous les worktrees
sh scripts/manage-worktrees.sh fetch
```

---

### 4. Script Wrapper pour Opérations dans un Worktree

**`scripts/worktree-exec.sh`**

```bash
#!/bin/bash
set -euo pipefail

MAIN_REPO="$(pwd)"
WORKTREES_DIR="${MAIN_REPO}/worktrees"

if [[ $# -lt 2 ]]; then
    echo "Usage: $0 <TICKET> <command> [args...]"
    echo ""
    echo "Execute a command inside a worktree context"
    echo ""
    echo "Examples:"
    echo "  $0 PROJ-123 npm test"
    echo "  $0 PROJ-123 make build"
    echo "  $0 PROJ-123 sh -c 'npm test && npm run lint'"
    exit 1
fi

TICKET="$1"
shift  # Remove first argument
COMMAND=("$@")

WORKTREE_PATH="${WORKTREES_DIR}/${TICKET}"

if [[ ! -d "$WORKTREE_PATH" ]]; then
    echo "❌ Worktree not found: $TICKET (path: $WORKTREE_PATH)"
    exit 1
fi

echo "📂 Executing in: $WORKTREE_PATH"
echo "🔧 Command: ${COMMAND[*]}"
echo ""

# Execute command in worktree context
cd "$WORKTREE_PATH"
exec "${COMMAND[@]}"
```

**Utilisation:**

```bash
# Run tests in a worktree
sh scripts/worktree-exec.sh PROJ-123 npm test

# Run build
sh scripts/worktree-exec.sh PROJ-123 npm run build

# Run complex command
sh scripts/worktree-exec.sh PROJ-123 sh -c 'npm test && npm run lint && npm run build'

# Run custom script
sh scripts/worktree-exec.sh PROJ-123 sh ../../../your-setup-script.sh
```

---

## GitHub Actions Workflow

### PR Template

**`.github/pr-template.md`**

```markdown
## 🎯 Objective
<!-- Link to ticket/issue -->
Resolves #{TICKET}

## 📝 Description
<!-- Describe your changes here in detail -->

## 🔄 Type of Change
- [ ] 🐛 Bug fix
- [ ] ✨ New feature
- [ ] 📚 Documentation
- [ ] 🔧 Configuration/Infrastructure
- [ ] ♻️  Refactoring
- [ ] ⚡ Performance improvement
- [ ] 🧪 Tests

## 📋 Checklist
- [ ] Code follows project style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex logic
- [ ] Documentation updated
- [ ] Tests added/updated
- [ ] No breaking changes
- [ ] Changes reviewed for security issues

## 🧪 Testing
<!-- Describe testing performed -->
- [ ] Manual testing completed
- [ ] Unit tests passing
- [ ] Integration tests passing
- [ ] E2E tests passing (if applicable)

## 📸 Screenshots
<!-- Add screenshots for UI changes, if applicable -->

## 📋 Additional Notes
<!-- Any additional information reviewers should know -->

---
**Related:** 
- Issue: #{TICKET}
- Breaking changes: No
```

### Workflow: Cleanup Post-Merge

**`.github/workflows/cleanup-worktree.yml`**

```yaml
name: Cleanup Worktree on PR Merge

on:
  pull_request:
    types: [closed]

permissions:
  contents: write
  pull-requests: read

jobs:
  cleanup:
    # Only run if PR was merged (not just closed)
    if: github.event.pull_request.merged == true
    
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout main repo
        uses: actions/checkout@v4
        with:
          fetch-depth: 0
      
      - name: Extract ticket from branch
        id: extract
        run: |
          BRANCH_NAME="${{ github.head_ref }}"
          TICKET=$(echo "$BRANCH_NAME" | sed -E 's|feature/([A-Z]+-[0-9]+).*|\1|')
          echo "ticket=$TICKET" >> $GITHUB_OUTPUT
          echo "branch=$BRANCH_NAME" >> $GITHUB_OUTPUT
      
      - name: Log merge info
        run: |
          echo "✅ PR Merged!"
          echo "Branch: ${{ steps.extract.outputs.branch }}"
          echo "Ticket: ${{ steps.extract.outputs.ticket }}"
          echo "PR: #${{ github.event.number }}"
      
      - name: Notify cleanup
        run: |
          echo "🧹 To clean up locally, run:"
          echo ""
          echo "  git worktree remove worktrees/${{ steps.extract.outputs.ticket }}"
          echo "  git worktree prune"
          echo ""
          echo "Or use the management script:"
          echo "  sh scripts/manage-worktrees.sh remove ${{ steps.extract.outputs.ticket }}"
      
      - name: Comment on PR
        uses: actions/github-script@v7
        with:
          script: |
            const ticket = '${{ steps.extract.outputs.ticket }}';
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: `## 🧹 Cleanup Complete
              
              To remove the worktree locally:
              \`\`\`bash
              git worktree remove worktrees/${ticket}
              git worktree prune
              \`\`\`
              
              Or use the management script:
              \`\`\`bash
              sh scripts/manage-worktrees.sh remove ${ticket}
              \`\`\`
              `
            })
```

---

## Gestion des Worktrees

### Opérations Basiques

```bash
# Lister tous les worktrees
git worktree list

# Avec format verbose
git worktree list --verbose

# Format porcelain (pour scripts)
git worktree list --porcelain

# Ajouter un worktree (basic)
git worktree add worktrees/PROJ-123 -b feature/PROJ-123-description

# Supprimer un worktree
git worktree remove worktrees/PROJ-123

# Nettoyer les métadonnées orphelines
git worktree prune

# Prune verbose
git worktree prune --verbose

# Nettoyer plus agressivement
git worktree prune --expire=now
```

### Alias Utiles

Ajouter à `.git/config` ou `~/.gitconfig`:

```ini
[alias]
    wt-list = worktree list --verbose
    wt-add = worktree add
    wt-rm = worktree remove
    wt-prune = worktree prune --verbose
    wt-clean = worktree prune --verbose --expire=now
    wt-status = "!sh scripts/manage-worktrees.sh status"
    wt-fetch = "!git worktree list --porcelain | awk '{print $2}' | xargs -I {} sh -c 'cd {} && git fetch origin'"
```

**Utilisation:**

```bash
git wt-list
git wt-add worktrees/PROJ-123 -b feature/PROJ-123-desc
git wt-rm worktrees/PROJ-123
git wt-fetch
```

### Détection Avancée du Merge

**`.github/workflows/cleanup-advanced.yml`**

```yaml
name: Advanced Worktree Cleanup

on:
  workflow_run:
    workflows: ["CI/CD Pipeline"]
    types: [completed]
  pull_request:
    types: [closed]

jobs:
  cleanup:
    runs-on: ubuntu-latest
    
    outputs:
      ticket: ${{ steps.extract.outputs.ticket }}
      merged: ${{ steps.check-merge.outputs.merged }}
    
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      
      - name: Extract ticket
        id: extract
        run: |
          BRANCH="${{ github.head_ref }}"
          TICKET=$(echo "$BRANCH" | sed -E 's|.*/([A-Z]+-[0-9]+).*|\1|')
          echo "ticket=$TICKET" >> $GITHUB_OUTPUT
      
      - name: Check if PR was merged
        id: check-merge
        run: |
          if [[ "${{ github.event.pull_request.merged }}" == "true" ]]; then
            echo "merged=true" >> $GITHUB_OUTPUT
          else
            echo "merged=false" >> $GITHUB_OUTPUT
          fi
      
      - name: Notify developers
        if: steps.check-merge.outputs.merged == 'true'
        uses: actions/github-script@v7
        with:
          script: |
            const ticket = '${{ steps.extract.outputs.ticket }}';
            const owner = context.repo.owner;
            const repo = context.repo.repo;
            
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: owner,
              repo: repo,
              body: `## 🎉 PR Merged!
              
              Your feature branch has been merged to main. 
              
              ### Local Cleanup
              
              Remove your worktree to keep the repository clean:
              
              \`\`\`bash
              sh scripts/manage-worktrees.sh remove ${ticket}
              \`\`\`
              
              Or manually:
              \`\`\`bash
              git worktree remove worktrees/${ticket}
              git worktree prune
              \`\`\`
              `
            })
```

---

## Patterns Avancés

### 1. Hooks Pre-commit dans Worktree

**`.git/hooks/pre-commit`** (ou **`.githooks/pre-commit`** + `git config core.hooksPath`)

```bash
#!/bin/bash

# Get current worktree ticket
WORKTREE_PATH=$(git rev-parse --git-dir)
TICKET=$(basename "$(dirname "$WORKTREE_PATH")" 2>/dev/null || echo "")

# Run linting if available
if command -v npm &> /dev/null; then
    npm run lint --fix
fi

# Check code quality
if command -v eslint &> /dev/null; then
    eslint . --fix || exit 1
fi

exit 0
```

### 2. Commandes Composées

```bash
# Create feature and enter immediately
create_and_enter() {
    local ticket="$1"
    local desc="$2"
    sh scripts/create-feature.sh "$ticket" "$desc" && \
    cd "worktrees/$ticket"
}

# Create feature, run setup, commit
create_and_setup() {
    local ticket="$1"
    local desc="$2"
    sh scripts/create-feature.sh "$ticket" "$desc" && \
    sh scripts/worktree-exec.sh "$ticket" npm install && \
    cd "worktrees/$ticket"
}

# Create PR and switch back to main
create_pr_and_return() {
    sh scripts/create-pr.sh && \
    cd ../.. && \
    git checkout main
}
```

### 3. Dashboard de Monitoring

**`scripts/dashboard.sh`**

```bash
#!/bin/bash

clear

echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║         Git Worktree Development Dashboard                    ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""

MAIN_REPO="$(pwd)"
WORKTREES_DIR="${MAIN_REPO}/worktrees"

# Active worktrees
echo "📂 Active Worktrees:"
git worktree list --porcelain | grep -E "^worktree.*${WORKTREES_DIR}" | while IFS= read -r line; do
    path=$(echo "$line" | awk '{print $2}')
    ticket=$(basename "$path")
    (
        cd "$path"
        branch=$(git rev-parse --abbrev-ref HEAD)
        commit=$(git rev-parse --short HEAD)
        changes=$(git status --short | wc -l)
        printf "   %-15s %s (%d changes)\n" "$ticket" "$branch [$commit]" "$changes"
    )
done

echo ""
echo "📊 Repository Status:"
echo "   Main branch: $(git branch --show-current)"
echo "   Latest commit: $(git log -1 --pretty='%h - %s (%ar)')"

echo ""
echo "🔗 Remote Status:"
git fetch origin 2>/dev/null
echo "   Branch count: $(git branch -r | wc -l)"

echo ""
echo "💻 Commands:"
echo "   Create feature:     sh scripts/create-feature.sh TICKET description"
echo "   List worktrees:     sh scripts/manage-worktrees.sh list"
echo "   Create PR:          sh scripts/create-pr.sh"
echo "   Remove worktree:    sh scripts/manage-worktrees.sh remove TICKET"
echo ""
```

---

## Options `gh pr create` Complètes

| Option | Description | Exemple |
|--------|-------------|---------|
| `--title` | Titre de la PR (requis si --fill absent) | `--title "feat: add login"` |
| `--body` | Corps de la PR en Markdown | `--body "Fixes #123"` |
| `--body-file FILE` | Lire le corps depuis un fichier | `--body-file pr-body.md` |
| `--template FILE` | Utiliser un template comme base | `--template .github/pr-template.md` |
| `--base BRANCH` | Branche cible (défaut: main) | `--base develop` |
| `--head BRANCH` | Branche source | `--head feature/PROJ-123` |
| `--draft` | Créer en mode draft | `--draft` |
| `--fill` | Auto-remplir depuis commits | `--fill` |
| `--fill-verbose` | Like --fill mais avec bodies | `--fill-verbose` |
| `--reviewer USER` | Assigner des reviewers | `--reviewer alice,bob` |
| `--assignee USER` | Assigner des assignees | `--assignee alice` |
| `--label LABEL` | Ajouter des labels | `--label "type:feature,priority:high"` |
| `--milestone MILESTONE` | Assigner à un milestone | `--milestone "v1.0"` |
| `--web` | Ouvrir dans le navigateur | `--web` |

**Exemple complet:**

```bash
gh pr create \
    --title "feat: user authentication" \
    --body-file pr-body.md \
    --base main \
    --head feature/PROJ-123-user-auth \
    --reviewer alice,bob \
    --assignee alice \
    --label "type:feature,priority:high" \
    --milestone "v1.0" \
    --web
```

---

## Troubleshooting

### Problème: "fatal: 'worktrees/TICKET' is already checked out"

**Cause:** Même branche dans deux worktrees

**Solutions:**

```bash
# 1. Lister tous les worktrees avec branches
git worktree list

# 2. Trouver où la branche est utilisée
git worktree list | grep "feature/PROJ-123"

# 3. Supprimer le worktree en conflit
git worktree remove worktrees/TICKET-OLD

# 4. Ou forcer si le répertoire a disparu
git worktree prune
```

### Problème: Worktree orpheline

**Cause:** Répertoire supprimé manuellement

**Solution:**

```bash
# Nettoyer
git worktree prune --verbose

# Plus agressif
git worktree prune --expire=now
```

### Problème: "Failed to create worktree - file exists"

**Cause:** Répertoire existe déjà

**Solution:**

```bash
# Vérifier et supprimer
rm -rf worktrees/PROJ-123
git worktree prune

# Recréer
git worktree add worktrees/PROJ-123 -b feature/PROJ-123-desc
```

### Problème: Branch push fails après creation

**Cause:** Branch locale non créée avant push

**Solution dans script:**

```bash
# Après git worktree add --detach
cd worktrees/PROJ-123
git checkout -b feature/PROJ-123-desc  # Créer la branche d'abord
git push -u origin feature/PROJ-123-desc
```

### Problème: Cannot remove worktree - has changes

**Solution:**

```bash
# Stash les changements
cd worktrees/PROJ-123
git stash

# Puis supprimer
git worktree remove .

# Ou revenir au repo principal
cd ../..
git worktree remove worktrees/PROJ-123
```

---

## Intégration avec Editeurs

### VS Code

**`.vscode/extensions.json`**

```json
{
  "recommendations": [
    "eamodio.gitlens",
    "GitHub.vscode-github-actions",
    "GitHub.copilot"
  ]
}
```

**`.vscode/settings.json`**

```json
{
  "git.ignoreLimitWarning": true,
  "[shellscript]": {
    "editor.defaultFormatter": "foxundermoon.shell-format"
  },
  "terminal.integrated.defaultProfile.linux": "bash"
}
```

### Zed (Pour votre setup)

**`.zed/settings.json`**

```json
{
  "git_status": true,
  "tab_bar_position": "top",
  "relative_line_numbers": true
}
```

### Fish Shell Alias

**`config/fish/config.fish`**

```fish
# Git worktree aliases
alias gwt-create="sh scripts/create-feature.sh"
alias gwt-list="sh scripts/manage-worktrees.sh list"
alias gwt-remove="sh scripts/manage-worktrees.sh remove"
alias gwt-status="sh scripts/manage-worktrees.sh status"
alias gwt-pr="sh scripts/create-pr.sh"

# Quick workflow
function gwt-full
    set ticket $argv[1]
    set desc $argv[2]
    sh scripts/create-feature.sh $ticket $desc && \
    cd "worktrees/$ticket" && \
    pwd
end
```

---

## Performance et Limitations

### Limitations de Git Worktree

| Limite | Description | Mitigation |
|--------|-------------|-----------|
| **Une branche par worktree** | Branche ne peut pas être checked out ailleurs | Créer branche unique par worktree |
| **Métadonnées partagées** | `.git/worktrees/` centralisé | Prune régulier |
| **Hooks partagés** | Pre/post-commit globaux | Utiliser core.hooksPath |
| **Objets partagés** | Disque utilisé pour tous | Normal, économique |

### Optimisations

```bash
# Worktree avec shallow clone (moins de disque)
git worktree add --detach worktrees/TICKET origin/main --depth=50

# Bare repository pour multi-worktrees (avancé)
git clone --bare https://github.com/user/repo repo.git
cd repo.git
git worktree add ../worktrees/main
git worktree add ../worktrees/PROJ-123 -b feature/PROJ-123

# Reduce .git size
git gc --aggressive
```

---

## Checklist Implémentation

- [ ] Créer dossier `scripts/`
- [ ] Copier `create-feature.sh` et rendre exécutable
- [ ] Copier `create-pr.sh` et rendre exécutable
- [ ] Copier `manage-worktrees.sh` et rendre exécutable
- [ ] Créer `pr-template.md` dans `.github/`
- [ ] Configurer `.github/workflows/cleanup-worktree.yml`
- [ ] Ajouter aliases git dans `.git/config`
- [ ] Tester workflow complet avec une feature test
- [ ] Former l'équipe aux commandes
- [ ] Documenter conventions de naming dans CONTRIBUTING.md

---

## Conclusion

Ce workflow offre une automatisation complète du cycle feature:

✅ **Création rapide** : `sh scripts/create-feature.sh PROJ-123 description`
✅ **Isolation** : Chaque feature dans son répertoire
✅ **PR automatique** : Template + cleanup post-merge
✅ **Parallélisation** : Plusieurs features simultanément
✅ **Gestion** : Scripts pour monitoring et cleanup
✅ **Production-ready** : Tous les cas d'erreur gérés

Les scripts sont conçus pour être chainables et intégrables dans des outils comme n8n ou des GitHub Actions avancées.
