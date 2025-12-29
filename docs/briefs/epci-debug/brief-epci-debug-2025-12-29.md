# Brief Fonctionnel — `/epci-debug`

> **Slug**: `epci-debug`
> **Date**: 2025-12-29
> **Complexité estimée**: STANDARD
> **EMS Final**: 85/100

---

## Contexte

Création d'une commande de debugging intégrée au workflow EPCI, adaptée de Debuggor v4.11 (anciennement conçu pour Cursor IDE) vers Claude Code. La commande doit exploiter les primitives natives (skills, subagents, MCP, web search) tout en respectant les patterns EPCI existants.

### Source d'inspiration

- **Debuggor v4.11** : Système expert de debugging avec thought tree, scoring des solutions, pipelines hybrides, et rollback automatique.
- **Adaptation requise** : Retirer les spécificités Cursor, intégrer Context7 MCP, aligner sur les conventions EPCI.

---

## Objectif

Permettre aux développeurs de diagnostiquer et corriger des bugs de manière structurée, avec :
- Analyse des causes racines (thought tree)
- Scoring des solutions
- Recherche automatique (web + Context7 MCP)
- Routing adaptatif (Quick vs Complet) basé sur le diagnostic
- Intégration avec les subagents et hooks EPCI existants

---

## Spécifications Fonctionnelles

### Composants à Créer

| Composant | Type | Fichier |
|-----------|------|---------|
| `/epci-debug` | Commande | `build/epci/commands/epci-debug.md` |
| `debugging-strategy` | Skill | `build/epci/skills/core/debugging-strategy/SKILL.md` |
| `thought-tree.md` | Référence | `build/epci/skills/core/debugging-strategy/references/thought-tree.md` |
| `scoring.md` | Référence | `build/epci/skills/core/debugging-strategy/references/scoring.md` |
| `thresholds.md` | Référence | `build/epci/skills/core/debugging-strategy/references/thresholds.md` |

### Pipeline Adaptatif Unique

```
/epci-debug [error message | stack trace | description]
     │
     ▼
PHASE 1: DIAGNOSTIC (toujours)
├── Thought tree (causes avec % confidence)
├── Context7 MCP (documentation libs)
├── Web search (erreurs connues)
└── Output: Cause identifiée + Complexité évaluée
     │
     ▼
ROUTING AUTOMATIQUE
├── Si bug trivial (typo, import, syntax) → Fix direct
├── Si Quick (1 cause, <50 LOC, risque faible) → Mode Quick
└── Si Complet (multi-causes, ≥50 LOC, risque) → Mode Complet
     │
     ├─────────────────┬─────────────────┐
     ▼                 ▼                 ▼
BUG TRIVIAL      MODE QUICK        MODE COMPLET
Fix direct       Phase 2: Fix      Phase 2: Plan + BREAKPOINT
     │                │             Phase 3: Fix
     │                │             Phase 4: Review (@code-reviewer)
     ▼                ▼                 ▼
Inline           Inline            Debug Report
summary          summary           docs/debug/<slug>.md
```

### Critères de Routing Post-Diagnostic

| Critère | Quick | Complet |
|---------|-------|---------|
| Causes probables | 1 | 2+ |
| LOC estimées | < 50 | ≥ 50 |
| Fichiers impactés | 1-2 | 3+ |
| Niveau de risque | Faible | Moyen/Élevé |
| Incertitude résiduelle | < 20% | ≥ 20% |

**Seuil** : ≥ 2 critères "Complet" → Mode Complet

### Format Thought Tree

```
🔍 ROOT CAUSE ANALYSIS
├── 🎯 Primary (72%): [Cause principale]
│   └── Evidence: [Preuves]
├── 🔸 Secondary (18%): [Cause secondaire]
│   └── Evidence: [Preuves]
└── 🔹 Tertiary (10%): [Cause tertiaire]
    └── Evidence: [Preuves]
```

### Scoring des Solutions

Score unique 1-100 avec justification, basé sur :
- Simplicité (30%) : `100 - (lines * 2)`
- Risque (25%) : `100 - (impact * 20)`
- Temps (20%) : `100 - (min / 2)`
- Maintenabilité (25%) : Expert score 1-100

**Format output** :
```
💡 SOLUTIONS PROPOSÉES
┌─────────────────────────────────────────────────┐
│ #1 [Titre solution] — Score: 85/100             │
├─────────────────────────────────────────────────┤
│ Simplicité: 90 | Risque: 80 | Temps: 85 | Maint: 85 │
│ Justification: [Explication]                    │
└─────────────────────────────────────────────────┘
```

### Intégrations

| Intégration | Usage | Condition |
|-------------|-------|-----------|
| **Context7 MCP** | Documentation libs à jour | Systématique en diagnostic, fallback web si absent |
| **Web Search** | Erreurs connues, SO, GitHub issues | Systématique, filtré < 2 ans |
| **@code-reviewer** | Validation fix | Mode Complet uniquement |
| **@security-auditor** | Si bug sécurité | Conditionnel (patterns auth/security) |
| **Skill `debugging-strategy`** | Logique diagnostic | Toujours chargé |
| **Stack skills** | Contexte techno | Auto-détecté |

### Hooks

| Hook | Moment | Usage |
|------|--------|-------|
| `pre-debug` | Avant diagnostic | Charger config, logs externes |
| `post-diagnostic` | Après Phase 1 | Notifier, créer ticket |
| `post-debug` | Après fix | Métriques, apprentissage, stockage pattern |

### Flags

| Flag | Effet |
|------|-------|
| `--full` | Forcer mode Complet (override routing) |
| `--no-report` | Mode Complet sans génération de fichier |
| `--context <path>` | Lier à un Feature Document existant |

### Output

| Mode | Output |
|------|--------|
| Bug trivial | Inline : fix appliqué + explication courte |
| Quick | Inline : diagnostic + fix + validation |
| Complet | Debug Report : `docs/debug/<slug>-<date>.md` |

---

## Contraintes Techniques

### Obligatoires

- [ ] Context7 MCP optionnel avec fallback gracieux (web search only + warning)
- [ ] Streaming du diagnostic (afficher progression en temps réel)
- [ ] Skill `debugging-strategy` < 3000 tokens (logique dans références)
- [ ] Web search filtré : priorité docs officielles, résultats < 2 ans
- [ ] Scoring avec justification explicite visible

### Qualité

- [ ] Détection "bug trivial" : typo, import manquant, syntax error → skip thought tree
- [ ] Intégration mémoire bugs : hook `post-debug` → `.project-memory/patterns/bugs/`
- [ ] Compatible avec workflow `/epci` : suggestion + skill inline disponible

---

## Hors Scope (v1)

- Debugging multi-repo
- Intégration IDE (VS Code, Cursor)
- Replay de sessions de debug
- Analyse de logs en temps réel (tail -f)

---

## Risques Identifiés

| Risque | Probabilité | Impact | Mitigation |
|--------|-------------|--------|------------|
| Context7 MCP absent | Moyenne | Élevé | Fallback web search + warning |
| Diagnostic trop lent | Moyenne | Élevé | Streaming des étapes |
| Mauvais routing | Faible | Élevé | Flag `--full` + confirmation breakpoint |
| Thought tree inutile (bug trivial) | Moyenne | Moyen | Détection bug trivial → skip |
| Web search bruyant | Moyenne | Moyen | Filtrage date + source |

---

## Critères d'Acceptation

1. **Diagnostic fonctionnel** : Thought tree généré avec causes scorées
2. **Routing correct** : Bug simple → Quick, bug complexe → Complet
3. **Context7 intégré** : Recherche doc libs automatique (ou fallback)
4. **Web search utile** : Résultats pertinents filtrés
5. **Fix validé** : @code-reviewer invoqué en mode Complet
6. **Output adapté** : Inline pour Quick, Debug Report pour Complet
7. **Hooks fonctionnels** : pre-debug, post-diagnostic, post-debug

---

## Commande EPCI Suggérée

```
/epci-brief [ce brief]
```

→ Devrait router vers `/epci` (STANDARD, 4-10 fichiers, tests requis)

---

## Annexes

### A. Mapping Debuggor v4.11 → EPCI

| Debuggor | EPCI | Notes |
|----------|------|-------|
| Phase 0: Stack detection | Auto (stack skills) | Natif Claude Code |
| Phase 1: Root cause | Phase 1: Diagnostic | Thought tree |
| Phase 2: Solutions | Phase 1 (suite) | Scoring simplifié |
| Phase 3: Comparative | Fusionné Phase 1 | Pas de phase séparée |
| Phase 4: Correction plan | Phase 2: Plan | Si mode Complet |
| Phase 5: Implementation | Phase 3: Fix | — |
| Phase 6: Quality control | Hooks + @code-reviewer | — |
| Phase 7: User validation | BREAKPOINT | Natif EPCI |
| Phase 8: Final report | Debug Report | Markdown |

### B. Éléments Retirés de Debuggor

- Commandes Cursor (`+light-mode`, `+deep-dive`)
- Format JSON du rapport final
- Diagrammes Mermaid dans le prompt
- Modes spécialisés (symfony-mode, react-mode) → remplacés par stack skills

### C. Éléments Ajoutés pour Claude Code

- Context7 MCP intégration
- Web search automatique
- Routing adaptatif post-diagnostic
- Intégration subagents EPCI
- Système de hooks
- Flag `--full` pour override
