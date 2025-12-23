# EPCI Hooks System

> **Version**: 1.1.0 (EPCI v3.7)
> **Date**: 2025-12-18

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
| `pre-commit` | Before commit decision | Final checks, memory update, validation |
| `post-commit` | After git commit | Notifications, CI trigger, webhooks |
| `post-phase-3` | After Phase 3 complete | Cleanup, final metrics |
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
| `feature_title` | string | Human-readable feature title |
| `files_modified` | array | List of modified file paths |
| `files_created` | int | Number of files created |
| `files_updated` | int | Number of files updated |
| `complexity` | string | TINY, SMALL, STANDARD, or LARGE |
| `complexity_score` | float | Numeric complexity score (0.0-1.0) |
| `test_results` | object | Test results (if available) |
| `breakpoint_type` | string | Breakpoint identifier (for on-breakpoint) |
| `timestamp` | string | ISO 8601 timestamp |
| `active_flags` | array | List of active flags (v3.1+) |
| `flag_sources` | object | Map of flag → source ("auto", "explicit", "alias") |
| `project_root` | string | Path to project root directory |
| `feature_document` | string | Path to Feature Document (if STANDARD/LARGE) |
| `estimated_time` | string | Estimated time (e.g., "2h 30m") |
| `actual_time` | string | Actual time (e.g., "3h 15m") |
| `agents_used` | array | List of subagents invoked (e.g., ["code-reviewer"]) |
| `review_findings` | object | Findings from subagent reviews (for post-phase-2) |

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

### Pre-Commit Context Example

```json
{
  "phase": "phase-3",
  "hook_type": "pre-commit",
  "feature_slug": "user-authentication",
  "files_modified": ["src/auth.py", "tests/test_auth.py"],
  "commit_message": "feat(auth): add user authentication\n\n- Add login endpoint\n- Add JWT validation",
  "pending_commit": true,
  "complexity": "STANDARD",
  "project_root": "/path/to/project",
  "timestamp": "2025-12-18T10:30:00Z"
}
```

### Post-Commit Context Example

```json
{
  "phase": "phase-3",
  "hook_type": "post-commit",
  "feature_slug": "user-authentication",
  "commit_hash": "a1b2c3d",
  "branch": "feature/user-authentication",
  "files_committed": ["src/auth.py", "tests/test_auth.py"],
  "project_root": "/path/to/project",
  "timestamp": "2025-12-18T10:35:00Z"
}
```

### Post-Phase-3 Context Example

```json
{
  "phase": "phase-3",
  "hook_type": "post-phase-3",
  "feature_slug": "user-authentication",
  "feature_title": "User Authentication",
  "files_modified": ["src/auth.py", "tests/test_auth.py"],
  "files_created": 2,
  "files_updated": 1,
  "complexity": "STANDARD",
  "complexity_score": 0.6,
  "estimated_time": "2h",
  "actual_time": "2h 30m",
  "commit_hash": "a1b2c3d",
  "commit_status": "committed",
  "agents_used": ["code-reviewer", "security-auditor"],
  "feature_document": "docs/features/user-authentication.md",
  "project_root": "/path/to/project",
  "timestamp": "2025-12-18T10:30:00Z"
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

| Example | Type | Purpose | Auto-Active |
|---------|------|---------|-------------|
| `pre-phase-2-lint.sh` | pre-phase-2 | Run linters (npm/composer/flake8) | Yes |
| `post-phase-2-suggestions.py` | post-phase-2 | Generate proactive suggestions | Yes |
| `pre-commit-memory.py` | pre-commit | Save feature to Project Memory (before commit) | Yes |
| `post-commit-notify.py` | post-commit | Send notifications after commit | No* |
| `post-phase-3-memory-update.py` | post-phase-3 | Legacy: Save feature to Project Memory | No |
| `post-phase-3-notify.py` | post-phase-3 | Send Slack/Discord notifications | No* |
| `on-breakpoint-memory-context.py` | on-breakpoint | Load memory context for breakpoint | Yes |
| `on-breakpoint-log.sh` | on-breakpoint | Log breakpoint events to file | No |

*Requires configuration (webhook URLs via environment variables)

### Project Memory Hooks (v3.7+)

The following hooks integrate with Project Memory for automatic learning:

**`post-phase-3-memory-update.py`** — Saves feature history after Phase 3:
- Records feature metadata (slug, complexity, files, agents)
- Updates velocity metrics
- Triggers calibration (if estimated/actual times provided)
- Increments features_completed counter

**`on-breakpoint-memory-context.py`** — Loads context at each breakpoint:
- Provides velocity metrics for display
- Finds similar features for suggestions
- Returns learning status

**`post-phase-2-suggestions.py`** — Generates proactive suggestions:
- Converts subagent findings to suggestions
- Runs pattern detector on changed files
- Formats output for breakpoint display

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

### v1.1.0 (2025-12-18)

- Added Project Memory integration hooks
- New hooks: `post-phase-3-memory-update.py`, `on-breakpoint-memory-context.py`
- Fixed `importlib` loading for hyphenated module names
- Extended context fields documentation
- Updated examples reference table

### v1.0.0 (2025-12-15)

- Initial release with EPCI v3.1
- 7 hook types supported
- Python, Bash, Node.js support
- Timeout and error handling
- 3 example hooks included
