#!/bin/bash
# tests/test-common.sh — Unit tests for lib/common.sh
# Custom Bash test harness (pass/fail counters)
set -uo pipefail

# === Test Framework ===
TESTS_PASSED=0
TESTS_FAILED=0
TESTS_TOTAL=0
CURRENT_TEST=""

pass() {
    ((TESTS_PASSED++))
    echo -e "  [PASS] $CURRENT_TEST"
}

fail() {
    ((TESTS_FAILED++))
    echo -e "  [FAIL] $CURRENT_TEST: $1"
}

run_test() {
    CURRENT_TEST="$1"
    ((TESTS_TOTAL++))
    shift
    "$@"
}

# === Setup ===
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Source the library under test
if [[ ! -f "$PROJECT_ROOT/lib/common.sh" ]]; then
    echo "ERROR: lib/common.sh not found"
    exit 1
fi
source "$PROJECT_ROOT/lib/common.sh"

# Temp dir for test artifacts
TEST_TMP="$(mktemp -d)"
trap 'rm -rf "$TEST_TMP"' EXIT

# === Test Cases ===

test_log_info_outputs_message() {
    local output
    output=$(LOG_DIR="$TEST_TMP" log_info "hello world" 2>&1)
    if echo "$output" | grep -q "hello world"; then
        pass
    else
        fail "Expected 'hello world' in output, got: $output"
    fi
}

test_log_info_has_timestamp() {
    local output
    output=$(LOG_DIR="$TEST_TMP" log_info "timestamp test" 2>&1)
    # ISO-8601 pattern: YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS
    if echo "$output" | grep -qE '[0-9]{4}-[0-9]{2}-[0-9]{2}'; then
        pass
    else
        fail "Expected ISO-8601 timestamp in output, got: $output"
    fi
}

test_log_info_has_info_level() {
    local output
    output=$(LOG_DIR="$TEST_TMP" log_info "level test" 2>&1)
    if echo "$output" | grep -qi "INFO"; then
        pass
    else
        fail "Expected INFO level marker, got: $output"
    fi
}

test_log_error_writes_to_stderr() {
    local stderr_output
    stderr_output=$(LOG_DIR="$TEST_TMP" log_error "error msg" 2>&1 1>/dev/null)
    if echo "$stderr_output" | grep -q "error msg"; then
        pass
    else
        fail "Expected 'error msg' on stderr, got: $stderr_output"
    fi
}

test_log_warn_has_warn_level() {
    local output
    output=$(LOG_DIR="$TEST_TMP" log_warn "warn test" 2>&1)
    if echo "$output" | grep -qi "WARN"; then
        pass
    else
        fail "Expected WARN level marker, got: $output"
    fi
}

test_log_debug_silent_when_not_enabled() {
    local output
    output=$(LOG_DIR="$TEST_TMP" DEBUG="" log_debug "debug msg" 2>&1)
    if [[ -z "$output" ]]; then
        pass
    else
        fail "Expected no output when DEBUG is empty, got: $output"
    fi
}

test_log_debug_outputs_when_enabled() {
    local output
    output=$(LOG_DIR="$TEST_TMP" DEBUG=1 log_debug "debug msg" 2>&1)
    if echo "$output" | grep -q "debug msg"; then
        pass
    else
        fail "Expected 'debug msg' in output, got: $output"
    fi
}

test_log_to_file_writes_logfile() {
    LOG_DIR="$TEST_TMP" log_info "file test" >/dev/null 2>&1
    local logfile
    logfile=$(ls "$TEST_TMP"/pipeline-*.log 2>/dev/null | head -1)
    if [[ -n "$logfile" ]] && grep -q "file test" "$logfile"; then
        pass
    else
        fail "Expected log entry in file, logfile=${logfile:-not_found}"
    fi
}

test_die_exits_nonzero() {
    local exit_code=0
    (LOG_DIR="$TEST_TMP" die "fatal error" 2>/dev/null) && exit_code=0 || exit_code=$?
    if [[ $exit_code -ne 0 ]]; then
        pass
    else
        fail "Expected non-zero exit code from die(), got: $exit_code"
    fi
}

test_die_outputs_error_message() {
    local output
    output=$(LOG_DIR="$TEST_TMP" die "fatal reason" 2>&1) || true
    if echo "$output" | grep -q "fatal reason"; then
        pass
    else
        fail "Expected 'fatal reason' in die output, got: $output"
    fi
}

test_require_command_passes_for_bash() {
    if require_command bash; then
        pass
    else
        fail "Expected require_command to succeed for bash"
    fi
}

test_require_command_fails_for_missing() {
    local exit_code=0
    require_command "nonexistent_cmd_xyz" >/dev/null 2>&1 && exit_code=0 || exit_code=$?
    if [[ $exit_code -ne 0 ]]; then
        pass
    else
        fail "Expected require_command to fail for missing command"
    fi
}

# === Run Tests ===
echo "=== tests/test-common.sh ==="
echo ""

run_test "log_info outputs message" test_log_info_outputs_message
run_test "log_info has ISO-8601 timestamp" test_log_info_has_timestamp
run_test "log_info has INFO level" test_log_info_has_info_level
run_test "log_error writes to stderr" test_log_error_writes_to_stderr
run_test "log_warn has WARN level" test_log_warn_has_warn_level
run_test "log_debug silent when not enabled" test_log_debug_silent_when_not_enabled
run_test "log_debug outputs when enabled" test_log_debug_outputs_when_enabled
run_test "log_to_file writes log file" test_log_to_file_writes_logfile
run_test "die exits with non-zero" test_die_exits_nonzero
run_test "die outputs error message" test_die_outputs_error_message
run_test "require_command passes for bash" test_require_command_passes_for_bash
run_test "require_command fails for missing cmd" test_require_command_fails_for_missing

# === Summary ===
echo ""
echo "Results: $TESTS_PASSED passed, $TESTS_FAILED failed out of $TESTS_TOTAL"
echo ""

if [[ $TESTS_FAILED -gt 0 ]]; then
    exit 1
fi
exit 0
