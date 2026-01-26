#!/bin/bash
# Ralph Runner — EPCI v6.0
# Feature: skill-implement v6 Refonte

set -e

FEATURE_ID="skill-implement"
PRD_JSON="docs/specs/skill-implement/skill-implement.prd.json"
PROMPT_FILE=".ralph/skill-implement/PROMPT.md"
MEMORY_FILE=".ralph/skill-implement/MEMORY.md"
BRANCH="feature/skill-implement-v6-refonte"
MAX_ITERATIONS=50

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  Ralph Batch Executor — EPCI v6.0     ${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo "Feature: $FEATURE_ID"
echo "PRD: $PRD_JSON"
echo "Max iterations: $MAX_ITERATIONS"
echo ""

# Pre-flight checks
echo -e "${YELLOW}Pre-flight checks...${NC}"

# Check PRD exists
if [ ! -f "$PRD_JSON" ]; then
    echo -e "${RED}ERROR: PRD file not found: $PRD_JSON${NC}"
    exit 1
fi
echo "  [OK] PRD file exists"

# Check PROMPT exists
if [ ! -f "$PROMPT_FILE" ]; then
    echo -e "${RED}ERROR: PROMPT file not found: $PROMPT_FILE${NC}"
    exit 1
fi
echo "  [OK] PROMPT file exists"

# Check MEMORY exists
if [ ! -f "$MEMORY_FILE" ]; then
    echo -e "${RED}ERROR: MEMORY file not found: $MEMORY_FILE${NC}"
    exit 1
fi
echo "  [OK] MEMORY file exists"

# Check git status
if [ -n "$(git status --porcelain)" ]; then
    echo -e "${YELLOW}WARNING: Uncommitted changes detected${NC}"
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi
echo "  [OK] Git status checked"

# Check or create branch
CURRENT_BRANCH=$(git branch --show-current)
if [ "$CURRENT_BRANCH" != "$BRANCH" ]; then
    echo -e "${YELLOW}Current branch: $CURRENT_BRANCH${NC}"
    echo -e "${YELLOW}Expected branch: $BRANCH${NC}"
    read -p "Create/switch to branch $BRANCH? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        git checkout -B "$BRANCH"
    fi
fi
echo "  [OK] Branch ready"

echo ""
echo -e "${GREEN}Pre-flight complete. Starting execution...${NC}"
echo ""

# Launch Claude Code
claude --print \
    --allowedTools "Read,Write,Edit,Glob,Grep,Bash,Task" \
    --max-turns "$MAX_ITERATIONS" \
    "$(cat <<EOF
Execute the feature implementation defined in:
- PROMPT: $PROMPT_FILE
- MEMORY: $MEMORY_FILE
- PRD: $PRD_JSON

Follow the task order respecting dependencies.
Update MEMORY.md after each task completion.
Run validation after each task.
Commit after each successful task.

Start with task-001.
EOF
)"

# Post-execution
echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  Execution Complete                   ${NC}"
echo -e "${GREEN}========================================${NC}"

# Show final status
echo ""
echo "Final MEMORY status:"
grep -A 10 "## Progress" "$MEMORY_FILE" || true

# Run final validation
echo ""
echo "Running final validation..."
python src/scripts/validate_all.py

echo ""
echo -e "${GREEN}Done.${NC}"
