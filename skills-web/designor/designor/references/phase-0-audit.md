# Phase 0 — Pre-Elicitation Audit

This reference details the 3-question gate before any detailed elicitation. **Q2 is a hard block.**

## Q1 — Deliverable Type Detection

### Auto-detection keywords

| Template | French keywords | English keywords |
|----------|-----------------|------------------|
| `ui` | prototype, app, interface, dashboard, écran, application | prototype, app, interface, dashboard, screen, application |
| `wireframe-handoff` | wireframe, handoff, maquette dev, structure pour code | wireframe, handoff, dev mockup, structure for code |
| `deck` | deck, présentation, pitch, slides, investisseur, sales deck | deck, presentation, pitch, slides, investor, sales deck |
| `one-pager` | one-pager, fiche produit, landing courte, sales sheet, plaquette | one-pager, product sheet, short landing, sales sheet, brochure |
| `social` | post, carousel, linkedin, instagram, social media, asset social | post, carousel, linkedin, instagram, social media, social asset |
| `explore` | variantes, explorations, directions, plusieurs styles, A/B | variants, explorations, directions, multiple styles, A/B |

### Disambiguation logic

If 2+ templates match (e.g., "designor pour mon site" → `ui` OR `one-pager`):
- ONE disambiguation question (see SKILL.md Tool Notes for environment-specific implementation)
- Options: the 2-3 matching templates with short descriptions
- Default to `ui` if user skips

If 0 templates match (vague request like "designor un truc design"):
- ONE disambiguation question with the 6 templates
- No default — wait for explicit choice

### Mode detection

| Mode | French keywords | English keywords | Default behavior |
|------|-----------------|------------------|------------------|
| `quick` | rapide, vite, quick, simple | quick, fast, simple | Use if explicit |
| `deep` | approfondi, complet, deep, stratégique | deep, thorough, strategic | Use if explicit |
| `standard` | (default) | (default) | If neither quick nor deep detected |

Flags `--quick` and `--deep` always override detection.

## Q2 — Visual Inspiration (BLOCKING)

### Why this blocks

Research consistently shows: without 3+ visual references, Claude Design output is generic regardless of prompt quality. This is the #1 cause of disappointing results.

### Question framing (in user's language)

```
🎯 Avant d'aller plus loin, question critique :

As-tu collecté 3+ références visuelles qui correspondent à la direction
que tu veux pour ce livrable ? (screenshots Pinterest, Dribbble, captures
de sites que tu aimes, etc.)

Sans inspiration visuelle, Claude Design produira un rendu générique.
C'est l'erreur la plus courante.
```

### If user has refs → proceed to Q3

### If user has no refs → PAUSE

Suggest sources adapted to deliverable type:

| Template | Sources to suggest | Search themes |
|----------|---------------------|---------------|
| `ui` | Dribbble, Mobbin, Pinterest "[product type] dashboard 2026" | "SaaS dashboard minimalist", "fintech app dark mode" |
| `wireframe-handoff` | Mobbin (real apps), Pinterest "wireframe [domain]" | "wireframe SaaS", "low-fi mockup B2B" |
| `deck` | Pinterest, Dribbble "investor deck", Pitch.com gallery | "investor deck SaaS minimalist", "pitch deck B2B" |
| `one-pager` | Pinterest "product one-pager", Dribbble "sales sheet" | "B2B one-pager", "product brochure modern" |
| `social` | Pinterest "[platform] carousel", Brand archives | "linkedin carousel B2B", "instagram brand grid" |
| `explore` | Multiple sources to ensure variety | Different styles to feed contrast (brutalist, editorial, retro...) |

After listing sources, end with:

```
Quand tu as 3+ refs, dis-moi "j'ai mes refs" et on continue.
Tu peux aussi forcer le passage avec --no-inspiration (warning : risque générique).
```

### `--no-inspiration` flag behavior

If user forces with flag, designor proceeds but injects in section 3 (token economy tips):

```
⚠️ Sans refs visuelles fournies, le résultat risque d'être générique.
Recommandation : ajoute 3+ images en attachement dans Claude Design
avant de soumettre le prompt, même tardivement.
```

## Q3 — Design System Status

### 4 cases conditioning subsequent elicitation

#### Case A — Pointable codebase (GitHub URL)

User has a real codebase Claude Design can extract from.

- **Skip**: token questions (palette, typo, radius, spacing)
- **Add to prompt**: `<design_system>Extrait depuis [URL repo]. Respecte composants existants.</design_system>`
- **Recommendation**: design system ENABLED in Claude Design (the cost is justified by extraction)

#### Case B — Figma files

User has Figma design files to import.

- **Skip**: token questions
- **Add to prompt**: `<design_system>Importé depuis Figma [lien]. Respecte tokens et composants.</design_system>`
- **Recommendation**: design system ENABLED, import Figma files in onboarding

#### Case C — Brand charter (palette + logo, no DS)

User has visual identity but no formal design system.

- **Light token questions**: palette confirmation, logo placement, typography preferences
- **Add to prompt**: full `<design_tokens>` block with brand values
- **Recommendation**: design system DISABLED for first project (charter loaded manually in prompt)

#### Case D — Nothing (greenfield)

User starts from zero on visual identity.

- **Full token questions**: palette suggestion (OKLCH-based), type scale (1.25 modular from 16px), spacing (4px system), radius
- **Add to prompt**: complete `<design_tokens>` block with explicit values
- **Recommendation**: design system DISABLED, mention `getdesign.m` for branded design systems if needed

## Audit Output Format

After Q1+Q2+Q3, designor confirms:

```
✅ Phase 0 complète

Type de livrable    : [template]
Mode               : [quick/standard/deep]
Inspiration        : [user has X refs / will collect / forced --no-inspiration]
Design system      : [Case A/B/C/D — description]

→ Passage à l'élicitation [template]-spécifique.
```

## Edge Cases

### User invokes `designor revise` directly
Skip Phase 0 entirely. The revise sub-command has its own flow (see [revise-pattern.md](revise-pattern.md)).

### User provides partial refs (1-2 instead of 3+)
Soft warning, accept but flag in section 3:
```
⚠️ Tu as fourni [N] refs, l'idéal est 3+. Le résultat peut être moins distinct.
Si possible, ajoute 1-2 refs avant de soumettre dans Claude Design.
```

### User claims to have refs but doesn't show/describe them
Take user's word. Designor doesn't audit their existence—but in the prompt's `<visual_direction>` section, instruct user to attach the refs in Claude Design alongside the prompt.

### Multiple deliverables in one request
Example: "designor un deck + 5 posts LinkedIn pour le lancement"
Designor produces ONE prompt at a time. Suggests:
```
Je détecte 2 livrables (deck + social). Je propose de traiter l'un après l'autre.
On commence par lequel ?
```

## Pivot Mid-Elicitation

If the user changes their mind during elicitation (e.g., "actually I want a deck not a dashboard"), follow this procedure to avoid restarting from scratch.

### Procedure

1. **Acknowledge the pivot** without resetting the session
2. **Preserve what's still valid**:
   - Visual references (Q2) — usually still relevant if project context unchanged
   - Design system status (Q3) — almost always preserved (codebase/Figma/charter same)
   - Brand anchors (if already selected) — preserved if same brand
   - Audience anchors (if applicable to new template)
3. **Re-detect** the new template + mode from the pivot message
4. **Restart elicitation** at the template-specific question phase (skip Phase 0 if all 3 questions still apply)
5. **Confirm** the preserved elements with the user before proceeding

### Decision logic — what's preserved

| Element | Preserved on pivot? | Notes |
|---------|---------------------|-------|
| Visual refs (Q2) | ✅ Almost always | Same project = same visual world |
| Design system (Q3) | ✅ Always | Brand identity is stable |
| Brand anchors | ✅ If same brand | Founder-led, premium B2B, etc. |
| Audience anchors | ⚠️ Depends | Investor for deck ≠ ops manager for dashboard |
| Style anchors | ⚠️ Depends | Linear-like UI ≠ Editorial deck |
| Density anchors | ❌ Re-ask | Density expectations vary by deliverable |
| Information hierarchy | ❌ Re-ask | Specific to deliverable structure |
| Screen-specific details | ❌ Discard | Will be replaced by new template fields |

### Example dialog

User (mid-elicitation, after Phase 0 + 4 questions on `ui` template):
> "Attends, je préfère un deck plutôt qu'un dashboard."

Designor response:
```
🔄 Pivot détecté : `ui` → `deck`

Je conserve :
✓ Tes 4 refs visuelles fournies (Pinterest + Dribbble)
✓ Ton design system (charte interne, palette + logo)
✓ Brand anchor : "Premium B2B mature"
✓ Audience anchor : "Ops manager" — à reconfirmer (un deck pour ops manager
  ou pour ton équipe direction ?)

À redéfinir pour le template `deck` :
- Audience finale (investisseurs / sales / interne)
- Arc narratif et nombre de slides
- Densité par slide
- Style anchors adaptés au format slide

On reprend ? Question 1 : audience cible du deck ?
```

### When to refuse the pivot

If the pivot is a **major scope change** (deck for product A → social campaign for product B), it's not a pivot, it's a new session. Designor responds:

```
Ce que tu décris ressemble plus à un nouveau projet qu'à un pivot. Je propose :
1. On finalise le brief actuel (peut-être utile plus tard)
2. On lance une nouvelle session designor pour le deuxième projet

Tu veux finir l'actuel d'abord ou lancer le nouveau directement ?
```

This avoids context confusion that would degrade both outputs.

## Token Cost of Phase 0

Phase 0 is lightweight: 3 questions, ~50-100 tokens of designor output before elicitation begins. Q2 pause (waiting for refs) costs zero designor tokens—it's just a wait state.
