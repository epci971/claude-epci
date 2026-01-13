#!/bin/bash
# =============================================================================
# Date Utilities for Ralph Wiggum
# =============================================================================
# Cross-platform date utilities for consistent timestamp generation.
# Adapted from frankbria/ralph-claude-code/lib/date_utils.sh
#
# EPCI Integration: v1.0
# =============================================================================

# Get ISO 8601 timestamp (UTC)
# Works on both macOS (BSD date) and Linux (GNU date)
get_iso_timestamp() {
    if date --version >/dev/null 2>&1; then
        # GNU date (Linux)
        date -u +"%Y-%m-%dT%H:%M:%SZ"
    else
        # BSD date (macOS)
        date -u +"%Y-%m-%dT%H:%M:%SZ"
    fi
}

# Get Unix timestamp (seconds since epoch)
get_unix_timestamp() {
    date +%s
}

# Get human-readable timestamp for logs
get_log_timestamp() {
    date +"%Y-%m-%d %H:%M:%S"
}

# Calculate elapsed time between two Unix timestamps
# Usage: elapsed_time $start_timestamp $end_timestamp
elapsed_time() {
    local start=$1
    local end=$2
    local diff=$((end - start))

    local hours=$((diff / 3600))
    local minutes=$(((diff % 3600) / 60))
    local seconds=$((diff % 60))

    if [[ $hours -gt 0 ]]; then
        printf "%dh %dm %ds" $hours $minutes $seconds
    elif [[ $minutes -gt 0 ]]; then
        printf "%dm %ds" $minutes $seconds
    else
        printf "%ds" $seconds
    fi
}

# Check if timestamp is older than N hours
# Usage: is_expired "$timestamp" $hours
is_expired() {
    local timestamp="$1"
    local hours="${2:-24}"

    local now=$(get_unix_timestamp)
    local then

    # Try to parse ISO timestamp
    if date --version >/dev/null 2>&1; then
        # GNU date
        then=$(date -d "$timestamp" +%s 2>/dev/null || echo "0")
    else
        # BSD date (macOS)
        then=$(date -j -f "%Y-%m-%dT%H:%M:%SZ" "$timestamp" +%s 2>/dev/null || echo "0")
    fi

    local age_hours=$(( (now - then) / 3600 ))

    [[ $age_hours -ge $hours ]]
}

# Export functions
export -f get_iso_timestamp
export -f get_unix_timestamp
export -f get_log_timestamp
export -f elapsed_time
export -f is_expired
