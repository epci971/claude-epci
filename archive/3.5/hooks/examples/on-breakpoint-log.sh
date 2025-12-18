#!/bin/bash
# =============================================================================
# Hook: on-breakpoint-log.sh
# Description: Log breakpoint events for debugging and metrics
# Type: on-breakpoint
#
# Usage:
#   1. Copy or symlink this file to hooks/active/
#   2. Make it executable: chmod +x on-breakpoint-log.sh
#
# Output:
#   Logs are written to ./epci-breakpoints.log
# =============================================================================

# Configuration
LOG_FILE="${EPCI_LOG_FILE:-epci-breakpoints.log}"

# Read context from stdin
CONTEXT=$(cat)

# Extract key fields using simple parsing (no jq dependency)
PHASE=$(echo "$CONTEXT" | grep -o '"phase"[[:space:]]*:[[:space:]]*"[^"]*"' | cut -d'"' -f4)
FEATURE=$(echo "$CONTEXT" | grep -o '"feature_slug"[[:space:]]*:[[:space:]]*"[^"]*"' | cut -d'"' -f4)
HOOK_TYPE=$(echo "$CONTEXT" | grep -o '"hook_type"[[:space:]]*:[[:space:]]*"[^"]*"' | cut -d'"' -f4)
BP_TYPE=$(echo "$CONTEXT" | grep -o '"breakpoint_type"[[:space:]]*:[[:space:]]*"[^"]*"' | cut -d'"' -f4)
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

# Build log entry
LOG_ENTRY="[${TIMESTAMP}] BREAKPOINT | phase=${PHASE:-unknown} | feature=${FEATURE:-unknown} | hook=${HOOK_TYPE:-on-breakpoint} | bp_type=${BP_TYPE:-unknown}"

# Write to log file
echo "$LOG_ENTRY" >> "$LOG_FILE"

# Also write full context for debugging (optional, can be removed)
echo "--- Full Context ---" >> "$LOG_FILE"
echo "$CONTEXT" >> "$LOG_FILE"
echo "-------------------" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"

# Return success
echo '{"status": "success", "message": "Breakpoint logged to '"$LOG_FILE"'"}'
