#!/bin/bash
# =============================================================================
# Circuit Breaker Component for Ralph Wiggum
# =============================================================================
# Prevents runaway token consumption by detecting stagnation.
# Based on Michael Nygard's "Release It!" pattern.
# Adapted from frankbria/ralph-claude-code/lib/circuit_breaker.sh
#
# EPCI Integration: v1.0
#
# States:
#   CLOSED    - Normal operation, progress detected
#   HALF_OPEN - Monitoring mode, checking for recovery
#   OPEN      - Failure detected, execution halted
# =============================================================================

# Source date utilities
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/date_utils.sh"

# Circuit Breaker States
CB_STATE_CLOSED="CLOSED"
CB_STATE_HALF_OPEN="HALF_OPEN"
CB_STATE_OPEN="OPEN"

# Circuit Breaker Configuration (configurable via environment)
CB_STATE_FILE="${CB_STATE_FILE:-.circuit_breaker_state}"
CB_HISTORY_FILE="${CB_HISTORY_FILE:-.circuit_breaker_history}"
CB_NO_PROGRESS_THRESHOLD="${CB_NO_PROGRESS_THRESHOLD:-3}"
CB_SAME_ERROR_THRESHOLD="${CB_SAME_ERROR_THRESHOLD:-5}"
CB_OUTPUT_DECLINE_THRESHOLD="${CB_OUTPUT_DECLINE_THRESHOLD:-70}"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# =============================================================================
# STATE MANAGEMENT
# =============================================================================

# Initialize circuit breaker state file
init_circuit_breaker() {
    if [[ -f "$CB_STATE_FILE" ]]; then
        # Validate JSON
        if ! jq '.' "$CB_STATE_FILE" > /dev/null 2>&1; then
            rm -f "$CB_STATE_FILE"
        fi
    fi

    if [[ ! -f "$CB_STATE_FILE" ]]; then
        # Use flock for atomic initialization
        (
            flock -x 200 || return 1
            cat > "$CB_STATE_FILE" << EOF
{
    "state": "$CB_STATE_CLOSED",
    "last_change": "$(get_iso_timestamp)",
    "consecutive_no_progress": 0,
    "consecutive_same_error": 0,
    "last_progress_loop": 0,
    "total_opens": 0,
    "reason": "",
    "current_loop": 0
}
EOF
        ) 200>"${CB_STATE_FILE}.lock"
    fi

    # Initialize history file
    if [[ ! -f "$CB_HISTORY_FILE" ]] || ! jq '.' "$CB_HISTORY_FILE" > /dev/null 2>&1; then
        echo '[]' > "$CB_HISTORY_FILE"
    fi
}

# Get current circuit breaker state
get_circuit_state() {
    if [[ ! -f "$CB_STATE_FILE" ]]; then
        echo "$CB_STATE_CLOSED"
        return
    fi
    jq -r '.state' "$CB_STATE_FILE" 2>/dev/null || echo "$CB_STATE_CLOSED"
}

# Check if execution is allowed
can_execute() {
    local state=$(get_circuit_state)
    [[ "$state" != "$CB_STATE_OPEN" ]]
}

# =============================================================================
# LOOP RESULT RECORDING
# =============================================================================

# Record loop execution result and update circuit breaker state
# Usage: record_loop_result <loop_number> <files_changed> <has_errors> <output_length>
record_loop_result() {
    local loop_number=$1
    local files_changed=${2:-0}
    local has_errors=${3:-false}
    local output_length=${4:-0}

    init_circuit_breaker

    # Read current state
    local state_data=$(cat "$CB_STATE_FILE")
    local current_state=$(echo "$state_data" | jq -r '.state')
    local consecutive_no_progress=$(echo "$state_data" | jq -r '.consecutive_no_progress // 0' | tr -d '[:space:]')
    local consecutive_same_error=$(echo "$state_data" | jq -r '.consecutive_same_error // 0' | tr -d '[:space:]')
    local last_progress_loop=$(echo "$state_data" | jq -r '.last_progress_loop // 0' | tr -d '[:space:]')
    local total_opens=$(echo "$state_data" | jq -r '.total_opens // 0' | tr -d '[:space:]')

    # Ensure integers
    consecutive_no_progress=$((consecutive_no_progress + 0))
    consecutive_same_error=$((consecutive_same_error + 0))
    last_progress_loop=$((last_progress_loop + 0))
    total_opens=$((total_opens + 0))

    # Detect progress
    local has_progress=false
    if [[ $files_changed -gt 0 ]]; then
        has_progress=true
        consecutive_no_progress=0
        last_progress_loop=$loop_number
    else
        consecutive_no_progress=$((consecutive_no_progress + 1))
    fi

    # Detect same error repetition
    if [[ "$has_errors" == "true" ]]; then
        consecutive_same_error=$((consecutive_same_error + 1))
    else
        consecutive_same_error=0
    fi

    # Determine new state
    local new_state="$current_state"
    local reason=""

    case $current_state in
        "$CB_STATE_CLOSED")
            if [[ $consecutive_no_progress -ge $CB_NO_PROGRESS_THRESHOLD ]]; then
                new_state="$CB_STATE_OPEN"
                reason="No progress in $consecutive_no_progress consecutive loops"
            elif [[ $consecutive_same_error -ge $CB_SAME_ERROR_THRESHOLD ]]; then
                new_state="$CB_STATE_OPEN"
                reason="Same error repeated $consecutive_same_error times"
            elif [[ $consecutive_no_progress -ge 2 ]]; then
                new_state="$CB_STATE_HALF_OPEN"
                reason="Monitoring: $consecutive_no_progress loops without progress"
            fi
            ;;
        "$CB_STATE_HALF_OPEN")
            if [[ "$has_progress" == "true" ]]; then
                new_state="$CB_STATE_CLOSED"
                reason="Progress detected, circuit recovered"
            elif [[ $consecutive_no_progress -ge $CB_NO_PROGRESS_THRESHOLD ]]; then
                new_state="$CB_STATE_OPEN"
                reason="No recovery after $consecutive_no_progress loops"
            fi
            ;;
        "$CB_STATE_OPEN")
            reason="Circuit breaker is open, execution halted"
            ;;
    esac

    # Update total opens counter
    if [[ "$new_state" == "$CB_STATE_OPEN" && "$current_state" != "$CB_STATE_OPEN" ]]; then
        total_opens=$((total_opens + 1))
    fi

    # Write updated state with file locking to prevent race conditions
    # Uses flock for atomic file operations (security: prevents state corruption)
    (
        flock -x 200 || {
            echo -e "${RED}[CB] Failed to acquire lock on state file${NC}" >&2
            return 1
        }
        cat > "$CB_STATE_FILE" << EOF
{
    "state": "$new_state",
    "last_change": "$(get_iso_timestamp)",
    "consecutive_no_progress": $consecutive_no_progress,
    "consecutive_same_error": $consecutive_same_error,
    "last_progress_loop": $last_progress_loop,
    "total_opens": $total_opens,
    "reason": "$reason",
    "current_loop": $loop_number
}
EOF
    ) 200>"${CB_STATE_FILE}.lock"

    # Log state transition
    if [[ "$new_state" != "$current_state" ]]; then
        log_circuit_transition "$current_state" "$new_state" "$reason" "$loop_number"
    fi

    # Return exit code based on state
    [[ "$new_state" != "$CB_STATE_OPEN" ]]
}

# =============================================================================
# LOGGING
# =============================================================================

log_circuit_transition() {
    local from_state=$1
    local to_state=$2
    local reason=$3
    local loop_number=$4

    # Append to history
    local transition=$(cat << EOF
{
    "timestamp": "$(get_iso_timestamp)",
    "loop": $loop_number,
    "from_state": "$from_state",
    "to_state": "$to_state",
    "reason": "$reason"
}
EOF
)
    local history=$(cat "$CB_HISTORY_FILE")
    echo "$history" | jq ". += [$transition]" > "$CB_HISTORY_FILE"

    # Console output
    case $to_state in
        "$CB_STATE_OPEN")
            echo -e "${RED}[CB] CIRCUIT BREAKER OPENED${NC}"
            echo -e "${RED}[CB] Reason: $reason${NC}"
            ;;
        "$CB_STATE_HALF_OPEN")
            echo -e "${YELLOW}[CB] CIRCUIT BREAKER: Monitoring Mode${NC}"
            echo -e "${YELLOW}[CB] Reason: $reason${NC}"
            ;;
        "$CB_STATE_CLOSED")
            echo -e "${GREEN}[CB] CIRCUIT BREAKER: Normal Operation${NC}"
            echo -e "${GREEN}[CB] Reason: $reason${NC}"
            ;;
    esac
}

# =============================================================================
# STATUS DISPLAY
# =============================================================================

show_circuit_status() {
    init_circuit_breaker

    local state=$(jq -r '.state' "$CB_STATE_FILE")
    local reason=$(jq -r '.reason' "$CB_STATE_FILE")
    local no_progress=$(jq -r '.consecutive_no_progress' "$CB_STATE_FILE")
    local current_loop=$(jq -r '.current_loop' "$CB_STATE_FILE")
    local total_opens=$(jq -r '.total_opens' "$CB_STATE_FILE")

    local color=""
    local icon=""
    case $state in
        "$CB_STATE_CLOSED") color=$GREEN; icon="✅" ;;
        "$CB_STATE_HALF_OPEN") color=$YELLOW; icon="⚠️" ;;
        "$CB_STATE_OPEN") color=$RED; icon="🚨" ;;
    esac

    echo -e "${color}╔════════════════════════════════════════╗${NC}"
    echo -e "${color}║     Circuit Breaker Status             ║${NC}"
    echo -e "${color}╚════════════════════════════════════════╝${NC}"
    echo -e "${color}State:${NC}              $icon $state"
    echo -e "${color}Reason:${NC}             $reason"
    echo -e "${color}Loops w/o progress:${NC} $no_progress"
    echo -e "${color}Current loop:${NC}       #$current_loop"
    echo -e "${color}Total opens:${NC}        $total_opens"
}

# =============================================================================
# RESET
# =============================================================================

reset_circuit_breaker() {
    local reason=${1:-"Manual reset"}

    cat > "$CB_STATE_FILE" << EOF
{
    "state": "$CB_STATE_CLOSED",
    "last_change": "$(get_iso_timestamp)",
    "consecutive_no_progress": 0,
    "consecutive_same_error": 0,
    "last_progress_loop": 0,
    "total_opens": 0,
    "reason": "$reason"
}
EOF

    echo -e "${GREEN}[CB] Circuit breaker reset to CLOSED state${NC}"
}

# Check if execution should halt
should_halt_execution() {
    local state=$(get_circuit_state)

    if [[ "$state" == "$CB_STATE_OPEN" ]]; then
        show_circuit_status
        echo ""
        echo -e "${RED}EXECUTION HALTED: Circuit Breaker Opened${NC}"
        echo ""
        echo -e "${YELLOW}To continue:${NC}"
        echo "  1. Review recent logs"
        echo "  2. Fix the blocking issue"
        echo "  3. Reset: /ralph --reset-circuit"
        return 0  # Signal to halt
    fi
    return 1  # Can continue
}

# Export functions
export -f init_circuit_breaker
export -f get_circuit_state
export -f can_execute
export -f record_loop_result
export -f show_circuit_status
export -f reset_circuit_breaker
export -f should_halt_execution
