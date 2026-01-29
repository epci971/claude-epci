#!/bin/bash
#
# test-worktree-scripts.sh - Integration tests for worktree scripts
#
# Usage: test-worktree-scripts.sh
#
# Exit codes:
#   0 - All tests passed
#   1 - One or more tests failed

set -uo pipefail
# Note: -e intentionally not set because arithmetic operations like ((TESTS_PASSED++))
# return non-zero when incrementing from 0, which would cause the script to exit

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Test counters
TESTS_PASSED=0
TESTS_FAILED=0

# Script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Test feature slug
TEST_SLUG="test-worktree-$$"

# Cleanup function
cleanup() {
    echo ""
    echo "Cleaning up..."

    # Remove worktree if exists
    local repo_root
    repo_root=$(git rev-parse --show-toplevel 2>/dev/null || echo "")

    if [[ -n "$repo_root" ]]; then
        local worktree_path="${repo_root}/../worktrees/${TEST_SLUG}"

        # Force remove worktree
        git worktree remove --force "${worktree_path}" 2>/dev/null || true
        git worktree prune 2>/dev/null || true

        # Delete test branch
        git branch -D "feature/${TEST_SLUG}" 2>/dev/null || true

        # Remove orphan directory if any
        rm -rf "${worktree_path}" 2>/dev/null || true
    fi

    echo "Cleanup complete."
}

# Register cleanup on exit
trap cleanup EXIT

# Test helper functions
pass() {
    echo -e "${GREEN}[PASS]${NC} $1"
    ((TESTS_PASSED++))
}

fail() {
    echo -e "${RED}[FAIL]${NC} $1"
    ((TESTS_FAILED++))
}

skip() {
    echo -e "${YELLOW}[SKIP]${NC} $1"
}

# Test 1: worktree-status.sh returns not exists for non-existent worktree
test_status_not_exists() {
    local output
    output=$("${SCRIPT_DIR}/worktree-status.sh" "${TEST_SLUG}" 2>/dev/null)

    if echo "$output" | grep -q '"exists": false'; then
        pass "Status returns exists=false for non-existent worktree"
    else
        fail "Status should return exists=false, got: $output"
    fi
}

# Test 2: worktree-create.sh creates worktree successfully
test_create_success() {
    local output
    local exit_code=0

    output=$("${SCRIPT_DIR}/worktree-create.sh" "${TEST_SLUG}" 2>&1) || exit_code=$?

    if [[ $exit_code -eq 0 ]] && echo "$output" | grep -q "Worktree created successfully"; then
        pass "Create worktree succeeds"
    else
        fail "Create worktree failed with exit code $exit_code: $output"
    fi
}

# Test 3: worktree-status.sh returns exists=true after creation
test_status_exists() {
    local output
    output=$("${SCRIPT_DIR}/worktree-status.sh" "${TEST_SLUG}" 2>/dev/null)

    if echo "$output" | grep -q '"exists": true'; then
        pass "Status returns exists=true for existing worktree"
    else
        fail "Status should return exists=true, got: $output"
    fi
}

# Test 4: worktree-status.sh returns clean=true for clean worktree
test_status_clean() {
    local output
    output=$("${SCRIPT_DIR}/worktree-status.sh" "${TEST_SLUG}" 2>/dev/null)

    if echo "$output" | grep -q '"clean": true'; then
        pass "Status returns clean=true for clean worktree"
    else
        fail "Status should return clean=true, got: $output"
    fi
}

# Test 5: worktree-create.sh fails for existing worktree
test_create_already_exists() {
    local exit_code=0

    "${SCRIPT_DIR}/worktree-create.sh" "${TEST_SLUG}" >/dev/null 2>&1 || exit_code=$?

    if [[ $exit_code -eq 2 ]]; then
        pass "Create fails with exit code 2 for existing worktree"
    else
        fail "Create should fail with exit code 2, got: $exit_code"
    fi
}

# Test 6: worktree-status.sh returns clean=false after modification
test_status_dirty() {
    local repo_root
    repo_root=$(git rev-parse --show-toplevel)
    local worktree_path="${repo_root}/../worktrees/${TEST_SLUG}"

    # Create a file to make worktree dirty
    echo "test" > "${worktree_path}/test-dirty-file.txt"

    local output
    output=$("${SCRIPT_DIR}/worktree-status.sh" "${TEST_SLUG}" 2>/dev/null)

    if echo "$output" | grep -q '"clean": false'; then
        pass "Status returns clean=false for dirty worktree"
    else
        fail "Status should return clean=false, got: $output"
    fi

    # Clean up the test file
    rm -f "${worktree_path}/test-dirty-file.txt"
}

# Test 7: worktree-finalize.sh fails without --force for dirty worktree
test_finalize_dirty_fails() {
    local repo_root
    repo_root=$(git rev-parse --show-toplevel)
    local worktree_path="${repo_root}/../worktrees/${TEST_SLUG}"

    # Create a file to make worktree dirty
    echo "test" > "${worktree_path}/test-dirty-file.txt"

    local exit_code=0
    "${SCRIPT_DIR}/worktree-finalize.sh" "${TEST_SLUG}" >/dev/null 2>&1 || exit_code=$?

    if [[ $exit_code -eq 3 ]]; then
        pass "Finalize fails with exit code 3 for dirty worktree without --force"
    else
        fail "Finalize should fail with exit code 3, got: $exit_code"
    fi

    # Clean up
    rm -f "${worktree_path}/test-dirty-file.txt"
}

# Test 8: worktree-finalize.sh succeeds for clean worktree
test_finalize_success() {
    local output
    local exit_code=0

    output=$("${SCRIPT_DIR}/worktree-finalize.sh" "${TEST_SLUG}" 2>&1) || exit_code=$?

    if [[ $exit_code -eq 0 ]] && echo "$output" | grep -q "Worktree removed"; then
        pass "Finalize worktree succeeds"
    else
        fail "Finalize worktree failed with exit code $exit_code: $output"
    fi
}

# Test 9: worktree-status.sh returns exists=false after finalization
test_status_after_finalize() {
    local output
    output=$("${SCRIPT_DIR}/worktree-status.sh" "${TEST_SLUG}" 2>/dev/null)

    if echo "$output" | grep -q '"exists": false'; then
        pass "Status returns exists=false after finalization"
    else
        fail "Status should return exists=false after finalization, got: $output"
    fi
}

# Test 10: Invalid feature slug rejected
test_invalid_slug() {
    local exit_code=0

    "${SCRIPT_DIR}/worktree-create.sh" "Invalid_Slug" >/dev/null 2>&1 || exit_code=$?

    if [[ $exit_code -eq 1 ]]; then
        pass "Invalid slug rejected with exit code 1"
    else
        fail "Invalid slug should be rejected with exit code 1, got: $exit_code"
    fi
}

# Run all tests
main() {
    echo "=========================================="
    echo "  Worktree Scripts Integration Tests"
    echo "=========================================="
    echo ""
    echo "Test slug: ${TEST_SLUG}"
    echo ""

    # Make scripts executable
    chmod +x "${SCRIPT_DIR}/worktree-create.sh"
    chmod +x "${SCRIPT_DIR}/worktree-finalize.sh"
    chmod +x "${SCRIPT_DIR}/worktree-status.sh"

    # Run tests in order
    test_status_not_exists
    test_create_success
    test_status_exists
    test_status_clean
    test_create_already_exists
    test_status_dirty
    test_finalize_dirty_fails
    test_finalize_success
    test_status_after_finalize
    test_invalid_slug

    echo ""
    echo "=========================================="
    echo "  Results: ${TESTS_PASSED} passed, ${TESTS_FAILED} failed"
    echo "=========================================="

    if [[ $TESTS_FAILED -gt 0 ]]; then
        exit 1
    fi

    exit 0
}

main "$@"
