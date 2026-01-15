# Audit Report — brainstorm.md

> **Date**: 2026-01-15
> **Auditor**: command-auditor v1.0.0
> **Mode**: STRICT

---

## Executive Summary

| Metric | Value |
|--------|-------|
| Score | **78/100** |
| Rules Checked | 95 |
| Blocking Errors | 1 |
| Errors | 2 |
| Warnings | 6 |
| Suggestions | 2 |
| **Verdict** | **⛔ BLOCKED** |

---

## Detected Workflow

```mermaid
flowchart TD
    A[Start] --> B{Phase 0: Session Detection}
    B --> C{Step 0: Input Clarification}
    C -->|--no-clarify| D[Phase 1: Initialisation]
    C -->|clarity < 0.6| E[Show Reformulation]
    E --> D
    C -->|clarity >= 0.6| D
    D --> F[Load Context]
    F --> G[Explore Background]
    G --> H[Generate HMW]
    H --> I[Questions de cadrage]
    I --> J{Phase 2: Iterations}
    J --> K[Integrate Responses]
    K --> L[@ems-evaluator]
    L --> M{weak_axes?}
    M -->|Yes| N[@technique-advisor]
    N --> O[Display Breakpoint]
    M -->|No| O
    O --> P{EMS >= 70?}
    P -->|Yes| Q[Finalization Checkpoint]
    P -->|No| R[Generate Questions]
    R --> J
    Q -->|Continuer| J
    Q -->|Preview| S[@planner Preview]
    S --> Q
    Q -->|Finaliser| T[Phase 3: Generation]
    T --> U[@planner]
    U --> V{Auth patterns?}
    V -->|Yes| W[@security-auditor]
    V -->|No| X[Create Brief]
    W --> X
    X --> Y[Create Journal]
    Y --> Z[Hook: post-brainstorm]
    Z --> AA[Display Summary]
    AA --> BB[End]
```

---

## Results by Category

### CAT-FM: Frontmatter (15 rules)

| Status | ID | Rule | Detail |
|--------|-----|------|--------|
| ✅ | FM-001 | Frontmatter YAML présent | OK |
| ✅ | FM-002 | Champ `description` obligatoire | OK |
| ✅ | FM-003 | Description ≤ 500 caractères | ~480 chars |
| ❌ | FM-004 | Description commence par verbe | "Brainstorming guide..." → Devrait être "Transformer..." |
| ✅ | FM-005 | Frontmatter < 15 lignes | 13 lignes |
| ✅ | FM-006 | `argument-hint` présent | OK |
| ✅ | FM-007 | Format argument-hint correct | `[optional]`, `--flags` |
| ✅ | FM-008 | `allowed-tools` si outils restreints | Présent |
| ✅ | FM-009 | Outils déclarés valides | Tous valides |
| ❌ | FM-010 | Bash restreint par pattern | **BLOQUANT**: `Bash` sans restriction |
| ✅ | FM-011 | Pas de tabs dans YAML | OK |
| ✅ | FM-012 | Caractères spéciaux échappés | OK |
| ✅ | FM-013 | Pas de champs non reconnus | OK |
| ✅ | FM-014 | `!` requiert Bash | Pas de `!` utilisé |
| ✅ | FM-015 | Budget description | OK |

### CAT-ST: Structure (20 rules)

| Status | ID | Rule | Detail |
|--------|-----|------|--------|
| ✅ | ST-001 | Section `## Overview` | Présente |
| ✅ | ST-002 | Overview 2-4 phrases | 3 phrases |
| ✅ | ST-003 | Section `## Process` | Présente |
| ✅ | ST-004 | Process étapes numérotées | Phase 0/1/2/3, Step 0 |
| ✅ | ST-005 | Section `## Output` | Présente |
| ❌ | ST-006 | Section `## Arguments` | ERREUR: Manquante (argument-hint présent) |
| ⚠️ | ST-007 | Arguments format tableau | WARNING: Pas de tableau arguments |
| ✅ | ST-008 | Section Skills documentée | Dans Configuration |
| ✅ | ST-009 | Section Subagents documentée | Dans Configuration |
| ✅ | ST-010 | Au moins 1 exemple | Multiples exemples |
| ⚠️ | ST-011 | Longueur 50-200 lignes | WARNING: 397 lignes |
| ✅ | ST-012 | Longueur < 500 lignes | OK |
| ✅ | ST-013 | Headers corrects | OK |
| ✅ | ST-014 | Pas de sections vides | OK |
| ✅ | ST-015 | Ordre logique | OK |
| ⚠️ | ST-016 | Section Error Handling | WARNING: Manquante |
| ⚠️ | ST-017 | Section Constraints | WARNING: Manquante |
| ✅ | ST-018 | Breakpoints ASCII box | Format correct |
| ⚠️ | ST-019 | Section See Also | WARNING: Références vers /brief, /epci sans See Also |
| ✅ | ST-020 | Section Flags | Référence vers flags.md |

### CAT-RD: Rédaction (25 rules)

| Status | ID | Rule | Detail |
|--------|-----|------|--------|
| ✅ | RD-001 | < 5000 tokens | ~4000 tokens |
| ✅ | RD-002 | Pas de duplication | OK |
| ✅ | RD-003 | Code blocks avec langage | OK |
| ✅ | RD-004 | Tables données structurées | OK |
| ✅ | RD-005 | Références `@fichier` | OK |
| ✅ | RD-006 | Pas de liens markdown internes | OK |
| ✅ | RD-007 | Subagents format `@name` | OK |
| ✅ | RD-008 | Impératifs instructions | OK |
| ✅ | RD-009 | Conditions explicites IF/WHEN | OK |
| ✅ | RD-010 | Pas de double négation | OK |
| ✅ | RD-011 | Flags format `--flag` | OK |
| ✅ | RD-012 | Pas de chemins hardcodés | OK |
| ✅ | RD-013 | Variables `{var}` format | OK |
| ✅ | RD-014 | Cohérence terminologie | OK (français) |
| ✅ | RD-015 | Pas de TODO/FIXME | OK |
| ✅ | RD-016 | Pas de commentaires perso | OK |
| ✅ | RD-017 | Emojis limités | OK (breakpoints, headers) |
| ✅ | RD-018 | Références `@` existent | OK (vérifiées) |
| ✅ | RD-019 | Contexte `!` < 30 lignes | N/A |
| ✅ | RD-020 | Instructions < 100 lignes | OK |
| ✅ | RD-021 | Frontmatter < 15 lignes | OK |
| ✅ | RD-022 | Spécificité | OK (brainstorming unique) |
| ✅ | RD-023 | Déterminisme | OK |
| ✅ | RD-024 | Testabilité | OK |
| ✅ | RD-025 | Maintenabilité | OK |

### CAT-WF: Workflow (10 rules)

| Status | ID | Rule | Detail |
|--------|-----|------|--------|
| ✅ | WF-001 | Workflow cohérent | Pas d'étapes orphelines |
| ✅ | WF-002 | Séquence logique | Phase 0→1→2→3 |
| ✅ | WF-003 | Pas de boucles infinies | Exit condition: `finish` |
| ✅ | WF-004 | Points de sortie explicites | Phase 3 → Output |
| ✅ | WF-005 | IF/ELSE complets | OK |
| ✅ | WF-006 | Étapes MANDATORY | Checkpoint bloquant |
| ✅ | WF-007 | Breakpoints décision | OK |
| ✅ | WF-008 | Fallbacks documentés | Partiellement |
| ✅ | WF-009 | DAG représentable | OK |
| ✅ | WF-010 | Routing documenté | Integration EPCI |

### CAT-IN: Integration (15 rules)

| Status | ID | Rule | Detail |
|--------|-----|------|--------|
| ✅ | IN-001 | Skills documentés | Configuration table |
| ✅ | IN-002 | Subagents documentés | Agents section |
| ✅ | IN-003 | Hooks documentés | post-brainstorm |
| ✅ | IN-004 | MCP servers documentés | --c7, --seq flags |
| ✅ | IN-005 | Personas documentés | Architecte, Sparring, Pragmatique |
| ✅ | IN-006 | Thinking level | `think hard` |
| ✅ | IN-007 | Routing documenté | Integration EPCI section |
| ✅ | IN-008 | Breakpoints MANDATORY | Finalization Checkpoint |
| ✅ | IN-009 | Output paths | docs/briefs/[slug]/ |
| ⚠️ | IN-010 | Error handling explicite | WARNING: Non détaillé |
| ⚠️ | IN-011 | Fallbacks documentés | WARNING: Partiels |
| ✅ | IN-012 | Context file schema | Session YAML |
| ✅ | IN-013 | Session persistence | ems_history tracking |
| ✅ | IN-014 | Memory hooks | post-brainstorm |
| ℹ️ | IN-015 | validate_command.py | N/A |

### CAT-DG: Detection (10 rules)

| Status | ID | Rule | Detail |
|--------|-----|------|--------|
| 💡 | DG-001 | Besoin skill | Phase 2 logic (~600 tokens) |
| ✅ | DG-002 | Besoin subagent | Déjà délégué |
| ✅ | DG-003 | Besoin référence | Utilise references/ |
| ✅ | DG-004 | Pattern répété | OK |
| ✅ | DG-005 | Template candidat | Déjà externalisé |
| ✅ | DG-006 | Hook candidat | Déjà créé |
| ✅ | DG-007 | Script candidat | N/A |
| 💡 | DG-008 | Décomposition > 300 | 397 lignes - suggéré |
| ✅ | DG-009 | Dense content | Utilise references/ |
| ✅ | DG-010 | Overlap | Pas d'overlap |

---

## Blocking Errors (MUST FIX)

### 1. ❌ FM-010: Bash sans restriction de pattern

**Ligne**: 12 (frontmatter)

**Problème**:
```yaml
allowed-tools: [Read, Write, Bash, Glob, Grep, Task, WebFetch, WebSearch, AskUserQuestion]
```

Le tool `Bash` est déclaré sans restriction de pattern. Cela viole le principe de moindre privilège et permet l'exécution de commandes arbitraires.

**Fix suggéré**:
```yaml
allowed-tools: [Read, Write, Bash(mkdir:*), Bash(python3:src/hooks/*), Glob, Grep, Task, WebFetch, WebSearch, AskUserQuestion]
```

Ou si Bash n'est pas réellement nécessaire, le retirer:
```yaml
allowed-tools: [Read, Write, Glob, Grep, Task, WebFetch, WebSearch, AskUserQuestion]
```

---

## Errors (SHOULD FIX)

### 2. ❌ FM-004: Description ne commence pas par un verbe

**Problème**:
```yaml
description: >-
  Brainstorming guide v5.2 pour decouvrir et specifier une feature.
```

**Fix suggéré**:
```yaml
description: >-
  Transformer une idee vague en brief fonctionnel via brainstorming structure.
  Phases Divergent/Convergent, scoring EMS v2, personas adaptatifs.
  Use when: incertitude technique, idee a clarifier.
```

### 3. ❌ ST-006: Section `## Arguments` manquante

**Problème**: Le frontmatter contient `argument-hint` mais il n'y a pas de section `## Arguments` documentant chaque argument.

**Fix suggéré**: Ajouter après `## Usage`:
```markdown
## Arguments

| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `description` | String | Oui | Description de la feature à explorer |
| `--template` | Enum | Non | Template: `feature`, `problem`, `decision` |
| `--quick` | Flag | Non | Mode rapide (moins d'itérations) |
| `--turbo` | Flag | Non | Mode turbo (@clarifier Haiku) |
| `--random` | Flag | Non | Technique aléatoire |
| `--progressive` | Flag | Non | Mode progressif |
| `--no-hmw` | Flag | Non | Désactive les questions HMW |
| `--no-security` | Flag | Non | Désactive @security-auditor |
| `--no-technique` | Flag | Non | Désactive auto-suggestion techniques |
| `--no-clarify` | Flag | Non | Désactive clarification initiale |
| `--competitive` | Flag | Non | Active analyse concurrentielle |
| `--c7` | Flag | Non | Active Context7 MCP |
| `--seq` | Flag | Non | Active Sequential MCP |
```

---

## Warnings (CONSIDER FIXING)

| ID | Issue | Suggested Action |
|----|-------|------------------|
| ST-011 | 397 lignes (idéal: 50-200) | Extraire plus de contenu vers references/ |
| ST-016 | Pas de Error Handling | Ajouter section avec tableau erreurs/recovery |
| ST-017 | Pas de Constraints | Documenter limites (ex: 7 itérations max, EMS thresholds) |
| ST-019 | Pas de See Also | Ajouter liens vers /brief, /epci, /decompose |
| IN-010 | Error handling implicite | Documenter: @Explore timeout, EMS stagnation |
| IN-011 | Fallbacks partiels | Documenter recovery pour chaque @agent |

---

## Generation Suggestions

| Type | Reason | Suggested Action |
|------|--------|------------------|
| 💡 Skill | Phase 2 logic ~600 tokens | Déjà dans `brainstormer/SKILL.md` - OK |
| 💡 Decompose | 397 lignes | Créer `references/brainstorm/iteration-logic.md` |

---

## Action Items

### Must Fix (Blocking)
- [ ] **FM-010**: Restreindre ou supprimer `Bash` dans allowed-tools

### Should Fix (Errors)
- [ ] **FM-004**: Reformuler description avec verbe initial
- [ ] **ST-006**: Ajouter section `## Arguments` avec tableau

### Consider (Warnings)
- [ ] **ST-016**: Ajouter `## Error Handling` section
- [ ] **ST-017**: Ajouter `## Constraints` section
- [ ] **ST-019**: Ajouter `## See Also` avec commandes liées
- [ ] Réduire longueur en extrayant vers references/

---

## Score Calculation

```
Score = 100 - (BLOQUANT × 10) - (ERREUR × 3) - (WARNING × 1)
Score = 100 - (1 × 10) - (2 × 3) - (6 × 1)
Score = 100 - 10 - 6 - 6
Score = 78/100
```

**Verdict**: ⛔ **BLOCKED** (présence d'erreur bloquante FM-010)

---

## Legend

| Symbol | Meaning |
|--------|---------|
| ❌ | Error (blocking or not) |
| ⚠️ | Warning |
| 💡 | Suggestion |
| ✅ | Compliant |
| ℹ️ | Info (no impact) |

---

*Audit Report generated by command-auditor v1.0.0 — EPCI Plugin*
