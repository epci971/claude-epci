# Journal — Brainstorm EPCI v4.2

> **Date** : 2026-01-06
> **Durée** : ~30 minutes
> **Itérations** : 7

---

## Contexte Initial

**Besoin:** Améliorer le système de brainstorming EPCI en s'inspirant de BMAD v6.

**Documents de référence:**
- `analyse-brainstorm-v4.1-etat-des-lieux.md` — État actuel EPCI
- `analyse-bmad-brainstorming-system.md` — Analyse BMAD v6
- `confrontation-epci-vs-bmad.md` — Comparaison et propositions

**HMW générés:**
1. Comment enrichir la bibliothèque de techniques sans complexifier l'UX ?
2. Comment implémenter la persistence de session sans alourdir project-memory ?
3. Comment intégrer les energy checkpoints de façon naturelle dans le flow EMS ?

---

## Historique des Itérations

### Iteration 1 | 🔀 Divergent | EMS: 30 → 45

**Questions:**
1. Scope de l'évolution v4.2 ?
   - **Réponse: B)** Équilibré — 5-6 features
2. Format bibliothèque techniques ?
   - **Réponse: B)** Dossier références (techniques/ par catégorie)
3. Intégration nouveaux modes ?
   - **Réponse: A)** Flags uniquement (--random, --progressive)

**Feedback utilisateur:**
> "Pas la peine de garder le système d'une seule question par itération. 3-5 questions avec auto-suggestion c'est bien. On garde le format A/B/C."

**Décision clé:** Abandon du One-at-a-Time strict → 3-5 questions par itération

---

### Iteration 2 | 🔀 Divergent | EMS: 45 → 58

**Questions:**
1. Catégories techniques à prioriser ?
   - **Réponse: B)** Mix créatif (Analysis + Ideation + Theatrical/Wild)
2. Trigger sauvegarde session ?
   - **Réponse: B)** Commande `save` explicite
3. Ton energy checkpoints ?
   - **Réponse: C)** Hybride CLI + message humain
4. Granularité commande back ?
   - **Réponse: A)** Back 1 step simple

---

### Iteration 3 | 🔀 Divergent | EMS: 58 → 68

**Questions:**
1. Détection session existante ?
   - **Réponse: A)** Auto-detect au lancement avec prompt
2. Stockage session ?
   - **Réponse: A)** .project-memory/brainstorm-sessions/
3. Logique mode Random ?
   - **Réponse: C)** Pondéré par phase + exclusion utilisées
4. Trigger agents @planner/@security ?
   - **Réponse: C)** Hybride avec confirmation [Y/n]

**Feedback utilisateur:**
> "Lors de la construction, vérifier que tous les agents et skills fonctionnent. Possibilité de paralléliser certains éléments pour gagner en performance et libérer la fenêtre de contexte."

**Décision clé:** Architecture parallélisée pour optimiser le contexte

---

### Iteration 4 | 🔀 Divergent | EMS: 68 → 72

**Questions:**
1. Éléments à paralléliser ?
   - **Réponse: B)** @Explore + pré-calcul techniques en background
2. Nouveaux agents dédiés ?
   - **Réponse: A)** Non, réutiliser existants
3. Optimisation contexte ?
   - **Réponse: C)** Session externalisée, contexte minimal
4. Structure skill brainstormer ?
   - **Réponse: A)** Monolithique enrichi (SKILL.md + references/)

**Energy Check proposé:** Utilisateur choisit [1] Continuer diverger

---

### Iteration 5 | 🔀 Divergent | EMS: 72 → 78

**Questions:**
1. Format technique dans bibliothèque ?
   - **Réponse: B)** Structuré (Nom + Description + Quand + Questions + Exemple)
2. Mode --progressive structure ?
   - **Réponse: C)** 3 phases (Divergent → Transition → Convergent)
3. Format breakpoint v4.2 ?
   - **Réponse: A)** Liste numérotée simple
4. Migration v4.1 → v4.2 ?
   - **Réponse: A)** Breaking change
5. Tests/Documentation ?
   - **Réponse: B)** Tests + exemples sessions

**Utilisateur demande:** converge

---

### Iteration 6 | 🎯 Convergent | EMS: 78 → 85

**Questions de convergence:**
1. Priorisation implémentation ?
   - **Réponse: A)** Core d'abord (session + back + energy)
2. Granularité livraison ?
   - **Réponse: B)** Incrémental (2-3 PRs)
3. Sélection techniques finale ?
   - **Réponse: A)** Top 15 du document confrontation
4. Nom de version ?
   - **Réponse: A)** v4.2

**Utilisateur demande:** finish

---

## Synthèse des Décisions

### Architecture

| Décision | Choix | Justification |
|----------|-------|---------------|
| Format questions | 3-5 par iter | Accélère le flow |
| Structure techniques | references/techniques/*.md | Cohérent avec existant |
| Session storage | .project-memory/ | Single source of truth |
| Gestion contexte | Session externalisée | Performance |
| Nouveaux agents | Non | Réutiliser existants suffit |

### Fonctionnalités

| Feature | Implémentation |
|---------|----------------|
| Session continuation | save explicite + auto-detect |
| Back navigation | 1 step simple |
| Energy checkpoints | Hybride CLI + humain |
| Mode Random | Pondéré + exclusion |
| Mode Progressive | 3 phases avec transition |
| Agents trigger | Confirmation [Y/n] |

### Techniques (~20)

| Catégorie | Techniques |
|-----------|------------|
| Analysis (8) | MoSCoW, 5 Whys, SWOT, Scoring, Pre-mortem, Constraint Mapping, Assumption Reversal, Question Storming |
| Ideation (6) | SCAMPER, Six Thinking Hats, Mind Mapping, What If, Analogical, First Principles |
| Perspective (3) | Role Playing, Time Travel, Reversal Inversion |
| Breakthrough (3) | Inner Child, Chaos Engineering, Nature's Solutions |

### Plan Livraison

1. **PR #1 (Core):** Session, back, energy, format questions, confirmation agents
2. **PR #2 (Techniques):** Bibliothèque 20 techniques, commande technique
3. **PR #3 (Modes):** --random, --progressive, parallélisation, tests

---

## Métriques Session

| Métrique | Valeur |
|----------|--------|
| Itérations totales | 7 |
| Questions posées | 25 |
| Décisions prises | 22 |
| Phase Divergent | Iter 1-5 |
| Phase Convergent | Iter 6-7 |
| EMS initial | 30 |
| EMS final | 85 |
| Delta total | +55 |

---

## Prochaines Étapes

1. [ ] Valider le brief avec l'équipe
2. [ ] Créer branche `feature/brainstorm-v4.2`
3. [ ] Implémenter PR #1 (Core)
4. [ ] Implémenter PR #2 (Techniques)
5. [ ] Implémenter PR #3 (Modes)
6. [ ] Tests et validation
7. [ ] Merge et release v4.2

---

*Journal généré le 2026-01-06 — Brainstorm EPCI v4.2*
