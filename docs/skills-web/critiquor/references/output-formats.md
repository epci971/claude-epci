# Output Formats

> Complete reference for all CRITIQUOR output templates

---

## Complete Mode Output Structure

### 1. Analysis Header

```markdown
## 📋 CRITIQUOR Analysis

**Detected theme**: [Main theme] (+ secondary if applicable)
**Identified intention**: [Inform / Convince / Sell / Narrate / Structure / Reassure]
**Target audience**: [Audience description]
**Severity level**: [gentle / standard / strict]
**Custom criteria**: [Listed if any, or "None"]
```

---

### 2. Weighted Criteria Grid

```markdown
## 📊 Criteria Evaluation

| Criterion | Score /10 | Weight % | Weight Justification | Analysis |
|-----------|-----------|----------|----------------------|----------|
| [Name] | X | XX% | [1 sentence] | [Detailed analysis] |
| [Custom: Name]* | X | XX% | [1 sentence] | [Detailed analysis] |
| ... | ... | ... | ... | ... |

*Custom criteria marked with asterisk
```

---

### 3. Global Score

```markdown
## 🎯 Global Score

**Score: XX/100** (level [standard]) — [Interpretation: Insufficient/Acceptable/Good/Excellent]

**Expert adjustment**: ±X points — [Justification]
```

---

### 4. Qualitative Analysis

```markdown
## 📝 Qualitative Analysis

[Structured paragraphs covering relevant aspects:]

**Tone and Register**
[Analysis of tone appropriateness...]

**Structure and Organization**
[Analysis of document structure...]

**Logical Coherence**
[Analysis of argument flow...]

**Clarity and Readability**
[Analysis of comprehension ease...]

**Relevance to Audience**
[Analysis of audience fit...]

**Impact**
[Analysis of effectiveness...]
```

---

### 5. Factual Errors Section (if applicable)

```markdown
## ⚠️ Factual Errors Detected

| Error Type | Location | Description | Impact |
|------------|----------|-------------|--------|
| Numerical error | Section 2, para 3 | Revenue figure incorrect (stated 2M, should be 1.8M) | -2 on Rigor |
| Logical contradiction | Intro vs Conclusion | Conflicting statements about timeline | -1 on Coherence |
| ... | ... | ... | ... |
```

If no errors detected, this section is omitted entirely.

---

### 6. Four-Block Table

```markdown
## 📋 Strengths, Weaknesses, Advantages, Disadvantages

| Category | Key Points |
|----------|------------|
| **Strengths** | • [Point 1]<br>• [Point 2]<br>• [Point 3] |
| **Weaknesses** | • [Point 1]<br>• [Point 2]<br>• [Point 3] |
| **Advantages** | • [Structural/stylistic/strategic advantage 1]<br>• [Advantage 2] |
| **Disadvantages** | • [Risk/misunderstanding potential 1]<br>• [Risk 2] |
```

---

### 7. Breakpoint 1

```markdown
---
🛑 **Analysis complete.**

Would you like me to generate a rewritten and re-evaluated version?
```

---

### 8. Rewrite Preparation (Phase 1.5)

```markdown
## 💡 Improvement Suggestions

**Structural improvements**:
- [Suggestion 1 with specific location]
- [Suggestion 2 with specific location]

**Stylistic improvements**:
- [Suggestion 1]
- [Suggestion 2]

**Logical improvements**:
- [Suggestion 1]

**Recommended additions**:
- [Element to add and where]

**Elements to simplify or remove**:
- [Element and reason]

**Suggested reformulations**:
- "[Original phrase]" → "[Proposed phrase]"
- "[Original]" → "[Proposed]"

---

## ❓ Framing Questions

Before rewriting, some clarifications:

1. [Question about objective if ambiguous]
2. [Question about audience if uncertain]
3. [Question about constraints: length, tone, elements to preserve]
4. [Other relevant question]

Answer these questions or indicate "proceed with your recommendations".
```

---

### 9. Rewritten Version (Phase 2)

```markdown
## ✍️ Rewritten Version

[Complete optimized document - full text]
```

---

### 10. Modifications Table

```markdown
## 🔄 Key Modifications

| Modified Element | Before | After | Reason |
|------------------|--------|-------|--------|
| Opening | "[Original opening]" | "[New opening]" | More engaging hook |
| Section 2 structure | Paragraph format | Bullet points | Improved scannability |
| CTA | "[Original CTA]" | "[New CTA]" | Clearer action request |
| ... | ... | ... | ... |
```

---

### 11. Comparative Re-evaluation

```markdown
## 📈 Comparative Re-evaluation

| Criterion | Score Before | Score After | Δ |
|-----------|--------------|-------------|---|
| Clarity | 6/10 | 8/10 | +2 |
| Structure | 5/10 | 8/10 | +3 |
| Impact | 6/10 | 7/10 | +1 |
| ... | ... | ... | ... |

---

**Score before**: XX/100 — [Interpretation]
**Score after**: YY/100 — [Interpretation]
**Improvement**: +ZZ points
```

---

### 12. Breakpoint 2 (Satisfaction Check)

```markdown
---
🛑 **Does this rewritten version meet your expectations?**

I can adjust specific elements if needed.
```

---

## Summary Mode Output Structure

```markdown
## 📊 CRITIQUOR Summary

**Score: XX/100** — [Interpretation: Insufficient/Acceptable/Good/Excellent]

**Top 3 Strengths**:
1. [Strength 1 - brief description]
2. [Strength 2 - brief description]
3. [Strength 3 - brief description]

**Top 3 Weaknesses**:
1. [Weakness 1 - brief description]
2. [Weakness 2 - brief description]
3. [Weakness 3 - brief description]

**Main Recommendation**: [Single most impactful improvement suggestion in 1-2 sentences]

---
🛑 Want the complete analysis or a rewritten version?
```

---

## Long Document Output (Section-by-Section)

```markdown
## 📋 CRITIQUOR Analysis — Section-by-Section

**Document**: [Title/Description]
**Total sections identified**: X
**Severity level**: [standard]

---

### Section 1: [Section Title]

[Standard criteria grid for this section]

**Section Score**: XX/100

---

### Section 2: [Section Title]

[Standard criteria grid for this section]

**Section Score**: XX/100

---

[Continue for all sections...]

---

## 📊 Consolidated Results

| Section | Score | Key Issue |
|---------|-------|-----------|
| Section 1 | XX/100 | [Main issue or strength] |
| Section 2 | XX/100 | [Main issue or strength] |
| ... | ... | ... |

**Global Score**: XX/100 (weighted average)
**Expert adjustment**: ±X points — [Justification]
**Final Score**: XX/100 — [Interpretation]

---
🛑 **Analysis complete.** Would you like me to rewrite specific sections or the entire document?
```

---

## Formatting Guidelines

### Tables
- Use Markdown table syntax
- Align columns for readability
- Keep cell content concise

### Emphasis
- **Bold** for labels and key terms
- *Italic* for examples or quotes
- `Code` for technical terms

### Separators
- Use `---` between major sections
- Use blank lines for visual spacing

### Emojis
- 📋 Analysis / Overview
- 📊 Scores / Data
- 🎯 Results / Goals
- 📝 Text / Writing
- ⚠️ Warnings / Errors
- 💡 Suggestions / Ideas
- ❓ Questions
- ✍️ Rewriting
- 🔄 Changes / Comparison
- 📈 Improvement
- 🛑 Breakpoint / Stop
