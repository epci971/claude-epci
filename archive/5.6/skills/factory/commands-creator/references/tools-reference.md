# Tools Reference - Claude Code Tool Capabilities

> Complete guide to available tools and their appropriate usage

---

## Tool Overview Matrix

| Tool | Purpose | Risk | Common Use |
|------|---------|------|------------|
| `Read` | Read file contents | Low | Analysis, inspection |
| `Write` | Create/overwrite files | Medium | Generation, export |
| `Edit` | Modify existing files | Medium | Refactoring, fixes |
| `Bash` | Execute shell commands | High | Build, test, git |
| `Grep` | Search file contents | Low | Code search |
| `Glob` | Find files by pattern | Low | File discovery |
| `Task` | Invoke subagents | Medium | Delegation |
| `WebFetch` | HTTP requests | Medium | API, docs |
| `TodoRead` | Read task list | Low | Progress tracking |
| `TodoWrite` | Modify task list | Low | Task management |

---

## Tool Specifications

### Read

**Purpose**: Read file contents from disk

**Capabilities**:
- Read any text file
- Support for binary files (images, PDFs)
- Line range selection with `offset` and `limit`
- Returns content with line numbers

**Usage Patterns**:
```
Read file_path="/path/to/file.md"
Read file_path="/path/to/file.md" offset=10 limit=50
```

**Best For**:
- Analyzing existing code
- Reading configuration files
- Inspecting documentation
- Understanding project structure

**Constraints**:
- Returns truncated content for very large files
- Line numbers start at 1

---

### Write

**Purpose**: Create new files or overwrite existing ones

**Capabilities**:
- Create files with any content
- Overwrite existing files completely
- Create parent directories if needed

**Usage Patterns**:
```
Write file_path="/path/to/new-file.md" content="..."
```

**Best For**:
- Generating new files
- Creating documentation
- Exporting reports
- Creating configuration files

**Constraints**:
- Requires Read before Write for existing files
- Overwrites entire file content
- Use Edit for partial modifications

---

### Edit

**Purpose**: Modify specific parts of existing files

**Capabilities**:
- Replace specific text strings
- Support for `replace_all` flag
- Preserves rest of file content

**Usage Patterns**:
```
Edit file_path="/path/to/file" old_string="before" new_string="after"
Edit file_path="/path/to/file" old_string="pattern" new_string="replacement" replace_all=true
```

**Best For**:
- Refactoring code
- Fixing bugs
- Updating configurations
- Renaming variables

**Constraints**:
- Requires Read before Edit
- `old_string` must be unique (unless `replace_all`)
- Cannot create new files

---

### Bash

**Purpose**: Execute shell commands

**Capabilities**:
- Run any shell command
- Access to system tools (git, npm, python, etc.)
- Background execution support
- Timeout control

**Usage Patterns**:
```
Bash command="npm test"
Bash command="git status"
Bash command="python script.py" timeout=300000
```

**Best For**:
- Running tests
- Git operations
- Build processes
- Installing dependencies
- System commands

**Constraints**:
- High risk - can modify system state
- Default timeout 120 seconds
- Prefer specialized tools when available
- Never use for: grep, find, cat, head, tail (use dedicated tools)

---

### Grep

**Purpose**: Search for patterns in file contents

**Capabilities**:
- Regex pattern matching
- Filter by file type or glob
- Multiple output modes
- Context lines support

**Usage Patterns**:
```
Grep pattern="function.*export" type="js"
Grep pattern="TODO" glob="**/*.md" output_mode="content"
Grep pattern="class.*Error" path="/src" -C=3
```

**Output Modes**:
| Mode | Returns |
|------|---------|
| `files_with_matches` | File paths only (default) |
| `content` | Matching lines with context |
| `count` | Match counts per file |

**Best For**:
- Finding code patterns
- Locating usages
- Searching for TODOs
- Finding definitions

---

### Glob

**Purpose**: Find files matching patterns

**Capabilities**:
- Pattern-based file search
- Returns paths sorted by modification time
- Fast for large codebases

**Usage Patterns**:
```
Glob pattern="**/*.ts"
Glob pattern="src/**/*.test.js"
Glob pattern="*.md" path="/docs"
```

**Best For**:
- Finding files by extension
- Locating test files
- Discovering project structure
- Finding configuration files

**Constraints**:
- Returns file paths only, not contents
- Use Read to inspect found files

---

### Task

**Purpose**: Invoke subagents for specialized tasks

**Capabilities**:
- Spawn specialized agents
- Parallel execution support
- Background task support
- Different agent types (Explore, Plan, general-purpose)

**Usage Patterns**:
```
Task subagent_type="Explore" prompt="Find authentication patterns"
Task subagent_type="general-purpose" prompt="Implement feature X"
Task subagent_type="Plan" prompt="Design API architecture"
```

**Agent Types**:
| Type | Tools | Use For |
|------|-------|---------|
| `Explore` | Read-only | Quick codebase exploration |
| `Plan` | Read-only | Research and planning |
| `general-purpose` | All | Complex implementation |

**Best For**:
- Delegating complex analysis
- Parallel task execution
- Specialized domain work
- Long-running operations

---

### WebFetch

**Purpose**: Fetch content from URLs

**Capabilities**:
- HTTP GET requests
- Markdown conversion for HTML
- AI-powered content processing
- Redirect handling

**Usage Patterns**:
```
WebFetch url="https://example.com/api/docs" prompt="Extract API endpoints"
```

**Best For**:
- Fetching documentation
- API reference lookup
- External resource access

**Constraints**:
- Read-only (GET only)
- Content may be summarized
- 15-minute cache

---

### TodoRead / TodoWrite

**Purpose**: Task list management for session

**Capabilities**:
- Track multi-step tasks
- Status: pending, in_progress, completed
- Session-scoped persistence

**Usage Patterns**:
```
TodoRead
TodoWrite todos=[{"content": "Task 1", "status": "pending", "activeForm": "Working on Task 1"}]
```

**Best For**:
- Complex multi-step operations
- Progress tracking
- User visibility into work

---

## Tool Selection Guide

### By Operation Type

| Operation | Primary Tools |
|-----------|---------------|
| Analysis | Read, Grep, Glob |
| Generation | Write, Read |
| Modification | Edit, Read |
| Build/Test | Bash, Read |
| Search | Grep, Glob |
| Orchestration | Task |
| Documentation | Read, Write, WebFetch |

### By Risk Level

| Risk | Tools | Mitigation |
|------|-------|------------|
| **Low** | Read, Grep, Glob, TodoRead | None needed |
| **Medium** | Write, Edit, Task, WebFetch, TodoWrite | Validate before action |
| **High** | Bash | Careful review, `--dry-run` |

### Least Privilege Patterns

```yaml
# Read-only analysis
allowed-tools: Read, Grep, Glob

# Generate without modify
allowed-tools: Read, Write, Glob

# Full modification
allowed-tools: Read, Write, Edit, Grep, Glob

# Build and test
allowed-tools: Read, Bash, Grep, Glob

# Orchestration
allowed-tools: Read, Task, Glob

# Everything
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, Task
```

---

## Anti-Patterns

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| `Bash command="cat file.txt"` | Inefficient | Use `Read` |
| `Bash command="grep pattern"` | Less capable | Use `Grep` |
| `Bash command="find . -name"` | Slower | Use `Glob` |
| `Write` without `Read` | May overwrite | Always Read first |
| All tools for simple task | Over-permissive | Least privilege |
| `Bash` for file operations | Risky | Use Read/Write/Edit |

---

## Quick Reference

```
+------------------------------------------+
|            TOOL SELECTION                 |
+------------------------------------------+
| Read file?        → Read                  |
| Create file?      → Write (after Read)    |
| Modify file?      → Edit (after Read)     |
| Find files?       → Glob                  |
| Search content?   → Grep                  |
| Run command?      → Bash                  |
| Delegate task?    → Task                  |
| Fetch URL?        → WebFetch              |
| Track tasks?      → TodoWrite             |
+------------------------------------------+
```
