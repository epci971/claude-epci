---
name: step-02-research
description: Multi-source research for error context and solutions
prev_step: steps/step-01-evidence.md
next_step: steps/step-03-thought-tree.md
---

# Step 02: Research

## MANDATORY EXECUTION RULES (READ FIRST):

- 🔴 NEVER skip research for COMPLEX-looking bugs
- 🔴 NEVER rely on single source
- ✅ ALWAYS try Context7 MCP first if framework detected
- ✅ ALWAYS follow cascade pattern with fallbacks
- ✅ ALWAYS note research findings for hypothesis generation
- 💭 FOCUS on finding similar issues and proven solutions

## EXECUTION PROTOCOLS:

### 1. Research Pipeline Overview

```
RESEARCH CASCADE:

1. Detect framework/library in error
   |
   +-> Framework detected?
       |
       +-> YES: Query Context7 MCP
       |        "{error} {framework} {version}"
       |        |
       |        +-> results >= 3 AND confidence >= 60%?
       |            |
       |            +-> YES: Use results, continue
       |            +-> NO: Fallback to WebSearch
       |
       +-> NO: Skip to WebSearch

2. WebSearch fallback
   Query: "{error} site:stackoverflow.com OR site:github.com/issues"
   Filter: < 2 years, official docs prioritized
   |
   +-> results >= 5?
       |
       +-> YES: Use results, continue
       +-> NO: Suggest Perplexity prompt

3. Perplexity (suggested, not auto)
   Mode: Deep Research if error rare/complex
   Prompt template provided to user
```

### 2. Context7 MCP Query (Primary)

If framework detected, use Context7:

```typescript
// Resolve library ID first
const libraryId = await mcp_context7_resolve_library_id({
  libraryName: detected_framework,
  query: error_message
});

// Query documentation
const docs = await mcp_context7_query_docs({
  libraryId: libraryId,
  query: `${error_type} ${error_message} troubleshooting`
});
```

**Context7 Query Patterns by Stack:**

| Stack | Library | Query Pattern |
|-------|---------|---------------|
| Django | `/django/django` | `{error} Django {version}` |
| React | `/facebook/react` | `{error} React hooks/components` |
| Spring | `/spring-projects/spring-boot` | `{error} Spring Boot {version}` |
| Symfony | `/symfony/symfony` | `{error} Symfony {version}` |
| Node | `/nodejs/node` | `{error} Node.js` |

### 3. WebSearch Fallback

If Context7 unavailable or insufficient:

```typescript
WebSearch({
  query: `${error_message} site:stackoverflow.com OR site:github.com/issues`,
  blocked_domains: ["w3schools.com", "tutorialspoint.com"]
})
```

**Query Templates:**

| Error Type | Query Pattern |
|------------|---------------|
| TypeError | `"TypeError: {msg}" {framework} fix` |
| HTTP error | `{status_code} error {endpoint_pattern} {framework}` |
| Database | `{db_error_code} {ORM} troubleshooting` |
| Auth | `{auth_error} {auth_provider} {framework}` |
| Import | `cannot find module {module} {framework}` |

### 4. Perplexity Suggestion (Manual)

If research insufficient, suggest Perplexity prompt:

```
PERPLEXITY SUGGESTED

Search Type: {Standard | Deep Research}

Prompt:
"{error_message} {framework} {version} root cause solution {current_year-1} {current_year}"

Inject results when ready, I'll continue hypothesis generation.
```

**Deep Research triggers:**
- Error appears rare (< 5 search results)
- Multiple possible causes in initial research
- Framework version-specific issue
- Security-related error

### 5. Stack-Specific Research

Load debug patterns from stack skill:

| Stack | Debug Resources |
|-------|-----------------|
| python-django | Django Debug Toolbar, Sentry patterns |
| javascript-react | React DevTools, error boundaries |
| java-springboot | Actuator endpoints, Micrometer |
| php-symfony | Profiler, WebProfilerBundle |
| frontend-editor | Browser DevTools, CSS debugging |

### 6. Synthesize Research Findings

Compile research into actionable insights:

```
RESEARCH SYNTHESIS:

Source: {Context7 | WebSearch | Perplexity | Stack skill}

Key Findings:
1. {finding 1} - Source: {url/doc}
2. {finding 2} - Source: {url/doc}
3. {finding 3} - Source: {url/doc}

Common Causes Identified:
- {cause 1} (mentioned in X sources)
- {cause 2} (mentioned in Y sources)

Suggested Solutions:
- {solution 1} (confidence: high)
- {solution 2} (confidence: medium)

Framework-Specific Notes:
{Any version-specific or config notes}
```

## CONTEXT BOUNDARIES:

- This step expects: Evidence packet from step-01
- This step produces: Research synthesis with potential causes and solutions

## OUTPUT FORMAT:

```
## Research Complete

### Sources Queried
| Source | Query | Results | Useful |
|--------|-------|---------|--------|
| Context7 | {query} | {N} | {Yes/No} |
| WebSearch | {query} | {N} | {Yes/No} |

### Key Findings

#### From Documentation (Context7)
{findings if available}

#### From Community (WebSearch)
{findings if available}

### Common Causes Identified
1. **{Cause 1}** - Confidence: {High | Medium | Low}
   - Evidence: {source reference}
2. **{Cause 2}** - Confidence: {High | Medium | Low}
   - Evidence: {source reference}

### Framework-Specific Context
{Stack-specific debug patterns and notes}

### Sources
- [Source 1](url)
- [Source 2](url)

Ready for hypothesis generation.
```

## PERPLEXITY FALLBACK FORMAT:

```
## Research Insufficient

Context7: {unavailable | insufficient results}
WebSearch: {N} results, {quality assessment}

PERPLEXITY SUGGESTED

Type: {Standard | Deep Research}
Prompt:
`{generated prompt}`

Reply with Perplexity results to continue, or type 'skip' to proceed with available data.
```

## NEXT STEP TRIGGER:

Proceed to step-03-thought-tree.md when:
- At least one research source provided useful data
- OR user provided Perplexity results
- OR user chose to skip with available data
