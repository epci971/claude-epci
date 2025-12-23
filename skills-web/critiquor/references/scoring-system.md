# Scoring System

> Complete reference for CRITIQUOR's scoring, radar visualization, confidence levels, and delta tracking

---

## Visual Radar

### Format

Display at the end of every critique:

```
📊 Radar des critères

Clarté        ████████████████░░░░ 78/100
Structure     ██████████████░░░░░░ 68/100
Impact        ████████████░░░░░░░░ 58/100 ⚠️
Pertinence    ██████████████████░░ 88/100 ✓
Ton           ████████████████░░░░ 75/100
Concision     ██████░░░░░░░░░░░░░░ 32/100 ❌

Score global: 67/100 — Acceptable 🎯
```

### Bar Generation

| Score | Bar (20 chars total) |
|-------|---------------------|
| 100 | `████████████████████` |
| 90 | `██████████████████░░` |
| 80 | `████████████████░░░░` |
| 70 | `██████████████░░░░░░` |
| 60 | `████████████░░░░░░░░` |
| 50 | `██████████░░░░░░░░░░` |
| 40 | `████████░░░░░░░░░░░░` |
| 30 | `██████░░░░░░░░░░░░░░` |
| 20 | `████░░░░░░░░░░░░░░░░` |
| 10 | `██░░░░░░░░░░░░░░░░░░` |

### Indicator Legend

| Indicator | Meaning | Score Range |
|-----------|---------|-------------|
| `✓` | Strong criterion | ≥85 |
| (none) | Acceptable | 66-84 |
| `⚠️` | Needs attention | 50-65 |
| `❌` | Weak criterion | <50 |

---

## Confidence Level

### Definition

Indicates how reliable the score is based on available information.

| Level | Icon | Conditions |
|-------|------|------------|
| **High** | 🎯 | Document >200 words AND clear theme AND context provided |
| **Medium** | 📊 | Document 50-200 words OR hybrid/unclear theme |
| **Low** | ⚠️ | Document <50 words OR missing critical context |

### Display Format

```
Score: 72/100 — Bon 🎯 (confiance haute)
Score: 65/100 — Acceptable 📊 (confiance moyenne — document court)
Score: 58/100 — Acceptable ⚠️ (confiance basse — contexte manquant)
```

### Factors Affecting Confidence

| Factor | Impact |
|--------|--------|
| Document length | <50 words = low, 50-200 = medium, >200 = high |
| Theme clarity | Clear single theme = +1, hybrid = 0, unclear = -1 |
| Context provided | Audience/intent specified = +1, missing = -1 |
| Technical content | Verifiable claims = +1, subjective = 0 |

---

## Score Interpretation

### Levels

| Range | Level | Description | Action Required |
|-------|-------|-------------|-----------------|
| 0-49 | Insuffisant | Major issues | Substantial rework, consider restructuring |
| 50-69 | Acceptable | Functional | Significant improvements possible |
| 70-84 | Bon | Solid quality | Minor polish recommended |
| 85-100 | Excellent | High quality | Minimal adjustments if any |

### Visual Badges

```
Score: 45/100 — Insuffisant ❌
Score: 62/100 — Acceptable ⚠️
Score: 76/100 — Bon ✓
Score: 91/100 — Excellent ⭐
```

---

## Delta & Trends (Iterate Mode)

### Delta Display

For successive critiques of the same document:

```
📈 Évolution

| Critère    | v1    | v2    | Δ     |
|------------|-------|-------|-------|
| Clarté     | 58    | 78    | +20 ↑ |
| Structure  | 62    | 68    | +6 ↗  |
| Impact     | 55    | 58    | +3 →  |
| Ton        | 70    | 65    | -5 ↘  |

Score global: 58 → 72 (+14 points) 📈
```

### Trend Indicators

| Indicator | Meaning | Delta Range |
|-----------|---------|-------------|
| `↑` | Strong improvement | +10 or more |
| `↗` | Improvement | +5 to +9 |
| `→` | Stable | -4 to +4 |
| `↘` | Regression | -5 to -9 |
| `↓` | Strong regression | -10 or less |

### Regression Alert

When a criterion regresses, flag it explicitly:

```
### ⚠️ Régression détectée

**Structure** (-8 points ↘) : La nouvelle intro crée une redondance avec la section 2.
Suggestion : Supprimer le paragraphe 2 de la section 2, déjà couvert dans l'intro.
```

---

## Section Scores (Long Documents)

### Trigger

Activate for documents >2000 words OR documents with clear sections (headers, chapters).

### Display Format

```
📊 Scores par section

| Section        | Score | Point faible           |
|----------------|-------|------------------------|
| Introduction   | 75    | —                      |
| Contexte       | 62    | Trop dense             |
| Proposition    | 81    | —                      |
| Argumentation  | 68    | Preuves insuffisantes  |
| Conclusion     | 54    | Call-to-action flou    |

Score consolidé: 68/100 — Acceptable
Pondération: Introduction 15%, Contexte 20%, Proposition 25%, Argumentation 25%, Conclusion 15%
```

### Section Weighting

| Section Type | Typical Weight |
|--------------|----------------|
| Introduction/Accroche | 10-15% |
| Context/Background | 15-20% |
| Main content/Body | 40-50% |
| Conclusion/CTA | 15-20% |

---

## Expert Adjustment

### Range

±5 points maximum on final score

### When to Apply

| Adjustment | Condition |
|------------|-----------|
| +1 to +3 | Overall coherence better than individual scores suggest |
| +4 to +5 | Exceptional quality not captured by criteria |
| -1 to -3 | General impression of carelessness |
| -4 to -5 | Fundamental flaw not reflected in criteria |

### Mandatory Justification

Always explain the adjustment:

```
**Ajustement expert**: +3 points — Cohérence remarquable malgré des scores individuels moyens
**Ajustement expert**: -2 points — Impression générale de négligence non capturée par les critères
```

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

**Final Score**: 70.4 + 2 = **72/100** (Bon)

---

## Severity Impact on Scores

### Gentle Mode (`--doux`)

- Individual scores: +1 to +2 compared to standard
- Expert adjustment: tends toward positive
- Interpretation: emphasize strengths

### Standard Mode (`--standard`)

- Individual scores: as observed
- Expert adjustment: balanced
- Interpretation: balanced critique

### Strict Mode (`--strict`)

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
