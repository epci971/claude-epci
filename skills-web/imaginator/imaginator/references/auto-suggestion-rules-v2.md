# Auto-Suggestion Rules v2

> Detection patterns for automatic parameter filling (12 parameters)

---

## The 12 Parameters

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
| 9 | Materials | Use case + mood combination (NEW) |
| 10 | Atmosphere | Mood + use case narrative (NEW) |
| 11 | Negatives | Use case defaults + ALWAYS watermark |
| 12 | Text content | Explicit mention detection |

---

## Use Case Detection

### Keywords → Use Case Mapping

| Keywords Detected | Use Case | Confidence Boost |
|-------------------|----------|------------------|
| `produit`, `e-commerce`, `packshot`, `boutique`, `article`, `vente` | Product | +30% |
| `scène`, `cinéma`, `film`, `dramatique`, `ambiance` | Cinematic | +30% |
| `portrait`, `personne`, `visage`, `headshot`, `profil` | Portrait | +30% |
| `bâtiment`, `immo`, `architecture`, `intérieur`, `maison`, `chambre`, `salon`, `cuisine` | Architecture | +30% |
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
+ Image analysis confirmation (Mode B): +10%
Maximum: 95%
```

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
| Architecture | photorealistic interior/architecture render |
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

---

## Materials Suggestions (NEW v2)

### Mood × Use Case → Materials

| Mood | Product | Portrait | Architecture |
|------|---------|----------|--------------|
| Professional | brushed metal, polished glass, matte plastic | structured wool, leather, silver jewelry | concrete, steel, tinted glass |
| Warm | natural wood, linen, ceramic | soft cotton, knit, amber jewelry | oak floors, exposed brick, linen curtains |
| Luxurious | marble, gold, crystal, silk | silk, velvet, gold jewelry | marble floors, brass fixtures, velvet |
| Natural | bamboo, recycled glass, cork | organic cotton, wood beads | raw stone, reclaimed wood, rattan |
| Minimalist | matte ceramic, clear glass, white plastic | simple cotton, no accessories | smooth concrete, white walls, light wood |
| Vintage | patinated metal, aged leather, amber glass | tweed, brass, pearls | weathered wood, wrought iron, terrazzo |

---

## Atmosphere Suggestions (NEW v2)

### Mood → Atmosphere Formulation

| Mood | Atmosphere (EN) |
|------|----------------|
| Professional | "clean corporate atmosphere, business confidence" |
| Dramatic | "intense cinematic tension, high-stakes atmosphere" |
| Warm | "cozy intimate warmth, inviting domestic comfort" |
| Minimalist | "serene quiet simplicity, contemplative space" |
| Luxurious | "opulent refined elegance, exclusive premium feel" |
| Energetic | "dynamic vibrant energy, movement and life" |
| Natural | "authentic organic calm, earthy grounded serenity" |
| Modern | "sleek contemporary edge, forward-thinking design" |
| Vintage | "nostalgic timeless charm, analog warmth" |

### Mood × Use Case → Atmosphere (detailed)

| Cas | Professional | Warm | Luxurious | Natural |
|-----|-------------|------|-----------|---------|
| Product | "premium studio showcase, editorial confidence" | "handcrafted artisanal warmth on natural surface" | "luxury magazine hero shot, exclusive feel" | "organic product in natural setting, raw beauty" |
| Portrait | "corporate headshot, authoritative presence" | "warm lifestyle portrait, approachable intimacy" | "high-fashion editorial, refined elegance" | "candid natural portrait, authentic expression" |
| Architecture | "professional visualization, precise geometry" | "welcoming interior, lived-in comfort" | "luxury real estate showcase, aspirational" | "biophilic design, harmony with nature" |
| Cinematic | "thriller tension, controlled precision" | "indie film intimacy, golden nostalgia" | "Bond-like opulence, grand scale" | "documentary authenticity, raw environment" |

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

---

## Negative Suggestions

### Use Case → Default Negatives

**CRITICAL: ALWAYS include "watermark, generated AI watermark" in every negative list.**

| Use Case | Auto-Suggested Negatives |
|----------|--------------------------|
| Product | harsh shadows, reflections, fingerprints, dust, busy background, text, watermark, generated AI watermark |
| Cinematic | blur, washed out, low quality, sketch, text, watermark, generated AI watermark |
| Portrait | harsh shadows, unfocused eyes, unnatural skin, blur, glasses reflection, watermark, generated AI watermark |
| Architecture | people, cars, construction, blur, washed colors, text, dark corners, watermark, generated AI watermark |
| Illustration | blur, modern elements, unfinished style, watermark, generated AI watermark |
| Text-Logo | blurry text, distorted label, extra text, misspelling, watermark, generated AI watermark |
| Image-to-Image | distorted subject, unnatural transitions, washed colors, watermark, generated AI watermark |
| Series | inconsistency, style breaks, watermark, generated AI watermark |

### Mode B Additional Negatives (per intent)

| Intent | Additional Negatives |
|--------|---------------------|
| Reproduce | elements not in reference, invented details |
| Inspire | elements from reference content (only style should transfer) |
| Transform | traces of removed elements, incomplete changes |
| Merge | mismatched wood tones, style clashes, inconsistent lighting between sources |

---

## Palette Detection

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

## Text Detection

### Trigger Keywords
`texte`, `écrit`, `titre`, `label`, `logo`, `"..."` (quoted text)

### Auto-Suggestions for Text

| Detected Context | Typography Suggestion |
|------------------|----------------------|
| Logo, brand | bold sans-serif |
| Title, headline | bold, large |
| Label, product | clean sans-serif |
| Elegant, luxury | elegant serif |
| Modern, tech | futuristic sans-serif |

---

## Mode B: Image-Based Parameter Override

When images are present, extracted visual data OVERRIDES auto-suggestions:

| Parameter | Text-only source | Image override |
|-----------|-----------------|----------------|
| Lighting | Mood × Use Case mapping | Actual lighting observed in images |
| Palette | Mood mapping or brand | Actual colors from images |
| Materials | Use Case × Mood mapping | Actual materials visible in images |
| Style | Use Case default | Style detected from images |
| Composition | Use Case default | Framing/angle observed in images |
| Mood | Adjective detection | Atmosphere felt from images |

**Rule**: Image data takes priority over text-based suggestions. Text input is used for INTENT (what to do) while images provide REALITY (what exists).
