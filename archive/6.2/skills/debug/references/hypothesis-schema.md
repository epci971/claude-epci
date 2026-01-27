# Hypothesis Schema (Tree of Thought)

## Overview

Schema for structured hypotheses in /debug workflow.
Based on Tree of Thought (ToT) research: thought generator + thought evaluator pattern.

## Full Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "DebugHypothesis",
  "type": "object",
  "required": ["id", "hypothesis", "confidence", "rationale", "evidence", "testable_prediction", "quick_check", "files_to_investigate", "status"],
  "properties": {
    "id": {
      "type": "string",
      "pattern": "^H[0-9]+$",
      "description": "Unique identifier (H1, H2, H3, H4)"
    },
    "hypothesis": {
      "type": "string",
      "minLength": 10,
      "maxLength": 200,
      "description": "Clear statement of suspected root cause"
    },
    "confidence": {
      "type": "integer",
      "minimum": 0,
      "maximum": 100,
      "description": "Confidence percentage (0-100)"
    },
    "rationale": {
      "type": "string",
      "description": "Why this hypothesis is plausible"
    },
    "evidence": {
      "type": "array",
      "items": { "type": "string" },
      "minItems": 1,
      "description": "Evidence supporting this hypothesis"
    },
    "testable_prediction": {
      "type": "string",
      "description": "What we expect to observe if hypothesis is true"
    },
    "quick_check": {
      "type": "string",
      "description": "Fast action to verify/falsify hypothesis"
    },
    "files_to_investigate": {
      "type": "array",
      "items": { "type": "string" },
      "minItems": 1,
      "description": "Files to examine for this hypothesis"
    },
    "status": {
      "type": "string",
      "enum": ["pending", "investigating", "confirmed", "infirmed"],
      "description": "Current status of hypothesis"
    }
  }
}
```

## Example Hypothesis

```json
{
  "id": "H1",
  "hypothesis": "Cache returns stale data due to TTL misconfiguration after recent config change",
  "confidence": 75,
  "rationale": "Recent commit abc123 modified cache settings. Stack trace shows CacheService.get() involvement. Similar bug #42 had identical pattern.",
  "evidence": [
    "Stack trace shows CacheService.get() at line 42",
    "Similar bug #42 had same root cause (TTL)",
    "git log shows cache.yml modified 2 days ago",
    "Error occurs only for data older than 1 hour"
  ],
  "testable_prediction": "Adding timestamp logging will show cached responses have outdated timestamps (> current TTL)",
  "quick_check": "Add console.log in CacheService.get() before return: log(key, cachedAt, now)",
  "files_to_investigate": [
    "src/services/CacheService.ts",
    "config/cache.yml",
    "src/middleware/cacheMiddleware.ts"
  ],
  "status": "pending"
}
```

## Field Guidelines

### hypothesis
- Start with suspected component/behavior
- Include suspected cause mechanism
- Be specific, not vague

**Good**: "Cache returns stale data due to TTL misconfiguration"
**Bad**: "Something wrong with cache"

### confidence
- 80-100: High confidence, strong evidence
- 60-79: Moderate, worth investigating
- 40-59: Low, possible but uncertain
- 0-39: Speculation only

### evidence
- Cite specific sources:
  - Stack trace line numbers
  - Git commit references
  - Similar bug IDs from project-memory
  - Research findings with URLs

### testable_prediction
- Must be falsifiable
- Describe observable outcome if hypothesis is TRUE
- Should be checkable without implementing fix

**Good**: "Logging will show timestamp delta > 3600s"
**Bad**: "It will work better"

### quick_check
- Action that can be done in < 5 minutes
- Non-destructive (no code changes that break things)
- Provides clear yes/no answer

**Good**: "Add console.log in X before return"
**Bad**: "Refactor the entire caching layer"

### files_to_investigate
- Order by relevance (most relevant first)
- Include related files (configs, tests)
- Limit to 5 files max per hypothesis

### status
- `pending`: Not yet investigated
- `investigating`: Currently being tested
- `confirmed`: Prediction validated, this is the cause
- `infirmed`: Prediction failed, not the cause

## Hypothesis Tree Structure

```
ROOT: {error_description}
|
+-- H1: {hypothesis} [confidence: 75%] [BEST]
|   +-- Evidence: {e1}, {e2}, {e3}
|   +-- Prediction: {testable_prediction}
|   +-- Quick Check: {quick_check}
|   +-- Files: {f1}, {f2}
|   +-- Status: pending
|
+-- H2: {hypothesis} [confidence: 62%]
|   +-- Evidence: {e1}, {e2}
|   +-- Prediction: {testable_prediction}
|   +-- Quick Check: {quick_check}
|   +-- Files: {f1}
|   +-- Status: pending
|
+-- H3: {hypothesis} [confidence: 48%]
|   +-- Evidence: {e1}
|   +-- Prediction: {testable_prediction}
|   +-- Quick Check: {quick_check}
|   +-- Files: {f1}
|   +-- Status: pending
|
+-- H4: {hypothesis} [confidence: 35%] [LOW]
    +-- Evidence: speculation
    +-- Prediction: {testable_prediction}
    +-- Quick Check: {quick_check}
    +-- Files: {f1}
    +-- Status: pending
```

## Status Transitions

```
pending → investigating → confirmed
                       → infirmed

When investigating:
1. Execute quick_check
2. Observe result vs testable_prediction
3. If match: confirmed
4. If no match: infirmed
5. If confirmed: proceed to fix
6. If infirmed: select next hypothesis
```

## Pairwise Ranking Rules

When ranking hypotheses:

1. Compare H1 vs H2 on each criterion
2. Winner gets point for that criterion
3. Total points determines rank

**Criteria weights:**
| Criterion | Weight |
|-----------|--------|
| Evidence strength | 30% |
| Simplicity | 25% |
| Testability | 20% |
| Research alignment | 15% |
| Recency (recent change) | 10% |

**Example comparison:**
```
H1 vs H2:
- Evidence: H1 > H2 (3 sources vs 1)
- Simplicity: H1 > H2 (single cause vs multiple)
- Testability: H1 = H2 (both have quick checks)
- Research: H1 > H2 (matches SO answer)
- Recency: H1 = H2 (both could be recent)

Winner: H1 (4 wins, 0 losses, 1 tie)
```
