# Cahier des Charges — Skill `/brainstorm` EPCI v6

> **Date** : 2026-01-26
> **Destination** : `/spec` → PRD technique
> **Sources** : v5 command, brainstormer cloud desktop, migration docs

---

## 1. Résumé Exécutif

### Objectif

Créer le skill `/brainstorm` pour EPCI v6 qui transforme une idée vague en brief fonctionnel (CDC) exploitable par `/spec`.

### Différenciateurs vs version Cloud Desktop

| Aspect | Cloud Desktop | EPCI v6 |
|--------|---------------|---------|
| Contexte | Conversation only | **Accès codebase** via @Explore |
| Storage | Conversation state | **Persistant** dans `.claude/state/sessions/` |
| Intégration | Standalone | **Chaîné** avec `/spec`, `/implement` |
| Core skills | Aucun | `project-memory`, `clarification-engine`, `breakpoint-system` |

### Décisions Architecture

| Décision | Choix | Justification |
|----------|-------|---------------|
| Storage | `.claude/state/sessions/` | Aligné avec state-manager v6 |
| Hooks | `post-brainstorm` inclus | Tracking métriques, learning |
| EMS | 5 axes + ancres objectives | Scoring cohérent (cloud v3) |
| Personas | 4 avec auto-switch | UX supérieure (cloud v3) |
| Agents | Existants réutilisés | 7/7 déjà dans `src/agents/` |

---

## 2. Analyse Fonctionnelle

### 2.1 Acteurs

| Acteur | Rôle |
|--------|------|
| **Utilisateur** | Fournit l'idée, répond aux questions, valide les outputs |
| **Skill brainstorm** | Orchestre le workflow, génère questions, calcule EMS |
| **@Explore** | Analyse codebase (stack, patterns, conventions) |
| **@ems-evaluator** | Calcule EMS après chaque itération |
| **@technique-advisor** | Suggère techniques selon axes faibles |
| **@planner** | Génère plan convergent en fin de session |
| **@security-auditor** | Audit sécurité si patterns auth détectés |

### 2.2 Use Cases Principaux

#### UC-01 : Session Standard

**Préconditions** : Utilisateur dans un projet avec codebase
**Déclencheur** : `/brainstorm "idée à explorer"`
**Flux principal** :
1. Skill initialise session, charge contexte projet
2. @Explore analyse codebase en background
3. Clarification input si nécessaire
4. Brief reformulé, validation utilisateur
5. HMW questions générées
6. Prompts Perplexity proposés (skip possible)
7. Boucle itérations avec EMS tracking
8. À EMS≥70, proposition finish
9. Génération brief + journal

**Postconditions** :
- `docs/briefs/{slug}/brief-{slug}-{date}.md` créé
- `docs/briefs/{slug}/journal-{slug}-{date}.md` créé
- Session stockée dans `.claude/state/sessions/`
- Hook `post-brainstorm` exécuté

#### UC-02 : Quick Mode

**Préconditions** : Idée simple ou contrainte temps
**Déclencheur** : `/brainstorm "idée" --quick`
**Différences** :
- Max 3 itérations
- EMS simplifié (score global uniquement)
- Persona fixe (Architecte)
- Output : report only (pas de journal)

#### UC-03 : Reprise Session

**Préconditions** : Session précédente interrompue
**Déclencheur** : `/brainstorm --continue {session-id}`
**Flux** :
1. Charger état session depuis storage
2. Restaurer EMS, phase, persona
3. Reprendre à l'itération N+1

#### UC-04 : Mode Party (optionnel)

**Déclencheur** : `/brainstorm "idée" --party`
**Comportement** : 5 personas simultanés via @party-orchestrator

#### UC-05 : Mode Panel (optionnel)

**Déclencheur** : `/brainstorm "idée" --panel`
**Comportement** : Panel 5 experts dev via @expert-panel

---

## 3. Workflow Détaillé

### Phase 1 — Initialisation

```
START
  │
  ├─▶ 1. Charger contexte via project-memory
  │     └─▶ get_patterns(), get_preferences(), recall_features()
  │
  ├─▶ 2. Parser arguments (flags, template)
  │
  ├─▶ 3. Clarification input (si score < 0.6)
  │     └─▶ via clarification-engine
  │     └─▶ BREAKPOINT: Reformulation proposée
  │
  ├─▶ 4. Lancer @Explore codebase (run_in_background: true)
  │     └─▶ Stack detection, patterns, conventions
  │
  ├─▶ 5. Reformuler besoin utilisateur
  │     └─▶ BREAKPOINT: Validation brief
  │     └─▶ Si rejeté → itérer jusqu'à validation
  │
  ├─▶ 6. Auto-détecter template
  │     └─▶ feature|audit|project|research|decision|problem|strategy
  │
  ├─▶ 7. Sync @Explore (attendre si pas terminé)
  │
  ├─▶ 8. Générer 3-5 HMW questions (basées sur codebase)
  │     └─▶ "How Might We..." contextualisées
  │
  ├─▶ 9. Générer prompts Perplexity (3-5)
  │     └─▶ Format: 🔍 Standard ou 🔬 Deep Research
  │     └─▶ BREAKPOINT: Attendre injection ou skip
  │
  ├─▶ 10. Initialiser EMS baseline
  │      └─▶ Clarté: 40 (brief validé), autres: 20
  │      └─▶ Ajustements si sources analysées
  │
  ├─▶ 11. Set état initial
  │      └─▶ Phase: 🔀 DIVERGENT
  │      └─▶ Persona: 📐 Architecte
  │
  └─▶ 12. BREAKPOINT: Questions cadrage (3 max)
         └─▶ Cible, contraintes, délai
```

### Phase 2 — Itérations

```
LOOP (jusqu'à finish ou max 10 itérations)
  │
  ├─▶ 1. Intégrer réponses utilisateur
  │
  ├─▶ 2. Recalculer EMS via @ems-evaluator
  │     └─▶ Input: session state, réponses
  │     └─▶ Output: scores 5 axes, delta, weak_axes[]
  │
  ├─▶ 3. Check auto-switch persona
  │     │
  │     ├─ Si certitude non étayée → 🥊 Sparring
  │     ├─ Si stagnation EMS → 🛠️ Pragmatique
  │     ├─ Si iter ≥ 6 sans décisions → 🛠️ Pragmatique
  │     ├─ Si synthesis needed → 📐 Architecte
  │     └─ Si exploration open → 🧒 Maïeuticien
  │
  ├─▶ 4. Check suggestion technique
  │     └─▶ IF weak_axes[] non vide AND pas de technique récente
  │     └─▶ Invoke @technique-advisor (Haiku)
  │     └─▶ BREAKPOINT: Technique suggérée
  │
  ├─▶ 5. Check recherche ciblée Perplexity
  │     └─▶ IF iter ≥ 2 AND EMS < 50 AND axes faibles
  │     └─▶ Proposer prompts ciblés par axe
  │
  ├─▶ 6. BREAKPOINT: Status EMS
  │     └─▶ Afficher radar 5 axes
  │     └─▶ Afficher phase + persona
  │     └─▶ Afficher progression (Init→Current)
  │     └─▶ Options: continue, dive, pivot, finish, checkpoint
  │
  ├─▶ 7. Transition check (EMS = 50)
  │     └─▶ BREAKPOINT: Suggérer passage Convergent
  │
  ├─▶ 8. Finalization check (EMS ≥ 70)
  │     └─▶ BREAKPOINT: Proposer finish
  │     └─▶ Options: Continuer, Preview (@planner), Finaliser
  │
  ├─▶ 9. Energy check
  │     └─▶ IF stagnation (delta < 3 × 2 iter) OR iter ≥ 7
  │     └─▶ BREAKPOINT: Energy checkpoint
  │     └─▶ Options: continuer, pause (save), accélérer, pivoter
  │
  └─▶ 10. Générer questions itération (3 max)
         └─▶ BREAKPOINT: Questions catégorisées
         └─▶ Tags: 🛑 Critical, ⚠️ Important, ℹ️ Info
```

### Phase 3 — Génération

```
FINALIZE
  │
  ├─▶ 1. @planner preview (si pas déjà fait)
  │     └─▶ Générer plan convergent
  │
  ├─▶ 2. @security-auditor (si patterns auth détectés)
  │     └─▶ Review sécurité préventive
  │
  ├─▶ 3. Validation section par section (sauf --quick)
  │     └─▶ BREAKPOINT par section majeure
  │
  ├─▶ 4. Créer répertoire output
  │     └─▶ mkdir -p docs/briefs/{slug}/
  │
  ├─▶ 5. Write brief-{slug}-{date}.md
  │     └─▶ Format PRD v3.0
  │     └─▶ Sections: Executive Summary, Problem, Goals,
  │         Non-Goals, Personas, User Stories, FAQ, Metrics
  │
  ├─▶ 6. Write journal-{slug}-{date}.md
  │     └─▶ Historique complet exploration
  │     └─▶ Progression EMS, décisions, pivots
  │
  ├─▶ 7. Calculate complexity routing
  │     └─▶ Via complexity-calculator
  │     └─▶ Output: TINY|SMALL|STANDARD|LARGE → routing skill
  │
  ├─▶ 8. Execute hook post-brainstorm
  │     └─▶ Données: slug, ems_score, techniques, iterations, duration
  │     └─▶ Stockage métriques dans project-memory
  │
  └─▶ 9. Display completion summary
         └─▶ EMS final + radar
         └─▶ Fichiers générés
         └─▶ Next steps recommandés
         └─▶ Routing: /spec → /implement ou /quick
```

---

## 4. Système EMS (v3 avec ancres)

### 4.1 Les 5 Axes

| Axe | Poids | Question clé |
|-----|-------|--------------|
| **Clarté** | 25% | Le sujet est-il bien défini ? |
| **Profondeur** | 25% | A-t-on creusé suffisamment ? |
| **Couverture** | 20% | A-t-on exploré tous les angles ? |
| **Décisions** | 20% | A-t-on tranché et progressé ? |
| **Actionnabilité** | 10% | Peut-on agir concrètement ? |

### 4.2 Ancres Objectives

| Score | Clarté | Profondeur | Couverture | Décisions | Actionnabilité |
|-------|--------|------------|------------|-----------|----------------|
| **20** | Sujet énoncé | Surface only | 1 angle | Tout ouvert | Idées vagues |
| **40** | Brief validé | 1 chaîne "pourquoi" | 2-3 angles | 1-2 orientations | "Il faudrait..." |
| **60** | + Contraintes + critères | Framework appliqué | Risques adressés | Décisions verrouillées | Actions + owner |
| **80** | + SMART + stakeholders | Insights non-évidents | Multi-stakeholders | Arbitrages + priorisation | + timeline + dépendances |
| **100** | Zéro ambiguïté | Cause racine tracée | Exhaustif | Tous fils fermés | Plan complet exécutable |

### 4.3 Seuils et Messages

| EMS | Icône | Statut | Message |
|-----|-------|--------|---------|
| 0-29 | 🌱 | Début | "Exploration débutante — continuons" |
| 30-59 | 🌿 | Développement | "En développement" |
| 60-89 | 🌳 | Mature | "`finish` disponible" |
| 90-100 | 🎯 | Complète | "`finish` recommandé" |

### 4.4 Formule

```
EMS = (Clarté × 0.25) + (Profondeur × 0.25) + (Couverture × 0.20)
    + (Décisions × 0.20) + (Actionnabilité × 0.10)
```

---

## 5. Système Personas

### 5.1 Les 4 Personas

| Persona | Icône | Philosophie | Patterns de langage |
|---------|-------|-------------|---------------------|
| **Maïeuticien** | 🧒 | Socratique, fait émerger | "Intéressant ! Dis-moi plus..." |
| **Sparring** | 🥊 | Challenge, demande preuves | "Attends — qu'est-ce qui te fait dire ça ?" |
| **Architecte** | 📐 | Structure, frameworks | "Structurons. Je vois 3 dimensions..." |
| **Pragmatique** | 🛠️ | Action, coupe le blabla | "OK, concrètement on fait quoi ?" |

### 5.2 Règles Auto-Switch

| Contexte détecté | Persona activé |
|------------------|----------------|
| Début session, sujet flou | 🧒 Maïeuticien |
| Génération HMW | 🧒 Maïeuticien |
| Sujet complexe, multi-dimensions | 📐 Architecte |
| Application framework | 📐 Architecte |
| Synthèse, récapitulatif | 📐 Architecte |
| Mots "évidemment", "forcément" | 🥊 Sparring |
| Exercice pre-mortem | 🥊 Sparring |
| Stagnation EMS (< 5 pts × 2 iter) | 🛠️ Pragmatique |
| Iteration ≥ 6 sans décisions | 🛠️ Pragmatique |
| Point de décision atteint | 🛠️ Pragmatique |
| Phase Convergent | 📐 + 🛠️ Mix |

### 5.3 Signalement

À chaque changement de persona, préfixer le message :
```
📐 [Structure] Organisons ce qu'on a exploré...
🥊 [Challenge] Pause — tu viens de dire "évidemment"...
```

---

## 6. Commandes et Flags

### 6.1 Commandes Session

| Commande | Action |
|----------|--------|
| `continue` | Itération suivante |
| `dive [topic]` | Deep dive sur un point |
| `pivot` | Réorienter vers sujet émergent |
| `converge` | Passer en phase Convergent |
| `diverge` | Revenir en phase Divergent |
| `modes` | Afficher personas disponibles |
| `mode [nom]` | Changer de persona |
| `premortem` | Exercice anticipation échecs |
| `research` | Générer nouveaux prompts Perplexity |
| `checkpoint` | Sauvegarder pour reprise |
| `finish` | Générer outputs |
| `finish --force` | Forcer même si EMS < seuil |
| `status` | Afficher état complet |

### 6.2 Flags Lancement

| Flag | Défaut | Description |
|------|--------|-------------|
| `--template [type]` | auto | feature, audit, project, research, decision, problem, strategy |
| `--quick` | off | Mode rapide (3 iter max, report only) |
| `--turbo` | off | Mode turbo via @clarifier (Haiku) |
| `--party` | off | Mode multi-persona (5 voix) |
| `--panel` | off | Panel 5 experts dev |
| `--competitive` | off | Analyse concurrentielle |
| `--challenge` | off | Devil's advocate dès le départ |
| `--no-hmw` | off | Skip génération HMW |
| `--no-security` | off | Skip @security-auditor |
| `--no-clarify` | off | Skip clarification input |
| `--continue [id]` | - | Reprendre session existante |

---

## 7. Subagents

### 7.1 Agents Requis (tous existants)

| Agent | Fichier | Model | Usage |
|-------|---------|-------|-------|
| @ems-evaluator | `src/agents/ems-evaluator.md` | Haiku | Calcul EMS chaque itération |
| @technique-advisor | `src/agents/technique-advisor.md` | Haiku | Suggestion techniques axes faibles |
| @planner | `src/agents/planner.md` | Sonnet | Plan convergent fin session |
| @security-auditor | `src/agents/security-auditor.md` | Opus | Audit si patterns auth |
| @clarifier | `src/agents/clarifier.md` | Haiku | Mode turbo |
| @party-orchestrator | `src/agents/party-orchestrator.md` | Sonnet | Mode --party |
| @expert-panel | `src/agents/expert-panel.md` | Sonnet | Mode --panel |

### 7.2 Agent Natif

| Agent | Usage |
|-------|-------|
| @Explore | Analyse codebase (stack, patterns, conventions) |

---

## 8. Core Skills

| Core Skill | Usage dans brainstorm |
|------------|----------------------|
| `project-memory` | `init()`, `get_patterns()`, `get_preferences()`, `recall_features()` en Phase 1 |
| `clarification-engine` | Nettoyage input vocal (Step 0 si score < 0.6) |
| `breakpoint-system` | Tous les breakpoints interactifs (validation, EMS, finish) |
| `complexity-calculator` | Routing final vers `/spec` → `/implement` ou `/quick` |

---

## 9. Storage et Outputs

### 9.1 Storage Session

```
.claude/state/sessions/
└── brainstorm-{slug}-{timestamp}.json
```

**Schema session** :
```json
{
  "id": "brainstorm-auth-oauth-20260126-143052",
  "slug": "auth-oauth",
  "status": "in_progress|completed|paused",
  "created_at": "ISO-8601",
  "last_update": "ISO-8601",
  "template": "feature",
  "flags": ["--competitive"],

  "phase": "divergent|convergent",
  "persona": "architecte|maieuticien|sparring|pragmatique",
  "iteration": 5,

  "ems": {
    "global": 68,
    "clarity": 78,
    "depth": 65,
    "coverage": 72,
    "decisions": 52,
    "actionability": 45,
    "history": [
      {"iter": 1, "score": 35, "delta": "+35"},
      {"iter": 2, "score": 48, "delta": "+13"}
    ]
  },

  "context": {
    "brief": "reformulated brief text",
    "hmw_questions": ["HMW 1", "HMW 2", "HMW 3"],
    "codebase_analysis": {},
    "perplexity_results": []
  },

  "decisions": [],
  "open_threads": [],
  "techniques_applied": []
}
```

### 9.2 Outputs

```
docs/briefs/{slug}/
├── brief-{slug}-{date}.md    # PRD v3.0 format
└── journal-{slug}-{date}.md  # Exploration history
```

**Sections brief (PRD v3.0)** :
1. Document Header (PRD-YYYY-XXX, Version, Status)
2. Executive Summary (TL;DR, Problem, Solution, Impact)
3. Background & Strategic Fit
4. Problem Statement (Current, Evidence, Impact)
5. Goals (Business, User, Technical + métriques)
6. Non-Goals (exclusions explicites)
7. Personas (minimum 1 primaire)
8. User Stories (format "En tant que... je veux... afin de")
9. User Flow (As-Is vs To-Be)
10. Assumptions (Technical, Business, User)
11. FAQ (Internal + External)
12. Success Metrics (KPIs)
13. Timeline & Milestones

---

## 10. Hook post-brainstorm

### Données envoyées

```json
{
  "hook": "post-brainstorm",
  "timestamp": "ISO-8601",
  "data": {
    "feature_slug": "auth-oauth",
    "ems_score": 78,
    "ems_axes": {
      "clarity": 85,
      "depth": 72,
      "coverage": 80,
      "decisions": 75,
      "actionability": 68
    },
    "iterations": 5,
    "duration_minutes": 35,
    "phase_final": "convergent",
    "techniques_applied": ["5-whys", "pre-mortem"],
    "personas_used": ["architecte", "sparring"],
    "template": "feature",
    "flags": [],
    "output_files": [
      "docs/briefs/auth-oauth/brief-auth-oauth-20260126.md",
      "docs/briefs/auth-oauth/journal-auth-oauth-20260126.md"
    ]
  }
}
```

### Effets

1. Sauvegarde métriques dans `project-memory`
2. Update velocity calibration si feature trackée
3. Learning sur techniques efficaces par type de projet

---

## 11. Breakpoints Types

### 11.1 Breakpoint Clarification

```yaml
type: clarification-input
title: "CLARIFICATION INPUT"
data:
  original: "{input_brut}"
  clarity_score: 0.45
  reformulated: "{input_clarifié}"
ask:
  question: "La reformulation vous convient-elle ?"
  options:
    - "✅ Utiliser (Recommended)"
    - "✏️ Modifier"
    - "➡️ Garder original"
```

### 11.2 Breakpoint EMS Status

```yaml
type: ems-status
title: "BRAINSTORM STATUS"
data:
  phase: "DIVERGENT"
  persona: "Architecte"
  iteration: 3
  ems:
    score: 58
    delta: "+12"
    axes: {clarity: 72, depth: 55, coverage: 60, decisions: 45, actionability: 40}
    weak_axes: ["decisions", "actionability"]
    progression: ["Init(25)", "Iter1(35)", "Iter2(46)", "Current(58)"]
  done: ["Brief validé", "HMW générées", "Stack analysée"]
  open: ["Contraintes techniques", "Timeline"]
commands: ["continue", "dive", "pivot", "finish", "checkpoint"]
```

### 11.3 Breakpoint Transition

```yaml
type: plan-review
title: "PHASE TRANSITION"
data:
  metrics:
    ems_score: 50
    milestone: "Mi-parcours atteint"
  preview_next_phase:
    phase_name: "CONVERGENT"
    description: "Passage de l'exploration à la convergence"
ask:
  question: "Mi-parcours EMS 50. Quelle direction ?"
  options:
    - "Continuer Divergent"
    - "Passer Convergent (Recommended)"
    - "Appliquer technique"
```

### 11.4 Breakpoint Finalization

```yaml
type: plan-review
title: "FINALIZATION CHECKPOINT"
data:
  metrics:
    ems_score: 78
    axes: {clarity: 85, depth: 72, coverage: 80, decisions: 75, actionability: 68}
  progression: "Init(25) → Iter5(78)"
  preview_next_phase:
    phase_name: "Phase 3: Génération"
    tasks:
      - "Générer brief PRD v3.0"
      - "Créer journal exploration"
ask:
  question: "Brief EMS 78/100 prêt. Quelle action ?"
  options:
    - "Continuer (plus d'itérations)"
    - "Preview (@planner)"
    - "Finaliser (Recommended)"
```

---

## 12. Contraintes et Limites

| Contrainte | Valeur | Rationale |
|------------|--------|-----------|
| Max itérations | 10 | Éviter sessions trop longues |
| EMS minimum pour finish | 70 | Garantir qualité brief |
| Questions par itération | 3 max | Éviter surcharge cognitive |
| Techniques par session | 5 max | Focus sur convergence |
| Session timeout | 2h | Préservation contexte |
| Bias alert max | 1 par type | Ne pas spammer |

---

## 13. Error Handling

| Erreur | Cause | Recovery |
|--------|-------|----------|
| @Explore timeout | Codebase trop large | Continuer avec contexte partiel |
| @ems-evaluator échec | Parsing error | Estimation manuelle, continuer |
| @technique-advisor indisponible | Rate limit | Proposer technique par défaut (Six Hats) |
| Session file corrupted | JSON error | Archiver, démarrer nouvelle |
| EMS stagnation | 3 iter < 3 pts | Proposer pivot ou technique |
| Brief rejeté × 3 | Incompréhension | Proposer reformuler le sujet |

---

## 14. Fichiers Sources Référence

| Fichier | Usage pour implémentation |
|---------|---------------------------|
| `archive/5.6/commands/brainstorm.md` | Workflow EPCI complet, breakpoints |
| `skills-web/brainstormer/SKILL.md` | Structure skill, decision tree |
| `skills-web/brainstormer/references/ems-system.md` | Ancres objectives détaillées |
| `skills-web/brainstormer/references/personas.md` | 4 personas, règles switch |
| `skills-web/brainstormer/references/frameworks.md` | Catalogue frameworks |
| `skills-web/brainstormer/references/perplexity-patterns.md` | Génération prompts |
| `src/agents/ems-evaluator.md` | Agent calcul EMS |
| `src/agents/technique-advisor.md` | Agent suggestion techniques |
| `src/skills/core/breakpoint-system/` | Système breakpoints |
| `src/skills/core/project-memory/` | Contexte projet |

---

## 15. Critères d'Acceptation

### Fonctionnels

- [ ] Session standard complète avec EMS tracking
- [ ] Quick mode (3 iter max, report only)
- [ ] 4 personas avec auto-switch
- [ ] Phases Divergent/Convergent explicites
- [ ] HMW questions après brief
- [ ] Prompts Perplexity générés
- [ ] Pre-mortem via commande
- [ ] Deep dive / Pivot supportés
- [ ] Checkpoint / Resume fonctionnels
- [ ] Output brief PRD v3.0 format
- [ ] Output journal exploration
- [ ] Hook post-brainstorm exécuté

### Techniques

- [ ] Storage dans `.claude/state/sessions/`
- [ ] Tous breakpoints via breakpoint-system
- [ ] Integration project-memory
- [ ] Integration clarification-engine
- [ ] Integration complexity-calculator
- [ ] 7 agents appelés correctement
- [ ] Validation `python3 src/scripts/validate.py`

---

## 16. Prochaine Étape

### 16.1 Sauvegarder le CDC

```bash
# Copier ce fichier vers l'emplacement projet
cp /home/epci/.claude/plans/dreamy-tumbling-pie.md /home/epci/apps/claude-epci/docs/specs/brainstorm-cdc.md
```

### 16.2 Lancer Factory

```bash
/epci:factory brainstorm --cdc docs/specs/brainstorm-cdc.md
```

Factory aura accès au contexte via :
- Le fichier CDC passé en argument
- Les fichiers sources listés en section 14
- Les agents existants dans `src/agents/`
- Les core skills dans `src/skills/core/`

### 16.3 Workflow Factory

1. Factory lit le CDC
2. Génère `src/skills/brainstorm/SKILL.md` complet
3. Génère `src/skills/brainstorm/references/` avec :
   - `ems-system.md` (copie/adaptation de cloud)
   - `personas.md` (copie/adaptation de cloud)
   - `brief-format.md` (template PRD v3.0)
   - `journal-format.md` (template journal)
4. Validation via `python3 src/scripts/validate.py`
