# Nano Prompt Structure v2 — 8 Components

> Complete reference for building Nano-optimized prompts

---

## The Formula

```
[SUBJECT] + [STYLE] + [LIGHTING] + [COMPOSITION] + [MATERIALS] + [MOOD] + [QUALITY] + Negative: [NEGATIVES]
```

Each component separated by comma. `Negative:` keyword introduces exclusion list.

---

## Component 1: SUBJECT (Foundation)

### Rules
- Describe precisely the main object, character, or scene
- Include specific details: materials, colors, textures, state
- Avoid vagueness: "a car" ❌ → "a sleek electric sedan in midnight blue" ✅

### Templates by Type

| Type | Template |
|------|----------|
| Product | "A [material] [product] in [finish/color] with [details]" |
| Person | "A [descriptor] [person type], [age], [expression], [clothing]" |
| Scene | "A [mood] [location] with [key elements]" |
| Object | "A [adjective] [object] made of [material] with [features]" |
| Interior | "A [style] [room type] with [key furniture], [architectural features]" |

### Examples
```
✅ "A premium wireless headphone in midnight black with rose gold accents"
✅ "A spacious bedroom with white walls, light oak parquet, large bay window"
❌ "A product" (too vague)
❌ "A nice room" (no details)
```

---

## Component 2: STYLE (One Only)

### Critical Rule
**Choose ONE style. Never combine multiple styles.**

❌ "watercolor + photorealistic + anime"
✅ "photorealistic"

### Available Styles

| Style | Best For | Keywords |
|-------|----------|----------|
| **Photorealistic** | Products, portraits, architecture, interiors | photorealistic, hyperrealistic |
| **3D Render** | Products, characters, objects | 3D render, 3D figurine, CGI |
| **Digital Art** | Illustrations, concepts | digital art, digital illustration |
| **Oil Painting** | Artistic, classic feel | oil painting, classical art |
| **Watercolor** | Soft, artistic | watercolor art, aquarelle |
| **Vector/Flat** | Icons, logos, UI | vector art, flat design |
| **Cinematic** | Scenes, moods | cinematic, film still |
| **Architectural** | Buildings, spaces | architectural render, visualization |

---

## Component 3: LIGHTING (Mood Setter)

### Rules
- NEVER vague: "good lighting" ❌
- Specify: source + quality + direction
- Match mood to use case

### Lighting Vocabulary

| Aspect | Options |
|--------|---------|
| **Source** | studio softbox, natural window, golden hour sun, neon, rim light, backlight |
| **Quality** | soft diffused, harsh dramatic, even flat, contrasty |
| **Direction** | from left, from right, from above, backlit, side-lit |
| **Color** | warm golden, cool blue, neutral white, warm accents |

### Templates by Mood

| Mood | Lighting Template |
|------|-------------------|
| Professional | "soft diffused studio light, neutral tones" |
| Luxury | "soft studio light with warm golden accents" |
| Dramatic | "harsh dramatic side lighting with deep shadows" |
| Natural | "soft natural window light, morning sun" |
| Cinematic | "neon rim lighting with warm streetlight glow" |
| Editorial | "dramatic side lighting, high contrast" |

---

## Component 4: COMPOSITION (Camera Work)

### Rules
- Use photography terminology (lens, aperture, angle)
- Specify aspect ratio
- Define framing and perspective

### Photography Terms

| Element | Options |
|---------|---------|
| **Focal Length** | 35mm (wide), 50mm (standard), 85mm (portrait), 100mm (macro), 200mm (telephoto) |
| **Aperture** | f/1.8 (shallow DOF), f/2.8 (product), f/4 (balanced), f/8 (sharp), f/11 (landscape) |
| **Angle** | eye level, low angle, high angle, aerial view, worm's eye |
| **Framing** | centered, rule of thirds, symmetrical, off-center |
| **Distance** | close-up, medium shot, wide shot, extreme close-up |

### Aspect Ratios

| Ratio | Use Case |
|-------|----------|
| 1:1 | Instagram, square formats |
| 4:3 | Standard photo, web |
| 16:9 | Hero images, widescreen |
| 9:16 | Stories, vertical mobile |
| 21:9 | Ultra-wide, cinematic |

---

## Component 5: MATERIALS & TEXTURES (NEW v2)

### Rules
- Describe primary surfaces and finishes
- Specify texture level (smooth, rough, grained)
- Include finish type (matte, glossy, brushed, weathered)
- Crucial for avoiding generic/plastic AI renders

### Vocabulary

| Category | Terms |
|----------|-------|
| **Wood** | oak, birch, walnut, pine, bamboo, driftwood + grain visible, polished, raw, weathered |
| **Metal** | brushed aluminum, polished chrome, matte black metal, brass, copper, oxidized steel |
| **Stone** | marble, granite, concrete, sandstone, slate + polished, rough, veined |
| **Fabric** | linen, cotton, silk, velvet, wool, leather + soft texture, structured, flowing |
| **Glass** | frosted, clear, tinted, textured, crystal + reflective, translucent, matte |
| **Ceramic** | porcelain, terracotta, stoneware + glazed, matte, handmade |
| **Organic** | natural wood grain, visible fibers, stone veins, leather patina |

### Templates by Use Case

```
Product:      "[material] with [finish], [texture detail]"
Interior:     "[floor material], [wall finish], [textile on furniture]"
Portrait:     "[clothing fabric texture], [jewelry material if present]"
Architecture: "[facade material], [structural elements], [surface finish]"
```

---

## Component 6: MOOD & ATMOSPHERE (NEW v2)

### Rules
- Encode the emotional/narrative intention
- One coherent mood (no contradictions)
- Must align with lighting and style choices

### Vocabulary by Mood

| Mood | Prompt Formulation |
|------|-------------------|
| Professional | "clean corporate atmosphere, business confidence" |
| Dramatic | "intense cinematic tension, high-stakes atmosphere" |
| Warm | "cozy intimate warmth, inviting domestic comfort" |
| Minimalist | "serene quiet simplicity, contemplative space" |
| Luxurious | "opulent refined elegance, exclusive premium feel" |
| Energetic | "dynamic vibrant energy, movement and life" |
| Natural | "authentic organic calm, earthy grounded serenity" |
| Modern | "sleek contemporary edge, forward-thinking design" |
| Vintage | "nostalgic timeless charm, analog warmth" |

### Mood × Use Case Examples

| Use Case | Warm | Luxurious |
|----------|------|-----------|
| Product | "handcrafted artisanal warmth on natural surface" | "luxury magazine hero shot, exclusive feel" |
| Portrait | "warm lifestyle portrait, approachable intimacy" | "high-fashion editorial, refined elegance" |
| Architecture | "welcoming interior, lived-in comfort" | "luxury real estate showcase, aspirational" |
| Cinematic | "indie film intimacy, golden nostalgia" | "Bond-like opulence, grand scale" |

---

## Component 7: QUALITY (Final Polish)

### Rules
- Add 2-3 quality signals maximum
- Adapt signals to the style chosen
- Don't overload with redundant terms

### Templates by Style

| Style | Quality Signals |
|-------|-----------------|
| Product | "4K professional quality, sharp product detail, premium studio render" |
| Portrait | "4K high detail, sharp facial features, professional headshot" |
| Cinematic | "4K cinematic detail, deep saturated colors, film grain" |
| Architecture | "4K architectural visualization, sharp detail, professional render" |
| Interior | "4K professional interior quality, natural warm tones, sharp detail" |
| Art | "high detail professional art quality, vibrant colors" |

---

## Component 8: NEGATIVES (What NOT to Generate)

### Critical Rules
- **Plain descriptions only**: list items to avoid
- **NO instruction words**: never use "no", "don't", "avoid", "without"
- Adapt to use case
- **ALWAYS include**: `watermark, generated AI watermark` (Nano/Gemini adds watermark by default)

### Format
```
Negative: item1, item2, item3, watermark, generated AI watermark
```

### Common Negatives by Use Case

| Use Case | Negatives |
|----------|-----------|
| **Product** | harsh shadows, reflections, fingerprints, dust, busy background, text, watermark, generated AI watermark |
| **Portrait** | harsh shadows, unfocused eyes, unnatural skin, blur, glasses reflection, watermark, generated AI watermark |
| **Interior** | dark corners, clutter, people, extreme distortion, watermark, generated AI watermark |
| **Scene** | people, cars, low quality, blur, washed colors, text, watermark, generated AI watermark |
| **Architecture** | people, cars, construction, blur, washed colors, text, watermark, generated AI watermark |
| **Illustration** | blur, modern elements, unfinished style, watermark, generated AI watermark |
| **Text/Logo** | blurry text, distorted label, extra text, misspelling, watermark, generated AI watermark |

### Anti-Patterns

| ❌ Don't | ✅ Do |
|----------|-------|
| "Negative: no blur" | "Negative: blur" |
| "Negative: avoid text" | "Negative: text" |
| "Negative: don't show shadows" | "Negative: harsh shadows" |
| Forget watermark | ALWAYS include "watermark, generated AI watermark" |

---

## Complete Example (8 Components)

### Product E-commerce
```
A sleek wireless headphone in midnight black and rose gold finish,
photorealistic,
soft diffused studio light on white backdrop,
50mm product shot f/2, centered composition on white surface,
brushed matte black plastic housing, polished rose gold metal accents, soft leather ear cushions,
premium studio showcase, editorial confidence,
4K professional quality, premium studio render,
Negative: shadows, reflections, extra parts, blur, sketch style, watermark, generated AI watermark
```

### Interior Architecture
```
A spacious bedroom with white walls, light oak parquet floor, large bay window,
king-size bed with white linen bedding centered against far wall,
photorealistic interior photography,
soft morning light from large window on the left, warm golden tones, gentle shadows,
35mm interior shot f/4, eye level from room entrance, balanced composition,
raw oak wood grain on floor and bed frame, crisp white linen texture, matte white walls,
peaceful morning serenity, boutique hotel comfort, airy brightness,
4K professional interior quality, natural warm tones,
Negative: dark corners, clutter, people, extreme wide angle distortion, cold bluish tint, text, watermark, generated AI watermark
```
