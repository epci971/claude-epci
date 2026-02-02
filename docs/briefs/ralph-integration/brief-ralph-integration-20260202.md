# Brief — Ralph Integration v6.1

> **Slug**: `ralph-integration`
> **Date**: 2026-02-02
> **Version**: 1.0
> **Status**: Ready for /spec
> **Complexity**: STANDARD (8-11h estimated)

---

## 1. Contexte

### Problème

Le skill `/spec` actuel (v6.0) génère des specs Markdown et un PRD.json, mais l'intégration avec le système d'exécution autonome Ralph est incomplète:

- Le format `prd.json` utilise `tasks[]` au lieu de `userStories[]` (format v5.6 éprouvé)
- Pas de skill `/ralph-exec` pour l'exécution story par story
- Le script `ralph.sh` généré est basique (pas de boucle autonome, pas de circuit breaker)
- Pas de tracking d'exécution (`execution`, `attempts`, `passes`)

### Objectif

Améliorer `/spec` pour générer un système **ready-to-execute** dès la fin de la génération:
- PRD.json au format `userStories[]` avec tracking execution
- Skill `/ralph-exec` pour exécution autonome par story
- Script `ralph.sh` avec boucle autonome et circuit breaker inline
- Détection de completion via RALPH_STATUS block

### Valeur attendue

- Exécution overnight automatique sans intervention humaine
- Libération contexte entre chaque story (fresh context)
- Détection automatique des boucles infinies et stagnation
- Traçabilité complète (attempts, errors, files modified)

---

## 2. User Stories

### US1 — Format PRD userStories[]

**En tant que** développeur utilisant /spec
**Je veux** un PRD.json au format `userStories[]` avec tracking execution
**Afin de** pouvoir exécuter les stories avec Ralph et suivre leur progression

**Complexité**: M (60min)
**Priorité**: Must-have

**Acceptance Criteria**:
- AC1: Le schema `src/schemas/prd-v2.json` utilise `userStories[]` au lieu de `tasks[]`
- AC2: Chaque story a les champs: `id`, `title`, `category`, `type`, `complexity`, `priority`, `status`, `passes`
- AC3: Chaque story a `acceptanceCriteria[]` avec `{id, description, done}`
- AC4: Chaque story a `tasks[]` avec `{id, description, done}`
- AC5: Chaque story a `dependencies` avec `{depends_on[], blocks[]}`
- AC6: Chaque story a `execution` avec `{attempts, last_error, files_modified[], completed_at, iteration}`
- AC7: Le schema inclut `meta` (branchName, projectName, generatedAt, generatedBy, source)
- AC8: Le schema inclut `config` (max_iterations, test_command, lint_command, granularity)
- AC9: Le schema inclut `metrics` (total_stories, completed, critical_path[])

### US2 — Skill /ralph-exec

**En tant que** script ralph.sh
**Je veux** invoquer un skill `/ralph-exec` pour chaque story
**Afin d'** avoir un contexte frais et des instructions claires par story

**Complexité**: L (120min)
**Priorité**: Must-have

**Acceptance Criteria**:
- AC1: Le skill existe dans `src/skills/ralph-exec/SKILL.md`
- AC2: Le skill a le frontmatter correct (name, description, user-invocable: true, argument-hint)
- AC3: Le skill accepte l'argument `--prd <path>` pour localiser le PRD.json
- AC4: Le skill identifie automatiquement la prochaine story `status: pending` et `passes: false`
- AC5: Le skill respecte l'ordre des dépendances (ne pas exécuter si `depends_on` non complété)
- AC6: Le skill exécute la story en mode TDD (RED-GREEN, pas de REFACTOR pour vitesse)
- AC7: Le skill met à jour le PRD.json après exécution (status, passes, execution.*)
- AC8: Le skill émet un RALPH_STATUS block en fin de réponse
- AC9: Le skill a 3 steps: init, execute, report

### US3 — RALPH_STATUS Block Format

**En tant que** script ralph.sh
**Je veux** parser un block RALPH_STATUS structuré dans la sortie Claude
**Afin de** détecter la completion et décider de continuer ou arrêter

**Complexité**: S (30min)
**Priorité**: Must-have

**Acceptance Criteria**:
- AC1: Le format est documenté dans `src/skills/ralph-exec/references/status-block.md`
- AC2: Le block commence par `---RALPH_STATUS---` et finit par `---END_RALPH_STATUS---`
- AC3: Le block contient: STATUS, STORY_ID, TASKS_COMPLETED_THIS_LOOP, FILES_MODIFIED
- AC4: Le block contient: TESTS_STATUS, WORK_TYPE, EXIT_SIGNAL, RECOMMENDATION
- AC5: STATUS est enum: `IN_PROGRESS | COMPLETE | BLOCKED`
- AC6: EXIT_SIGNAL est boolean: `true | false`
- AC7: Le step-02-report.md du skill /ralph-exec génère ce block

### US4 — Script ralph.sh avec boucle autonome

**En tant que** développeur
**Je veux** un script ralph.sh généré avec boucle autonome complète
**Afin d'** exécuter toutes les stories overnight sans intervention

**Complexité**: M (90min)
**Priorité**: Must-have

**Acceptance Criteria**:
- AC1: Le template existe dans `src/skills/spec/templates/ralph.sh.template`
- AC2: Le script utilise `--dangerously-skip-permissions` pour mode autonome
- AC3: Le script boucle avec `MAX_ITERATIONS` configurable (default 50)
- AC4: Le script appelle `claude "/ralph-exec --prd $PRD_FILE"` pour chaque iteration
- AC5: Le script parse RALPH_STATUS pour décider de continuer/arrêter
- AC6: Le script affiche progression (completed/total, elapsed time)
- AC7: Le script supporte `--quiet`, `--dry-run`, `--help` flags
- AC8: Le script log dans progress.txt avec timestamps

### US5 — Circuit Breaker inline

**En tant que** script ralph.sh
**Je veux** un circuit breaker inline (sans libs externes)
**Afin de** détecter les boucles infinies et stagnation automatiquement

**Complexité**: M (60min)
**Priorité**: Must-have

**Acceptance Criteria**:
- AC1: Le circuit breaker est inline dans ralph.sh (pas de fichiers lib/ séparés)
- AC2: Détection no-progress: arrêt après 3 iterations sans changement de fichiers (state hash)
- AC3: Détection same-error: arrêt après 3 mêmes erreurs consécutives (error hash)
- AC4: Détection max-iterations: arrêt à MAX_ITERATIONS avec message
- AC5: Exit codes: 0=success, 1=max iterations, 2=circuit breaker, 3=blocked
- AC6: Logging des triggers circuit breaker avec timestamp

### US6 — Mise à jour /spec step-03

**En tant que** skill /spec
**Je veux** que step-03-generate-ralph.md génère tous les artifacts Ralph
**Afin que** le système soit ready-to-execute dès la fin de /spec

**Complexité**: M (60min)
**Priorité**: Must-have

**Acceptance Criteria**:
- AC1: Le step génère `docs/specs/{slug}/{slug}.prd.json` au format userStories[]
- AC2: Le step génère `.ralph/{slug}/PROMPT.md` avec contexte stack-aware
- AC3: Le step génère `.ralph/{slug}/MEMORY.md` template
- AC4: Le step génère `.ralph/{slug}/ralph.sh` exécutable (chmod +x)
- AC5: Le step met à jour `.ralph/index.json` avec la nouvelle feature
- AC6: Le step affiche le breakpoint final avec commande d'exécution
- AC7: Le step utilise les templates de `templates/` pour génération

### US7 — Templates génération

**En tant que** skill /spec
**Je veux** des templates pour PRD.json, PROMPT.md, MEMORY.md, ralph.sh
**Afin de** garantir la cohérence et faciliter la maintenance

**Complexité**: M (45min)
**Priorité**: Should-have

**Acceptance Criteria**:
- AC1: Template `templates/prd.json.template` avec placeholders
- AC2: Template `templates/prompt.md.template` avec sections stack-specific
- AC3: Template `templates/memory.md.template` avec structure tracking
- AC4: Template `templates/ralph.sh.template` avec circuit breaker inline
- AC5: Chaque template a des variables clairement documentées ({{variable}})

### US8 — Registry index.json

**En tant que** système Ralph
**Je veux** un registre central `.ralph/index.json`
**Afin de** lister toutes les features Ralph-enabled et leur status

**Complexité**: S (30min)
**Priorité**: Should-have

**Acceptance Criteria**:
- AC1: Le schema existe dans `src/schemas/ralph-index-v1.json`
- AC2: Chaque entry a: slug, title, created_at, status, complexity, stories_count
- AC3: Chaque entry a: spec_path, ralph_path, prd_path
- AC4: Status enum: `ready | running | completed | paused | failed`
- AC5: /spec crée ou met à jour ce fichier automatiquement
- AC6: Pas de doublons par slug (vérification avant ajout)

---

## 3. Contraintes techniques

### Stack

- **Scripts**: Bash (ralph.sh, circuit breaker)
- **Skills**: Markdown (SKILL.md, steps/, references/)
- **Schemas**: JSON Schema draft 2020-12
- **Config**: JSON (prd.json, index.json)

### Architecture

```
src/skills/
├── spec/                          # Existant, à modifier
│   ├── SKILL.md
│   ├── steps/
│   │   └── step-03-generate-ralph.md  # À modifier
│   ├── references/
│   │   └── prd-schema.md              # À modifier
│   └── templates/                      # À créer/compléter
│       ├── prd.json.template
│       ├── prompt.md.template
│       ├── memory.md.template
│       └── ralph.sh.template
│
└── ralph-exec/                    # Nouveau skill
    ├── SKILL.md
    ├── steps/
    │   ├── step-00-init.md
    │   ├── step-01-execute.md
    │   └── step-02-report.md
    └── references/
        └── status-block.md

src/schemas/
├── prd-v2.json                    # À modifier
└── ralph-index-v1.json            # Nouveau
```

### Storage (dual)

```
docs/specs/{slug}/
├── index.md
├── task-XXX.md
└── {slug}.prd.json                # PRD machine-readable

.ralph/{slug}/
├── PROMPT.md                      # Instructions Claude
├── MEMORY.md                      # État exécution
└── ralph.sh                       # Script runner

.ralph/
└── index.json                     # Registre global
```

### Conventions

- PRD IDs: `US-001`, `US-002`, etc.
- AC IDs: `AC1`, `AC2` (locaux par story)
- Task IDs: `T1`, `T2` (locaux par story)
- Status: `pending | in_progress | completed | failed | blocked`
- Granularity: `micro` (15-30min) | `small` (30-60min) | `standard` (1-2h)

---

## 4. Hors scope

- Migration des PRD existants vers le nouveau format
- Interface web pour visualiser la progression
- Intégration avec CI/CD (GitHub Actions)
- Support multi-branch (worktrees parallèles)
- Rollback automatique en cas d'échec

---

## 5. Risques et mitigations

| Risque | Impact | Mitigation |
|--------|--------|------------|
| Circuit breaker trop sensible | Arrêts prématurés | Seuils configurables, logs détaillés |
| RALPH_STATUS mal parsé | Boucle infinie | Fallback heuristique (patterns completion) |
| PRD.json corrompu mid-execution | Perte état | Backup avant chaque update |
| Story dependencies cycles | Blocage | Validation DAG avant exécution |

---

## 6. Métriques de succès

- **Fonctionnel**: Exécution complète d'un PRD de 10 stories overnight
- **Fiabilité**: Circuit breaker déclenché correctement sur stuck loop simulé
- **Traçabilité**: Chaque story a `execution.attempts` et `execution.iteration` remplis
- **Performance**: < 5min overhead par story (parsing, status update)

---

## 7. Dépendances

| Dépendance | Type | Status |
|------------|------|--------|
| Skill `/spec` existant | Interne | ✅ Disponible |
| Schema `prd-v2.json` existant | Interne | ✅ À modifier |
| Claude Code CLI | Externe | ✅ Disponible |
| `--dangerously-skip-permissions` flag | Externe | ✅ Disponible |

---

## 8. Plan de décomposition suggéré

| Task | Stories | Effort | Dépendances |
|------|---------|--------|-------------|
| T1: Schema PRD v2 | US1 | 1h | - |
| T2: Skill /ralph-exec | US2, US3 | 2.5h | T1 |
| T3: Circuit breaker | US5 | 1h | - |
| T4: Script ralph.sh | US4 | 1.5h | T2, T3 |
| T5: Templates | US7 | 45min | T1 |
| T6: Update /spec step-03 | US6 | 1h | T4, T5 |
| T7: Registry index.json | US8 | 30min | T6 |
| T8: Tests E2E | - | 1h | T7 |

**Chemin critique**: T1 → T2 → T4 → T6 → T7 → T8

---

## 9. Commandes suivantes

```bash
# Générer les specs détaillées
/spec ralph-integration @docs/briefs/ralph-integration/brief-ralph-integration-20260202.md

# Exécuter manuellement
/implement ralph-integration

# Ou exécution autonome (après génération)
./.ralph/ralph-integration/ralph.sh
```

---

*Brief généré par /brainstorm — EPCI v6.0*
*EMS atteint: ~75 (Mature)*
