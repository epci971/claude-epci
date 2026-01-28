# Step 01: Clarify

> Clarify user input, reformulate, and validate brief.

## Trigger

- Previous step: `step-00-init.md` completed (default flow)
- `--no-clarify` flag: Skip to step-02

## Inputs

| Input | Source | Required |
|-------|--------|----------|
| `idea_raw` | From step-00 state | Yes |
| `project_context` | From step-00 | No |
| `--turbo` flag | From step-00 | No |

## Reference Files

@../references/breakpoint-formats.md

| Reference | Purpose |
|-----------|---------|
| breakpoint-formats.md | Clarification box (section #clarification-box), Brief validation box (section #brief-validation-box) |

## Protocol

### 1. Assess Input Clarity

Calculate clarity score (0.0 - 1.0):

| Factor | Weight | Indicators |
|--------|--------|------------|
| Specificity | 0.3 | Named entities, concrete nouns |
| Completeness | 0.3 | Who, what, why present |
| Actionability | 0.2 | Verbs, outcomes mentioned |
| Context | 0.2 | Domain references, constraints |

```
IF clarity_score >= 0.8:
  → Skip clarification, proceed to reformulation
ELSE IF clarity_score >= 0.6:
  → Light clarification (1-2 questions)
ELSE:
  → Full clarification (2-3 questions)
```

### 2. Generate Clarification Questions

**Mode Turbo (--turbo flag)**:
Lance un agent clarifier pour générer les questions rapidement.

```
Task({
  subagent_type: "clarifier",
  model: "haiku",
  prompt: "Génère 2-3 questions de clarification pour ce brainstorm.
    Idée: {idea_raw}
    Contexte projet: {project_context}

    Retourne: questions[] avec catégorie, texte, suggestion."
})
```

**Mode Standard**:
Génère les questions selon le score de clarté:

| Score clarté | Questions | Focus |
|--------------|-----------|-------|
| < 0.6 | 3 questions | scope, users, success |
| 0.6 - 0.8 | 2 questions | scope, constraints |
| > 0.8 | 1 question | confirmation |

Question categories:
- **Scope**: "What's the boundary of this feature?"
- **Users**: "Who is the primary user?"
- **Constraints**: "Any technical or business constraints?"
- **Success**: "How will you know it's successful?"

### 3. BREAKPOINT: Clarification (OBLIGATOIRE)

AFFICHE la boîte Clarification (section #clarification-box de breakpoint-formats.md importé ci-dessus):

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

Remplis les variables:
- `{idea_raw}`, `{clarity_score}` depuis session state
- Questions et suggestions de clarification générées

APPELLE AskUserQuestion:
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

⏸️ ATTENDS la réponse utilisateur avant de continuer.

### 4. Integrate Responses

```
FOR each answer:
  - Extract key information
  - Update context with new details
  - Recalculate clarity_score
```

### 5. Generate Reformulation

Synthesize into structured brief:

```markdown
## Brief (v0)

**Subject**: {one-line summary}

**Context**: {why this matters, what problem it solves}

**Scope**: {what's included and excluded}

**Users**: {primary and secondary users}

**Constraints**: {technical, business, timeline}

**Success Criteria**: {how to measure success}
```

### 6. BREAKPOINT: Brief Validation (OBLIGATOIRE)

AFFICHE la boîte Brief Validation (section #brief-validation-box de breakpoint-formats.md importé ci-dessus):

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

Remplis les variables:
- `{reformulated_brief}` - le brief reformulé
- `{diff1}`, `{diff2}` - changements par rapport à l'original

APPELLE AskUserQuestion:
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

⏸️ ATTENDS la réponse utilisateur avant de continuer.

### 7. Handle Rejection Loop

```
IF rejected:
  rejection_count++
  IF rejection_count >= 3:
    BREAKPOINT: "Multiple rejections - let's reformulate the topic entirely"
    → Return to step-01 with fresh input
  ELSE:
    → Iterate on reformulation
```

## Outputs

| Output | Destination |
|--------|-------------|
| `idea_refined` | Session state |
| `clarity_score` | Session state |
| `brief_v0` | Session state |

## Next Step

| Condition | Next Step |
|-----------|-----------|
| Brief validated | → `step-02-framing.md` |
| Rejection loop (3x) | → `step-01-clarify.md` (restart) |
| `--no-clarify` flag | → `step-02-framing.md` |

## Error Handling

| Error | Resolution |
|-------|------------|
| @clarifier unavailable | Use built-in question generation |
| User timeout | Remind and wait |
| All questions skipped | Proceed with low confidence flag |
