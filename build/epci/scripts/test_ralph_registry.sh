#!/usr/bin/env bash
# test_ralph_registry.sh - Unit tests for Ralph Registry schema and step-03 logic
# Tests: schema fields, status enum, duplicate handling, auto-creation
# Task-007: Create Registry index.json

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
SCHEMA_FILE="${SCRIPT_DIR}/../schemas/ralph-registry-v1.json"
STEP_FILE="${SCRIPT_DIR}/../skills/spec/steps/step-03-generate-ralph.md"

# ------------------------------------------------------------------
# Test Helpers
# ------------------------------------------------------------------

assert_file_exists() {
    local file="$1"
    local desc="$2"

    if [[ -f "$file" ]]; then
        return 0
    else
        echo -e "${RED}ASSERTION FAILED${NC}: File not found: $file"
        echo "  Description: $desc"
        return 1
    fi
}

assert_contains() {
    local file="$1"
    local needle="$2"
    local desc="$3"

    if grep -q "$needle" "$file" 2>/dev/null; then
        return 0
    else
        echo -e "${RED}ASSERTION FAILED${NC}: '$file' does not contain '$needle'"
        echo "  Description: $desc"
        return 1
    fi
}

assert_json_has_field() {
    local file="$1"
    local field="$2"
    local desc="$3"

    if grep -q "\"$field\"" "$file" 2>/dev/null; then
        return 0
    else
        echo -e "${RED}ASSERTION FAILED${NC}: JSON '$file' missing field '$field'"
        echo "  Description: $desc"
        return 1
    fi
}

run_test() {
    local test_name="$1"
    local test_func="$2"

    TESTS_RUN=$((TESTS_RUN + 1))
    echo -n "  Testing: $test_name... "

    if $test_func; then
        echo -e "${GREEN}PASS${NC}"
        TESTS_PASSED=$((TESTS_PASSED + 1))
    else
        echo -e "${RED}FAIL${NC}"
        TESTS_FAILED=$((TESTS_FAILED + 1))
    fi
}

# ------------------------------------------------------------------
# Test Cases: AC1 - Schema Definition
# ------------------------------------------------------------------

test_schema_exists() {
    assert_file_exists "$SCHEMA_FILE" "Registry schema should exist"
}

test_schema_has_slug() {
    assert_json_has_field "$SCHEMA_FILE" "slug" "Schema should have slug field"
}

test_schema_has_title() {
    assert_json_has_field "$SCHEMA_FILE" "title" "Schema should have title field"
}

test_schema_has_created_at() {
    assert_json_has_field "$SCHEMA_FILE" "created_at" "Schema should have created_at field"
}

test_schema_has_status() {
    assert_json_has_field "$SCHEMA_FILE" "status" "Schema should have status field"
}

test_schema_has_complexity() {
    assert_json_has_field "$SCHEMA_FILE" "complexity" "Schema should have complexity field"
}

test_schema_has_stories_count() {
    assert_json_has_field "$SCHEMA_FILE" "stories_count" "Schema should have stories_count field"
}

test_schema_has_spec_path() {
    assert_json_has_field "$SCHEMA_FILE" "spec_path" "Schema should have spec_path field"
}

test_schema_has_ralph_path() {
    assert_json_has_field "$SCHEMA_FILE" "ralph_path" "Schema should have ralph_path field"
}

test_schema_has_prd_path() {
    assert_json_has_field "$SCHEMA_FILE" "prd_path" "Schema should have prd_path field"
}

# ------------------------------------------------------------------
# Test Cases: AC2 - Status Enum
# ------------------------------------------------------------------

test_status_ready() {
    assert_contains "$SCHEMA_FILE" "ready" "Status enum should include 'ready'"
}

test_status_running() {
    assert_contains "$SCHEMA_FILE" "running" "Status enum should include 'running'"
}

test_status_completed() {
    assert_contains "$SCHEMA_FILE" "completed" "Status enum should include 'completed'"
}

test_status_paused() {
    assert_contains "$SCHEMA_FILE" "paused" "Status enum should include 'paused'"
}

test_status_failed() {
    assert_contains "$SCHEMA_FILE" "failed" "Status enum should include 'failed'"
}

# ------------------------------------------------------------------
# Test Cases: AC3 - No Duplicates (step-03 logic)
# ------------------------------------------------------------------

test_step_mentions_duplicate_check() {
    assert_contains "$STEP_FILE" "duplicate" "Step should mention duplicate check"
}

test_step_mentions_existing_slug() {
    assert_contains "$STEP_FILE" "slug" "Step should check for existing slug"
}

# ------------------------------------------------------------------
# Test Cases: AC4 - Auto-Creation (step-03 logic)
# ------------------------------------------------------------------

test_step_handles_no_index() {
    assert_contains "$STEP_FILE" "exists" "Step should handle non-existent index"
}

test_step_creates_new_file() {
    assert_contains "$STEP_FILE" "create" "Step should create new file if missing"
}

# ------------------------------------------------------------------
# Main Test Runner
# ------------------------------------------------------------------

main() {
    echo ""
    echo "========================================"
    echo " Ralph Registry Unit Tests"
    echo " (Task-007: Registry index.json)"
    echo "========================================"
    echo ""

    echo "Schema file: $SCHEMA_FILE"
    echo "Step file: $STEP_FILE"
    echo ""

    # AC1: Schema Definition
    echo "AC1 - Schema Definition:"
    run_test "schema exists" test_schema_exists
    run_test "has slug field" test_schema_has_slug
    run_test "has title field" test_schema_has_title
    run_test "has created_at field" test_schema_has_created_at
    run_test "has status field" test_schema_has_status
    run_test "has complexity field" test_schema_has_complexity
    run_test "has stories_count field" test_schema_has_stories_count
    run_test "has spec_path field" test_schema_has_spec_path
    run_test "has ralph_path field" test_schema_has_ralph_path
    run_test "has prd_path field" test_schema_has_prd_path
    echo ""

    # AC2: Status Enum
    echo "AC2 - Status Enum:"
    run_test "status has 'ready'" test_status_ready
    run_test "status has 'running'" test_status_running
    run_test "status has 'completed'" test_status_completed
    run_test "status has 'paused'" test_status_paused
    run_test "status has 'failed'" test_status_failed
    echo ""

    # AC3: No Duplicates
    echo "AC3 - No Duplicates:"
    run_test "mentions duplicate check" test_step_mentions_duplicate_check
    run_test "checks existing slug" test_step_mentions_existing_slug
    echo ""

    # AC4: Auto-Creation
    echo "AC4 - Auto-Creation:"
    run_test "handles non-existent index" test_step_handles_no_index
    run_test "creates new file" test_step_creates_new_file
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
