# Processing Rules — Extraction Methodology

> Detailed rules for extracting structured information from transcripts

---

## Core Principles

1. **Read entire transcript before processing** — Prevents missing corrections
2. **Later statements override earlier** — Contradictions resolved by recency
3. **Never invent** — If not stated, mark as absent
4. **Preserve technical terms** — Don't translate or "improve" jargon

---

## Pre-Analysis Phase

### 1. Full Read-Through

**Always** read the complete transcript before any extraction:
- Catch later corrections ("actually", "no wait", "rather")
- Identify the primary vs secondary intents
- Note constraints mentioned at the end

### 2. Segmentation

Identify logical segments:

| Segment Type | Markers |
|--------------|---------|
| Topic introduction | "So the idea is...", "What I need is..." |
| Topic change | "Also...", "Another thing...", "Oh and..." |
| Reversal | "Actually...", "No wait...", "Let's do X instead" |
| Emphasis | "The important thing is...", "Must have...", "Priority..." |
| Uncertainty | "Maybe...", "Not sure if...", "We'll see..." |

### 3. Complexity Assessment

| Word Count | Classification | Mode |
|------------|----------------|------|
| < 50 words | Short | Quick fix (if corrective) |
| 50-200 words | Medium | Standard |
| > 200 words | Long | Major (with synthesis) |

---

## Linguistic Normalization

### Speech Artifacts to Remove

| Type | Examples | Action |
|------|----------|--------|
| Hesitations | "euh", "um", "uh", "hum" | Delete |
| Fillers | "tu vois", "genre", "quoi", "voilà" | Delete |
| Self-corrections | "non en fait", "je veux dire" | Keep corrected version only |
| Repetitions | "il faut, il faut que..." | Keep once |
| Tangents | Unrelated anecdotes | Delete |

### Sentence Reconstruction

**Before**:
> "Donc euh on voudrait genre un truc qui fait les factures tu vois et euh qui les envoie quoi"

**After**:
> "Le système doit générer et envoyer automatiquement les factures."

**Rules**:
- Explicit subject (not "on" → "le système")
- Clear verb
- Intelligible complement
- Present tense preferred
- Neutral voice (avoid je/tu/nous in brief)

### Term Preservation

Keep technical terms exactly as stated:
- API names, product names
- Acronyms (REST, CRUD, SSO, JWT)
- Domain vocabulary (TCB, Brix, etc.)
- Stack names (Symfony, React, Django)

**Never** translate or "correct" technical jargon.

---

## Intent Prioritization

### Weighted Scoring

For each distinct intent in transcript:

```
SCORE = (Development × 0.4) + (Recurrence × 0.3) + (Position × 0.2) + (Emphasis × 0.1)
```

### Scoring Criteria

**Development (40%)**
| Words dedicated | Score |
|-----------------|-------|
| < 20 words | 1 |
| 20-50 words | 2 |
| 50-100 words | 3 |
| > 100 words | 4 |

**Recurrence (30%)**
| Mentions | Score |
|----------|-------|
| Once | 1 |
| 2-3 times | 2 |
| 4+ times | 3 |
| Running theme | 4 |

**Position (20%)**
| Location | Score |
|----------|-------|
| Early only (first quarter) | 1 |
| Middle | 2 |
| Late (final quarter) | 3 |
| Conclusion position | 4 |

**Emphasis (10%)**
| Markers | Score |
|---------|-------|
| None | 1 |
| "important" | 2 |
| "must have", "priority" | 3 |
| "the main thing is..." | 4 |

### Classification

- **Highest score** → Primary Intent → Objective
- **Second highest** → Secondary → Important Notes
- **Others** → Tertiary → Important Notes (if relevant)

---

## Contradiction Resolution

### Detection Markers

| French | English | Meaning |
|--------|---------|---------|
| "finalement" | "finally", "in the end" | Decision change |
| "plutôt" | "rather", "instead" | Alternative chosen |
| "non en fait" | "actually no" | Correction |
| "oublie ce que j'ai dit" | "forget what I said" | Explicit retraction |
| "on va faire comme ça" | "let's do it this way" | Final decision |

### Resolution Rules

1. **Later overrides earlier**: Last stated position wins
2. **Explicit beats implicit**: "Let's do X" > implied Y
3. **Specific beats general**: "Use PostgreSQL" > "some database"

### Documentation

In brief's Notes section (only if context-useful):
```markdown
## Notes

- Une approche fichiers CSV initialement envisagée puis abandonnée 
  au profit d'une intégration API directe.
```

---

## Information Classification

### Decision Tree

For each piece of information:

```
Is it about PURPOSE/WHY?
    YES → Objective
    NO ↓

Is it about CONTEXT/HOW IT WORKS generally?
    YES → Description
    NO ↓

Is it an OBSERVABLE BEHAVIOR the system must perform?
    YES → FR (Functional Requirement)
    NO ↓

Is it a QUALITY ATTRIBUTE (performance, security, UX)?
    YES → NFR (Non-Functional Requirement)
    NO ↓

Is it a TECHNICAL/BUSINESS LIMIT?
    YES → Constraints
    NO ↓

Is it SECONDARY, OPTIONAL, or FOR LATER?
    YES → Important Notes
    NO → Probably noise, discard
```

### Classification Examples

| Statement | Classification |
|-----------|---------------|
| "Enable automated invoice generation" | Objective |
| "Integrates with existing ERP via REST API" | Description |
| "Users can export reports to PDF" | FR |
| "Response time < 2 seconds" | NFR |
| "Must use PostgreSQL" | Constraint |
| "Maybe add batch export later" | Notes |

---

## Long Transcript Handling

### Synthesis Strategy (> 500 words)

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

### Keep vs Discard

| KEEP | DISCARD |
|------|---------|
| Objective statement | Background stories |
| Explicit FR/NFR | Reasoning justifications |
| Technical constraints | Comparisons with other projects |
| Final decisions | Intermediate thinking |
| Specific numbers/dates | Vague time references |
| Named integrations | General wishes |

---

## Poor/Vague Transcript Handling

### Minimum Viable Brief

Even from minimal input, produce:
- Title (even generic: "Fonctionnalité à définir")
- Objective (even partial)
- Explicit absence markers for missing sections

### Never Invent

**Wrong**:
> "Le système devra probablement aussi gérer les utilisateurs."

**Correct**:
> "Aucun FR explicitement mentionné dans la source."

---

## Quality Checklist

Before outputting brief:

### Structure
- [ ] All sections present (or absence markers)
- [ ] Valid Markdown syntax
- [ ] Header with complexity/time/confidence

### Content
- [ ] No transcript references ("le transcript", "la transcription")
- [ ] No user references ("l'utilisateur demande")
- [ ] No invented requirements
- [ ] Contradictions resolved (latest version only)
- [ ] Technical terms preserved exactly

### Quality
- [ ] Self-contained (readable without source)
- [ ] Professional tone
- [ ] Absence markers where needed
- [ ] Confidence level appropriate to content

---

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Multiple distinct features | Multi-task detection |
| No clear intent at all | LOW confidence, generic title |
| All constraints, no features | Focus on context, note FR needs definition |
| Technical jargon unknown | Preserve exactly, don't interpret |
| Contradictory final statements | Flag as unresolved, LOW confidence |
