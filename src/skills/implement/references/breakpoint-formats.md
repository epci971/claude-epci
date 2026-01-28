# Breakpoint Formats

> ASCII box templates for implement skill interactive breakpoints.

---

## Init Breakpoint {#init}

```
┌─────────────────────────────────────────────────────────────────────┐
│ EVALUATION COMPLEXITE                                               │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│ Detection complexite terminee                                       │
│                                                                     │
│ Feature: {feature-slug}                                             │
│ Complexite: {complexity}                                            │
│ Estimation: ~{loc} LOC sur {files} fichiers                         │
│                                                                     │
│ Critere de succes: L'utilisateur confirme le workflow approprie     │
│                                                                     │
├─────────────────────────────────────────────────────────────────────┤
│ ┌─ Options ──────────────────────────────────────────────────────┐ │
│ │  [A] Continuer avec EPCI (Recommended) - Workflow complet      │ │
│ │  [B] Retrograder vers /quick - Plus simple qu'estime           │ │
│ │  [C] Abandonner - Affiner les requirements d'abord             │ │
│ │  [?] Autre reponse...                                          │ │
│ └────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
```

**AskUserQuestion options:**
- "Continuer avec EPCI (Recommended)" → "Workflow complet pour features STANDARD+"
- "Retrograder vers /quick" → "Plus simple qu'estime, utiliser quick workflow"
- "Abandonner" → "Affiner les requirements d'abord"

---

## Explore Breakpoint {#explore}

```
┌─────────────────────────────────────────────────────────────────────┐
│ EXPLORATION TERMINEE [E->P]                                         │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│ RESUME DE PHASE                                                     │
│ - Phase terminee: explore                                           │
│ - Phase suivante: plan                                              │
│ - Duree: {duration}                                                 │
│ - Fichiers modifies: aucun (read-only)                              │
│ - Tests: N/A                                                        │
│                                                                     │
│ CHECKPOINT                                                          │
│ - ID: {feature_id}-checkpoint-explore                               │
│ - Reprise possible: oui                                             │
│                                                                     │
├─────────────────────────────────────────────────────────────────────┤
│ SUGGESTIONS PROACTIVES                                              │
│ [P1] Reviser {N} fichiers a modifier avant planning                 │
│ [P2] Suivre les patterns identifies: {patterns}                     │
├─────────────────────────────────────────────────────────────────────┤
│ ┌─ Options ──────────────────────────────────────────────────────┐ │
│ │  [A] Continuer vers Plan (Recommended) - Planifier impl        │ │
│ │  [B] Etendre exploration - Explorer plus de fichiers           │ │
│ │  [C] Abandonner - Scope trop large                             │ │
│ │  [?] Autre reponse...                                          │ │
│ └────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
```

**AskUserQuestion options:**
- "Continuer vers Plan (Recommended)" → "Proceder a la planification"
- "Etendre exploration" → "Explorer plus de fichiers avant de planifier"
- "Abandonner" → "Scope trop large, annuler implementation"

---

## Plan Validation Breakpoint {#plan}

```
┌─────────────────────────────────────────────────────────────────────┐
│ VALIDATION DU PLAN                                                  │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│ METRIQUES                                                           │
│ - Complexite: {complexity} (score: {score})                         │
│ - Fichiers impactes: {N}                                            │
│ - Temps estime: {hours}h                                            │
│ - Niveau de risque: {LOW|MEDIUM|HIGH}                               │
│ - Description risque: {risk notes}                                  │
│                                                                     │
│ VALIDATIONS                                                         │
│ - @plan-validator: {APPROVED}                                       │
│   - Completude: {phases} phases definies                            │
│   - Coherence: Dependances mappees                                  │
│   - Faisabilite: Dans le scope                                      │
│   - Qualite: Strategie TDD definie                                  │
│                                                                     │
│ PREVIEW TACHES                                                      │
│ | Phase 1: {summary_1} | ~{estimate_1} |                            │
│ | Phase 2: {summary_2} | ~{estimate_2} |                            │
│ | Phase 3: {summary_3} | ~{estimate_3} |                            │
│ Taches restantes: {N}                                               │
│                                                                     │
│ Skills charges: tdd-enforcer, state-manager                         │
│ Doc feature: .epci/features/{feature-slug}/FEATURE.md               │
│                                                                     │
├─────────────────────────────────────────────────────────────────────┤
│ SUGGESTIONS PROACTIVES                                              │
│ [P1] Cycle TDD enforced: RED -> GREEN -> REFACTOR                   │
│ [P2] Cible coverage: {%}%                                           │
├─────────────────────────────────────────────────────────────────────┤
│ ┌─ Options ──────────────────────────────────────────────────────┐ │
│ │  [A] Approuver et Coder (Recommended) - Passer au TDD          │ │
│ │  [B] Modifier le plan - Ajuster phases ou approche             │ │
│ │  [C] Abandonner - Reviser requirements d'abord                 │ │
│ │  [?] Autre reponse...                                          │ │
│ └────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
```

**AskUserQuestion options:**
- "Approuver et Coder (Recommended)" → "Proceder a l'implementation TDD"
- "Modifier le plan" → "Ajuster phases ou approche"
- "Abandonner" → "Reviser requirements d'abord"

---

## Code Review Breakpoint {#review}

```
┌─────────────────────────────────────────────────────────────────────┐
│ CODE REVIEW TERMINE [C->I]                                          │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│ RESUME DE PHASE                                                     │
│ - Phase terminee: code                                              │
│ - Phase suivante: inspect                                           │
│ - Duree: {duration}                                                 │
│ - Taches completees: {N}                                            │
│ - Fichiers modifies: {files}                                        │
│ - Tests: {passing}/{total} passing                                  │
│                                                                     │
│ CHECKPOINT                                                          │
│ - ID: {feature_id}-checkpoint-code                                  │
│ - Reprise possible: oui                                             │
│                                                                     │
├─────────────────────────────────────────────────────────────────────┤
│ SUGGESTIONS PROACTIVES                                              │
│ [P1] Coverage: {%}% atteint                                         │
│ [P2] {N} issues trouves ({severity})                                │
├─────────────────────────────────────────────────────────────────────┤
│ ┌─ Options ──────────────────────────────────────────────────────┐ │
│ │  [A] Accepter et Documenter (Recommended) - Passer a la doc    │ │
│ │  [B] Demander Security Review - Audit securite approfondi      │ │
│ │  [C] Demander QA Validation - Tests QA additionnels            │ │
│ │  [D] Traiter les findings - Corriger avant de continuer        │ │
│ │  [?] Autre reponse...                                          │ │
│ └────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
```

**AskUserQuestion options:**
- "Accepter et Documenter (Recommended)" → "Passer a la phase documentation"
- "Demander Security Review" → "Audit securite approfondi necessaire"
- "Demander QA Validation" → "Tests QA additionnels necessaires"
- "Traiter les findings" → "Corriger les issues avant de continuer"

---

## Security Review Breakpoint {#security}

```
┌─────────────────────────────────────────────────────────────────────┐
│ SECURITY REVIEW TERMINE                                             │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│ Audit securite par @security-auditor termine                        │
│                                                                     │
│ Feature: {feature-slug}                                             │
│ Vulnerabilites totales: {N}                                         │
│ - Critical/High: {N} (a corriger obligatoirement)                   │
│ - Medium/Low: {N} (recommande)                                      │
│                                                                     │
│ Critere de succes: Aucune vulnerabilite CRITICAL/HIGH non resolue   │
│                                                                     │
├─────────────────────────────────────────────────────────────────────┤
│ SUGGESTIONS PROACTIVES                                              │
│ [P1] OWASP Top 10 verifie                                           │
│ [P2] Reviser {N} findings avant de continuer                        │
├─────────────────────────────────────────────────────────────────────┤
│ ┌─ Options ──────────────────────────────────────────────────────┐ │
│ │  [A] Continuer (Recommended) - Posture securite acceptable     │ │
│ │  [B] Corriger issues critiques - Traiter high-severity d'abord │ │
│ │  [C] Accepter le risque - Documenter et continuer              │ │
│ │  [?] Autre reponse...                                          │ │
│ └────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
```

**AskUserQuestion options:**
- "Continuer (Recommended)" → "Posture securite acceptable"
- "Corriger issues critiques" → "Traiter les findings high-severity d'abord"
- "Accepter le risque" → "Documenter la raison et continuer"

---

## QA Review Breakpoint {#qa}

```
┌─────────────────────────────────────────────────────────────────────┐
│ QA REVIEW TERMINE                                                   │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│ Validation QA par @qa-reviewer terminee                             │
│                                                                     │
│ Feature: {feature-slug}                                             │
│ Criteres d'acceptation: {N}/{N} valides                             │
│ Taux de succes tests: {%}%                                          │
│ Defauts trouves: {N}                                                │
│                                                                     │
│ Critere de succes: Tous les AC valides, aucun defaut bloquant       │
│                                                                     │
├─────────────────────────────────────────────────────────────────────┤
│ SUGGESTIONS PROACTIVES                                              │
│ [P1] {N}/{N} criteres d'acceptation valides                         │
│ [P2] Reviser {N} defauts trouves                                    │
├─────────────────────────────────────────────────────────────────────┤
│ ┌─ Options ──────────────────────────────────────────────────────┐ │
│ │  [A] Continuer (Recommended) - Validation QA reussie           │ │
│ │  [B] Corriger defauts d'abord - Traiter les issues trouves     │ │
│ │  [C] Accepter issues connues - Documenter et continuer         │ │
│ │  [?] Autre reponse...                                          │ │
│ └────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
```

**AskUserQuestion options:**
- "Continuer (Recommended)" → "Validation QA reussie"
- "Corriger defauts d'abord" → "Traiter les issues trouves"
- "Accepter issues connues" → "Documenter et continuer"

---

## Finish Summary {#finish}

```
┌─────────────────────────────────────────────────────────────────────┐
│ IMPLEMENTATION COMPLETE                                             │
├─────────────────────────────────────────────────────────────────────┤
│ Feature: {feature-slug}                                             │
│                                                                     │
│ Summary:                                                            │
│ - {N} files created                                                 │
│ - {N} files modified                                                │
│ - {N} tests added ({coverage}% coverage)                            │
│ - Documentation complete                                            │
│                                                                     │
│ EPCI Phases Completed:                                              │
│ [E] Explore                                                         │
│ [P] Plan                                                            │
│ [C] Code                                                            │
│ [I] Inspect                                                         │
│                                                                     │
│ Ready for commit and review.                                        │
└─────────────────────────────────────────────────────────────────────┘
```

**Note:** Info-only display, no AskUserQuestion needed.

---

## Memory Summary {#memory}

```
+------------------------------------------------------------------+
| [M] MEMORY PHASE COMPLETE                                        |
+------------------------------------------------------------------+
| Feature: {feature-slug}                                          |
|                                                                  |
| Summary: {1-2 sentence summary}                                  |
|                                                                  |
| Modified Files: {count}                                          |
| Tests Added: {count}                                             |
|                                                                  |
| index.json updated at:                                           |
| .claude/state/features/index.json                                |
+------------------------------------------------------------------+
```

**Note:** Info-only display, no AskUserQuestion needed.
