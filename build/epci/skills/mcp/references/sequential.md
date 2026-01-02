# Sequential MCP Server

## Overview

Sequential provides structured multi-step reasoning for complex problem analysis.

| Attribute | Value |
|-----------|-------|
| **Function** | Multi-step structured reasoning |
| **Tools** | `sequentialthinking` |
| **Timeout** | 30 seconds |
| **Fallback** | Native Claude reasoning |

## When to Use

- Complex debugging sessions
- Performance investigation
- Architecture analysis
- Security threat modeling
- Multi-factor decision making

## Auto-Triggers

### Flags
- `--think-hard`
- `--ultrathink`

### Keywords
`debug`, `analyze`, `investigate`, `complex`, `think`, `reason`, `step`, `systematic`, `diagnose`, `trace`

### Personas
- **architect** (secondary)
- **backend** (secondary)
- **security** (primary)

## Workflow

```
1. Identify complex problem requiring structured analysis
2. Decompose into sequential thinking steps
3. Analyze each step with intermediate conclusions
4. Build progressive reasoning chain
5. Synthesize final conclusions
```

## Example Usage

**Brief**: "Diagnose why performance degraded after last deploy"
**Flag**: `--think-hard`

```
 Sequential activated (flag: --think-hard)
 Step 1: Identify symptoms (response time +300%)
 Step 2: Collect metrics (CPU normal, DB queries +500%)
 Step 3: Analyze causes (N+1 query in new endpoint)
 Step 4: Test hypothesis (query count before/after)
 Step 5: Propose solution (eager loading)
 Completed 5-step analysis
```

## Token Considerations

Sequential thinking uses significant context:
- Minimum: ~4K tokens per analysis
- With `--think-hard`: ~10K tokens
- With `--ultrathink`: ~32K tokens

**Recommendation**: Only auto-activate with explicit thinking flags.

## Fallback

If Sequential is unavailable:

```
 [MCP] Sequential error, using native reasoning
```

Falls back to Claude's built-in reasoning capabilities without structured steps.

## Best Practices

1. **Reserve for complex problems** — Don't use for simple tasks
2. **Combine with --think-hard** — Ensures adequate token budget
3. **Review intermediate steps** — Verify reasoning chain
4. **Document conclusions** — Capture in Feature Document

## Configuration

```json
{
  "sequential": {
    "enabled": true,
    "auto_activate": true,
    "timeout_seconds": 30
  }
}
```

---

*Sequential Reference — F12 MCP Integration*
