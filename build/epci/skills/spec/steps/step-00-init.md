---
name: step-00-init
description: Initialize spec workflow and parse input
prev_step: null
next_step: steps/step-01-analyze.md
---

# Step 00: Initialization

## MANDATORY EXECUTION RULES (READ FIRST):

- 🔴 NEVER proceed without valid input source
- 🔴 NEVER skip project context loading
- ✅ ALWAYS parse input arguments first
- ✅ ALWAYS load project-memory context
- ✅ ALWAYS validate source exists if path provided
- 💭 FOCUS on understanding input before proceeding

## EXECUTION PROTOCOLS:

### 1. Parse Input Arguments

```
INPUT PARSING:
├── feature-slug (required)
│   └─ Must be kebab-case
├── @path (optional)
│   └─ If starts with @docs/ or @*.md → Brief file
│   └─ If starts with @" → Inline text description
└── No @ argument
    └─ Discovery mode: search for existing brief
```

**Extract:**
- `feature_slug`: Kebab-case identifier
- `source_type`: `brief` | `text` | `discovery`
- `source_path`: File path if applicable
- `source_content`: Raw content if text

### 2. Validate Input

```python
# Validation rules
if source_type == "brief":
    assert file_exists(source_path), "Brief file not found"
    assert source_path.endswith(".md"), "Brief must be Markdown"

if source_type == "text":
    assert len(source_content) > 20, "Description too short"

assert is_kebab_case(feature_slug), "Slug must be kebab-case"
```

### 3. Load Project Context

Invoke `project-memory` to retrieve:

```
project-memory.init()
├── get_patterns() → Coding patterns used
├── get_preferences() → User preferences
├── get_velocity() → Historical velocity data
└── recall_features(similar_to=feature_slug) → Related past features
```

Store context for calibration in later steps.

### 4. Source Resolution

**If source_type == "brief":**
- Read file content
- Validate structure (has sections: Context, Decisions, Action Plan)
- Extract key metadata (EMS score, date, template)

**If source_type == "text":**
- Check clarity score
- If clarity < 0.6, invoke `clarification-engine`
- Present BREAKPOINT for clarification if needed

**If source_type == "discovery":**
- Search for existing brief: `docs/briefs/{feature_slug}/brief-*.md`
- If found: Switch to brief mode
- If not found: Ask user for input via AskUserQuestion

### 5. Initialize State

Create initial state object:

```json
{
  "feature_slug": "{slug}",
  "source_type": "brief|text|discovery",
  "source_path": "{path or null}",
  "source_content": "{parsed content}",
  "project_context": {
    "patterns": [...],
    "preferences": {...},
    "velocity": {...}
  },
  "phase": "init",
  "timestamp": "ISO-8601"
}
```

## CONTEXT BOUNDARIES:

- This step expects: User input (feature-slug, optional @source)
- This step produces: Validated source, project context, initial state

## OUTPUT FORMAT:

```
## Initialization Complete

Feature: {feature-slug}
Source: {source-type} - {path or "inline"}

Project Context:
• Patterns: {count} loaded
• Velocity: {value or "not calibrated"}
• Related features: {list or "none"}

Ready for: Analysis & Decomposition
```

## BREAKPOINT (if clarification needed) - OBLIGATOIRE

AFFICHE cette boîte:

```
┌─────────────────────────────────────────────────────────────────────┐
│ ❓ CLARIFICATION NÉCESSAIRE                                         │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│ La description fournie nécessite des précisions                     │
│                                                                     │
│ Feature: {feature-slug}                                             │
│ Source: {text|discovery}                                            │
│ Questions de clarification:                                         │
│ {clarification questions}                                           │
│                                                                     │
│ Critère de succès: Requirements clairs pour génération spec         │
│                                                                     │
├─────────────────────────────────────────────────────────────────────┤
│ ┌─ Options ──────────────────────────────────────────────────────┐ │
│ │  [A] Répondre aux questions (Recommended)                      │ │
│ │  [B] Fournir fichier brief — Fichier structuré                 │ │
│ │  [C] Annuler — Affiner requirements                            │ │
│ │  [?] Autre réponse...                                          │ │
│ └────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
```

APPELLE:
```
AskUserQuestion({
  questions: [{
    question: "Comment voulez-vous clarifier?",
    header: "Clarify",
    multiSelect: false,
    options: [
      { label: "Répondre aux questions (Recommended)", description: "Fournir clarifications inline" },
      { label: "Fournir fichier brief", description: "Fournir un document brief structuré" },
      { label: "Annuler", description: "Annuler et affiner requirements" }
    ]
  }]
})
```

⏸️ ATTENDS la réponse utilisateur avant de continuer.

## BREAKPOINT (if discovery mode and no brief found) - OBLIGATOIRE

AFFICHE cette boîte:

```
┌─────────────────────────────────────────────────────────────────────┐
│ 📄 SOURCE REQUISE                                                   │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│ Aucun brief existant trouvé pour cette feature                      │
│                                                                     │
│ Feature: {feature-slug}                                             │
│ Recherché: docs/briefs/{slug}/                                      │
│ Besoin: fichier brief, description texte, ou brainstorm d'abord     │
│                                                                     │
│ Critère de succès: Source valide fournie                            │
│                                                                     │
├─────────────────────────────────────────────────────────────────────┤
│ ┌─ Options ──────────────────────────────────────────────────────┐ │
│ │  [A] Fournir chemin brief — Chemin vers fichier existant       │ │
│ │  [B] Description texte — Décrire requirements inline           │ │
│ │  [C] Lancer /brainstorm d'abord (Recommended) — Explorer       │ │
│ │  [D] Annuler — Abandonner le workflow                          │ │
│ │  [?] Autre réponse...                                          │ │
│ └────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
```

APPELLE:
```
AskUserQuestion({
  questions: [{
    question: "Comment voulez-vous fournir la source?",
    header: "Source",
    multiSelect: false,
    options: [
      { label: "Fournir chemin brief", description: "Chemin vers fichier brief existant" },
      { label: "Description texte", description: "Décrire requirements inline" },
      { label: "Lancer /brainstorm d'abord (Recommended)", description: "Explorer l'idée avant de spécifier" },
      { label: "Annuler", description: "Abandonner le workflow" }
    ]
  }]
})
```

⏸️ ATTENDS la réponse utilisateur avant de continuer.

## NEXT STEP TRIGGER:

When source is validated and project context loaded, proceed to `step-01-analyze.md`.
