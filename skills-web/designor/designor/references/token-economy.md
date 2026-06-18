# Token Economy — Claude Design Optimization

> ⚠️ **DISCLAIMER — Chiffres datés (avril 2026)**
>
> Les chiffres techniques cités dans ce document (quotas, pourcentages de consommation, prix des plans, comportements UI spécifiques) proviennent de sources publiées entre le 17 et le 30 avril 2026, alors que Claude Design est en research preview depuis 13 jours seulement. **Ces chiffres peuvent évoluer rapidement** :
>
> - Quotas Claude Design (Pro / Max / Team / Enterprise) — vérifier sur [claude.ai/upgrade](https://claude.ai/upgrade)
> - Comportement du design system (consommation tokens à l'activation) — peut être optimisé sans préavis
> - Workflow handoff Claude Code — interface susceptible de changer
> - Mécanique des Tweaks (instruction "agressifs", coût des modes Edit/Comment/Chat) — basée sur retours d'utilisateurs early access
> - Comportements `--no-inspiration` et `--freshness-check` — non testés en conditions d'usage massif
>
> **Avant déploiement extensif** : valider via la doc officielle Anthropic ([docs.claude.com](https://docs.claude.com)) ou un perplexitor ciblé. Les patterns conceptuels (Edit > Tweaks > Comment > Chat, délégation animations à Claude Code) restent valides indépendamment des chiffres exacts.

---

Claude Design has its own token quota, separate from Claude Code and chat. Without awareness, two intensive sessions can consume 50%+ of weekly Pro quota. This reference details all token-saving patterns designor systematically applies.

## The 3 Cost Tiers in Claude Design

| Action | Token Cost | When to use |
|--------|------------|-------------|
| **Edit** (click element, modify directly) | **0** | Adjust size, color, typography, margin on a specific element |
| **Tweaks** (sliders, toggles auto-generated) | **0** | Iterate on global properties (palette, density, radius, spacing) |
| **Comment** (point + instruction on element) | Moderate | Modify behavior or content of a specific element |
| **Chat** (conversation, new generation) | High | Structural changes, new sections, full regenerations |

**Order of preference**: Edit > Tweaks > Comment > Chat.

## Pattern 1 — Aggressive Tweaks (ALWAYS injected)

After the first generation in Claude Design, Claude exposes a few default Tweaks. The user can dramatically expand them with a single Chat instruction.

**Exact text designor injects in section 3 of every output**:

```
🎛️ Astuce critique — Maximiser les Tweaks (à faire APRÈS la 1ère génération) :

Dans le chat de Claude Design, tape exactement :
"Augmente le nombre de Tweaks de façon agressive. Je veux pouvoir jouer avec
le design un maximum."

Cela démultiplie les sliders/toggles disponibles : couleurs, typographie, layout,
espacement, rotation d'éléments, contenu, etc. Une fois en place, chaque
modification est INSTANTANÉE et SANS CONSOMMATION DE TOKENS.

Investir 1 requête Chat pour ça est rentable sur l'ensemble du projet.
```

Justification: video research confirmed this is the single most impactful token-saving move.

## Pattern 2 — Design System Toggle

Activating the Claude Design "design system" feature consumes 20-25% of project quota at startup, before any creation.

**Designor's recommendation logic**:

| Scenario | Recommendation |
|----------|----------------|
| First project ever / experimentation | **DISABLE** design system → save 20-25% quota |
| Pointable codebase + valuable extraction | **ENABLE** if the cost is justified by reusable extraction |
| Figma files to import | **ENABLE** for proper Figma extraction |
| Brand charter (palette + logo, no DS) | **DISABLE**, charter loaded manually in prompt's `<design_tokens>` |
| Returning project with existing setup | **ENABLE** (already paid, reuse) |

Injected in section 3 of output:

```
⚙️ Configuration recommandée pour ce projet :
Design system Claude Design : [DÉSACTIVÉ / ACTIVÉ]
Justification : [...]
```

## Pattern 3 — Animations / 3D / Scroll Effects → Claude Code

Claude Design is NOT optimized for animations, 3D models, or complex scroll effects. Asking for them in the Design prompt:
- Burns Design tokens for poor results
- Produces fragile or static animations
- Better delegated to Claude Code in handoff phase

**Rule**: designor NEVER asks for animations/3D/scroll-effects in the prompt, EXCEPT in `wireframe-handoff` template, where it prepares hooks for Claude Code:

```xml
<!-- In wireframe-handoff template only -->
<animation_hooks>
Préparer les zones où Claude Code ajoutera des animations en aval :
- Hero : marquer comme zone d'animation parallax / split-reveal
- Cards : marquer comme entrée animée au scroll (stagger)
- CTAs : marquer comme micro-interactions hover/active
Ne PAS implémenter les animations dans le rendu Claude Design — laisser Claude Code gérer.
</animation_hooks>
```

For other templates, designor injects in section 3:

```
🎬 Animations / 3D / scroll effects :
Ne demande PAS ces éléments à Claude Design (consommation tokens élevée pour résultats fragiles).
Délègue à Claude Code en aval :
- Animations CSS / motion → Claude Code via composants 21st.dev
- Modèles 3D → Sketchfab GLB → Claude Code intègre via Three.js
- Scroll effects → 21st.dev "Scroll Media Expansion Hero" ou équivalent
```

## Pattern 4 — High Fidelity vs Low Fidelity Trade-off

Claude Design offers fidelity levels at project creation:
- **High Fidelity** : polished design, 1-2 generations to good result, but more tokens per generation
- **Low Fidelity** : wireframes, more generations needed, less tokens each

**Designor recommendation logic**:

| Template | Recommended fidelity | Reasoning |
|----------|---------------------|-----------|
| `ui` | High | Polished UI is the goal, save iteration cycles |
| `wireframe-handoff` | Low | Wireframes ARE the deliverable, hi-fi adds noise |
| `deck` | High | Polished slides expected immediately |
| `one-pager` | High | Production-ready output expected |
| `social` | High | Final-form visuals expected |
| `explore` | High | Need to feel the visual difference between directions |

Injected in section 2 (preparation checklist):

```
⚙️ Mode fidélité Claude Design : [High Fidelity / Low Fidelity]
```

## Pattern 5 — Visual Inspiration Attached, Not Described

Long verbal descriptions of visual references waste tokens. Better: attach actual images.

**Designor instructs in section 2**:

```
📎 Préparation visuelle :
Attache 3+ images de référence DIRECTEMENT dans Claude Design (pas via description texte).
Sources :
- Pinterest : recherche "[theme adapté au livrable]"
- Dribbble : recherche "[theme]"
- Mobbin (apps réelles) : pour template ui/wireframe
- Captures de sites que tu aimes
Les images attachées sont 10x plus efficaces qu'une description verbale, et consomment
moins de tokens d'élicitation.
```

## Pattern 6 — Batching Modifications

When multiple modifications are needed:
- ❌ Bad: send 5 separate Chat messages → 5x token cost
- ✅ Good: batch into 1 Chat message with numbered list

Injected occasionally in section 3 when relevant:

```
💡 Si plusieurs modifications nécessaires en Chat, batch-les en 1 message :
"Modifie 3 choses :
1. Hero : aligner CTA à gauche
2. Section bénéfices : passer de 3 à 4 colonnes
3. Footer : ajouter logo + mentions légales"
```

## Pattern 7 — Prompt Length Discipline

XML prompts produced by designor are dense but bounded. Avoid:
- Repetition between sections (e.g., palette mentioned in both visual_direction and design_tokens)
- Over-specification of obvious patterns
- Multiple paragraphs where bullets suffice

**Designor's prompt length targets**:

| Mode | Target prompt length |
|------|----------------------|
| `quick` | 100-200 words (4-block brief) |
| `standard` | 400-600 words (full XML) |
| `deep` | 600-900 words (XML + variants) |

Going beyond reduces effectiveness AND increases token cost.

## Pattern 8 — Re-generation vs Tweaks vs Comment Decision Tree

When user wants to iterate, designor's `revise` sub-command suggests:

```
Avant d'appliquer la révision via Chat (coût tokens élevé), évalue d'abord :

1. Les défauts peuvent-ils être corrigés via Tweaks (palette, density, radius, spacing) ?
   → Si oui : applique les Tweaks (0 token), puis re-évalue.

2. Les défauts touchent un élément spécifique (un seul CTA, un seul header) ?
   → Si oui : utilise Comment sur cet élément (coût modéré).

3. Les défauts sont structurels (hiérarchie, layout, narrative) ?
   → Alors seulement : utilise Chat avec le revision_prompt structuré (coût élevé).
```

## Pattern 9 — Quota Awareness Warnings

In `deep` mode, designor proactively warns about quota:

```
⚠️ Attention quota :
Une session deep mode + 2-3 itérations ≈ 30-40% de ton quota Claude Design hebdo (Pro).
Si tu prévois plusieurs projets cette semaine :
- Privilégier mode standard pour les autres
- Désactiver le design system sur ce projet (si pas vital)
- Maximiser Tweaks et Edit (0 token)
```

## Pattern 10 — Handoff to Claude Code Optimization

For `wireframe-handoff` template specifically:

```
🔁 Optimisation handoff Claude Code :
Une fois le design validé dans Claude Design :
- Utilise Share → Send to Claude Code (la commande pré-écrite)
- Le handoff bundle préserve tokens, layout, composants — FIDÉLITÉ MAXIMALE
- Ne PAS demander à Claude Design de "préparer le code" (perte de tokens)
- Animations, 3D, assets dynamiques → ajoutés UNIQUEMENT côté Claude Code

Workflow optimal :
Phase 1 (Claude Design) : design statique parfait → handoff
Phase 2 (Claude Code) : intégration animations + assets + interactivité dynamique
```

## Summary — Section 3 Output Structure

Every designor output's section 3 (token economy tips) systematically contains:

1. ✅ Aggressive Tweaks instruction (exact text)
2. ✅ Design system toggle recommendation (case-specific)
3. ✅ Animations/3D delegation note (template-aware)
4. ✅ Visual inspiration attachment reminder
5. ✅ Mode fidélité (High Fidelity / Low Fidelity) recommandation
6. Conditional based on context:
   - Batching tip (if multi-modification expected)
   - Quota warning (deep mode only)
   - Handoff optimization (wireframe-handoff only)

This systematization is what differentiates designor's output from a manual prompt — the user gets the elicitation expertise AND the operational expertise in one shot.
