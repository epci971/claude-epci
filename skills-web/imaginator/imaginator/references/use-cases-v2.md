# Use Cases v2 — 8 Templates + Mode B Intent Templates

> Ready-to-use templates for each visual category + 4 Mode B intent templates

---

## Mode A Templates (8 Use Cases)

### Case 1: PRODUCT / E-COMMERCE 📦

**Keywords**: `produit`, `e-commerce`, `packshot`, `boutique`, `shop`, `vente`

| Parameter | Default Value |
|-----------|---------------|
| Style | photorealistic |
| Lighting | soft diffused studio light |
| Composition | 50-100mm macro, f/2-2.8, centered |
| Materials | based on product type + mood |
| Mood | based on detected mood |
| Ratio | 1:1 (Instagram) or 4:3 (web) |
| Quality | 4K professional quality, premium studio render |
| Negatives | shadows, reflections, fingerprints, dust, blur, text, watermark, generated AI watermark |

**Template**:
```
A [material] [product] in [finish/color] with [specific details],
photorealistic,
soft diffused studio light on [background color/surface],
[focal]mm product shot f/[aperture], centered composition on [surface],
[material finish], [surface texture], [detail level],
[mood atmosphere],
4K professional quality, premium studio render,
Negative: shadows, reflections, fingerprints, dust, blur, text, watermark, generated AI watermark
```

---

### Case 2: CINEMATIC / SCENE 🎬

**Keywords**: `scène`, `cinéma`, `film`, `dramatique`, `ambiance`, `atmosphère`

| Parameter | Default Value |
|-----------|---------------|
| Style | cinematic photoreal |
| Lighting | dramatic with contrast, neon, or golden hour |
| Composition | 35mm wide shot, dynamic angles |
| Materials | environment-specific |
| Mood | dramatic or narrative |
| Ratio | 16:9 or 21:9 |

**Template**:
```
A [subject/character] [action] in/through [environment],
cinematic photoreal,
[dramatic lighting description],
35mm wide shot, [perspective], [environmental details],
[surface materials], [environmental textures],
[narrative atmosphere],
4K cinematic detail, [color mood],
Negative: blur, washed out, low quality, sketch, text, watermark, generated AI watermark
```

---

### Case 3: PORTRAIT 👤

**Keywords**: `portrait`, `personne`, `visage`, `headshot`, `professionnel`

| Parameter | Default Value |
|-----------|---------------|
| Style | photorealistic |
| Lighting | soft diffused studio, warm tones |
| Composition | 85mm f/1.8, shallow DOF, blurred background |
| Materials | clothing/fabric textures |
| Mood | based on context |
| Ratio | 4:3 or 1:1 |

**Template**:
```
A [descriptor] [person type], age [X], [expression], [clothing/style],
photorealistic,
soft diffused studio light from [direction], [tone] tones,
85mm portrait f/1.8, shallow depth of field, blurred background,
[clothing fabric texture], [accessory materials],
[mood atmosphere],
4K high detail, sharp facial features, professional headshot,
Negative: harsh shadows, unfocused eyes, unnatural skin, blur, watermark, generated AI watermark
```

---

### Case 4: ARCHITECTURE / INTERIOR 🏢

**Keywords**: `bâtiment`, `immo`, `architecture`, `intérieur`, `extérieur`, `maison`, `chambre`, `salon`

| Parameter | Default Value |
|-----------|---------------|
| Style | photorealistic architecture/interior render |
| Lighting | golden hour or natural daylight |
| Composition | 24-35mm wide, symmetrical |
| Materials | construction + decoration materials |
| Mood | aspirational or welcoming |
| Ratio | 16:9 or 4:3 |

**Template (Exterior)**:
```
A [style] [building type] with [architectural features],
photorealistic architecture render,
[time of day] light, [sky/weather description],
[ratio] wide shot from [angle], [composition style], [environment],
[facade material], [structural material], [surface finish],
[atmosphere description],
4K architectural visualization, sharp detail, professional render,
Negative: people, cars, low quality, blur, washed colors, sketch, watermark, generated AI watermark
```

**Template (Interior)**:
```
A [style] [room type] with [key furniture and features],
photorealistic interior photography,
[light source and direction], [quality], [temperature],
[focal]mm interior shot f/[aperture], [angle], [composition],
[floor material], [wall finish], [furniture materials], [textile textures],
[mood and atmosphere],
4K professional interior quality, [color description],
Negative: dark corners, clutter, people, extreme distortion, text, watermark, generated AI watermark
```

---

### Case 5: ILLUSTRATION / ART 🎨

**Keywords**: `illustration`, `art`, `dessin`, `peinture`, `artistique`

**Template**:
```
A [subject] [action/pose] in [environment], [genre] world,
[single art style],
[dramatic/expressive lighting description],
[focal] [composition type], [scale], [background elements],
[artistic textures: brushstrokes, paper grain, ink quality],
[emotional atmosphere],
high detail professional art quality, [color description],
Negative: blur, [anachronistic elements], text, unfinished style, watermark, generated AI watermark
```

---

### Case 6: TEXT / LOGO 📝

**Keywords**: `texte`, `logo`, `affiche`, `bannière`, `titre`, `label`

**Critical**: Max 25 characters, explicit placement.

**Template**:
```
A [product/surface] with "[TEXT MAX 25 CHARS]" [typography] text [placement],
photorealistic product render,
soft studio light on [background],
[focal]mm [shot type], [composition],
[surface material], [text material: embossed/engraved/printed/neon],
[brand atmosphere],
4K high detail, [aesthetic] quality,
Negative: blurry text, distorted label, extra text, misspelling, watermark, generated AI watermark
```

---

### Case 7: IMAGE-TO-IMAGE 🔄

**Keywords**: `modifier`, `changer`, `remplacer`, `éditer`, `transformer`

**Template**:
```
Keep original [elements to preserve],
replace [element] with [new element],
change [aspect] to [new state],
add [new elements],
maintain [qualities to keep],
[style],
[preserved materials] + [new materials],
[target mood],
Negative: [unwanted changes], unnatural transitions, washed colors, watermark, generated AI watermark
```

---

### Case 8: SERIES / CONSISTENCY 🔁

**Keywords**: `série`, `variations`, `déclinaisons`, `cohérent`, `collection`

**Base Template**:
```
BASE (same for all):
A [fixed character/subject description],
[fixed style],
[fixed materials],
[VARIABLE: lighting, background, pose, clothing, mood]

VARIATION [N]: [specific changes for this variant]
```

Each variation includes: `Negative: inconsistency, style breaks, watermark, generated AI watermark`

---

---

## Mode B Templates (4 Intents)

### Intent: REPRODUCE 📋

**When**: User wants to recreate what images show.
**Strategy**: Prompt describes precisely, reinforces what Nano will see in images.

```
[Detailed subject description extracted from images],
[STYLE detected from images],
[LIGHTING: source + quality + direction as observed in images],
[COMPOSITION: framing + angle + focal as observed],
[MATERIALS: specific surfaces and finishes observed in images],
[MOOD: atmosphere and narrative tone from images],
[QUALITY: 2-3 signals matching the style],
Negative: [artifacts to avoid + elements NOT present that could appear + watermark, generated AI watermark]
```

**Example**:
```
A bright open-plan living room with white walls, light oak parquet floor,
large bay window on the left wall, linen sofa facing the window, potted plants on windowsill,
photorealistic interior photography,
soft natural daylight from left bay window, gentle shadows on floor, warm afternoon tones,
35mm wide interior shot f/5.6, eye level, symmetrical composition from doorway,
light oak wood grain on floor, white matte walls, natural linen texture on sofa, terracotta pots,
serene domestic comfort, airy lived-in warmth, Scandinavian simplicity,
4K architectural interior quality, sharp detail throughout,
Negative: harsh shadows, dark corners, clutter, people, pets, extreme wide angle distortion, text, watermark, generated AI watermark
```

**Writing rules**:
- Describe what images show in detail — the prompt reinforces
- Include observed materials and atmosphere
- Negatives focus on preventing AI artifacts

---

### Intent: INSPIRE ✨

**When**: User wants the aesthetic/mood from images applied to a different subject.
**Strategy**: Extract style/mood/palette from images, apply to user's new subject.

```
[NEW SUBJECT from user text, described in detail],
[STYLE extracted from reference images],
[LIGHTING: replicate the lighting approach from images],
[COMPOSITION: user-defined or adapted from images],
[MATERIALS: relevant to new subject, informed by image aesthetic],
[MOOD: atmosphere transferred from reference images],
[QUALITY: matching the quality level observed],
Negative: [style-breaking elements + standard artifacts + watermark, generated AI watermark]
```

**Example** (ref: Scandinavian interior → new subject: tea shop):
```
A small artisanal tea shop interior with wooden shelving displaying ceramic tea canisters,
counter with dried flower arrangement, handwritten chalkboard menu,
photorealistic interior photography,
soft natural daylight from storefront window, warm afternoon glow, gentle shadows,
35mm interior shot f/4, eye level from entrance, inviting depth,
light birch wood shelves, matte ceramic containers, raw linen tablecloth, chalk texture on board,
serene intimate warmth, Scandinavian-inspired simplicity, artisanal care,
4K professional interior quality, natural color palette,
Negative: harsh lighting, plastic surfaces, modern industrial feel, clutter, people, text, watermark, generated AI watermark
```

**Writing rules**:
- New subject described independently
- Style/mood/lighting borrowed from images
- Materials adapted to new subject but informed by image aesthetic

---

### Intent: TRANSFORM 🔄

**When**: User wants to modify what images show.
**Strategy**: Explicit keep/change structure.

```
[Subject as seen in reference images with noted changes],
[STYLE: original or new target style],
[LIGHTING: keep original OR specify new lighting],
[COMPOSITION: keep original framing OR specify changes],
[MATERIALS: keep existing OR specify replacements],
[MOOD: original mood adjusted toward target mood],
[QUALITY],
Negative: [unwanted artifacts + elements from original to remove + transition artifacts + watermark, generated AI watermark]
```

**Example** (cluttered room → minimalist):
```
The same living room layout as shown in the reference image,
but decluttered and minimalist — only the sofa, one coffee table, and two plants remain,
photorealistic interior photography,
bright clean natural light from the existing window, even soft illumination, no harsh shadows,
same 35mm wide angle from doorway, symmetrical, generous negative space,
smooth white walls, light oak floor, matte ceramic plant pots, clean linen upholstery,
serene minimalist calm, breathing space, curated simplicity,
4K clean interior visualization, crisp detail,
Negative: clutter, extra furniture, decorative objects, dark corners, busy patterns, dust, text, watermark, generated AI watermark
```

**Writing rules**:
- Explicitly state what stays ("same layout", "keep lighting")
- Explicitly state what changes
- Negatives include removed elements to prevent them reappearing

---

### Intent: MERGE 🧩

**When**: User wants to combine elements from multiple images.
**Strategy**: Assign explicit role per image, compose from each.

```
[Subject combining elements: "room layout from reference image 1"
+ "furniture piece from reference image 2" + any user additions],
[STYLE: coherent style bridging both images],
[LIGHTING: chosen from one image OR harmonized],
[COMPOSITION: typically from the spatial/context image],
[MATERIALS: merged from both images with coherence check],
[MOOD: target atmosphere combining the best of both],
[QUALITY],
Negative: [style clashes between images + incoherence artifacts + watermark, generated AI watermark]
```

**Example** (image 1: empty bedroom / image 2: wooden bed with white linen):
```
A spacious bedroom with the layout and natural lighting from reference image 1,
furnished with the wooden king-size bed frame and white linen bedding from reference image 2,
bed centered against the far wall, nightstands on each side,
photorealistic interior photography,
soft morning light from the large window on the left as seen in image 1,
warm golden tones casting gentle shadows across the bed,
35mm interior shot f/4, eye level from room entrance, balanced composition,
raw oak bed frame with visible wood grain, crisp white linen sheets,
matte white walls, light wood parquet from image 1,
peaceful morning serenity, boutique hotel comfort, airy brightness,
4K professional interior quality, natural warm tones,
Negative: mismatched wood tones, dark corners, cluttered nightstands,
harsh shadows, cold bluish tint, unmade bed, text, watermark, generated AI watermark
```

**Writing rules**:
- Reference each image by number: "from reference image 1", "from reference image 2"
- Assign clear role: which image provides what
- Resolve any material/light conflicts explicitly
- Negatives include cross-image incoherences (mismatched tones, style clashes)
- Coherence > absolute fidelity to any single source

---

## Quick Reference: Mode A vs Mode B

| Aspect | Mode A | Mode B |
|--------|--------|--------|
| Input | Text only | Text + images |
| Parameter source | Auto-suggestion rules | Image analysis overrides |
| Subject description | From user text | From images + user text |
| Materials | Auto-suggested by mood | Extracted from images |
| Rationale | Choice justifications | Traced to image sources |
| Output extras | — | Analysis summary + Nano brief |
| Negatives | Use case defaults + watermark | + intent-specific + watermark |
