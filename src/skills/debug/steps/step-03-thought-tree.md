---
name: step-03-thought-tree
description: Build Tree of Thought hypotheses with ranking
prev_step: steps/step-02-research.md
next_step: steps/step-04-routing.md
---

# Step 03: Thought Tree

## MANDATORY EXECUTION RULES (READ FIRST):

- 🔴 NEVER generate fewer than 2 hypotheses
- 🔴 NEVER generate more than 4 hypotheses
- 🔴 NEVER skip testable_prediction or quick_check
- ✅ ALWAYS use hypothesis schema from references
- ✅ ALWAYS rank by pairwise comparison (not absolute scoring)
- ✅ ALWAYS link evidence to each hypothesis
- 💭 FOCUS on testable, falsifiable hypotheses

## EXECUTION PROTOCOLS:

### 1. Hypothesis Generation

Generate 3-4 hypotheses based on:
- Evidence from step-01
- Research findings from step-02
- Similar bugs from project-memory
- Stack-specific common issues

**Generation Strategy:**
```
1. Most likely cause (from research + evidence)
2. Recent change cause (from git history)
3. Configuration/environment cause
4. Edge case/race condition cause (if complex)
```

### 2. Hypothesis Schema

Each hypothesis MUST follow this schema:

```json
{
  "id": "H1",
  "hypothesis": "Cache returns stale data due to TTL misconfiguration",
  "confidence": 75,
  "rationale": "Recent config change in commit abc123 modified cache settings",
  "evidence": [
    "Stack trace shows CacheService.get() at line 42",
    "Similar bug #123 had same root cause"
  ],
  "testable_prediction": "Adding logging will show outdated timestamp in cached responses",
  "quick_check": "Add console.log in CacheService.get() before return",
  "files_to_investigate": [
    "src/services/CacheService.ts",
    "config/cache.yml"
  ],
  "status": "pending"
}
```

@../references/hypothesis-schema.md

See hypothesis-schema.md (imported above) for full schema.

### 3. Pairwise Ranking

Rank hypotheses using pairwise comparison (more stable than absolute scoring):

```
PAIRWISE COMPARISON:

Compare H1 vs H2:
- Evidence strength: H1 > H2 (H1 has stack trace, H2 is speculation)
- Simplicity: H1 > H2 (single cause vs multiple)
- Testability: H1 = H2 (both have quick checks)
Winner: H1

Compare H1 vs H3:
...

Final Ranking: H1 > H3 > H2 > H4
```

**Ranking Criteria:**

| Criterion | Weight | Question |
|-----------|--------|----------|
| Evidence strength | 30% | How well does evidence support this? |
| Simplicity | 25% | Is this the simplest explanation? |
| Testability | 20% | Can this be quickly verified/falsified? |
| Research alignment | 15% | Does research support this cause? |
| Recency | 10% | Does recent change correlate? |

### 4. Confidence Calculation

Calculate confidence for display (0-100):

```
confidence = (
  evidence_strength * 0.30 +
  simplicity * 0.25 +
  testability * 0.20 +
  research_alignment * 0.15 +
  recency * 0.10
) * 100
```

**Confidence Interpretation:**

| Range | Interpretation |
|-------|----------------|
| 80-100 | High confidence, likely correct |
| 60-79 | Moderate confidence, worth investigating |
| 40-59 | Low confidence, possible but uncertain |
| 0-39 | Speculation, investigate only if others fail |

### 5. --turbo Mode

In turbo mode, generate only top 2 hypotheses:

```
if --turbo:
  max_hypotheses = 2
  skip_low_confidence = true (< 50%)
  auto_select = hypotheses[0] if confidence >= 70%
```

### 6. Build Thought Tree

Structure hypotheses as tree:

```
ROOT: {error_description}
|
+-- H1: {hypothesis} [confidence: 75%] [BEST]
|   +-- Evidence: {e1}, {e2}
|   +-- Test: {quick_check}
|   +-- Files: {f1}, {f2}
|
+-- H2: {hypothesis} [confidence: 62%]
|   +-- Evidence: {e1}
|   +-- Test: {quick_check}
|   +-- Files: {f1}
|
+-- H3: {hypothesis} [confidence: 48%]
    +-- Evidence: {e1}
    +-- Test: {quick_check}
    +-- Files: {f1}
```

## CONTEXT BOUNDARIES:

- This step expects: Evidence + Research synthesis
- This step produces: Ranked hypothesis tree with testable predictions

## OUTPUT FORMAT:

```
## Thought Tree Generated

### Hypotheses (Ranked)

#### H1: {title} [Confidence: XX%] ⭐ BEST
**Hypothesis**: {full hypothesis statement}
**Rationale**: {why this is likely}
**Evidence**:
- {evidence 1}
- {evidence 2}
**Testable Prediction**: {what we expect if true}
**Quick Check**: {fast verification action}
**Files to Investigate**:
- `{path1}`
- `{path2}`

#### H2: {title} [Confidence: XX%]
**Hypothesis**: {full hypothesis statement}
**Rationale**: {why this is likely}
**Evidence**:
- {evidence 1}
**Testable Prediction**: {what we expect if true}
**Quick Check**: {fast verification action}
**Files to Investigate**:
- `{path1}`

#### H3: {title} [Confidence: XX%]
{...}

### Ranking Rationale
H1 > H2: {reason}
H2 > H3: {reason}

### Best-First Strategy
Starting investigation with H1 ({title}).
If prediction fails, will proceed to H2.

Ready for routing evaluation.
```

## TURBO MODE OUTPUT:

```
## Thought Tree (Turbo)

### Top 2 Hypotheses

#### H1: {title} [Confidence: XX%] ⚡ AUTO-SELECT
**Quick Check**: {action}
**Files**: `{path1}`, `{path2}`

#### H2: {title} [Confidence: XX%] (Fallback)
**Quick Check**: {action}

Proceeding with H1 (confidence >= 70%).
```

## NEXT STEP TRIGGER:

Proceed to step-04-routing.md with:
- At least 2 ranked hypotheses
- Each with testable_prediction and quick_check
- Files to investigate identified
