# Breakpoint Display Formats

> ASCII box templates for brainstorm breakpoints. Single source of truth for visual formats.

## Common Elements

### Progress Bars

```
Format: [{filled}{empty}] {score}/100

Filled char: █
Empty char: ░

Examples:
[████████░░] 80/100
[██████░░░░] 60/100
[████░░░░░░] 40/100
[██░░░░░░░░] 20/100
```

### Proactive Suggestions

```
Format: [P{n}] {suggestion}

Priority levels:
[P1] — Critical/Most impactful
[P2] — Important/Recommended
[P3] — Nice-to-have/Optional
```

### Standard Options Block

```
├─────────────────────────────────────────────────────────────────────┤
│ ┌─ Options ──────────────────────────────────────────────────────┐ │
│ │  [A] {primary} (Recommended) — {description}                   │ │
│ │  [B] {secondary} — {description}                               │ │
│ │  [C] {tertiary} — {description}                                │ │
│ │  [?] Autre réponse...                                          │ │
│ └────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
```

---

## EMS Status Box

Used in: `step-04-iteration.md` (section 6)

### Template

```
┌─────────────────────────────────────────────────────────────────────┐
│ 📊 STATUT ITÉRATION {iteration}                                     │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│ EMS GLOBAL: {score}/100 ({delta})                                   │
│                                                                     │
│ AXES EMS                                                            │
│ ┌─────────────────────────────────────────────────────────────────┐ │
│ │ Clarté        [{bar}] {clarity}/100                             │ │
│ │ Profondeur    [{bar}] {depth}/100                               │ │
│ │ Couverture    [{bar}] {coverage}/100                            │ │
│ │ Décisions     [{bar}] {decisions}/100                           │ │
│ │ Actionnabilité[{bar}] {actionability}/100                       │ │
│ └─────────────────────────────────────────────────────────────────┘ │
│                                                                     │
│ Phase: {DIVERGENT|CONVERGENT} | Persona: {persona}                  │
│ Itération: {n}/10 | Technique suggérée: {technique or "-"}          │
│ Axes faibles: {weak_axes}                                           │
│                                                                     │
├─────────────────────────────────────────────────────────────────────┤
│ SUGGESTIONS PROACTIVES                                              │
│ [P1] Focus sur {weak_axis} — actuellement le plus bas               │
│ [P2] Essaie {technique} pour débloquer {axis}                       │
│ [P3] Considère sauvegarder checkpoint si pause                      │
├─────────────────────────────────────────────────────────────────────┤
│ ┌─ Options ──────────────────────────────────────────────────────┐ │
│ │  [A] Continuer (Recommended) — Répondre et itérer              │ │
│ │  [B] Dive [sujet] — Approfondir un point                       │ │
│ │  [C] Pivoter — Réorienter                                      │ │
│ │  [D] Finir — Générer les outputs maintenant                    │ │
│ │  [?] Autre réponse...                                          │ │
│ └────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
```

### Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `{iteration}` | Current iteration number | `3` |
| `{score}` | EMS global score | `68` |
| `{delta}` | Change from previous | `+12` |
| `{bar}` | Progress bar (10 chars) | `████████░░` |
| `{clarity}` | Clarity axis score | `78` |
| `{depth}` | Depth axis score | `65` |
| `{coverage}` | Coverage axis score | `72` |
| `{decisions}` | Decisions axis score | `52` |
| `{actionability}` | Actionability axis score | `45` |
| `{phase}` | Current phase | `DIVERGENT` |
| `{persona}` | Active persona | `architecte` |
| `{technique}` | Suggested technique | `Six Hats` |
| `{weak_axes}` | Axes with score < 50 | `Decisions, Actionability` |

### AskUserQuestion Options

```json
{
  "question": "Comment voulez-vous continuer?",
  "header": "EMS {score}",
  "multiSelect": false,
  "options": [
    { "label": "Continuer (Recommended)", "description": "Répondre aux questions et itérer" },
    { "label": "Dive [sujet]", "description": "Approfondir un point spécifique" },
    { "label": "Pivoter", "description": "Réorienter vers un sujet émergent" },
    { "label": "Finir", "description": "Générer les outputs maintenant" }
  ]
}
```

---

## Framing Validation Box

Used in: `step-03-breakpoint-framing.md` (section 3)

### Template

```
┌─────────────────────────────────────────────────────────────────────┐
│ 📋 VALIDATION DU CADRAGE                                            │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│ MÉTRIQUES                                                           │
│ • Template: {template}                                              │
│ • EMS initial: {ems_initial}/100                                    │
│ • Questions HMW: {hmw_count}                                        │
│ • Contexte codebase: {available|partial|none}                       │
│                                                                     │
│ RÉSUMÉ DU BRIEF                                                     │
│ {brief_v0_condensed}                                                │
│                                                                     │
│ QUESTIONS DE CADRAGE                                                │
│ [Target] {question_target}                                          │
│   → Suggestion: {suggestion_target}                                 │
│ [Constraints] {question_constraints}                                │
│   → Suggestion: {suggestion_constraints}                            │
│ [Timeline] {question_timeline}                                      │
│   → Suggestion: {suggestion_timeline}                               │
│                                                                     │
├─────────────────────────────────────────────────────────────────────┤
│ SUGGESTIONS PROACTIVES                                              │
│ [P1] Template '{template}' sélectionné — adapté à votre sujet       │
│ [P2] EMS départ: {ems.global} — typique pour brief validé           │
│ [P3] Révisez les questions HMW — elles guident l'exploration        │
├─────────────────────────────────────────────────────────────────────┤
│ ┌─ Options ──────────────────────────────────────────────────────┐ │
│ │  [A] Démarrer itérations (Recommended) — Exploration structurée│ │
│ │  [B] Ajuster cadrage — Modifier template ou brief              │ │
│ │  [C] Ajouter contexte — Plus de background d'abord             │ │
│ │  [?] Autre réponse...                                          │ │
│ └────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
```

### Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `{template}` | Selected template | `feature-development` |
| `{ems_initial}` | Initial EMS score | `35` |
| `{hmw_count}` | Number of HMW questions | `3` |
| `{brief_v0_condensed}` | Summary of brief | `Build auth system...` |
| `{question_target}` | Target clarification | `Who exactly will use this?` |
| `{question_constraints}` | Constraints question | `Any technical limits?` |
| `{question_timeline}` | Timeline question | `Is there a deadline?` |

### AskUserQuestion Options

```json
{
  "question": "Prêt à démarrer les itérations d'exploration?",
  "header": "Framing",
  "multiSelect": false,
  "options": [
    { "label": "Démarrer itérations (Recommended)", "description": "Commencer exploration structurée" },
    { "label": "Ajuster cadrage", "description": "Modifier template ou brief" },
    { "label": "Ajouter contexte", "description": "Fournir plus de background d'abord" }
  ]
}
```

---

## Finish Validation Box

Used in: `step-05-breakpoint-finish.md` (section 3)

### Template

```
┌─────────────────────────────────────────────────────────────────────┐
│ 🏁 FIN D'EXPLORATION                                                │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│ MÉTRIQUES                                                           │
│ • Itérations: {count}                                               │
│ • EMS final: {ems.global}/100                                       │
│ • Décisions prises: {decisions.length}                              │
│ • Threads ouverts: {open_threads.length}                            │
│ • Techniques utilisées: {techniques_applied.length}                 │
│                                                                     │
│ RÉSUMÉ                                                              │
│ Décisions clés:                                                     │
│ • {decision_1}                                                      │
│ • {decision_2}                                                      │
│                                                                     │
│ Progression EMS: {initial} → {final} (+{delta})                     │
│ Évaluation qualité: {EXCELLENT|GOOD|ADEQUATE|LOW}                   │
│                                                                     │
├─────────────────────────────────────────────────────────────────────┤
│ SUGGESTIONS PROACTIVES                                              │
│ [P1] {open_threads.length} threads ouverts seront notés dans brief  │
│ [P2] EMS final {score} — {quality_assessment}                       │
│ [P3] Preview montre le découpage avant validation                   │
├─────────────────────────────────────────────────────────────────────┤
│ ┌─ Options ──────────────────────────────────────────────────────┐ │
│ │  [A] Générer outputs (Recommended) — Créer brief et journal    │ │
│ │  [B] Preview d'abord — Voir découpage @planner                 │ │
│ │  [C] Continuer itérations — Explorer davantage                 │ │
│ │  [D] Sauvegarder checkpoint — Pause pour reprise               │ │
│ │  [?] Autre réponse...                                          │ │
│ └────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
```

### Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `{count}` | Total iterations | `5` |
| `{ems.global}` | Final EMS score | `78` |
| `{decisions.length}` | Number of decisions | `8` |
| `{open_threads.length}` | Open threads count | `2` |
| `{techniques_applied.length}` | Techniques used | `3` |
| `{decision_1}`, `{decision_2}` | Key decisions | `Use JWT auth` |
| `{initial}` | Starting EMS | `35` |
| `{final}` | Ending EMS | `78` |
| `{delta}` | Total delta | `+43` |
| `{quality_assessment}` | Quality level | `GOOD` |

### Quality Levels

| EMS Range | Level | Color |
|-----------|-------|-------|
| 90-100 | EXCELLENT | Green |
| 70-89 | GOOD | Blue |
| 50-69 | ADEQUATE | Yellow |
| < 50 | LOW | Red |

### AskUserQuestion Options

```json
{
  "question": "Prêt à générer les outputs?",
  "header": "Finish",
  "multiSelect": false,
  "options": [
    { "label": "Générer outputs (Recommended)", "description": "Créer brief et journal" },
    { "label": "Preview d'abord", "description": "Voir découpage @planner avant finalisation" },
    { "label": "Continuer itérations", "description": "Ajouter plus d'exploration" },
    { "label": "Sauvegarder checkpoint", "description": "Pause pour reprise ultérieure" }
  ]
}
```

---

## Clarification Box

Used in: `step-01-clarify.md` (section 3)

### Template

```
┌─────────────────────────────────────────────────────────────────────┐
│ ❓ CLARIFICATION                                                    │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│ Idée originale: {idea_raw}                                          │
│ Score de clarté: {clarity_score}/1.0                                │
│                                                                     │
│ Questions de clarification:                                         │
│ ┌─────────────────────────────────────────────────────────────────┐ │
│ │ [Scope] {question_1}                                            │ │
│ │   → Suggestion: {suggestion_1}                                  │ │
│ │                                                                 │ │
│ │ [Users] {question_2}                                            │ │
│ │   → Suggestion: {suggestion_2}                                  │ │
│ └─────────────────────────────────────────────────────────────────┘ │
│                                                                     │
├─────────────────────────────────────────────────────────────────────┤
│ ┌─ Options ──────────────────────────────────────────────────────┐ │
│ │  [A] Répondre aux questions (Recommended) — fournir réponses   │ │
│ │  [B] Ignorer clarification — continuer tel quel                │ │
│ │  [C] Reformuler l'idée — recommencer                           │ │
│ │  [?] Autre réponse...                                          │ │
│ └────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
```

### Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `{idea_raw}` | Original user idea | `Add dark mode to the app` |
| `{clarity_score}` | Calculated clarity score | `0.6` |
| `{question_1}` | First clarification question | `What's the boundary of this feature?` |
| `{suggestion_1}` | Suggestion for question 1 | `Focus on the main UI only` |
| `{question_2}` | Second clarification question | `Who is the primary user?` |
| `{suggestion_2}` | Suggestion for question 2 | `End users on web platform` |

### AskUserQuestion Options

```json
{
  "question": "Répondez aux questions pour clarifier votre idée:",
  "header": "Clarify",
  "multiSelect": false,
  "options": [
    { "label": "Répondre aux questions (Recommended)", "description": "Fournir réponses inline" },
    { "label": "Ignorer clarification", "description": "Continuer tel quel" },
    { "label": "Reformuler l'idée", "description": "Recommencer avec description plus claire" }
  ]
}
```

---

## Brief Validation Box

Used in: `step-01-clarify.md` (section 6)

### Template

```
┌─────────────────────────────────────────────────────────────────────┐
│ ✅ VALIDATION DU BRIEF                                              │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│ Brief reformulé:                                                    │
│ ┌─────────────────────────────────────────────────────────────────┐ │
│ │ {reformulated_brief}                                            │ │
│ └─────────────────────────────────────────────────────────────────┘ │
│                                                                     │
│ Changements par rapport à l'original:                               │
│ • {diff1}                                                           │
│ • {diff2}                                                           │
│                                                                     │
├─────────────────────────────────────────────────────────────────────┤
│ ┌─ Options ──────────────────────────────────────────────────────┐ │
│ │  [A] Valider (Recommended) — Continuer avec ce brief           │ │
│ │  [B] Ajuster — Faire des corrections                           │ │
│ │  [C] Rejeter — Recommencer                                     │ │
│ │  [?] Autre réponse...                                          │ │
│ └────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
```

### Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `{reformulated_brief}` | Reformulated brief content | `Build a dark mode toggle...` |
| `{diff1}` | First change from original | `Added scope boundaries` |
| `{diff2}` | Second change from original | `Clarified target users` |

### AskUserQuestion Options

```json
{
  "question": "Cette reformulation est-elle correcte?",
  "header": "Validate",
  "multiSelect": false,
  "options": [
    { "label": "Valider (Recommended)", "description": "Continuer avec ce brief" },
    { "label": "Ajuster", "description": "Faire des corrections" },
    { "label": "Rejeter", "description": "Recommencer" }
  ]
}
```

---

## Perplexity Research Box

Used in: `step-02-framing.md` (section 5)

### Template

```
┌─────────────────────────────────────────────────────────────────────┐
│ 🔍 PROMPTS DE RECHERCHE PERPLEXITY                                  │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│ Prompts générés pour recherche externe:                             │
│                                                                     │
│ **1. {topic_1}** {mode_1}                                           │
│ `{query_1}`                                                         │
│ → Objectif: {objective_1}                                           │
│                                                                     │
│ **2. {topic_2}** {mode_2}                                           │
│ `{query_2}`                                                         │
│ → Objectif: {objective_2}                                           │
│                                                                     │
│ 💡 Copiez les prompts vers Perplexity, collez les résultats ici     │
│                                                                     │
├─────────────────────────────────────────────────────────────────────┤
│ ┌─ Options ──────────────────────────────────────────────────────┐ │
│ │  [A] Lancer recherche (Recommended) — Je colle quand prêt      │ │
│ │  [B] Ignorer recherche — Continuer sans recherche externe      │ │
│ │  [C] Autres prompts — Ajuster le focus                         │ │
│ │  [?] Autre réponse...                                          │ │
│ └────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
```

### Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `{topic_1}` | First research topic | `Authentication patterns` |
| `{mode_1}` | Research mode | `Standard` or `Deep Research` |
| `{query_1}` | Perplexity query | `Django 5 OAuth2 best practices 2025 2026` |
| `{objective_1}` | Why this research helps | `Identify recommended auth flow` |
| `{topic_2}` | Second research topic | `Testing strategies` |
| `{mode_2}` | Research mode | `Standard` |
| `{query_2}` | Perplexity query | `pytest Django integration testing 2025 2026` |
| `{objective_2}` | Why this research helps | `Ensure test coverage approach` |

### AskUserQuestion Options

```json
{
  "question": "Voulez-vous lancer ces recherches Perplexity?",
  "header": "Research",
  "multiSelect": false,
  "options": [
    { "label": "Lancer recherche (Recommended)", "description": "Je colle les résultats quand prêt" },
    { "label": "Ignorer recherche", "description": "Continuer sans recherche externe" },
    { "label": "Autres prompts", "description": "Ajuster le focus de recherche" }
  ]
}
```

---

## Preview Implementation Box

Used in: `step-06-preview.md` (section 5)

### Template

```
┌─────────────────────────────────────────────────────────────────────┐
│ 👁️ PREVIEW IMPLÉMENTATION                                           │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│ MÉTRIQUES                                                           │
│ • Complexité estimée: {complexity}                                  │
│ • Nombre de tâches: {tasks_count}                                   │
│ • Risques identifiés: {risks_count}                                 │
│                                                                     │
│ DÉCOUPAGE TÂCHES                                                    │
│ | # | Tâche | Complexité | Dépendances |                            │
│ |---|-------|------------|-------------|                            │
│ | 1 | {title_1} | {complexity_1} | - |                              │
│ | 2 | {title_2} | {complexity_2} | T1 |                             │
│                                                                     │
│ AUDIT SÉCURITÉ                                                      │
│ • Déclenché: {triggered}                                            │
│ • Niveau risque: {risk_level}                                       │
│ • Préoccupations: {concerns}                                        │
│                                                                     │
│ ROUTING RECOMMANDÉ                                                  │
│ → {routing}                                                         │
│ → Raison: {routing_reason}                                          │
│                                                                     │
├─────────────────────────────────────────────────────────────────────┤
│ SUGGESTIONS PROACTIVES                                              │
│ [P1] Complexité {level} → recommande {skill}                        │
│ [P2] {concern} — sera noté dans le brief                            │
│ [P3] Considère {mitigation} pour {risk}                             │
├─────────────────────────────────────────────────────────────────────┤
│ ┌─ Options ──────────────────────────────────────────────────────┐ │
│ │  [A] Générer brief (Recommended) — Créer outputs finaux        │ │
│ │  [B] Ajuster scope — Modifier selon preview                    │ │
│ │  [C] Ajouter notes sécurité — Inclure recommandations          │ │
│ │  [?] Autre réponse...                                          │ │
│ └────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
```

### Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `{complexity}` | Estimated overall complexity | `STANDARD` |
| `{tasks_count}` | Number of tasks in breakdown | `5` |
| `{risks_count}` | Number of identified risks | `2` |
| `{title_1}`, `{title_2}` | Task titles | `Setup auth middleware` |
| `{complexity_1}`, `{complexity_2}` | Task complexities | `SMALL` |
| `{triggered}` | Security audit triggered | `Yes` or `No` |
| `{risk_level}` | Security risk level | `LOW`, `MEDIUM`, `HIGH` |
| `{concerns}` | Security concerns | `Token storage, CSRF` |
| `{routing}` | Recommended skill | `/implement` or `/quick` |
| `{routing_reason}` | Routing justification | `Multiple tasks with dependencies` |
| `{level}` | Complexity level for P1 | `STANDARD` |
| `{skill}` | Recommended skill for P1 | `/implement` |
| `{concern}` | Concern for P2 | `Token expiration handling` |
| `{mitigation}` | Mitigation for P3 | `rate limiting` |
| `{risk}` | Risk for P3 | `brute force attacks` |

### AskUserQuestion Options

```json
{
  "question": "Procéder à la génération du brief?",
  "header": "Preview",
  "multiSelect": false,
  "options": [
    { "label": "Générer brief (Recommended)", "description": "Créer outputs finaux" },
    { "label": "Ajuster scope", "description": "Modifier selon preview" },
    { "label": "Ajouter notes sécurité", "description": "Inclure recommandations sécurité" }
  ]
}
```

---

## Section Validation Box

Used in: `step-07-validate.md` (section 3)

### Template

```
┌─────────────────────────────────────────────────────────────────────┐
│ ✅ VALIDATION: {section_name}                                       │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│ CONTENU                                                             │
│ ┌─────────────────────────────────────────────────────────────────┐ │
│ │ {section_content}                                               │ │
│ └─────────────────────────────────────────────────────────────────┘ │
│                                                                     │
│ Source: {source_decisions}                                          │
│ Confiance: {confidence}                                             │
│                                                                     │
├─────────────────────────────────────────────────────────────────────┤
│ ┌─ Options ──────────────────────────────────────────────────────┐ │
│ │  [A] Approuver (Recommended) — Section correcte                │ │
│ │  [B] Éditer — Faire des modifications                          │ │
│ │  [C] Ignorer le reste — Auto-approuver suivantes               │ │
│ │  [?] Autre réponse...                                          │ │
│ └────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
```

### Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `{section_name}` | Name of the section | `Executive Summary` |
| `{section_content}` | Section content to validate | `Build a secure auth...` |
| `{source_decisions}` | Decisions that informed this section | `Decision #3, #5` |
| `{confidence}` | Confidence level | `HIGH`, `MEDIUM`, `LOW` |

### AskUserQuestion Options

```json
{
  "question": "Cette section {section_name} est-elle correcte?",
  "header": "{section}",
  "multiSelect": false,
  "options": [
    { "label": "Approuver (Recommended)", "description": "Section correcte" },
    { "label": "Éditer", "description": "Faire des modifications" },
    { "label": "Ignorer le reste", "description": "Auto-approuver les sections suivantes" }
  ]
}
```

---

*Breakpoint Formats v1.0 - EPCI Brainstorm v6.0*
