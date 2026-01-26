---
name: step-00-init
description: Initialize spec workflow and parse input
prev_step: null
next_step: steps/step-01-analyze.md
---

# Step 00: Initialization

## MANDATORY EXECUTION RULES (READ FIRST):

- :red_circle: NEVER proceed without valid input source
- :red_circle: NEVER skip project context loading
- :white_check_mark: ALWAYS parse input arguments first
- :white_check_mark: ALWAYS load project-memory context
- :white_check_mark: ALWAYS validate source exists if path provided
- :thought_balloon: FOCUS on understanding input before proceeding

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

## BREAKPOINT (if clarification needed):

```
┌─────────────────────────────────────────────────────────────────────┐
│ [CLARIFICATION] Input Needs Refinement                               │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│ Feature: {feature-slug}                                              │
│ Source type: {text|discovery}                                        │
│                                                                      │
│ The provided description needs clarification:                        │
│ {clarification questions from clarification-engine}                  │
│                                                                      │
├─────────────────────────────────────────────────────────────────────┤
│ [A] Answer questions  [B] Provide brief file  [C] Cancel             │
└─────────────────────────────────────────────────────────────────────┘
```

## BREAKPOINT (if discovery mode and no brief found):

```
┌─────────────────────────────────────────────────────────────────────┐
│ [INPUT] Source Required                                              │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│ Feature: {feature-slug}                                              │
│ No existing brief found in docs/briefs/{slug}/                       │
│                                                                      │
│ Please provide a source:                                             │
│                                                                      │
├─────────────────────────────────────────────────────────────────────┤
│ [A] Path to brief file                                               │
│ [B] Text description                                                 │
│ [C] Run /brainstorm first                                            │
│ [D] Cancel                                                           │
└─────────────────────────────────────────────────────────────────────┘
```

## NEXT STEP TRIGGER:

When source is validated and project context loaded, proceed to `step-01-analyze.md`.
