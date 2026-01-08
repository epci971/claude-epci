---
allowed-tools: []
description: "Simple greeting command"
category: "Examples"
---

# /hello:world - Simple Greeting

## Purpose
Demonstrate a minimal Claude Code plugin command with basic functionality.

## Usage
```bash
/hello:world [name]
```

## Arguments
- `[name]` - Name to greet (optional, defaults to "World")

## Examples

```bash
# Basic greeting
/hello:world
# Output: Hello, World!

# Personalized greeting
/hello:world Alice
# Output: Hello, Alice!

# Multiple names
/hello:world Alice Bob Charlie
# Output: Hello, Alice, Bob, and Charlie!
```

## Implementation

This command demonstrates:
- Simple argument parsing
- Optional parameters with defaults
- Basic string concatenation
- Clean output formatting

## Related Commands
- None (standalone example)

## Notes
This is a minimal example to demonstrate plugin structure. Real plugins would typically:
- Use Claude Code tools (Read, Write, Bash, etc.)
- Integrate with MCP servers
- Activate AI personas
- Implement complex workflows
