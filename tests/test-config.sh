#!/bin/bash
# tests/test-config.sh — Unit tests for lib/config.sh
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
if [[ ! -f "$PROJECT_ROOT/lib/config.sh" ]]; then
    echo "ERROR: lib/config.sh not found"
    exit 1
fi
source "$PROJECT_ROOT/lib/config.sh"

# Temp dir for test artifacts
TEST_TMP="$(mktemp -d)"
trap 'rm -rf "$TEST_TMP"' EXIT

# Suppress log output during tests
export LOG_DIR="$TEST_TMP"

# === Test Data ===

create_valid_env() {
    cat > "$TEST_TMP/.env" << 'EOF'
NOTION_API_KEY=secret_test123
GITHUB_TOKEN=ghp_test456
TELEGRAM_BOT_TOKEN=123456789:TESTTOKEN
TELEGRAM_CHAT_ID=-100123456
EOF
}

create_incomplete_env() {
    cat > "$TEST_TMP/.env" << 'EOF'
NOTION_API_KEY=secret_test123
EOF
}

create_valid_projects_json() {
    cat > "$TEST_TMP/projects.json" << 'EOF'
{
  "version": "1.0",
  "projects": [
    {
      "slug": "gardel",
      "directory": "/home/pipeline/apps/gardel",
      "github_repo": "epci971/gardel",
      "notion_project_id": "abc-123-def",
      "defaults": {
        "model": "sonnet",
        "timeout": 1800,
        "flags": ["validate_plan"]
      }
    },
    {
      "slug": "maison-bois",
      "directory": "/home/pipeline/apps/maison-bois",
      "github_repo": "epci971/maison-bois",
      "notion_project_id": "xyz-789-uvw",
      "defaults": {
        "model": "haiku",
        "timeout": 900,
        "flags": []
      }
    }
  ]
}
EOF
}

create_invalid_projects_json() {
    echo "not valid json {{{" > "$TEST_TMP/projects.json"
}

create_missing_fields_projects_json() {
    cat > "$TEST_TMP/projects.json" << 'EOF'
{
  "version": "1.0",
  "projects": [
    {
      "slug": "incomplete",
      "directory": "/home/pipeline/apps/incomplete"
    }
  ]
}
EOF
}

# === Test Cases ===

test_load_env_exports_variables() {
    create_valid_env
    # Run in subshell to avoid polluting test env
    local result
    result=$(
        load_env "$TEST_TMP/.env" 2>/dev/null
        echo "NOTION=$NOTION_API_KEY|GITHUB=$GITHUB_TOKEN|TELEGRAM=$TELEGRAM_BOT_TOKEN|CHAT=$TELEGRAM_CHAT_ID"
    )
    if echo "$result" | grep -q "NOTION=secret_test123"; then
        pass
    else
        fail "Expected NOTION_API_KEY to be exported, got: $result"
    fi
}

test_load_env_fails_on_missing_variable() {
    create_incomplete_env
    local exit_code=0
    load_env "$TEST_TMP/.env" >/dev/null 2>&1 && exit_code=0 || exit_code=$?
    if [[ $exit_code -ne 0 ]]; then
        pass
    else
        fail "Expected load_env to fail on missing required variables"
    fi
}

test_load_env_fails_on_missing_file() {
    local exit_code=0
    load_env "$TEST_TMP/nonexistent.env" >/dev/null 2>&1 && exit_code=0 || exit_code=$?
    if [[ $exit_code -ne 0 ]]; then
        pass
    else
        fail "Expected load_env to fail on missing .env file"
    fi
}

test_load_projects_validates_valid_json() {
    create_valid_projects_json
    local exit_code=0
    load_projects "$TEST_TMP/projects.json" >/dev/null 2>&1 && exit_code=0 || exit_code=$?
    if [[ $exit_code -eq 0 ]]; then
        pass
    else
        fail "Expected load_projects to succeed with valid JSON"
    fi
}

test_load_projects_rejects_invalid_json() {
    create_invalid_projects_json
    local exit_code=0
    load_projects "$TEST_TMP/projects.json" >/dev/null 2>&1 && exit_code=0 || exit_code=$?
    if [[ $exit_code -ne 0 ]]; then
        pass
    else
        fail "Expected load_projects to reject invalid JSON"
    fi
}

test_load_projects_rejects_missing_fields() {
    create_missing_fields_projects_json
    local exit_code=0
    load_projects "$TEST_TMP/projects.json" >/dev/null 2>&1 && exit_code=0 || exit_code=$?
    if [[ $exit_code -ne 0 ]]; then
        pass
    else
        fail "Expected load_projects to reject entries with missing required fields"
    fi
}

test_get_project_config_returns_correct_project() {
    create_valid_projects_json
    load_projects "$TEST_TMP/projects.json" >/dev/null 2>&1
    local result
    result=$(get_project_config "gardel" 2>/dev/null)
    if echo "$result" | jq -e '.slug == "gardel"' >/dev/null 2>&1; then
        pass
    else
        fail "Expected project config for 'gardel', got: $result"
    fi
}

test_get_project_config_returns_all_fields() {
    create_valid_projects_json
    load_projects "$TEST_TMP/projects.json" >/dev/null 2>&1
    local result
    result=$(get_project_config "gardel" 2>/dev/null)
    local has_dir has_repo has_notion
    has_dir=$(echo "$result" | jq -e '.directory' 2>/dev/null)
    has_repo=$(echo "$result" | jq -e '.github_repo' 2>/dev/null)
    has_notion=$(echo "$result" | jq -e '.notion_project_id' 2>/dev/null)
    if [[ -n "$has_dir" && -n "$has_repo" && -n "$has_notion" ]]; then
        pass
    else
        fail "Expected all fields in config, got: $result"
    fi
}

test_get_project_config_fails_for_unknown_slug() {
    create_valid_projects_json
    load_projects "$TEST_TMP/projects.json" >/dev/null 2>&1
    local exit_code=0
    get_project_config "nonexistent" >/dev/null 2>&1 && exit_code=0 || exit_code=$?
    if [[ $exit_code -ne 0 ]]; then
        pass
    else
        fail "Expected get_project_config to fail for unknown slug"
    fi
}

# === Run Tests ===
echo "=== tests/test-config.sh ==="
echo ""

run_test "load_env exports variables" test_load_env_exports_variables
run_test "load_env fails on missing variable" test_load_env_fails_on_missing_variable
run_test "load_env fails on missing file" test_load_env_fails_on_missing_file
run_test "load_projects validates valid JSON" test_load_projects_validates_valid_json
run_test "load_projects rejects invalid JSON" test_load_projects_rejects_invalid_json
run_test "load_projects rejects missing fields" test_load_projects_rejects_missing_fields
run_test "get_project_config returns correct project" test_get_project_config_returns_correct_project
run_test "get_project_config returns all fields" test_get_project_config_returns_all_fields
run_test "get_project_config fails for unknown slug" test_get_project_config_fails_for_unknown_slug

# === Summary ===
echo ""
echo "Results: $TESTS_PASSED passed, $TESTS_FAILED failed out of $TESTS_TOTAL"
echo ""

if [[ $TESTS_FAILED -gt 0 ]]; then
    exit 1
fi
exit 0
