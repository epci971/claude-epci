# EPCI Plugin — Claude Code Development Assistant

> **Version** : 5.4.1 | **Date** : Janvier 2025

---

## 1. Overview

EPCI (Explore → Plan → Code → Inspect) structure le développement en phases avec validation à chaque étape.

### Philosophie v4

| Principe            | Description                                                   |
| ------------------- | ------------------------------------------------------------- |
| **Simplicité**      | 14 commandes spécialisées                                     |
| **Modularité**      | 35 Skills, 16 Subagents, Hooks natifs                         |
| **Traçabilité**     | Feature Document comme fil rouge                              |
| **MCP Integration** | 5 serveurs externes (Context7, Sequential, Magic, Playwright, Notion) |

### Nouveautés v5.4.0 (Perplexity Research Integration)

- **Nouveau skill `perplexity-research`** : Recherche externe via Perplexity Pro (human-in-the-loop)
- **Nouveau type breakpoint `research-prompt`** : Affiche prompt copyable avec mode Standard/Deep Research
- **Intégration `/brief`** : Step 2.1 propose recherche si librairie externe ou architecture complexe
- **Intégration `/debug`** : Step 1.2.1 propose recherche si Context7/WebSearch insuffisants
- **Intégration `/brainstorm`** : Phase 1 (market analysis) + Phase 2 (axes faibles)
- **35 Skills** : Total passe de 34 à 35 skills
- **10 types breakpoints** : Ajout de `research-prompt` au système breakpoint-display

### Nouveautés v5.3.10 (Anti-Plan-Natif Fix)

- **Fix critique `/brief`** : Correction du bug où `/brief` basculait en mode plan natif au lieu de générer un Feature Document
- **Garde anti-plan-natif** : Nouvelle box ASCII de vérification obligatoire dans Step 5 de `/brief`
- **Règle globale CLAUDE.md** : Protection anti-EnterPlanMode ajoutée dans `~/.claude/CLAUDE.md`
- **Routing restauré** : Step 6 (routing vers `/quick` ou `/epci`) s'exécute correctement après Step 5

### Nouveautés v5.3.8 (Skills Integration & Default Suggestions)

- **Intégration `complexity-calculator`** : Calcul complexité centralisé intégré dans `/brief`, `/quick`, `/decompose`, `/ralph-exec`
- **Intégration `tdd-workflow`** : Cycle TDD standardisé intégré dans `/epci`, `/quick`, `/ralph-exec`
- **Suggestions proactives par défaut** : `/brainstorm` affiche maintenant les suggestions automatiquement
- **Nouveau flag `--no-suggest`** : Remplace `--suggest` pour désactiver les suggestions (par défaut activées)
- **Références skills unifiées** : Toutes les commandes référencent les skills via `@skill:` invocations
- **Documentation enrichie** : Exemples d'invocation skill dans chaque commande

### Nouveautés v5.3.7 (Discovery Mode & New Skills)

- **Discovery Mode pour /brainstorm** : Flag `--suggest` pour suggestions proactives (maintenant par défaut en v5.3.8)
- **12 patterns discovery** : Catalogue de suggestions contextuelles (arch, security, ems-based)
- **Champ `suggestions[]`** : Nouveau champ dans breakpoint-display pour suggestions
- **Nouveau skill `complexity-calculator`** : Calcul centralisé complexité TINY/SMALL/STANDARD/LARGE
- **Nouveau skill `tdd-workflow`** : Cycle TDD standardisé RED-GREEN-REFACTOR-VERIFY
- **Documentation clarifiée** : `input-clarifier` vs `clarification-intelligente` mieux documentés
- **34 Skills** : Total passe de 32 à 34 skills

### Nouveautés v5.3.6 (Full Breakpoint Migration)

- **Migration complète breakpoint-display** : Toutes les commandes EPCI utilisent maintenant le skill centralisé
- **6 commandes migrées** : `/debug`, `/decompose`, `/orchestrate`, `/commit`, `/save-plan`, `/quick`
- **12 breakpoints au total** : Tous migrés vers `@skill:breakpoint-display`
- **~70% économie tokens moyenne** : Breakpoints uniformisés via skill centralisé
- **Cohérence UI totale** : Toutes les commandes EPCI avec boutons natifs AskUserQuestion

### Nouveautés v5.3.5 (Brainstorm Migration)

- **Migration `/brainstorm` vers `breakpoint-display`** : 6 breakpoints migrés vers skill centralisé
- **Nouveau template `ems-status`** : Affichage EMS 5 axes avec barres de progression pour brainstorm
- **9 types de breakpoints** : validation, plan-review, analysis, decomposition, diagnostic, interactive-plan, lightweight, info-only, ems-status
- **~57% économie tokens** : Breakpoints brainstorm via skill au lieu de ASCII boxes manuelles
- **Cohérence UI complète** : `/brief`, `/epci` et `/brainstorm` utilisent maintenant le même système

### Nouveautés v5.3.4 (Breakpoint Display Skill)

- **Nouveau skill `breakpoint-display`** : Système unifié pour affichage breakpoints interactifs
- **73% réduction tokens** : ~300 tokens/breakpoint → ~80 tokens via skill centralisé
- **AskUserQuestion natif** : UI Claude Code native avec boutons cliquables vs choix textuels
- **8 types de breakpoints** : validation, plan-review, analysis, decomposition, diagnostic, interactive-plan, lightweight, info-only
- **4 composants réutilisables** : metrics-block, validations-block, preview-block, flags-block
- **Migration /brief et /epci** : 4 breakpoints migrés vers nouveau système (Step 1, Step 4, BP1, BP2)
- **Guides complets** : AskUserQuestion integration guide + migration guide pour 9 commandes
- **32 Skills** : Total des skills EPCI passe de 31 à 32

### Nouveautés v5.3.0 (Save Plan)

- **Nouvelle commande `/save-plan`** : Sauvegarde les plans natifs Claude Code dans le projet
- **Auto-détection du plan** : Détecte automatiquement le dernier plan dans `~/.claude/plans/`
- **Auto-génération du slug** : Génère un slug intelligent basé sur le contenu du plan
- **Horodatage complet** : Format `<slug>-<YYYYMMDD-HHmmss>.md` pour éviter les collisions
- **Frontmatter YAML** : Métadonnées ajoutées (saved_at, source, slug, auto_detected)
- **Breakpoint de confirmation** : Validation du slug avant sauvegarde
- **14 commandes** : Total des commandes EPCI passe de 13 à 14

### Nouveautés v5.2.0 (Ralph Simplification)

- **Suppression `/ralph` et `/cancel-ralph`** : Remplacés par workflow plus simple
- **Nouvelle commande `/ralph-exec`** : Exécute UNE story avec EPCT inline (sans routing vers /brief ou /epci)
- **Suppression `@ralph-executor`** : Logique migrée dans `/ralph-exec`
- **Libération contexte** : Chaque appel `claude "/ralph-exec"` = contexte frais
- **Promise tag simplifié** : `<promise>STORY_DONE</promise>` pour détection complétion
- **ralph.sh mis à jour** : Appelle `/ralph-exec` au lieu de PROMPT.md
- **Workflow overnight simplifié** : `./ralph.sh` directement depuis terminal

**Architecture simplifiée** :
```
/decompose → prd.json + ralph.sh
                    │
                    ↓
            ./ralph.sh (terminal)
                    │
          ┌─────────┴─────────┐
          ▼                   ▼
  claude "/ralph-exec"  claude "/ralph-exec"
   (contexte frais)      (contexte frais)
```

### Nouveautés v5.1.2 (Auto Backlog Generation)

- **Génération automatique backlog.md** : `/decompose` génère maintenant automatiquement le backlog table
- **Génération automatique prd.json** : Plus besoin de flag, toujours généré
- **Deux niveaux de granularité** : Sub-specs (1-5 jours) + Stories (1-2h) dans backlog

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
├── agents/           # 16 subagents (7 core + 3 turbo + 5 brainstorm + 1 setup)
├── commands/         # 14 commandes (brief, epci, quick, ralph-exec, etc.)
├── hooks/            # Système hooks (runner.py, examples/, active/)
├── mcp/              # MCP Integration (config, activation, registry)
├── orchestration/    # Wave orchestration
├── scripts/          # Validation (validate_all.py, etc.)
├── settings/         # Configuration (flags.md)
└── skills/           # 34 skills
    ├── core/         # 21 skills fondamentaux (inclut complexity-calculator, tdd-workflow)
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

Workflow simplifié pour exécution autonome sur plusieurs heures sans supervision :

```
PRD complet → /decompose → backlog.md + prd.json + ralph.sh (auto)
                                          │
                                          ↓
                              ./ralph.sh (depuis terminal)
                                          │
                              ┌───────────┴───────────┐
                              ▼                       ▼
                    claude "/ralph-exec"    claude "/ralph-exec"
                     (contexte frais)        (contexte frais)
                              │                       │
                              └───────────┬───────────┘
                                          ↓
                              <promise>STORY_DONE</promise>
                                   ou FAILED
```

**Principe clé** : Chaque `claude "/ralph-exec"` = contexte frais (libération mémoire).

**Commandes** :

```bash
# Workflow G : Ralph Wiggum (overnight)
/decompose migration-prd.md --granularity small
# → Génère automatiquement :
#   - Sub-specs S01-SNN.md (1-5 jours chacune)
#   - backlog.md (stories 1-2h, format Architector)
#   - prd.json (format Ralph v2)
#   - ralph.sh (appelle /ralph-exec)
#   - progress.txt (logging)

# Exécuter directement depuis le terminal
cd docs/specs/migration/
./ralph.sh
# → Boucle sur chaque story
# → Contexte frais à chaque appel
# → Commits automatiques par story

# Pour annuler : Ctrl+C dans le terminal
```

**Avantages du workflow simplifié** :
- ✅ Libération contexte à chaque story
- ✅ Architecture ultra-simple (1 commande au lieu de 3)
- ✅ Pas de routing vers /brief ou /epci
- ✅ Commits atomiques par story complétée
- ✅ Sessions overnight longues sans erreur mémoire

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
| `/ralph-exec` | **Exécute UNE story avec EPCT inline — appelé par ralph.sh** |
| `/orchestrate`| Exécution batch de specs — DAG, priorité                    |
| `/commit`     | Finalisation git avec contexte EPCI                         |
| `/rules`      | Génère .claude/rules/ — conventions projet automatiques     |
| `/brainstorm` | Feature discovery v5.3.8 — Suggestions proactives par défaut, `--no-suggest` pour désactiver |
| `/debug`      | Diagnostic bugs structuré                                   |
| `/decompose`  | Décomposition PRD en sous-specs + backlog.md + prd.json + ralph.sh |
| `/memory`     | Gestion mémoire projet + learning (calibration, préférences)|
| `/promptor`   | Voice-to-brief — dictée vocale → brief structuré + Notion   |
| `/create`     | Component Factory (skill\|command\|agent)                   |
| `/save-plan`  | Sauvegarde plans natifs → docs/plans/ avec slug auto-généré |

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
| `@planner`      | sonnet | Planification rapide        | `/epci --turbo` P1, `/quick` [P], `/brainstorm` (converge), `/ralph-exec` (M/L) |
| `@implementer`  | sonnet | Implémentation TDD rapide   | `/epci --turbo` P2, `/quick` [C], `/ralph-exec` (M/L) |

### Brainstorm Subagents (5) — v4.8+

| Subagent             | Model | Rôle                          | Invoqué par     |
| -------------------- | ----- | ----------------------------- | --------------- |
| `@ems-evaluator`     | haiku | Calcul EMS 5 axes + weak_axes | `/brainstorm` (chaque itération) |
| `@technique-advisor` | haiku | Auto-sélection techniques     | `/brainstorm` (si axe < 50) |
| `@expert-panel`      | opus  | Panel d'experts multi-perspective | `/brainstorm` v5.0 |
| `@party-orchestrator`| sonnet| Orchestration sessions brainstorm | `/brainstorm` v5.0 |
| `@rule-clarifier`    | haiku | Clarification règles métier   | `/brainstorm` v5.0 |

### Utility Subagents (1) — v5.2.0+

| Subagent             | Model | Rôle                          | Invoqué par     |
| -------------------- | ----- | ----------------------------- | --------------- |
| `@statusline-setup`  | haiku | Configure ccusage statusline  | Manuel, `/brief` (si slug statusline) |

---

## 6. Skills (35)

### Core (23)

`epci-core`, `architecture-patterns`, `code-conventions`, `testing-strategy`,
`git-workflow`, `flags-system`, `project-memory`, `brainstormer`,
`debugging-strategy`, `learning-optimizer`, `breakpoint-metrics`,
`clarification-intelligente`, `proactive-suggestions`, `rules-generator`,
`input-clarifier`, `orchestrator-batch`, `ralph-analyzer`, `ralph-converter`,
`breakpoint-display`, `complexity-calculator`, `tdd-workflow`,
`perplexity-research`, `command-auditor`

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

### Références et invocations

#### Règle du préfixe `src/` (v5.4.1)

**RÈGLE CRITIQUE** : Ne JAMAIS utiliser le préfixe `src/` dans les références internes entre commandes, skills et agents.

```markdown
# ❌ INCORRECT — préfixe src/ redondant
Voir @src/skills/core/tdd-workflow/SKILL.md
Consulter src/commands/references/brief/turbo-mode.md

# ✅ CORRECT — référence relative sans src/
Voir documentation du skill `tdd-workflow`
Consulter @references/brief/turbo-mode.md
```

**Pourquoi** : Les fichiers du plugin sont déjà dans `src/`, le préfixe est donc redondant et crée de la confusion.

**Exception unique** : Le chemin complet avec `src/` est accepté UNIQUEMENT pour les instructions Read tool qui doivent lire un fichier physique.

#### Convention de référencement des Skills (v5.4.1)

| Usage | Pattern | Exemple |
|-------|---------|---------|
| **Invoquer** un skill | `@skill:{name}` (YAML block) | `@skill:breakpoint-display` |
| **Documenter** un skill | Mention textuelle | `Voir documentation du skill \`tdd-workflow\`` |
| **Référencer** une doc locale | `@references/...` | `@references/brief/turbo-mode.md` |
| **Lire** un template (Read tool) | Chemin complet | `Read src/skills/core/rules-generator/templates/...` |

**Invocation skill (format YAML) :**
```yaml
@skill:breakpoint-display
  type: validation
  title: "..."
  data: {...}
  ask: {...}
```

**Référence documentaire (texte) :**
```markdown
> Voir documentation du skill `complexity-calculator` pour la formule complète.
```

**Anti-patterns à éviter :**

| ❌ Incorrect | ✅ Correct |
|--------------|------------|
| `@src/skills/core/tdd-workflow/SKILL.md` | `skill \`tdd-workflow\`` |
| `src/skills/mcp/SKILL.md` | `skill \`mcp\`` |
| `Voir @src/skills/...` | `Voir documentation du skill \`...\`` |

**Exception** : Les chemins physiques sont acceptés pour les instructions Read tool (templates à lire).

#### Références de fichiers locaux

Pour référencer un fichier de documentation locale (pas un skill) :

| Correct | Incorrect |
|---------|-----------|
| `@references/brainstorm/commands.md` | `src/commands/references/brainstorm/commands.md` |
| `@references/epci/phase-1-planning.md` | `@src/commands/references/epci/...` |
| `@docs/architecture.md` | Chemin absolu avec src/ |

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

---

## 13. Worktree Integration (v5.2.2+)

### Concept

Les Git worktrees permettent de développer plusieurs features en parallèle avec isolation totale. EPCI intègre ce workflow pour les features STANDARD et LARGE.

### Scripts disponibles

| Script | Rôle | Usage |
|--------|------|-------|
| `worktree-create.sh` | Crée worktree + branche + copie .env | `./src/scripts/worktree-create.sh <feature-slug>` |
| `worktree-finalize.sh` | Merge + cleanup | `./src/scripts/worktree-finalize.sh` |
| `worktree-abort.sh` | Abandon propre | `./src/scripts/worktree-abort.sh` |

### Workflow intégré

```
/brief (STANDARD/LARGE) → Suggestion worktree
           ↓
   worktree-create.sh feature-slug
           ↓
   cd ../projet-feature-slug
           ↓
   /epci feature-slug (dans worktree)
           ↓
   worktree-finalize.sh (merge vers main)
```

### Règles importantes

- **Isolation** : Chaque worktree = branche séparée, fichiers séparés
- **Copie .env** : Le script copie automatiquement les fichiers d'environnement
- **Préfixe branche** : `feature/<slug>` créé automatiquement
- **Cleanup** : `worktree-finalize.sh` supprime le worktree après merge

**Documentation complète** : `docs/guidelines/worktrees.md`

---

## 14. Conventions de Développement Avancées

### Versioning (Convention de bump)

Format : `5.x.y` (majeur.mineur.patch)

**Fichiers à mettre à jour simultanément** :

| Fichier | Champ |
|---------|-------|
| `CLAUDE.md` | Header `Version : 5.x.y` |
| `src/.claude-plugin/plugin.json` | `"version"` |
| `build/epci/.claude-plugin/plugin.json` | `"version"` |

**Règle** : Toujours bumper les 3 fichiers ensemble dans le même commit.

### MANDATORY EXECUTION pour Skills

Certains skills (comme `breakpoint-display`) ont une section `MANDATORY EXECUTION` qui DOIT être exécutée automatiquement.

**Workflow obligatoire** :

```yaml
# Quand tu rencontres @skill:<name> :
1. LIRE src/skills/core/<name>/SKILL.md
2. TROUVER section "MANDATORY EXECUTION"
3. EXECUTER les instructions de cette section
4. ATTENDRE la réponse utilisateur si AskUserQuestion requis
```

**Skills avec MANDATORY EXECUTION** :

| Skill | Usage |
|-------|-------|
| `breakpoint-display` | Affichage breakpoints interactifs ASCII |
| `complexity-calculator` | Calcul catégorie TINY/SMALL/STANDARD/LARGE |
| `tdd-workflow` | Cycle TDD RED-GREEN-REFACTOR-VERIFY |

### Préfixe `epci:` dans les scripts automatisés

**Règle** : Dans les scripts shell (ralph.sh, etc.), utiliser le préfixe `epci:` pour les commandes :

```bash
# ✅ Correct (dans scripts)
claude "/epci:ralph-exec"

# ❌ Incorrect
claude "/ralph-exec"
```

**Raison** : Le préfixe garantit le namespace du plugin et évite les collisions.

### Scopes de commit enrichis

| Scope | Usage | Exemple |
|-------|-------|---------|
| `(skills)` | Modification de skills | `feat(skills): add perplexity-research` |
| `(commands)` | Modification de commandes | `fix(commands): brief routing` |
| `(infra)` | Scripts, worktree, CI | `feat(infra): add worktree-create.sh` |
| `(ralph)` | Système Ralph Wiggum | `feat(ralph): verbose mode` |
| `(decompose)` | Décomposition PRD | `fix(decompose): backlog format` |
| `(agents)` | Subagents | `feat(agents): add rule-clarifier` |
| `(hooks)` | Système hooks | `fix(hooks): post-phase-3 memory` |
