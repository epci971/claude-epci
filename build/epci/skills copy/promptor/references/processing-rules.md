# Processing Rules — Extraction Methodology

> Rules for extracting structured information from transcripts

---

## Core Principles

1. **Read entire transcript first** — Catch corrections
2. **Later statements override earlier** — Resolve contradictions
3. **Never invent** — Mark absent if not stated
4. **Preserve technical terms** — Don't translate jargon

---

## Pre-Analysis

### Full Read-Through

Always read complete transcript before extraction:
- Catch corrections ("actually", "no wait")
- Identify primary vs secondary intents
- Note constraints mentioned at the end

### Complexity Assessment

| Word Count | Classification |
|------------|----------------|
| < 50 words | Quick fix |
| 50-200 words | Standard |
| > 200 words | Major |

---

## Linguistic Normalization

### Sentence Reconstruction

**Before**:
> "Donc euh on voudrait genre un truc qui fait les factures"

**After**:
> "Le système doit générer automatiquement les factures."

**Rules**:
- Explicit subject (not "on" → "le système")
- Clear verb
- Present tense preferred
- Neutral voice (avoid je/tu/nous)

---

## Intent Prioritization

### Weighted Scoring

```
SCORE = (Development × 0.4) + (Recurrence × 0.3) + 
        (Position × 0.2) + (Emphasis × 0.1)
```

### Classification

- **Highest score** → Primary Intent → Objective
- **Second highest** → Secondary → Important Notes
- **Others** → Tertiary → Notes (if relevant)

---

## Contradiction Resolution

### Detection Markers

| French | Meaning |
|--------|---------|
| "finalement" | Decision change |
| "plutôt" | Alternative chosen |
| "non en fait" | Correction |
| "oublie ce que j'ai dit" | Explicit retraction |

### Rules

1. **Later overrides earlier**
2. **Explicit beats implicit**
3. **Specific beats general**

---

## Information Classification

```
Is it about PURPOSE/WHY?
    → Objective

Is it about CONTEXT/HOW IT WORKS?
    → Description

Is it OBSERVABLE BEHAVIOR?
    → FR (Functional Requirement)

Is it a QUALITY ATTRIBUTE?
    → NFR (Non-Functional Requirement)

Is it a TECHNICAL/BUSINESS LIMIT?
    → Constraints

Is it SECONDARY/OPTIONAL?
    → Notes
```

---

## Long Transcript (> 500 words)

### Synthesis Strategy

1. Extract skeleton first (objective, FR, constraints)
2. Condense narratives to facts
3. Preserve precision (numbers, names, specs)

### Keep vs Discard

| KEEP | DISCARD |
|------|---------|
| Objective statement | Background stories |
| Explicit FR/NFR | Reasoning |
| Technical constraints | Comparisons |
| Final decisions | Intermediate thinking |

---

## Quality Checklist

- [ ] All sections present (or absence markers)
- [ ] Valid Markdown syntax
- [ ] No transcript references
- [ ] No user references
- [ ] No invented requirements
- [ ] Contradictions resolved
- [ ] Technical terms preserved
- [ ] Self-contained
