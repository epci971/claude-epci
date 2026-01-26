# Breakpoint Templates

ASCII box templates for each breakpoint type. Read this file and substitute variables.

## General Structure

```
┌─────────────────────────────────────────────────────────────────────┐
│ {ICON} {title}                                                      │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│ {CONTENT - type specific}                                           │
│                                                                     │
├─────────────────────────────────────────────────────────────────────┤
│ SUGGESTIONS PROACTIVES (only if suggestions[] present)              │
│ {priority_icon} [{priority}] {text} → {action}                      │
├─────────────────────────────────────────────────────────────────────┤
│ ┌─ Options ──────────────────────────────────────────────────────┐ │
│ │  [A] {option1.label} (Recommended) — {option1.description}     │ │
│ │  [B] {option2.label} — {option2.description}                   │ │
│ │  [C] {option3.label} — {option3.description}                   │ │
│ │  [?] Autre reponse...                                          │ │
│ └────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
```

**Priority icons:**
- P1: `[!]` (Critical)
- P2: `[*]` (Important)  
- P3: `[i]` (Nice-to-have)

---

## Template: validation

**Icon:** `[V]`

```
┌─────────────────────────────────────────────────────────────────────┐
│ [V] {title}                                                         │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│ {data.context}                                                      │
│                                                                     │
│ - Objectif: {data.item_to_validate.objectif}                        │
│ - Contexte: {data.item_to_validate.contexte}                        │
│ - Contraintes: {data.item_to_validate.contraintes}                  │
│ - Criteres: {data.item_to_validate.success_criteria}                │
│                                                                     │
│ ┌─ Options ──────────────────────────────────────────────────────┐ │
│ │  [A] {options[0].label} (Recommended) — {options[0].desc}      │ │
│ │  [B] {options[1].label} — {options[1].description}             │ │
│ │  [C] {options[2].label} — {options[2].description}             │ │
│ │  [?] Autre reponse...                                          │ │
│ └────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Template: analysis

**Icon:** `[A]`

```
┌─────────────────────────────────────────────────────────────────────┐
│ [A] {title}                                                         │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│ EXPLORATION                                                         │
│ - Stack: {data.exploration.stack}                                   │
│ - Fichiers impactes: {data.exploration.files_impacted}              │
│ - Patterns: {data.exploration.patterns.join(", ")}                  │
│ - Risques: {data.exploration.risks.join(", ")}                      │
│                                                                     │
│ QUESTIONS DE CLARIFICATION                                          │
│ {for q in data.questions}                                           │
│ {q.tag} {q.text}                                                    │
│    -> Suggestion: {q.suggestion}                                    │
│ {endfor}                                                            │
│                                                                     │
│ SUGGESTIONS IA                                                      │
│ - Architecture: {data.suggestions_ia.architecture}                  │
│ - Implementation: {data.suggestions_ia.implementation}              │
│ - Risques: {data.suggestions_ia.risks}                              │
│                                                                     │
│ EVALUATION                                                          │
│ ┌──────────────┬────────┬───────────┬────────┐                     │
│ │ Categorie    │ Files  │ LOC Est.  │ Risque │                     │
│ ├──────────────┼────────┼───────────┼────────┤                     │
│ │ {evaluation.category} │ {files} │ {loc_estimate} │ {risk} │      │
│ └──────────────┴────────┴───────────┴────────┘                     │
│                                                                     │
│ ┌─ Options ──────────────────────────────────────────────────────┐ │
│ │  [A] {options[0].label} — {options[0].description}             │ │
│ │  [B] {options[1].label} (Recommended) — {options[1].desc}      │ │
│ │  [C] {options[2].label} — {options[2].description}             │ │
│ │  [?] Autre reponse...                                          │ │
│ └────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Template: plan-review

**Icon:** `[P]`

```
┌─────────────────────────────────────────────────────────────────────┐
│ [P] {title}                                                         │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│ METRIQUES                                                           │
│ ┌──────────────────┬─────────────────────────────────────────────┐ │
│ │ Complexite       │ {data.metrics.complexity} ({score})         │ │
│ │ Fichiers         │ {data.metrics.files_impacted}               │ │
│ │ Temps estime     │ {data.metrics.time_estimate}                │ │
│ │ Niveau risque    │ {data.metrics.risk_level}                   │ │
│ │ Detail risque    │ {data.metrics.risk_description}             │ │
│ └──────────────────┴─────────────────────────────────────────────┘ │
│                                                                     │
│ VALIDATIONS                                                         │
│ Plan Validator: {data.validations.plan_validator.verdict}           │
│ - Completeness: {completeness}                                      │
│ - Consistency: {consistency}                                        │
│ - Feasibility: {feasibility}                                        │
│ - Quality: {quality}                                                │
│                                                                     │
│ Skills charges: {data.skills_loaded.join(", ")}                     │
│                                                                     │
│ PREVIEW PROCHAINE PHASE                                             │
│ {for task in data.preview_next.tasks}                               │
│ - {task.title} ({task.time})                                        │
│ {endfor}                                                            │
│ + {data.preview_next.remaining_tasks} taches restantes              │
│                                                                     │
│ Feature Doc: {data.feature_doc_path}                                │
│                                                                     │
│ ┌─ Options ──────────────────────────────────────────────────────┐ │
│ │  [A] Continuer (Recommended) — Passer a la phase suivante      │ │
│ │  [B] Modifier plan — Reviser avant implementation              │ │
│ │  [C] Voir details — Afficher Feature Document complet          │ │
│ │  [?] Autre reponse...                                          │ │
│ └────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Template: phase-transition

**Icon:** `[>]`

```
┌─────────────────────────────────────────────────────────────────────┐
│ [>] {title}                                                         │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│ TRANSITION DE PHASE                                                 │
│                                                                     │
│ Phase terminee: {data.phase_completed}                              │
│ Prochaine phase: {data.phase_next}                                  │
│                                                                     │
│ RESUME                                                              │
│ - Duree: {data.summary.duration}                                    │
│ - Taches completees: {data.summary.tasks_completed}                 │
│ - Fichiers modifies: {data.summary.files_modified.length}           │
│   {for file in data.summary.files_modified}                         │
│   - {file}                                                          │
│   {endfor}                                                          │
│ - Tests: {data.summary.tests_status}                                │
│                                                                     │
│ CHECKPOINT                                                          │
│ ID: {data.checkpoint_created.id}                                    │
│ Resumable: {data.checkpoint_created.resumable ? "Oui" : "Non"}      │
│                                                                     │
│ ┌─ Options ──────────────────────────────────────────────────────┐ │
│ │  [A] Continuer (Recommended) — Passer a {phase_next}           │ │
│ │  [B] Pause — Sauvegarder et reprendre plus tard                │ │
│ │  [C] Annuler — Abandonner le workflow                          │ │
│ │  [?] Autre reponse...                                          │ │
│ └────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Template: decomposition

**Icon:** `[D]`

```
┌─────────────────────────────────────────────────────────────────────┐
│ [D] {title}                                                         │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│ Source: {data.source_file}                                          │
│ Lignes: {data.analysis.lines} | Effort total: {data.analysis.total_effort}j │
│ Structure: {data.analysis.structure}                                │
│                                                                     │
│ SPECIFICATIONS                                                      │
│ ┌──────┬─────────────────────┬────────┬──────┬────────┬──────────┐ │
│ │ ID   │ Titre               │ Effort │ Prio │ Deps   │ Status   │ │
│ ├──────┼─────────────────────┼────────┼──────┼────────┼──────────┤ │
│ {for spec in data.specs}                                            │
│ │ {spec.id} │ {spec.title} │ {spec.effort}j │ {spec.priority} │ {spec.deps} │ {spec.status} │ │
│ {endfor}                                                            │
│ └──────┴─────────────────────┴────────┴──────┴────────┴──────────┘ │
│                                                                     │
│ PARALLELISATION                                                     │
│ Niveau: {data.parallelization}                                      │
│ Duree optimisee: {data.optimized_duration}j (vs {data.sequential_duration}j sequentiel) │
│                                                                     │
│ ALERTES                                                             │
│ {for alert in data.alerts}                                          │
│ [!] {alert}                                                         │
│ {endfor}                                                            │
│                                                                     │
│ Validator: {data.validator_verdict}                                 │
│                                                                     │
│ ┌─ Options ──────────────────────────────────────────────────────┐ │
│ │  [A] Valider (Recommended) — Generer fichiers sous-specs       │ │
│ │  [B] Modifier — Ajuster decoupage avant generation             │ │
│ │  [C] Annuler — Abandonner decomposition                        │ │
│ │  [?] Autre reponse...                                          │ │
│ └────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
```

**Sub-menu if "Modifier" selected:**

```
┌─────────────────────────────────────────────────────────────────────┐
│ [D] MODIFICATION DECOUPAGE                                          │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│ ┌─ Options ──────────────────────────────────────────────────────┐ │
│ │  [A] Fusionner specs — Ex: Fusionner S04 et S05                │ │
│ │  [B] Decouper spec — Ex: Decouper S07 en 2 parties             │ │
│ │  [C] Renommer — Ex: S03 → Modeles Fondamentaux                 │ │
│ │  [D] Changer dependances — Ex: S06 ne depend plus de S03       │ │
│ │  [?] Autre reponse...                                          │ │
│ └────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Template: diagnostic

**Icon:** `[?]`

```
┌─────────────────────────────────────────────────────────────────────┐
│ [?] {title}                                                         │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│ ROOT CAUSE ANALYSIS                                                 │
│                                                                     │
│ Cause identifiee: {data.root_cause}                                 │
│ Confiance: {Math.round(data.confidence * 100)}%                     │
│                                                                     │
│ Arbre de decision:                                                  │
│ {data.decision_tree}                                                │
│                                                                     │
│ SOLUTIONS PROPOSEES                                                 │
│ ┌──────┬─────────────────────────┬────────┬────────┐               │
│ │ ID   │ Solution                │ Effort │ Risque │               │
│ ├──────┼─────────────────────────┼────────┼────────┤               │
│ {for sol in data.solutions}                                         │
│ │ {sol.id} │ {sol.title} │ {sol.effort} │ {sol.risk} │             │
│ {endfor}                                                            │
│ └──────┴─────────────────────────┴────────┴────────┘               │
│                                                                     │
│ ┌─ Options ──────────────────────────────────────────────────────┐ │
│ │  [A] {solutions[0].id}: {solutions[0].title} (Recommended)     │ │
│ │  [B] {solutions[1].id}: {solutions[1].title}                   │ │
│ │  [C] {solutions[2].id}: {solutions[2].title}                   │ │
│ │  [?] Autre reponse...                                          │ │
│ └────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Template: ems-status

**Icon:** `[E]`

**Note:** Display-only, no AskUserQuestion.

```
┌─────────────────────────────────────────────────────────────────────┐
│ [E] {title} — Iteration {data.iteration}                            │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│ Phase: {data.phase}                    EMS Score: {data.ems.score}/100 ({data.ems.delta}) │
│                                                                     │
│ ┌─ EMS Axes ─────────────────────────────────────────────────────┐ │
│ │ Clarity      {renderBar(data.ems.axes.clarity)} {clarity}%     │ │
│ │ Depth        {renderBar(data.ems.axes.depth)} {depth}%         │ │
│ │ Coverage     {renderBar(data.ems.axes.coverage)} {coverage}% {weak?} │ │
│ │ Decisions    {renderBar(data.ems.axes.decisions)} {decisions}% │ │
│ │ Actionable   {renderBar(data.ems.axes.actionability)} {act}%   │ │
│ └────────────────────────────────────────────────────────────────┘ │
│                                                                     │
│ [ok] Done: {data.done.join(", ")}                                   │
│ [ ] Open: {data.open.join(", ")}                                    │
│                                                                     │
│ Commands: {data.commands.join(" | ")}                               │
└─────────────────────────────────────────────────────────────────────┘
```

**Bar rendering function:**
```
renderBar(value):
  filled = Math.round(value / 10)
  empty = 10 - filled
  return "#".repeat(filled) + "-".repeat(empty)
  
Example: 75% -> "########--"
```

---

## Template: info-only

**Icon:** `[i]`

**Note:** Display-only, no AskUserQuestion.

```
┌─────────────────────────────────────────────────────────────────────┐
│ [i] {title}                                                         │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│ {data.summary}                                                      │
│                                                                     │
│ METRIQUES                                                           │
│ {for key, value in data.metrics}                                    │
│ - {key}: {value}                                                    │
│ {endfor}                                                            │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Suggestions Block

Insert before options block when `suggestions[]` is present and non-empty.

```
├─────────────────────────────────────────────────────────────────────┤
│ SUGGESTIONS PROACTIVES                                              │
│ {for sugg in suggestions.sortBy(priority).slice(0,3)}               │
│ {priorityIcon(sugg.priority)} [{sugg.priority}] {sugg.text}         │
│    -> {sugg.action}                                                 │
│ {endfor}                                                            │
```

**Priority icons:**
```
priorityIcon(priority):
  P1 -> "[!]"
  P2 -> "[*]"
  P3 -> "[i]"
```

---

## Options Block

Always present for interactive types. Free response ALWAYS last.

```
│ ┌─ Options ──────────────────────────────────────────────────────┐ │
│ │  [A] {option1.label} {recommended?} — {option1.description}    │ │
│ │  [B] {option2.label} — {option2.description}                   │ │
│ │  [C] {option3.label} — {option3.description}                   │ │
│ │  [?] Autre reponse...                                          │ │
│ └────────────────────────────────────────────────────────────────┘ │
```

**Rules:**
- Max 3 custom options + 1 free response = 4 total
- First option marked `(Recommended)` if it's the default path
- `[?]` always last for free text input
