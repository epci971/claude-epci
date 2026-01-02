# Context7 MCP Server

## Overview

Context7 provides access to up-to-date documentation for external libraries and frameworks.

| Attribute | Value |
|-----------|-------|
| **Function** | Library documentation lookup |
| **Tools** | `resolve-library-id`, `query-docs` |
| **Timeout** | 15 seconds |
| **Fallback** | Web search |

## When to Use

- Importing external packages
- Questions about framework APIs
- Looking for best practices
- Integration patterns

## Auto-Triggers

### Keywords
`import`, `require`, `use`, `library`, `framework`, `documentation`, `docs`, `api`, `package`, `dependency`

### Files
`package.json`, `composer.json`, `requirements.txt`, `pyproject.toml`, `pom.xml`, `build.gradle`

### Personas
- **architect** (primary)
- **backend** (primary)
- **frontend** (secondary)
- **doc** (primary)

## Workflow

```
1. Detect import/dependency in code or brief
2. resolve-library-id → Find Context7 library ID
3. query-docs → Retrieve relevant documentation
4. Integrate patterns into generated code
```

## Example Usage

**Brief**: "Add pagination to product list"
**Stack**: Symfony (composer.json detected)

```
 Context7 activated (auto: backend)
 resolve-library-id("doctrine pagination")
 query-docs(topic="pagination")
 Integrating KnpPaginator patterns
```

## Fallback

If Context7 is unreachable:

```
 [MCP] Context7 unreachable, using web search
```

1. Retry 2 times with 15s timeout
2. If still failing, use WebSearch tool
3. Log warning, continue workflow

## Best Practices

1. **Be specific** with library names
2. **Include version** if known (`react@18`, `symfony/7`)
3. **Combine with stack detection** for better results
4. **Cache responses** during session (automatic)

## Configuration

```json
{
  "context7": {
    "enabled": true,
    "auto_activate": true,
    "timeout_seconds": 15
  }
}
```

---

*Context7 Reference — F12 MCP Integration*
