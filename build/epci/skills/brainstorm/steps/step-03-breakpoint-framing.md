# Step 03: Breakpoint Framing

> Validate framing before entering iteration loop.

## Trigger

- Previous step: `step-02-framing.md` completed
- Template, HMW, and EMS baseline established

## Inputs

| Input | Source | Required |
|-------|--------|----------|
| `brief_v0` | From step-01 | Yes |
| `template` | From step-02 | Yes |
| `hmw_questions` | From step-02 | No |
| `ems` | From step-02 | Yes |
| `codebase_analysis` | From step-02 | No |
| `--quick` flag | From step-00 | No |

## Protocol

### 1. Prepare Framing Summary

Compile all framing information:

```markdown
## Session Framing

**Topic**: {idea_refined}
**Template**: {template}
**Initial EMS**: {ems.global}/100

### Brief Summary
{brief_v0 condensed}

### Codebase Context
- Stack: {detected stack}
- Related modules: {list}
- Patterns found: {list}

### HMW Questions
1. {hmw_1}
2. {hmw_2}
3. {hmw_3}
```

### 2. Generate Framing Questions (3 max)

Target critical missing information:

| Category | Question Type |
|----------|---------------|
| **Target** | "Who exactly will use this?" |
| **Constraints** | "Any technical limits we should know?" |
| **Timeline** | "Is there a deadline or milestone?" |
| **Dependencies** | "Does this depend on other work?" |
| **Priority** | "What's the most critical aspect?" |

```
IF --quick mode:
  → Limit to 2 questions
  → Focus on Target and Priority only
```

### 3. BREAKPOINT: Framing Validation (OBLIGATOIRE)

AFFICHE cette boîte:

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

APPELLE:
```
AskUserQuestion({
  questions: [{
    question: "Prêt à démarrer les itérations d'exploration?",
    header: "Framing",
    multiSelect: false,
    options: [
      { label: "Démarrer itérations (Recommended)", description: "Commencer exploration structurée" },
      { label: "Ajuster cadrage", description: "Modifier template ou brief" },
      { label: "Ajouter contexte", description: "Fournir plus de background d'abord" }
    ]
  }]
})
```

⏸️ ATTENDS la réponse utilisateur avant de continuer.

### 4. Integrate Responses

```
IF framing questions answered:
  → Update brief with new information
  → Recalculate EMS clarity axis
  → Store decisions made

IF "Adjust framing" selected:
  → Allow template change
  → Allow brief modification
  → Return to this breakpoint

IF "Add context" selected:
  → Open-ended input
  → Process and integrate
  → Return to this breakpoint
```

### 5. Finalize Iteration Setup

```json
{
  "iteration": 1,
  "phase": "DIVERGENT",
  "persona": "architecte",
  "exploration_ready": true,
  "framing_complete": true
}
```

## Outputs

| Output | Destination |
|--------|-------------|
| `framing_complete` | Session state |
| `exploration_ready` | Session state |
| Updated `brief_v0` | Session state |
| Updated `ems` | Session state |

## Next Step

| Condition | Next Step |
|-----------|-----------|
| Framing validated | → `step-04-iteration.md` |
| Adjust framing | → `step-03-breakpoint-framing.md` (loop) |
| Cancel session | → Exit with summary |

## Error Handling

| Error | Resolution |
|-------|------------|
| User wants to restart | → `step-01-clarify.md` |
| Template mismatch | Allow template change |
| Missing critical info | Generate additional questions |
