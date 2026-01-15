# Commit Context Reference

> Shared commit context schema for /epci, /quick, /debug.

## Context File

**Location:** `.epci-commit-context.json` (project root)

## Schema

```json
{
  "source": "epci|quick|debug",
  "type": "feat|fix|refactor|docs|style|test|chore|perf|ci",
  "scope": "<module-name>",
  "description": "<what was done>",
  "files": ["<file1>", "<file2>"],
  "featureDoc": "<path/to/feature-doc.md>",
  "breaking": false,
  "ticket": "<JIRA-123>"
}
```

## Conventional Commits

| Type | Usage |
|------|-------|
| `feat` | New feature |
| `fix` | Bug fix |
| `docs` | Documentation only |
| `style` | Formatting |
| `refactor` | Code restructuring |
| `test` | Adding/modifying tests |
| `chore` | Maintenance |
| `perf` | Performance |
| `ci` | CI/CD changes |

## Message Format

```
{type}({scope}): {description}

- {detail 1}
- {detail 2}

Refs: {featureDoc}
{ticket if present}
```

## Breaking Changes

If `breaking: true`:
- Add `!` after type: `feat(scope)!: description`
- Add `BREAKING CHANGE:` footer

## Workflow Integration

| Source | Context Generator | Commit Trigger |
|--------|-------------------|----------------|
| /epci | Phase 3 | `/commit` suggested |
| /quick | Resume Final | `/commit` suggested |
| /debug | --commit flag | `/commit` suggested |

## Cleanup

After successful commit, `/commit` deletes the context file.
