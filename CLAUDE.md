# EPCI Plugin — Claude Code Development Assistant

> **Version** : 4.9 | **Date** : Janvier 2025

---

## 1. Overview

EPCI (Explore → Plan → Code → Inspect) structure le développement en phases avec validation à chaque étape.

### Philosophie v4

| Principe            | Description                                                   |
| ------------------- | ------------------------------------------------------------- |
| **Simplicité**      | 11 commandes spécialisées                                     |
| **Modularité**      | 27 Skills, 15 Subagents, Hooks natifs                         |
| **Traçabilité**     | Feature Document comme fil rouge                              |
| **MCP Integration** | 5 serveurs externes (Context7, Sequential, Magic, Playwright, Notion) |

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
├── agents/           # 12 subagents (7 core + 3 turbo + 2 brainstorm)
├── commands/         # 11 commandes (brief, epci, quick, brainstorm, etc.)
├── hooks/            # Système hooks (runner.py, examples/, active/)
├── mcp/              # MCP Integration (config, activation, registry)
├── orchestration/    # Wave orchestration
├── scripts/          # Validation (validate_all.py, etc.)
├── settings/         # Configuration (flags.md)
└── skills/           # 26 skills
    ├── core/         # 14 skills fondamentaux
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

### Feature Document (STD/LARGE)

```markdown
# Feature Document — [Titre]

## §1 — Brief Fonctionnel ← /brief

## §2 — Plan d'Implémentation ← /epci Phase 1

## §3 — Implementation ← /epci Phases 2-3
```

---

## 4. Commands (11)

| Commande      | Rôle                                                        |
| ------------- | ----------------------------------------------------------- |
| `/brief`      | Point d'entrée unique — exploration, clarification, routing |
| `/epci`       | Workflow complet 3 phases (STD/LARGE)                       |
| `/quick`      | Workflow condensé EPCT (TINY/SMALL)                         |
| `/commit`     | Finalisation git avec contexte EPCI                         |
| `/rules`      | Génère .claude/rules/ — conventions projet automatiques     |
| `/brainstorm` | Feature discovery v4.8 — Auto-techniques, mix, transition checks |
| `/debug`      | Diagnostic bugs structuré                                   |
| `/decompose`  | Décomposition PRD en sous-specs                             |
| `/memory`     | Gestion mémoire projet + learning (calibration, préférences)|
| `/promptor`   | Voice-to-brief — dictée vocale → brief structuré + Notion   |
| `/create`     | Component Factory (skill\|command\|agent)                   |

---

## 5. Subagents (15)

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

### Brainstorm Subagents (5) — v4.8+

| Subagent             | Model | Rôle                          | Invoqué par     |
| -------------------- | ----- | ----------------------------- | --------------- |
| `@ems-evaluator`     | haiku | Calcul EMS 5 axes + weak_axes | `/brainstorm` (chaque itération) |
| `@technique-advisor` | haiku | Auto-sélection techniques     | `/brainstorm` (si axe < 50) |
| `@expert-panel`      | opus  | Panel d'experts multi-perspective | `/brainstorm` v5.0 |
| `@party-orchestrator`| sonnet| Orchestration sessions brainstorm | `/brainstorm` v5.0 |
| `@rule-clarifier`    | haiku | Clarification règles métier   | `/brainstorm` v5.0 |

---

## 6. Skills (27)

### Core (15)

`epci-core`, `architecture-patterns`, `code-conventions`, `testing-strategy`,
`git-workflow`, `flags-system`, `project-memory`, `brainstormer`,
`debugging-strategy`, `learning-optimizer`, `breakpoint-metrics`,
`clarification-intelligente`, `proactive-suggestions`, `rules-generator`,
`input-clarifier`

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
