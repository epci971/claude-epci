# EPCI Plugin — Claude Code Development Assistant

> **Version** : 5.1.2 | **Date** : Janvier 2025

---

## 1. Overview

EPCI (Explore → Plan → Code → Inspect) structure le développement en phases avec validation à chaque étape.

### Philosophie v4

| Principe            | Description                                                   |
| ------------------- | ------------------------------------------------------------- |
| **Simplicité**      | 14 commandes spécialisées                                     |
| **Modularité**      | 30 Skills, 16 Subagents, Hooks natifs                         |
| **Traçabilité**     | Feature Document comme fil rouge                              |
| **MCP Integration** | 5 serveurs externes (Context7, Sequential, Magic, Playwright, Notion) |

### Nouveautés v5.1.2 (Auto Backlog Generation)

- **Génération automatique backlog.md** : `/decompose` génère maintenant automatiquement le backlog table
- **Génération automatique prd.json** : Plus besoin de flag, toujours généré
- **Flag `--wiggum` supprimé** : Tous les fichiers Ralph générés automatiquement
- **Deux niveaux de granularité** : Sub-specs (1-5 jours) + Stories (1-2h) dans backlog
- **ralph.sh et PROMPT.md** : Générés automatiquement avec détection stack

### Nouveautés v5.1.0 (Ralph Wiggum Integration)

- **Nouvelle commande `/ralph`** : Exécution autonome overnight avec boucle itérative
- **Nouvelle commande `/cancel-ralph`** : Annulation d'une session Ralph en cours
- **Deux modes d'exécution** : Hook (même session, <2h) et Script (contexte frais, overnight)
- **Circuit Breaker** : Détection automatique des boucles bloquées (3 états: CLOSED/HALF_OPEN/OPEN)
- **RALPH_STATUS Block** : Format structuré de communication avec double condition de sortie
- **Flag `--granularity`** : Contrôle la taille des stories (micro/small/standard)
- **Nouveaux skills** : `ralph-analyzer`, `ralph-converter`
- **Nouvel agent** : `@ralph-executor` pour exécution des stories individuelles
- **Hooks Ralph** : `ralph-stop`, `ralph-session-init`, `ralph-iteration`, `ralph-session-reset`

### Nouveautés v4.9.1 (Native Plan Integration)

- **Flag `--from-native-plan <file>`** : Import du plan natif Claude Code comme base pour Phase 1
- **Exploration conditionnelle** : @Explore automatique si §1 manquant lors de l'import
- **Copie automatique pour traçabilité** : Plan natif archivé dans Feature Document §2
- **Raffinement intelligent** : Phase 1 raffine le plan natif (2-15 min) au lieu de repartir de zéro
- **Workflow hybride** : `/epci` peut maintenant fonctionner avec ou sans `/brief` préalable
- **Traçabilité git** : Plan natif copié dans le projet pour collaboration d'équipe

### Nouveautés v4.9 (Expert Panel & Rule Clarifier)

- **3 nouveaux agents** : `@expert-panel`, `@party-orchestrator`, `@rule-clarifier` pour brainstorming v5.0
- **Nouveau skill** : `input-clarifier` pour validation entrées utilisateur
- **Finalization Checkpoint obligatoire** : À EMS >= 70, checkpoint bloquant avec choix [1] Continuer / [2] Preview / [3] Finaliser
- **Pas de finalisation automatique** : Ne JAMAIS passer en Phase 3 sans choix explicite utilisateur
- **Preview sans finalisation** : Option [2] permet de voir le plan @planner puis revenir au brainstorm

### Nouveautés v4.8.1 (Finalization Checkpoint)

- **Finalization Checkpoint** : EMS >= 85 pour déclencher checkpoint

### Nouveautés v4.8 (Auto-Techniques Brainstorm)

- **Auto-sélection techniques** : Basée sur axes EMS faibles (< 50) via `@technique-advisor`
- **Mix de techniques** : Proposition de 2 techniques complémentaires si 2+ axes faibles
- **Transition check explicite** : Choix Divergent/Convergent à EMS=50
- **Preview @planner/@security** : En phase Convergent à EMS >= 65
- **Hook post-brainstorm documenté** : Tracking `techniques_applied` dans métriques
- **Flag `--no-technique`** : Désactive l'auto-suggestion de techniques
- **Workflow Phase 1 réordonné** : HMW générés après @Explore pour contexte codebase

### Nouveautés v4.6 (Brief Refactoring)

- **Inversion reformulation/exploration** : La reformulation est maintenant AVANT l'exploration dans `/brief`
- **Breakpoint validation obligatoire** : Toujours afficher un breakpoint apres reformulation pour valider le besoin
- **Hooks pre-brief et post-brief actifs** : Nouveaux hooks pour tracabilite complete
- **Fusion Analysis + Complexity** : Step 2 et Step 4 fusionnees pour eliminer la redondance
- **@clarifier explicite** : Invocation @clarifier (Haiku) documentee dans mode --turbo
- **Gestion erreur @Explore** : Fallback documente si exploration echoue

### Nouveautés v4.5 (Brainstorming v4.1 — SuperPowers Integration)

- **One-at-a-Time Questions** : Une question à la fois avec choix multiples A/B/C (pattern SuperPowers)
- **Section-by-Section Validation** : Validation incrémentale du brief section par section
- **@planner in Brainstorm** : Plan préliminaire automatique en phase Convergent
- **@security-auditor in Brainstorm** : Analyse sécurité conditionnelle si patterns auth/payment détectés
- **Nouvelles commandes brainstorm** : `batch`, `plan-preview`, `security-check`
- **Nouveaux flags** : `--no-security`, `--no-plan`

### Nouveautés v4.4

- **Fusion learn → memory** : `/learn` supprimé, learning intégré dans `/memory` via subcommands `learn status|reset|calibrate`
- **Ajout `/commit`** : Commande dédiée pour finalisation git avec contexte EPCI
- **3 nouveaux agents turbo** : `@clarifier`, `@planner`, `@implementer` pour modes rapides
- **Hooks obligatoires documentés** : Section 11 ajoutée pour garantir la mise à jour mémoire

### Nouveautés v4.3

- **Fusion spike → brainstorm** : `/spike` supprimé, exploration technique intégrée dans `/brainstorm` via commande `spike [duration] [question]`

### Nouveautés v4.2

- **Renommage commandes** : Préfixe `epci-` supprimé (ex: `/epci:brief` au lieu de `/epci:epci-brief`)
- **MCP Integration** : Context7 (docs), Sequential (reasoning), Magic (UI), Playwright (E2E)
- **Auto-activation MCP** : Basée sur personas et contexte
- **Flags MCP** : `--c7`, `--seq`, `--magic`, `--play`, `--no-mcp`
- **6 Personas** : Architect, Frontend, Backend, Security, QA, Doc

---

## 2. Repository Structure

```
src/
├── agents/           # 13 subagents (7 core + 3 turbo + 2 brainstorm + 1 ralph)
├── commands/         # 14 commandes (brief, epci, quick, ralph, etc.)
├── hooks/            # Système hooks (runner.py, examples/, active/)
├── mcp/              # MCP Integration (config, activation, registry)
├── orchestration/    # Wave orchestration
├── scripts/          # Validation (validate_all.py, etc.)
├── settings/         # Configuration (flags.md)
└── skills/           # 30 skills
    ├── core/         # 18 skills fondamentaux (inclut ralph-analyzer, ralph-converter)
    ├── stack/        # 5 skills technologie (react, django, symfony, spring, frontend)
    ├── personas/     # Système personas
    ├── mcp/          # MCP skill
    ├── promptor/     # Voice-to-brief + Notion export
    └── factory/      # Component Factory (4 skills)

docs/                 # Documentation détaillée
build/                # Production v2.7 (référence)
archive/              # Versions dépréciées
```

---

## 3. Core Workflow

### Routing par complexité

```
Brief brut → /brief → Évaluation
                        │
       ┌────────────────┴────────────────┐
       ▼                                 ▼
  TINY/SMALL                         STD/LARGE
    /quick                             /epci
```

| Catégorie    | Critères                            | Workflow           |
| ------------ | ----------------------------------- | ------------------ |
| **TINY**     | 1 fichier, < 50 LOC                 | `/quick`           |
| **SMALL**    | 2-3 fichiers, < 200 LOC             | `/quick`           |
| **STANDARD** | 4-10 fichiers, tests requis         | `/epci` (3 phases) |
| **LARGE**    | 10+ fichiers, architecture complexe | `/epci --large`    |

> **Note** : Pour les incertitudes techniques, utiliser `/brainstorm` avec la commande `spike [duration] [question]` intégrée.

### Workflow avec Plan Natif (v4.9.1+)

Nouveau workflow permettant d'utiliser le plan natif de Claude Code :

```
Plan Natif Claude Code → /epci --from-native-plan plan.md --slug feature-name
                              ↓
                         [Step 0.5]
                              ↓
                    ┌─────────┴─────────┐
                    ▼                   ▼
              §1 existe ?           §1 manquant
                  ↓                     ↓
            Utilise §1          Lance @Explore
                  ↓                     ↓
                  └──────────┬──────────┘
                             ↓
                    Copie plan natif en §2
                             ↓
                    Phase 1: Raffine plan
                    (découpage 2-15 min)
                             ↓
                    Phase 2-3: Standard
```

**Commandes** :

```bash
# Workflow A : Standard (recommandé)
/brief "description feature"
# → Crée Feature Document avec §1
/epci feature-slug
# → Phase 1-3 complètes

# Workflow B : Avec plan natif (nouveau)
<mode plan natif Claude Code>
# → Génère ~/.claude/plans/plan.md
/epci --from-native-plan ~/.claude/plans/plan.md --slug feature-auth
# → Crée §1 via @Explore (si manquant)
# → Copie plan natif en §2
# → Raffine en Phase 1
# → Phase 2-3 standard

# Workflow C : Hybride
/brief "description feature"
# → Crée Feature Document avec §1
<mode plan natif Claude Code>
# → Génère plan haut niveau
/epci --from-native-plan ~/.claude/plans/plan.md --slug feature-slug
# → Utilise §1 existant + plan natif comme base
# → Phase 1 raffine le plan natif
```

**Avantages du workflow B/C** :
- ✅ Plan natif comme base haut niveau
- ✅ Phase 1 raffine (2-15 min, tests, validation)
- ✅ Traçabilité : plan copié dans git
- ✅ Collaboration : équipe voit le raisonnement initial

---

### Workflow avec Brainstorm (idée vague → specs)

Workflow complet pour transformer une idée vague en spécifications exécutables :

```
Idée vague → /brainstorm → Brief structuré avec User Stories
                              │
                              ↓ (Calcul effort automatique)
                              │
             ┌────────────────┼────────────────┐
             ▼                ▼                ▼
        Effort ≤2j       Effort 3-5j      Effort >5j
        (TINY)           (STANDARD)       (LARGE)
             │                │                │
             ↓                ↓                ↓
          /brief           /brief          /decompose
             │                │                │
             ↓                ↓                ↓
    /quick --autonomous   /quick ou       Sous-specs
                          /epci           (S01-SNN.md)
                                               │
                                    ┌──────────┴──────────┐
                                    ▼                     ▼
                              /orchestrate          /brief @S01
                              (batch DAG)           (manuel)
```

**Decision automatique basée sur User Stories** :

| Must-have Stories | Complexité | Effort total | Catégorie | Commande recommandée |
|-------------------|------------|--------------|-----------|----------------------|
| US1, US2 | S, S | 2 jours | TINY | `/brief` → `/quick --autonomous` |
| US1, US2 | S, M | 4 jours | STANDARD | `/brief` (option: `/decompose`) |
| US1, US2, US3 | M, M, M | 9 jours | LARGE | `/decompose` → `/orchestrate` |

**Commandes** :

```bash
# Workflow D : Brainstorm → Brief direct (TINY/STANDARD)
/brainstorm "système de notifications temps réel"
# → EMS iterations, HMW, personas
# → Génère brief avec User Stories
# → Calcul: 2 stories Must-have (S+M) = 4j → STANDARD
# → Recommandation: /brief @./docs/briefs/notif-temps-reel/brief-notif-2025-01-12.md

/brief @./docs/briefs/notif-temps-reel/brief-notif-2025-01-12.md
# → @Explore ciblé
# → Route vers /quick ou /epci selon files impacted

# Workflow E : Brainstorm → Decompose → Orchestrate (LARGE)
/brainstorm "migration architecture vers microservices"
# → EMS iterations, techniques (MoSCoW, Pre-mortem)
# → Génère brief avec 6 User Stories Must-have
# → Calcul: 6 stories (M+L+M+M+L+M) = 17j → LARGE
# → Recommandation: /decompose

/decompose ./docs/briefs/migration-microservices/brief-migration-2025-01-12.md
# → Auto-détecte format brainstorm (### US1 —)
# → Mappe complexité: S→1j, M→3j, L→5j
# → Génère INDEX.md + S01-S06.md avec dépendances

/orchestrate ./docs/specs/migration-microservices/
# → Exécution DAG automatique
# → Priorité, parallélisation, auto-retry

# Workflow F : Brainstorm → Decompose → Manuel
/brainstorm "refonte complète admin"
# → Génère brief avec User Stories

/decompose ./docs/briefs/admin-refonte/brief-admin-2025-01-12.md
# → Sous-specs S01-S09.md

# Exécution manuelle contrôlée
/brief @./docs/specs/admin-refonte/S01-auth-base.md
/brief @./docs/specs/admin-refonte/S02-roles-perms.md
# ... etc.
```

**Avantages du workflow Brainstorm** :
- ✅ Idée vague → specs structurées via EMS iterations
- ✅ Personas et User Stories pour ancrage utilisateur
- ✅ Calcul effort automatique basé sur complexité (S/M/L)
- ✅ Recommendation next steps intelligente
- ✅ Pour LARGE : décomposition automatique en sous-specs
- ✅ Journal d'exploration pour traçabilité des décisions

**Quand utiliser chaque workflow** :

| Situation | Workflow | Raison |
|-----------|----------|--------|
| Brief clair, scope défini | A (Standard) | `/brief` → `/epci` direct |
| Plan natif Claude Code existe | B (Plan natif) | Réutiliser raisonnement initial |
| Idée vague, besoin exploration | D/E/F (Brainstorm) | Clarification via EMS iterations |
| PRD existant, déjà structuré | Direct `/decompose` | Document déjà complet |
| Exécution overnight autonome | G (Ralph) | Sans supervision humaine |

---

### Workflow avec Ralph Wiggum (exécution overnight)

Workflow pour exécution autonome sur plusieurs heures sans supervision :

```
PRD complet → /decompose → backlog.md + prd.json + ralph.sh (auto)
                                          │
                                          ↓
                                     /ralph <dir>
                                          │
                              ┌───────────┴───────────┐
                              ▼                       ▼
                         Mode Hook              Mode Script
                       (même session)        (contexte frais)
                           <2h                   overnight
                              │                       │
                              └───────────┬───────────┘
                                          ↓
                                   Boucle itérative
                                          │
                              ┌───────────┼───────────┐
                              ▼           ▼           ▼
                          Story N    Circuit     RALPH_STATUS
                        @executor    Breaker      Analysis
                              │           │           │
                              └───────────┼───────────┘
                                          ↓
                               ┌──────────┴──────────┐
                               ▼                     ▼
                          EXIT_SIGNAL          Continue
                           = true                loop
                               │                     │
                               ↓                     ↓
                          Completion            Next story
```

**Modes d'exécution** :

| Mode | Contexte | Durée | Robustesse | Auto-sélection |
|------|----------|-------|------------|----------------|
| `hook` | Même session | <2h | Medium | stories < 10 AND duration < 2h |
| `script` | Frais/itération | >2h | High | stories >= 10 OR duration >= 2h |

**Commandes** :

```bash
# Workflow G : Ralph Wiggum (overnight)
/decompose migration-prd.md --granularity small
# → Génère automatiquement :
#   - Sub-specs S01-SNN.md (1-5 jours chacune)
#   - backlog.md (stories 1-2h, format Architector)
#   - prd.json (format Ralph)
#   - ralph.sh (script exécutable)
#   - PROMPT.md (prompt personnalisé)

/ralph docs/specs/migration/ --overnight --safety-level moderate
# → Mode script auto-sélectionné
# → Circuit breaker activé
# → Boucle jusqu'à completion ou max_iterations
# → Commits automatiques par story

# Pour annuler une session en cours
/cancel-ralph
```

**Avantages du workflow Ralph** :
- ✅ Exécution overnight sans supervision
- ✅ Circuit breaker pour détecter boucles bloquées
- ✅ Rate limiting pour éviter surcharge API
- ✅ Commits atomiques par story complétée
- ✅ Progression persistée (.ralph-session.json)
- ✅ Dual-condition exit (indicateurs + EXIT_SIGNAL explicite)

---

### Feature Document (STD/LARGE)

```markdown
# Feature Document — [Titre]

## §1 — Brief Fonctionnel ← /brief

## §2 — Plan d'Implémentation ← /epci Phase 1

## §3 — Implementation ← /epci Phases 2-3
```

---

## 4. Commands (14)

| Commande      | Rôle                                                        |
| ------------- | ----------------------------------------------------------- |
| `/brief`      | Point d'entrée unique — exploration, clarification, routing |
| `/epci`       | Workflow complet 3 phases (STD/LARGE)                       |
| `/quick`      | Workflow condensé EPCT (TINY/SMALL)                         |
| `/ralph`      | **Exécution autonome overnight — boucle itérative, circuit breaker** |
| `/cancel-ralph` | **Annulation session Ralph en cours**                     |
| `/orchestrate`| Exécution batch de specs — DAG, priorité (préférer `/ralph`) |
| `/commit`     | Finalisation git avec contexte EPCI                         |
| `/rules`      | Génère .claude/rules/ — conventions projet automatiques     |
| `/brainstorm` | Feature discovery v4.8 — Auto-techniques, mix, transition checks |
| `/debug`      | Diagnostic bugs structuré                                   |
| `/decompose`  | Décomposition PRD en sous-specs + backlog.md + prd.json     |
| `/memory`     | Gestion mémoire projet + learning (calibration, préférences)|
| `/promptor`   | Voice-to-brief — dictée vocale → brief structuré + Notion   |
| `/create`     | Component Factory (skill\|command\|agent)                   |

---

## 5. Subagents (16)

### Core Subagents (7)

| Subagent               | Model | Rôle                       | Invoqué par     |
| ---------------------- | ----- | -------------------------- | --------------- |
| `@plan-validator`      | opus  | Valide plan avant Phase 2  | `/epci` Phase 1 |
| `@code-reviewer`       | opus  | Revue qualité code         | `/epci` Phase 2, `/debug` |
| `@security-auditor`    | opus  | Audit OWASP (conditionnel) | `/epci` Phase 2, `/brainstorm` (si auth/payment) |
| `@qa-reviewer`         | sonnet | Revue tests (conditionnel) | `/epci` Phase 2 |
| `@doc-generator`       | sonnet | Génération documentation   | `/epci` Phase 3 |
| `@decompose-validator` | opus  | Valide décomposition PRD   | `/decompose`    |
| `@rules-validator`     | opus  | Valide .claude/rules/      | `/rules`        |

### Turbo/Quick Subagents (3) — v4.4+

| Subagent        | Model  | Rôle                        | Invoqué par     |
| --------------- | ------ | --------------------------- | --------------- |
| `@clarifier`    | haiku  | Questions clarification rapides | `/brief --turbo`, `/brainstorm --turbo` |
| `@planner`      | sonnet | Planification rapide        | `/epci --turbo` P1, `/quick` [P], `/brainstorm` (converge) |
| `@implementer`  | sonnet | Implémentation TDD rapide   | `/epci --turbo` P2, `/quick` [C] |

### Ralph Subagent (1) — v4.9.2+

| Subagent          | Model  | Rôle                           | Invoqué par     |
| ----------------- | ------ | ------------------------------ | --------------- |
| `@ralph-executor` | sonnet | Exécution story individuelle   | `/ralph` loop   |

### Brainstorm Subagents (5) — v4.8+

| Subagent             | Model | Rôle                          | Invoqué par     |
| -------------------- | ----- | ----------------------------- | --------------- |
| `@ems-evaluator`     | haiku | Calcul EMS 5 axes + weak_axes | `/brainstorm` (chaque itération) |
| `@technique-advisor` | haiku | Auto-sélection techniques     | `/brainstorm` (si axe < 50) |
| `@expert-panel`      | opus  | Panel d'experts multi-perspective | `/brainstorm` v5.0 |
| `@party-orchestrator`| sonnet| Orchestration sessions brainstorm | `/brainstorm` v5.0 |
| `@rule-clarifier`    | haiku | Clarification règles métier   | `/brainstorm` v5.0 |

---

## 6. Skills (30)

### Core (18)

`epci-core`, `architecture-patterns`, `code-conventions`, `testing-strategy`,
`git-workflow`, `flags-system`, `project-memory`, `brainstormer`,
`debugging-strategy`, `learning-optimizer`, `breakpoint-metrics`,
`clarification-intelligente`, `proactive-suggestions`, `rules-generator`,
`input-clarifier`, `orchestrator-batch`, `ralph-analyzer`, `ralph-converter`

### Stack (5) — Auto-détectés

| Skill              | Détection                             |
| ------------------ | ------------------------------------- |
| `php-symfony`      | `composer.json`                       |
| `javascript-react` | `package.json` + react                |
| `frontend-editor`  | Fichiers frontend (CSS, UI)           |
| `python-django`    | `requirements.txt` / `pyproject.toml` |
| `java-springboot`  | `pom.xml` / `build.gradle`            |

### Promptor (1) — Voice-to-Brief

| Skill     | Description                                        |
| --------- | -------------------------------------------------- |
| `promptor`| Transformation dictée vocale → brief + export Notion |

### Personas (1) + MCP (1) + Factory (4)

---

## 7. Personas & MCP

### 6 Personas (auto-activation si score > 0.6)

| Persona      | Focus                     | Flag                  |
| ------------ | ------------------------- | --------------------- |
| 🏗️ Architect | System thinking, patterns | `--persona-architect` |
| 🎨 Frontend  | UI/UX, accessibility      | `--persona-frontend`  |
| ⚙️ Backend   | APIs, data integrity      | `--persona-backend`   |
| 🔒 Security  | OWASP, compliance         | `--persona-security`  |
| 🧪 QA        | Tests, coverage           | `--persona-qa`        |
| 📝 Doc       | Documentation             | `--persona-doc`       |

### 5 MCP Servers

| Server     | Function                  | Flags     |
| ---------- | ------------------------- | --------- |
| Context7   | Documentation librairies  | `--c7`    |
| Sequential | Raisonnement multi-étapes | `--seq`   |
| Magic      | Génération UI (21st.dev)  | `--magic` |
| Playwright | Tests E2E                 | `--play`  |
| Notion     | Export tâches vers Notion | `/promptor` |

**Désactiver tous** : `--no-mcp`

---

## 8. Flags Universels

| Catégorie   | Flags                                           |
| ----------- | ----------------------------------------------- |
| Thinking    | `--think`, `--think-hard`, `--ultrathink`       |
| Compression | `--uc`, `--verbose`                             |
| Workflow    | `--safe`, `--no-hooks`, `--large`, `--continue` |
| Wave        | `--wave`, `--wave-strategy`                     |

**Auto-activation** :

- Fichiers > 10 → `--think-hard`
- Context > 75% → `--uc`
- Fichiers sensibles → `--safe`

---

## 9. Development Guidelines

### Conventions

| Élément   | Convention       | Exemple                |
| --------- | ---------------- | ---------------------- |
| Commandes | kebab-case.md    | `brief.md`             |
| Subagents | kebab-case.md    | `code-reviewer.md`     |
| Skills    | dossier/SKILL.md | `php-symfony/SKILL.md` |
| Scripts   | snake_case.py    | `validate_skill.py`    |

### Limites tokens

| Composant    | Limite        |
| ------------ | ------------- |
| Commandes    | < 5000 tokens |
| Skills       | < 5000 tokens |
| Subagents    | < 2000 tokens |
| Descriptions | ≤ 1024 chars  |

### Validation

```bash
# Valider tout
python src/scripts/validate_all.py

# Valider un composant spécifique
python src/scripts/validate_skill.py src/skills/core/epci-core/
python src/scripts/validate_command.py src/commands/brief.md
python src/scripts/validate_subagent.py src/agents/code-reviewer.md
```

---

## 10. Quick Reference

### Créer un composant

```bash
/epci:create skill mon-skill
/epci:create command ma-commande
/epci:create agent mon-agent
```

### Workflow type

```
1. /epci:brief "description feature"
2. → Routing automatique vers /epci:quick ou /epci:epci
3. → Validation via subagents
4. → Feature Document complété
```

### Documentation détaillée

| Sujet             | Fichier                                                  |
| ----------------- | -------------------------------------------------------- |
| Spec complète v3  | `docs/migration/27-30/epci-v3-complete-specification.md` |
| Component Factory | `docs/migration/27-30/epci-component-factory-spec-v3.md` |
| Best practices    | `docs/Guide_Bonnes_Pratiques_Claude_Code_EPCI.md`        |
| Hooks             | `src/hooks/README.md`                                    |
| Flags             | `src/settings/flags.md`                                  |
| MCP               | `src/skills/mcp/SKILL.md`                                |
| Personas          | `src/skills/personas/SKILL.md`                           |
| Audit Workflow    | `docs/audits/AUDIT_PROMPT.md`                            |

---

## 11. Hooks Obligatoires

### Post-Phase-3 Memory Update

**CRITIQUE** : Ce hook DOIT être exécuté à la fin de `/epci` et `/quick` pour sauvegarder l'historique des features.

```bash
python3 src/hooks/runner.py post-phase-3 --context '{
  "phase": "phase-3",
  "feature_slug": "<slug>",
  "complexity": "<TINY|SMALL|STANDARD|LARGE>",
  "files_modified": ["<files>"],
  "actual_time": "<duration>",
  "commit_status": "<committed|pending>"
}'
```

**Effets** :
- Sauvegarde dans `.project-memory/history/features/`
- Met à jour les métriques de vélocité
- Incrémente le compteur `features_completed`
- Permet la calibration des estimations

### Hooks Actifs par Défaut

| Hook | Type | Fichier |
|------|------|---------|
| Brief logging pre-exploration | pre-brief | `pre-brief.py` |
| Brief completion logging | post-brief | `post-brief.py` |
| Debug session start | pre-debug | `pre-debug.py` |
| Debug session record | post-debug | `post-debug.py` |
| Memory context at breakpoints | on-breakpoint | `on-breakpoint-memory-context.py` |
| Suggestions post-P2 | post-phase-2 | `post-phase-2-suggestions.py` |
| Memory update post-P3 | post-phase-3 | `post-phase-3-memory-update.py` |

**Désactiver** : `--no-hooks`

---

## 12. Audit et Qualité

### Audit Régulier

Exécuter l'audit de cohérence régulièrement :

```bash
# Voir docs/audits/AUDIT_PROMPT.md pour le prompt complet
```

### Score Qualité Cible

| Critère | Objectif |
|---------|----------|
| Cohérence globale | >= 85/100 |
| Documentation sync | >= 95/100 |
| Hooks fonctionnels | 100% |
| Tests passants | 100% |
