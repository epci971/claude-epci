# Migration Guide — breakpoint-display

## Overview

Guide pour migrer les 9 commandes EPCI vers le skill `breakpoint-display` unifié.

**Ordre recommandé :**
1. `/brief` (2 breakpoints) — HIGH priority
2. `/epci` (2 breakpoints) — HIGH priority
3. `/decompose` (1 breakpoint) — MEDIUM priority
4. `/commit` (1 breakpoint) — MEDIUM priority
5. `/debug` (1 breakpoint) — MEDIUM priority
6. `/orchestrate` (1 breakpoint) — LOW priority
7. `/save-plan` (1 breakpoint) — LOW priority
8. `/quick` (1 breakpoint) — LOW priority
9. `/ralph-exec` (1 breakpoint) — LOW priority

## Migration Pattern

### Before (Textual Breakpoint)

```markdown
### BREAKPOINT

```
┌─────────────────────────────────────────────────────────────────────┐
│ ⏸️  BREAKPOINT — TITRE                                              │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│ [300 lines of ASCII box with data...]                              │
│                                                                     │
├─────────────────────────────────────────────────────────────────────┤
│ OPTIONS:                                                            │
│   [1] Option 1                                                      │
│   [2] Option 2                                                      │
│   [3] Option 3                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

**Attendre input textuel "1", "2", ou "3"**

~350 tokens
```

### After (Skill Invocation)

```markdown
### BREAKPOINT

Invoquer le skill @breakpoint-display:

@skill:breakpoint-display
  type: {TYPE}
  title: "{TITLE}"
  data: {
    // Type-specific data
  }
  ask: {
    question: "{QUESTION}",
    header: "{HEADER}",
    options: [
      {label: "{LABEL}", description: "{DESCRIPTION}"},
      ...
    ]
  }

~90 tokens (74% réduction)
```

## Command-by-Command Migration

### 1. /brief (2 breakpoints)

#### Breakpoint 1: Step 1 Validation

**Location:** `src/commands/brief.md:121`

**Before:**
```markdown
### Step 1: Reformulation + Validation (BREAKPOINT OBLIGATOIRE)

[300-line ASCII box with original + reformulated brief]

OPTIONS:
  [1] Valider → Continuer vers l'exploration
  [2] Modifier → Je reformule moi-même
  [3] Annuler → Arrêter le workflow
```

**After:**
```markdown
### Step 1: Reformulation + Validation (BREAKPOINT OBLIGATOIRE)

Invoquer @breakpoint-display type `validation`:

@skill:breakpoint-display
  type: validation
  title: "VALIDATION DU BRIEF"
  data: {
    original: "{raw_brief}",
    modified: {true|false},
    detection_info: {
      artefacts_vocaux: {count},
      type_detected: "{type}"
    },
    modified_content: {
      objectif: "...",
      contexte: "...",
      contraintes: "...",
      success_criteria: "..."
    }
  }
  ask: {
    question: "Le brief vous convient-il ?",
    header: "📝 Validation",
    options: [
      {label: "Valider (Recommended)", description: "Continuer vers exploration"},
      {label: "Modifier", description: "Je reformule moi-même"},
      {label: "Annuler", description: "Arrêter workflow"}
    ]
  }
```

**Template:** @templates/validation.md

---

#### Breakpoint 2: Step 4 Analysis

**Location:** `src/commands/brief.md:275`

**Before:**
```markdown
### Step 4: BREAKPOINT — Revue Analyse (OBLIGATOIRE)

[450-line ASCII box with exploration + questions + suggestions + eval]

OPTIONS:
  [1] Répondre aux questions
  [2] Valider les suggestions
  [3] Modifier les suggestions
  [4] Lancer {COMMAND}
```

**After:**
```markdown
### Step 4: BREAKPOINT — Revue Analyse (OBLIGATOIRE)

Invoquer @breakpoint-display type `analysis`:

@skill:breakpoint-display
  type: analysis
  title: "ANALYSE DU BRIEF"
  data: {
    exploration: {
      stack: "{stack}",
      files_impacted: {count},
      patterns: [...],
      risks: [...]
    },
    questions: [
      {tag: "🛑", text: "...", suggestion: "..."},
      ...
    ],
    suggestions: {
      architecture: "...",
      implementation: "...",
      risks: "...",
      stack_specific: "..."
    },
    evaluation: {
      category: "{category}",
      files: {count},
      loc_estimate: {loc},
      risk: "{risk}",
      flags: [...]
    },
    recommended_command: "{command}",
    worktree_tip: {true|false}
  }
  ask: {
    question: "Comment souhaitez-vous procéder avec cette analyse ?",
    header: "🚀 Action",
    options: [
      {label: "Répondre questions", description: "Je fournis réponses clarification"},
      {label: "Valider suggestions (Recommended)", description: "J'accepte suggestions IA"},
      {label: "Modifier suggestions", description: "Je veux changer suggestions"},
      {label: "Lancer /epci", description: "Tout OK, passer implémentation"}
    ]
  }
```

**Template:** @templates/analysis.md

---

### 2. /epci (2 breakpoints)

#### Breakpoint 1: Phase 1 — Plan Validé

**Location:** `src/commands/epci.md:271`

**Before:**
```markdown
### BREAKPOINT BP1 (MANDATORY)

[350-line ASCII box with metrics + validations + preview]

Options:
  • Tapez "Continuer" → Passer à Phase 2
  • Tapez "Modifier le plan" → Réviser le plan
  • Tapez "Voir détails" → Afficher Feature Document complet
  • Tapez "Annuler" → Abandonner le workflow
```

**After:**
```markdown
### BREAKPOINT BP1 (MANDATORY)

Invoquer @breakpoint-display type `plan-review`:

@skill:breakpoint-display
  type: plan-review
  title: "PHASE 1 — Plan Validé"
  data: {
    flags: {
      active: [...],
      sources: {...}
    },
    metrics: {
      complexity: "{category}",
      complexity_score: {score},
      files_impacted: {count},
      time_estimate: "{time}",
      risk_level: "{level}",
      risk_description: "{text}"
    },
    validations: {
      plan_validator: {
        verdict: "{verdict}",
        completeness: "{status}",
        consistency: "{status}",
        feasibility: "{status}",
        quality: "{status}"
      }
    },
    skills_loaded: [...],
    preview_next_phase: {
      phase_name: "Phase 2: Implementation",
      tasks: [
        {title: "...", time: "..."},
        ...
      ],
      remaining_tasks: {count}
    },
    feature_doc_path: "{path}"
  }
  ask: {
    question: "Comment souhaitez-vous procéder ?",
    header: "🚀 Phase 2",
    options: [
      {label: "Continuer (Recommended)", description: "Passer à Phase 2 Implémentation"},
      {label: "Modifier plan", description: "Réviser plan avant implémentation"},
      {label: "Voir détails", description: "Afficher Feature Document complet"},
      {label: "Annuler", description: "Abandonner workflow"}
    ]
  }
```

**Template:** @templates/plan-review.md

---

#### Breakpoint 2: Phase 2 — Code Implémenté

**Location:** `src/commands/epci.md:354`

**Before:**
```markdown
### BREAKPOINT BP2 (MANDATORY)

[350-line ASCII box with implementation metrics + validations + preview P3]

Options:
  • Tapez "Continuer" → Passer à Phase 3
  • Tapez "Revoir code" → Examiner implémentation en détail
  • Tapez "Annuler" → Abandonner le workflow
```

**After:**
```markdown
### BREAKPOINT BP2 (MANDATORY)

Invoquer @breakpoint-display type `plan-review`:

@skill:breakpoint-display
  type: plan-review
  title: "PHASE 2 — Code Implémenté"
  data: {
    metrics: {...},
    implementation_metrics: {
      tasks_completed: {completed},
      tasks_total: {total},
      tests_count: {count},
      tests_status: "{status}",
      coverage: {percent},
      deviations: "{status}"
    },
    validations: {
      code_reviewer: {verdict: "...", summary: "..."},
      security_auditor: {verdict: "..."},
      qa_reviewer: {verdict: "..."}
    },
    preview_next_phase: {
      phase_name: "Phase 3: Finalization",
      tasks: [...],
      remaining_tasks: 0
    },
    feature_doc_path: "{path}"
  }
  ask: {
    question: "Comment souhaitez-vous procéder ?",
    header: "🚀 Phase 3",
    options: [
      {label: "Continuer (Recommended)", description: "Passer à Phase 3 Finalization"},
      {label: "Revoir code", description: "Examiner implémentation en détail"},
      {label: "Annuler", description: "Abandonner workflow"}
    ]
  }
```

**Template:** @templates/plan-review.md

---

### 3. /decompose (1 breakpoint)

**Location:** `src/commands/decompose.md:147`

**Type:** `decomposition`

**Template:** @templates/decomposition.md

**Changes:**
- Replace ASCII table with skill invocation
- Use AskUserQuestion for main choices + sub-menu
- MultiSelect for modification options

---

### 4. /commit (1 breakpoint)

**Location:** `src/commands/commit.md:144`

**Type:** `validation`

**Template:** @templates/validation.md

**Changes:**
- Simple 3-choice validation
- Display git status + proposed message
- Use AskUserQuestion instead of textual input

---

### 5. /debug (1 breakpoint)

**Location:** `src/commands/debug.md:284`

**Type:** `diagnostic`

**Template:** @templates/diagnostic.md

**Changes:**
- Display root cause + ranked solutions
- Use AskUserQuestion for solution selection
- Mark recommended solution with `(Recommended)`

---

### 6. /orchestrate (1 breakpoint)

**Location:** `src/commands/orchestrate.md:98`

**Type:** `interactive-plan`

**Template:** @templates/interactive-plan.md

**Changes:**
- Display DAG + execution plan
- Use AskUserQuestion for complex options (launch/reorder/skip)
- Handle multi-level choices if needed

---

### 7. /save-plan (1 breakpoint)

**Location:** `src/commands/save-plan.md:170`

**Type:** `validation`

**Template:** @templates/validation.md

**Changes:**
- Display source + slug + destination
- Simple 3-choice validation
- Handle "Modifier slug" with follow-up question

---

### 8. /quick (1 breakpoint)

**Location:** `src/commands/quick.md:98`

**Type:** `lightweight`

**Template:** @templates/lightweight.md

**Changes:**
- Minimal display
- Auto-continue after 3s timeout
- AskUserQuestion with timeout

---

### 9. /ralph-exec (1 breakpoint)

**Location:** `src/commands/ralph-exec.md:555`

**Type:** `info-only`

**Template:** @templates/info-only.md

**Changes:**
- Display-only, no interaction
- Show story blocked info
- No AskUserQuestion needed

---

## Validation Checklist

After migrating each command:

- [ ] Breakpoint displays correct type template
- [ ] All data fields populated correctly
- [ ] AskUserQuestion invoked (if applicable)
- [ ] Headers ≤ 12 characters
- [ ] Options have clear labels + descriptions
- [ ] Recommended option marked with `(Recommended)`
- [ ] Response handling updated in command
- [ ] Tokens reduced by ~70%+
- [ ] Command validation passes: `python src/scripts/validate_command.py`
- [ ] Manual test with sample input

## Testing Strategy

1. **Unit test each breakpoint type independently**
   - Validate data structure
   - Check AskUserQuestion integration
   - Verify response handling

2. **Integration test in command context**
   - Run command end-to-end
   - Verify breakpoint displays at correct step
   - Test all user response paths

3. **Token measurement**
   - Compare before/after token counts
   - Verify ~70% reduction achieved

## Rollback Plan

If issues arise during migration:

1. **Keep legacy format commented** in command for quick rollback
2. **Flag `--legacy-breakpoints`** to use old format temporarily
3. **Gradual rollout:** Migrate 1-2 commands at a time, validate in production

## Success Metrics

| Metric | Target |
|--------|--------|
| Token reduction | ≥70% per breakpoint |
| Commands migrated | 9/9 |
| User satisfaction | No complaints about UX regression |
| Validation passing | 100% commands |
| Bugs introduced | 0 critical bugs |

## References

- Breakpoint Display Skill: @src/skills/core/breakpoint-display/SKILL.md
- AskUserQuestion Guide: @references/askuserquestion-guide.md
- Templates: @templates/
- Components: @components/
