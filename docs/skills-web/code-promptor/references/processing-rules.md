# Processing Rules — Detailed Extraction Methodology

> Complete reference for transcript analysis and information extraction

---

## 1. Pre-Analysis Phase

### 1.1 Full Read-Through
**Always** read the entire transcript before any processing. This prevents:
- Missing later corrections/reversals
- Misidentifying primary intent
- Overlooking constraints mentioned at the end

### 1.2 Segmentation
Mentally divide the transcript into logical segments:

| Segment Type | Markers |
|--------------|---------|
| Topic introduction | "So the idea is...", "What I need is..." |
| Topic change | "Also...", "Another thing...", "Oh and..." |
| Reversal | "Actually...", "No wait...", "Let's do X instead" |
| Emphasis | "The important thing is...", "Must have...", "Priority..." |
| Uncertainty | "Maybe...", "Not sure if...", "We'll see..." |

### 1.3 Complexity Assessment

| Word Count | Classification | Mode |
|------------|----------------|------|
| < 100 words | Short | Compact (if single intent) |
| 100-500 words | Medium | Standard |
| > 500 words | Long | Standard with synthesis |

---

## 2. Linguistic Normalization

### 2.1 Remove Speech Artifacts

| Artifact Type | Examples | Action |
|---------------|----------|--------|
| Hesitations | "euh", "um", "uh" | Delete |
| Filler words | "tu vois", "genre", "quoi", "voilà" | Delete |
| Self-corrections | "non en fait", "je veux dire" | Keep corrected version only |
| Repetitions | "il faut, il faut que..." | Keep once |
| Tangents | Unrelated personal anecdotes | Delete |

### 2.2 Sentence Reconstruction

**Before**: "Donc euh on voudrait genre un truc qui fait les factures tu vois et euh qui les envoie quoi"

**After**: "Le système doit générer et envoyer automatiquement les factures."

**Rules**:
- Explicit subject
- Clear verb
- Intelligible complement
- Present tense preferred
- Neutral voice (avoid "je/tu/nous")

### 2.3 Terminology Preservation
Keep technical terms exactly as stated:
- API names, product names
- Technical acronyms (REST, CRUD, SSO)
- Domain-specific vocabulary
- Do NOT translate or "improve" technical terms

---

## 3. Intent Prioritization Algorithm

### 3.1 Weighted Scoring System

For each distinct intent identified, calculate:

```
SCORE = (Development × 0.4) + (Recurrence × 0.3) + (Position × 0.2) + (Emphasis × 0.1)
```

### 3.2 Scoring Criteria

**Development (40%)**
| Metric | Score |
|--------|-------|
| < 20 words dedicated | 1 |
| 20-50 words | 2 |
| 50-100 words | 3 |
| > 100 words | 4 |

**Recurrence (30%)**
| Metric | Score |
|--------|-------|
| Mentioned once | 1 |
| Mentioned 2-3 times | 2 |
| Mentioned 4+ times | 3 |
| Running theme throughout | 4 |

**Position (20%)**
| Metric | Score |
|--------|-------|
| Early only (first quarter) | 1 |
| Middle | 2 |
| Late (final quarter) | 3 |
| Mentioned at end as conclusion | 4 |

**Emphasis (10%)**
| Metric | Score |
|--------|-------|
| No emphasis markers | 1 |
| Some emphasis ("important") | 2 |
| Strong emphasis ("must have", "priority") | 3 |
| Explicit primary ("the main thing is...") | 4 |

### 3.3 Intent Classification

| Result | Classification |
|--------|----------------|
| Highest score | **Primary Intent** → Objective |
| Second highest | **Secondary** → Important Notes |
| Others | **Tertiary** → Important Notes (if relevant) |

---

## 4. Contradiction Resolution

### 4.1 Detection Markers

| French | English | Meaning |
|--------|---------|---------|
| "finalement" | "finally", "in the end" | Decision change |
| "plutôt" | "rather", "instead" | Alternative chosen |
| "non en fait" | "actually no" | Correction |
| "oublie ce que j'ai dit" | "forget what I said" | Explicit retraction |
| "on va faire comme ça" | "let's do it this way" | Final decision |

### 4.2 Resolution Rules

1. **Later overrides earlier**: The last stated position is the valid one
2. **Explicit beats implicit**: "Let's do X" beats implied preference for Y
3. **Specific beats general**: "Use PostgreSQL" beats "some database"

### 4.3 Documentation

When resolving contradictions:
- Keep **only** the final version in Objective/FR
- **Optionally** note the change in Important Notes (only if context-useful)

**Example**:
```markdown
## Important Notes

- Une approche basée sur des fichiers CSV a été initialement envisagée puis 
  abandonnée au profit d'une intégration API directe.
```

---

## 5. Long Transcript Handling

### 5.1 Synthesis Strategy

For transcripts > 500 words:

1. **Extract skeleton first**:
   - Main objective
   - Explicit FR/NFR (verbatim capture)
   - Technical constraints
   - Final decisions

2. **Condense narratives**:
   - Replace stories with facts
   - Remove redundant explanations
   - Keep one instance of repeated points

3. **Preserve precision**:
   - Numbers, dates, names
   - Technical specifications
   - Explicit requirements

### 5.2 What to Keep vs Discard

| KEEP | DISCARD |
|------|---------|
| Objective statement | Background stories |
| Explicit FR/NFR | Reasoning justifications |
| Technical constraints | Comparisons with other projects |
| Final decisions | Intermediate thinking |
| Specific numbers/dates | Vague time references |
| Named integrations | General wishes |

---

## 6. Poor/Vague Transcript Handling

### 6.1 Minimum Viable Brief

Even from minimal input, produce:
- Title (even generic like "Fonctionnalité à définir")
- Objective (even partial)
- Explicit absence markers for missing sections

### 6.2 Confidence Indicators

| Scenario | Confidence | Gaps to Flag |
|----------|------------|--------------|
| Clear intent, all sections populated | HIGH | 0 |
| Clear intent, missing FR/NFR | MEDIUM | 1-2 |
| Vague intent, multiple gaps | LOW | 3+ |

### 6.3 Never Invent

**Wrong approach**:
> "Le système devra probablement aussi gérer les utilisateurs."

**Correct approach**:
> "Aucun FR explicitement mentionné dans la source."

---

## 7. Classification Decision Tree

For each piece of information:

```
Is it about PURPOSE/WHY?
    YES → Objective
    NO ↓

Is it about CONTEXT/HOW IT WORKS generally?
    YES → Description
    NO ↓

Is it an OBSERVABLE BEHAVIOR the system must perform?
    YES → FR
    NO ↓

Is it a QUALITY ATTRIBUTE (performance, security, UX)?
    YES → NFR
    NO ↓

Is it a TECHNICAL/BUSINESS LIMIT or REQUIREMENT?
    YES → Constraints
    NO ↓

Is it SECONDARY, OPTIONAL, or FOR LATER?
    YES → Important Notes
    NO → Probably noise, discard
```

---

## 8. Final Checklist

Before outputting the brief:

### Structure
- [ ] All 7 sections present (or 3 for compact mode)
- [ ] Metadata header included
- [ ] Valid Markdown syntax

### Content
- [ ] No transcript references ("le transcript", "la transcription")
- [ ] No user references ("l'utilisateur demande", "vous voulez")
- [ ] No invented requirements
- [ ] Contradictions resolved (latest version only)
- [ ] Technical terms preserved exactly

### Quality
- [ ] Self-contained (readable without source)
- [ ] Professional tone
- [ ] Absence markers where needed
- [ ] Confidence level appropriate

---

## 9. Edge Cases

| Scenario | Handling |
|----------|----------|
| Multiple distinct features | Produce brief for most developed one, note others exist |
| No clear intent at all | LOW confidence, generic title, note ambiguity |
| All constraints, no features | Focus on context, note FR needs definition |
| Technical jargon unknown | Preserve exactly as stated, don't interpret |
| Contradictory final statements | Flag as unresolved, LOW confidence |
