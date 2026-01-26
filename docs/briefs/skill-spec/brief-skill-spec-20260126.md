# Brief PRD v3.0 — Skill /spec

**Feature**: Skill /spec — Transformation CDC vers spécifications techniques
**Date**: 2026-01-26
**Session**: Brainstorm EPCI v6.0
**EMS Final**: 82/100
**Durée session**: ~45 min

---

## 1. Contexte et Objectif Initial

### Origine de la demande

Le workflow EPCI v6.0 définit une chaîne : `/brainstorm` → `/spec` → `/implement`. Le skill `/brainstorm` génère un CDC (Cahier des Charges) fonctionnel. Il manque le maillon `/spec` qui transforme ce CDC en spécifications techniques décomposées, prêtes pour l'exécution par `/implement` ou Ralph (exécution batch autonome).

### Objectif

Créer le skill `/spec` qui :
1. **Parse** le CDC issu de `/brainstorm` (ou une description textuelle)
2. **Décompose** en tâches techniques de 1-2h avec granularité fine (steps 15-30 min)
3. **Génère** les fichiers de spécification (MD + JSON)
4. **Produit** les artifacts Ralph pour exécution batch

### Contraintes identifiées

- Compatibilité avec le format Brief PRD v3.0 de `/brainstorm`
- Intégration avec les core skills existants (complexity-calculator, project-memory, breakpoint-system)
- Support du système Ralph (PROMPT.md, MEMORY.md, ralph.sh)
- Pas de duplication : MD = source, JSON = transformation

---

## 2. Résumé Exécutif

### Insight clé

> **Le skill `/spec` est le pont entre le fonctionnel (CDC) et le technique (tâches exécutables). La source de vérité est Markdown avec YAML frontmatter. Le PRD.json est une sérialisation machine, pas une duplication.**

### Décisions architecturales

| Décision | Choix | Rationale |
|----------|-------|-----------|
| Double granularité | Task (1-2h) + Steps (15-30 min) | Humain = Tasks, Ralph = Steps |
| Source de vérité | task-XXX.md (Markdown) | PRD.json généré depuis MD |
| Structure index.md | Table + Mermaid DAG | Lisibilité + visualisation deps |
| Phases workflow | 3 phases avec breakpoints | Validation progressive |
| Calibration | project-memory si historique | Estimations ajustées |
| Acceptance Criteria | Obligatoires dans MD et JSON | Orientent les tests TDD |

### Livrables

```
docs/specs/{feature-slug}/
├── index.md                    # Orchestrateur (table + Mermaid + contexte)
├── task-001-{slug}.md          # Tâche 1 (1-2h, avec Steps)
├── task-002-{slug}.md          # Tâche 2
├── ...
└── {feature-slug}.prd.json     # Version machine (Ralph-ready)

.ralph/{feature-slug}/
├── PROMPT.md                   # Instructions Claude Code (stack-aware)
├── MEMORY.md                   # Contexte persistant (template)
└── ralph.sh                    # Script runner
```

---

## 3. Analyse et Résultats Clés

### 3.1 Patterns de décomposition (source: Perplexity Research)

| Pattern | Description | Application |
|---------|-------------|-------------|
| Atomic User Stories | WHO/WHAT/WHY + acceptance criteria | Chaque task-XXX.md |
| Goldilocks Zone | Ni trop petit (overhead), ni trop grand (drift) | 1-2h tasks, 15-30min steps |
| DAG Orchestration | Topological sort pour ordre exécution | index.md Mermaid |
| Contract-based | Inputs, outputs, tests, dépendances explicites | YAML frontmatter |

### 3.2 Format optimal

| Format | Usage | Avantage |
|--------|-------|----------|
| Markdown + YAML | task-XXX.md, index.md | Lisible humain + LLM |
| JSON | {feature}.prd.json | Parsable machine, Ralph |
| Mermaid | index.md DAG | Visualisation dépendances |

### 3.3 Calibration estimations

Utilisation de `project-memory` pour :
- Charger la vélocité historique du projet
- Ajuster les estimations basées sur features similaires
- Appliquer les conventions projet (naming, patterns)

---

## 4. Décisions et Orientations

### D1: Double granularité [Confiance: HAUTE]

**Choix**: Task MD (1-2h) avec section Steps (15-30 min)

**Rationale**:
- L'humain raisonne en tâches 1-2h
- Ralph exécute en steps atomiques
- Même fichier, pas de duplication

### D2: Source de vérité unique [Confiance: HAUTE]

**Choix**: task-XXX.md est la source, PRD.json est généré

**Rationale**:
- Évite la désynchro entre formats
- Modification = éditer le MD, régénérer le JSON
- Inspiré de ralph-converter v5.6

### D3: Workflow en 3 phases [Confiance: HAUTE]

**Choix**: Analyse → Génération Specs → Génération Ralph, avec breakpoints

**Rationale**:
- Validation progressive
- Possibilité de modifier avant génération
- Cohérent avec EPCI (breakpoints à chaque transition)

### D4: Acceptance Criteria obligatoires [Confiance: HAUTE]

**Choix**: AC dans task-XXX.md ET dans PRD.json

**Rationale**:
- Orientent les tests TDD dans `/implement`
- Critères de succès mesurables
- Given-When-Then ou checklist

---

## 5. Plan d'Action

### Phase 1: Analyse & Décomposition

| # | Action | Core Skill/Agent | Output |
|---|--------|------------------|--------|
| 1.1 | Parser le CDC (brief brainstorm) | - | Structure parsée |
| 1.2 | Charger contexte projet | `project-memory` | Conventions, vélocité |
| 1.3 | Calculer complexité globale | `complexity-calculator` | TINY/SMALL/STANDARD/LARGE |
| 1.4 | Décomposer en tâches 1-2h | - | Liste tâches + deps |
| 1.5 | Générer steps 15-30 min par tâche | - | Steps par task |
| 1.6 | Calculer DAG (topological sort) | - | Ordre exécution |
| 1.7 | Valider décomposition | `@decompose-validator` | APPROVED/NEEDS_REVISION |

**BREAKPOINT 1**: `decomposition`
- Table des tâches proposées
- DAG Mermaid
- Warnings validator
- Options: [Valider] [Modifier] [Re-décomposer]

### Phase 2: Génération Specs

| # | Action | Output |
|---|--------|--------|
| 2.1 | Créer dossier `docs/specs/{slug}/` | Dossier |
| 2.2 | Générer `index.md` | Orchestrateur |
| 2.3 | Générer `task-XXX.md` pour chaque tâche | Specs individuelles |
| 2.4 | Générer `{feature}.prd.json` | Version machine |

**BREAKPOINT 2**: `plan-review`
- Preview index.md (structure)
- Preview 1-2 task-XXX.md (sample)
- Estimation totale (minutes)
- Options: [Valider] [Éditer] [Régénérer]

### Phase 3: Génération Ralph

| # | Action | Output |
|---|--------|--------|
| 3.1 | Détecter stack projet | Stack info |
| 3.2 | Créer dossier `.ralph/{slug}/` | Dossier |
| 3.3 | Générer `PROMPT.md` (stack-aware) | Instructions Ralph |
| 3.4 | Générer `MEMORY.md` (template) | Contexte persistant |
| 3.5 | Générer `ralph.sh` | Script runner |
| 3.6 | Mettre à jour `.ralph/index.json` | Registre features |

**BREAKPOINT 3**: `validation`
- Résumé fichiers générés
- Routing recommandé: `/implement` ou `/quick`
- Options: [Terminer] [Lancer /implement] [Lancer Ralph]

---

## 6. Risques et Considérations

| Risque | Impact | Probabilité | Mitigation |
|--------|--------|-------------|------------|
| CDC mal structuré | Décomposition incorrecte | Moyen | Clarification-engine + breakpoint validation |
| Estimations incorrectes | Tasks trop longues/courtes | Moyen | Calibration project-memory + feedback loop |
| Dépendances circulaires | DAG invalide | Faible | @decompose-validator obligatoire |
| Stack non détectée | PROMPT.md générique | Faible | Fallback vers prompt générique |

---

## 7. Avenues Non Explorées

- **Décomposition interactive** : L'utilisateur guide la décomposition task par task
- **Import depuis issue tracker** : Parser directement depuis GitHub/Jira
- **Estimation ML** : Modèle entraîné sur l'historique projet
- **Visualisation DAG interactive** : Interface web pour manipuler le graphe

---

## 8. Synthèse Mindmap

```mermaid
graph TB
    subgraph Input
        CDC[CDC / Brief brainstorm]
        TXT[Description textuelle]
    end

    subgraph Phase1[Phase 1: Analyse]
        PARSE[Parser CDC]
        MEMORY[project-memory]
        COMPLEX[complexity-calculator]
        DECOMP[Décomposer tâches]
        DAG[Calculer DAG]
        VALID[@decompose-validator]
    end

    subgraph BP1[Breakpoint 1]
        TABLE[Table tâches]
        MERMAID[Mermaid DAG]
        WARN[Warnings]
    end

    subgraph Phase2[Phase 2: Specs]
        INDEX[index.md]
        TASKS[task-XXX.md]
        PRD[PRD.json]
    end

    subgraph BP2[Breakpoint 2]
        PREVIEW[Preview specs]
        EST[Estimation]
    end

    subgraph Phase3[Phase 3: Ralph]
        STACK[Detect stack]
        PROMPT[PROMPT.md]
        MEMORY_R[MEMORY.md]
        SCRIPT[ralph.sh]
    end

    subgraph BP3[Breakpoint 3]
        RESUME[Résumé]
        ROUTE[Routing]
    end

    CDC --> PARSE
    TXT --> PARSE
    PARSE --> MEMORY
    MEMORY --> COMPLEX
    COMPLEX --> DECOMP
    DECOMP --> DAG
    DAG --> VALID
    VALID --> TABLE
    TABLE --> MERMAID
    MERMAID --> WARN
    WARN --> INDEX
    INDEX --> TASKS
    TASKS --> PRD
    PRD --> PREVIEW
    PREVIEW --> EST
    EST --> STACK
    STACK --> PROMPT
    PROMPT --> MEMORY_R
    MEMORY_R --> SCRIPT
    SCRIPT --> RESUME
    RESUME --> ROUTE
```

---

## 9. Critères de Succès

| Critère | Mesure | Seuil |
|---------|--------|-------|
| Décomposition correcte | Pas de cycles, couverture 100% | @decompose-validator APPROVED |
| Granularité respectée | Tâches 1-2h, Steps 15-30 min | Vérification automatique |
| Fichiers générés | index.md + task-XXX.md + PRD.json | Tous présents |
| Ralph artifacts | PROMPT.md + MEMORY.md + ralph.sh | Tous présents |
| Routing correct | Complexité → workflow approprié | `/quick` ou `/implement` |

---

## 10. Score EMS Final

```
     Clarity:      ██████████  90%
     Depth:        ██████████  85%
     Coverage:     █████████░  80%
     Decisions:    █████████░  75%
     Actionability:█████████░  75%
     ─────────────────────────────────────────────────────────────
     EMS Global:   █████████░  82/100
```

---

## 11. Sources et Références

### Documents internes

- `/home/epci/apps/claude-epci/docs/migration/50-60/epci-v6-brainstorm-report.md`
- `/home/epci/apps/claude-epci/docs/migration/50-60/epci-v6-implementation-plan.md`
- `/home/epci/apps/claude-epci/archive/5.6/skills/core/ralph-converter/SKILL.md`
- `/home/epci/apps/claude-epci/src/agents/decompose-validator.md`
- `/home/epci/apps/claude-epci/src/skills/core/breakpoint-system/SKILL.md`
- `/home/epci/apps/claude-epci/src/skills/core/complexity-calculator/SKILL.md`

### Recherches Perplexity

1. **Décomposition atomique** — Patterns Goldilocks Zone, atomic user stories
2. **PRD pour agents IA** — AGENTS.md, formats structurés, Claude/Cursor/Aider/Devin comparison
3. **Orchestration DAG** — Topological sort, Airflow/Argo patterns
4. **Estimation effort LLM** — Story points ML, calibration historique

---

## 12. Prochaines Étapes

### Routing recommandé

**Complexité calculée**: STANDARD (4-10 fichiers, ~3 jours)

**Workflow**: `/spec` → `/implement`

### Actions immédiates

1. **Créer SKILL.md** — Structure complète du skill /spec
2. **Créer templates/** — Templates index.md, task-XXX.md
3. **Créer references/** — ralph-generation.md, prd-schema.md
4. **Intégrer @decompose-validator** — Adapter pour nouvelle structure
5. **Tester avec CDC réel** — Valider le workflow complet

### Commande suggérée

```bash
/spec @docs/briefs/skill-spec/brief-skill-spec-20260126.md
```

---

*Document généré par brainstorm EPCI v6.0*
*EMS Final: 82/100 | Itérations: 6 | Durée: ~45 min*
