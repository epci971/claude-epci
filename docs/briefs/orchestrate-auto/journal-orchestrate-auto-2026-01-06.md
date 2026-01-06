# Journal Brainstorm — Orchestrateur Automatique EPCI

> **Session**: orchestrate-auto
> **Date**: 2026-01-06
> **Durée**: 4 itérations
> **EMS Final**: 75/100

---

## Chronologie

### Iteration 0 — Initialisation

**Phase**: 🔀 Divergent
**Persona**: 📐 Architecte
**EMS**: 35/100 (+35)

**Actions:**
- Exploration codebase via @Explore
- Découverte infrastructure orchestration mature
- Identification patterns réutilisables (DAG, WaveContext, Hooks)

**HMW générés:**
1. Comment orchestrer N features séquentiellement avec libération contexte ?
2. Comment permettre la reprise après erreur sans perdre la progression ?
3. Comment valider automatiquement les checkpoints sans intervention ?

**Questions posées:**
- Q1: Niveau d'autonomie souhaité (Full auto / Semi-auto / Supervisé)
- Q2: Gestion des erreurs (Stop / Skip / Retry)
- Q3: Source des specs (Répertoire / Decompose / Mixte)
- Q4: Parallélisme inter-features
- Q5: Intégration (Nouvelle commande / Extension / Script)

---

### Iteration 1 — Cadrage

**Phase**: 🔀 Divergent
**EMS**: 50/100 (+15)

**Réponses utilisateur:**
- Autonomie: **Full auto** avec auto-correction via tests
- Erreurs: **Hybride B/C** — retry puis skip, jamais bloquer
- Source: **Mixte** mais principalement répertoire
- Parallélisme: **Séquentiel strict**
- Intégration: **Nouvelle commande `/orchestrate`**

**Décisions prises:**
- Journal d'exécution temps réel
- Rapport final complet à la fin
- Auto-correction basée sur tests
- Fichier index.md pour définir l'ordre

**Questions posées:**
- Q1: Format fichier index.md
- Q2: Mécanisme auto-correction
- Q3: Limite retries par feature
- Q4: Format journal
- Q5: Contenu rapport final

---

### Iteration 2 — Exemple concret

**Phase**: 🎯 Convergent
**EMS**: 66/100 (+16)

**Réponses utilisateur:**
- Format index: **YAML/Markdown** (exemple fourni)
- Auto-correction: **Full loop** (tests + lint + review)
- Retries: **3 max** (configurable)
- Journal: **Dual** (MD + JSON)
- Rapport: **Tout inclus**

**Analyse exemple specs fourni:**
```
/docs/briefs/brainstorm-v4/specs/
├── INDEX.md (tableau + Mermaid + Progress)
├── S01-core.md
├── S02-techniques.md
└── S03-modes-finish.md
```

**Découvertes clés:**
- INDEX.md contient déjà tableau de progression
- Format specs très structuré (frontmatter, tasks, acceptance criteria)
- Dépendances explicites (S03 dépend de S01 et S02)
- Effort estimé par spec

---

### Iteration 3 — Convergence finale

**Phase**: 🎯 Convergent
**EMS**: 75/100 (+9)

**Réponses utilisateur:**
- Gestion dépendances: **B** — Optimiser selon DAG (skip intelligemment)
- Mise à jour INDEX.md: **A** — Après chaque spec (temps réel)
- Format journal: **Approuvé**
- Nom commande: **A** — `/orchestrate`

**Architecture finale validée:**
```
PARSE → PLAN → EXECUTE (loop) → REPORT
                  │
                  ├── /brief
                  ├── /epci ou /quick
                  ├── Validation (full loop)
                  ├── Retry (max 3)
                  ├── /commit
                  ├── Update INDEX.md
                  └── Clear contexte
```

---

## Décisions clés

| # | Décision | Justification |
|---|----------|---------------|
| D1 | Full auto sans breakpoints | Use case overnight |
| D2 | Retry-then-skip (max 3) | Robustesse sans blocage |
| D3 | Séquentiel strict | Évite conflits git |
| D4 | Journal dual (MD + JSON) | Lisibilité + tooling |
| D5 | DAG-aware skip | Intelligence sur dépendances |
| D6 | Update INDEX.md temps réel | Visibilité progression |
| D7 | Full loop validation | Tests + lint + review |

---

## Questions résolues

| Question | Réponse |
|----------|---------|
| Peut-on enchaîner les commandes EPCI ? | Oui, via Task tool et skills |
| Skills peuvent s'appeler mutuellement ? | Oui, via invocation Task |
| Gestion contexte entre features ? | Clear équivalent entre specs |
| Format specs existant ? | INDEX.md + Sxx-name.md |
| Hooks disponibles ? | Oui, post-phase-3 réutilisable |

---

## Patterns découverts (codebase)

### Infrastructure existante

| Pattern | Fichier | Réutilisable |
|---------|---------|--------------|
| DAGBuilder | `orchestration/dag_builder.py` | ✅ Directement |
| WaveContext | `orchestration/wave_context.py` | ✅ Pattern applicable |
| HookRunner | `hooks/runner.py` | ✅ Extensible |
| ProgressiveStrategy | `orchestration/strategies/` | ✅ Adaptable |
| ProjectMemory | `project-memory/manager.py` | ✅ Pour persistence |

### Points d'extension identifiés

1. Hook `post-phase-3` → Update mémoire batch
2. WaveOrchestrator → Extensible pour batch
3. DAG → Validation inter-features
4. Project-memory → Queue persistante

---

## Métriques session

| Métrique | Valeur |
|----------|--------|
| Itérations | 4 |
| EMS initial | 35 |
| EMS final | 75 |
| Delta total | +40 |
| Questions posées | 10 |
| Décisions prises | 7 |
| Spikes | 0 |
| Durée estimée | ~20 min |

---

## Prochaines étapes

1. **Lancer `/brief`** avec le contenu du brief généré
2. L'exploration identifiera les fichiers exacts à modifier
3. Workflow EPCI standard (3 phases)
4. La commande `/orchestrate` sera disponible

---

*Generated by /brainstorm — 2026-01-06*
