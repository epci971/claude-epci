---
name: step-02-framing
description: Auto-detect template, generate HMW questions, Perplexity prompts, and EMS baseline
prev_step: steps/step-01-clarify.md
next_step: steps/step-03-breakpoint-framing.md
---

# Step 02: Framing

> Auto-detect template, generate HMW questions, Perplexity prompts, and EMS baseline.

## Trigger

- Previous step: `step-01-clarify.md` completed
- Brief validated by user

## Inputs

| Input | Source | Required |
|-------|--------|----------|
| `brief_v0` | From step-01 | Yes |
| `idea_refined` | From step-01 | Yes |
| `codebase_analysis` | From @Explore | No |
| `--template` flag | From step-00 | No |
| `--quick` flag | From step-00 | No |
| `--no-hmw` flag | From step-00 | No |

## Reference Files

*(Breakpoint templates are inline in this file)*

## Protocol

### 1. Sync @Explore Results

```
IF @Explore still running:
  → Wait for completion (max 30s)
  → Timeout: continue with partial context

Store codebase_analysis:
  - stack: detected stack (Django, React, etc.)
  - patterns: existing code patterns
  - conventions: naming, structure
  - related_files: potentially impacted areas
  - security_patterns: auth, permissions present
```

### 2. Auto-detect Template

| Template | Trigger Patterns |
|----------|------------------|
| `feature` | "add", "create", "implement", "build" |
| `audit` | "review", "analyze", "check", "audit" |
| `project` | "new project", "from scratch", "bootstrap" |
| `research` | "explore", "investigate", "compare", "evaluate" |
| `decision` | "should we", "which", "choose", "decide" |
| `problem` | "fix", "solve", "issue", "bug", "error" |
| `strategy` | "plan", "roadmap", "architecture", "design" |

```
IF --template provided:
  → Use specified template
ELSE:
  → Analyze brief for trigger patterns
  → Default: feature
```

### 3. Generate HMW Questions (unless --no-hmw)

Generate 3-5 "How Might We" questions based on brief and codebase:

```markdown
## HMW Questions

1. **HMW** {enable users to} {achieve goal} {without constraint}?
2. **HMW** {leverage existing patterns} {to accelerate development}?
3. **HMW** {ensure security} {while maintaining UX}?
4. **HMW** {test this feature} {given the current test infrastructure}?
5. **HMW** {integrate with existing} {system/module}?
```

Contextualize with codebase:
- Reference existing patterns
- Mention related modules
- Consider test infrastructure

### 4. Generate Perplexity Prompts (3-5)

Based on template and brief, generate research prompts:

```markdown
## Perplexity Research Prompts

**1. {Topic}** {Standard | Deep Research}
`{stack} {version} {action} {context} best practices {YYYY-1} {YYYY}`
-> Objective: {why this research helps}

**2. {Topic}** {Standard | Deep Research}
`{query}`
-> Objective: {why}
```

### 5. BREAKPOINT: Perplexity Research (OBLIGATOIRE)

AFFICHE cette boîte:

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

Remplis les variables:
- `{topic_1}`: First research topic (e.g., "Authentication patterns")
- `{mode_1}`: Research mode (`Standard` or `Deep Research`)
- `{query_1}`: Perplexity query (e.g., `Django 5 OAuth2 best practices 2025 2026`)
- `{objective_1}`: Why this research helps
- `{topic_2}`, `{mode_2}`, `{query_2}`, `{objective_2}`: Second research item

APPELLE AskUserQuestion:
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

⏸️ ATTENDS la réponse utilisateur avant de continuer.

### 6. Initialize EMS Baseline

Set initial EMS scores based on current state:

```python
ems = {
  "clarity": 40,      # Brief validated
  "depth": 20,        # Not yet explored
  "coverage": 20,     # Not yet explored
  "decisions": 20,    # No decisions yet
  "actionability": 20 # Not yet concrete
}

# Adjustments
IF codebase_analysis available:
  ems["coverage"] += 10  # Context from codebase

IF perplexity_results injected:
  ems["depth"] += 15     # External research

ems["global"] = calculate_weighted_ems(ems)
```

### 7. Set Initial State

```json
{
  "phase": "DIVERGENT",
  "persona": "architecte",
  "iteration": 0,
  "template": "{detected}",
  "hmw_questions": [...],
  "perplexity_prompts": [...],
  "perplexity_results": null
}
```

## Outputs

| Output | Destination |
|--------|-------------|
| `template` | Session state |
| `hmw_questions` | Session state |
| `perplexity_prompts` | Session state |
| `ems` | Session state |
| `phase` | Session state |
| `persona` | Session state |
| `codebase_analysis` | Session state |

## Next Step

→ `step-03-breakpoint-framing.md`

## Error Handling

| Error | Resolution |
|-------|------------|
| @Explore timeout | Continue with partial analysis |
| Template unclear | Default to "feature" |
| HMW generation fails | Skip, proceed without |
