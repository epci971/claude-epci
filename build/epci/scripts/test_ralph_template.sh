#!/usr/bin/env bash
# test_ralph_template.sh - Tests for ralph.sh.template
# Tests: placeholder substitution, CLI flags, RALPH_STATUS parsing, circuit breaker integration

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Test counters
TESTS_RUN=0
TESTS_PASSED=0
TESTS_FAILED=0

# Paths
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TEMPLATE_PATH="${SCRIPT_DIR}/../skills/spec/templates/ralph.sh.template"
TEST_DIR=""
GENERATED_SCRIPT=""

# ------------------------------------------------------------------
# Setup and Teardown
# ------------------------------------------------------------------

setup() {
    TEST_DIR=$(mktemp -d)

    # Create test PRD file
    mkdir -p "${TEST_DIR}/.ralph/test-feature"
    cat > "${TEST_DIR}/prd.json" << 'EOF'
{
    "title": "Test Feature",
    "version": "2.0",
    "slug": "test-feature",
    "userStories": [
        {
            "id": "US1",
            "title": "First Story",
            "status": "pending",
            "passes": false,
            "dependencies": { "depends_on": [] }
        },
        {
            "id": "US2",
            "title": "Second Story",
            "status": "pending",
            "passes": false,
            "dependencies": { "depends_on": ["US1"] }
        },
        {
            "id": "US3",
            "title": "Third Story",
            "status": "completed",
            "passes": true,
            "dependencies": { "depends_on": [] }
        }
    ]
}
EOF

    # Generate script from template
    GENERATED_SCRIPT="${TEST_DIR}/ralph.sh"
    sed -e "s|{{FEATURE_SLUG}}|test-feature|g" \
        -e "s|{{PRD_FILE}}|${TEST_DIR}/prd.json|g" \
        -e "s|{{SPEC_DIR}}|${TEST_DIR}|g" \
        -e "s|{{RALPH_DIR}}|${TEST_DIR}/.ralph/test-feature|g" \
        "$TEMPLATE_PATH" > "$GENERATED_SCRIPT"
    chmod +x "$GENERATED_SCRIPT"
}

teardown() {
    rm -rf "$TEST_DIR"
}

# ------------------------------------------------------------------
# Test Helpers
# ------------------------------------------------------------------

assert_equals() {
    local expected="$1"
    local actual="$2"
    local message="${3:-}"

    if [[ "$expected" == "$actual" ]]; then
        return 0
    else
        echo -e "${RED}ASSERTION FAILED${NC}: Expected '$expected', got '$actual'"
        [[ -n "$message" ]] && echo "  Message: $message"
        return 1
    fi
}

assert_contains() {
    local haystack="$1"
    local needle="$2"
    local message="${3:-}"

    if [[ "$haystack" == *"$needle"* ]]; then
        return 0
    else
        echo -e "${RED}ASSERTION FAILED${NC}: Output does not contain '$needle'"
        [[ -n "$message" ]] && echo "  Message: $message"
        return 1
    fi
}

assert_exit_code() {
    local expected="$1"
    local actual="$2"
    local message="${3:-}"

    if [[ "$expected" == "$actual" ]]; then
        return 0
    else
        echo -e "${RED}ASSERTION FAILED${NC}: Expected exit code '$expected', got '$actual'"
        [[ -n "$message" ]] && echo "  Message: $message"
        return 1
    fi
}

run_test() {
    local test_name="$1"
    local test_func="$2"

    TESTS_RUN=$((TESTS_RUN + 1))
    echo -n "  Testing: $test_name... "

    setup

    if $test_func; then
        echo -e "${GREEN}PASS${NC}"
        TESTS_PASSED=$((TESTS_PASSED + 1))
    else
        echo -e "${RED}FAIL${NC}"
        TESTS_FAILED=$((TESTS_FAILED + 1))
    fi

    teardown
}

# ------------------------------------------------------------------
# Test Cases: Template Structure (AC1, AC6)
# ------------------------------------------------------------------

test_template_exists() {
    [[ -f "$TEMPLATE_PATH" ]]
}

test_placeholders_substituted() {
    # Check no placeholders remain after substitution
    if grep -q '{{' "$GENERATED_SCRIPT"; then
        echo "Unsubstituted placeholders found"
        return 1
    fi
    return 0
}

test_help_flag() {
    local output
    output=$("$GENERATED_SCRIPT" --help 2>&1)

    assert_contains "$output" "Ralph Wiggum" "Should show title" && \
    assert_contains "$output" "--quiet" "Should document --quiet" && \
    assert_contains "$output" "--dry-run" "Should document --dry-run" && \
    assert_contains "$output" "--dangerously-skip-permissions" "Should document --dangerously-skip-permissions"
}

test_unknown_flag_error() {
    local output exit_code
    output=$("$GENERATED_SCRIPT" --unknown-flag 2>&1) || exit_code=$?

    assert_contains "$output" "Unknown option" "Should report unknown option" && \
    [[ ${exit_code:-0} -ne 0 ]]
}

test_requires_dangerously_skip_permissions() {
    local output exit_code
    output=$("$GENERATED_SCRIPT" 2>&1) || exit_code=$?

    assert_contains "$output" "--dangerously-skip-permissions is required" "Should require flag" && \
    [[ ${exit_code:-0} -ne 0 ]]
}

# ------------------------------------------------------------------
# Test Cases: PRD Validation
# ------------------------------------------------------------------

test_prd_not_found_error() {
    # Modify script to point to non-existent PRD
    local bad_script="${TEST_DIR}/bad_ralph.sh"
    sed "s|${TEST_DIR}/prd.json|/nonexistent/prd.json|g" "$GENERATED_SCRIPT" > "$bad_script"
    chmod +x "$bad_script"

    local output exit_code
    output=$("$bad_script" --dangerously-skip-permissions 2>&1) || exit_code=$?

    assert_contains "$output" "PRD file not found" "Should report missing PRD"
}

test_prd_invalid_json_error() {
    # Create invalid JSON
    echo "not valid json" > "${TEST_DIR}/prd.json"

    local output exit_code
    output=$("$GENERATED_SCRIPT" --dangerously-skip-permissions 2>&1) || exit_code=$?

    assert_contains "$output" "not valid JSON" "Should report invalid JSON"
}

test_prd_missing_userstories_error() {
    # Create JSON without userStories
    echo '{"title": "Test", "version": "2.0"}' > "${TEST_DIR}/prd.json"

    local output exit_code
    output=$("$GENERATED_SCRIPT" --dangerously-skip-permissions 2>&1) || exit_code=$?

    assert_contains "$output" "missing userStories" "Should report missing userStories"
}

# ------------------------------------------------------------------
# Test Cases: Dry Run Mode (AC6)
# ------------------------------------------------------------------

test_dry_run_shows_stories() {
    local output
    output=$("$GENERATED_SCRIPT" --dry-run 2>&1)

    assert_contains "$output" "DRY RUN" "Should indicate dry run" && \
    assert_contains "$output" "US1" "Should show US1" && \
    assert_contains "$output" "US2" "Should show US2" && \
    assert_contains "$output" "2 pending" "Should show pending count"
}

test_dry_run_exits_zero() {
    local exit_code=0
    "$GENERATED_SCRIPT" --dry-run >/dev/null 2>&1 || exit_code=$?

    assert_exit_code "0" "$exit_code" "Dry run should exit 0"
}

# ------------------------------------------------------------------
# Test Cases: RALPH_STATUS Parsing (AC4)
# ------------------------------------------------------------------

# Helper to extract status from RALPH_STATUS block (mirrors template logic)
_test_extract_status() {
    local output="$1"
    local status_block
    status_block=$(echo "$output" | sed -n '/<<<RALPH_STATUS>>>/,/<<<END_RALPH_STATUS>>>/p' | grep -v '<<<')
    echo "$status_block" | grep "^status:" | cut -d':' -f2- | xargs
}

test_parse_ralph_status_success() {
    local test_output='Some output
<<<RALPH_STATUS>>>
story_id: US1
status: SUCCESS
passes: true
error: null
files_modified: [test.py]
next_story: US2
timestamp: 2026-02-02T10:00:00Z
<<<END_RALPH_STATUS>>>'

    local status
    status=$(_test_extract_status "$test_output")

    assert_equals "SUCCESS" "$status" "Should parse SUCCESS status"
}

test_parse_ralph_status_all_done() {
    local test_output='<<<RALPH_STATUS>>>
story_id: null
status: ALL_DONE
passes: true
error: null
files_modified: []
next_story: null
timestamp: 2026-02-02T10:00:00Z
<<<END_RALPH_STATUS>>>'

    local status
    status=$(_test_extract_status "$test_output")

    assert_equals "ALL_DONE" "$status" "Should parse ALL_DONE status"
}

test_parse_ralph_status_blocked() {
    local test_output='<<<RALPH_STATUS>>>
story_id: null
status: BLOCKED
passes: false
error: "US3 blocked by failed US2"
files_modified: []
next_story: null
timestamp: 2026-02-02T10:00:00Z
<<<END_RALPH_STATUS>>>'

    local status
    status=$(_test_extract_status "$test_output")

    assert_equals "BLOCKED" "$status" "Should parse BLOCKED status"
}

test_parse_ralph_status_failure() {
    local test_output='<<<RALPH_STATUS>>>
story_id: US1
status: FAILURE
passes: false
error: "Tests failed"
files_modified: []
next_story: null
timestamp: 2026-02-02T10:00:00Z
<<<END_RALPH_STATUS>>>'

    local status
    status=$(_test_extract_status "$test_output")

    assert_equals "FAILURE" "$status" "Should parse FAILURE status"
}

test_no_status_block() {
    local test_output='Some output without status block'

    local status_block
    status_block=$(echo "$test_output" | sed -n '/<<<RALPH_STATUS>>>/,/<<<END_RALPH_STATUS>>>/p' | grep -v '<<<' || echo "")

    [[ -z "$status_block" ]]
}

# ------------------------------------------------------------------
# Test Cases: Circuit Breaker Integration (AC3 - via task-003)
# ------------------------------------------------------------------

test_circuit_breaker_functions_exist() {
    # Check that circuit breaker functions are in the generated script
    assert_contains "$(cat "$GENERATED_SCRIPT")" "reset_circuit_breaker" "Should have reset function" && \
    assert_contains "$(cat "$GENERATED_SCRIPT")" "record_and_check" "Should have record_and_check function" && \
    assert_contains "$(cat "$GENERATED_SCRIPT")" "check_circuit_breaker" "Should have check function" && \
    assert_contains "$(cat "$GENERATED_SCRIPT")" "CB_THRESHOLD" "Should have threshold config"
}

test_circuit_breaker_inline() {
    # Verify circuit breaker is inline (no source command for it)
    if grep -q "source.*circuit-breaker" "$GENERATED_SCRIPT"; then
        echo "Circuit breaker should be inline, not sourced"
        return 1
    fi
    return 0
}

# ------------------------------------------------------------------
# Test Cases: Progress Logging (AC5, AC7)
# ------------------------------------------------------------------

test_progress_file_created() {
    # Dry run should still show progress file path
    local output
    output=$("$GENERATED_SCRIPT" --dry-run 2>&1)

    # Check PROGRESS_FILE is set correctly
    assert_contains "$(cat "$GENERATED_SCRIPT")" "PROGRESS_FILE=" "Should define PROGRESS_FILE"
}

test_log_progress_function() {
    # Check log_progress function exists
    assert_contains "$(cat "$GENERATED_SCRIPT")" "log_progress()" "Should have log_progress function" && \
    assert_contains "$(cat "$GENERATED_SCRIPT")" "date -Iseconds" "Should use ISO timestamps"
}

test_progress_bar_function() {
    # Check progress bar function exists
    assert_contains "$(cat "$GENERATED_SCRIPT")" "show_progress_bar()" "Should have progress bar function"
}

test_elapsed_time_function() {
    # Check elapsed time function exists
    assert_contains "$(cat "$GENERATED_SCRIPT")" "get_elapsed()" "Should have elapsed time function"
}

# ------------------------------------------------------------------
# Test Cases: Main Loop Structure (AC2)
# ------------------------------------------------------------------

test_max_iterations_config() {
    assert_contains "$(cat "$GENERATED_SCRIPT")" 'MAX_ITERATIONS=${MAX_ITERATIONS:-50}' "Should have MAX_ITERATIONS default"
}

test_main_loop_exists() {
    assert_contains "$(cat "$GENERATED_SCRIPT")" 'for ((i=1; i<=MAX_ITERATIONS; i++))' "Should have main loop"
}

test_exit_codes() {
    # Check all exit codes are documented
    assert_contains "$(cat "$GENERATED_SCRIPT")" "exit 0" "Should have exit 0 (success)" && \
    assert_contains "$(cat "$GENERATED_SCRIPT")" "exit 1" "Should have exit 1 (max iterations)" && \
    assert_contains "$(cat "$GENERATED_SCRIPT")" "exit 2" "Should have exit 2 (circuit breaker)" && \
    assert_contains "$(cat "$GENERATED_SCRIPT")" "exit 3" "Should have exit 3 (blocked)"
}

# ------------------------------------------------------------------
# Test Cases: Claude Invocation (AC1, AC3)
# ------------------------------------------------------------------

test_claude_invocation() {
    assert_contains "$(cat "$GENERATED_SCRIPT")" 'claude --dangerously-skip-permissions "/ralph-exec --prd' "Should invoke claude with correct args"
}

# ------------------------------------------------------------------
# Main Test Runner
# ------------------------------------------------------------------

main() {
    echo ""
    echo "========================================"
    echo " Ralph Template Unit Tests"
    echo "========================================"
    echo ""

    # Check template exists
    if [[ ! -f "$TEMPLATE_PATH" ]]; then
        echo -e "${RED}ERROR${NC}: Template not found at: $TEMPLATE_PATH"
        exit 1
    fi

    echo "Template path: $TEMPLATE_PATH"
    echo ""

    # Template Structure (AC1, AC6)
    echo "Template Structure:"
    run_test "template exists" test_template_exists
    run_test "placeholders substituted" test_placeholders_substituted
    run_test "--help flag works" test_help_flag
    run_test "unknown flag error" test_unknown_flag_error
    run_test "requires --dangerously-skip-permissions" test_requires_dangerously_skip_permissions
    echo ""

    # PRD Validation
    echo "PRD Validation:"
    run_test "PRD not found error" test_prd_not_found_error
    run_test "PRD invalid JSON error" test_prd_invalid_json_error
    run_test "PRD missing userStories error" test_prd_missing_userstories_error
    echo ""

    # Dry Run Mode (AC6)
    echo "Dry Run Mode (AC6):"
    run_test "shows pending stories" test_dry_run_shows_stories
    run_test "exits zero" test_dry_run_exits_zero
    echo ""

    # RALPH_STATUS Parsing (AC4)
    echo "RALPH_STATUS Parsing (AC4):"
    run_test "parse SUCCESS status" test_parse_ralph_status_success
    run_test "parse ALL_DONE status" test_parse_ralph_status_all_done
    run_test "parse BLOCKED status" test_parse_ralph_status_blocked
    run_test "parse FAILURE status" test_parse_ralph_status_failure
    run_test "handle no status block" test_no_status_block
    echo ""

    # Circuit Breaker Integration
    echo "Circuit Breaker Integration:"
    run_test "functions exist" test_circuit_breaker_functions_exist
    run_test "inline (not sourced)" test_circuit_breaker_inline
    echo ""

    # Progress Logging (AC5, AC7)
    echo "Progress Logging (AC5, AC7):"
    run_test "progress file defined" test_progress_file_created
    run_test "log_progress function" test_log_progress_function
    run_test "progress bar function" test_progress_bar_function
    run_test "elapsed time function" test_elapsed_time_function
    echo ""

    # Main Loop Structure (AC2)
    echo "Main Loop Structure (AC2):"
    run_test "MAX_ITERATIONS config" test_max_iterations_config
    run_test "main loop exists" test_main_loop_exists
    run_test "exit codes defined" test_exit_codes
    echo ""

    # Claude Invocation (AC1, AC3)
    echo "Claude Invocation (AC1, AC3):"
    run_test "claude invocation correct" test_claude_invocation
    echo ""

    # Summary
    echo "========================================"
    echo " Results: $TESTS_PASSED/$TESTS_RUN passed"
    echo "========================================"

    if [[ $TESTS_FAILED -gt 0 ]]; then
        echo -e "${RED}$TESTS_FAILED test(s) failed${NC}"
        exit 1
    else
        echo -e "${GREEN}All tests passed!${NC}"
        exit 0
    fi
}

main "$@"
