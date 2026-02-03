#!/usr/bin/env bash
# test_step03_generate.sh - Unit tests for step-03-generate-ralph.md updates
# Tests: template references, PRD generation, circuit breaker, registry
# Task-006: Update /spec step-03

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
STEP_FILE="${SCRIPT_DIR}/../skills/spec/steps/step-03-generate-ralph.md"
TEMPLATES_DIR="${SCRIPT_DIR}/../skills/spec/templates"

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

assert_not_contains() {
    local file="$1"
    local needle="$2"
    local desc="$3"

    if grep -q "$needle" "$file" 2>/dev/null; then
        echo -e "${RED}ASSERTION FAILED${NC}: '$file' should not contain '$needle'"
        echo "  Description: $desc"
        return 1
    else
        return 0
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
# Test Cases: AC1 - PRD.json Generation
# ------------------------------------------------------------------

test_step_references_prd_template() {
    assert_contains "$STEP_FILE" "prd.json.template" "Step should reference prd.json.template"
}

test_step_prd_location_correct() {
    assert_contains "$STEP_FILE" "docs/specs/{" "PRD should go to docs/specs/{slug}/"
}

test_step_prd_filename_format() {
    assert_contains "$STEP_FILE" ".prd.json" "PRD filename should end with .prd.json"
}

test_step_mentions_userstories() {
    assert_contains "$STEP_FILE" "userStories" "Step should mention userStories format"
}

# ------------------------------------------------------------------
# Test Cases: AC2 - PROMPT.md Generation
# ------------------------------------------------------------------

test_step_references_prompt_template() {
    assert_contains "$STEP_FILE" "prompt.md.template" "Step should reference prompt.md.template"
}

test_step_prompt_location_correct() {
    assert_contains "$STEP_FILE" ".ralph/{" "PROMPT should go to .ralph/{slug}/"
}

test_step_prompt_stack_detection() {
    assert_contains "$STEP_FILE" "STACK_FRAMEWORK" "Step should mention stack framework variable"
}

# ------------------------------------------------------------------
# Test Cases: AC3 - MEMORY.md Generation
# ------------------------------------------------------------------

test_step_references_memory_template() {
    assert_contains "$STEP_FILE" "memory.md.template" "Step should reference memory.md.template"
}

test_step_memory_has_task_initialization() {
    assert_contains "$STEP_FILE" "pending" "Step should initialize tasks as pending"
}

# ------------------------------------------------------------------
# Test Cases: AC4 - ralph.sh Generation
# ------------------------------------------------------------------

test_step_references_ralph_template() {
    assert_contains "$STEP_FILE" "ralph.sh.template" "Step should reference ralph.sh.template"
}

test_step_mentions_circuit_breaker() {
    assert_contains "$STEP_FILE" "circuit" "Step should mention circuit breaker"
}

test_step_makes_executable() {
    assert_contains "$STEP_FILE" "chmod" "Step should make ralph.sh executable"
}

test_step_no_hardcoded_ralph_script() {
    # Verify the old inline script pattern is replaced by template reference
    # Check that "Launch Claude Code" is no longer hardcoded in ralph.sh section
    ! grep -q "Launch Claude Code" "$STEP_FILE" 2>/dev/null
}

# ------------------------------------------------------------------
# Test Cases: AC5 - Registry Update
# ------------------------------------------------------------------

test_step_updates_registry() {
    assert_contains "$STEP_FILE" "index.json" "Step should update .ralph/index.json"
}

test_step_registry_has_prd_path() {
    assert_contains "$STEP_FILE" "prd_path" "Registry entry should include prd_path"
}

# ------------------------------------------------------------------
# Test Cases: AC6 - Final Breakpoint
# ------------------------------------------------------------------

test_step_has_breakpoint() {
    assert_contains "$STEP_FILE" "BREAKPOINT" "Step should have final breakpoint"
}

test_step_has_routing_recommendation() {
    assert_contains "$STEP_FILE" "Recommended" "Breakpoint should show routing recommendation"
}

test_step_shows_execution_command() {
    assert_contains "$STEP_FILE" "ralph.sh" "Breakpoint should show execution command"
}

# ------------------------------------------------------------------
# Test Cases: Template Existence (dependencies from task-005)
# ------------------------------------------------------------------

test_prd_template_exists() {
    assert_file_exists "${TEMPLATES_DIR}/prd.json.template" "prd.json.template should exist"
}

test_prompt_template_exists() {
    assert_file_exists "${TEMPLATES_DIR}/prompt.md.template" "prompt.md.template should exist"
}

test_memory_template_exists() {
    assert_file_exists "${TEMPLATES_DIR}/memory.md.template" "memory.md.template should exist"
}

test_ralph_template_exists() {
    assert_file_exists "${TEMPLATES_DIR}/ralph.sh.template" "ralph.sh.template should exist"
}

# ------------------------------------------------------------------
# Main Test Runner
# ------------------------------------------------------------------

main() {
    echo ""
    echo "========================================"
    echo " Step-03 Generate Ralph Unit Tests"
    echo " (Task-006: Update /spec step-03)"
    echo "========================================"
    echo ""

    if [[ ! -f "$STEP_FILE" ]]; then
        echo -e "${RED}ERROR${NC}: Step file not found: $STEP_FILE"
        exit 1
    fi

    echo "Step file: $STEP_FILE"
    echo "Templates dir: $TEMPLATES_DIR"
    echo ""

    # Template dependencies (from task-005)
    echo "Template Dependencies:"
    run_test "prd.json.template exists" test_prd_template_exists
    run_test "prompt.md.template exists" test_prompt_template_exists
    run_test "memory.md.template exists" test_memory_template_exists
    run_test "ralph.sh.template exists" test_ralph_template_exists
    echo ""

    # AC1: PRD.json Generation
    echo "AC1 - PRD.json Generation:"
    run_test "references prd.json.template" test_step_references_prd_template
    run_test "PRD location in docs/specs/" test_step_prd_location_correct
    run_test "PRD filename format" test_step_prd_filename_format
    run_test "mentions userStories format" test_step_mentions_userstories
    echo ""

    # AC2: PROMPT.md Generation
    echo "AC2 - PROMPT.md Generation:"
    run_test "references prompt.md.template" test_step_references_prompt_template
    run_test "PROMPT location in .ralph/" test_step_prompt_location_correct
    run_test "stack detection variables" test_step_prompt_stack_detection
    echo ""

    # AC3: MEMORY.md Generation
    echo "AC3 - MEMORY.md Generation:"
    run_test "references memory.md.template" test_step_references_memory_template
    run_test "initializes tasks as pending" test_step_memory_has_task_initialization
    echo ""

    # AC4: ralph.sh Generation
    echo "AC4 - ralph.sh Generation:"
    run_test "references ralph.sh.template" test_step_references_ralph_template
    run_test "mentions circuit breaker" test_step_mentions_circuit_breaker
    run_test "makes script executable" test_step_makes_executable
    run_test "no hardcoded script (uses template)" test_step_no_hardcoded_ralph_script
    echo ""

    # AC5: Registry Update
    echo "AC5 - Registry Update:"
    run_test "updates index.json" test_step_updates_registry
    run_test "registry has prd_path" test_step_registry_has_prd_path
    echo ""

    # AC6: Final Breakpoint
    echo "AC6 - Final Breakpoint:"
    run_test "has breakpoint" test_step_has_breakpoint
    run_test "shows routing recommendation" test_step_has_routing_recommendation
    run_test "shows execution command" test_step_shows_execution_command
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
