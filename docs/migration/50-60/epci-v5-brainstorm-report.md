# 📋 Rapport de Brainstorming — Refonte Plugin EPCI v5

**Date** : 22 janvier 2026  
**Auteur** : Édouard + Claude  
**Session** : Brainstorming Architectural  
**Durée** : ~45 minutes  
**EMS Final** : 78/100 🌳

---

## 1. Résumé Exécutif

### Contexte

Le plugin EPCI (Explore → Plan → Code → Inspect) v2.7 est devenu une "usine à gaz" avec ~10 787 LOC répartis sur 12 fichiers. La refonte v5 vise à :

- **Simplifier** l'architecture en exploitant les primitives natives Claude Code 2026 (Skills + Subagents)
- **Modulariser** en 4 modules indépendants mais chainables
- **Standardiser** les breakpoints interactifs avec AskUserQuestion
- **Imposer** le TDD sur tout le code généré

### Décisions Clés

| Décision | Choix retenu | Justification |
|----------|--------------|---------------|
| Factory unique vs deux | **Une seule `/factory`** avec flag `--type` | Même structure YAML, évite duplication |
| Chaînage brainstorm→spec | **Deux skills séparés** | Permet entrée à n'importe quelle étape |
| AskUserQuestion dans subagents | **Main thread uniquement** | Limitation technique confirmée |
| Personas | **Non retenu** | Alourdit plus qu'autre chose |

### Livrables Attendus

1. **7 skills** : `/factory`, `/brainstorm`, `/spec`, `/epci`, `/quick`, `/debug`, `/improve`
2. **15 subagents** réutilisables (certains existants, certains à créer)
3. **Shared components** : Breakpoint System, Complexity Calculator, Clarification Engine, TDD Enforcer

---

## 2. Architecture Cible

```
┌─────────────────────────────────────────────────────────────────────┐
│                        PLUGIN EPCI v5.0                             │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐│
│  │   FACTORY   │  │  ARCHITECTE │  │  IMPLEMENT  │  │  EVOLUTION  ││
│  ├─────────────┤  ├─────────────┤  ├─────────────┤  ├─────────────┤│
│  │             │  │             │  │             │  │             ││
│  │ /factory    │  │ /brainstorm │  │ /epci       │  │ /debug      ││
│  │             │  │             │  │ (complexe)  │  │             ││
│  │ Génère:     │  │ /spec       │  │             │  │ /improve    ││
│  │ • Skills    │  │             │  │ /quick      │  │             ││
│  │ • Agents    │  │             │  │ (simple)    │  │             ││
│  │             │  │             │  │             │  │             ││
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘│
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────────┐│
│  │                    SHARED COMPONENTS                            ││
│  ├─────────────────────────────────────────────────────────────────┤│
│  │  • Breakpoint System (ASCII + AskUserQuestion)                  ││
│  │  • Complexity Calculator (TINY/SMALL/STANDARD/LARGE/SPIKE)      ││
│  │  • Clarification Engine (reformulation dictée vocale)           ││
│  │  • Perplexity Research Generator                                ││
│  │  • TDD Enforcer (tests obligatoires)                            ││
│  │  • Validator Pattern (checklist → severity → verdict)           ││
│  └─────────────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────────┘
```

### Flux Global

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│   Idée       │     │     CDC      │     │  PRD +       │
│   brute      │────▶│  fonctionnel │────▶│  Tâches      │
│              │     │  (client)    │     │  (dev)       │
└──────────────┘     └──────────────┘     └──────────────┘
       │                    │                    │
       ▼                    ▼                    ▼
  /brainstorm            /spec              /epci ou /quick
                                                 │
                                                 ▼
                                          Code + Tests
                                                 │
                         ┌───────────────────────┼───────────────────────┐
                         ▼                       ▼                       ▼
                     Bug fix               Amélioration            Nouvelle feature
                         │                       │                       │
                         ▼                       ▼                       ▼
                      /debug                 /improve                 /epci
```

---

## 3. Spécifications par Module

### 3.1 Module FACTORY

#### Skill : `/factory`

**Objectif** : Créer des skills et subagents conformes aux best practices 2026

**Flags** :
| Flag | Valeurs | Défaut | Description |
|------|---------|--------|-------------|
| `--type` | `skill`, `agent` | `skill` | Type de composant à générer |
| `--target` | `web`, `code`, `both` | `code` | Plateforme cible |
| `--migrate` | (flag) | off | Mode migration prompt/GPT existant |

**Workflow (6 phases)** :

| Phase | Nom | Actions | Breakpoint |
|-------|-----|---------|------------|
| 1 | Analyse | Questions sur le besoin, fréquence, persona, triggers | ✅ Fin phase |
| 2 | Architecture | Structure fichiers, complexité, multi-workflow | |
| 3 | Description | Crafting description optimale pour triggering | |
| 4 | Workflow | Design des instructions et règles | |
| 5 | Validation | Preview complet, checklist 12 points | ✅ Approbation |
| 6 | Génération | Création fichiers, rapport conformité | |

**Différences Skill vs Agent** :

| Aspect | Skill | Agent |
|--------|-------|-------|
| Emplacement | `.claude/skills/` | `.claude/agents/` |
| Frontmatter | `name`, `description`, `allowed-tools` | + `model`, `skills` (preload) |
| Invocation | `/slash-command` ou auto | Délégation depuis main agent |
| Contexte | Partagé ou `context: fork` | Toujours isolé |

**Subagents utilisés** : Aucun (main thread pour AskUserQuestion)

---

### 3.2 Module ARCHITECTE

#### Skill : `/brainstorm`

**Objectif** : Transformer une idée brute en CDC fonctionnel compréhensible par le client

**Features clés** :
- EMS (Exploration Maturity Score) sur 5 axes
- 66 techniques de brainstorming (11 catégories)
- Génération prompts Perplexity
- Clarification dictée vocale
- Mode challenge proactif

**Subagents** :
| Agent | Model | Rôle |
|-------|-------|------|
| `@ems-evaluator` | Haiku | Calcul EMS après chaque itération |
| `@technique-advisor` | Haiku | Suggestion techniques selon axes faibles |
| `@expert-panel` | Sonnet | Mode panel 5 thought leaders (optionnel) |
| `@party-orchestrator` | Sonnet | Mode party multi-persona (optionnel) |

**Breakpoints** :
1. **Brief validation** — Avant itérations
2. **Fin itérations** — Quand EMS ≥ 70 ou `finish`

**Output** : CDC fonctionnel en markdown

---

#### Skill : `/spec`

**Objectif** : Convertir un CDC en PRD technique + liste de tâches granulaires

**Workflow** :

```
CDC Input
    │
    ▼
Phase 1: Use Cases Extraction
    │
    ▼
Phase 2: Complexity Calculation
    │
    ▼  ⏸️ BREAKPOINT: PRD Review
    │
Phase 3: Task Decomposition
    │
    ▼  ⏸️ BREAKPOINT: Tasks Review
    │
PRD + Tasks Output
```

**Subagents** :
| Agent | Model | Rôle |
|-------|-------|------|
| `@decompose-validator` | Opus | Validation DAG, détection cycles |
| `@planner` | Sonnet | Décomposition en tâches atomiques |

**Complexity Calculator** :

| Complexité | Score | Caractéristiques | Routing |
|------------|-------|------------------|---------|
| TINY | 0-1 | 1 fichier, <50 LOC | `/quick` |
| SMALL | 2-3 | 2-3 fichiers, <200 LOC | `/quick` |
| STANDARD | 4-6 | 4-10 fichiers, tests requis | `/epci` |
| LARGE | 7-9 | 10+ fichiers, architecture | `/epci` |
| SPIKE | 10+ | Incertitude technique | Exploration |

---

### 3.3 Module IMPLEMENT

#### Skill : `/epci` (STANDARD/LARGE)

**Phases** :

| Phase | Icône | Actions | Subagents | Breakpoint |
|-------|-------|---------|-----------|------------|
| **E**xplore | 🔍 | Analyse codebase, patterns, risques | `@Explore` (natif) | ✅ Fin phase |
| **P**lan | 📋 | Backlog tâches, dépendances | `@planner`, `@plan-validator` | ✅ Fin phase |
| **C**ode | ⚡ | TDD: Red→Green→Refactor | `@implementer` | |
| **I**nspect | 🔎 | Review code, sécurité, QA | `@code-reviewer`, `@security-auditor`, `@qa-reviewer`, `@doc-generator` | ✅ Si révision |

**Subagents** :
| Agent | Model | Phase | Rôle |
|-------|-------|-------|------|
| `@Explore` | Natif | E | Read-only codebase analysis |
| `@planner` | Sonnet | P | Task decomposition |
| `@plan-validator` | Opus | P | Plan validation |
| `@implementer` | Sonnet | C | TDD implementation |
| `@code-reviewer` | Opus | I | Code quality review |
| `@security-auditor` | Opus | I | OWASP + defense-in-depth |
| `@qa-reviewer` | Sonnet | I | Test quality review |
| `@doc-generator` | Sonnet | I | Documentation generation |

**Output** : Feature Document complet dans `docs/features/[slug].md`

---

#### Skill : `/quick` (TINY/SMALL)

**Workflow par complexité** :

| Complexité | Phases | Tests | Breakpoint |
|------------|--------|-------|------------|
| **TINY** | Analyse → Code → Done | Non | Aucun |
| **SMALL** | Analyse → Code → Test → Validation | Unit tests | ✅ Avant code |

**Subagents** :
| Agent | Model | Rôle |
|-------|-------|------|
| `@clarifier` | Haiku | Clarification si ambiguïté |
| `@implementer` | Sonnet | Code direct |

---

### 3.4 Module EVOLUTION

#### Skill : `/debug`

**Objectif** : Corriger un bug avec approche Tree of Thought

**Workflow** :

```
Bug Report
    │
    ▼
Phase 1: Hypothesis Generation (3-4 hypothèses avec confiance %)
    │
    ▼  ⏸️ BREAKPOINT: Sélection hypothèse
    │
Phase 2: Investigation (confirmer/infirmer)
    │
    ▼
Phase 3: Fix + Test de régression
    │
    ▼
Fix Completed
```

**Subagents** :
| Agent | Model | Rôle |
|-------|-------|------|
| `@Explore` | Natif | Analyse du code concerné |
| `@implementer` | Sonnet | Implémentation du fix |
| `@qa-reviewer` | Sonnet | Validation test régression |

---

#### Skill : `/improve`

**Objectif** : Améliorer une feature existante avec impact minimal

**Workflow** :

```
Improvement Request
    │
    ▼
Phase 1: Impact Analysis (fichiers, tests, risques)
    │
    ▼
Phase 2: Minimal Plan
    │
    ▼  ⏸️ BREAKPOINT: Plan validation
    │
Phase 3: Implementation + Validation
    │
    ▼
Improvement Completed
```

**Subagents** :
| Agent | Model | Rôle |
|-------|-------|------|
| `@Explore` | Natif | Impact analysis |
| `@planner` | Sonnet | Plan minimal |
| `@implementer` | Sonnet | Implémentation |
| `@code-reviewer` | Opus | Validation |

---

## 4. Shared Components

### 4.1 Breakpoint System

**Template standard** :
```
┌─────────────────────────────────────────────────────────────────────┐
│ [ICON] BREAKPOINT — [TITLE]                                         │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│ [CONTEXT SECTION]                                                   │
│                                                                     │
│ ┌─ Options ──────────────────────────────────────────────────────┐ │
│ │  1. [Option principale] (Recommended)                          │ │
│ │  2. [Alternative 1]                                            │ │
│ │  3. [Alternative 2]                                            │ │
│ │  4. [Réponse libre] ← OBLIGATOIRE                              │ │
│ └────────────────────────────────────────────────────────────────┘ │
│                                                                     │
│ [FOOTER - timing, document, progress]                               │
└─────────────────────────────────────────────────────────────────────┘
```

**Règles** :
- Option 4 = réponse libre **TOUJOURS PRÉSENT**
- Maximum 4 options (limitation AskUserQuestion)
- "Recommended" marqué si applicable

---

### 4.2 Complexity Calculator

```python
def calculate_complexity(feature: dict) -> str:
    score = 0
    
    # Fichiers impactés (0-3 points)
    files = feature.get('files_count', 0)
    if files <= 1: score += 0
    elif files <= 3: score += 1
    elif files <= 10: score += 2
    else: score += 3
    
    # LOC estimées (0-3 points)
    loc = feature.get('estimated_loc', 0)
    if loc < 50: score += 0
    elif loc < 200: score += 1
    elif loc < 500: score += 2
    else: score += 3
    
    # Nouvelles dépendances (0-2 points)
    score += min(feature.get('new_dependencies', 0), 2)
    
    # Tests requis (0-2 points)
    tests = feature.get('test_strategy', 'none')
    score += {'none': 0, 'unit': 1}.get(tests, 2)
    
    # Risque régression (0-2 points)
    risk = feature.get('regression_risk', 'low')
    score += {'low': 0, 'medium': 1}.get(risk, 2)
    
    # Mapping
    if score <= 1: return "TINY"
    elif score <= 3: return "SMALL"
    elif score <= 6: return "STANDARD"
    elif score <= 9: return "LARGE"
    return "SPIKE"
```

---

### 4.3 Clarification Engine

**Triggers** :
- Phrases incomplètes
- Homophones probables
- Répétitions de mots
- Structure syntaxique incohérente

**Process** :
1. Analyser input pour patterns dictée vocale
2. Si ambiguïté > 0.3 → proposer reformulation
3. Demander confirmation via breakpoint

---

### 4.4 TDD Enforcer

| Complexité | Tests requis | Coverage minimum |
|------------|--------------|------------------|
| TINY | Aucun | N/A |
| SMALL | Unit tests | 60% |
| STANDARD | Unit + Integration | 80% |
| LARGE | Unit + Integration + E2E | 80%+ |

---

### 4.5 Validator Pattern

**Structure commune** :

```markdown
## [Type] Validation Report

### Verdict
**[APPROVED | APPROVED_WITH_WARNINGS | NEEDS_REVISION]**

### Issues

#### 🔴 Critical (Bloquant)
#### 🟠 Important (Devrait corriger)
#### 🟡 Minor (Nice to have)

### Next Steps
```

---

## 5. Subagents Inventory

| Agent | Model | Module | Rôle |
|-------|-------|--------|------|
| `@ems-evaluator` | Haiku | Architecte | Calcul EMS 5 axes |
| `@technique-advisor` | Haiku | Architecte | Suggestion techniques |
| `@expert-panel` | Sonnet | Architecte | Mode panel |
| `@party-orchestrator` | Sonnet | Architecte | Mode party |
| `@clarifier` | Haiku | Shared | Clarification rapide |
| `@planner` | Sonnet | Shared | Décomposition tâches |
| `@plan-validator` | Opus | Implement | Validation plan |
| `@decompose-validator` | Opus | Architecte | Validation DAG |
| `@implementer` | Sonnet | Implement | TDD implementation |
| `@code-reviewer` | Opus | Implement | Code quality review |
| `@security-auditor` | Opus | Implement | Security review |
| `@qa-reviewer` | Sonnet | Implement | Test quality review |
| `@doc-generator` | Sonnet | Implement | Documentation |

**Natifs Claude Code** : `@Explore`, `@Plan`

---

## 6. Structure de Fichiers Cible

```
.claude/
├── CLAUDE.md
├── settings.json
├── skills/
│   ├── factory/
│   │   ├── SKILL.md
│   │   └── references/
│   ├── brainstorm/
│   │   ├── SKILL.md
│   │   └── references/
│   ├── spec/
│   │   ├── SKILL.md
│   │   └── references/
│   ├── epci/
│   │   ├── SKILL.md
│   │   └── references/
│   ├── quick/
│   │   └── SKILL.md
│   ├── debug/
│   │   └── SKILL.md
│   ├── improve/
│   │   └── SKILL.md
│   └── _shared/
│       ├── breakpoint-system.md
│       ├── complexity-calculator.md
│       ├── clarification-engine.md
│       └── tdd-enforcer.md
└── agents/
    ├── ems-evaluator.md
    ├── technique-advisor.md
    ├── planner.md
    ├── implementer.md
    ├── code-reviewer.md
    └── [...]
```

---

## 7. Plan de Développement

| Phase | Semaine | Contenu | Effort |
|-------|---------|---------|--------|
| 1 | S1 | Shared Components + Factory | 8h |
| 2 | S2-3 | Module Architecte (brainstorm + spec) | 12h |
| 3 | S3-4 | Module Implement (epci + quick) | 14h |
| 4 | S4 | Module Evolution (debug + improve) | 7h |
| 5 | S5 | Intégration & Tests | 8h |

**Total estimé** : ~50 heures sur 5 semaines

---

## 8. Risques Identifiés

| Risque | Impact | Mitigation |
|--------|--------|------------|
| AskUserQuestion ne fonctionne pas dans subagents | Confirmé | Main thread pour breakpoints |
| Token overflow sur skills complexes | Medium | Progressive disclosure strict |
| Complexité chaînage brainstorm→spec | Medium | Skills indépendants |
| Migration subagents existants | Low | Conserver structure |

---

## 9. Critères de Succès

| Critère | Cible |
|---------|-------|
| Réduction LOC | -70% (de 10787 à ~3000) |
| Modularité | 100% skills testables unitairement |
| Breakpoints | Tous skills avec breakpoints |
| TDD | ≥80% coverage pour STANDARD/LARGE |

---

## 10. Prochaine Étape

**Développer le Module Factory en premier** pour pouvoir générer les autres skills de manière standardisée.

Chaînage recommandé : `/spec` sur ce CDC pour générer le PRD technique et les tâches de développement.

---

*Document généré par le skill brainstormer v3.1*  
*EMS Final: 78/100 | Itérations: 4 | Durée: 45 min*
