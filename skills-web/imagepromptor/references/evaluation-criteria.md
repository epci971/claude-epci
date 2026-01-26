# Evaluation Criteria

> 8 criteria for quality indicator (🟢🟡🔴)

---

## Overview

The quality indicator is determined by evaluating the generated prompt against 8 weighted criteria. The evaluation happens in the background — user only sees the indicator, not the detailed scores.

---

## The 8 Criteria

| # | Criterion | Weight | What It Measures |
|---|-----------|--------|------------------|
| 1 | Subject Clarity | 15% | Is the subject specific and detailed? |
| 2 | Style Uniqueness | 15% | Is there ONE coherent style? |
| 3 | Lighting Precision | 12% | Is lighting specific, not vague? |
| 4 | Composition Rigor | 12% | Are photo terms used correctly? |
| 5 | Quality Signals | 10% | Are quality markers present and adapted? |
| 6 | Negatives Relevance | 10% | Are negatives appropriate and formatted? |
| 7 | Global Coherence | 13% | Do all elements work together? |
| 8 | Brand Compliance | 13% | Does it match provided guidelines? |

---

## Criterion 1: Subject Clarity (15%)

### What to Evaluate
- Is the main subject clearly identifiable?
- Are specific details included (materials, colors, textures)?
- Is there enough information for Nano to render accurately?

### Scoring

| Score | Description | Example |
|-------|-------------|---------|
| 5/5 | Precise subject with rich details | "A premium skincare serum in frosted glass with gold cap and minimalist label" |
| 4/5 | Clear subject, some details missing | "A skincare bottle with gold cap" |
| 3/5 | Identifiable but generic | "A cosmetic product" |
| 2/5 | Vague, needs interpretation | "A nice bottle" |
| 1/5 | Missing or incomprehensible | "Something beautiful" |

---

## Criterion 2: Style Uniqueness (15%)

### What to Evaluate
- Is exactly ONE style specified?
- Is the style appropriate for the use case?
- Are there NO contradictory style elements?

### Scoring

| Score | Description | Example |
|-------|-------------|---------|
| 5/5 | Single coherent style, well-formulated | "photorealistic" |
| 4/5 | Clear style, minor formulation issue | "photo realistic style" |
| 3/5 | Style present but too generic | "realistic" |
| 2/5 | Multiple styles mentioned | "photorealistic illustration" |
| 1/5 | Contradictory styles or missing | "watercolor photorealistic anime" |

### Critical Rule
**Any style mixing = automatic max 2/5**

---

## Criterion 3: Lighting Precision (12%)

### What to Evaluate
- Is the light source specified?
- Is the light quality described (soft, harsh, diffused)?
- Is the direction indicated?

### Scoring

| Score | Description | Example |
|-------|-------------|---------|
| 5/5 | Source + quality + direction specified | "soft diffused studio light with warm accents from right side" |
| 4/5 | Two of three elements present | "soft studio light from left" |
| 3/5 | Type mentioned without detail | "studio lighting" |
| 2/5 | Vague descriptor | "good lighting" |
| 1/5 | Missing or meaningless | "nice light" or absent |

---

## Criterion 4: Composition Rigor (12%)

### What to Evaluate
- Are photography terms used (focal, aperture)?
- Is the framing/angle specified?
- Is the aspect ratio indicated or implied?

### Scoring

| Score | Description | Example |
|-------|-------------|---------|
| 5/5 | Focal + aperture + angle + framing | "85mm f/1.8, centered composition, shallow depth of field" |
| 4/5 | Most photo terms present | "85mm portrait, shallow DOF" |
| 3/5 | Basic framing, partial terms | "close-up shot, centered" |
| 2/5 | Vague framing | "from the side" |
| 1/5 | No composition info | absent |

---

## Criterion 5: Quality Signals (10%)

### What to Evaluate
- Are 2-3 quality signals present?
- Are they adapted to the chosen style?
- Is there no overloading (too many redundant terms)?

### Scoring

| Score | Description | Example |
|-------|-------------|---------|
| 5/5 | 2-3 targeted signals, style-appropriate | "4K professional quality, luxury magazine aesthetic" |
| 4/5 | Signals present, slightly generic | "high quality, detailed" |
| 3/5 | One signal only | "4K" |
| 2/5 | Signals present but mismatched | "8K sketch quality" |
| 1/5 | Missing or contradictory | absent |

---

## Criterion 6: Negatives Relevance (10%)

### What to Evaluate
- Are negatives present?
- Are they formatted correctly (no "no", "don't", "avoid")?
- Are they relevant to the use case?

### Scoring

| Score | Description | Example |
|-------|-------------|---------|
| 5/5 | Relevant list, correct format, use-case adapted | "Negative: harsh shadows, fingerprints, dust, reflections, text" |
| 4/5 | Good list, minor format or relevance issue | "Negative: blur, bad quality, shadows" |
| 3/5 | Present but too generic | "Negative: blur, low quality" |
| 2/5 | Format error OR irrelevant | "Negative: no blur, don't show text" |
| 1/5 | Missing or completely wrong | absent or "Negative: avoid everything bad" |

### Critical Rule
**Any "no", "don't", "avoid" in negatives = automatic max 2/5**

---

## Criterion 7: Global Coherence (13%)

### What to Evaluate
- Do all elements reinforce each other?
- Is there internal consistency (mood, style, lighting align)?
- Are there NO contradictions?

### Scoring

| Score | Description | Example Issue |
|-------|-------------|---------------|
| 5/5 | All elements perfectly aligned | — |
| 4/5 | Coherent with 1 minor mismatch | Slightly mismatched lighting for mood |
| 3/5 | Generally coherent, 2 issues | Energetic mood with soft flat lighting |
| 2/5 | Noticeable contradictions | Minimalist style with busy composition |
| 1/5 | Major conflicts | Luxurious mood with sketch style |

### Contradiction Examples

| Element A | Element B | Conflict |
|-----------|-----------|----------|
| "minimalist" | "highly detailed busy scene" | ❌ |
| "dramatic lighting" | "flat even light" | ❌ |
| "professional portrait" | "35mm wide shot" | ❌ |
| "natural organic" | "neon cyberpunk" | ❌ |

---

## Criterion 8: Brand Compliance (13%)

### What to Evaluate
- If brand guidelines provided: are they respected?
- If no guidelines: is this criterion neutral (3/5 baseline)?
- Are forbidden elements excluded?

### Scoring (with brand guidelines)

| Score | Description |
|-------|-------------|
| 5/5 | All brand elements integrated, forbidden elements avoided |
| 4/5 | Most brand elements present, minor gaps |
| 3/5 | Partial compliance, some elements missing |
| 2/5 | Significant brand mismatch |
| 1/5 | Brand completely ignored or contradicted |

### Scoring (no brand guidelines)

| Score | Description |
|-------|-------------|
| 3/5 | Neutral baseline (no guidelines to comply with) |

---

## Indicator Calculation

### Step 1: Score Each Criterion (1-5)

```
Subject:     ?/5
Style:       ?/5
Lighting:    ?/5
Composition: ?/5
Quality:     ?/5
Negatives:   ?/5
Coherence:   ?/5
Brand:       ?/5
```

### Step 2: Apply Weights

```
Weighted Score = 
  (Subject × 0.15) + 
  (Style × 0.15) + 
  (Lighting × 0.12) + 
  (Composition × 0.12) + 
  (Quality × 0.10) + 
  (Negatives × 0.10) + 
  (Coherence × 0.13) + 
  (Brand × 0.13)

Max = 5.0
```

### Step 3: Determine Indicator

| Weighted Score | Indicator | Meaning |
|----------------|-----------|---------|
| ≥ 4.0 | 🟢 **Prêt** | Ready to use |
| 3.0 - 3.9 | 🟡 **Améliorable** | Functional, can improve |
| < 3.0 | 🔴 **À retravailler** | Needs significant work |

### Alternative Rule-Based Detection

| Condition | Indicator |
|-----------|-----------|
| 6+ criteria at 4-5/5, none at 1-2/5 | 🟢 |
| 4-5 criteria at 4-5/5, max 2 at 2/5 | 🟡 |
| <4 criteria at 4-5/5 OR any at 1/5 | 🔴 |

---

## Improvement Suggestions

When indicator is 🟡 or 🔴, auto-generate suggestions based on weak criteria:

| Weak Criterion | Suggested Question |
|----------------|-------------------|
| Subject | "Peux-tu préciser les matériaux, couleurs ou détails du sujet ?" |
| Style | "Quel style unique veux-tu ? (photo, illustration, 3D...)" |
| Lighting | "Quelle ambiance lumineuse ? (studio doux, dramatique, naturel...)" |
| Composition | "Quel cadrage préfères-tu ? (gros plan, plan large, angle particulier)" |
| Quality | — (auto-fix, add appropriate signals) |
| Negatives | — (auto-fix, add use-case defaults) |
| Coherence | "Il y a une incohérence entre [X] et [Y]. Que préfères-tu garder ?" |
| Brand | "Le prompt ne respecte pas [élément charte]. Dois-je ajuster ?" |

---

## Example Evaluation

**Prompt**:
```
A premium skincare serum bottle in frosted glass with gold cap,
photorealistic,
soft diffused studio light with warm golden accents from right,
100mm macro f/2.8, centered on beige marble surface, shallow depth of field,
4K professional quality, luxury magazine aesthetic,
Negative: harsh shadows, fingerprints, dust, reflections, text, watermark
```

**Evaluation**:

| Criterion | Score | Rationale |
|-----------|-------|-----------|
| Subject | 5/5 | Detailed: material, finish, specific element |
| Style | 5/5 | Single style: photorealistic |
| Lighting | 5/5 | Source + quality + direction + color |
| Composition | 5/5 | Focal + aperture + framing + surface |
| Quality | 5/5 | Two targeted signals, style-appropriate |
| Negatives | 5/5 | Relevant list, correct format |
| Coherence | 5/5 | Luxury mood aligned throughout |
| Brand | 3/5 | No guidelines provided (neutral) |

**Weighted Score**: 4.7/5.0

**Indicator**: 🟢 **Prêt**
