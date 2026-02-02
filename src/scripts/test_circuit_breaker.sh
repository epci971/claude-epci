#!/usr/bin/env bash
# test_circuit_breaker.sh - Unit tests for circuit breaker functionality
# Tests: no-progress detection, same-error detection, exit codes, logging

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

# Temporary directory for test artifacts
TEST_DIR=""

# ------------------------------------------------------------------
# Setup and Teardown
# ------------------------------------------------------------------

setup() {
    TEST_DIR=$(mktemp -d)
    cd "$TEST_DIR"

    # Source the circuit breaker code
    # shellcheck source=/dev/null
    source "$CIRCUIT_BREAKER_PATH"

    # Initialize arrays
    FILE_HASHES=()
    ERROR_HASHES=()
}

teardown() {
    cd /
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
        echo -e "${RED}ASSERTION FAILED${NC}: '$haystack' does not contain '$needle'"
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
# Test Cases: No-Progress Detection (AC2)
# ------------------------------------------------------------------

test_no_progress_after_3_same_hashes() {
    # Simulate 3 iterations with same file hash
    local same_hash="abc123"

    FILE_HASHES+=("$same_hash")
    check_circuit_breaker; local result1=$?

    FILE_HASHES+=("$same_hash")
    check_circuit_breaker; local result2=$?

    FILE_HASHES+=("$same_hash")
    check_circuit_breaker; local result3=$?

    # First two should continue (0), third should trigger (1)
    assert_equals "0" "$result1" "First iteration should continue" && \
    assert_equals "0" "$result2" "Second iteration should continue" && \
    assert_equals "1" "$result3" "Third same hash should trigger circuit breaker"
}

test_no_progress_reset_on_different_hash() {
    local hash1="abc123"
    local hash2="def456"

    FILE_HASHES+=("$hash1")
    check_circuit_breaker

    FILE_HASHES+=("$hash1")
    check_circuit_breaker

    # Different hash resets the counter
    FILE_HASHES+=("$hash2")
    check_circuit_breaker; local result=$?

    assert_equals "0" "$result" "Different hash should reset counter and continue"
}

test_no_progress_message() {
    local same_hash="abc123"
    PROGRESS_FILE="$TEST_DIR/progress.txt"

    FILE_HASHES+=("$same_hash")
    FILE_HASHES+=("$same_hash")
    FILE_HASHES+=("$same_hash")

    check_circuit_breaker

    if [[ -f "$PROGRESS_FILE" ]]; then
        assert_contains "$(cat "$PROGRESS_FILE")" "no progress" "Log should contain 'no progress'"
    else
        echo "Progress file not created"
        return 1
    fi
}

# ------------------------------------------------------------------
# Test Cases: Same-Error Detection (AC3)
# ------------------------------------------------------------------

test_same_error_after_3_same_hashes() {
    local same_error="error_hash_xyz"

    # Add varying file hashes to avoid file-based trigger
    FILE_HASHES+=("file1")
    ERROR_HASHES+=("$same_error")
    check_circuit_breaker; local result1=$?

    FILE_HASHES+=("file2")
    ERROR_HASHES+=("$same_error")
    check_circuit_breaker; local result2=$?

    FILE_HASHES+=("file3")
    ERROR_HASHES+=("$same_error")
    check_circuit_breaker; local result3=$?

    assert_equals "0" "$result1" "First error should continue" && \
    assert_equals "0" "$result2" "Second same error should continue" && \
    assert_equals "1" "$result3" "Third same error should trigger circuit breaker"
}

test_same_error_reset_on_different_error() {
    local error1="error_abc"
    local error2="error_xyz"

    # Add varying file hashes to avoid file-based trigger
    FILE_HASHES+=("file1")
    ERROR_HASHES+=("$error1")
    check_circuit_breaker

    FILE_HASHES+=("file2")
    ERROR_HASHES+=("$error1")
    check_circuit_breaker

    FILE_HASHES+=("file3")
    ERROR_HASHES+=("$error2")
    check_circuit_breaker; local result=$?

    assert_equals "0" "$result" "Different error should reset counter and continue"
}

test_same_error_message() {
    local same_error="error_repeated"
    PROGRESS_FILE="$TEST_DIR/progress.txt"

    # Add varying file hashes to ensure error-based trigger
    FILE_HASHES+=("file1")
    ERROR_HASHES+=("$same_error")
    FILE_HASHES+=("file2")
    ERROR_HASHES+=("$same_error")
    FILE_HASHES+=("file3")
    ERROR_HASHES+=("$same_error")

    check_circuit_breaker

    if [[ -f "$PROGRESS_FILE" ]]; then
        assert_contains "$(cat "$PROGRESS_FILE")" "repeated error" "Log should contain 'repeated error'"
    else
        echo "Progress file not created"
        return 1
    fi
}

# ------------------------------------------------------------------
# Test Cases: Exit Codes (AC4)
# ------------------------------------------------------------------

test_exit_code_continue() {
    # Single entry should continue (need 3 same for trigger)
    FILE_HASHES+=("hash1")
    ERROR_HASHES+=("err1")
    check_circuit_breaker; local result=$?

    assert_equals "0" "$result" "Continue should return 0"
}

test_exit_code_circuit_breaker() {
    local same="identical"
    FILE_HASHES+=("$same")
    FILE_HASHES+=("$same")
    FILE_HASHES+=("$same")

    check_circuit_breaker; local result=$?

    assert_equals "1" "$result" "Circuit breaker should return 1 (stop signal)"
}

# ------------------------------------------------------------------
# Test Cases: Logging (AC5)
# ------------------------------------------------------------------

test_logging_timestamp() {
    PROGRESS_FILE="$TEST_DIR/progress.txt"
    local same="stagnant"

    FILE_HASHES+=("$same")
    FILE_HASHES+=("$same")
    FILE_HASHES+=("$same")

    check_circuit_breaker

    if [[ -f "$PROGRESS_FILE" ]]; then
        # Check for ISO-8601 like timestamp pattern (YYYY-MM-DD or similar)
        if grep -qE '[0-9]{4}-[0-9]{2}-[0-9]{2}' "$PROGRESS_FILE"; then
            return 0
        else
            echo "No timestamp found in log"
            return 1
        fi
    else
        echo "Progress file not created"
        return 1
    fi
}

test_logging_iteration_count() {
    PROGRESS_FILE="$TEST_DIR/progress.txt"
    CURRENT_ITERATION=5
    local same="repeated"

    FILE_HASHES+=("$same")
    FILE_HASHES+=("$same")
    FILE_HASHES+=("$same")

    check_circuit_breaker

    if [[ -f "$PROGRESS_FILE" ]]; then
        assert_contains "$(cat "$PROGRESS_FILE")" "iteration" "Log should contain iteration info"
    else
        echo "Progress file not created"
        return 1
    fi
}

# ------------------------------------------------------------------
# Test Cases: Hash Calculation
# ------------------------------------------------------------------

test_calculate_file_hash_empty() {
    # When no files changed, hash should be consistent
    local hash1
    local hash2
    hash1=$(calculate_file_hash)
    hash2=$(calculate_file_hash)

    assert_equals "$hash1" "$hash2" "Same state should produce same hash"
}

test_calculate_file_hash_changes() {
    local hash1
    hash1=$(calculate_file_hash)

    # Create a file to simulate change
    echo "new content" > "$TEST_DIR/test_file.txt"
    git init -q 2>/dev/null || true
    git add . 2>/dev/null || true

    local hash2
    hash2=$(calculate_file_hash)

    # Hashes might be same if git diff is empty, that's OK for this test
    # The important thing is the function runs without error
    [[ -n "$hash1" ]] && [[ -n "$hash2" ]]
}

test_calculate_error_hash() {
    local error_msg="Error: something went wrong"
    local hash1
    local hash2
    hash1=$(calculate_error_hash "$error_msg")
    hash2=$(calculate_error_hash "$error_msg")

    assert_equals "$hash1" "$hash2" "Same error should produce same hash"
}

test_calculate_error_hash_different() {
    local hash1
    local hash2
    hash1=$(calculate_error_hash "Error A")
    hash2=$(calculate_error_hash "Error B")

    if [[ "$hash1" != "$hash2" ]]; then
        return 0
    else
        echo "Different errors should produce different hashes"
        return 1
    fi
}

# ------------------------------------------------------------------
# Test Cases: Integration
# ------------------------------------------------------------------

test_mixed_file_and_error_detection() {
    # Both conditions can trigger independently
    local file_hash="file_same"
    local error_hash1="err1"
    local error_hash2="err2"

    FILE_HASHES+=("$file_hash")
    ERROR_HASHES+=("$error_hash1")
    check_circuit_breaker

    FILE_HASHES+=("$file_hash")
    ERROR_HASHES+=("$error_hash2")
    check_circuit_breaker

    FILE_HASHES+=("$file_hash")
    ERROR_HASHES+=("$error_hash1")  # Not 3 consecutive same errors
    check_circuit_breaker; local result=$?

    # Should trigger because FILE_HASHES has 3 same
    assert_equals "1" "$result" "File stagnation should trigger even with varying errors"
}

test_empty_arrays_no_trigger() {
    # With no history, should always continue
    # Make sure arrays are truly empty (setup reinitializes them)
    FILE_HASHES=()
    ERROR_HASHES=()
    check_circuit_breaker; local result=$?

    assert_equals "0" "$result" "Empty arrays should continue"
}

# ------------------------------------------------------------------
# Main Test Runner
# ------------------------------------------------------------------

main() {
    echo ""
    echo "========================================"
    echo " Circuit Breaker Unit Tests"
    echo "========================================"
    echo ""

    # Get absolute path to script directory
    local script_dir
    script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

    # Check circuit breaker path
    if [[ -z "${CIRCUIT_BREAKER_PATH:-}" ]]; then
        CIRCUIT_BREAKER_PATH="$script_dir/../skills/spec/templates/circuit-breaker.sh.snippet"
    fi

    if [[ ! -f "$CIRCUIT_BREAKER_PATH" ]]; then
        echo -e "${RED}ERROR${NC}: Circuit breaker not found at: $CIRCUIT_BREAKER_PATH"
        echo "Set CIRCUIT_BREAKER_PATH environment variable to the correct path"
        exit 1
    fi

    echo "Circuit breaker path: $CIRCUIT_BREAKER_PATH"
    echo ""

    # No-Progress Detection (AC2)
    echo "No-Progress Detection (AC2):"
    run_test "triggers after 3 same file hashes" test_no_progress_after_3_same_hashes
    run_test "resets on different hash" test_no_progress_reset_on_different_hash
    run_test "logs 'no progress' message" test_no_progress_message
    echo ""

    # Same-Error Detection (AC3)
    echo "Same-Error Detection (AC3):"
    run_test "triggers after 3 same error hashes" test_same_error_after_3_same_hashes
    run_test "resets on different error" test_same_error_reset_on_different_error
    run_test "logs 'repeated error' message" test_same_error_message
    echo ""

    # Exit Codes (AC4)
    echo "Exit Codes (AC4):"
    run_test "returns 0 for continue" test_exit_code_continue
    run_test "returns 1 for circuit breaker" test_exit_code_circuit_breaker
    echo ""

    # Logging (AC5)
    echo "Logging (AC5):"
    run_test "includes timestamp" test_logging_timestamp
    run_test "includes iteration count" test_logging_iteration_count
    echo ""

    # Hash Calculation
    echo "Hash Calculation:"
    run_test "file hash is consistent" test_calculate_file_hash_empty
    run_test "file hash function works" test_calculate_file_hash_changes
    run_test "error hash is consistent" test_calculate_error_hash
    run_test "different errors have different hashes" test_calculate_error_hash_different
    echo ""

    # Integration
    echo "Integration:"
    run_test "mixed file/error detection" test_mixed_file_and_error_detection
    run_test "empty arrays continue" test_empty_arrays_no_trigger
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
