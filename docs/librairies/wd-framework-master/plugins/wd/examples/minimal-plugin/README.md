# Hello Plugin - Minimal Example

This is a minimal Claude Code plugin example to demonstrate the basic structure and requirements.

## What's Included

- `.claude-plugin/marketplace.json` - Plugin configuration
- `commands/hello.md` - Single greeting command
- `README.md` - This file

## Installation

```bash
# Clone or download this example
cd examples/minimal-plugin

# Initialize git repository
git init
git add .
git commit -m "Initial commit"

# Push to GitHub
git remote add origin https://github.com/yourusername/hello-plugin.git
git push -u origin main

# Install in Claude Code
/plugin marketplace add yourusername/hello-plugin
```

## Usage

```bash
/hello:world
# Output: Hello, World!

/hello:world Alice
# Output: Hello, Alice!
```

## Structure

```
hello-plugin/
├── .claude-plugin/
│   └── marketplace.json    # Plugin metadata
├── commands/
│   └── hello.md           # Greeting command
└── README.md              # Documentation
```

## Key Concepts

### marketplace.json
Defines plugin metadata, components, and installation profiles.

### Command File (hello.md)
- YAML frontmatter with `allowed-tools` and `description`
- Markdown body with usage, examples, and documentation

### Minimal Requirements
- `.claude-plugin/marketplace.json` - Required
- At least one component (command, agent, hook, or MCP config)
- `README.md` - Recommended
- `LICENSE` - Recommended

## Next Steps

To create a more advanced plugin:
1. Add more commands in `commands/` directory
2. Create agents in `agents/` directory
3. Add MCP server configs in `mcp/` directory
4. Define hooks in `hooks/` directory

See the [Plugin Development Guide](../../PLUGIN_DEVELOPMENT.md) for details.

## License

MIT
