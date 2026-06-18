# Revise Pattern — Directed Critique for Iteration

When the user receives a disappointing Claude Design output, `designor revise` produces a structured revision prompt instead of a vague "try again" or "make it better".

## Why This Pattern Works

Anthropic documentation and community feedback converge: vague revision requests like "make it more modern", "make it pop", or "improve the UX" produce inconsistent results. Claude needs **observable criteria** to revise productively.

The directed critique pattern provides exactly that.

## The 4-Part Structure

Every revision prompt follows this structure:

### 1. Explicitly preserve (what stays)
Tell Claude what works and must NOT change. This anchors the revision.

```
Conserve la structure générale et les données affichées.
Conserve la hiérarchie des sections.
Conserve la palette et la typo.
```

### 2. Name 2-4 precise defects
Be specific. Not "it's bad" but "the visual hierarchy is too flat".

```
Le rendu actuel a 3 problèmes :
1. La hiérarchie visuelle est trop plate, tout a le même poids.
2. Le layout paraît générique "template SaaS".
3. La version mobile est une simple réduction du desktop, pas pensée native.
```

**Why 2-4**: less than 2 = vague; more than 4 = Claude struggles to prioritize.

### 3. Set sharper target (visual or functional)
What should the revised version achieve? Be measurable.

```
Révise avec ces objectifs :
- Rendre la zone d'alertes immédiatement dominante (taille, contraste, position).
- Introduire une composition asymétrique (sortir du grid 3 colonnes uniformes).
- Différencier nettement primaire / secondaire / tertiaire (size + weight + color).
- Mobile pensé natif (stack vertical, alertes en haut, KPI compactés).
```

### 4. Request complete new version (not patch)
Ask for full output, not partial fixes.

```
Livre directement la version révisée complète.
Ne m'explique pas les changements.
```

## Full Template

```xml
<revision_request>
<preserve>
Conserve [structure / contenu / palette / hiérarchie globale].
[Liste précise de ce qui fonctionne].
</preserve>

<defects>
Le rendu actuel a [N=2-4] problèmes :
1. [défaut précis observable]
2. [défaut précis observable]
3. [défaut précis observable]
</defects>

<target>
Révise avec ces objectifs :
- [objectif mesurable 1]
- [objectif mesurable 2]
- [objectif mesurable 3]
</target>

<output>
Livre directement la version révisée complète.
Ne m'explique pas les changements.
</output>
</revision_request>
```

## Workflow of `designor revise`

### Step 1 — Collect inputs

Designor asks for:
1. The original prompt (paste)
2. Free-form critique of the result (text + optional screenshot descriptions)

### Step 2 — Analyze critique

Designor extracts:
- What the user implicitly wants to keep (often unsaid)
- The 2-4 most pressing defects (prioritize, don't list all)
- The implicit target (what would make it good?)

### Step 3 — Translate vague into specific

Common translations:

| User says | Designor translates to |
|-----------|------------------------|
| "C'est pas ouf" | Need 2-4 specific defects → ask which ones (prioritize visual / structural / content) |
| "Plus moderne" | Layout asymmetry / less generic patterns / specific style anchor |
| "Plus premium" | More space / refined typography / restrained color / quality details |
| "Plus dynamique" | Visual tension / asymmetric composition / hierarchy contrast |
| "Mobile pas terrible" | Mobile native (not just responsive) / touch-first / specific issues |
| "Trop générique" | Identify 3-4 generic patterns to break (gradient, equal cards, hero centered) |
| "Pas assez de personnalité" | Specific brand voice / typographic personality / one signature element |

### Step 4 — Generate revision prompt

Output the structured XML revision following the 4-part template, in the user's language.

### Step 5 — Suggest next iterations

After producing the revision prompt, suggest:
- Test the revision in Claude Design with Tweaks aggressive (free iterations)
- If still not satisfying, second revise with new defects
- After 2-3 revises with no convergence, suggest pivot (different style anchors entirely)

## Examples

### Example 1 — Dashboard SaaS too generic

**User critique** :
```
Le dashboard est ok mais ça fait template. Toutes les cartes se ressemblent,
y'a rien qui ressort, on dirait un wireframe Bootstrap.
```

**Designor revise output** :

```xml
<revision_request>
<preserve>
Conserve la structure des sections (header, KPI, calendrier, tableau).
Conserve les données affichées et leurs labels.
Conserve la palette et la typo.
</preserve>

<defects>
Le rendu actuel a 3 problèmes majeurs :
1. Les 4 cartes KPI ont exactement le même poids visuel — aucune ne ressort.
2. Le layout suit un grid 3 colonnes uniforme (pattern Bootstrap reconnaissable).
3. Aucun élément ne crée de tension visuelle ou de point focal.
</defects>

<target>
Révise avec ces objectifs :
- Différencier les 4 KPI : 1 dominant (taille 2x, position privilégiée), 2 médians, 1 secondaire en bas.
- Casser le grid 3 colonnes : composition asymétrique avec tailles variables.
- Créer un point focal (alerte, KPI critique, ou métrique signature) qui attire l'œil dès le chargement.
- Personnalité typographique : différentiation claire entre titres et corps (size + weight).
</target>

<output>
Livre directement la version révisée complète.
Pas d'explication avant le rendu.
</output>
</revision_request>
```

### Example 2 — Pitch deck too corporate

**User critique** :
```
Le deck est propre mais corporate, on dirait un template McKinsey.
Pour un pitch early-stage de startup, faut plus d'audace, plus de personnalité.
```

**Designor revise output** :

```xml
<revision_request>
<preserve>
Conserve l'arc narratif (Problème → Solution → Marché → Produit → Traction → Ask).
Conserve les chiffres et données.
Conserve la structure 12 slides.
</preserve>

<defects>
Le rendu actuel a 4 problèmes :
1. Style trop corporate / consulting (palette neutre, layouts ultra-symétriques).
2. Photos stock impersonnelles (handshakes, smiling people in suits).
3. Aucune slide de rupture — tout enchaîne au même rythme.
4. Manque de signature visuelle (rien qu'on retiendrait de ce deck).
</defects>

<target>
Révise avec ces objectifs :
- Adopter un style founder-led / indie maker plutôt que consulting (palette plus affirmée, typo avec personnalité).
- Remplacer les photos stock par des mockups produit ou illustrations sur-mesure.
- Ajouter 2 slides de rupture (transitions visuelles fortes entre Problème→Solution et Produit→Traction).
- Créer un élément signature qui revient sur 3-4 slides (mark visuelle, motif, citation, etc.).
- Assumer plus de tension visuelle : asymmetric layouts, contrast, bold typography.
</target>

<output>
Livre directement la version révisée complète.
Pas d'explication avant le rendu.
</output>
</revision_request>
```

### Example 3 — One-pager too dense

**User critique** :
```
Trop dense, on lit pas. Les bénéfices sont noyés dans le texte.
Faut alléger.
```

**Designor revise output** :

```xml
<revision_request>
<preserve>
Conserve la structure des sections (Hero, Bénéfices, Preuve, CTA).
Conserve le contenu textuel intégral, je veux juste le présenter mieux.
Conserve la palette et le logo placement.
</preserve>

<defects>
Le rendu actuel a 2 problèmes :
1. Densité texte trop élevée — paragraphes longs au lieu de phrases courtes.
2. Les 3 bénéfices clés sont noyés visuellement (pas assez différenciés du reste du contenu).
</defects>

<target>
Révise avec ces objectifs :
- Convertir les paragraphes en phrases courtes (6-12 mots) ou bullets serrés.
- Mettre les 3 bénéfices clés en avant : icônes plus visibles, typo plus marquée, encadré ou couleur de fond distincte.
- Créer une vraie respiration entre sections (white space accru).
- Hero plus impactant avec CTA primaire dominant visuellement.
</target>

<output>
Livre directement la version révisée complète.
Pas d'explication avant le rendu.
</output>
</revision_request>
```

## Anti-Patterns in Revise Prompts

### ❌ Avoid

- "Refais en mieux" → no observable criteria
- "Plus de [adjectif vague]" → modern, premium, sexy, beautiful
- "Inverse les problèmes du précédent" → Claude doesn't know what was wrong
- "Refais à partir de zéro" → loses what worked
- 5+ defects listed → Claude can't prioritize
- Multiple targets that contradict → "plus dense ET plus aéré"
- "Tu peux m'expliquer ce que tu vas changer ?" → loses revision opportunity to chat overhead

### ✅ Prefer

- 2-4 specific observable defects
- Targets that are measurable or visualizable
- Preserve clause that anchors the revision
- "Livre directement" to bypass explanation overhead

## When to Stop Revising

After 2-3 revisions without convergence:

```
⚠️ On en est à la [3e] révision sans convergence claire.
Suggestion : changer d'angle d'attaque plutôt que continuer à itérer.

Options :
1. Changer de style anchors (Linear-like → Editorial magazine)
2. Repartir du brief initial avec angle audience différent
3. Mode `explore` pour générer 3 directions radicalement différentes

Laquelle te tente ?
```

This prevents the user from spiraling on a fundamentally bad direction.

## Integration with Token Economy

Revise prompts are typically used IN Claude Design via Comment mode (moderate token cost) or new generation (high). Designor recommends:

1. First try Tweaks for the specific defects (palette, density, radius via sliders) — 0 tokens
2. If Tweaks insufficient, use revise prompt via Comment on specific section — moderate cost
3. Full new generation only if revision is structural — high cost

```
💡 Astuce : avant d'appliquer cette révision, teste si tes défauts peuvent être
corrigés via Tweaks (palette, density, radius) — ça consomme 0 token.
Si oui, applique d'abord les Tweaks, puis re-évalue les défauts restants.
```
