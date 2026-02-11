#!/bin/bash
# lib/config.sh — Environment and project configuration loader
# Sources lib/common.sh for logging. Provides load_env(), load_projects(), get_project_config().
# Usage: source "$(dirname "${BASH_SOURCE[0]}")/../lib/config.sh"

# Source common utilities
source "$(dirname "${BASH_SOURCE[0]}")/common.sh"

# Required environment variables
_REQUIRED_ENV_VARS=(
    "NOTION_API_KEY"
    "GITHUB_TOKEN"
    "TELEGRAM_BOT_TOKEN"
    "TELEGRAM_CHAT_ID"
)

# Module-level: loaded projects data (JSON string)
_PROJECTS_JSON=""

# Load and validate a .env file
# Arguments:
#   $1 - path to .env file
# Returns:
#   0 on success, 1 on failure
load_env() {
    local env_file="$1"

    if [[ ! -f "$env_file" ]]; then
        log_error "Environment file not found: $env_file"
        return 1
    fi

    # Source the .env file (skip comments and blank lines)
    while IFS='=' read -r key value; do
        # Skip comments and empty lines
        [[ -z "$key" || "$key" =~ ^# ]] && continue
        # Trim whitespace
        key=$(echo "$key" | xargs)
        value=$(echo "$value" | xargs)
        export "$key=$value"
    done < "$env_file"

    # Validate required variables
    local missing=()
    for var in "${_REQUIRED_ENV_VARS[@]}"; do
        if [[ -z "${!var:-}" ]]; then
            missing+=("$var")
        fi
    done

    if [[ ${#missing[@]} -gt 0 ]]; then
        log_error "Missing required environment variables: ${missing[*]}"
        return 1
    fi

    log_info "Environment loaded from $env_file"
    return 0
}

# Load and validate projects.json
# Arguments:
#   $1 - path to projects.json
# Returns:
#   0 on success, 1 on failure
load_projects() {
    local projects_file="$1"

    if [[ ! -f "$projects_file" ]]; then
        log_error "Projects file not found: $projects_file"
        return 1
    fi

    # Validate JSON syntax
    if ! jq '.' "$projects_file" >/dev/null 2>&1; then
        log_error "Invalid JSON in projects file: $projects_file"
        return 1
    fi

    # Validate required fields per project entry
    local required_fields=("slug" "directory" "github_repo" "notion_project_id")
    local project_count
    project_count=$(jq '.projects | length' "$projects_file")

    local i
    for ((i = 0; i < project_count; i++)); do
        for field in "${required_fields[@]}"; do
            local value
            value=$(jq -r ".projects[$i].$field // empty" "$projects_file")
            if [[ -z "$value" ]]; then
                local slug
                slug=$(jq -r ".projects[$i].slug // \"entry[$i]\"" "$projects_file")
                log_error "Project '$slug' missing required field: $field"
                return 1
            fi
        done
    done

    # Store validated JSON for later use
    _PROJECTS_JSON=$(cat "$projects_file")
    log_info "Loaded $project_count project(s) from $projects_file"
    return 0
}

# Get configuration for a single project by slug
# Arguments:
#   $1 - project slug
# Returns:
#   JSON object on stdout, 0 on success, 1 if not found
get_project_config() {
    local slug="$1"

    if [[ -z "$_PROJECTS_JSON" ]]; then
        log_error "Projects not loaded. Call load_projects() first."
        return 1
    fi

    local result
    result=$(echo "$_PROJECTS_JSON" | jq -e ".projects[] | select(.slug == \"$slug\")" 2>/dev/null)

    if [[ -z "$result" ]]; then
        log_error "Project not found: $slug"
        return 1
    fi

    echo "$result"
    return 0
}
