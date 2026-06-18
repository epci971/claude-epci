# Style Anchors Library

Modular, combinable, versioned reference of design anchors across 5 dimensions. User selects 1-2 per dimension or designor infers from refs visuelles.

## Versioning

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-04-30 | Initial library — 5 dimensions, ~40 anchors total |
| 1.1.0 | 2026-04-30 | Perplexity validation pass — Aquacro renamed → Liquid Glass (stable, Apple WWDC 2025), Editorial magazine promoted emerging → stable, Retro-futuriste split into 3 distinct anchors (Synthwave UI, Cassette futurism, Y2K revival), Soft pastel maximalist renamed → Tactile maximalism, Néo-brutaliste enriched with 2.0/soft/functional variants |

**Freshness tags**:
- `stable` — well-established references, evergreen relevance
- `emerging` — current 2026 trends, validated by multiple sources
- `experimental` — niche or polarizing, use with intent

**Freshness check**: in `deep` mode, designor offers to run perplexitor on selected anchors to validate current relevance:

```
💡 Recherche Perplexity recommandée pour valider la fraîcheur :
"Le style [anchor name] est-il toujours pertinent pour [type de livrable]
en 2026 ? Quelles évolutions notables, quelles tendances proches ?"
```

## Dimension 1 — Style Anchors

The dominant visual language of the design.

### Stable

| Anchor | Description | Best for |
|--------|-------------|----------|
| **Linear-like** | Précision, clean sans-serif, dark mode natif, density élevée, accents froids (cyan/violet doux) | UI ops, dashboards techniques, dev tools |
| **Stripe-like** | Hierarchy claire, palette pastel, illustrations subtiles, généreux mais pas vide | UI fintech, B2B SaaS, landing pages crédibles |
| **Apple HIG** | Sobriété, espace négatif, typographie premium, focus sur le contenu | Premium B2C, apps grand public, ne pas surcharger |
| **Material 3** | Tokens systémiques, élévation, shapes, palette dynamique, accessibilité native | Apps multi-plateforme, projets ouverts à la systématisation |
| **Notion-like** | Éditorial, clarté typographique, blocs modulaires, accents discrets | Tools knowledge, decks, contenus structurés |
| **Vercel-like** | Très geek, dark mode profond, typographie technique, accents précis | Outils dev, landing tech, audiences techniques senior |
| **shadcn/ui-like** | Sobriété fonctionnelle, neutre, accents sémantiques, base personnalisable | Dashboards SaaS, apps internes, MVP rapides |
| **Liquid Glass / Aqua glassmorphism** | Surfaces translucides à reflets fluides, blur Gaussian, gradients subtils, highlights spéculaires, palette bleu-vert apaisante. Langage officiel Apple WWDC 2025, repris par Linear ("A Linear spin on Liquid Glass"). ⚠️ Le terme "Aquacro" n'existe PAS — utiliser "Liquid Glass aqua UI" ou "Aqua glassmorphism" en com client. | Apps wellness, fintech moderne, dashboards "calmes", premium B2C/B2B avec mood apaisant |
| **Editorial magazine** | Hiérarchie typographique forte (XXL titres, type-led), asymétries contrôlées, photographie premium, mise en page proche d'un magazine print, beaucoup de blanc. Vocabulaire alternatif : "type-led design", "typography-first", "magazine-style web". | Marques créatives, culturelles, luxe, portfolios, médias, SaaS design-driven (Squarespace, Webflow templates) |

### Emerging (2026)

| Anchor | Description | Best for |
|--------|-------------|----------|
| **Néo-brutaliste 2.0** | Bords nets, contrastes forts, asymétrie, typographie audacieuse, ombres dures. Variantes : 2.0 (codes maîtrisés, pas pur 2018-2021), soft/post-brutalism (palettes adoucies, plus de blanc), brutalisme fonctionnel (montre les "entrailles" : data brute, code, états d'erreur). Refs concrètes : RetroUI (template SaaS), Figma (cas cité), Back Market. ⚠️ Pas pour banque/assurance/enterprise. | B2B/SaaS dev tools, analytics, produits créatifs, Web3, fintech alt, marques jeunes |
| **Synthwave UI / 80s neon corporate** | Dark mode dominant, néons magenta/cyan réservés aux CTA et charts, horizon grids, palettes 80s revisitées. La variante "corporate" intègre néons dans une grille stricte avec beaucoup de vide. | Devtools "premium tech", AI platforms, fintech alt, branding tech-différenciant |
| **Cassette futurism (70s-80s space age)** | Boutons physiques, switches, interfaces inspirées de vieux équipements audio/computer, palettes beige/orange/brun + touches fluo, typographies "space program". Très distinct du synthwave. | Outils dev/infra (console-like), dashboards avec sliders inspirés équipements audio, UI "instrument panel" |
| **Editorial typographique expressive** | Variation de Editorial magazine pour SaaS sérieux : XXL titres servant de structure, polices variables, contrastes typographiques forts dans des layouts SaaS modernes. | Landing SaaS qui veulent se distinguer du minimalisme générique, content tools, marques B2B "design-driven" |
| **Tactile maximalism (digital pastels)** | Layering, textures de bruit (1-3% noise), hyper-skeuomorphisme doux, profondeur marquée, densité visuelle élevée mais lisible, palettes pastel saturées. ⚠️ Le nom "Soft pastel maximalist" n'est pas canonisé — vocabulaire établi : "tactile maximalism", "soft UI", "digital pastels". | Wellness, éducation créative, creator tools, lifestyle, marques "feel good". Pas pour finance/B2B enterprise |

### Experimental

| Anchor | Description | Best for |
|--------|-------------|----------|
| **Brutaliste raw** | Style "construction", typographies système, layout irrégulier, anti-design. Plus extrême que Néo-brutaliste 2.0 (qui est en emerging) | Underground, art, statements, niche design-aware |
| **Art Déco géométrique** | Symétries, dorures (chromatic), motifs, élégance. Variante "soft" : pastels + or désaturé + arches répétées | Luxe, premium niche, gastronomie, hospitality haut de gamme |
| **Y2K revival** | Reflets chrome, boutons bulle, gradients lisses, typo techno, smileys, glitter, éléments 3D cartoon. ⚠️ En B2B sérieux : limiter à callouts/hero, jamais l'UI globale. Voir aussi `Synthwave UI` (emerging) pour version plus mature. | Brands jeunes Gen Z, fashion, gaming, marketing créatif |
| **Cyberpunk neon** | Néon sur dark, cyber elements, glitch effects, palettes saturées extrêmes | Gaming, niche tech, statements ambitieux. Pas SaaS B2B. |
| **Retro-brutal / techno-brutal** | Hybridation brutalism + rétro digital : grilles visibles, blocs massifs, typo mono, textures CRT, pixellisation légère, codes early-internet | Devtools "builder-centric", AI infra, Web3, branding "outsider tech" |

## Dimension 2 — Density Anchors

How information is packed visually.

| Anchor | Description | Best for |
|--------|-------------|----------|
| **Dense ops dashboard** | Beaucoup d'infos par écran, density élevée, multiples panneaux, KPI multiples | Trading, monitoring, ops tools |
| **Balanced SaaS** | Équilibre information/respiration, sections claires, white space modéré | B2B SaaS courant, apps utilitaires |
| **Generous editorial** | Beaucoup d'espace négatif, focus sur 1-2 éléments par section | Landing premium, content sites, brand sites |
| **Compact mobile-first** | Optimisé écran petit, hiérarchie verticale forte, touch-friendly | Apps mobiles, web mobile-dominant |
| **Spacious landing** | Large hero, sections aérées, scroll généreux | Landing pages B2B/B2C marketing |
| **Magazine-style** | Layouts mixtes (grilles + breakouts), variétés d'echelles | Éditorial, content marketing |

## Dimension 3 — Brand Anchors

The brand personality the design should convey.

| Anchor | Description | Best for |
|--------|-------------|----------|
| **Premium B2B mature** | Sobre, crédible, autorité, palette froide, typographie classique | Enterprise SaaS, financial, consulting |
| **Founder-led startup** | Personnalité affirmée, parfois imparfait par choix, ton direct, hooks forts | Solo founders, indie SaaS, opinionated tools |
| **Growth-marketing punchy** | CTAs visibles, urgency cues, social proof in-your-face, contrast élevé | Conversion-focused landing, e-commerce |
| **Corporate enterprise** | Conventions du secteur, neutre, zéro risque visuel, conformité | Grandes entreprises, secteurs régulés |
| **Indie maker** | Personnel, transparent, parfois playful, story-driven | Solo products, building in public, communauté |
| **Creator / personal brand** | Photographie incarnée, typo expressive, palette personnelle | Solopreneurs, coaches, creators |
| **Educational platform** | Clair, pédagogique, hiérarchie d'apprentissage, soft colors | EdTech, formations, knowledge bases |

## Dimension 4 — Audience Anchors

The end user the design serves. Conditions density, vocabulary, complexity tolerance.

| Anchor | Description | Implications |
|--------|-------------|--------------|
| **Tech senior** | Familier des conventions techniques, supporte densité et jargon | Dense ops density, abréviations OK, peu de hand-holding |
| **Ops manager** | Pressé, orienté décision, scan plutôt que lecture | Hiérarchie très claire, KPI en haut, alertes prioritaires |
| **C-level decider** | Cherche synthèses et confiance, pas le détail | Generous density, charts simples, narrative claire |
| **End-user grand public** | Variable expertise, attente d'évidence | Compact mobile-first, gros CTAs, vocabulaire simple |
| **Investor early-stage** | Cherche traction + équipe + vision, lit beaucoup de pitchs | Density modérée, mockups produits, KPI d'élan |
| **Agence B2B** | Achetez en équipe, comparent, demandent ROI | Cas d'usage, témoignages, calculateurs ROI |
| **Developer / technical buyer** | Veut voir le code, l'API, les détails | Stack visible, code samples, intégrations claires |

## Dimension 5 — Anti-Patterns Banks

Per-deliverable specific anti-patterns to explicitly bann in the prompt.

### `ui` Anti-patterns
- Gradient violet sur blanc (signature IA generic)
- 3 cartes feature identiques alignées
- Hero centré générique avec "headline + subhead + CTA + image stock"
- Icônes dans bulles colorées (cliché SaaS)
- Fonts génériques : Inter, Roboto, Arial, system fonts
- Empilement vertical infini sans hiérarchie
- Sidebar gauche + main + sidebar droite "template by default"

### `wireframe-handoff` Anti-patterns
- Wireframes trop décorés (sortir du low-fi quand on demande low-fi)
- Composants nommés vaguement (button1, card2)
- Pas d'états error / empty / loading prévus
- Layout qui suppose hover (mobile cassé d'office)

### `deck` Anti-patterns
- 5+ bullets par slide (death by bullet)
- Hero générique "Title + Subtitle + Image"
- Slides surchargées (1 idée/slide est la règle)
- Photos stock impersonnelles (handshakes, smiling people in suits)
- Manque de slides de rupture (transitions)
- Pas de mockups produit (deck théorique)

### `one-pager` Anti-patterns
- Zoning flou (sections mal délimitées)
- CTA absent en bas
- Densité décorrélée de l'objectif (trop dense pour landing email, trop creux pour fiche commerciale)
- Illustrations cartoon (sauf si brand le justifie)
- Logo client en grille équivalente (perd la signification)

### `social` Anti-patterns
- Texte trop dense (max 10 mots / visuel)
- Ratio image/texte mal équilibré (50/50 = générique)
- CTA noyé dans la composition
- Pas de hook fort en slide 1 (carrousel)
- Cohérence de pack absente (chaque visuel "freelance")

### `explore` Anti-patterns
- Variations cosmétiques (juste palette différente)
- Directions trop similaires (pas de vraie tension)
- Pas d'éléments communs (perte de comparabilité)
- Direction "safe" + 2 "wild" (biais utilisable)

## How to Combine Anchors

### Designor's combination rules

1. **Style + Density** : check coherence. "Linear-like + Generous editorial" works (Linear allows space). "Néo-brutaliste + Compact mobile-first" needs care (brutalist often needs space).

2. **Style + Brand** : alignment expected. "Vercel-like + Founder-led" coherent. "Apple HIG + Founder-led" possible but requires intent.

3. **Audience drives density default** : if user picks audience first, density auto-suggests:
   - Tech senior → Dense ops
   - C-level → Generous editorial
   - End-user grand public → Compact mobile-first

4. **Max 2 style anchors** : combining 3+ creates incoherence. Prefer "Linear-like + Notion-like" (compatible) over 3-way mixes.

### Example combinations

| User context | Suggested combination |
|--------------|------------------------|
| SaaS PMS dashboard for ops managers | Style: Linear-like + Stripe-like / Density: Dense ops / Brand: Premium B2B mature / Audience: Ops manager |
| Pitch deck for early-stage VCs | Style: Notion-like / Density: Generous editorial / Brand: Founder-led startup / Audience: Investor early-stage |
| Landing page for indie SaaS launch | Style: Vercel-like + Néo-brutaliste 2.0 (soft variant) / Density: Spacious landing / Brand: Indie maker / Audience: Developer |
| Carousel LinkedIn pour gestionnaires immobiliers | Style: Editorial magazine / Density: Compact mobile-first / Brand: Educational platform / Audience: Agence B2B |
| Wellness app dashboard | Style: Liquid Glass / Aqua glassmorphism / Density: Generous editorial / Brand: Premium B2C / Audience: End-user grand public |
| Devtools landing AI platform | Style: Synthwave UI + Vercel-like / Density: Balanced SaaS / Brand: Founder-led / Audience: Developer |
| Creator tool for educators | Style: Tactile maximalism (digital pastels) / Density: Balanced SaaS / Brand: Educational platform / Audience: Creator |

## Anchors Inference from Refs

If user provides refs Pinterest/Dribbble, designor can infer anchors instead of asking:

```
🔍 Analyse des refs visuelles fournies :
- Style dominant : [Linear-like / Stripe-like / etc.]
- Density observée : [...]
- Brand personality : [...]

Confirmes-tu cette lecture ? Si oui, on continue. Sinon, indique les ajustements.
```

This avoids redundant elicitation when user has already done visual research.
