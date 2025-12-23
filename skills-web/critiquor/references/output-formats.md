# Output Formats

> Complete reference for all CRITIQUOR v2 output templates

---

## Standard Mode Output Structure

### 1. Analysis Header

```markdown
## 📋 CRITIQUOR Analysis

[Persona icon] [Persona name] [Opening phrase]...

**Detected theme**: [Main theme] (+ secondary if applicable) [Confidence icon]
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

### 3. Visual Radar (NEW v2)

```markdown
## 📊 Radar des critères

Clarté        ████████████████░░░░ 78/100
Structure     ██████████████░░░░░░ 68/100
Impact        ████████████░░░░░░░░ 58/100 ⚠️
Pertinence    ██████████████████░░ 88/100 ✓
Ton           ████████████████░░░░ 75/100
Concision     ██████░░░░░░░░░░░░░░ 32/100 ❌
```

---

### 4. Global Score

```markdown
## 🎯 Global Score

**Score: XX/100** — [Level] [Confidence icon] (confiance [haute/moyenne/basse])

**Expert adjustment**: ±X points — [Justification]
```

---

### 5. Qualitative Analysis

```markdown
## 📝 Qualitative Analysis

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

### 6. Factual Errors Section (if applicable)

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

### 7. Four-Block Table

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

### 8. Breakpoint 1

```markdown
---
🛑 **Analysis complete.**

Would you like me to generate a rewritten and re-evaluated version?
```

---

### 9. Rewrite Preparation (Phase 1.5)

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

### 10. Rewritten Version (Phase 2)

```markdown
## ✍️ Rewritten Version

[Complete optimized document - full text]
```

---

### 11. Modifications Table

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

### 12. Comparative Re-evaluation with Delta (NEW v2)

```markdown
## 📈 Comparative Re-evaluation

| Criterion | Score Before | Score After | Δ |
|-----------|--------------|-------------|---|
| Clarity | 6/10 | 8/10 | +2 ↗ |
| Structure | 5/10 | 8/10 | +3 ↗ |
| Impact | 6/10 | 7/10 | +1 → |
| ... | ... | ... | ... |

---

**Score before**: XX/100 — [Interpretation]
**Score after**: YY/100 — [Interpretation]
**Improvement**: +ZZ points [Trend icon]
```

---

### 13. Breakpoint 2 (Satisfaction Check)

```markdown
---
🛑 **Does this rewritten version meet your expectations?**

I can adjust specific elements if needed.
```

---

## Express Mode Output (NEW v2)

```markdown
## ⚡ CRITIQUOR Express

[Persona icon] [Persona] Analyse rapide...

**Score: XX/100** — [Level] [Confidence icon]

📊 Radar
Clarté      ████████████████░░░░ 78
Structure   ██████████████░░░░░░ 65
Impact      ██████████░░░░░░░░░░ 52 ⚠️
Pertinence  ██████████████████░░ 85 ✓
Ton         ████████████████░░░░ 72

💪 **Forces** : [Point 1], [Point 2], [Point 3]
⚠️ **Faiblesses** : [Point 1], [Point 2], [Point 3]
🎯 **Priorité #1** : [Single most impactful improvement in 1-2 sentences]

---
Critique complète ? → `approfondir`
```

---

## Focus Mode Output (NEW v2)

```markdown
## 🔍 CRITIQUOR Focus — [Section Name]

[Persona icon] [Persona] Concentrons-nous sur [section]...

**Score section: XX/100** [Indicator]

| Criterion | Score /10 | Analysis |
|-----------|-----------|----------|
| [Section-specific] | X | [Analysis] |
| ... | ... | ... |

📊 Radar section
[Mini radar]

### 💡 Recommendations

1. [Specific recommendation]
2. [Specific recommendation]

### ✍️ Suggested rewrite (section only)

[Rewritten section if applicable]

---
Critique du document entier ? → `critique complète`
```

---

## Compare Mode Output (NEW v2)

```markdown
## ⚖️ CRITIQUOR Comparatif

[Persona icon] [Persona] Analysons les deux versions...

### 📊 Comparison Table

| Criterion | Version A | Version B | Verdict |
|-----------|-----------|-----------|---------|
| Clarity | 65 | 78 | B +13 ✓ |
| Structure | 72 | 68 | A +4 |
| Impact | 58 | 71 | B +13 ✓ |
| Tone | 75 | 74 | ≈ |
| **Global** | **67** | **73** | **B +6** |

### 🏆 Verdict

**Version [X] recommended** (+Z points)

**What A does better**:
- [Point 1]
- [Point 2]

**What B does better**:
- [Point 1]
- [Point 2]

### 💡 Optimal Version

[Suggestion for combining best elements]

---
Generate this fused version? → `fusionner`
```

---

## Iterate Mode Output (NEW v2)

```markdown
## 🔁 CRITIQUOR Itération #N

[Persona icon] [Persona] Analyse des modifications...

### Changements détectés

- [Section] : [status: réécrite/modifiée/inchangée] [✓/⚠️]
- ...

### Impact sur le score

| Criterion | Before | After | Δ |
|-----------|--------|-------|---|
| Clarity | 65 | 78 | +13 ↑ |
| Impact | 58 | 72 | +14 ↑ |
| Structure | 72 | 70 | -2 → |

**Score: XX → YY (+/-Z)** [Trend icon]

### ⚠️ Regression Detected (if any)

**[Criterion]** (-X points [trend]): [Explanation]
Suggestion: [How to fix]

### ✅ Improvements Confirmed

- [What improved and why]

---
Continue iterating? Provide next version.
```

---

## Checklist Mode Output (NEW v2)

```markdown
## ✅ CRITIQUOR Checklist

📋 Pre-send validation: [Document type]

| Check | Status | Detail |
|-------|--------|--------|
| ✅ Spelling | OK | No errors detected |
| ✅ Grammar | OK | Syntax correct |
| ✅ Tone | OK | Professional, appropriate |
| ⚠️ Length | ATTENTION | 450 words — may be too long |
| ✅ CTA | OK | Clear meeting request |
| ❌ Subject | MISSING | No subject line provided |
| ✅ Personalization | OK | Client name used |
| ⚠️ Urgency | LOW | No deadline mentioned |

**Verdict: X/Y checks OK** — [Recommendation]

🎯 **Actions before sending**:
1. [Action 1]
2. [Action 2]
3. [Optional action]

---
Full critique? → `critique complète`
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
🛑 **Analysis complete.** Rewrite specific sections or entire document?
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
- `Code` for technical terms and commands

### Separators
- Use `---` between major sections
- Use blank lines for visual spacing

### Emojis Reference

| Emoji | Usage |
|-------|-------|
| 📋 | Analysis / Overview |
| 📊 | Scores / Data / Radar |
| 🎯 | Results / Goals |
| 📝 | Text / Writing |
| ⚠️ | Warnings / Errors / Attention needed |
| 💡 | Suggestions / Ideas |
| ❓ | Questions |
| ✍️ | Rewriting |
| 🔄 | Changes / Comparison |
| 📈 | Improvement |
| 🛑 | Breakpoint / Stop |
| ⚡ | Express mode |
| 🔍 | Focus mode |
| ⚖️ | Compare mode |
| 🔁 | Iterate mode |
| ✅ | Checklist / Validation |
| 🎓 | Mentor persona |
| ✂️ | Editor persona |
| 😈 | Devil's Advocate persona |
| 👤 | Target Reader persona |
| ✓ | Strong criterion (≥85) |
| ❌ | Weak criterion (<50) |
| ↑↗→↘↓ | Trend indicators |
