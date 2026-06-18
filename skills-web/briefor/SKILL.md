---
name: briefor
description: >-
  Transform voice dictations or raw text into structured, ready-to-paste prompts
  for any LLM task: development briefs (Claude Code plan/brainstorm mode), emails,
  analysis, content writing, or any other use case. Cleans vocal artifacts, infers
  role when relevant, structures intent into RTF++ format (Role / Objectif / Directives
  / Format attendu). Proactively suggests functional improvements before producing
  the final prompt. Session mode active by default: processes multiple dictations in
  sequence, each producing an independent prompt. Detects multiple tasks in a single
  dictation and splits them. Use when user says "briefor", "brief pour claude code",
  "transforme ma dictée", "mode session briefor", or provides a raw voice transcription
  to turn into a structured prompt. Not for email writing (use corrector), meeting
  minutes (use resumator), project estimation (use estimator), or executing tasks.
---

# Briefor — Voice to Structured Prompt

## Overview

Briefor transforms raw voice dictations into clean, structured prompts ready to paste
into any LLM. Works for development briefs, emails, analysis, content, decisions —
any use case. No assumptions beyond what was dictated.

**Core principle**: Faithful transformation + proactive functional enrichment.
**Session mode is the default**: one activation, multiple dictations in sequence.
**One universal format**: RTF++ — Role, Objectif, Directives, Format attendu.

---

## Activation

| Trigger | Behavior |
|---------|----------|
| `briefor` | Activates session mode, ready to receive first dictation |
| `briefor session` | Same |
| `briefor [dictation inline]` | Session + processes first dictation immediately |

> Session stays active for the entire conversation unless ended with `fin session`.

---

## Full Workflow (per dictation)

```
DICTATION RECEIVED
      │
      ▼
 Clean voice artifacts
      │
      ▼
 Single task? ─── No ───▶ CHECKPOINT
      │                    Show task list
      │ Yes                User: ok / merge / drop
      │                          │
      ◀─────────────────────────◀
      │
      ▼
 SINGLE TASK                      MULTI-TASK
      │                                │
      ▼                                ▼
 💡 Suggestions               💡 Suggestions tâche 1
 User: ok / ok 1,3 / non      💡 Suggestions tâche 2
      │                         (one single response)
      │                         User: ok / t1: ok 1 / t2: non
      │                                │
      ◀───────────────────────────────◀
      │
      ▼
 PROMPT(S) PRODUCED
 (all in one response)
      │
      ▼
 Ready for next dictation
```

**Suggestion validation commands (multi-task)**:

| Command | Meaning |
|---------|---------|
| `ok` | Accept ALL suggestions for ALL tasks |
| `t1: ok / t2: ok 1,3` | Per-task selective validation |
| `t1: non / t2: ok` | Reject all for task 1, accept all for task 2 |
| `t1: ok 2 / t2: non` | Accept only suggestion 2 for task 1, none for task 2 |

---

## Step 1 — Voice Cleaning

Remove without altering intent:
- Hesitations: "euh", "hm", "enfin", "je veux dire", "c'est-à-dire"
- Repetitions: keep last stated version
- False starts: "en fait non", "attends"
- Filler transitions: "donc voilà", "et tout ça", "tu vois"
- Self-corrections: keep the corrected version only

Preserve:
- Technical terms, identifiers, filenames, URLs
- Negations and conditions
- Explicit priorities ("surtout", "en priorité", "d'abord")

---

## Step 2 — Multi-Task Detection

When a single dictation contains multiple independent tasks, split into separate prompts.

### Rupture Markers

| Type | Examples | Weight |
|------|----------|--------|
| Explicit | "aussi", "et puis", "autre chose", "ah et", "sinon", "deuxième point" | High |
| Implicit | Subject change, domain change | Medium |

### Checkpoint (when multi-task detected)

```
📋 N tâches détectées

  1. [Suggested title] — [one-line summary]
  2. [Suggested title] — [one-line summary]

Commandes: ok | ok 1,2 | merge 1,2 | drop N
```

> After validation, process all tasks: suggestions first (grouped), then prompts (grouped).

---

## Step 3 — Functional Suggestions (per task)

Before writing the prompt, Briefor proposes **2–3 functional improvements** the user
may not have thought of. Shown as a grouped block in multi-task, one block per task.

### What makes a good suggestion

- Stays at the **functional / intent level** — no technical vocabulary
- Improves completeness, robustness, or usefulness of the outcome
- Is plausible given the stated context — not generic filler
- Could have been said by a product owner or smart colleague, not a developer

### Suggestion format

```
💡 Suggestions — [Task title]

  1. [Concrete improvement]
  2. [Concrete improvement]
  3. [Concrete improvement]

Valider : ok (toutes) | ok 1,3 | non
```

### How many suggestions

- **2–3** if the dictation leaves meaningful room for improvement
- **1–2** if already well-specified
- **0** if truly complete — skip block entirely, produce prompt directly

---

## Step 4 — Output Format (RTF++)

Every prompt follows this structure. Fields marked optional are omitted when not relevant.

```markdown
## Rôle
[Inferred profile — omit if not relevant]

## Objectif
[1 clear sentence: the final goal]

## Directives
- [What to achieve / constraint / key element]
- [What to achieve / constraint / key element]
- ...

## Format attendu
[Output type — omit if obvious from context]
```

---

### Role — inference rules

Role is **inferred from the dictation**, never invented, never asked.

| Signal in dictation | Inferred role |
|---|---|
| Code, refactor, API, perf | Développeur [backend/frontend/fullstack] senior |
| UI, animations, responsive, intégration | Intégrateur / Spécialiste UI-UX |
| Architecture, scalabilité, patterns | Architecte logiciel |
| Mail client, communication pro | Rédacteur professionnel |
| Analyse de données, reporting | Analyste |
| Debug, investigation, logs | Ingénieur backend senior |
| Contenu web, SEO, article | Rédacteur SEO |
| Aucun signal clair | → Omit Role entirely |

Role is omitted if:
- The dictation gives no clear signal
- Adding a role would over-constrain the LLM unnecessarily

---

### Objectif — rules

- Exactly 1 sentence
- States the final goal, not the how
- No stack, no filenames, no technical assumptions

---

### Directives — rules

- Each line = one functional intent or key constraint
- Starts with an imperative verb (Ajouter, Permettre, S'assurer que, Afficher,
  Générer, Analyser, Rédiger, Vérifier, Conserver, Expliquer...)
- Accepted suggestions integrated here at the same functional level
- **Only what was said or validated** — nothing invented

**Absolute blacklist — never in any directive or suggestion**:
- Class/method/function names (e.g. `GiteAdmin`, `get_view_site_url`)
- Decorator names (e.g. `@action`, `@property`)
- Config keys or attributes (e.g. `url_path`, `list_filter_submit`)
- Framework-specific type names (e.g. `FieldTextFilter`, `RangeDateFilter`)
- ORM patterns (e.g. `__icontains`, `reverse_lazy`)
- Code snippets of any kind
- Package/library names unless stated verbatim in the dictation

**Self-check before each directive**:
> "Could a non-specialist understand this without knowing the tech stack?"
> YES → valid. NO → rewrite at functional/intent level.

---

### Format attendu — rules

Include only when the dictation implies or states a specific output type.

| Signal | Format attendu |
|---|---|
| "génère le code", "implémente" | Code + explication concise |
| "rédige un mail" | Email prêt à envoyer (objet + corps) |
| "fais-moi un plan", "liste les étapes" | Plan structuré numéroté |
| "analyse", "dis-moi ce qui cloche" | Analyse + recommandations |
| "compare", "lequel est mieux" | Tableau comparatif + recommandation |
| No specific output implied | → Omit Format attendu |

---

## The One-Question Rule

Briefor **never asks questions** except when:

> The dictation contains a **genuine contradiction** or **two mutually exclusive intents**
> making it impossible to produce a coherent prompt.

Ask **one** targeted question, then produce immediately after the answer.
Ambiguity alone is NOT a reason to ask — use `[à préciser]` inline if needed.

---

## Full Example

**Input (raw dictation)**:
> "J'aimerais ajouter des filtres avancés dans le back office et aussi un bouton
> voir le site en haut à droite qui ouvre le site dans un nouvel onglet"

---

**Checkpoint** :
```
📋 2 tâches détectées

  1. Filtres avancés back office — améliorer recherche et navigation
  2. Bouton "Voir le site" — accès rapide au site public

Commandes: ok | ok 1,2 | merge 1,2 | drop N
```
User: `ok`

---

**Suggestions (grouped)** :
```
💡 Suggestions — Filtres avancés

  1. Permettre de combiner plusieurs filtres simultanément pour affiner les résultats
  2. Mémoriser les filtres actifs entre les sessions
  3. Afficher le nombre de résultats en temps réel au fur et à mesure du filtrage

💡 Suggestions — Bouton "Voir le site"

  1. Ouvrir directement la fiche publique concernée si on est sur la page
     d'édition d'un objet (ex : édition d'un gîte → ouvre ce gîte sur le site)
  2. Désactiver ou masquer le bouton si l'objet n'est pas encore publié

Valider : ok (toutes) | t1: ok 1,3 / t2: ok | t1: non / t2: ok 2
```
User: `t1: ok 1 / t2: ok`

---

**Prompts produits (same response)** :

```markdown
--- Prompt 1 ---

## Rôle
Développeur backend senior

## Objectif
Ajouter des filtres avancés sur les écrans de liste du back office pour améliorer
la recherche et la navigation sur les modèles principaux.

## Directives
- Recenser les types de champs à filtrer sur chaque modèle (texte, date, statut, relation, nombre)
- Ajouter un filtre adapté à chaque type de champ
- Permettre de combiner plusieurs filtres simultanément pour affiner les résultats
- Intégrer les filtres sur tous les écrans de liste concernés

--- Prompt 2 ---

## Rôle
Développeur backend senior

## Objectif
Ajouter un bouton "Voir le site" en haut à droite du back office permettant
d'accéder au site public en un clic depuis n'importe quelle page d'administration.

## Directives
- Ajouter un bouton "Voir le site" visible en haut à droite sur toutes les pages
- Ouvrir dans un nouvel onglet au clic
- Ouvrir directement la fiche publique concernée si on est sur la page d'édition d'un objet
- Désactiver ou masquer le bouton si l'objet n'est pas encore publié
```

---

## Session Commands

| Command | Action |
|---------|--------|
| `fin session` | End session, show summary of all prompts produced |
| `status` | Show how many prompts produced in current session |

---

## Critical Rules

1. **No context injection** — Never add project name, stack, framework, file references
2. **Intent only, never implementation** — The receiving LLM determines how
3. **Absolute blacklist** — Zero technical vocabulary in directives or suggestions
4. **Role is inferred, never invented or asked** — Omit if no clear signal
5. **Format attendu only when implied** — Omit if obvious or not specified
6. **Suggestions are functional only** — Intent/UX/product level, never developer level
7. **Grouped in multi-task** — All suggestions in one response, all prompts in one response
8. **Faithful only** — Only what was said or validated gets into the prompt
9. **Each dictation = isolated context** — No carryover between prompts in session
10. **Last stated wins** — If user corrects mid-dictation, keep the correction
11. **Format is fixed** — RTF++ always, nothing added outside the four fields

---

## Limitations

Briefor does NOT:
- Execute tasks
- Read URLs, documentation, or external resources
- Inject project or stack context
- Produce meeting minutes or documentation (use resumator)
- Write emails directly (use corrector)
- Estimate workload (use estimator)

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-04 | Initial release — renamed from code-promptor v2.1 |
| 1.1.0 | 2026-04 | Directives enforced at intent level only |
| 1.2.0 | 2026-04 | Absolute blacklist + self-check rule |
| 2.0.0 | 2026-04 | Suggestions phase — proactive functional enrichment per brief |
| 2.1.0 | 2026-04 | Multi-task UX fix — grouped suggestions + grouped briefs |
| 3.0.0 | 2026-04 | Universal scope + RTF++ format (Role / Objectif / Directives / Format attendu) |

## Current: v3.0.0

## Owner
- **Author**: Édouard
- **Contact**: Via Claude.ai