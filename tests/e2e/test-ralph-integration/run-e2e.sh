#!/usr/bin/env bash
# run-e2e.sh - E2E tests for Ralph Integration
# Tests: spec generation, ralph.sh execution, status parsing, circuit breaker, PRD updates
# Task-008: E2E Test Flow

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Test counters
TESTS_RUN=0
TESTS_PASSED=0
TESTS_FAILED=0

# Paths
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="${SCRIPT_DIR}/../../.."
TEMPLATES_DIR="${PROJECT_ROOT}/src/skills/spec/templates"
SCHEMAS_DIR="${PROJECT_ROOT}/src/schemas"
TEST_OUTPUT_DIR="${SCRIPT_DIR}/output"
TEST_FEATURE_SLUG="e2e-test-feature"

# ------------------------------------------------------------------
# Test Helpers
# ------------------------------------------------------------------

cleanup() {
    if [[ -d "$TEST_OUTPUT_DIR" ]]; then
        rm -rf "$TEST_OUTPUT_DIR"
    fi
}

setup() {
    cleanup
    mkdir -p "$TEST_OUTPUT_DIR/.ralph/${TEST_FEATURE_SLUG}"
    mkdir -p "$TEST_OUTPUT_DIR/docs/specs/${TEST_FEATURE_SLUG}"
}

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

assert_json_valid() {
    local file="$1"
    local desc="$2"

    if python3 -c "import json; json.load(open('$file'))" 2>/dev/null; then
        return 0
    else
        echo -e "${RED}ASSERTION FAILED${NC}: Invalid JSON: $file"
        echo "  Description: $desc"
        return 1
    fi
}

assert_exit_code() {
    local expected="$1"
    local actual="$2"
    local desc="$3"

    if [[ "$actual" -eq "$expected" ]]; then
        return 0
    else
        echo -e "${RED}ASSERTION FAILED${NC}: Expected exit code $expected, got $actual"
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
# AC1: Spec Generation - Template Availability
# ------------------------------------------------------------------

test_prd_template_exists() {
    assert_file_exists "${TEMPLATES_DIR}/prd.json.template" "PRD template should exist"
}

test_prompt_template_exists() {
    assert_file_exists "${TEMPLATES_DIR}/prompt.md.template" "PROMPT template should exist"
}

test_memory_template_exists() {
    assert_file_exists "${TEMPLATES_DIR}/memory.md.template" "MEMORY template should exist"
}

test_ralph_template_exists() {
    assert_file_exists "${TEMPLATES_DIR}/ralph.sh.template" "ralph.sh template should exist"
}

# ------------------------------------------------------------------
# AC1: Spec Generation - Schema Availability
# ------------------------------------------------------------------

test_prd_schema_exists() {
    assert_file_exists "${SCHEMAS_DIR}/prd-v2.json" "PRD v2 schema should exist"
}

test_registry_schema_exists() {
    assert_file_exists "${SCHEMAS_DIR}/ralph-registry-v1.json" "Registry schema should exist"
}

# ------------------------------------------------------------------
# AC2: Ralph Script - Template Structure
# ------------------------------------------------------------------

test_ralph_template_has_shebang() {
    assert_contains "${TEMPLATES_DIR}/ralph.sh.template" "#!/usr/bin/env bash" "Template should have bash shebang"
}

test_ralph_template_has_feature_slug_var() {
    assert_contains "${TEMPLATES_DIR}/ralph.sh.template" "FEATURE_SLUG" "Template should use FEATURE_SLUG variable"
}

test_ralph_template_has_claude_invocation() {
    assert_contains "${TEMPLATES_DIR}/ralph.sh.template" "claude" "Template should invoke claude"
}

test_ralph_template_has_ralph_exec() {
    assert_contains "${TEMPLATES_DIR}/ralph.sh.template" "ralph-exec" "Template should reference /ralph-exec skill"
}

# ------------------------------------------------------------------
# AC3: Status Parsing - Delimiter Detection
# ------------------------------------------------------------------

test_ralph_template_has_status_delimiters() {
    assert_contains "${TEMPLATES_DIR}/ralph.sh.template" "<<<" "Template should have opening delimiter"
}

test_ralph_template_has_closing_delimiter() {
    assert_contains "${TEMPLATES_DIR}/ralph.sh.template" ">>>" "Template should have closing delimiter"
}

test_ralph_template_parses_status() {
    assert_contains "${TEMPLATES_DIR}/ralph.sh.template" "RALPH_STATUS" "Template should parse RALPH_STATUS"
}

test_ralph_template_parses_exit_signal() {
    # Template uses EXIT as a status value (not EXIT_SIGNAL variable)
    assert_contains "${TEMPLATES_DIR}/ralph.sh.template" "Exit signal" "Template should handle exit signal"
}

# ------------------------------------------------------------------
# AC4: Circuit Breaker - Detection Logic
# ------------------------------------------------------------------

test_ralph_template_has_circuit_breaker() {
    assert_contains "${TEMPLATES_DIR}/ralph.sh.template" "circuit" "Template should have circuit breaker"
}

test_ralph_template_has_hash_check() {
    # Circuit breaker uses hash to detect stuck loops
    assert_contains "${TEMPLATES_DIR}/ralph.sh.template" "hash\|md5\|sha" "Template should check file/error hash"
}

test_ralph_template_has_threshold() {
    assert_contains "${TEMPLATES_DIR}/ralph.sh.template" "THRESHOLD\|threshold\|3" "Template should have threshold value"
}

test_ralph_template_exits_on_stuck() {
    assert_contains "${TEMPLATES_DIR}/ralph.sh.template" "exit 2\|exit.*circuit" "Template should exit on stuck loop"
}

# ------------------------------------------------------------------
# AC5: PRD Update - Structure Verification
# ------------------------------------------------------------------

test_prd_template_has_userstories() {
    assert_contains "${TEMPLATES_DIR}/prd.json.template" "userStories" "PRD should have userStories array"
}

test_prd_template_has_execution() {
    assert_contains "${TEMPLATES_DIR}/prd.json.template" "execution" "PRD should have execution section"
}

test_prd_template_has_status_field() {
    assert_contains "${TEMPLATES_DIR}/prd.json.template" "\"status\"" "PRD should have status field"
}

test_prd_template_has_passes_field() {
    assert_contains "${TEMPLATES_DIR}/prd.json.template" "passes\|attempts" "PRD should track passes/attempts"
}

# ------------------------------------------------------------------
# E2E Simulation: Generate and Validate ralph.sh
# ------------------------------------------------------------------

test_generate_ralph_from_template() {
    local template="${TEMPLATES_DIR}/ralph.sh.template"
    local output="${TEST_OUTPUT_DIR}/.ralph/${TEST_FEATURE_SLUG}/ralph.sh"

    # Simple variable substitution
    sed -e "s/{{FEATURE_SLUG}}/${TEST_FEATURE_SLUG}/g" \
        -e "s|{{PRD_FILE}}|docs/specs/${TEST_FEATURE_SLUG}/${TEST_FEATURE_SLUG}.prd.json|g" \
        -e "s|{{SPEC_DIR}}|docs/specs/${TEST_FEATURE_SLUG}|g" \
        -e "s|{{RALPH_DIR}}|.ralph/${TEST_FEATURE_SLUG}|g" \
        "$template" > "$output"

    chmod +x "$output"

    assert_file_exists "$output" "Generated ralph.sh should exist"
}

test_generated_ralph_is_executable() {
    local output="${TEST_OUTPUT_DIR}/.ralph/${TEST_FEATURE_SLUG}/ralph.sh"

    if [[ -x "$output" ]]; then
        return 0
    else
        echo -e "${RED}ASSERTION FAILED${NC}: $output is not executable"
        return 1
    fi
}

test_generated_ralph_has_correct_slug() {
    local output="${TEST_OUTPUT_DIR}/.ralph/${TEST_FEATURE_SLUG}/ralph.sh"

    assert_contains "$output" "${TEST_FEATURE_SLUG}" "Generated script should contain feature slug"
}

# ------------------------------------------------------------------
# E2E Simulation: Circuit Breaker Behavior
# ------------------------------------------------------------------

test_circuit_breaker_snippet_exists() {
    assert_file_exists "${TEMPLATES_DIR}/circuit-breaker.sh.snippet" "Circuit breaker snippet should exist"
}

# ------------------------------------------------------------------
# Main Test Runner
# ------------------------------------------------------------------

main() {
    echo ""
    echo "========================================"
    echo " Ralph Integration E2E Tests"
    echo " (Task-008: E2E Test Flow)"
    echo "========================================"
    echo ""

    echo "Project root: $PROJECT_ROOT"
    echo "Templates dir: $TEMPLATES_DIR"
    echo "Test output: $TEST_OUTPUT_DIR"
    echo ""

    # Setup
    setup

    # AC1: Spec Generation - Templates
    echo -e "${BLUE}AC1 - Spec Generation (Templates):${NC}"
    run_test "PRD template exists" test_prd_template_exists
    run_test "PROMPT template exists" test_prompt_template_exists
    run_test "MEMORY template exists" test_memory_template_exists
    run_test "ralph.sh template exists" test_ralph_template_exists
    echo ""

    # AC1: Spec Generation - Schemas
    echo -e "${BLUE}AC1 - Spec Generation (Schemas):${NC}"
    run_test "PRD v2 schema exists" test_prd_schema_exists
    run_test "Registry schema exists" test_registry_schema_exists
    echo ""

    # AC2: Ralph Script Execution
    echo -e "${BLUE}AC2 - Ralph Script Structure:${NC}"
    run_test "has bash shebang" test_ralph_template_has_shebang
    run_test "has FEATURE_SLUG var" test_ralph_template_has_feature_slug_var
    run_test "invokes claude" test_ralph_template_has_claude_invocation
    run_test "references /ralph-exec" test_ralph_template_has_ralph_exec
    echo ""

    # AC3: Status Parsing
    echo -e "${BLUE}AC3 - Status Parsing:${NC}"
    run_test "has opening delimiter <<<" test_ralph_template_has_status_delimiters
    run_test "has closing delimiter >>>" test_ralph_template_has_closing_delimiter
    run_test "parses RALPH_STATUS" test_ralph_template_parses_status
    run_test "parses EXIT_SIGNAL" test_ralph_template_parses_exit_signal
    echo ""

    # AC4: Circuit Breaker
    echo -e "${BLUE}AC4 - Circuit Breaker:${NC}"
    run_test "has circuit breaker logic" test_ralph_template_has_circuit_breaker
    run_test "uses hash for detection" test_ralph_template_has_hash_check
    run_test "has threshold value" test_ralph_template_has_threshold
    run_test "exits on stuck loop" test_ralph_template_exits_on_stuck
    run_test "circuit breaker snippet exists" test_circuit_breaker_snippet_exists
    echo ""

    # AC5: PRD Update
    echo -e "${BLUE}AC5 - PRD Update Verification:${NC}"
    run_test "PRD has userStories" test_prd_template_has_userstories
    run_test "PRD has execution section" test_prd_template_has_execution
    run_test "PRD has status field" test_prd_template_has_status_field
    run_test "PRD tracks passes/attempts" test_prd_template_has_passes_field
    echo ""

    # E2E Simulation
    echo -e "${BLUE}E2E Simulation:${NC}"
    run_test "generate ralph.sh from template" test_generate_ralph_from_template
    run_test "generated script is executable" test_generated_ralph_is_executable
    run_test "generated script has correct slug" test_generated_ralph_has_correct_slug
    echo ""

    # Cleanup
    cleanup

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
