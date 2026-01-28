# Breakpoint Formats

> ASCII box templates for quick skill breakpoints and info displays.

---

## Complexity Alert Breakpoint {#complexity}

Used in step-01-mini-explore when exploration reveals higher complexity than expected.

```
┌─────────────────────────────────────────────────────────────────────┐
│ ALERTE COMPLEXITE                                                   │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│ L'exploration revele une complexite plus elevee qu'estimee          │
│                                                                     │
│ Initial: {TINY|SMALL}                                               │
│ Apres exploration: Semble {STANDARD}                                │
│                                                                     │
│ Raison: {explanation of why complexity seems higher}                │
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

**AskUserQuestion options:**
- "Continuer avec /quick" → "Proceder malgre complexite (peut prendre plus de temps)"
- "Utiliser /implement (Recommended)" → "Escalader vers workflow EPCI complet"
- "Abandonner" → "Annuler et reevaluer requirements"

---

## TDD Failure Breakpoint {#tdd-failure}

Used in step-03-code when tests fail after 2 retry attempts.

```
┌─────────────────────────────────────────────────────────────────────┐
│ ECHEC TDD                                                           │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│ Root Cause: {identified cause or 'Unknown - needs investigation'}   │
│ Confidence: 50%                                                     │
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
│ [P1] Derniere erreur: {error message}                               │
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

**AskUserQuestion options:**
- "Continuer investigation" → "Peut prendre plus de temps mais reste dans /quick"
- "Utiliser /debug (Recommended)" → "Workflow debugging structure"
- "Abandonner" → "Corriger manuellement en dehors du workflow"

---

## Completion Summary {#complete}

Used in step-05-memory as info-only display (no user interaction).

```
┌─────────────────────────────────────────────────────────────────┐
│ [COMPLETE] /quick Execution Finished                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│ Summary: {1-2 sentence summary}                                  │
│                                                                  │
│ ┌─ Stats ───────────────────────────────────────────────────┐   │
│ │  Complexity: {TINY|SMALL}                                 │   │
│ │  Files Modified: {count}                                  │   │
│ │  Tests Added: {count}                                     │   │
│ │  Duration: {time}                                         │   │
│ └───────────────────────────────────────────────────────────┘   │
│                                                                  │
│ Modified Files:                                                  │
│ • {path/to/file1.ts}                                            │
│ • {path/to/file2.test.ts}                                       │
│                                                                  │
│ Memory updated: .claude/state/features/index.json               │
│                                                                  │
├─────────────────────────────────────────────────────────────────┤
│ Next: git commit | /commit | Create PR                          │
└─────────────────────────────────────────────────────────────────┘
```

**Note:** Info-only display, no AskUserQuestion needed.

---

## Escalation Trigger {#escalation}

Used in step-00-detect when complexity exceeds /quick limits (info-only).

```
┌─────────────────────────────────────────────────────────────────┐
│ [ESCALATION] Task Too Complex for /quick                         │
├─────────────────────────────────────────────────────────────────┤
│ Detected Complexity: {STANDARD | LARGE}                          │
│ Estimated: ~{loc} LOC across {files} files                       │
│                                                                  │
│ This task exceeds /quick limits (max SMALL: 200 LOC, 3 files)   │
│                                                                  │
│ Recommended: /implement {feature-slug}                           │
└─────────────────────────────────────────────────────────────────┘
```

**Note:** Info-only display, workflow aborts after this.
