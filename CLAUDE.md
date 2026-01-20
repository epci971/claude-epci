# EPCI Plugin — Claude Code Development Assistant

> **Version** : 5.6.0 | **Date** : Janvier 2025

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

### Nouveautés v5.6.0

> Voir [CHANGELOG.md](CHANGELOG.md) pour l'historique complet des versions.

**Highlights :**
- **Skip [E][P] pour /quick avec plan natif** : Détection automatique → exécution directe [C][T]
- **Extraction tâches intelligente** : Supporte checkboxes, listes, headers, bullets
- **SMALL par défaut** : Plan natif implique complexité minimale → Sonnet
- **Workflow simplifié** : `/quick @docs/plans/...` = exécution immédiate

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

### Workflow avec Plan Natif (v5.6.0+)

**Plus besoin de flag** — détection automatique basée sur `docs/plans/`.
**Nouveau v5.6.0** : `/quick` skip [E][P] pour exécution accélérée.

```
Plan Natif Claude Code → /save-plan → /brief @docs/plans/... (AUTO-DETECTION)
                                             ↓
                                    ┌────────┴────────┐
                                    ▼                 ▼
                              TINY/SMALL          STD/LARGE
                                    ↓                 ↓
                    /quick @docs/plans/...    /epci slug @docs/plans/...
                                    ↓                 ↓
                         Skip [E][P] (v5.6+)    §2 intègre plan
                                    ↓                 ↓
                           [C][T] direct       Phase 1-3 standard
```

**Algorithme de détection** (unifié entre commandes) :

```python
def is_native_plan(file_path):
    if "docs/plans/" in file_path:
        return True
    frontmatter = parse_yaml_frontmatter(read_file(file_path))
    if frontmatter and "saved_at" in frontmatter:
        return True
    return False
```

**Commandes** :

```bash
# Workflow A : Standard (recommandé)
/brief "description feature"
# → Crée Feature Document avec §1
/epci feature-slug
# → Phase 1-3 complètes

# Workflow B : Via /brief avec plan natif (AUTO-DETECTION)
<mode plan natif Claude Code>
# → ~/.claude/plans/random-name.md
/save-plan
# → docs/plans/auth-oauth-20260120-143052.md
/brief @docs/plans/auth-oauth-20260120-143052.md
# → Détecte plan natif automatiquement
# → Route vers /quick ou /epci avec contexte @path

# Workflow C : Direct /epci avec plan natif
/epci auth-oauth @docs/plans/auth-oauth-20260120-143052.md
# → Auto-détecte plan natif (chemin docs/plans/)
# → Intègre en §2 automatiquement
# → Phase 1 raffine le plan natif

# Workflow D : Direct /quick pour petits scopes (Fast Path v5.6.0+)
/quick "small fix" @docs/plans/fix-20260120.md
# → Auto-détecte plan natif (chemin docs/plans/)
# → Skip [E][P] — tâches extraites du plan
# → Phase [C] avec Sonnet (SMALL par défaut)
# → Phase [T] validation
```

> **Note v5.6.0** : Quand un plan natif est fourni à `/quick`, les phases [E] et [P] sont automatiquement sautées car l'exploration et la planification sont déjà faites.

**Avantages** :
- ✅ Plus de flag à retenir — détection automatique
- ✅ Plan natif archivé dans git (`docs/plans/`)
- ✅ Skip intelligent [E][P] pour exécution accélérée
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

**Emplacement**: `docs/features/<slug>-<YYYYMMDD-HHmmss>.md`

```markdown
# Feature Document — [Titre]

## §1 — Brief Fonctionnel ← /brief

## §2 — Plan d'Implémentation ← /epci Phase 1

## §3 — Implementation ← /epci Phases 2-3
```

> **Note**: Le format de nommage avec horodatage (`<YYYYMMDD-HHmmss>`) est cohérent avec `/save-plan` et évite les collisions de fichiers.

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
1. LOCALISER le skill dans le projet :
   - Repo dev : src/skills/core/<name>/SKILL.md
   - Plugin installé : skills/core/<name>/SKILL.md
2. LIRE le fichier SKILL.md avec Read tool
3. TROUVER section "MANDATORY EXECUTION"
4. SI le skill référence des templates (ex: references/...) :
   → LIRE le fichier template avec Read tool (dans le même dossier que SKILL.md)
5. EXECUTER les instructions de la section MANDATORY EXECUTION
6. ATTENDRE la réponse utilisateur si AskUserQuestion requis
```

**Exemple concret pour `breakpoint-display`** (repo dev) :

```yaml
# Quand tu vois @skill:breakpoint-display type: analysis :
1. Read("src/skills/core/breakpoint-display/SKILL.md")
2. Trouver section "MANDATORY EXECUTION"
3. Read("src/skills/core/breakpoint-display/references/execution-templates.md")
4. Trouver section "Template: analysis"
5. Afficher la boîte ASCII selon le template (avec ┌───┐ └───┘)
6. Invoquer AskUserQuestion avec les options définies dans ask:
7. Attendre la réponse
```

**Note** : Dans le plugin installé, remplacer `src/skills/` par `skills/`.

**IMPORTANT** : Les breakpoints DOIVENT utiliser des boîtes ASCII (`┌───┐` `└───┘`), PAS des tableaux markdown simples.

**Skills avec MANDATORY EXECUTION** :

| Skill | Usage | Fichier templates (relatif au skill) |
|-------|-------|--------------------------------------|
| `breakpoint-display` | Breakpoints interactifs ASCII | `references/execution-templates.md` |
| `complexity-calculator` | Calcul catégorie TINY/SMALL/STANDARD/LARGE | Inline dans SKILL.md |
| `tdd-workflow` | Cycle TDD RED-GREEN-REFACTOR-VERIFY | Inline dans SKILL.md |

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
