#!/usr/bin/env bash
# ralph.sh — Ralph Wiggum Autonomous Executor
# Feature: OpenClaw Notion Task Runner
# Generated: 2026-02-13
#
# Usage:
#   ./ralph.sh                              # Verbose output (default)
#   ./ralph.sh --quiet                      # Minimal output
#   ./ralph.sh --dry-run                    # Show pending stories without executing
#   ./ralph.sh --help                       # Show help
#
# Exit codes:
#   0 = success (all stories completed)
#   1 = max iterations reached
#   2 = circuit breaker triggered
#   3 = blocked (dependency issue)
#
# Dependencies: bash 4+, jq, md5sum or md5, git

set -euo pipefail

# Cleanup trap for temp files on interruption
OUTPUT_FILE=""
cleanup() {
    [[ -n "$OUTPUT_FILE" && -f "$OUTPUT_FILE" ]] && rm -f "$OUTPUT_FILE" 2>/dev/null || true
}
trap cleanup EXIT INT TERM

# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════

FEATURE_SLUG="notion-runner"
SPEC_DIR="docs/specs/notion-runner"
RALPH_DIR=".ralph/notion-runner"
PRD_FILE="docs/specs/notion-runner/notion-runner.prd.json"
PROGRESS_FILE="${RALPH_DIR}/progress.txt"

MAX_ITERATIONS=${MAX_ITERATIONS:-50}

# Circuit breaker configuration
CB_THRESHOLD=${CB_THRESHOLD:-3}

# CLI flags (defaults)
VERBOSE=true
DRY_RUN=false
DANGEROUSLY_SKIP_PERMISSIONS=false

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m'

# Time tracking
START_TIME=$(date +%s)

# ═══════════════════════════════════════════════════════════════════════════════
# CIRCUIT BREAKER (inline)
# ═══════════════════════════════════════════════════════════════════════════════

declare -a FILE_HASHES
declare -a ERROR_HASHES
CURRENT_ITERATION=0

calculate_file_hash() {
    local diff_output hash
    if git rev-parse --git-dir &>/dev/null; then
        diff_output=$(git diff 2>/dev/null || echo "")
        [[ -z "$diff_output" ]] && diff_output=$(git diff --cached 2>/dev/null || echo "")
    else
        diff_output=$(find . -type f -newer /tmp/cb_marker 2>/dev/null || echo "")
    fi
    [[ -z "$diff_output" ]] && { echo "empty_state"; return; }
    if command -v md5sum &>/dev/null; then
        hash=$(echo "$diff_output" | md5sum | cut -d' ' -f1)
    elif command -v md5 &>/dev/null; then
        hash=$(echo "$diff_output" | md5)
    else
        hash=$(echo "$diff_output" | cksum | cut -d' ' -f1)
    fi
    echo "$hash"
}

calculate_error_hash() {
    local error_msg="${1:-}" hash
    [[ -z "$error_msg" ]] && { echo "no_error"; return; }
    local normalized
    normalized=$(echo "$error_msg" | sed -E 's/[0-9]{2}:[0-9]{2}:[0-9]{2}//g' | sed -E 's/line [0-9]+/line N/g')
    if command -v md5sum &>/dev/null; then
        hash=$(echo "$normalized" | md5sum | cut -d' ' -f1)
    elif command -v md5 &>/dev/null; then
        hash=$(echo "$normalized" | md5)
    else
        hash=$(echo "$normalized" | cksum | cut -d' ' -f1)
    fi
    echo "$hash"
}

_cb_log() {
    local reason="$1" details="${2:-}" timestamp
    timestamp=$(date -Iseconds 2>/dev/null || date '+%Y-%m-%dT%H:%M:%S')
    local log_entry="[$timestamp] CIRCUIT BREAKER: $reason at iteration $CURRENT_ITERATION"
    [[ -n "$details" ]] && log_entry="$log_entry - $details"
    local log_dir; log_dir=$(dirname "$PROGRESS_FILE")
    [[ "$log_dir" != "." ]] && mkdir -p "$log_dir" 2>/dev/null || true
    echo "$log_entry" >> "$PROGRESS_FILE"
    echo "$log_entry" >&2
}

_count_consecutive_same() {
    local arr_name=$1 len
    eval "len=\${#${arr_name}[@]}"
    [[ $len -eq 0 ]] && { echo "0"; return; }
    [[ $len -eq 1 ]] && { echo "1"; return; }
    local last; eval "last=\${${arr_name}[$((len - 1))]}"
    local count=1
    for ((i = len - 2; i >= 0; i--)); do
        local current; eval "current=\${${arr_name}[$i]}"
        [[ "$current" == "$last" ]] && count=$((count + 1)) || break
    done
    echo "$count"
}

check_circuit_breaker() {
    local file_consecutive error_consecutive
    file_consecutive=$(_count_consecutive_same FILE_HASHES)
    if [[ $file_consecutive -ge $CB_THRESHOLD ]]; then
        _cb_log "no progress" "same file state for $file_consecutive consecutive iterations"
        return 1
    fi
    error_consecutive=$(_count_consecutive_same ERROR_HASHES)
    if [[ $error_consecutive -ge $CB_THRESHOLD ]]; then
        _cb_log "repeated error" "same error for $error_consecutive consecutive iterations"
        return 1
    fi
    return 0
}

record_and_check() {
    local last_error="${1:-}"
    local file_hash; file_hash=$(calculate_file_hash)
    FILE_HASHES+=("$file_hash")
    local error_hash; error_hash=$(calculate_error_hash "$last_error")
    ERROR_HASHES+=("$error_hash")
    check_circuit_breaker
}

reset_circuit_breaker() {
    FILE_HASHES=()
    ERROR_HASHES=()
    CURRENT_ITERATION=0
    touch /tmp/cb_marker 2>/dev/null || true
}

# ═══════════════════════════════════════════════════════════════════════════════
# RALPH_STATUS PARSER
# ═══════════════════════════════════════════════════════════════════════════════

extract_ralph_status() {
    local output="$1"
    echo "$output" | sed -n '/<<<RALPH_STATUS>>>/,/<<<END_RALPH_STATUS>>>/p' | grep -v '<<<'
}

get_field() {
    local content="$1" field="$2"
    echo "$content" | grep "^${field}:" | cut -d':' -f2- | xargs
}

parse_ralph_status() {
    local output="$1"
    local status_block; status_block=$(extract_ralph_status "$output")
    [[ -z "$status_block" ]] && { echo "NO_STATUS"; return 3; }
    local status next_story
    status=$(get_field "$status_block" "status")
    next_story=$(get_field "$status_block" "next_story")
    case "$status" in
        SUCCESS)
            [[ "$next_story" != "null" && -n "$next_story" ]] && { echo "CONTINUE"; return 0; } || { echo "EXIT"; return 1; }
            ;;
        FAILURE) echo "CONTINUE"; return 0 ;;
        ALL_DONE) echo "EXIT"; return 1 ;;
        BLOCKED) echo "BLOCKED"; return 2 ;;
        *) echo "CONTINUE"; return 0 ;;
    esac
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
    -q, --quiet                     Disable verbose output
    --dry-run                       Show pending stories without executing
    --dangerously-skip-permissions  Run claude in autonomous mode (required)
    -h, --help                      Show this help

Environment:
    MAX_ITERATIONS   Maximum loop iterations (default: 50)
    CB_THRESHOLD     Circuit breaker threshold (default: 3)

Exit Codes:
    0   All stories completed successfully
    1   Max iterations reached
    2   Circuit breaker triggered
    3   Blocked (dependency issue)
EOF
}

show_progress_bar() {
    local completed=$1 total=$2 width=40
    [[ $total -eq 0 ]] && return
    local percent=$((completed * 100 / total))
    local filled=$((completed * width / total))
    local bar=""
    for ((j=0; j<filled; j++)); do bar+="█"; done
    for ((j=filled; j<width; j++)); do bar+="░"; done
    printf "[%s] %d%% (%d/%d)\n" "$bar" "$percent" "$completed" "$total"
}

get_elapsed() {
    local elapsed=$(($(date +%s) - START_TIME))
    printf "%02d:%02d:%02d" $((elapsed/3600)) $((elapsed%3600/60)) $((elapsed%60))
}

log_progress() {
    local message="$1" timestamp
    timestamp=$(date -Iseconds 2>/dev/null || date '+%Y-%m-%dT%H:%M:%S')
    local log_dir; log_dir=$(dirname "$PROGRESS_FILE")
    [[ "$log_dir" != "." ]] && mkdir -p "$log_dir" 2>/dev/null || true
    echo "[$timestamp] $message" >> "$PROGRESS_FILE"
}

validate_prd() {
    local prd_file="$1"
    if [[ ! -f "$prd_file" ]]; then
        echo -e "${RED}Error: PRD file not found: ${prd_file}${NC}" >&2
        return 1
    fi
    if ! jq empty "$prd_file" 2>/dev/null; then
        echo -e "${RED}Error: PRD file is not valid JSON: ${prd_file}${NC}" >&2
        return 1
    fi
    if ! jq -e '.userStories // .tasks' "$prd_file" &>/dev/null; then
        echo -e "${RED}Error: PRD file missing userStories/tasks array: ${prd_file}${NC}" >&2
        return 1
    fi
    return 0
}

get_story_counts() {
    local prd_file="$1"
    local stories_key
    stories_key=$(jq -r 'if .userStories then "userStories" else "tasks" end' "$prd_file" 2>/dev/null)
    local pending completed total
    pending=$(jq "[.${stories_key}[] | select(.status == \"pending\" or .status == \"in_progress\" or .status == null)] | length" "$prd_file" 2>/dev/null || echo "0")
    completed=$(jq "[.${stories_key}[] | select(.status == \"completed\")] | length" "$prd_file" 2>/dev/null || echo "0")
    total=$(jq ".${stories_key} | length" "$prd_file" 2>/dev/null || echo "0")
    echo "$pending $completed $total"
}

get_current_story() {
    local prd_file="$1"
    local stories_key
    stories_key=$(jq -r 'if .userStories then "userStories" else "tasks" end' "$prd_file" 2>/dev/null)
    jq -r ".${stories_key}[] | select(.status == \"pending\" or .status == null) | .id" "$prd_file" 2>/dev/null | head -1
}

# ═══════════════════════════════════════════════════════════════════════════════
# ARGUMENT PARSING
# ═══════════════════════════════════════════════════════════════════════════════

while [[ $# -gt 0 ]]; do
    case $1 in
        -q|--quiet) VERBOSE=false; shift ;;
        --dry-run) DRY_RUN=true; shift ;;
        --dangerously-skip-permissions) DANGEROUSLY_SKIP_PERMISSIONS=true; shift ;;
        -h|--help) show_help; exit 0 ;;
        *) echo -e "${RED}Unknown option: $1${NC}" >&2; echo "Use --help for usage information" >&2; exit 1 ;;
    esac
done

if [[ "$DRY_RUN" == "false" && "$DANGEROUSLY_SKIP_PERMISSIONS" == "false" ]]; then
    echo -e "${RED}Error: --dangerously-skip-permissions is required for autonomous execution${NC}" >&2
    echo "Use --dry-run to preview stories without executing." >&2
    exit 1
fi

# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════

echo "════════════════════════════════════════════════════════════════"
echo -e "  ${BOLD}Ralph Wiggum — Autonomous Executor${NC}"
[[ "$VERBOSE" == "true" ]] && echo -e "  ${CYAN}[VERBOSE MODE]${NC}"
[[ "$DRY_RUN" == "true" ]] && echo -e "  ${YELLOW}[DRY RUN MODE]${NC}"
echo "════════════════════════════════════════════════════════════════"
echo "Feature: ${FEATURE_SLUG}"
echo "PRD: ${PRD_FILE}"
echo "Max iterations: ${MAX_ITERATIONS}"
echo "Circuit breaker threshold: ${CB_THRESHOLD}"
echo ""

if ! validate_prd "$PRD_FILE"; then
    exit 1
fi

if [[ "$DRY_RUN" == "true" ]]; then
    echo -e "${CYAN}=== DRY RUN ===${NC}"
    echo "Pending stories:"
    local_key=$(jq -r 'if .userStories then "userStories" else "tasks" end' "$PRD_FILE" 2>/dev/null)
    jq -r ".${local_key}[] | select(.status == \"pending\" or .status == null) | \"  - \(.id): \(.title) [deps: \(.dependencies // [] | if type == \"array\" then join(\", \") else . end)]\"" "$PRD_FILE" 2>/dev/null || echo "  (unable to parse PRD)"
    read -r pending completed total <<< "$(get_story_counts "$PRD_FILE")"
    echo ""
    echo "Summary: $pending pending, $completed completed, $total total"
    exit 0
fi

log_progress "Ralph started for ${FEATURE_SLUG}"
log_progress "PRD: ${PRD_FILE}, Max iterations: ${MAX_ITERATIONS}"
reset_circuit_breaker

# ═══════════════════════════════════════════════════════════════════════════════
# MAIN LOOP
# ═══════════════════════════════════════════════════════════════════════════════

for ((i=1; i<=MAX_ITERATIONS; i++)); do
    CURRENT_ITERATION=$i
    read -r pending completed total <<< "$(get_story_counts "$PRD_FILE")"

    if [[ "$pending" -eq 0 ]]; then
        echo -e "${GREEN}All stories completed!${NC}"
        log_progress "COMPLETE: All $total stories finished"
        exit 0
    fi

    current_story=$(get_current_story "$PRD_FILE")

    if [[ "$VERBOSE" == "true" ]]; then
        echo ""
        echo -e "${BLUE}══════════════════════════════════════════════════════════════════${NC}"
        printf "  Iteration %-3d of %-3d\n" "$i" "$MAX_ITERATIONS"
        echo -e "${BLUE}══════════════════════════════════════════════════════════════════${NC}"
        echo -e "${YELLOW}Elapsed:${NC} $(get_elapsed)"
        echo -e "${YELLOW}Current story:${NC} ${current_story:-"(determining...)"}"
        show_progress_bar "$completed" "$total"
    else
        echo -e "\n${YELLOW}=== Iteration $i ===${NC}"
        echo "Progress: $completed/$total | Story: ${current_story:-"?"}"
    fi

    echo -e "\n${CYAN}Executing /ralph-exec...${NC}"
    OUTPUT_FILE=$(mktemp)
    LAST_ERROR=""

    if [[ "$VERBOSE" == "true" ]]; then
        if claude --dangerously-skip-permissions "/ralph-exec --prd $PRD_FILE" 2>&1 | tee "$OUTPUT_FILE"; then
            :
        else
            LAST_ERROR=$(tail -20 "$OUTPUT_FILE" | grep -i "error\|failed\|exception" || echo "")
        fi
    else
        if claude --dangerously-skip-permissions "/ralph-exec --prd $PRD_FILE" > "$OUTPUT_FILE" 2>&1; then
            :
        else
            LAST_ERROR=$(tail -20 "$OUTPUT_FILE" | grep -i "error\|failed\|exception" || echo "")
        fi
    fi

    OUTPUT=$(cat "$OUTPUT_FILE")

    if ! record_and_check "$LAST_ERROR"; then
        echo -e "${RED}Circuit breaker triggered!${NC}"
        echo -e "${RED}   Stopping due to repeated failures or no progress.${NC}"
        rm -f "$OUTPUT_FILE"
        exit 2
    fi

    DECISION=$(parse_ralph_status "$OUTPUT")
    PARSE_EXIT_CODE=$?

    case "$DECISION" in
        EXIT)
            echo -e "${GREEN}Execution complete!${NC}"
            log_progress "COMPLETE: Exit signal received after iteration $i"
            rm -f "$OUTPUT_FILE"
            exit 0
            ;;
        BLOCKED)
            echo -e "${RED}Blocked — manual intervention required${NC}"
            blocked_status_block=$(extract_ralph_status "$OUTPUT")
            blocked_error_msg=$(get_field "$blocked_status_block" "error")
            [[ -n "$blocked_error_msg" && "$blocked_error_msg" != "null" ]] && echo -e "${RED}   Reason: $blocked_error_msg${NC}"
            log_progress "BLOCKED: Manual intervention needed - $blocked_error_msg"
            rm -f "$OUTPUT_FILE"
            exit 3
            ;;
        NO_STATUS)
            echo -e "${YELLOW}No RALPH_STATUS block found, continuing...${NC}"
            log_progress "WARNING: No RALPH_STATUS in iteration $i output"
            ;;
        CONTINUE)
            echo -e "${CYAN}Continuing to next iteration...${NC}"
            ;;
    esac

    rm -f "$OUTPUT_FILE"
    log_progress "Iteration $i completed, decision: $DECISION, story: ${current_story:-unknown}"
    sleep 2
done

echo -e "${RED}Max iterations ($MAX_ITERATIONS) reached${NC}"
log_progress "MAX_ITERATIONS reached after $MAX_ITERATIONS iterations"
exit 1
