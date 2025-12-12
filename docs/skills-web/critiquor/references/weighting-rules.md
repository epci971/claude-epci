# Weighting Rules

> Complete reference for criteria weighting and score calculation

---

## Number of Criteria

| Document Complexity | Criteria Count |
|---------------------|----------------|
| Simple (short email, note) | 5-6 |
| Standard (proposal, article) | 7-8 |
| Complex (technical doc, report) | 9-10 |
| With custom criteria | Up to 12 |

---

## Weight Attribution Rules

### Impact-Based Allocation

| Impact Type | Weight Range | Examples |
|-------------|--------------|----------|
| Direct impact on comprehension | 20-30% | Clarity, Structure |
| Impact on credibility | 15-25% | Accuracy, Rigor |
| Impact on structure | 10-20% | Organization, Flow |
| Misunderstanding risks | 10-15% | Ambiguity, Terminology |
| Secondary importance | 5-10% | Style details, Minor aspects |

### Absolute Rule

**Sum of all weights MUST equal 100%**

---

## Weight Justification

Every weight must be justified in one sentence. Examples:

- "25% because this criterion directly influences comprehension by the target audience."
- "20% given the professional context where credibility is paramount."
- "10% as secondary aspect that supports overall quality."
- "15% due to high risk of misinterpretation if not properly executed."

---

## Weight Redistribution for Custom Criteria

When adding custom criteria:

1. **Determine custom criterion weight** based on its importance (typically 10-15%)
2. **Calculate reduction factor**: `factor = (100 - custom_weight) / 100`
3. **Apply to existing weights**: `new_weight = old_weight × factor`
4. **Verify total** = 100%

### Example

Original grid (5 criteria):
- Clarity: 25%
- Structure: 20%
- Relevance: 20%
- Impact: 20%
- Fluidity: 15%
- **Total: 100%**

Adding SEO at 15%:
- Factor = (100 - 15) / 100 = 0.85
- Clarity: 25% × 0.85 = 21.25% → 21%
- Structure: 20% × 0.85 = 17%
- Relevance: 20% × 0.85 = 17%
- Impact: 20% × 0.85 = 17%
- Fluidity: 15% × 0.85 = 12.75% → 13%
- SEO: 15%
- **Total: 100%**

---

## Expert Adjustment

### Range

±5 points maximum on final score

### When to Apply

| Adjustment | When |
|------------|------|
| +1 to +3 | Overall coherence better than individual scores suggest |
| +4 to +5 | Exceptional quality not captured by criteria |
| -1 to -3 | General impression of carelessness |
| -4 to -5 | Fundamental flaw not reflected in criteria |

### Mandatory Justification

Always explain the adjustment:
- "+3 points: remarkable overall coherence despite average individual criteria"
- "-2 points: general impression of carelessness not captured in individual scores"
- "+4 points: exceptional creativity and originality throughout"
- "-3 points: critical logical flaw undermines entire argument"

---

## Score Calculation Formula

```
SCORE = Σ (Criterion_Score × Criterion_Weight) + Expert_Adjustment
```

### Step-by-Step Example

**Document**: Professional email  
**Severity**: Standard  
**Criteria Grid**:

| Criterion | Score /10 | Weight % | Contribution |
|-----------|-----------|----------|--------------|
| Clarity | 8 | 25% | 8 × 0.25 = 2.00 |
| Relevance | 7 | 20% | 7 × 0.20 = 1.40 |
| Action orientation | 6 | 20% | 6 × 0.20 = 1.20 |
| Formal tone | 8 | 15% | 8 × 0.15 = 1.20 |
| Structure | 7 | 12% | 7 × 0.12 = 0.84 |
| Conciseness | 5 | 8% | 5 × 0.08 = 0.40 |

**Subtotal**: 2.00 + 1.40 + 1.20 + 1.20 + 0.84 + 0.40 = **7.04 → 70.4/100**

**Expert Adjustment**: +2 (good overall impression despite weak conciseness)

**Final Score**: 70.4 + 2 = **72/100** (Good)

---

## Severity Level Impact on Scores

### Gentle Mode (`doux`)

- Individual scores: +1 to +2 compared to standard
- Expert adjustment: tends toward positive
- Interpretation: emphasize strengths

### Standard Mode (`standard`)

- Individual scores: as observed
- Expert adjustment: balanced
- Interpretation: balanced critique

### Strict Mode (`strict`)

- Individual scores: -1 to -2 compared to standard
- Expert adjustment: tends toward negative
- Interpretation: emphasize areas for improvement

### Example: Same Document, Different Modes

| Criterion | Gentle | Standard | Strict |
|-----------|--------|----------|--------|
| Clarity | 9 | 8 | 7 |
| Structure | 8 | 7 | 6 |
| Impact | 7 | 6 | 5 |
| **Score** | ~78 | ~70 | ~62 |

---

## Score Interpretation Thresholds

| Range | Level | Action Required |
|-------|-------|-----------------|
| 0-49 | Insufficient | Substantial rework, consider restructuring |
| 50-69 | Acceptable | Functional but needs significant improvements |
| 70-84 | Good | Solid quality, minor polish recommended |
| 85-100 | Excellent | Ready for use, minimal adjustments if any |

---

## Re-evaluation Rules

When re-evaluating after rewrite:

1. **Use identical criteria grid** (same criteria, same weights)
2. **Re-score each criterion** based on rewritten version
3. **Recalculate expert adjustment** if overall impression changed
4. **Calculate delta**: `Δ = Score_After - Score_Before`
5. **Expected improvement**: +5 to +20 points typically

### Improvement Assessment

| Delta | Assessment |
|-------|------------|
| < +5 | Marginal improvement |
| +5 to +10 | Solid improvement |
| +10 to +15 | Significant improvement |
| > +15 | Substantial transformation |

---

## Common Pitfalls

| Pitfall | Problem | Solution |
|---------|---------|----------|
| All scores at 7-8 | No differentiation | Force ranking, identify weakest |
| Weights don't sum to 100% | Calculation error | Always verify total |
| No weight justification | Arbitrary weighting | One sentence per weight |
| Expert adjustment > ±5 | Rules violation | Cap at ±5, explain why |
| Different grid for re-eval | Unfair comparison | Use identical grid |
