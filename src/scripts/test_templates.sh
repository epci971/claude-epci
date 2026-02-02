#!/usr/bin/env bash
# test_templates.sh - Unit tests for generation templates
# Tests: variable documentation, placeholder format, structure validation

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

assert_variable_documented() {
    local file="$1"
    local variable="$2"

    # Check if variable exists in file and is documented (mentioned in comments)
    if grep -q "{{$variable}}" "$file" 2>/dev/null; then
        # Variable is used, check if documented
        if grep -qE "(<!--.*$variable|#.*$variable|\$comment.*$variable|Variables:.*$variable)" "$file" 2>/dev/null; then
            return 0
        else
            echo -e "${YELLOW}WARNING${NC}: Variable '$variable' used but not documented in comments"
            return 0  # Non-fatal warning
        fi
    else
        # Variable not used, that's OK
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
# Test Cases: prd.json.template (AC1, AC4)
# ------------------------------------------------------------------

test_prd_template_exists() {
    assert_file_exists "${TEMPLATES_DIR}/prd.json.template" "PRD template should exist"
}

test_prd_template_has_version() {
    assert_contains "${TEMPLATES_DIR}/prd.json.template" '"version": "2.0"' "PRD should have version 2.0"
}

test_prd_template_has_userstories() {
    assert_contains "${TEMPLATES_DIR}/prd.json.template" '"userStories"' "PRD should have userStories array"
}

test_prd_template_has_meta() {
    assert_contains "${TEMPLATES_DIR}/prd.json.template" '"meta"' "PRD should have meta section"
}

test_prd_template_has_config() {
    assert_contains "${TEMPLATES_DIR}/prd.json.template" '"config"' "PRD should have config section"
}

test_prd_template_has_metrics() {
    assert_contains "${TEMPLATES_DIR}/prd.json.template" '"metrics"' "PRD should have metrics section"
}

test_prd_template_documented_variables() {
    # Check that $comment blocks exist for documentation
    assert_contains "${TEMPLATES_DIR}/prd.json.template" '"\$comment"' "PRD should have variable documentation comments"
}

test_prd_template_has_execution() {
    assert_contains "${TEMPLATES_DIR}/prd.json.template" '"execution"' "PRD userStory should have execution section"
}

# ------------------------------------------------------------------
# Test Cases: prompt.md.template (AC2, AC4)
# ------------------------------------------------------------------

test_prompt_template_exists() {
    assert_file_exists "${TEMPLATES_DIR}/prompt.md.template" "PROMPT template should exist"
}

test_prompt_template_has_feature_section() {
    assert_contains "${TEMPLATES_DIR}/prompt.md.template" "## Feature" "PROMPT should have Feature section"
}

test_prompt_template_has_stack_section() {
    assert_contains "${TEMPLATES_DIR}/prompt.md.template" "## Stack" "PROMPT should have Stack section"
}

test_prompt_template_has_execution_rules() {
    assert_contains "${TEMPLATES_DIR}/prompt.md.template" "## Execution Rules" "PROMPT should have Execution Rules section"
}

test_prompt_template_has_tdd_rule() {
    assert_contains "${TEMPLATES_DIR}/prompt.md.template" "TDD" "PROMPT should mention TDD workflow"
}

test_prompt_template_has_documentation_block() {
    assert_contains "${TEMPLATES_DIR}/prompt.md.template" "Variables" "PROMPT should have Variables documentation"
}

test_prompt_template_has_resumption() {
    assert_contains "${TEMPLATES_DIR}/prompt.md.template" "Resumption Protocol" "PROMPT should have Resumption Protocol"
}

# ------------------------------------------------------------------
# Test Cases: memory.md.template (AC3, AC4)
# ------------------------------------------------------------------

test_memory_template_exists() {
    assert_file_exists "${TEMPLATES_DIR}/memory.md.template" "MEMORY template should exist"
}

test_memory_template_has_status() {
    assert_contains "${TEMPLATES_DIR}/memory.md.template" "## Status" "MEMORY should have Status section"
}

test_memory_template_has_progress() {
    assert_contains "${TEMPLATES_DIR}/memory.md.template" "## Progress" "MEMORY should have Progress table"
}

test_memory_template_has_files_modified() {
    assert_contains "${TEMPLATES_DIR}/memory.md.template" "## Files Modified" "MEMORY should have Files Modified table"
}

test_memory_template_has_tests_created() {
    assert_contains "${TEMPLATES_DIR}/memory.md.template" "## Tests Created" "MEMORY should have Tests Created table"
}

test_memory_template_has_issues() {
    assert_contains "${TEMPLATES_DIR}/memory.md.template" "## Issues Encountered" "MEMORY should have Issues table"
}

test_memory_template_has_documentation_block() {
    assert_contains "${TEMPLATES_DIR}/memory.md.template" "Variables:" "MEMORY should have Variables documentation"
}

test_memory_template_has_resumption_checklist() {
    assert_contains "${TEMPLATES_DIR}/memory.md.template" "Resumption Checklist" "MEMORY should have Resumption Checklist"
}

# ------------------------------------------------------------------
# Test Cases: Placeholder Format Consistency (AC4)
# ------------------------------------------------------------------

test_all_placeholders_double_braces() {
    # Check that templates use {{VAR}} format consistently
    local bad_format=0

    for template in "${TEMPLATES_DIR}"/*.template; do
        # Check for single brace patterns that should be double (excluding handlebars helpers)
        if grep -qE '\{[A-Z_]+\}' "$template" 2>/dev/null | grep -v '{{' | grep -v '{#'; then
            echo "Found single-brace placeholder in: $template"
            bad_format=1
        fi
    done

    [[ $bad_format -eq 0 ]]
}

# ------------------------------------------------------------------
# Main Test Runner
# ------------------------------------------------------------------

main() {
    echo ""
    echo "========================================"
    echo " Generation Templates Unit Tests"
    echo "========================================"
    echo ""

    if [[ ! -d "$TEMPLATES_DIR" ]]; then
        echo -e "${RED}ERROR${NC}: Templates directory not found: $TEMPLATES_DIR"
        exit 1
    fi

    echo "Templates directory: $TEMPLATES_DIR"
    echo ""

    # prd.json.template (AC1, AC4)
    echo "PRD Template (AC1, AC4):"
    run_test "template exists" test_prd_template_exists
    run_test "has version 2.0" test_prd_template_has_version
    run_test "has userStories" test_prd_template_has_userstories
    run_test "has meta section" test_prd_template_has_meta
    run_test "has config section" test_prd_template_has_config
    run_test "has metrics section" test_prd_template_has_metrics
    run_test "has execution tracking" test_prd_template_has_execution
    run_test "variables documented" test_prd_template_documented_variables
    echo ""

    # prompt.md.template (AC2, AC4)
    echo "PROMPT Template (AC2, AC4):"
    run_test "template exists" test_prompt_template_exists
    run_test "has Feature section" test_prompt_template_has_feature_section
    run_test "has Stack section" test_prompt_template_has_stack_section
    run_test "has Execution Rules" test_prompt_template_has_execution_rules
    run_test "mentions TDD workflow" test_prompt_template_has_tdd_rule
    run_test "has documentation block" test_prompt_template_has_documentation_block
    run_test "has Resumption Protocol" test_prompt_template_has_resumption
    echo ""

    # memory.md.template (AC3, AC4)
    echo "MEMORY Template (AC3, AC4):"
    run_test "template exists" test_memory_template_exists
    run_test "has Status section" test_memory_template_has_status
    run_test "has Progress table" test_memory_template_has_progress
    run_test "has Files Modified table" test_memory_template_has_files_modified
    run_test "has Tests Created table" test_memory_template_has_tests_created
    run_test "has Issues table" test_memory_template_has_issues
    run_test "has documentation block" test_memory_template_has_documentation_block
    run_test "has Resumption Checklist" test_memory_template_has_resumption_checklist
    echo ""

    # Placeholder format (AC4)
    echo "Placeholder Format Consistency (AC4):"
    run_test "all use {{VAR}} format" test_all_placeholders_double_braces
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
