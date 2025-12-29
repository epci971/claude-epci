# Journal d'Exploration — `/epci-debug`

> **Session**: 2025-12-29
> **Durée**: ~4 itérations
> **EMS Final**: 85/100
> **Persona**: 📐 Architecte

---

## Résumé Exécutif

Brainstorming pour créer une commande de debugging intégrée à EPCI, basée sur l'analyse de Debuggor v4.11 (système expert pour Cursor IDE). La session a convergé vers une architecture avec pipeline adaptatif unique, intégration Context7 MCP + web search automatique, et routing intelligent post-diagnostic.

---

## Itération 1 — Analyse Initiale

### Input
- Document source : `docs/debuggor.md` (Debuggor v4.11)
- Contexte : Adaptation Cursor → Claude Code

### Analyse Comparative

**Points forts Debuggor conservés :**
- Thought tree avec % confidence
- Scoring pondéré des solutions
- Pipelines hybrides (Full/Light)
- Quality thresholds
- Automatic rollback
- Modes spécialisés par stack

**Éléments à adapter :**
- Mode Cursor "Thinking + Execution" → flags `think`/`think hard`
- Append-only reports → Feature Document + journal
- Convergence analysis → fusionner avec @plan-validator

**Éléments retirés :**
- Commandes Cursor enrichies
- Format JSON rapport final
- Mermaid dans le prompt

### Questions Posées
1. Type de bugs à cibler ?
2. Niveau d'intégration EPCI ?
3. Système de scoring ?
4. Output formel ?
5. Recherche web ?

### Décisions
| Question | Réponse |
|----------|---------|
| Type bugs | Tous (polyvalent) |
| Intégration | Commande + Skill (A+D) |
| Scoring | Simplifié (B) - Score unique 1-100 |
| Output | Hybride (D) - Inline/Report selon complexité |
| Web | Automatique + Context7 MCP |

**EMS**: 25 → 45 (+20)

---

## Itération 2 — Architecture

### Questions Posées
1. Architecture skill `debugging-strategy` ?
2. Phases du pipeline ?
3. Nouveau subagent @root-cause-analyzer ?
4. Format thought tree ?
5. Intégration Context7 ?

### Décisions
| Question | Réponse |
|----------|---------|
| Architecture skill | Modulaire (B) - SKILL.md + references/ |
| Pipeline | Mapping 8→4 phases (voir brief) |
| Nouveau subagent | Non - logique dans le skill |
| Thought tree | Format CLI-friendly (voir brief) |
| Context7 | Systématique en diagnostic |

### Pipeline Proposé
- Light (TINY) : Diagnostic → Fix → Inline
- Full (SMALL+) : Diagnostic → Plan → Fix → Review → Report

**EMS**: 45 → 70 (+25)

---

## Itération 3 — Simplification

### Insight Clé
> "En debug, on ne connaît pas la complexité avant le diagnostic"

Contrairement aux features où on évalue en amont, le debug révèle la complexité pendant l'exécution.

### Décision Majeure
**Pipeline adaptatif unique** au lieu de 2 pipelines séparés :
- Une seule commande `/epci-debug`
- Routing automatique après Phase 1 (Diagnostic)
- Critères : causes, LOC, fichiers, risque, incertitude

### Questions Finales
1. Nom commande → `/epci-debug` ✓
2. Hooks → pre-debug, post-diagnostic, post-debug ✓
3. Intégration /epci → Suggestion + skill inline ✓

**EMS**: 70 → 85 (+15)

---

## Itération 4 — Premortem

### Risques Critiques Identifiés

| Risque | Mitigation |
|--------|------------|
| **R1**: Context7 MCP absent | Fallback gracieux (web only + warning) |
| **R2**: Diagnostic trop lent | Streaming des étapes en temps réel |
| **R3**: Mauvais routing | Flag `--full` + confirmation breakpoint |

### Risques Importants

| Risque | Mitigation |
|--------|------------|
| **R4**: Thought tree inutile (bug trivial) | Détection typo/import → skip |
| **R5**: Conflit workflow EPCI | Flag `--context <feature-doc>` |
| **R6**: Scoring mal calibré | Justification explicite visible |
| **R7**: Web search bruyant | Filtrage date (<2 ans) + source |

### Risques Mineurs

| Risque | Mitigation |
|--------|------------|
| **R8**: Debug Report jamais relu | Flag `--no-report` |
| **R9**: Skill trop gros | < 3000 tokens, références externalisées |
| **R10**: Pas de mémoire bugs | Hook post-debug → .project-memory |

### Décisions Issues du Premortem
- Context7 optionnel avec fallback
- Flag `--full` pour override routing
- Détection bug trivial → skip thought tree
- Streaming diagnostic obligatoire
- Web search filtré (date, source)
- Scoring toujours justifié

**EMS**: 85 (stable)

---

## Arbre de Décisions

```
Debuggor v4.11 (Cursor)
├── Conserver
│   ├── Thought tree + % confidence
│   ├── Scoring solutions (simplifié)
│   ├── Quality thresholds
│   └── Rollback capability
├── Adapter
│   ├── 8 phases → 4 phases
│   ├── Cursor modes → EPCI flags
│   └── JSON report → Markdown
├── Retirer
│   ├── Commandes Cursor
│   ├── Mermaid inline
│   └── Modes stack hardcodés
└── Ajouter
    ├── Context7 MCP
    ├── Web search auto
    ├── Routing adaptatif
    ├── Intégration subagents EPCI
    └── Système hooks
```

---

## Questions Résolues

| Question | Résolution | Itération |
|----------|------------|-----------|
| Types de bugs | Tous (polyvalent) | 1 |
| Intégration EPCI | Commande + Skill | 1 |
| Scoring | Simplifié 1-100 + justification | 1 |
| Output | Hybride (inline/report) | 1 |
| Web search | Auto + Context7 MCP | 1 |
| Architecture skill | Modulaire avec references/ | 2 |
| Nouveau subagent | Non (logique dans skill) | 2 |
| 1 ou 2 pipelines | 1 adaptatif | 3 |
| Nom commande | /epci-debug | 3 |
| Hooks | 3 (pre, post-diag, post) | 3 |
| Fallback Context7 | Web search + warning | 4 |

---

## Métriques Session

| Métrique | Valeur |
|----------|--------|
| Itérations | 4 |
| Questions posées | 15 |
| Décisions prises | 18 |
| Risques identifiés | 10 |
| Mitigations définies | 10 |
| EMS progression | 25 → 45 → 70 → 85 |
| Phase finale | 🎯 CONVERGENT |

---

## Prochaines Étapes

1. **Créer le skill** `debugging-strategy` avec références
2. **Créer la commande** `/epci-debug`
3. **Implémenter les hooks** (pre-debug, post-diagnostic, post-debug)
4. **Tester** avec différents types de bugs
5. **Documenter** dans CLAUDE.md

---

## Fichiers Générés

| Fichier | Description |
|---------|-------------|
| `docs/briefs/epci-debug/brief-epci-debug-2025-12-29.md` | Brief fonctionnel EPCI-ready |
| `docs/briefs/epci-debug/journal-epci-debug-2025-12-29.md` | Ce journal |
