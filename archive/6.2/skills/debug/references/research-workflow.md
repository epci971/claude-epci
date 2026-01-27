# Research Workflow

## Overview

Multi-source research cascade for gathering error context and potential solutions.
Follows graceful degradation pattern: Context7 → WebSearch → Perplexity.

## Pipeline Diagram

```
                     RESEARCH PIPELINE

                    ┌───────────────────┐
                    │ DETECT FRAMEWORK  │
                    │ in error message  │
                    └─────────┬─────────┘
                              │
              ┌───────────────┴───────────────┐
              │                               │
         Framework?                      No framework
              │                               │
              v                               │
    ┌─────────────────┐                       │
    │   CONTEXT7 MCP  │                       │
    │ query library   │                       │
    └────────┬────────┘                       │
             │                                │
    ┌────────┴────────┐                       │
    │                 │                       │
  Results?        No/Poor                     │
    │               │                         │
    v               v                         v
  USE IT    ┌─────────────────────────────────┐
            │        WEBSEARCH                │
            │ site:stackoverflow.com          │
            │ site:github.com/issues          │
            └────────────┬────────────────────┘
                         │
              ┌──────────┴──────────┐
              │                     │
          Results?              No/Poor
              │                     │
              v                     v
           USE IT          ┌─────────────────┐
                           │   PERPLEXITY    │
                           │  (suggested)    │
                           └─────────────────┘
```

## Step 1: Framework Detection

Detect framework/library from error message:

| Pattern | Framework |
|---------|-----------|
| `django.` / `Django` | Django |
| `react` / `React` / `jsx` | React |
| `spring` / `SpringBoot` | Spring Boot |
| `symfony` / `Symfony` | Symfony |
| `express` / `Express` | Express.js |
| `node:` / `Node.js` | Node.js |
| `flask` / `Flask` | Flask |
| `laravel` / `Laravel` | Laravel |

Also detect from:
- File extensions in stack trace
- Import statements in error context
- Config files in codebase

## Step 2: Context7 MCP (Primary)

If framework detected, query Context7:

### Resolve Library ID

```typescript
const libraryId = await mcp_context7_resolve_library_id({
  libraryName: "django",
  query: "TypeError in ORM query"
});
// Returns: "/django/django"
```

### Common Library IDs

| Framework | Library ID |
|-----------|------------|
| Django | `/django/django` |
| React | `/facebook/react` |
| Spring Boot | `/spring-projects/spring-boot` |
| Symfony | `/symfony/symfony` |
| Express.js | `/expressjs/express` |
| Node.js | `/nodejs/node` |
| Flask | `/pallets/flask` |
| Laravel | `/laravel/laravel` |

### Query Documentation

```typescript
const docs = await mcp_context7_query_docs({
  libraryId: "/django/django",
  query: "QuerySet TypeError NoneType fix troubleshooting"
});
```

### Query Templates by Error Type

| Error Type | Query Template |
|------------|----------------|
| TypeError | `"{error_msg}" TypeError troubleshooting` |
| ImportError | `cannot import {module} fix` |
| HTTP error | `{status_code} error handling` |
| Database | `{db_error} query fix` |
| Auth | `authentication {error} security` |

### Success Criteria

Context7 results are sufficient if:
- >= 3 relevant results
- Confidence >= 60%
- At least one result mentions fix/solution

## Step 3: WebSearch (Fallback)

If Context7 unavailable or insufficient:

### Query Construction

```typescript
WebSearch({
  query: `"${error_message}" site:stackoverflow.com OR site:github.com/issues`,
  blocked_domains: ["w3schools.com", "tutorialspoint.com", "geeksforgeeks.org"]
});
```

### Query Templates

| Error Type | Query |
|------------|-------|
| Generic | `"{error_msg}" fix solution {year}` |
| Framework-specific | `"{error_msg}" {framework} {version} fix` |
| Library error | `"{library} {error}" github issues` |
| Config error | `"{error}" configuration troubleshooting` |

### Filter Criteria

- **Recency**: Prefer results < 2 years old
- **Source priority**:
  1. Official documentation
  2. GitHub issues (closed, with solution)
  3. Stack Overflow (accepted answers)
  4. Blog posts (reputable authors)

### Success Criteria

WebSearch results are sufficient if:
- >= 5 relevant results
- At least one from official docs or GitHub
- Clear solution or workaround mentioned

## Step 4: Perplexity (Suggested)

If WebSearch insufficient, suggest Perplexity prompt:

### When to Suggest

- < 5 WebSearch results
- Error appears rare
- Framework version-specific issue
- Security-related (needs careful research)
- Multiple conflicting solutions found

### Prompt Templates

**Standard Search:**
```
{error_message} {framework} {version} root cause solution {year-1} {year}
```

**Deep Research:**
```
Deep analysis: {error_message}

Context:
- Framework: {framework} {version}
- Environment: {environment}
- Stack trace: {key_lines}

Questions:
1. What are the common causes of this error?
2. What are the recommended solutions?
3. Are there version-specific considerations?
4. What are the best practices to prevent this?
```

### Deep Research Triggers

- Error appears in < 5 search results
- Security implications
- Data integrity concerns
- Production incident
- Multiple potential causes (> 3)

## Source Synthesis

After gathering from available sources:

### Synthesis Template

```markdown
## Research Synthesis

### Sources Used
- Context7: {Yes/No/Partial}
- WebSearch: {N} results
- Perplexity: {Yes/No}

### Key Findings
1. **{Finding 1}** — Source: {url/doc}
2. **{Finding 2}** — Source: {url/doc}
3. **{Finding 3}** — Source: {url/doc}

### Common Causes Identified
| Cause | Frequency | Confidence |
|-------|-----------|------------|
| {cause 1} | {N} sources | High |
| {cause 2} | {N} sources | Medium |

### Suggested Solutions
| Solution | Source | Risk |
|----------|--------|------|
| {sol 1} | {url} | Low |
| {sol 2} | {url} | Medium |

### Framework-Specific Notes
{version-specific caveats, deprecations, etc.}
```

## Error Handling

| Scenario | Action |
|----------|--------|
| Context7 MCP unavailable | Skip to WebSearch |
| Context7 returns 0 results | Fallback to WebSearch |
| WebSearch blocked | Use allowed domains only |
| All sources fail | Proceed with evidence only |
| Rate limited | Wait and retry once |

## Cache Behavior

- Context7: No local cache (MCP handles)
- WebSearch: Internal 15-minute cache
- Research results: Store in working memory for session
