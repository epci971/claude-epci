#!/bin/bash
# EPCI Plugin Pre-Commit Hook
#
# This hook runs validation checks before each commit.
# Install: cp src/hooks/examples/pre-commit-validate.sh .git/hooks/pre-commit && chmod +x .git/hooks/pre-commit
#
# Options:
#   - Fast mode (default): Only critical validations
#   - Full mode: All validations including slow ones
#
# To skip: git commit --no-verify

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${YELLOW}  EPCI Pre-Commit Validation${NC}"
echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

# Find project root
PROJECT_ROOT=$(git rev-parse --show-toplevel 2>/dev/null)
if [ -z "$PROJECT_ROOT" ]; then
    echo -e "${RED}Error: Not in a git repository${NC}"
    exit 1
fi

cd "$PROJECT_ROOT"

# Check if validate_all.py exists
VALIDATE_SCRIPT="src/scripts/validate_all.py"
if [ ! -f "$VALIDATE_SCRIPT" ]; then
    echo -e "${YELLOW}Warning: $VALIDATE_SCRIPT not found${NC}"
    echo -e "${YELLOW}Skipping validation (commit allowed)${NC}"
    exit 0
fi

# Check if any src/ files are staged
STAGED_SRC=$(git diff --cached --name-only --diff-filter=ACMR -- 'src/**' 2>/dev/null | wc -l)
if [ "$STAGED_SRC" -eq 0 ]; then
    echo -e "${GREEN}No src/ files staged, skipping validation${NC}"
    exit 0
fi

echo -e "\nStaged files in src/: $STAGED_SRC"
echo ""

# Run validation in fast mode (critical checks only)
# Use --fast to skip slow validations (triggering, breakpoints, markdown refs)
echo -e "Running validations..."
echo ""

if python3 "$VALIDATE_SCRIPT" --fast; then
    echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${GREEN}  ✅ All validations passed!${NC}"
    echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    exit 0
else
    echo -e "${RED}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${RED}  ❌ Validation failed!${NC}"
    echo -e "${RED}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
    echo -e "${YELLOW}To fix automatically (when possible):${NC}"
    echo -e "  python3 $VALIDATE_SCRIPT --fix"
    echo ""
    echo -e "${YELLOW}To bypass this check (use sparingly):${NC}"
    echo -e "  git commit --no-verify"
    echo ""
    exit 1
fi
