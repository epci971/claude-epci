# Step 00: Init

> Parse input, detect stack, validate scope, launch exploration.

## Trigger

- Skill invocation: `/refactor <target> [--scope] [--pattern]`

## Inputs

| Input | Source | Required |
|-------|--------|----------|
| `target` | User argument (path or description) | Yes |
| `--scope` | User flag | No (auto-detect) |
| `--pattern` | User flag | No (auto-suggest) |
| `--turbo` | User flag | No |
| `--dry-run` | User flag | No |
| `--atomic` | User flag | No |

## Protocol

### 1. Parse Input

```
IF target is file path:
  → Validate file exists
  → Extract file extension for stack detection
ELSE IF target is directory path:
  → Validate directory exists
  → Count files for scope estimation
ELSE:
  → Treat as natural language description
  → Use @Explore to identify target files
```

### 2. Detect Stack Skills

Check for stack signatures in order:

```python
STACK_DETECTION = {
    "python-django": ["manage.py", "django" in requirements],
    "javascript-react": ["react" in package.json],
    "java-springboot": ["spring-boot" in pom.xml or build.gradle],
    "php-symfony": ["symfony" in composer.json],
    "frontend-editor": ["tailwind.config.*"]
}

for stack, triggers in STACK_DETECTION:
    if any trigger matches:
        load stack skill references
        break
```

### 3. Estimate Scope (if not provided)

| Criteria | Scope |
|----------|-------|
| 1 file | single |
| 2-5 files in same module | module |
| 5-15 files across modules | cross-module |
| 15+ files or system-wide | architecture |

### 4. Initialize State

```json
{
  "refactor_id": "refactor-{timestamp}",
  "target": "<parsed target>",
  "scope": "<single|module|cross-module|architecture>",
  "pattern_hint": "<user pattern or null>",
  "stack": "<detected stack or generic>",
  "flags": {
    "turbo": false,
    "dry_run": false,
    "atomic": false
  },
  "metrics_before": null,
  "metrics_after": null,
  "transformations": [],
  "status": "initialized"
}
```

### 5. Launch @Explore (Background)

```
Task: Explore codebase for refactoring context
Focus:
  - Target file(s) structure and dependencies
  - Related test files
  - Import/export relationships
  - Existing patterns in codebase
```

### 6. Validate Preconditions

| Check | Action if Fails |
|-------|-----------------|
| Target exists | Error: "Target not found" |
| Tests exist for target | Warning: "No tests found, proceed with caution" |
| Git clean (if --atomic) | Error: "Uncommitted changes, commit or stash first" |

## Outputs

| Output | Destination |
|--------|-------------|
| Refactor state | `state-manager` |
| Stack context | Loaded for subsequent steps |
| @Explore task | Running in background |

## Next Step

→ `step-01-analysis.md`

## Error Handling

| Error | Resolution |
|-------|------------|
| Target not found | Ask user to clarify path |
| Multiple stacks detected | Use primary (first match) |
| Unknown stack | Continue without stack skill |
