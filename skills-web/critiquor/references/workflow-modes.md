# Workflow Modes

> Complete reference for CRITIQUOR's 5 critique modes + standard workflow

---

## Modes Overview

| Mode | Command | Purpose | Output |
|------|---------|---------|--------|
| **Standard** | (default) | Full analysis + rewrite | Complete critique + optional rewrite |
| **Express** | `--express` | Quick validation | Score + radar + 3 key points |
| **Focus** | `--focus [target]` | Section-specific | Targeted critique |
| **Compare** | `--compare` | Version comparison | Side-by-side analysis |
| **Iterate** | `--iterate` | Revision tracking | Delta-focused feedback |
| **Checklist** | `--checklist` | Pre-send validation | Pass/fail checks |

---

## Standard Mode (Default)

### When to Use

- First critique of a document
- When complete analysis is needed
- When rewrite is likely desired

### Workflow

```
Document
    │
    ▼
┌─────────────────────────────────┐
│  PHASE 1: CRITIQUE              │
│  1. Theme detection             │
│  2. Persona selection           │
│  3. Grid construction           │
│  4. Criterion scoring           │
│  5. Global score + radar        │
│  6. Qualitative analysis        │
│  7. Four-block table            │
└─────────────────────────────────┘
    │
    ▼
🛑 BREAKPOINT 1
"Analysis complete. Rewrite?"
    │
    ├── No → END
    │
    ▼ Yes
┌─────────────────────────────────┐
│  PHASE 1.5: PREPARATION         │
│  1. Improvement suggestions     │
│  2. Framing questions           │
│  3. User answers                │
└─────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────┐
│  PHASE 2: REWRITE               │
│  1. Complete rewrite            │
│  2. Modifications table         │
│  3. Re-evaluation (same grid)   │
│  4. Delta display               │
└─────────────────────────────────┘
    │
    ▼
🛑 BREAKPOINT 2
"Satisfied? Adjustments?"
    │
    ├── Yes → END
    │
    ▼ Adjustments
PHASE 3: REFINEMENT
```

### Output Template

```markdown
## 📋 CRITIQUOR Analysis

[Persona icon] [Persona] [Opening]...

**Detected theme**: [Theme] (+ secondary if applicable)
**Identified intention**: [Intent]
**Target audience**: [Audience]
**Severity level**: [standard/doux/strict]

## 📊 Criteria Evaluation

| Criterion | Score /10 | Weight % | Analysis |
|-----------|-----------|----------|----------|
| ... | ... | ... | ... |

## 📊 Radar des critères

[Visual radar]

**Score: XX/100** — [Level] [Confidence]

**Expert adjustment**: ±X points — [Justification]

## 📝 Qualitative Analysis

[Structured analysis paragraphs]

## ⚠️ Factual Errors (if any)

| Error Type | Location | Description | Impact |
|------------|----------|-------------|--------|

## 📋 Strengths / Weaknesses / Advantages / Disadvantages

| Category | Key Points |
|----------|------------|
| **Strengths** | • ... |
| **Weaknesses** | • ... |
| **Advantages** | • ... |
| **Disadvantages** | • ... |

---
🛑 **Analysis complete.** Rewritten version?
```

---

## Express Mode (`--express` / `--quick`)

### When to Use

- Quick validation before sending
- Triage of multiple documents
- When only score matters
- Time-constrained situations

### Characteristics

| Aspect | Behavior |
|--------|----------|
| Output length | ~30% of standard |
| Grid display | No (radar only) |
| Qualitative analysis | No |
| Breakpoints | No |
| Rewrite offer | No (suggest `approfondir`) |

### Output Template

```markdown
## ⚡ CRITIQUOR Express

[Persona icon] [Persona] Analyse rapide...

**Score: XX/100** — [Level] [Confidence]

📊 Radar
Clarté      ████████████████░░░░ 78
Structure   ██████████████░░░░░░ 65
Impact      ██████████░░░░░░░░░░ 52 ⚠️
Pertinence  ██████████████████░░ 85 ✓
Ton         ████████████████░░░░ 72

💪 **Forces** : [3 points, comma-separated]
⚠️ **Faiblesses** : [3 points, comma-separated]
🎯 **Priorité #1** : [Single most impactful recommendation]

---
Critique complète ? → `approfondir`
```

### Exiting Express Mode

- Command: `approfondir`
- Effect: Restarts with full standard analysis
- Context: Preserves document and initial observations

---

## Focus Mode (`--focus [target]`)

### When to Use

- Specific section needs work
- Iterating on one part
- Time-limited feedback on specific area

### Available Targets

| Command | Target |
|---------|--------|
| `--focus intro` | Introduction / opening |
| `--focus conclusion` | Conclusion / CTA |
| `--focus section:N` | Numbered section |
| `--focus "Section Title"` | Named section |
| `--focus argumentation` | Argument chain only |
| `--focus accroche` | Hook / opening line |

### Characteristics

| Aspect | Behavior |
|--------|----------|
| Scope | Single section only |
| Grid | Adapted to section type |
| Score | Section score (not global) |
| Rewrite | Section only if requested |

### Output Template

```markdown
## 🔍 CRITIQUOR Focus — [Section Name]

[Persona icon] [Persona] Concentrons-nous sur [section]...

**Score section: XX/100** [Indicator]

| Criterion | Score /10 | Analysis |
|-----------|-----------|----------|
| [Section-specific criterion] | X | ... |
| ... | ... | ... |

📊 Radar section
[Mini radar for section criteria]

### 💡 Recommendations

1. [Specific recommendation]
2. [Specific recommendation]

### ✍️ Suggested rewrite (section only)

[If applicable]

---
Critique du document entier ? → `critique complète`
```

### Section-Specific Criteria

| Section | Key Criteria |
|---------|--------------|
| Introduction | Hook strength, context clarity, promise, transition |
| Conclusion | Summary, CTA clarity, memorability, closing strength |
| Argumentation | Logic chain, evidence, counterargument handling |
| Body sections | Relevance, depth, flow, examples |

---

## Compare Mode (`--compare`)

### When to Use

- Choosing between two versions
- A/B testing content
- Evaluating revision effectiveness

### Input Format

```
compare
[Version A text]
---
[Version B text]
```

Or with files:
```
compare [file1] vs [file2]
```

### Characteristics

| Aspect | Behavior |
|--------|----------|
| Grid | Same grid for both versions |
| Output | Side-by-side comparison |
| Verdict | Clear winner recommendation |
| Fusion | Optional combined version |

### Output Template

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

**Version B recommended** (+6 points)

**What A does better**:
- [Point 1]
- [Point 2]

**What B does better**:
- [Point 1]
- [Point 2]
- [Point 3]

### 💡 Optimal Version

Combine A's structure with B's tone. Specifically:
1. Keep B's opening hook
2. Use A's body organization
3. Close with B's CTA

---
Generate this fused version? → `fusionner`
```

### Fusion Command

After compare, `fusionner` generates a new version combining the best of both, then critiques it.

---

## Iterate Mode (`--iterate`)

### When to Use

- Working through multiple revisions
- Tracking improvement over time
- Ensuring changes had positive impact

### Characteristics

| Aspect | Behavior |
|--------|----------|
| Memory | Stores previous critique in session |
| Focus | Changes only (unless major revision) |
| Output | Delta-focused, regression alerts |
| Iteration count | Tracked and displayed |

### Behavior

1. First iteration: Full standard critique
2. Subsequent iterations:
   - Detect modified sections
   - Re-score changed criteria
   - Display deltas and trends
   - Alert on regressions

### Output Template

```markdown
## 🔁 CRITIQUOR Itération #N

[Persona icon] [Persona] Analyse des modifications...

### Changements détectés

- Introduction : réécrite ✓
- Section 2 : modifiée
- Conclusion : inchangée

### Impact sur le score

| Criterion | Before | After | Δ |
|-----------|--------|-------|---|
| Clarity | 65 | 78 | +13 ↑ |
| Impact | 58 | 72 | +14 ↑ |
| Structure | 72 | 70 | -2 → |

**Score: 67 → 75 (+8)** 📈

### ⚠️ Regression Detected (if any)

**[Criterion]** (-X points [trend]): [Explanation]
Suggestion: [How to fix]

### ✅ Improvements Confirmed

- [What improved and why]

---
Continue iterating? Provide next version.
```

---

## Checklist Mode (`--checklist`)

### When to Use

- Final validation before send/publish
- Quick pass/fail assessment
- Ensuring nothing is forgotten

### Characteristics

| Aspect | Behavior |
|--------|----------|
| Output | Binary checks (pass/fail) |
| Depth | Surface-level only |
| Score | X/Y checks passed |
| Focus | Completeness, not quality |

### Document-Type Checklists

#### Email Checklist
| Check | What |
|-------|------|
| Spelling | No errors |
| Grammar | Correct syntax |
| Tone | Appropriate |
| Length | Suitable for context |
| CTA | Present and clear |
| Subject line | Provided and effective |
| Personalization | Name/context used |
| Urgency | If needed, present |

#### Proposal Checklist
| Check | What |
|-------|------|
| Executive summary | Present |
| Problem statement | Clear |
| Solution | Articulated |
| Pricing | Included |
| Timeline | Defined |
| CTA/Next steps | Explicit |
| Contact info | Present |
| Proofreading | No errors |

### Output Template

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

**Verdict: 6/8 checks OK** — Minor adjustments recommended

🎯 **Actions before sending**:
1. Add subject line
2. Consider adding deadline for response
3. Optional: trim ~100 words

---
Full critique? → `critique complète`
```

---

## Mode Selection Guide

| Situation | Recommended Mode |
|-----------|------------------|
| First look at a document | Standard |
| "Is this ready to send?" | Express or Checklist |
| "Which version is better?" | Compare |
| "How did my changes help?" | Iterate |
| "Just fix my intro" | Focus |
| "Quick score please" | Express |
| Multiple revision rounds | Iterate |
| Final pre-publish check | Checklist |

---

## Commands Summary

| Command | Effect |
|---------|--------|
| `critique` | Standard mode |
| `--express` / `--quick` | Express mode |
| `--focus [target]` | Focus mode |
| `--compare` / `compare` | Compare mode |
| `--iterate` | Iterate mode |
| `--checklist` | Checklist mode |
| `approfondir` | Express → Standard |
| `fusionner` | After compare, generate optimal |
| `critique complète` | From any mode → Standard |
