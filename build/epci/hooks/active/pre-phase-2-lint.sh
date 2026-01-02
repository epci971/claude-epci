#!/bin/bash
# =============================================================================
# Hook: pre-phase-2-lint.sh
# Description: Run linters before the coding phase
# Type: pre-phase-2
#
# Usage:
#   1. Copy or symlink this file to hooks/active/
#   2. Make it executable: chmod +x pre-phase-2-lint.sh
#
# Dependencies:
#   - npm (for JS/TS projects) OR
#   - composer (for PHP projects) OR
#   - python with flake8/black (for Python projects)
# =============================================================================

# Read context from stdin (we don't need it for this hook, but capture it)
read -r CONTEXT

# Detect project type and run appropriate linter
run_linter() {
    # JavaScript/TypeScript project
    if [ -f "package.json" ]; then
        if grep -q '"lint"' package.json 2>/dev/null; then
            echo "Running npm lint..." >&2
            npm run lint --silent 2>&1
            return $?
        fi
    fi

    # PHP/Composer project
    if [ -f "composer.json" ]; then
        if [ -f "vendor/bin/php-cs-fixer" ]; then
            echo "Running PHP CS Fixer..." >&2
            vendor/bin/php-cs-fixer fix --dry-run --diff 2>&1
            return $?
        elif [ -f "vendor/bin/phpcs" ]; then
            echo "Running PHPCS..." >&2
            vendor/bin/phpcs 2>&1
            return $?
        fi
    fi

    # Python project
    if [ -f "requirements.txt" ] || [ -f "pyproject.toml" ]; then
        if command -v flake8 &>/dev/null; then
            echo "Running flake8..." >&2
            flake8 . 2>&1
            return $?
        elif command -v ruff &>/dev/null; then
            echo "Running ruff..." >&2
            ruff check . 2>&1
            return $?
        fi
    fi

    # No linter found
    echo "No linter configured" >&2
    return 0
}

# Execute linter
OUTPUT=$(run_linter)
EXIT_CODE=$?

# Return JSON result
if [ $EXIT_CODE -eq 0 ]; then
    echo '{"status": "success", "message": "Linting passed"}'
else
    # Escape output for JSON
    ESCAPED_OUTPUT=$(echo "$OUTPUT" | head -5 | tr '\n' ' ' | sed 's/"/\\"/g')
    echo "{\"status\": \"warning\", \"message\": \"Linting issues found: ${ESCAPED_OUTPUT}\"}"
fi
