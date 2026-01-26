# Nano Prompt Structure — 6 Components

> Complete reference for building Nano-optimized prompts

---

## The Formula

```
[SUBJECT] + [STYLE] + [LIGHTING] + [COMPOSITION] + [QUALITY] + Negative: [NEGATIVES]
```

Each component is separated by a comma. The `Negative:` keyword introduces the exclusion list.

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

### Examples
```
✅ "A premium wireless headphone in midnight black with rose gold accents"
✅ "A confident businesswoman, age 35, natural smile, navy blazer"
✅ "A cozy coffee shop corner with warm lighting and vintage furniture"
❌ "A product" (too vague)
❌ "A nice photo" (no subject)
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
| **Photorealistic** | Products, portraits, architecture | photorealistic, hyperrealistic, photo |
| **3D Render** | Products, characters, objects | 3D render, 3D figurine, CGI |
| **Digital Art** | Illustrations, concepts | digital art, digital illustration |
| **Oil Painting** | Artistic, classic feel | oil painting, classical art |
| **Watercolor** | Soft, artistic | watercolor art, aquarelle |
| **Vector/Flat** | Icons, logos, UI | vector art, flat design, minimal illustration |
| **Cinematic** | Scenes, moods | cinematic, film still |
| **Architectural** | Buildings, spaces | architectural render, visualization |

### Examples
```
✅ "photorealistic"
✅ "digital painting oil style"
✅ "3D product render"
❌ "photorealistic watercolor" (mixing styles)
```

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

### Examples
```
✅ "soft diffused studio light with warm golden accents from right side"
✅ "golden hour backlight, long shadows, warm tones"
✅ "cold neon rim lighting with warm streetlight glow"
❌ "nice lighting" (vague)
❌ "good light" (meaningless)
```

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

### Templates

```
Product:    "100mm macro f/2.8, centered on [surface], shallow depth of field"
Portrait:   "85mm portrait f/1.8, shallow depth of field, blurred background"
Scene:      "35mm wide shot, eye level, rule of thirds composition"
Arch:       "24mm wide angle, low angle, symmetrical composition"
```

### Examples
```
✅ "85mm portrait f/1.8, centered composition, shallow depth of field"
✅ "35mm wide shot, aerial perspective, 16:9"
✅ "100mm macro f/2.8, product centered on marble surface"
❌ "zoomed in" (imprecise)
❌ "from the side" (use "side view" or angle terminology)
```

---

## Component 5: QUALITY (Final Polish)

### Rules
- Add 2-3 quality signals maximum
- Adapt signals to the style chosen
- Don't overload with redundant terms

### Quality Vocabulary

| Category | Terms |
|----------|-------|
| **Resolution** | 4K, 8K, high resolution, ultra HD |
| **Detail** | high detail, sharp detail, intricate detail |
| **Professional** | professional quality, studio quality, magazine quality |
| **Aesthetic** | premium finish, luxury aesthetic, cinematic depth |
| **Style-specific** | Vogue ad style, editorial quality, architectural visualization |

### Templates by Style

| Style | Quality Signals |
|-------|-----------------|
| Product | "4K professional quality, sharp product detail, premium studio render" |
| Portrait | "4K high detail, sharp facial features, professional headshot" |
| Cinematic | "4K cinematic detail, deep saturated colors, film grain" |
| Architecture | "4K architectural visualization, sharp detail, professional render" |
| Art | "high detail professional art quality, vibrant colors" |

### Examples
```
✅ "4K professional quality, luxury magazine aesthetic"
✅ "high detail, sharp focus, premium finish"
❌ "4K 8K ultra HD high resolution maximum detail" (overloaded)
```

---

## Component 6: NEGATIVES (What NOT to Generate)

### Critical Rules
- **Plain descriptions only**: list items to avoid
- **NO instruction words**: never use "no", "don't", "avoid", "without"
- Adapt to use case (products ≠ portraits ≠ scenes)

### Format
```
Negative: item1, item2, item3, item4
```

### Common Negatives by Use Case

| Use Case | Negatives |
|----------|-----------|
| **Product** | harsh shadows, reflections, fingerprints, dust, busy background, text, watermark |
| **Portrait** | harsh shadows, unfocused eyes, unnatural skin, blur, glasses reflection |
| **Scene** | people, cars, low quality, blur, washed colors, text |
| **Architecture** | people, cars, construction, blur, washed colors |
| **Illustration** | blur, modern elements, watermark, text, unfinished style |
| **Text/Logo** | blurry text, distorted label, extra text, misspelling |

### Universal Negatives (Almost Always Include)
```
blur, low quality, watermark, text (if no text wanted)
```

### Examples
```
✅ "Negative: harsh shadows, fingerprints, dust, reflections, text, watermark"
✅ "Negative: blur, washed out, low quality, sketch, extra limbs"
❌ "Negative: don't show shadows" (instruction word)
❌ "Negative: no blur" (instruction word)
❌ "Negative: avoid text" (instruction word)
```

---

## Complete Examples

### Product E-commerce
```
A sleek wireless headphone in midnight black and rose gold finish,
photorealistic,
soft diffused studio light on white backdrop,
50mm product shot f/2, centered composition on white surface,
4K professional quality, premium studio render,
Negative: shadows, reflections, extra parts, blur, sketch style
```

### Cinematic Scene
```
A lone figure walking through neon-lit Tokyo street at night,
cinematic photoreal,
cold neon rim lighting with warm streetlight glow,
35mm wide shot, aerial perspective, rain-soaked pavement,
4K cinematic detail, deep saturated colors,
Negative: blur, washed out, low quality, sketch, text, watermark
```

### Portrait
```
A confident business woman, age 35, natural expression,
photorealistic,
soft diffused studio light from left side, warm golden tones,
85mm portrait f/1.8, shallow depth of field, blurred background,
4K high detail, sharp facial features, professional headshot,
Negative: harsh shadows, unfocused eyes, unnatural skin, blur
```

### Architecture
```
A modern sustainable residential building with glass facade and green terraces,
photorealistic architecture render,
golden hour afternoon light, dramatic cloud shadows,
21:9 wide shot from street level, symmetrical composition, blue sky,
4K architectural visualization, sharp detail,
Negative: people, cars, low quality, blur, washed colors
```

---

## Anti-Patterns

| ❌ Don't | ✅ Do |
|----------|-------|
| Mix styles | Choose ONE style |
| "good lighting" | "soft diffused studio light from left" |
| "nice composition" | "85mm f/1.8, centered, shallow DOF" |
| "Negative: no blur" | "Negative: blur" |
| Overload quality terms | 2-3 targeted quality signals |
| Generic subject | Specific with materials, colors, details |
