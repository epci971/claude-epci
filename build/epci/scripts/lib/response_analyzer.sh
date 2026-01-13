#!/bin/bash
# =============================================================================
# Response Analyzer for Ralph Wiggum
# =============================================================================
# Analyzes Claude's output to detect completion, stuck loops, and work type.
# Supports dual-condition exit (completion indicators + explicit EXIT_SIGNAL).
# Adapted from frankbria/ralph-claude-code/lib/response_analyzer.sh
#
# EPCI Integration: v1.0
# =============================================================================

# Source utilities
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/date_utils.sh"

# Configuration
RA_COMPLETION_THRESHOLD="${RA_COMPLETION_THRESHOLD:-2}"
RA_RATE_LIMIT_PER_HOUR="${RA_RATE_LIMIT_PER_HOUR:-100}"
RA_SESSION_EXPIRY_HOURS="${RA_SESSION_EXPIRY_HOURS:-24}"

# State files
RA_ANALYSIS_FILE="${RA_ANALYSIS_FILE:-.response_analysis}"
RA_RATE_LIMIT_FILE="${RA_RATE_LIMIT_FILE:-.rate_limit_state}"

# =============================================================================
# RALPH_STATUS PARSING
# =============================================================================

# Parse RALPH_STATUS block from Claude output
# Returns JSON with parsed fields
parse_ralph_status() {
    local output="$1"

    # Extract block between ---RALPH_STATUS--- and ---END_RALPH_STATUS---
    local block=$(echo "$output" | sed -n '/---RALPH_STATUS---/,/---END_RALPH_STATUS---/p')

    if [[ -z "$block" ]]; then
        # No block found, return empty JSON
        echo '{"found": false}'
        return 1
    fi

    # Parse individual fields
    local status=$(echo "$block" | grep -E '^STATUS:' | sed 's/STATUS: *//' | tr -d '[:space:]')
    local tasks=$(echo "$block" | grep -E '^TASKS_COMPLETED_THIS_LOOP:' | sed 's/TASKS_COMPLETED_THIS_LOOP: *//' | tr -d '[:space:]')
    local files=$(echo "$block" | grep -E '^FILES_MODIFIED:' | sed 's/FILES_MODIFIED: *//' | tr -d '[:space:]')
    local tests=$(echo "$block" | grep -E '^TESTS_STATUS:' | sed 's/TESTS_STATUS: *//' | tr -d '[:space:]')
    local work_type=$(echo "$block" | grep -E '^WORK_TYPE:' | sed 's/WORK_TYPE: *//' | tr -d '[:space:]')
    local exit_signal=$(echo "$block" | grep -E '^EXIT_SIGNAL:' | sed 's/EXIT_SIGNAL: *//' | tr -d '[:space:]')
    local recommendation=$(echo "$block" | grep -E '^RECOMMENDATION:' | sed 's/RECOMMENDATION: *//')

    # Normalize exit_signal to boolean
    case "$exit_signal" in
        true|True|TRUE|1|yes|Yes|YES) exit_signal="true" ;;
        *) exit_signal="false" ;;
    esac

    # Validate status against allowed values
    case "$status" in
        IN_PROGRESS|COMPLETE|BLOCKED|UNKNOWN) ;;
        *) status="UNKNOWN" ;;
    esac

    # Validate tests_status against allowed values
    case "$tests" in
        PASSING|FAILING|NOT_RUN) ;;
        *) tests="NOT_RUN" ;;
    esac

    # Validate work_type against allowed values
    case "$work_type" in
        IMPLEMENTATION|TESTING|DOCUMENTATION|REFACTORING|UNKNOWN) ;;
        *) work_type="UNKNOWN" ;;
    esac

    # Sanitize numeric fields
    if ! [[ "$tasks" =~ ^[0-9]+$ ]]; then tasks=0; fi
    if ! [[ "$files" =~ ^[0-9]+$ ]]; then files=0; fi

    # Properly escape recommendation for JSON (security: prevent injection)
    # Escape backslashes, quotes, tabs, newlines, and control characters
    recommendation=$(echo "$recommendation" | \
        sed 's/\\/\\\\/g' | \
        sed 's/"/\\"/g' | \
        sed 's/\t/\\t/g' | \
        tr '\n' ' ' | \
        sed 's/[[:cntrl:]]//g')

    # Output JSON
    cat << EOF
{
    "found": true,
    "status": "${status}",
    "tasks_completed": ${tasks},
    "files_modified": ${files},
    "tests_status": "${tests}",
    "work_type": "${work_type}",
    "exit_signal": $exit_signal,
    "recommendation": "${recommendation}"
}
EOF
}

# =============================================================================
# COMPLETION DETECTION
# =============================================================================

# Completion indicator patterns
COMPLETION_PATTERNS=(
    "all tests pass"
    "all.*stories.*complete"
    "project.*complete"
    "implementation complete"
    "nothing.*left.*to.*do"
    "all tasks completed"
    "COMPLETE"
    "100%.*complete"
)

# Count completion indicators in output
count_completion_indicators() {
    local output="$1"
    local output_lower=$(echo "$output" | tr '[:upper:]' '[:lower:]')
    local count=0

    for pattern in "${COMPLETION_PATTERNS[@]}"; do
        if echo "$output_lower" | grep -qiE "$pattern"; then
            count=$((count + 1))
        fi
    done

    echo $count
}

# Check for explicit completion promise (hook mode)
check_completion_promise() {
    local output="$1"
    local promise="${2:-COMPLETE}"

    # Check <promise>X</promise> pattern
    if echo "$output" | grep -q "<promise>$promise</promise>"; then
        return 0
    fi

    return 1
}

# =============================================================================
# EXIT DECISION (DUAL-CONDITION)
# =============================================================================

# Determine if loop should exit
# Returns: "continue", "project_complete", "blocked", "max_iterations"
should_exit() {
    local output="$1"
    local iteration="$2"
    local max_iterations="${3:-50}"

    # Check iteration limit first
    if [[ $iteration -ge $max_iterations ]]; then
        echo "max_iterations"
        return 0
    fi

    # Parse RALPH_STATUS block
    local status_json=$(parse_ralph_status "$output")
    local block_found=$(echo "$status_json" | jq -r '.found')
    local exit_signal=$(echo "$status_json" | jq -r '.exit_signal')
    local status=$(echo "$status_json" | jq -r '.status')

    # Check for blocked status
    if [[ "$status" == "BLOCKED" ]]; then
        echo "blocked"
        return 0
    fi

    # Count completion indicators
    local indicators=$(count_completion_indicators "$output")

    # DUAL-CONDITION: Need BOTH indicators AND explicit exit_signal
    if [[ $indicators -ge $RA_COMPLETION_THRESHOLD ]]; then
        if [[ "$exit_signal" == "true" ]]; then
            echo "project_complete"
            return 0
        else
            # Indicators present but EXIT_SIGNAL is false
            # Claude explicitly says to continue - respect that
            echo "continue"
            return 0
        fi
    fi

    # Check explicit exit_signal alone (if block found)
    if [[ "$block_found" == "true" && "$exit_signal" == "true" ]]; then
        echo "project_complete"
        return 0
    fi

    # Check hook-mode completion promise
    if check_completion_promise "$output"; then
        echo "project_complete"
        return 0
    fi

    echo "continue"
}

# =============================================================================
# STUCK LOOP DETECTION
# =============================================================================

# Check if same error appears in multiple consecutive outputs
# Usage: detect_stuck_loop <current_output> [history_file]
detect_stuck_loop() {
    local current="$1"
    local history_file="${2:-.ralph_output_history}"

    # Extract error patterns from current output
    local current_errors=$(echo "$current" | grep -iE "error|failed|exception" | head -3 | md5sum | cut -d' ' -f1)

    if [[ ! -f "$history_file" ]]; then
        echo "$current_errors" > "$history_file"
        return 1  # Not stuck yet
    fi

    # Check if same error hash in last 3 entries
    local match_count=$(grep -c "$current_errors" "$history_file" 2>/dev/null || echo 0)

    # Append current to history (keep last 5)
    echo "$current_errors" >> "$history_file"
    tail -5 "$history_file" > "$history_file.tmp"
    mv "$history_file.tmp" "$history_file"

    [[ $match_count -ge 2 ]]
}

# =============================================================================
# RATE LIMITING
# =============================================================================

# Initialize or read rate limit state
init_rate_limit() {
    if [[ ! -f "$RA_RATE_LIMIT_FILE" ]]; then
        cat > "$RA_RATE_LIMIT_FILE" << EOF
{
    "hour_start": $(date +%s),
    "calls_this_hour": 0
}
EOF
    fi
}

# Check and update rate limit
# Returns: 0 if OK, 1 if rate limited
check_rate_limit() {
    init_rate_limit

    local now=$(date +%s)
    local hour_start=$(jq -r '.hour_start' "$RA_RATE_LIMIT_FILE")
    local calls=$(jq -r '.calls_this_hour' "$RA_RATE_LIMIT_FILE")

    # Check if new hour
    local elapsed=$((now - hour_start))
    if [[ $elapsed -ge 3600 ]]; then
        # Reset for new hour
        hour_start=$now
        calls=0
    fi

    # Check limit
    if [[ $calls -ge $RA_RATE_LIMIT_PER_HOUR ]]; then
        local remaining=$((3600 - elapsed))
        echo -e "\033[1;33m[Rate Limit] Limit reached ($RA_RATE_LIMIT_PER_HOUR/hour). Wait ${remaining}s\033[0m"
        return 1
    fi

    # Increment counter
    calls=$((calls + 1))
    cat > "$RA_RATE_LIMIT_FILE" << EOF
{
    "hour_start": $hour_start,
    "calls_this_hour": $calls
}
EOF

    return 0
}

# =============================================================================
# ANALYSIS OUTPUT
# =============================================================================

# Analyze response and write analysis file
analyze_response() {
    local output="$1"
    local iteration="$2"

    local status_json=$(parse_ralph_status "$output")
    local indicators=$(count_completion_indicators "$output")
    local exit_decision=$(should_exit "$output" "$iteration")
    local is_stuck=$(detect_stuck_loop "$output" && echo "true" || echo "false")

    # Write analysis
    cat > "$RA_ANALYSIS_FILE" << EOF
{
    "timestamp": "$(get_iso_timestamp)",
    "iteration": $iteration,
    "ralph_status": $status_json,
    "completion_indicators": $indicators,
    "exit_decision": "$exit_decision",
    "stuck_loop_detected": $is_stuck
}
EOF

    echo "$exit_decision"
}

# Export functions
export -f parse_ralph_status
export -f count_completion_indicators
export -f check_completion_promise
export -f should_exit
export -f detect_stuck_loop
export -f check_rate_limit
export -f analyze_response
