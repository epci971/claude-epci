# EPCI Hooks System

> **Version**: 1.0.0 (EPCI v3.1)
> **Date**: 2025-12-15

## Overview

The EPCI Hooks System allows you to execute custom scripts at specific points in the EPCI workflow. This enables:

- Running linters before coding
- Sending notifications when features complete
- Collecting metrics at breakpoints
- Integrating with external tools (CI/CD, issue trackers, etc.)

## Quick Start

### 1. Create a Hook

Create a script in the `examples/` directory or directly in `active/`:

```bash
# hooks/active/pre-phase-2-lint.sh
#!/bin/bash
echo '{"status": "success", "message": "Linting passed"}'
```

### 2. Make it Executable

```bash
chmod +x hooks/active/pre-phase-2-lint.sh
```

### 3. Run the EPCI Workflow

Hooks in `active/` are executed automatically at their respective trigger points.

---

## Hook Types

| Hook Type | Trigger Point | Use Case |
|-----------|--------------|----------|
| `pre-phase-1` | Before Phase 1 starts | Load context, check prerequisites |
| `post-phase-1` | After plan validation | Notify team, create tickets |
| `pre-phase-2` | Before coding starts | Run linters, setup environment |
| `post-phase-2` | After code review | Additional tests, coverage checks |
| `pre-phase-3` | Before finalization | Verify all tests pass |
| `post-phase-3` | After completion | Deploy, notify, collect metrics |
| `on-breakpoint` | At each breakpoint | Logging, metrics collection |

---

## Directory Structure

```
hooks/
├── README.md           # This file
├── runner.py           # Hook execution engine
├── examples/           # Example hooks (templates)
│   ├── pre-phase-2-lint.sh
│   ├── post-phase-3-notify.py
│   └── on-breakpoint-log.sh
└── active/             # Active hooks (executed automatically)
    └── .gitkeep
```

**Active hooks** are discovered from `hooks/active/` based on their filename prefix.

---

## Hook Naming Convention

Hooks are discovered by matching the filename prefix to the hook type:

```
{hook-type}[-optional-name].{extension}
```

**Examples:**
- `pre-phase-2.sh` → runs at `pre-phase-2`
- `pre-phase-2-lint.sh` → runs at `pre-phase-2`
- `post-phase-3-notify.py` → runs at `post-phase-3`
- `on-breakpoint-log.sh` → runs at `on-breakpoint`

Multiple hooks of the same type are executed in alphabetical order.

---

## Writing Hooks

### Supported Languages

| Language | Extension | Shebang |
|----------|-----------|---------|
| Bash | `.sh` | `#!/bin/bash` |
| Python | `.py` | `#!/usr/bin/env python3` |
| Node.js | `.js` | `#!/usr/bin/env node` |

### Input: Context via stdin

Hooks receive a JSON context object via **stdin**:

```json
{
  "phase": "phase-2",
  "hook_type": "pre-phase-2",
  "feature_slug": "user-authentication",
  "files_modified": ["src/auth.py", "tests/test_auth.py"],
  "test_results": {},
  "breakpoint_type": "",
  "timestamp": "2025-12-15T10:30:00Z"
}
```

### Output: JSON Result

Hooks should output a JSON object to **stdout**:

```json
{
  "status": "success",
  "message": "Hook completed successfully"
}
```

**Status values:**
- `success` — Hook passed, workflow continues
- `warning` — Hook had issues but workflow continues
- `error` — Hook failed (behavior depends on `fail_on_error` setting)

### Minimal Examples

**Bash:**
```bash
#!/bin/bash
CONTEXT=$(cat)
echo '{"status": "success", "message": "Hook executed"}'
```

**Python:**
```python
#!/usr/bin/env python3
import sys, json
context = json.loads(sys.stdin.read())
print(json.dumps({"status": "success", "message": f"Phase: {context['phase']}"}))
```

**Node.js:**
```javascript
#!/usr/bin/env node
let data = '';
process.stdin.on('data', chunk => data += chunk);
process.stdin.on('end', () => {
  const context = JSON.parse(data);
  console.log(JSON.stringify({status: 'success', message: `Phase: ${context.phase}`}));
});
```

---

## Context Fields

| Field | Type | Description |
|-------|------|-------------|
| `phase` | string | Current phase (phase-1, phase-2, phase-3) |
| `hook_type` | string | Hook type being executed |
| `feature_slug` | string | Feature identifier (e.g., "user-auth") |
| `files_modified` | array | List of modified file paths |
| `test_results` | object | Test results (if available) |
| `breakpoint_type` | string | Breakpoint identifier (for on-breakpoint) |
| `timestamp` | string | ISO 8601 timestamp |
| `active_flags` | array | List of active flags (v3.1+) |
| `flag_sources` | object | Map of flag → source ("auto", "explicit", "alias") |

### Flags Example (v3.1+)

```json
{
  "phase": "phase-2",
  "active_flags": ["--think-hard", "--safe", "--wave"],
  "flag_sources": {
    "--think-hard": "alias",
    "--safe": "auto",
    "--wave": "alias"
  }
}
```

---

## Configuration

Hooks can be configured via environment variables or a settings file.

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `EPCI_HOOKS_ENABLED` | `true` | Enable/disable all hooks |
| `EPCI_HOOKS_TIMEOUT` | `30` | Timeout in seconds |
| `EPCI_HOOKS_FAIL_ON_ERROR` | `false` | Stop workflow on hook error |

### Settings File (Optional)

Create `project-memory/settings.json`:

```json
{
  "hooks": {
    "enabled": true,
    "timeout_seconds": 30,
    "fail_on_error": false,
    "active": [
      "pre-phase-2-lint",
      "post-phase-3-notify"
    ]
  }
}
```

---

## Error Handling

### Default Behavior (`fail_on_error: false`)

- Hook timeout → Warning logged, workflow continues
- Hook exit code ≠ 0 → Warning logged, workflow continues
- Invalid JSON output → Warning logged, workflow continues
- Hook not found → Silently skipped

### Strict Mode (`fail_on_error: true`)

- Hook timeout → Workflow pauses with error
- Hook exit code ≠ 0 → Workflow pauses with error
- Invalid JSON output → Workflow pauses with error

---

## Testing Hooks

### Using the CLI

```bash
# List all discovered hooks
python hooks/runner.py --list

# Run a specific hook type with context
python hooks/runner.py pre-phase-2 --context '{"phase": "phase-2", "feature_slug": "test"}'

# Run with custom timeout
python hooks/runner.py post-phase-3 --timeout 60

# Verbose output
python hooks/runner.py on-breakpoint --verbose
```

### Manual Testing

```bash
# Test a hook directly
echo '{"phase": "phase-2"}' | ./hooks/active/pre-phase-2-lint.sh
```

---

## Activating Example Hooks

The `examples/` directory contains ready-to-use hooks. To activate:

```bash
# Option 1: Symlink (recommended)
cd hooks/active
ln -s ../examples/pre-phase-2-lint.sh pre-phase-2-lint.sh

# Option 2: Copy
cp hooks/examples/pre-phase-2-lint.sh hooks/active/
```

---

## Security Considerations

**Hooks run with the same privileges as Claude Code.** Exercise caution:

1. **Review hook contents** before activating
2. **Only use trusted hooks** from known sources
3. **Avoid storing secrets** in hook files (use environment variables)
4. **Be careful with external commands** (avoid `curl | bash` patterns)

---

## Troubleshooting

### Hook Not Running

1. Check hook is in `hooks/active/` directory
2. Verify filename matches hook type (e.g., `pre-phase-2*.sh`)
3. Ensure file is executable (`chmod +x`)
4. Check shebang line is correct

### Hook Failing

1. Run hook manually: `echo '{}' | ./hooks/active/your-hook.sh`
2. Check for syntax errors
3. Verify JSON output format
4. Check timeout (default 30s)

### Debugging

Enable verbose mode:
```bash
python hooks/runner.py pre-phase-2 --verbose
```

Check logs:
```bash
cat epci-breakpoints.log  # If using on-breakpoint-log example
```

---

## Examples Reference

| Example | Type | Purpose |
|---------|------|---------|
| `pre-phase-2-lint.sh` | pre-phase-2 | Run linters (npm/composer/flake8) |
| `post-phase-3-notify.py` | post-phase-3 | Send Slack/Discord notifications |
| `on-breakpoint-log.sh` | on-breakpoint | Log breakpoint events to file |

---

## API Reference

### runner.py

```python
from hooks.runner import run_hooks, HookConfig

# Run hooks with default config
results = run_hooks('pre-phase-2', {'phase': 'phase-2', 'feature_slug': 'auth'})

# Run with custom config
config = HookConfig(timeout_seconds=60, fail_on_error=True)
results = run_hooks('post-phase-3', context_dict, config)

# Check results
for result in results:
    print(f"{result.hook_name}: {result.status} - {result.message}")
```

---

## Changelog

### v1.0.0 (2025-12-15)

- Initial release with EPCI v3.1
- 7 hook types supported
- Python, Bash, Node.js support
- Timeout and error handling
- 3 example hooks included
