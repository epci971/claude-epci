# Evaluation Criteria v2

> 10 criteria for quality indicator (🟢🟡🔴) + 1 bonus for Mode B

---

## Overview

Quality indicator determined by evaluating the prompt against 10 weighted criteria. Evaluation happens in background — user only sees the indicator. In Mode B, an additional bonus criterion checks image-prompt alignment.

---

## The 10 Criteria

| # | Criterion | Weight | What It Measures |
|---|-----------|--------|------------------|
| 1 | Subject Clarity | 13% | Is the subject specific and detailed? |
| 2 | Style Uniqueness | 13% | Is there ONE coherent style? |
| 3 | Lighting Precision | 10% | Is lighting specific, not vague? |
| 4 | Composition Rigor | 10% | Are photo terms used correctly? |
| 5 | Materials & Textures | 10% | Are surface details present and specific? (NEW) |
| 6 | Mood & Atmosphere | 10% | Is emotional/narrative intent encoded? (NEW) |
| 7 | Quality Signals | 8% | Are quality markers present and adapted? |
| 8 | Negatives Relevance | 8% | Are negatives appropriate, formatted, and include anti-watermark? |
| 9 | Global Coherence | 10% | Do all elements work together? |
| 10 | Brand Compliance | 8% | Does it match provided guidelines? |

**Mode B Bonus**:
| 11 | Image-Prompt Alignment | Evaluated separately | Is the prompt coherent with what images show? |

---

## Criterion 1: Subject Clarity (13%)

| Score | Description | Example |
|-------|-------------|---------|
| 5/5 | Precise subject with rich details | "A premium skincare serum in frosted glass with gold cap and minimalist label" |
| 4/5 | Clear subject, some details missing | "A skincare bottle with gold cap" |
| 3/5 | Identifiable but generic | "A cosmetic product" |
| 2/5 | Vague, needs interpretation | "A nice bottle" |
| 1/5 | Missing or incomprehensible | "Something beautiful" |

---

## Criterion 2: Style Uniqueness (13%)

| Score | Description |
|-------|-------------|
| 5/5 | Single coherent style, well-formulated |
| 4/5 | Clear style, minor formulation issue |
| 3/5 | Style present but too generic |
| 2/5 | Multiple styles mentioned |
| 1/5 | Contradictory styles or missing |

**Critical Rule**: Any style mixing = automatic max 2/5

---

## Criterion 3: Lighting Precision (10%)

| Score | Description | Example |
|-------|-------------|---------|
| 5/5 | Source + quality + direction + color | "soft diffused studio light with warm golden accents from right side" |
| 4/5 | Two of three elements present | "soft studio light from left" |
| 3/5 | Type mentioned without detail | "studio lighting" |
| 2/5 | Vague descriptor | "good lighting" |
| 1/5 | Missing or meaningless | "nice light" or absent |

---

## Criterion 4: Composition Rigor (10%)

| Score | Description |
|-------|-------------|
| 5/5 | Focal + aperture + angle + framing |
| 4/5 | Most photo terms present |
| 3/5 | Basic framing, partial terms |
| 2/5 | Vague framing |
| 1/5 | No composition info |

---

## Criterion 5: Materials & Textures (10%) — NEW

| Score | Description | Example |
|-------|-------------|---------|
| 5/5 | Specific materials + finishes + texture detail | "raw oak wood grain on floor, crisp white linen texture, matte ceramic pots" |
| 4/5 | Materials named with some finish detail | "wooden floor, linen sofa, ceramic" |
| 3/5 | Generic material mentions | "wood and fabric" |
| 2/5 | Vague or single material | "natural materials" |
| 1/5 | Missing entirely | No material/texture info |

**Note**: For Illustration use case, this criterion adapts — "visible brushstrokes, paper texture" counts as valid material description.

---

## Criterion 6: Mood & Atmosphere (10%) — NEW

| Score | Description | Example |
|-------|-------------|---------|
| 5/5 | Specific emotional + narrative atmosphere | "peaceful morning serenity, boutique hotel comfort, airy brightness" |
| 4/5 | Clear mood with some narrative context | "warm cozy atmosphere, inviting" |
| 3/5 | Generic mood | "nice atmosphere" |
| 2/5 | Mood implied but not explicit | Only visible through other components |
| 1/5 | Missing or contradictory mood | No mood info or conflicting signals |

**Critical Rule**: Mood must align with lighting and style. "Dramatic mood" + "flat even light" = coherence penalty on criterion 9.

---

## Criterion 7: Quality Signals (8%)

| Score | Description |
|-------|-------------|
| 5/5 | 2-3 targeted signals, style-appropriate |
| 4/5 | Signals present, slightly generic |
| 3/5 | One signal only |
| 2/5 | Signals present but mismatched |
| 1/5 | Missing or contradictory |

---

## Criterion 8: Negatives Relevance (8%)

| Score | Description |
|-------|-------------|
| 5/5 | Relevant list, correct format, use-case adapted, includes anti-watermark |
| 4/5 | Good list with anti-watermark, minor relevance issue |
| 3/5 | Present but too generic, anti-watermark included |
| 2/5 | Format error OR missing anti-watermark |
| 1/5 | Missing or completely wrong |

**Critical Rules**:
- Any "no", "don't", "avoid" in negatives = automatic max 2/5
- Missing "watermark, generated AI watermark" = automatic max 3/5

---

## Criterion 9: Global Coherence (10%)

| Score | Description |
|-------|-------------|
| 5/5 | All 8 components perfectly aligned |
| 4/5 | Coherent with 1 minor mismatch |
| 3/5 | Generally coherent, 2 issues |
| 2/5 | Noticeable contradictions |
| 1/5 | Major conflicts |

### Contradiction Examples

| Element A | Element B | Conflict |
|-----------|-----------|----------|
| "minimalist" mood | "highly detailed busy scene" subject | ❌ |
| "dramatic lighting" | "flat even light" | ❌ |
| "professional portrait" | "35mm wide shot" | ❌ |
| "natural organic" mood | "neon cyberpunk" style | ❌ |
| "warm cozy" mood | "cool bluish" palette | ❌ |
| "matte surfaces" materials | "highly reflective" quality | ❌ |

---

## Criterion 10: Brand Compliance (8%)

### With brand guidelines

| Score | Description |
|-------|-------------|
| 5/5 | All brand elements integrated, forbidden elements avoided |
| 4/5 | Most brand elements present |
| 3/5 | Partial compliance |
| 2/5 | Significant brand mismatch |
| 1/5 | Brand completely ignored |

### Without brand guidelines
| 3/5 | Neutral baseline |

---

## Bonus Criterion 11: Image-Prompt Alignment (Mode B only)

Evaluated separately, does not affect the weighted score but is displayed alongside.

| Score | Description |
|-------|-------------|
| 5/5 | Prompt perfectly describes/extends what images show |
| 4/5 | Minor misalignment (e.g., prompt describes different material than visible) |
| 3/5 | Partial alignment, some elements not matching |
| 2/5 | Significant contradictions between prompt and images |
| 1/5 | Prompt ignores or contradicts image content |

**Display format**: "📎 Alignement image-prompt : [score]/5"

---

## Indicator Calculation

### Step 1: Score Each Criterion (1-5)

### Step 2: Apply Weights

```
Weighted Score =
  (Subject × 0.13) +
  (Style × 0.13) +
  (Lighting × 0.10) +
  (Composition × 0.10) +
  (Materials × 0.10) +
  (Mood × 0.10) +
  (Quality × 0.08) +
  (Negatives × 0.08) +
  (Coherence × 0.10) +
  (Brand × 0.08)

Max = 5.0
```

### Step 3: Determine Indicator

| Weighted Score | Indicator |
|----------------|-----------|
| ≥ 4.0 | 🟢 **Prêt** |
| 3.0 - 3.9 | 🟡 **Améliorable** |
| < 3.0 | 🔴 **À retravailler** |

### Alternative Rule-Based

| Condition | Indicator |
|-----------|-----------|
| 7+ criteria at 4-5/5, none at 1-2/5 | 🟢 |
| 5-6 criteria at 4-5/5, max 2 at 2/5 | 🟡 |
| <5 criteria at 4-5/5 OR any at 1/5 | 🔴 |

---

## Improvement Suggestions

When indicator is 🟡 or 🔴, auto-generate suggestions based on weak criteria:

| Weak Criterion | Suggested Question |
|----------------|-------------------|
| Subject | "Peux-tu préciser les matériaux, couleurs ou détails du sujet ?" |
| Style | "Quel style unique veux-tu ? (photo, illustration, 3D...)" |
| Lighting | "Quelle ambiance lumineuse ? (studio doux, dramatique, naturel...)" |
| Composition | "Quel cadrage préfères-tu ? (gros plan, plan large, angle)" |
| Materials | "Quels matériaux/surfaces sont importants ? (bois, métal, tissu...)" |
| Mood | "Quelle émotion/atmosphère vises-tu ? (cozy, luxe, épuré...)" |
| Quality | — (auto-fix: add appropriate signals) |
| Negatives | — (auto-fix: add use-case defaults + anti-watermark) |
| Coherence | "Incohérence entre [X] et [Y]. Que préfères-tu garder ?" |
| Brand | "Le prompt ne respecte pas [élément charte]. Dois-je ajuster ?" |
| Image-Prompt (B) | "Le prompt semble en décalage avec l'image [N] sur [aspect]. Clarifier ?" |
