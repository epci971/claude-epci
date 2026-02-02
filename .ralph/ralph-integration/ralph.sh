#!/bin/bash
# Ralph Runner — Ralph Integration v6.1
# Generated: 2026-02-02
#
# Usage:
#   ./ralph.sh              # Verbose output (default)
#   ./ralph.sh --quiet      # Minimal output
#   ./ralph.sh --dry-run    # Show tasks without executing
#   ./ralph.sh --help       # Show help
#
# To stop: Ctrl+C

set -e

# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════

FEATURE_SLUG="ralph-integration"
SPEC_DIR="docs/specs/${FEATURE_SLUG}"
RALPH_DIR=".ralph/${FEATURE_SLUG}"
PRD_FILE="${SPEC_DIR}/${FEATURE_SLUG}.prd.json"
PROGRESS_FILE="${RALPH_DIR}/progress.txt"

MAX_ITERATIONS=${MAX_ITERATIONS:-50}
NO_PROGRESS_THRESHOLD=3
SAME_ERROR_THRESHOLD=3

# CLI flags
VERBOSE=${VERBOSE:-true}
DRY_RUN=false

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

# ═══════════════════════════════════════════════════════════════════════════════
# CIRCUIT BREAKER (inline)
# ═══════════════════════════════════════════════════════════════════════════════

declare -a FILE_HASHES=()
declare -a ERROR_HASHES=()
NO_PROGRESS_COUNT=0

check_circuit_breaker() {
    local current_hash=$1
    local error_hash=$2

    # Check no-progress (same state hash N times)
    if [[ ${#FILE_HASHES[@]} -gt 0 && "${FILE_HASHES[-1]}" == "$current_hash" ]]; then
        ((NO_PROGRESS_COUNT++))
        if [[ $NO_PROGRESS_COUNT -ge $NO_PROGRESS_THRESHOLD ]]; then
            echo -e "${RED}⚠️ Circuit breaker: No progress for $NO_PROGRESS_COUNT iterations${NC}"
            echo "[$(date -Iseconds)] CIRCUIT_BREAKER: No progress after $NO_PROGRESS_COUNT iterations" >> "$PROGRESS_FILE"
            return 1
        fi
    else
        NO_PROGRESS_COUNT=0
    fi
    FILE_HASHES+=("$current_hash")

    # Check same error repeated
    if [[ -n "$error_hash" && "$error_hash" != "d41d8cd98f00b204e9800998ecf8427e" ]]; then
        local same_error_count=0
        for h in "${ERROR_HASHES[@]: -$SAME_ERROR_THRESHOLD}"; do
            [[ "$h" == "$error_hash" ]] && ((same_error_count++))
        done
        if [[ $same_error_count -ge $SAME_ERROR_THRESHOLD ]]; then
            echo -e "${RED}⚠️ Circuit breaker: Same error $same_error_count times${NC}"
            echo "[$(date -Iseconds)] CIRCUIT_BREAKER: Same error repeated $same_error_count times" >> "$PROGRESS_FILE"
            return 1
        fi
        ERROR_HASHES+=("$error_hash")
    fi

    return 0
}

# ═══════════════════════════════════════════════════════════════════════════════
# RALPH_STATUS PARSER
# ═══════════════════════════════════════════════════════════════════════════════

parse_ralph_status() {
    local output="$1"

    # Extract RALPH_STATUS block
    local status_block
    status_block=$(echo "$output" | sed -n '/---RALPH_STATUS---/,/---END_RALPH_STATUS---/p')

    if [[ -z "$status_block" ]]; then
        echo "NO_STATUS"
        return 1
    fi

    # Parse fields
    local STATUS EXIT_SIGNAL
    STATUS=$(echo "$status_block" | grep "^STATUS:" | cut -d: -f2 | tr -d ' ')
    EXIT_SIGNAL=$(echo "$status_block" | grep "^EXIT_SIGNAL:" | cut -d: -f2 | tr -d ' ')

    # Dual-condition logic
    if [[ "$EXIT_SIGNAL" == "true" ]]; then
        echo "EXIT"
        return 0
    elif [[ "$STATUS" == "COMPLETE" ]]; then
        echo "COMPLETE"
        return 0
    elif [[ "$STATUS" == "BLOCKED" ]]; then
        echo "BLOCKED"
        return 2
    else
        echo "CONTINUE"
        return 3
    fi
}

# ═══════════════════════════════════════════════════════════════════════════════
# HELPERS
# ═══════════════════════════════════════════════════════════════════════════════

show_help() {
    cat << EOF
Ralph Wiggum — Autonomous Executor
Feature: ${FEATURE_SLUG}

Usage: ./ralph.sh [OPTIONS]

Options:
    -q, --quiet      Disable verbose output
    --dry-run        Show pending tasks without executing
    -h, --help       Show this help

Environment:
    MAX_ITERATIONS   Maximum loop iterations (default: 50)

Examples:
    ./ralph.sh                    # Normal execution
    ./ralph.sh --dry-run          # Preview tasks
    MAX_ITERATIONS=10 ./ralph.sh  # Limit iterations
EOF
}

show_progress_bar() {
    local completed=$1 total=$2 width=40
    [[ $total -eq 0 ]] && return
    local percent=$((completed * 100 / total))
    local filled=$((completed * width / total))
    printf "[%-${width}s] %d%% (%d/%d)\n" "$(printf '#%.0s' $(seq 1 $filled 2>/dev/null))" "$percent" "$completed" "$total"
}

# Time tracking
START_TIME=$(date +%s)
get_elapsed() {
    local elapsed=$(($(date +%s) - START_TIME))
    printf "%02d:%02d:%02d" $((elapsed/3600)) $((elapsed%3600/60)) $((elapsed%60))
}

# ═══════════════════════════════════════════════════════════════════════════════
# ARGUMENT PARSING
# ═══════════════════════════════════════════════════════════════════════════════

while [[ $# -gt 0 ]]; do
    case $1 in
        -q|--quiet) VERBOSE=false; shift ;;
        --dry-run) DRY_RUN=true; shift ;;
        -h|--help) show_help; exit 0 ;;
        *) echo "Unknown option: $1"; exit 1 ;;
    esac
done

# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════

echo "════════════════════════════════════════════════════════════════"
echo "  Ralph Wiggum — Autonomous Executor"
[[ "$VERBOSE" == "true" ]] && echo -e "         ${CYAN}[VERBOSE MODE]${NC}"
echo "════════════════════════════════════════════════════════════════"
echo "Feature: ${FEATURE_SLUG}"
echo "PRD: ${PRD_FILE}"
echo "Max iterations: ${MAX_ITERATIONS}"
echo ""

# Validation
if [[ ! -f "$PRD_FILE" ]]; then
    echo -e "${RED}Error: PRD file not found: ${PRD_FILE}${NC}"
    exit 1
fi

if [[ ! -d "$SPEC_DIR" ]]; then
    echo -e "${RED}Error: Spec directory not found: ${SPEC_DIR}${NC}"
    exit 1
fi

# Dry run mode
if [[ "$DRY_RUN" == "true" ]]; then
    echo -e "${CYAN}=== DRY RUN ===${NC}"
    echo "Pending tasks:"
    jq -r '.tasks[] | select(.dependencies | length == 0 or all(. as $dep | .tasks[] | select(.id == $dep) | .status == "completed")) | "  - \(.id): \(.title)"' "$PRD_FILE" 2>/dev/null || echo "  (unable to parse PRD)"
    exit 0
fi

# Initialize progress log
echo "[$(date -Iseconds)] Ralph started for ${FEATURE_SLUG}" >> "$PROGRESS_FILE"

# ═══════════════════════════════════════════════════════════════════════════════
# MAIN LOOP
# ═══════════════════════════════════════════════════════════════════════════════

for ((i=1; i<=MAX_ITERATIONS; i++)); do
    # Check pending tasks (simplified - actual logic would parse PRD properly)
    PENDING=$(jq '[.tasks[] | select(.status != "completed")] | length' "$PRD_FILE" 2>/dev/null || echo "0")
    COMPLETED=$(jq '[.tasks[] | select(.status == "completed")] | length' "$PRD_FILE" 2>/dev/null || echo "0")
    TOTAL=$(jq '.tasks | length' "$PRD_FILE" 2>/dev/null || echo "8")

    if [[ "$PENDING" -eq 0 ]]; then
        echo -e "${GREEN}✅ All tasks complete!${NC}"
        echo "[$(date -Iseconds)] COMPLETE: All tasks finished" >> "$PROGRESS_FILE"
        exit 0
    fi

    if [[ "$VERBOSE" == "true" ]]; then
        echo ""
        echo -e "${BLUE}╔════════════════════════════════════════════════════════════════╗${NC}"
        echo -e "${BLUE}║        Iteration $i of $MAX_ITERATIONS                                      ║${NC}"
        echo -e "${BLUE}╚════════════════════════════════════════════════════════════════╝${NC}"
        echo -e "${YELLOW}Elapsed:${NC} $(get_elapsed)"
        show_progress_bar "$COMPLETED" "$TOTAL"
    else
        echo -e "\n${YELLOW}=== Iteration $i ===${NC}"
        echo "Progress: $COMPLETED/$TOTAL"
    fi

    # Execute /ralph-exec
    echo -e "\n${CYAN}Executing /ralph-exec...${NC}"
    OUTPUT_FILE=$(mktemp)

    # Capture output (use tee for real-time display in verbose mode)
    if [[ "$VERBOSE" == "true" ]]; then
        claude --dangerously-skip-permissions "/ralph-exec --prd $PRD_FILE" 2>&1 | tee "$OUTPUT_FILE" || true
    else
        claude --dangerously-skip-permissions "/ralph-exec --prd $PRD_FILE" > "$OUTPUT_FILE" 2>&1 || true
    fi

    OUTPUT=$(cat "$OUTPUT_FILE")

    # Calculate hashes for circuit breaker
    CURRENT_HASH=$(git diff --stat 2>/dev/null | md5sum | cut -d' ' -f1)
    ERROR_HASH=$(echo "$OUTPUT" | grep -i "error\|failed\|exception" | md5sum | cut -d' ' -f1)

    # Check circuit breaker
    if ! check_circuit_breaker "$CURRENT_HASH" "$ERROR_HASH"; then
        echo -e "${RED}🛑 Stopping due to circuit breaker${NC}"
        rm -f "$OUTPUT_FILE"
        exit 2
    fi

    # Parse RALPH_STATUS
    DECISION=$(parse_ralph_status "$OUTPUT")
    EXIT_CODE=$?

    case "$DECISION" in
        EXIT|COMPLETE)
            echo -e "${GREEN}✅ Execution complete!${NC}"
            echo "[$(date -Iseconds)] COMPLETE: Exit signal received" >> "$PROGRESS_FILE"
            rm -f "$OUTPUT_FILE"
            exit 0
            ;;
        BLOCKED)
            echo -e "${RED}🚫 Blocked — manual intervention required${NC}"
            echo "[$(date -Iseconds)] BLOCKED: Manual intervention needed" >> "$PROGRESS_FILE"
            rm -f "$OUTPUT_FILE"
            exit 2
            ;;
        NO_STATUS)
            echo -e "${YELLOW}⚠️ No RALPH_STATUS block found, continuing...${NC}"
            ;;
        CONTINUE)
            echo -e "${CYAN}➡️ Continuing to next iteration...${NC}"
            ;;
    esac

    rm -f "$OUTPUT_FILE"
    echo "[$(date -Iseconds)] Iteration $i completed, decision: $DECISION" >> "$PROGRESS_FILE"

    # Brief pause between iterations
    sleep 2
done

echo -e "${RED}⚠️ Max iterations ($MAX_ITERATIONS) reached${NC}"
echo "[$(date -Iseconds)] MAX_ITERATIONS reached" >> "$PROGRESS_FILE"
exit 1
