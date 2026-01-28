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

## Reference Files Used

| Reference | Purpose |
|-----------|---------|
| [breakpoint-formats.md](../references/breakpoint-formats.md#clarification-box) | Clarification ASCII box template |
| [breakpoint-formats.md](../references/breakpoint-formats.md#brief-validation-box) | Brief validation ASCII box template |

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

AFFICHE le format Clarification depuis [references/breakpoint-formats.md](../references/breakpoint-formats.md#clarification-box).

Remplis les variables:
- `{idea_raw}`, `{clarity_score}`
- Questions et suggestions de clarification

APPELLE AskUserQuestion avec les options depuis la référence.

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

AFFICHE le format Brief Validation depuis [references/breakpoint-formats.md](../references/breakpoint-formats.md#brief-validation-box).

Remplis les variables:
- `{reformulated_brief}`, `{diff1}`, `{diff2}`

APPELLE AskUserQuestion avec les options depuis la référence.

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
