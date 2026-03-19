# Imaginator v2 — Rapport de synthèse

> Brainstorm : Évolution du skill imagepromptor v1.0 → Imaginator v2.0
> Date : 13 mars 2026
> Itérations : 4 | EMS final : 82/100 🌳

---

## Contexte et objectif

Le skill imagepromptor v1.0 génère des prompts optimisés pour Nano (Google) à partir de descriptions textuelles. L'objectif de cette évolution est double :

1. **Renommage** : imagepromptor → **Imaginator** (cohérence naming convention `-ator`, affordance immédiate)
2. **Ajout de l'analyse d'images** : permettre l'upload de 1 à N images comme contexte visuel pour enrichir la génération de prompts

Le principe fondamental : **les mêmes images sont envoyées à Claude (pour analyse) ET à Nano (pour génération)**. Le prompt ne remplace pas les images — il les pilote.

---

## Décisions prises

### D1 — Nom : Imaginator
- Préfixe "imag-" facilite l'auto-détection (image, imagine, imaginer)
- Suffixe "-ator" cohérent avec estimator, propositor, comparator, resumator
- "Bananatore" écarté : fun mais zéro affordance

### D2 — Structure prompt : 6 → 8 composants
Ajout de **Materials & Textures** et **Mood & Atmosphere** :
```
[SUBJECT], [STYLE], [LIGHTING], [COMPOSITION], [MATERIALS], [MOOD], [QUALITY], Negative: [NEGATIVES]
```

### D3 — Deux modes (pas trois)
- **Mode A — Texte seul** : v1 amélioré avec 8 composants et nouveaux mappings
- **Mode B — Image-Assisted** : nouveau, analyse d'images uploadées
- Mode C (Reverse Prompt) écarté : pas assez de valeur ajoutée

### D4 — 4 intentions en Mode B
| Intention | Usage |
|-----------|-------|
| Reproduire | Recréer fidèlement ce que montrent les images |
| S'inspirer | Extraire style/mood/palette, appliquer à un nouveau sujet |
| Transformer | Partir des images, spécifier ce qui change |
| Fusionner | Combiner des éléments de plusieurs images |

### D5 — 4 rôles d'image
| Rôle | Fonction |
|------|----------|
| Contexte | Lieu, décor, environnement spatial |
| Sujet | Produit, meuble, objet focal |
| Style | Référence esthétique pure |
| Détail | Texture, matériau, finition spécifique |

### D6 — 10 critères d'évaluation (+1 bonus)
8 critères v1 réajustés + Materials & Textures (10%) + Mood & Atmosphere (10%). En Mode B : critère bonus Image-Prompt Alignment.

### D7 — Moteur cible : Nano uniquement
Pas d'ouverture multi-moteur pour cette version.

---

## Architecture fonctionnelle

### Mode A — Texte seul (v1 amélioré)

```
INPUT: Description textuelle (+ brand guidelines optionnelles)
  │
  ▼
ANALYSE SILENCIEUSE
  ├── Détection cas d'usage (8 types, score confiance)
  ├── Extraction charte si fournie
  ├── Auto-fill 10 paramètres (→ étendu à 12 avec materials + mood)
  └── Nouveaux mappings : mood→materials, mood→atmosphere
  │
  ▼
OUTPUT: Brief + Prompt 8 composants + 2 variantes + Rationale + Qualité
```

Améliorations v2 du Mode A :
- Structure 8 composants au lieu de 6
- Suggestions matériaux automatiques par cas d'usage × mood
- Vocabulaire atmosphère structuré par mood × cas d'usage
- Détection de contradictions renforcée

### Mode B — Image-Assisted (nouveau)

```
INPUT: 1-N images + description textuelle
  │
  ▼
ÉTAPE 1 — ANALYSE PAR IMAGE
  ├── Pour chaque image : fiche 7 axes
  │   ├── Sujet / composition
  │   ├── Perspective / objectif photo
  │   ├── Lumière
  │   ├── Palette
  │   ├── Matériaux / textures
  │   ├── Style / medium
  │   └── Atmosphère / narration
  └── Identification du rôle probable (contexte/sujet/style/détail)
  │
  ▼
ÉTAPE 2 — SYNTHÈSE MULTI-IMAGE
  ├── Invariants (communs à toutes les images)
  ├── Variables (diffèrent entre images)
  └── Score de cohérence inter-images
  │
  ▼
ÉTAPE 3 — DÉTECTION D'INTENTION
  ├── Auto-détection : reproduire / s'inspirer / transformer / fusionner
  ├── Si ambiguïté → question ciblée avec rôles détectés
  └── Confirmation utilisateur
  │
  ▼
ÉTAPE 4 — GÉNÉRATION PROMPT 8 COMPOSANTS
  ├── Prompt calibré pour accompagner les images (pas les remplacer)
  ├── 2 variantes créatives
  ├── Rationale avec traçabilité image → composant
  └── Brief d'envoi Nano inclus
  │
  ▼
OUTPUT: Analyse visible + Prompt + Variantes + Rationale tracé + Brief Nano + Qualité
```

---

## Mappings de référence

### Materials & Textures — Par cas d'usage

| Cas | Matériaux typiques | Finitions |
|-----|-------------------|-----------|
| Product | verre, métal, plastique premium, bois, céramique | glossy, matte, frosted, brushed |
| Cinematic | béton, métal oxydé, verre mouillé, néon | weathered, wet, reflective |
| Portrait | textile (lin, laine, soie, cuir), bijoux | soft, structured, flowing |
| Architecture | béton, verre, bois, pierre, acier, végétal | poli, brut, brossé, patiné |
| Illustration | selon style artistique | coups de pinceau, texture papier |
| Text-Logo | surface support (papier, métal, verre, mur) | embossed, engraved, printed, neon |

### Materials & Textures — Croisement Mood × Matériaux

| Mood | Matériaux | Finitions |
|------|-----------|-----------|
| Professional | acier brossé, verre clair, cuir structuré | clean, polished, matte |
| Dramatic | métal oxydé, béton brut, verre brisé | weathered, rough, wet |
| Warm | bois naturel, lin, laine, terre cuite | natural grain, soft texture, handmade |
| Minimalist | béton lisse, verre dépoli, céramique blanche | smooth, matte, seamless |
| Luxurious | marbre, or, velours, cristal, soie | polished, glossy, brushed gold |
| Natural | pierre brute, bois flotté, rotin, coton | organic, raw, unfinished |
| Modern | aluminium, verre, résine, composite | sleek, reflective, high-gloss |
| Vintage | bois patiné, cuivre, cuir vieilli, papier | aged, distressed, sepia-toned |

### Mood & Atmosphere — Vocabulaire par mood

| Mood | Formulation prompt (EN) | Genre visuel |
|------|------------------------|-------------|
| Professional | clean corporate atmosphere, business confidence | editorial, corporate photography |
| Dramatic | intense cinematic tension, high-stakes atmosphere | film still, key art |
| Warm | cozy intimate warmth, inviting domestic comfort | lifestyle photography |
| Minimalist | serene quiet simplicity, contemplative space | architectural digest, zen |
| Luxurious | opulent refined elegance, exclusive premium feel | luxury magazine |
| Energetic | dynamic vibrant energy, movement and life | sports, advertising |
| Natural | authentic organic calm, earthy grounded serenity | eco brand, nature documentary |
| Modern | sleek contemporary edge, forward-thinking design | tech editorial |
| Vintage | nostalgic timeless charm, analog warmth | retro campaign |

### Mood & Atmosphere — Croisement Cas × Mood

| Cas | Professional | Warm | Luxurious | Natural |
|-----|-------------|------|-----------|---------|
| Product | premium studio showcase, editorial confidence | handcrafted artisanal warmth on natural surface | luxury magazine hero shot, exclusive feel | organic product in natural setting, raw beauty |
| Portrait | corporate headshot, authoritative presence | warm lifestyle portrait, approachable intimacy | high-fashion editorial, refined elegance | candid natural portrait, authentic expression |
| Architecture | professional visualization, precise geometry | welcoming interior, lived-in comfort | luxury real estate showcase, aspirational | biophilic design, harmony with nature |
| Cinematic | thriller tension, controlled precision | indie film intimacy, golden nostalgia | Bond-like opulence, grand scale | documentary authenticity, raw environment |

---

## Templates de prompt Mode B

### Template REPRODUIRE

```
[Detailed subject description extracted from images],
[STYLE detected from images],
[LIGHTING: source + quality + direction as observed in images],
[COMPOSITION: framing + angle + focal as observed],
[MATERIALS: specific surfaces and finishes observed],
[MOOD: atmosphere and narrative tone from images],
[QUALITY: 2-3 signals matching the style],
Negative: [artifacts to avoid + elements NOT present in images that could appear]
```

Exemple :
```
A bright open-plan living room with white walls, light oak parquet floor,
large bay window on the left wall, linen sofa facing the window, potted plants on windowsill,
photorealistic interior photography,
soft natural daylight from left bay window, gentle shadows on floor, warm afternoon tones,
35mm wide interior shot f/5.6, eye level, symmetrical composition from doorway,
light oak wood grain on floor, white matte walls, natural linen texture on sofa, terracotta pots,
serene domestic comfort, airy lived-in warmth, Scandinavian simplicity,
4K architectural interior quality, sharp detail throughout,
Negative: harsh shadows, dark corners, clutter, people, pets, extreme wide angle distortion, text
```

### Template S'INSPIRER

```
[NEW SUBJECT from user text, described in detail],
[STYLE extracted from reference images],
[LIGHTING: replicate the lighting approach from images],
[COMPOSITION: user-defined or adapted from images],
[MATERIALS: relevant to new subject, informed by image aesthetic],
[MOOD: atmosphere transferred from reference images],
[QUALITY: matching the quality level observed],
Negative: [style-breaking elements + standard artifacts]
```

Exemple (ref: intérieur scandinave → nouveau sujet: boutique de thé) :
```
A small artisanal tea shop interior with wooden shelving displaying ceramic tea canisters,
counter with dried flower arrangement, handwritten chalkboard menu,
photorealistic interior photography,
soft natural daylight from storefront window, warm afternoon glow, gentle shadows,
35mm interior shot f/4, eye level from entrance, inviting depth,
light birch wood shelves, matte ceramic containers, raw linen tablecloth, chalk texture on board,
serene intimate warmth, Scandinavian-inspired simplicity, artisanal care,
4K professional interior quality, natural color palette,
Negative: harsh lighting, plastic surfaces, modern industrial feel, clutter, people, text
```

### Template TRANSFORMER

```
[Subject as seen in reference images with noted changes],
[STYLE: original or new target style],
[LIGHTING: keep original OR specify new lighting],
[COMPOSITION: keep original framing OR specify changes],
[MATERIALS: keep existing OR specify replacements],
[MOOD: original mood adjusted toward target mood],
[QUALITY],
Negative: [unwanted artifacts + elements from original to remove + transition artifacts]
```

Exemple (salon encombré → minimaliste) :
```
The same living room layout as shown in the reference image,
but decluttered and minimalist — only the sofa, one coffee table, and two plants remain,
photorealistic interior photography,
bright clean natural light from the existing window, even soft illumination, no harsh shadows,
same 35mm wide angle from doorway, symmetrical, generous negative space,
smooth white walls, light oak floor, matte ceramic plant pots, clean linen upholstery,
serene minimalist calm, breathing space, curated simplicity,
4K clean interior visualization, crisp detail,
Negative: clutter, extra furniture, decorative objects, dark corners, busy patterns, dust, text
```

### Template FUSIONNER

```
[Subject combining elements: "room layout from reference image 1"
+ "furniture piece from reference image 2" + any user additions],
[STYLE: coherent style bridging both images],
[LIGHTING: chosen from one image OR harmonized],
[COMPOSITION: typically from the spatial/context image],
[MATERIALS: merged from both images with coherence check],
[MOOD: target atmosphere combining the best of both],
[QUALITY],
Negative: [style clashes between images + incoherence artifacts + standard]
```

Exemple (image 1: chambre vide + image 2: lit bois/linge blanc) :
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
harsh shadows, cold bluish tint, unmade bed, text
```

---

## Règles de rédaction Mode B

1. **Référencer les images explicitement** : "as seen in reference image 1", "from reference image 2"
2. **Ne pas redécrire l'évident** : le prompt pilote, il ne remplace pas les images
3. **Toujours résoudre les conflits** : si les images ont des lumières contradictoires, le prompt tranche
4. **Prioriser la cohérence** : en mode Fusionner, cohérence matériaux/lumière > fidélité absolue à chaque source
5. **Négatifs spécifiques au mode** : en Fusionner, inclure les incohérences potentielles entre sources

---

## Critères d'évaluation v2

| # | Critère | Poids | Nouveau |
|---|---------|-------|---------|
| 1 | Subject Clarity | 13% | Ajusté |
| 2 | Style Uniqueness | 13% | Ajusté |
| 3 | Lighting Precision | 10% | Ajusté |
| 4 | Composition Rigor | 10% | Ajusté |
| 5 | Materials & Textures | 10% | 🆕 |
| 6 | Mood & Atmosphere | 10% | 🆕 |
| 7 | Quality Signals | 8% | Ajusté |
| 8 | Negatives Relevance | 8% | Ajusté |
| 9 | Global Coherence | 10% | Ajusté |
| 10 | Brand Compliance | 8% | Ajusté |

**Mode B uniquement** — Critère bonus :
| 11 | Image-Prompt Alignment | Évalué | Le prompt est-il cohérent avec ce que les images montrent ? |

---

## Tableau comparatif v1 → v2

| Aspect | v1 (imagepromptor) | v2 (imaginator) |
|--------|-------------------|-----------------|
| Nom | imagepromptor | **imaginator** |
| Modes | Texte seul | **Texte seul (A) + Image-assisted (B)** |
| Structure prompt | 6 composants | **8 composants** (+Materials, +Mood) |
| Input images | ❌ | **1 à N images analysées** |
| Rôles d'image | ❌ | **4 rôles** (contexte, sujet, style, détail) |
| Intentions | ❌ | **4 intentions** (reproduire, inspirer, transformer, fusionner) |
| Critères qualité | 8 | **10 (+1 bonus Mode B)** |
| Moteur cible | Nano | **Nano** (inchangé) |
| Rationale | Choix justifiés | **+ traçabilité image → composant** |
| Brief d'envoi | ❌ | **Instructions Nano incluses** |
| Mappings materials | ❌ | **Cas × Mood → matériaux/finitions** |
| Mappings atmosphere | ❌ | **Cas × Mood → atmosphère/narration** |

---

## Prochaines étapes

1. **Implémenter via skill-factory** : générer le package complet Imaginator v2
   - SKILL.md principal
   - references/nano-structure-v2.md (8 composants)
   - references/image-analysis.md (7 axes, rôles, intentions)
   - references/materials-mappings.md
   - references/atmosphere-mappings.md
   - references/evaluation-criteria-v2.md (10 critères)
   - references/use-cases-v2.md (templates Mode B inclus)
   - references/auto-suggestion-rules-v2.md (12 paramètres)

2. **Tester sur cas réels** : utiliser les photos des gîtes Au Jardin d'Éole comme premier test du Mode B Fusionner

3. **Itérer** : ajuster les mappings et templates après les premiers retours Nano

---

## EMS Final

```
📊 EMS: 82/100 🌳

   Clarté       ██████████████████░░ 88/100
   Profondeur   ████████████████░░░░ 82/100
   Couverture   ████████████████░░░░ 80/100
   Actionnabilité ████████████████░░░░ 78/100
   Originalité  ████████████████░░░░ 75/100
```

---

*Rapport généré par Brainstormer v3.1 — Session du 13 mars 2026*
