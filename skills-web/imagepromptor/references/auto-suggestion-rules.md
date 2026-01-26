# Auto-Suggestion Rules

> Detection patterns for automatic parameter filling

---

## Overview

When user provides a vague idea, imagepromptor analyzes keywords and context to auto-fill the 10 parameters. This happens silently — user sees suggested values they can modify.

---

## The 10 Parameters

| # | Parameter | Source |
|---|-----------|--------|
| 1 | Subject | Direct extraction from input |
| 2 | Use case | Keyword detection |
| 3 | Style | Use case + mood indicators |
| 4 | Mood/Ambiance | Adjective detection |
| 5 | Lighting | Mood + use case combination |
| 6 | Framing | Use case defaults |
| 7 | Ratio | Channel/platform detection |
| 8 | Palette | Brand if provided, else mood |
| 9 | Negatives | Use case defaults |
| 10 | Text content | Explicit mention detection |

---

## Use Case Detection

### Keywords → Use Case Mapping

| Keywords Detected | Use Case | Confidence Boost |
|-------------------|----------|------------------|
| `produit`, `e-commerce`, `packshot`, `boutique`, `article`, `vente` | Product | +30% |
| `scène`, `cinéma`, `film`, `dramatique`, `ambiance` | Cinematic | +30% |
| `portrait`, `personne`, `visage`, `headshot`, `profil` | Portrait | +30% |
| `bâtiment`, `immo`, `architecture`, `intérieur`, `maison` | Architecture | +30% |
| `illustration`, `art`, `dessin`, `peinture`, `artistique` | Illustration | +30% |
| `texte`, `logo`, `affiche`, `titre`, `label` | Text-Logo | +30% |
| `modifier`, `changer`, `remplacer`, `éditer` | Image-to-Image | +30% |
| `série`, `variations`, `déclinaisons`, `collection` | Series | +30% |

### Confidence Calculation

```
Base confidence: 50%
+ Primary keyword match: +30%
+ Secondary keyword match: +10%
+ Context reinforcement: +10%
Maximum: 95%
```

### Ambiguous Cases

If multiple use cases score similarly:
- List top 2-3 with confidence
- Ask user to confirm
- Example: "Cas détecté : Produit (67%) ou Portrait (58%) — lequel ?"

---

## Style Detection

### Mood → Style Mapping

| Mood Keywords | Suggested Style |
|---------------|-----------------|
| `réaliste`, `photo`, `authentique` | photorealistic |
| `3D`, `render`, `figurine` | 3D render |
| `illustration`, `dessin` | digital illustration |
| `peinture`, `artistique`, `classique` | oil painting / digital painting |
| `minimaliste`, `flat`, `icône` | vector art, flat design |
| `cinéma`, `film`, `dramatique` | cinematic photoreal |

### Use Case → Style Defaults

| Use Case | Default Style |
|----------|---------------|
| Product | photorealistic |
| Cinematic | cinematic photoreal |
| Portrait | photorealistic |
| Architecture | photorealistic architecture render |
| Illustration | digital painting |
| Text-Logo | photorealistic product render |
| Image-to-Image | (preserve original) |
| Series | (consistent with base) |

---

## Mood Detection

### Adjective Mapping

| Detected Adjectives | Mood Category |
|---------------------|---------------|
| `professionnel`, `corporate`, `sérieux` | Professional |
| `dramatique`, `intense`, `puissant` | Dramatic |
| `chaleureux`, `accueillant`, `cozy` | Warm |
| `minimaliste`, `épuré`, `simple` | Minimalist |
| `luxueux`, `premium`, `haut de gamme` | Luxurious |
| `énergique`, `dynamique`, `vibrant` | Energetic |
| `naturel`, `organique`, `bio` | Natural |
| `moderne`, `contemporain`, `tech` | Modern |
| `vintage`, `rétro`, `classique` | Vintage |

---

## Lighting Suggestions

### Mood × Use Case → Lighting

| Mood | Product | Portrait | Scene | Architecture |
|------|---------|----------|-------|--------------|
| Professional | soft diffused studio | soft studio from left | even natural light | overcast soft light |
| Dramatic | dramatic side light | dramatic rim light | neon + contrast | golden hour dramatic |
| Warm | warm golden accents | warm golden tones | golden hour | sunset warm |
| Minimalist | flat even light | soft flat light | clean bright | bright overcast |
| Luxurious | soft studio + gold | soft + warm accents | ambient luxury | golden hour |
| Natural | natural window | natural soft | natural daylight | natural light |

### Default Lighting Formulas

```
Professional = "soft diffused studio light, neutral tones"
Dramatic = "dramatic [direction] lighting with deep shadows"
Warm = "[source] light with warm golden tones"
Natural = "soft natural [source] light"
Luxurious = "soft studio light with warm golden accents"
```

---

## Ratio Detection

### Platform Keywords → Ratio

| Keywords | Suggested Ratio |
|----------|-----------------|
| `Instagram`, `insta`, `post`, `feed` | 1:1 |
| `story`, `stories`, `reels`, `TikTok` | 9:16 |
| `site web`, `hero`, `banner`, `header` | 16:9 |
| `cinéma`, `film`, `widescreen` | 21:9 |
| `portrait`, `vertical` | 4:5 or 9:16 |
| `paysage`, `landscape`, `horizontal` | 16:9 |

### Use Case → Ratio Defaults

| Use Case | Default Ratio |
|----------|---------------|
| Product | 1:1 |
| Cinematic | 16:9 or 21:9 |
| Portrait | 4:3 |
| Architecture | 16:9 |
| Illustration | varies |
| Text-Logo | varies by format |

---

## Palette Detection

### From Brand Guidelines

If user provides brand description, extract:
- Primary color mentions (hex, names)
- Secondary/accent colors
- Forbidden colors
- Tone descriptors

### From Mood (no brand provided)

| Mood | Suggested Palette |
|------|-------------------|
| Professional | neutral, blue, gray, white |
| Warm | orange, gold, brown, cream |
| Natural | green, earth tones, beige |
| Luxurious | gold, black, cream, deep colors |
| Energetic | bright, saturated, contrast |
| Minimalist | white, gray, single accent |
| Vintage | muted, sepia, desaturated |

---

## Negative Suggestions

### Use Case → Default Negatives

| Use Case | Auto-Suggested Negatives |
|----------|--------------------------|
| Product | harsh shadows, reflections, fingerprints, dust, busy background, text, watermark |
| Cinematic | blur, washed out, low quality, sketch, text, watermark |
| Portrait | harsh shadows, unfocused eyes, unnatural skin, blur, glasses reflection |
| Architecture | people, cars, construction, blur, washed colors, text |
| Illustration | blur, modern elements, watermark, text, unfinished style |
| Text-Logo | blurry text, distorted label, extra text, misspelling |
| Image-to-Image | distorted subject, unnatural transitions, washed colors |
| Series | inconsistency, style breaks |

### Universal Negatives (always consider)

```
blur, low quality, watermark
```

Add `text` if no text is wanted in the image.

---

## Text Detection

### Trigger Keywords

`texte`, `écrit`, `titre`, `label`, `logo`, `"..."` (quoted text)

### Extraction Rules

1. If quoted text found → extract as content
2. If `logo` mentioned → expect brand name
3. If `titre` or `title` → expect headline

### Auto-Suggestions for Text

| Detected Context | Typography Suggestion |
|------------------|----------------------|
| Logo, brand | bold sans-serif |
| Title, headline | bold, large |
| Label, product | clean sans-serif |
| Elegant, luxury | elegant serif |
| Modern, tech | futuristic sans-serif |

---

## Confidence Display Format

```markdown
## 📋 Brief détecté

**Cas** : Product (87%) · **Style** : Photoréaliste · **Ratio** : 1:1

| Paramètre | Suggestion | Indice utilisé |
|-----------|------------|----------------|
| Sujet | Bouteille cosmétique premium | "cosmétique" dans input |
| Éclairage | Studio doux + touches dorées | mood "luxe" détecté |
| Ratio | 1:1 | "Instagram" mentionné |

*[Modifier un paramètre ?]*
```

---

## Edge Cases

### No Clear Keywords
- Default to Product if object-like
- Default to Scene if environment-like
- Ask clarifying question if truly ambiguous

### Contradictory Keywords
- "photo réaliste illustration" → Flag contradiction, ask user
- "minimaliste chargé" → Flag contradiction, ask user

### Missing Critical Info
- No subject at all → Ask "Quel est le sujet principal ?"
- No platform/ratio hint → Default to 1:1 (most versatile)

---

## Example Analysis

**Input**: 
> "Je veux une image pour mon site e-commerce de cosmétiques bio, ambiance luxe naturel pour Instagram"

**Analysis**:

| Signal | Detection | Confidence |
|--------|-----------|------------|
| "e-commerce" | → Product | +30% |
| "cosmétiques" | → Product (reinforce) | +10% |
| "bio" | → Natural mood | — |
| "luxe" | → Luxurious mood | — |
| "naturel" | → Natural mood | — |
| "Instagram" | → Ratio 1:1 | — |

**Result**:
```
Cas: Product (89%)
Style: Photoréaliste
Mood: Luxueux + Naturel
Lighting: Soft studio + warm golden accents
Ratio: 1:1
Palette: Earth tones, gold accents, cream
Negatives: shadows, reflections, artificial feel, plastic, text
```
