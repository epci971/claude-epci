# Templates by Deliverable

Full templates × 6 deliverable types + quick mode brief format. All templates exist in FR and EN — designor matches user's input language.

## Quick Mode — 4-Block Brief (all templates)

For `quick` mode, output is a compact 4-block brief, not full XML:

```
[Type d'artefact] pour [audience].
[Spécificités contenu : structure, sections, longueur].
[Style visuel : style anchors + density + brand].
[Contraintes / output : format, technique, accessibilité, exports].
```

**Example (deck quick)**:
```
Pitch deck investisseur de 12 slides pour fonds early-stage européens.
Arc problème → solution → traction → ask, 1 idée/slide max, mockups produit aux slides 4-5.
Style Linear-like minimaliste, palette bleu lagon + sable, typo Space Grotesk + Inter.
Export PPTX, ratio 16:9, contenu en français, pas de lorem ipsum.
```

## Standard / Deep Mode — XML Templates (6 deliverables)

### Template `ui` — Interactive UI Prototype

```xml
<role>
Tu es senior product designer + frontend engineer expert de Claude Design.
Tu conçois une interface distinctive, crédible en production, jamais générique.
</role>

<artifact_target>
Type : Prototype UI interactif
Fidélité : Haute fidélité
</artifact_target>

<product_intent>
Produit : [nom]
But principal : [action utilisateur la plus critique]
Succès : [ce que l'utilisateur doit faire en X secondes]
</product_intent>

<persona>
Cible : [profil détaillé]
Contexte d'usage : [device, état d'esprit, expertise technique]
Motivations / frictions : [...]
</persona>

<visual_direction>
Style anchors : [Linear-like / Stripe-like / Apple HIG / Material 3 / etc.]
Density : [dense ops / balanced SaaS / generous editorial]
Brand : [premium B2B / founder-led / corporate / indie maker]
Inspiration : [refs Pinterest/Dribbble — JOINDRE LES IMAGES DANS CLAUDE DESIGN]
À éviter absolument :
- Gradient violet sur blanc
- 3 cartes feature identiques
- Hero centré générique
- Icônes dans bulles colorées
- Fonts génériques (Inter, Roboto, Arial)
</visual_direction>

<information_hierarchy>
1. [élément le plus important visuellement]
2. [élément secondaire]
3. [détails / actions]
</information_hierarchy>

<screens>
1. [Nom écran 1] - [sections principales] - [interactions]
2. [Nom écran 2] - [...]
[...]
</screens>

<design_tokens>
[Si codebase/Figma : "Extrait via Claude Design"]
[Si charte : palette + logo placement]
[Si rien : palette OKLCH explicite, type scale 1.25 modulaire, spacing 4px, radius]
</design_tokens>

<responsive_rules>
Mobile first à partir de 375px.
Touch targets ≥ 44x44px.
Container queries pour cartes réutilisables (pas que media queries).
Pas de dépendance au hover sur mobile.
</responsive_rules>

<accessibility>
WCAG 2.2 AA : contraste 4.5:1 corps, focus visibles, labels, alt text, navigation clavier complète, support 200% zoom.
</accessibility>

<output_requirements>
Génère directement le prototype interactif.
Tous les éléments cliquables doivent faire quelque chose de cohérent.
Pas d'explication avant le rendu.
Pas de lorem ipsum, contenu réel et synthétique.
</output_requirements>
```

### Template `wireframe-handoff` — Wireframes for Claude Code

```xml
<role>
Tu es lead product designer dans une équipe full-stack [stack].
Tu produis des wireframes haute fidélité PARFAITEMENT structurés pour handoff Claude Code.
</role>

<artifact_target>
Type : Set de wireframes hi-fi
Fidélité : Haute fidélité, prêts pour handoff
</artifact_target>

<product_context>
Produit : [...]
Stack cible : [Symfony + React + Tailwind / Django + React / etc.]
Audience utilisateur : [...]
Breakpoints : [Desktop d'abord / Mobile first]
</product_context>

<screens_to_design>
1. [Nom] — Header [...], zone principale [...], sections [...]
2. [Nom] — [...]
3. [Nom] — [...]
</screens_to_design>

<component_architecture>
Organise les composants pour mapping direct vers code :
- Atoms : button, input, badge, icon
- Molecules : form-row, card-header, search-field
- Organisms : navbar, sidebar, data-table, filter-panel
- Templates : page layouts
Nomme chaque section avec un id unique pour les développeurs.
</component_architecture>

<visual_direction>
Style : moderne, sobre, proche [Stripe / Linear / shadcn]
Style anchors : [...]
À éviter : SaaS générique, gradients flashy, sur-décoration
</visual_direction>

<design_tokens>
[Comme template ui — adapté au design system existant si présent]
</design_tokens>

<interactivity>
- États visibles : hover, focus, active, disabled, loading, error, empty
- Transitions entre écrans modélisées comme vrais écrans cliquables
- Pas d'animations complexes (déléguer à Claude Code en aval)
</interactivity>

<accessibility>
WCAG 2.2 AA, focus rings visibles, ordre tabulaire logique, labels explicites.
</accessibility>

<handoff_preparation>
Le rendu doit faciliter le handoff Claude Code :
- Composants isolables et nommés
- Tokens en CSS variables (pas en valeurs en dur)
- Structure DOM logique mappable vers JSX
- Annotations possibles pour interactions complexes à coder
</handoff_preparation>

<output_requirements>
Rendu hi-fi complet, tous les écrans connectés.
Pas de lorem ipsum, contenu plausible métier.
</output_requirements>
```

### Template `deck` — Pitch / Sales Deck

```xml
<role>
Tu es brand & presentation designer senior.
Tu crées un pitch deck on-brand, prêt à être exporté en PPTX et utilisé en réunion réelle.
</role>

<artifact_target>
Type : Pitch deck
Format : 16:9, [N] slides
Export : PPTX et/ou Canva
</artifact_target>

<context>
Startup / produit : [...]
Audience : [investisseurs early-stage / sales B2B / interne / clients]
Objectif business : [convaincre de quoi exactement]
Durée prévue : [pitch 5min / réunion 30min / lecture asynchrone]
</context>

<narrative_arc>
1. Title slide — logo, baseline, visuel produit
2. Problème — [tension précise]
3. Solution — [...]
4. Marché — [TAM/SAM simplifié]
5. Produit — [écrans clés, mockups si pertinent]
6. Traction — [KPI, MRR, croissance]
7. Roadmap — [12-18 mois]
8. Team — [...]
9. Ask — [montant, use of funds]
[Adapter selon objectif]
</narrative_arc>

<density_rules>
1 idée principale par slide.
Max 3 bullets par slide.
Texte synthétique, pas de paragraphes longs.
Slides de rupture entre sections (transitions visuelles).
</density_rules>

<visual_direction>
Style anchors : [Linear-like sobre / Notion-like clair / Pitch.com-like / Editorial]
Brand : [premium / founder-led / corporate]
Palette : [...]
Typo : [titre / corps]
Photos / mockups : [vrais visuels produit / illustrations / pas de stock photos]
À éviter : 5+ bullets, hero générique, slides surchargées, photos stock impersonnelles
</visual_direction>

<content_specifications>
[Pour chaque slide : titre, sous-titre, layout suggéré, type de visuel, contenu textuel]
</content_specifications>

<output_requirements>
Deck complet, slides séquencées, layouts cohérents d'une slide à l'autre.
Respect strict de la palette et de la typo.
Pas de lorem ipsum, contenu réel synthétique.
Prêt à exporter en PPTX.
</output_requirements>
```

### Template `one-pager` — Marketing One-Pager

```xml
<role>
Tu es directeur artistique dans une équipe growth B2B.
Tu crées un one-pager marketing prêt à être exporté en PDF et envoyé.
</role>

<artifact_target>
Type : One-pager marketing
Format : A4 portrait/landscape — [préciser]
Export : PDF à envoyer par email / impression
</artifact_target>

<context>
Produit / offre : [...]
Cible : [...]
Objectif de conversion : [démo / inscription / téléchargement / call]
Canal de diffusion : [email outbound / téléchargement site / event print]
</context>

<sections_structure>
- Hero (haut) : logo, baseline, visuel produit, CTA principal
- Bloc gauche : Problème → Solution
- Bloc droite : 3 bénéfices clés avec icônes
- Bandeau central : capture dashboard ou 3 chiffres clés
- Bas de page : logos clients, mentions, coordonnées, CTA secondaire
</sections_structure>

<copy_voice>
Ton : [pédagogue direct / corporate / startup / décalé]
Phrases courtes (6-12 mots).
Titres lisibles rapidement.
Bénéfices orientés résultat (gain temps, réduction risque, hausse revenu).
</copy_voice>

<visual_direction>
Style anchors : [...]
Palette : [...]
Densité texte/visuel : [60/40 ou 40/60 selon richesse contenu]
À éviter : zoning flou, CTA absent en bas, illustrations cartoon, surcharge
</visual_direction>

<content_specifications>
[Texte concret pour chaque section, pas de placeholder]
</content_specifications>

<output_requirements>
One-pager complet, lisible imprimé et à l'écran.
Pas de lorem ipsum, contenu réel.
Variantes de CTA prévues si pertinent (Book demo / Talk to sales).
</output_requirements>
```

### Template `social` — Social Media Assets

```xml
<role>
Tu es social media designer pour [contexte marque].
Tu crées un pack cohérent de visuels social adaptés à la plateforme cible.
</role>

<artifact_target>
Type : Pack social media
Plateforme : [LinkedIn / Instagram / X / TikTok]
Format : [1200x627 single image / carousel 5-10 slides / story 9:16 / etc.]
Quantité : [N] visuels cohérents
</artifact_target>

<context>
Marque / projet : [...]
Cible audience : [...]
Angle / sujet : [...]
Objectif : [engagement / clic site / notoriété / UGC]
</context>

<content_structure>
Slide 1 / Visuel 1 : Hook fort (1 phrase courte), fond visuel impactant
Slides 2-N : développement (2 bullets max chacune), layout 2 colonnes (visuel/texte)
Slide finale : récap + CTA + logo
</content_structure>

<copy_voice>
Ton : [corp / founder / fun / sérieux]
Hooks textuels : [...]
Max 10 mots sur chaque visuel.
Texte légende séparé (ne pas mettre tout dans l'image).
</copy_voice>

<visual_direction>
Style anchors : [...]
Palette : [...]
Logo : [placement, taille]
Cohérence pack : numérotation visible, template réutilisable
À éviter : texte trop dense, ratio image/texte mal équilibré, CTA noyé
</visual_direction>

<output_requirements>
Pack complet, cohérence visuelle d'un asset à l'autre.
Versions "template" pour réutilisation avec autres textes si demandé.
Pas de chiffres sensibles, données plausibles génériques.
</output_requirements>
```

### Template `explore` — Multi-Direction Explorations

```xml
<role>
Tu es design lead.
Tu proposes [N] directions de design RADICALEMENT différentes pour le même brief.
Pas de variations cosmétiques (juste couleur changée), de vraies directions opposées.
</role>

<artifact_target>
Type : Explorations design multi-directions
Nombre de directions : [3 par défaut, ajustable]
</artifact_target>

<common_brief>
Produit / écran : [...]
Cible : [...]
Objectif : [...]
Éléments communs (tous les directions doivent les avoir) :
- [élément 1, ex: CTA principal "Réserver une démo"]
- [élément 2]
</common_brief>

<directions>
Direction A — [Nom évocateur, ex: "Minimaliste éditoriale"] :
- Style : [...]
- Layout : [...]
- Densité : [...]
- Tone : [...]

Direction B — [Nom, ex: "Lively brutaliste"] :
- Style : [...]
- Layout : [...]
- Densité : [...]
- Tone : [...]

Direction C — [Nom, ex: "App-first dashboard dark"] :
- Style : [...]
- Layout : [...]
- Densité : [...]
- Tone : [...]
</directions>

<variation_axes>
Axes orthogonaux entre les directions :
- Style visuel (sobre vs maximaliste vs brutaliste)
- Densité (aéré vs dense)
- Layout (symétrique vs asymétrique vs grille libre)
- Mood (corporate vs founder vs editorial)
</variation_axes>

<output_requirements>
Chaque direction conçue comme prototype distinct cliquable.
Texte en [langue], contenu réel.
Toutes les directions respectent les éléments communs.
Variations RÉELLES, pas juste palette différente.
</output_requirements>
```

## Elicitation Questions by Template

For each template, here are the standard mode questions (8-12). Quick mode picks 3-5 essentials. Deep mode adds 5-8 more.

### `ui` — UI Prototype

**Quick (3-5)**:
1. Quel produit / quel écran principal ?
2. Style anchors (1-2 parmi Linear, Stripe, Apple HIG, Material 3, Notion, autre) ?
3. Density (dense ops / balanced SaaS / generous editorial) ?

**Standard (8-12)** adds:
4. Persona utilisateur principal (profil + contexte d'usage) ?
5. Action critique en X secondes ?
6. Hiérarchie d'info (3 priorités max) ?
7. Brand voice (premium B2B / founder-led / corporate) ?
8. Écrans à concevoir (liste) ?

**Deep (15-20)** adds:
9. Frictions / motivations utilisateur ?
10. Anti-patterns IA spécifiques à exclure (4-5 nommés) ?
11. États à modéliser (hover, focus, error, loading, empty) ?
12. Anticipation Tweaks (axes d'itération à exposer) ?
13. Variantes alternatives à demander en parallèle ?

### `wireframe-handoff` — Wireframes Dev

**Quick (3-5)**:
1. Stack cible (Symfony+React / Django / etc.) ?
2. Écrans à concevoir (liste) ?
3. Niveau de fidélité (low-fi / hi-fi) ?

**Standard (8-12)** adds:
4. User stories par écran ?
5. Flows entre écrans ?
6. Composants réutilisables identifiés ?
7. États à couvrir (error, empty, loading) ?
8. Design system existant pointable ?

**Deep (15-20)** adds:
9. Annotations composants pour devs ?
10. Patterns responsives spécifiques ?
11. Contraintes performance / accessibilité particulières ?
12. Mode handoff direct Claude Code prévu ?

### `deck` — Pitch / Sales Deck

**Quick (3-5)**:
1. Type de deck (investisseur / sales / interne) + audience ?
2. Nombre de slides ?
3. Style anchors (Linear sobre / Notion / Pitch.com / Editorial) ?

**Standard (8-12)** adds:
4. Objectif business concret ?
5. Arc narratif (problème → solution → preuve → ask) ?
6. Slides produit avec mockups ?
7. Densité (1 idée/slide ou 2-3) ?
8. Brand (palette, typo, logos) ?

**Deep (15-20)** adds:
9. Tension principale à mettre en scène ?
10. Slides de rupture / transitions ?
11. KPI à présenter (chiffres précis ou plausibles) ?
12. Anti-patterns deck à éviter (5+ bullets, photos stock, etc.) ?
13. Export PPTX direct ou Canva pour ajustements ?

### `one-pager` — Marketing One-Pager

**Quick (3-5)**:
1. Produit / offre + audience cible ?
2. Objectif de conversion (démo / call / téléchargement) ?
3. Format (A4 portrait / landscape) ?

**Standard (8-12)** adds:
4. Sections (hero / bénéfices / preuve / CTA) ?
5. Voix (pédagogue / corporate / startup) ?
6. Densité texte/visuel ?
7. Canal de diffusion (email / web / print) ?
8. Brand (palette, typo) ?

**Deep (15-20)** adds:
9. Bénéfices orientés résultat (3 max) ?
10. Objections principales à lever ?
11. Preuve sociale (logos clients, citations, chiffres) ?
12. Variantes de CTA (Book demo / Talk to sales) ?

### `social` — Social Assets

**Quick (3-5)**:
1. Plateforme + format exact ?
2. Sujet / angle ?
3. Quantité de visuels ?

**Standard (8-12)** adds:
4. Audience cible ?
5. Objectif (engagement / clic / notoriété) ?
6. Hook (slide 1) ?
7. Structure carousel si pertinent ?
8. Brand (palette, logo, typo) ?

**Deep (15-20)** adds:
9. Ton (corp / founder / fun) ?
10. CTA final ?
11. Templates réutilisables prévus ?
12. Cohérence campagne (lien avec autres assets) ?

### `explore` — Multi-Direction

**Quick (3-5)**:
1. Brief produit commun ?
2. Nombre de directions (3 par défaut) ?
3. Axes de variation principaux (style / densité / layout) ?

**Standard (8-12)** adds:
4. Audience cible ?
5. Éléments communs obligatoires (CTA, sections) ?
6. Style anchors par direction (3 anchors radicalement différents) ?
7. Tone par direction (sobre / maximaliste / brutaliste) ?
8. Pattern "liste les styles d'abord" demandé ?

**Deep (15-20)** adds:
9. Critères de choix entre directions ?
10. Direction prévue pour A/B test utilisateur ?
11. Direction la plus risquée à explorer ?
12. Anti-cosmétique : forcer vraies différences pas juste palette ?
