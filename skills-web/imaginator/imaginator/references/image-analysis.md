# Image Analysis — Mode B Reference

> 7 analysis axes, 4 image roles, 4 user intents, Mode B workflow details

---

## Overview

When images are uploaded, Imaginator activates Mode B. Claude analyzes each image across 7 axes, detects the role of each image, identifies user intent, then generates a prompt calibrated to accompany the images (not replace them).

**Key principle**: The same images go to Claude (analysis) AND to Nano (generation). The prompt pilots intent on top of shared visual references.

---

## The 7 Analysis Axes

For each uploaded image, Claude silently produces an analysis covering:

| # | Axis | What to Extract |
|---|------|-----------------|
| 1 | **Subject & Composition** | Main subject, secondary elements, framing, symmetry, number of objects |
| 2 | **Perspective & Camera** | Estimated focal length, depth of field, angle, distortion |
| 3 | **Lighting** | Source type, direction, quality (soft/hard), color temperature, contrast level |
| 4 | **Color Palette** | Temperature (warm/cool), dominant colors, saturation, overall tone |
| 5 | **Materials & Textures** | Surface types, finishes (matte/glossy), texture detail level, material quality |
| 6 | **Style & Medium** | Photorealistic/illustration/3D, genre, realism level, aesthetic references |
| 7 | **Atmosphere & Narrative** | Emotional mood, scene type, implied story, visual genre |

### Internal Analysis Template (per image)

```
Image [N] — Silent Analysis
├── Subject: [description + position + state]
├── Camera: [estimated focal] [angle] [DOF] [framing]
├── Light: [source] [direction] [quality] [temperature]
├── Palette: [temperature] [dominants] [saturation] [contrast]
├── Materials: [primary surfaces] [finishes] [textures]
├── Style: [medium] [genre] [realism level]
└── Mood: [emotion] [scene type] [narrative]
```

This analysis is performed silently — user only sees a synthesis summary.

---

## The 4 Image Roles

Each image is classified into one of 4 roles:

| Role | Icon | Function | Detection Signals |
|------|------|----------|-------------------|
| **Context** | 🏠 | Space, environment, layout, setting | Room, landscape, background, architectural space |
| **Subject** | 🎯 | Focal object, product, furniture, person | Single object/item in focus, product shot |
| **Style** | 🎨 | Pure aesthetic reference, mood board | Artistic image, design reference, no specific subject |
| **Detail** | 🔍 | Specific texture, material, finish | Close-up, macro, material sample |

### Role Detection Logic

```
IF image shows a space/room/environment → Context
IF image shows a specific object/product in focus → Subject
IF image conveys a mood/style without clear focal subject → Style
IF image is a close-up of surface/material/texture → Detail
IF ambiguous → Flag for user confirmation
```

### Multi-Image Role Assignment

When multiple images are uploaded:
1. Analyze each independently
2. Detect if roles are complementary (ideal) or overlapping
3. If all images have the same role → likely Reproduce intent
4. If different roles → likely Merge intent
5. Display detected roles for user confirmation if ambiguous

---

## The 4 User Intents

| Intent | Icon | Keywords | Prompt Strategy |
|--------|------|----------|-----------------|
| **Reproduce** | 📋 | "comme ça", "pareil", "fidèle", "même style", "refais" | Describe what images show precisely, prompt reinforces |
| **Inspire** | ✨ | "ambiance", "dans le style de", "ce genre de", "inspiré de" | Extract style/mood/palette, apply to NEW subject |
| **Transform** | 🔄 | "améliorer", "changer le", "version X de", "rendre plus" | Specify keep/change explicitly |
| **Merge** | 🧩 | "combine", "mélange", "prends X de celle-ci et Y de celle-là" | Assign role per image, compose from each |

### Intent Detection Logic

```
IF user describes SAME subject as images → Reproduce
IF user describes DIFFERENT subject + references images for aesthetic → Inspire
IF user wants to MODIFY what images show → Transform
IF user references MULTIPLE images for different elements → Merge
IF ambiguous → Ask: "Je détecte [intent]. C'est correct ?"
```

### Intent × Role Matrix

| | 1 image Context | 1 image Subject | Multi-image mixed roles |
|---|---|---|---|
| **Reproduce** | Recreate this space | Recreate this product | Recreate this scene |
| **Inspire** | Use this ambiance for [X] | Use this aesthetic for [Y] | Combine these vibes for [Z] |
| **Transform** | Improve/change this space | Modify this product | Upgrade elements |
| **Merge** | N/A (need 2+) | N/A (need 2+) | Take space from img1, object from img2 |

---

## Multi-Image Synthesis

When multiple images are provided, Claude performs a cross-analysis:

### Step 1: Identify Invariants
Elements present in ALL images:
- Common lighting type
- Shared color palette
- Consistent materials
- Same style/medium

### Step 2: Identify Variables
Elements that DIFFER between images:
- Different angles of same space
- Different objects/subjects
- Different moods
- Different detail levels

### Step 3: Coherence Score

| Score | Meaning | Action |
|-------|---------|--------|
| **High** (images are consistent) | Same subject from different angles, or complementary elements | Proceed normally |
| **Medium** (some differences) | Different moods or styles, but combinable | Note differences in rationale |
| **Low** (contradictions) | Clashing styles, incompatible elements | Flag for user, ask which to prioritize |

### Conflict Resolution Rules

When images contradict each other:
1. **Lighting conflict** (warm vs cool) → Ask user OR default to the Context image's lighting
2. **Style conflict** (modern vs vintage) → Ask user, never auto-resolve
3. **Material conflict** (matching wood tones) → Explicitly note in negatives ("mismatched wood tones")
4. **Mood conflict** → Ask user which mood to target

---

## Mode B Output Format

### Analysis Summary (visible to user)

```markdown
## 🔍 Analyse des images

**[N] images analysées** · Cohérence : [Haute/Moyenne/Basse]

| Image | Rôle | Éléments clés |
|-------|------|---------------|
| Image 1 | 🏠 Contexte | [2-3 key observations] |
| Image 2 | 🎯 Sujet | [2-3 key observations] |

**Invariants** : [common elements]
**Variables** : [differences]

**Intention détectée** : [Intent] ([confidence]%)
*[Modifier ?]*
```

### Traced Rationale (Mode B specific)

```markdown
## 💡 Rationale (tracé)
- **[Component]** → Extrait de l'image [N] ([specific detail])
- **[Component]** → Intention utilisateur ([quote from text])
- **[Component]** → Cohérence entre images [N] et [M]
- **[Component]** → Ajout recommandé (pas dans les images)
```

### Nano Sending Brief

```markdown
## 📎 Brief d'envoi Nano

> **Images à joindre** : [list which images to send]
> **Rôle des images** : [context/subject/style/detail description]
> **Le prompt pilote** : [what the prompt adds/reinforces/changes vs the images]
>
> 💡 Coller le prompt ci-dessus dans Nano avec les images jointes.
> Le watermark Nano sera atténué par les négatifs du prompt.
```

---

## Mode B Prompt Writing Rules

1. **Reference images explicitly**: "as seen in reference image 1", "from reference image 2"
2. **Don't over-describe the obvious**: if images clearly show oak parquet, "light oak parquet from the reference" suffices
3. **Always resolve conflicts**: if images have contradictory lighting, the prompt MUST choose
4. **Prioritize coherence**: in Merge mode, material/lighting coherence > absolute fidelity to each source
5. **Merge-specific negatives**: include potential cross-image incoherences ("mismatched wood tones", "style clashes")
6. **ALWAYS include anti-watermark negatives**: "watermark, generated AI watermark"

---

## Edge Cases

### Single Image, No Clear Intent
- Default to Reproduce if user says "image like this"
- Default to Transform if user implies improvement
- Ask if truly ambiguous

### Many Images (5+)
- Analyze top 4 most distinct images
- Group similar images (e.g., "3 images of same room from different angles" = 1 Context role)
- Warn user if too many roles make prompt unfocused

### Image Quality Issues
- Blurry or dark images: note in analysis, suggest the prompt compensates ("sharp detail", "bright natural light")
- Very small images: warn that Nano may not extract much from them as references

### No Text Input (Images Only)
- If user uploads images without text description:
  - Analyze images
  - Ask: "Que souhaitez-vous faire avec ces images ?" + suggest most likely intent
  - Never generate without understanding intent
