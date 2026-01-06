# Brief — Brainstorm EPCI v4.2

> **Date** : 2026-01-06
> **Complexité** : STANDARD
> **EMS Final** : 85/100

---

## 1. Contexte

### Problème
Le système de brainstorming EPCI v4.1 est fonctionnel mais limité comparé aux alternatives modernes (BMAD v6). Les utilisateurs manquent de:
- Variété de techniques créatives (5 frameworks vs 62 chez BMAD)
- Persistence de session pour brainstormings longs
- Flexibilité des modes d'exploration
- Energy checkpoints pour gérer la fatigue cognitive

### Analyse préalable
- **État des lieux EPCI v4.1** : `analyse-brainstorm-v4.1-etat-des-lieux.md`
- **Analyse BMAD v6** : `analyse-bmad-brainstorming-system.md`
- **Confrontation** : `confrontation-epci-vs-bmad.md`

### Objectif
Faire évoluer le brainstormer EPCI vers v4.2 en intégrant les meilleurs patterns BMAD tout en conservant les forces EPCI (EMS, spike, agents auto).

---

## 2. Spécifications Fonctionnelles

### 2.1 Format Questions (CHANGEMENT MAJEUR)

**Avant (v4.1):** 1 question par itération (One-at-a-Time strict)
**Après (v4.2):** 3-5 questions par itération avec suggestions A/B/C

```
1. [Question 1]
   A) Option A  B) Option B  C) Option C
   → Suggestion: B

2. [Question 2]
   A) Option A  B) Option B  C) Option C
   → Suggestion: A

3. [Question 3]
   A) Option A  B) Option B  C) Option C
```

### 2.2 Bibliothèque de Techniques (~20 techniques)

**Structure fichiers:**
```
references/techniques/
├── analysis.md      # 8 techniques
├── ideation.md      # 6 techniques
├── perspective.md   # 3 techniques
└── breakthrough.md  # 3 techniques
```

**Format par technique:**
```markdown
### [Nom Technique]

**Description:** [2-3 lignes]

**Quand utiliser:**
- [Situation 1]
- [Situation 2]

**Questions types:**
1. [Question guidée 1]
2. [Question guidée 2]

**Exemple:**
> [Exemple concret d'application]
```

**Techniques à implémenter (Top 15 + existants):**

| Catégorie | Techniques |
|-----------|------------|
| **Analysis** | MoSCoW*, 5 Whys*, SWOT*, Scoring*, Pre-mortem*, Constraint Mapping, Assumption Reversal, Question Storming |
| **Ideation** | SCAMPER, Six Thinking Hats, Mind Mapping, What If Scenarios, Analogical Thinking, First Principles |
| **Perspective** | Role Playing, Time Travel, Reversal Inversion |
| **Breakthrough** | Inner Child Conference, Chaos Engineering, Nature's Solutions |

*\* = existants dans v4.1*

### 2.3 Session Continuation

**Stockage:** `.project-memory/brainstorm-sessions/[slug].yaml`

**Format session:**
```yaml
session:
  id: "feature-auth-2026-01-06"
  slug: "feature-auth"
  status: "in_progress"  # in_progress | completed | abandoned
  phase: "divergent"     # divergent | transition | convergent
  ems: 45
  persona: "architecte"
  iteration: 3
  techniques_used: ["moscow", "5whys"]
  ideas:
    - id: 1
      content: "OAuth2 avec refresh tokens"
      score: 8
    - id: 2
      content: "Session JWT stateless"
      score: 7
  history:
    - iteration: 1
      questions: [...]
      responses: [...]
      ems_delta: +15
  last_question: "Quel mécanisme de révocation privilégier?"
  created: "2026-01-06T10:30:00"
  updated: "2026-01-06T11:15:00"
```

**Commandes:**
- `save` — Sauvegarde explicite de la session
- `continue-session` — Reprendre une session (ou auto-detect au lancement)

**Auto-detection au lancement:**
```
-------------------------------------------------------
📂 Session existante détectée: "feature-auth" (EMS: 45)
   Dernière activité: il y a 2 heures

[1] Reprendre cette session
[2] Nouvelle session
-------------------------------------------------------
```

### 2.4 Navigation

**Nouvelle commande `back`:**
- Revient à l'itération précédente
- Restaure l'état (EMS, questions, phase)
- Simple: 1 step back uniquement

**Commandes v4.2 complètes:**
```
continue          # Itération suivante
dive [topic]      # Approfondir un aspect
pivot             # Réorienter
status            # EMS détaillé
modes             # Afficher/changer persona
mode [nom]        # Forcer persona
premortem         # Exercice anticipation risques
diverge           # Forcer phase Divergent
converge          # Forcer phase Convergent
scoring           # Évaluer et prioriser idées
framework [x]     # Appliquer un framework
technique [x]     # Appliquer une technique (NOUVEAU)
spike [dur] [q]   # Exploration technique
save              # Sauvegarder session (NOUVEAU)
back              # Itération précédente (NOUVEAU)
energy            # Forcer energy check (NOUVEAU)
finish            # Générer brief + journal
```

### 2.5 Energy Checkpoints

**Triggers:**
1. EMS atteint 50 (mi-parcours)
2. EMS atteint 75 (près de la fin)
3. Itération >= 7 sans commande utilisateur
4. Changement de phase Divergent → Convergent

**Format (hybride CLI + humain):**
```
-------------------------------------------------------
⚡ ENERGY CHECK | EMS: 52/100 | Phase: 🔀 Divergent
-------------------------------------------------------
On a bien avancé sur l'exploration. Comment tu te sens?

[1] Continuer — Je suis dans le flow
[2] Pause — Sauvegarder et reprendre plus tard
[3] Accélérer — Passons à la convergence
[4] Pivoter — Je veux changer d'angle
-------------------------------------------------------
```

### 2.6 Modes de Sélection (Flags)

**--random**
- Sélection aléatoire de techniques
- Pondéré par phase (Divergent → Ideation, Convergent → Analysis)
- Exclut les techniques déjà utilisées dans la session

**--progressive**
- 3 phases structurées: Divergent → Transition → Convergent
- Transition = Energy check obligatoire + résumé mi-parcours
- Mapping automatique des techniques par phase

### 2.7 Agents (Comportement modifié)

**@planner / @security-auditor:**
- Trigger auto conservé (EMS ≥70, patterns auth/payment)
- NOUVEAU: Confirmation avant lancement
```
-------------------------------------------------------
🎯 EMS atteint 72 — Prêt pour un plan préliminaire?
   Lancer @planner? [Y/n]
-------------------------------------------------------
```

**Parallélisation:**
- @Explore en background pendant les questions utilisateur
- Pré-calcul des techniques suggérées en parallèle

### 2.8 Gestion Contexte

**Session externalisée:**
- État complet dans `.project-memory/brainstorm-sessions/`
- Contexte conversation = minimum (question courante + résumé)
- Lazy loading des techniques (charge uniquement l'active)

---

## 3. Architecture Technique

### 3.1 Structure Fichiers

```
src/skills/core/brainstormer/
├── SKILL.md                      # Flow principal (mis à jour)
└── references/
    ├── ems-system.md             # Existant (inchangé)
    ├── personas.md               # Existant (inchangé)
    ├── frameworks.md             # Existant (5 frameworks)
    ├── brief-format.md           # Existant (inchangé)
    ├── session-format.md         # NOUVEAU - Format YAML session
    └── techniques/               # NOUVEAU - Bibliothèque
        ├── analysis.md           # 8 techniques
        ├── ideation.md           # 6 techniques
        ├── perspective.md        # 3 techniques
        └── breakthrough.md       # 3 techniques
```

### 3.2 Modifications Commande

`src/commands/brainstorm.md`:
- Ajouter flags `--random`, `--progressive`
- Ajouter commandes `save`, `back`, `energy`, `technique`
- Modifier format breakpoint (3-5 questions)
- Ajouter logique auto-detect session
- Ajouter energy checkpoints

### 3.3 Project Memory

`.project-memory/brainstorm-sessions/`:
- Fichiers YAML par session
- Nettoyage auto sessions > 30 jours
- Index des sessions actives

---

## 4. Plan d'Implémentation

### Phase 1: Core (PR #1)
1. Session continuation (save, continue-session, auto-detect)
2. Commande `back`
3. Energy checkpoints
4. Format 3-5 questions par itération
5. Confirmation agents [Y/n]

### Phase 2: Techniques (PR #2)
1. Structure `references/techniques/`
2. 20 techniques documentées (4 fichiers)
3. Commande `technique [x]`
4. Mapping techniques → phases

### Phase 3: Modes (PR #3)
1. Flag `--random` avec logique pondérée
2. Flag `--progressive` avec 3 phases
3. Parallélisation @Explore
4. Tests et exemples

---

## 5. Critères de Succès

| Critère | Mesure |
|---------|--------|
| Session continuation fonctionne | Save/restore sans perte de données |
| 20 techniques documentées | Toutes avec format complet |
| Energy checks se déclenchent | Aux 4 triggers définis |
| Back fonctionne | Restaure état précédent correctement |
| Modes random/progressive | Fonctionnent avec flags |
| Tests passent | 100% coverage sur session + techniques |
| Pas de régression | v4.1 features toujours fonctionnelles |

---

## 6. Fichiers Impactés

### Modifications
- `src/commands/brainstorm.md`
- `src/skills/core/brainstormer/SKILL.md`

### Créations
- `src/skills/core/brainstormer/references/session-format.md`
- `src/skills/core/brainstormer/references/techniques/analysis.md`
- `src/skills/core/brainstormer/references/techniques/ideation.md`
- `src/skills/core/brainstormer/references/techniques/perspective.md`
- `src/skills/core/brainstormer/references/techniques/breakthrough.md`
- `.project-memory/brainstorm-sessions/` (runtime)

### Tests
- `src/scripts/test_brainstorm_session.py`
- `docs/briefs/brainstorm-v4/examples/` (sessions exemples)

---

## 7. Risques et Mitigations

| Risque | Impact | Mitigation |
|--------|--------|------------|
| Session corruption | Données perdues | Validation YAML stricte + backup |
| Surcharge contexte | Performance | Session externalisée + lazy loading |
| Trop de techniques | Confusion utilisateur | Suggestions intelligentes par phase |
| Breaking change | Utilisateurs perturbés | Documentation migration claire |

---

## 8. Exploration Summary

**Stack:** Plugin Claude Code (Markdown + Python)
**Patterns:** Skill-based architecture, project-memory, subagents
**Fichiers candidats:** Identifiés section 6

---

*Brief généré le 2026-01-06 — Brainstorm EPCI v4.2*
