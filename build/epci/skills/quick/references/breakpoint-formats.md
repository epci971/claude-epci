# Breakpoint Formats

> ASCII box templates for quick skill breakpoints and info displays.

## Common Elements

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
│ │  [?] Autre reponse...                                          │ │
│ └────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Complexity Alert Breakpoint {#complexity}

Used in: step-01-mini-explore.md (when exploration reveals higher complexity than expected)

### Template

```
┌─────────────────────────────────────────────────────────────────────┐
│ ALERTE COMPLEXITE                                                   │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│ L'exploration revele une complexite plus elevee qu'estimee          │
│                                                                     │
│ Initial: {initial_complexity}                                       │
│ Apres exploration: Semble {revised_complexity}                      │
│                                                                     │
│ Raison: {complexity_reason}                                         │
│                                                                     │
│ Critere de succes: Utilisateur confirme le workflow approprie       │
│                                                                     │
├─────────────────────────────────────────────────────────────────────┤
│ SUGGESTIONS PROACTIVES                                              │
│ [P1] Les taches STANDARD+ beneficient du workflow EPCI complet      │
├─────────────────────────────────────────────────────────────────────┤
│ ┌─ Options ──────────────────────────────────────────────────────┐ │
│ │  [A] Continuer avec /quick - Malgre complexite plus elevee     │ │
│ │  [B] Utiliser /implement (Recommended) - Workflow EPCI complet │ │
│ │  [C] Abandonner - Reevaluer les requirements                   │ │
│ │  [?] Autre reponse...                                          │ │
│ └────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
```

### Variables

| Variable | Source | Description |
|----------|--------|-------------|
| `{initial_complexity}` | complexity-calculator | Original estimate (TINY/SMALL) |
| `{revised_complexity}` | Exploration analysis | Revised estimate after exploration (STANDARD) |
| `{complexity_reason}` | Exploration | Why complexity seems higher |

### AskUserQuestion

```json
{
  "question": "Comment voulez-vous proceder avec la complexite revisee?",
  "header": "Complexity",
  "multiSelect": false,
  "options": [
    { "label": "Utiliser /implement (Recommended)", "description": "Escalader vers workflow EPCI complet" },
    { "label": "Continuer avec /quick", "description": "Proceder malgre complexite (peut prendre plus de temps)" },
    { "label": "Abandonner", "description": "Annuler et reevaluer requirements" }
  ]
}
```

---

## TDD Failure Breakpoint {#tdd-failure}

Used in: step-03-code.md (when tests fail after 2 retry attempts)

### Template

```
┌─────────────────────────────────────────────────────────────────────┐
│ ECHEC TDD                                                           │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│ Root Cause: {root_cause}                                            │
│ Confidence: {confidence}%                                           │
│                                                                     │
│ Decision Tree:                                                      │
│ RED failed -> GREEN attempt 1 failed -> GREEN attempt 2 failed      │
│                                                                     │
│ Solutions:                                                          │
│ | S1 | Continue Investigation | 5-10 min | Risk: Medium |           │
│ | S2 | Use /debug Workflow    | 15-30 min | Risk: Low   |           │
│ | S3 | Abort and Fix Manually | Variable  | Risk: Low   |           │
│                                                                     │
├─────────────────────────────────────────────────────────────────────┤
│ SUGGESTIONS PROACTIVES                                              │
│ [P1] Derniere erreur: {last_error}                                  │
│ [P2] /debug fournit investigation hypothesis-driven                 │
├─────────────────────────────────────────────────────────────────────┤
│ ┌─ Options ──────────────────────────────────────────────────────┐ │
│ │  [A] Continuer investigation - Reste dans /quick               │ │
│ │  [B] Utiliser /debug (Recommended) - Workflow debug structure  │ │
│ │  [C] Abandonner - Corriger manuellement                        │ │
│ │  [?] Autre reponse...                                          │ │
│ └────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
```

### Variables

| Variable | Source | Description |
|----------|--------|-------------|
| `{root_cause}` | TDD analysis | Identified cause or 'Unknown - needs investigation' |
| `{confidence}` | TDD analysis | Confidence percentage in root cause |
| `{last_error}` | Test runner | Last error message from failed test |

### AskUserQuestion

```json
{
  "question": "Comment gerer l'echec TDD?",
  "header": "TDD Failure",
  "multiSelect": false,
  "options": [
    { "label": "Utiliser /debug (Recommended)", "description": "Workflow debugging structure" },
    { "label": "Continuer investigation", "description": "Peut prendre plus de temps mais reste dans /quick" },
    { "label": "Abandonner", "description": "Corriger manuellement en dehors du workflow" }
  ]
}
```

---

## Completion Summary {#complete}

Used in: step-05-memory.md (info-only display, no user interaction)

### Template

```
┌─────────────────────────────────────────────────────────────────┐
│ [COMPLETE] /quick Execution Finished                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│ Summary: {summary}                                               │
│                                                                  │
│ ┌─ Stats ───────────────────────────────────────────────────┐   │
│ │  Complexity: {complexity}                                 │   │
│ │  Files Modified: {files_count}                            │   │
│ │  Tests Added: {tests_count}                               │   │
│ │  Duration: {duration}                                     │   │
│ └───────────────────────────────────────────────────────────┘   │
│                                                                  │
│ Modified Files:                                                  │
│ • {file_1}                                                       │
│ • {file_2}                                                       │
│                                                                  │
│ Memory updated: .claude/state/features/index.json               │
│                                                                  │
├─────────────────────────────────────────────────────────────────┤
│ Next: git commit | /commit | Create PR                          │
└─────────────────────────────────────────────────────────────────┘
```

### Variables

| Variable | Source | Description |
|----------|--------|-------------|
| `{summary}` | Generation | 1-2 sentence task summary |
| `{complexity}` | complexity-calculator | TINY/SMALL |
| `{files_count}` | Git diff | Number of files modified |
| `{tests_count}` | Test analysis | Number of tests added |
| `{duration}` | State tracking | Time spent on task |
| `{file_1}`, `{file_2}` | Git diff | Modified file paths |

**Note:** Info-only display, no AskUserQuestion needed.

---

## Escalation Trigger {#escalation}

Used in: step-00-detect.md (when complexity exceeds /quick limits, info-only)

### Template

```
┌─────────────────────────────────────────────────────────────────┐
│ [ESCALATION] Task Too Complex for /quick                         │
├─────────────────────────────────────────────────────────────────┤
│ Detected Complexity: {detected_complexity}                       │
│ Estimated: ~{loc} LOC across {files} files                       │
│                                                                  │
│ This task exceeds /quick limits (max SMALL: 200 LOC, 3 files)   │
│                                                                  │
│ Recommended: /implement {feature-slug}                           │
└─────────────────────────────────────────────────────────────────┘
```

### Variables

| Variable | Source | Description |
|----------|--------|-------------|
| `{detected_complexity}` | complexity-calculator | STANDARD or LARGE |
| `{loc}` | complexity-calculator | Estimated lines of code |
| `{files}` | complexity-calculator | Estimated number of files |
| `{feature-slug}` | Input parsing | Kebab-case feature identifier |

**Note:** Info-only display, workflow aborts after this.
