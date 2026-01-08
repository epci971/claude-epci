#!/bin/bash

# GoDev Framework Plugin Validation Script
# Validates plugin structure before installation

set -e

PLUGIN_DIR="/Users/adev/Documents/GoDev_Framework/godev-framework-plugin"
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "🔍 GoDev Framework Plugin Validation"
echo "======================================"
echo ""

# Check plugin.json
echo "1. Validating plugin.json..."
if [ -f "$PLUGIN_DIR/.claude-plugin/plugin.json" ]; then
    if jq empty "$PLUGIN_DIR/.claude-plugin/plugin.json" 2>/dev/null; then
        echo -e "${GREEN}✅ plugin.json is valid JSON${NC}"

        # Check required fields
        NAME=$(jq -r '.name' "$PLUGIN_DIR/.claude-plugin/plugin.json")
        VERSION=$(jq -r '.version' "$PLUGIN_DIR/.claude-plugin/plugin.json")
        DESC=$(jq -r '.description' "$PLUGIN_DIR/.claude-plugin/plugin.json")

        echo "   Name: $NAME"
        echo "   Version: $VERSION"
        echo "   Description: ${DESC:0:60}..."
    else
        echo -e "${RED}❌ plugin.json is invalid JSON${NC}"
        exit 1
    fi
else
    echo -e "${RED}❌ plugin.json not found${NC}"
    exit 1
fi
echo ""

# Check marketplace.json
echo "2. Validating marketplace.json..."
if [ -f "$PLUGIN_DIR/.claude-plugin/marketplace.json" ]; then
    if jq empty "$PLUGIN_DIR/.claude-plugin/marketplace.json" 2>/dev/null; then
        echo -e "${GREEN}✅ marketplace.json is valid JSON${NC}"

        # Check required fields
        MARKET_NAME=$(jq -r '.name' "$PLUGIN_DIR/.claude-plugin/marketplace.json")
        OWNER_NAME=$(jq -r '.owner.name' "$PLUGIN_DIR/.claude-plugin/marketplace.json")
        PLUGINS_COUNT=$(jq '.plugins | length' "$PLUGIN_DIR/.claude-plugin/marketplace.json")

        echo "   Marketplace: $MARKET_NAME"
        echo "   Owner: $OWNER_NAME"
        echo "   Plugins: $PLUGINS_COUNT"

        # Validate plugins array
        if [ "$PLUGINS_COUNT" -eq 0 ]; then
            echo -e "${RED}❌ No plugins defined in marketplace.json${NC}"
            exit 1
        fi
    else
        echo -e "${RED}❌ marketplace.json is invalid JSON${NC}"
        exit 1
    fi
else
    echo -e "${RED}❌ marketplace.json not found${NC}"
    exit 1
fi
echo ""

# Check commands directory
echo "3. Validating commands..."
if [ -d "$PLUGIN_DIR/commands" ]; then
    CMD_COUNT=$(find "$PLUGIN_DIR/commands" -name "*.md" -type f | wc -l | tr -d ' ')
    echo -e "${GREEN}✅ Found $CMD_COUNT command files${NC}"

    # List command files
    echo "   Commands:"
    find "$PLUGIN_DIR/commands" -name "*.md" -type f -exec basename {} \; | sed 's/^/     - /'

    # Check for frontmatter in first command
    FIRST_CMD=$(find "$PLUGIN_DIR/commands" -name "*.md" -type f | head -1)
    if head -1 "$FIRST_CMD" | grep -q "^---"; then
        echo -e "${GREEN}✅ Commands have YAML frontmatter${NC}"
    else
        echo -e "${RED}❌ Commands missing YAML frontmatter${NC}"
        exit 1
    fi
else
    echo -e "${RED}❌ commands/ directory not found${NC}"
    exit 1
fi
echo ""

# Check agents directory
echo "4. Validating agents..."
if [ -d "$PLUGIN_DIR/agents" ]; then
    AGENT_COUNT=$(find "$PLUGIN_DIR/agents" -name "*.md" -type f | wc -l | tr -d ' ')
    echo -e "${GREEN}✅ Found $AGENT_COUNT agent files${NC}"

    # List agent files
    echo "   Agents:"
    find "$PLUGIN_DIR/agents" -name "*.md" -type f -exec basename {} \; | sed 's/^/     - /'

    # Check for frontmatter in first agent
    FIRST_AGENT=$(find "$PLUGIN_DIR/agents" -name "*.md" -type f | head -1)
    if head -1 "$FIRST_AGENT" | grep -q "^---"; then
        echo -e "${GREEN}✅ Agents have YAML frontmatter${NC}"
    else
        echo -e "${RED}❌ Agents missing YAML frontmatter${NC}"
        exit 1
    fi
else
    echo -e "${RED}❌ agents/ directory not found${NC}"
    exit 1
fi
echo ""

# Check .claude directory
echo "5. Validating .claude core files..."
if [ -d "$PLUGIN_DIR/.claude" ]; then
    CORE_COUNT=$(find "$PLUGIN_DIR/.claude" -name "*.md" -type f | wc -l | tr -d ' ')
    echo -e "${GREEN}✅ Found $CORE_COUNT core files${NC}"

    # Check for CLAUDE.md entry point
    if [ -f "$PLUGIN_DIR/.claude/CLAUDE.md" ]; then
        echo -e "${GREEN}✅ CLAUDE.md entry point found${NC}"
    else
        echo -e "${YELLOW}⚠️  CLAUDE.md entry point not found${NC}"
    fi
else
    echo -e "${YELLOW}⚠️  .claude/ directory not found (optional)${NC}"
fi
echo ""

# Summary
echo "======================================"
echo -e "${GREEN}✅ Plugin validation completed successfully!${NC}"
echo ""
echo "Plugin ready for installation:"
echo "  /plugin marketplace add $PLUGIN_DIR"
echo ""
