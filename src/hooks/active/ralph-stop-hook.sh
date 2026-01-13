#!/bin/bash
# =============================================================================
# Ralph Stop Hook for Claude Code
# =============================================================================
# Implements the Anthropic-style stop hook for Ralph Wiggum integration.
# This hook intercepts Claude's exit and reinjects the prompt for continuous
# autonomous execution.
#
# Based on: anthropics/claude-plugins-official/ralph-loop
# EPCI Integration: v1.0
#
# Usage:
#   This hook is automatically invoked by Claude Code when configured.
#   It reads state from .claude/ralph-loop.local.md
#
# =============================================================================

set -e

# Configuration
STATE_FILE=".claude/ralph-loop.local.md"
COMPLETION_PROMISE="COMPLETE"
MAX_ITERATIONS=50

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

log_info() {
    echo -e "${BLUE}[ralph-hook]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[ralph-hook]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[ralph-hook]${NC} $1"
}

log_error() {
    echo -e "${RED}[ralph-hook]${NC} $1"
}

# Get ISO timestamp
get_timestamp() {
    date -u +"%Y-%m-%dT%H:%M:%SZ"
}

# =============================================================================
# STATE MANAGEMENT
# =============================================================================

# Check if state file exists
check_state_file() {
    if [[ ! -f "$STATE_FILE" ]]; then
        log_info "No Ralph loop active (state file not found)"
        return 1
    fi
    return 0
}

# Read YAML frontmatter value from state file
read_state_value() {
    local key="$1"
    local default="$2"

    if [[ ! -f "$STATE_FILE" ]]; then
        echo "$default"
        return
    fi

    # Extract value from YAML frontmatter (between --- markers)
    local value=$(awk '/^---$/{p=!p;next} p && /^'"$key"':/{gsub(/^'"$key"': */, ""); print; exit}' "$STATE_FILE")

    if [[ -z "$value" ]]; then
        echo "$default"
    else
        # Remove quotes if present
        echo "$value" | sed 's/^["'"'"']//;s/["'"'"']$//'
    fi
}

# Update state file with new iteration
update_state() {
    local new_iteration="$1"
    local new_status="${2:-RUNNING}"

    if [[ ! -f "$STATE_FILE" ]]; then
        return 1
    fi

    # Validate iteration is a number
    if ! [[ "$new_iteration" =~ ^[0-9]+$ ]]; then
        log_error "Invalid iteration value: $new_iteration"
        return 1
    fi

    # Validate status against allowed values (security: prevent command injection)
    case "$new_status" in
        RUNNING|PAUSED|COMPLETE|CANCELLED|BLOCKED)
            ;;
        *)
            log_error "Invalid status value: $new_status"
            return 1
            ;;
    esac

    # Update iteration count in YAML frontmatter
    sed -i "s/^iteration: .*/iteration: $new_iteration/" "$STATE_FILE"
    sed -i "s/^status: .*/status: $new_status/" "$STATE_FILE"
    sed -i "s/^last_update: .*/last_update: $(get_timestamp)/" "$STATE_FILE"
}

# =============================================================================
# COMPLETION DETECTION
# =============================================================================

# Check if completion promise is present in Claude's output
check_completion_promise() {
    local output="$1"
    local promise=$(read_state_value "completion_promise" "$COMPLETION_PROMISE")

    # Check for <promise>COMPLETE</promise> pattern (Anthropic style)
    if echo "$output" | grep -q "<promise>$promise</promise>"; then
        return 0
    fi

    # Also check for bare promise word at end of output
    if echo "$output" | tail -5 | grep -qw "$promise"; then
        return 0
    fi

    return 1
}

# =============================================================================
# MAIN HOOK LOGIC
# =============================================================================

# Main hook function - called when Claude attempts to exit
ralph_stop_hook() {
    local claude_output="$1"

    # Check if Ralph loop is active
    if ! check_state_file; then
        # No active loop, allow normal exit
        return 0
    fi

    # Read current state
    local current_iteration=$(read_state_value "iteration" "1")
    local max_iter=$(read_state_value "max_iterations" "$MAX_ITERATIONS")
    local status=$(read_state_value "status" "RUNNING")

    # Check if loop is paused or cancelled
    if [[ "$status" == "PAUSED" ]] || [[ "$status" == "CANCELLED" ]]; then
        log_info "Ralph loop is $status, allowing exit"
        return 0
    fi

    # Check for completion promise
    if check_completion_promise "$claude_output"; then
        log_success "Completion promise detected! Ralph loop complete."
        update_state "$current_iteration" "COMPLETE"
        return 0
    fi

    # Check iteration limit
    if [[ $current_iteration -ge $max_iter ]]; then
        log_warning "Max iterations ($max_iter) reached. Stopping Ralph loop."
        update_state "$current_iteration" "COMPLETE"
        return 0
    fi

    # Increment iteration and continue
    local next_iteration=$((current_iteration + 1))
    update_state "$next_iteration" "RUNNING"

    log_info "Iteration $current_iteration complete. Starting iteration $next_iteration/$max_iter"

    # Return non-zero to signal hook should reinject prompt
    # The prompt is read from the state file (after YAML frontmatter)
    return 2
}

# =============================================================================
# HOOK ENTRY POINT
# =============================================================================

# This script is sourced by the hook runner
# The main function will be called with Claude's output as argument

# If run directly (for testing), execute main function
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    if [[ $# -eq 0 ]]; then
        echo "Usage: $0 <claude_output>"
        echo "  Or source this script and call ralph_stop_hook()"
        exit 1
    fi

    ralph_stop_hook "$1"
    exit $?
fi

# Export functions for sourcing
export -f ralph_stop_hook
export -f check_state_file
export -f read_state_value
export -f update_state
export -f check_completion_promise
