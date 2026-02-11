# Pipeline Orchestration — SPEC-02 + SPEC-03 + SPEC-04

> Genere le 2026-02-11 - 4 iterations - Template: feature - EMS final: 76/100

---

## 1. Contexte et Objectif

Le pipeline de developpement semi-automatise ClawdBot transforme un backlog Notion en Pull Requests GitHub, sans intervention humaine pendant l'execution. Le skill `implement-auto` (SPEC-01) est implemente et operationnel. Il manque la couche d'orchestration : les scripts qui lancent les taches (SPEC-02), la base Notion qui les alimente (SPEC-03), et les notifications qui informent (SPEC-04).

**Question/probleme initial**:
> Mettre en place les specs pour la partie orchestration du pipeline ClawdBot (Notion + Claude Code + GitHub), sachant que implement-auto est deja fait.

**Perimetre**:
- IN: `pipeline-runner.sh`, `run-task.sh`, `quota-checker.sh`, schema Notion "OpenClawTasks", Notion API (query/update), bot Telegram (notifications + kill switch), config multi-projet, securite secrets, dependances inter-taches (relation Notion), auto-merge PRs (3 niveaux), sync automatique spec→Notion
- OUT: Skill implement-auto (fait), dashboard web, parallelisme (V2), commandes Telegram avancees (/status, /pause, /resume)

**Criteres de succes definis**:
1. Les 3 specs sont suffisamment detaillees pour etre implementees via `/implement`
2. Les interfaces entre SPEC-02/03/04 sont clairement definies (contrats JSON, mapping API)
3. Les 10 gaps identifies dans le premortem (G1-G10) sont tous adresses
4. Chaque composant est testable isolement (dry-run mode)

---

## 2. Synthese Executive

Le pipeline se decompose en 3 specs complementaires : l'orchestrateur Bash (SPEC-02) qui coordonne l'ensemble, le schema Notion (SPEC-03) qui sert de source de verite, et les notifications Telegram (SPEC-04) qui assurent l'observabilite. L'architecture est intentionnellement simple : Bash + jq + curl, pas de Python, pas de framework, pas de base de donnees locale.

**Insight cle**: **L'approche hybride Notion body + Git optionnel centralise les specs dans Notion par defaut (pas de limite de taille sur le contenu de page) tout en preservant la possibilite d'utiliser des fichiers Git pour les cas complexes. Le systeme de dependances + auto-merge 3 niveaux transforme le pipeline d'un systeme "execute et attends" en une chaine de traitement quasi-autonome.**

**Decisions principales**:
1. Specs dans Notion page body par defaut, fichier Git optionnel (si `Spec Path` renseigne) (D1 revisee)
2. API Notion en curl/jq pur (pas de MCP, pas de dependance Claude Code pour les queries)
3. Dependances inter-taches via relation Notion "Bloque par" (D9)
4. Auto-merge 3 niveaux : dependances Notion + `gh pr merge --auto` + label `pipeline-safe` pour PRs simples (D10+D11)
5. Sync direct spec→Notion : `/spec` cree les pages dans la DB Notion via API apres generation des fichiers (D12)

**Routing recommande**: STANDARD → `/spec` puis `/implement` (3 composants a implementer sequentiellement)

---

## 3. Personas et Scenarios d'Usage

### 3.1 Persona Principal: Edouard (Operateur Pipeline)

| Attribut | Description |
|----------|-------------|
| Role | Auto-entrepreneur fullstack, seul operateur du pipeline |
| Objectif | Multiplier le throughput dev par 3-5x via execution automatisee |
| Frustration actuelle | 30+ taches pre-qualifiees qui prennent 2-3 jours manuellement |
| Niveau technique | Expert (gere le VPS, Claude Code, Notion, GitHub) |
| Contexte d'usage | VPS Linux, pipeline tourne le weekend/nuit, review lundi matin |

**Scenario d'usage typique**:
> Edouard qualifie 20 taches dans Notion le vendredi soir, chacune avec un lien vers un fichier spec dans le repo. Il lance le pipeline (ou il est deja programme en cron). Le samedi matin, il recoit des notifications Telegram au fil des taches traitees. Le lundi matin, il ouvre Notion, voit 15 taches "En review" avec des liens vers les PRs GitHub, et 5 "Echouees" avec les messages d'erreur. Il review les PRs une par une, merge celles qui sont OK, et requalifie les taches echouees pour un prochain run.

### 3.2 Persona Secondaire: Pipeline (Systeme Automatise)

| Attribut | Description |
|----------|-------------|
| Role | Orchestrateur cron qui execute les taches sans intervention |
| Objectif | Traiter le maximum de taches dans la fenetre de quota disponible |
| Contrainte | Quota Claude Max 5x, pas d'interaction possible |
| Comportement | Sequentiel, defensif (circuit breaker, health check, cleanup) |

---

## 4. Analyse et Conclusions Cles

### 4.1 Notion comme source de verite (hybride)

La decision revisee (D1r) etablit Notion comme source de contenu par defaut. Le body d'une page Notion n'a pas de limite pratique de taille (contrairement aux proprietes rich_text limitees a 2000 chars/block). Edouard ecrit deja des documents de 70+ pages dans Notion. L'option Git reste disponible pour les specs qui beneficient du versioning ou du diffing.

**Lecture hybride** : `run-task.sh` lit d'abord la propriete `Spec Path`. Si elle est renseignee et pointe vers un fichier existant, il lit le fichier Git. Sinon, il lit le body de la page Notion via `GET /v1/blocks/{page_id}/children` et convertit les blocks en Markdown.

**Implications pour l'implementation**:
- Propriete `Spec Path` (text) = optionnelle. Si vide, le body Notion fait foi
- Fonction `extract_spec_content()` dans `run-task.sh` gere les 2 sources
- API Notion blocks : pagination via `next_cursor` si > 100 blocks
- Conversion blocks→Markdown : paragraph, heading_1/2/3, bulleted/numbered_list_item, code, divider
- L'export brainstorm→Notion = ecrire le contenu dans le body de la page Notion

**Schema de la DB "OpenClawTasks" (16 proprietes)** :

| Propriete | Type Notion | Rempli par | Notes |
|-----------|-------------|------------|-------|
| Name | title | /spec (sync) | Titre de la tache |
| Spec Path | text | /spec (optionnel) | Chemin fichier Git si spec hors Notion |
| Projet | relation | /spec (sync) | Relation vers la table "Projets" existante |
| Priorite | select | /spec (sync) | P0, P1, P2, P3 |
| Complexite | select | /spec (sync) | Simple, Moyenne, Complexe |
| Statut | select | Pipeline (auto) | A faire, Bloque, En cours, En review, En review (partiel), Echoue, Termine |
| Bloque par | relation (self) | /spec (sync) | Relation vers d'autres taches de la meme DB |
| Branch | text | Pipeline (auto) | feature/{slug} |
| PR URL | url | Pipeline (auto) | Lien PR GitHub |
| Cout tokens | number | Pipeline (auto) | Tokens consommes |
| Duree | number | Pipeline (auto) | Secondes d'execution |
| Flags | multi_select | /spec ou manuel | validate_plan, with_review, no_auto_merge |
| Erreurs | text | Pipeline (auto) | Dernier message d'erreur |
| Demarre le | date | Pipeline (auto) | Timestamp debut execution |
| Termine le | date | Pipeline (auto) | Timestamp fin |
| Auto-merged | checkbox | Pipeline (auto) | True si PR auto-mergee |

### 4.2 Quota management pragmatique

Le quota Claude Max n'a pas d'API de consultation. La strategie V1 est purement reactive :
- Detecter le throttle dans les logs Claude Code (pattern `rate_limit`, `429`, `too_many_requests`)
- Appliquer un cooldown de 30 minutes apres detection
- Arreter le cycle et attendre le prochain declenchement cron

Le tracking proactif (M1 du BRIEF) est reporte apres calibration avec des donnees reelles. Les seuils speculatifs (27 sessions/fenetre, 3 sessions/tache) seront valides ou ajustes apres les premiers runs.

**Implications pour l'implementation**:
- `quota-checker.sh` est plus simple que prevu (grep logs + cooldown timer)
- Les seuils seront ajoutes dans une V1.1 apres les premiers weekends de production

### 4.3 Notifications minimalistes mais suffisantes

Telegram en mode basique : notifications par tache + kill switch. Pas de commandes /status ni /pause. Le kill switch fonctionne sans daemon : le pipeline verifie les messages Telegram recents (getUpdates) en debut de chaque cycle cron.

**Implications pour l'implementation**:
- `notify.sh` = wrapper autour de `curl` vers Telegram sendMessage
- Le kill switch est integre dans `pipeline-runner.sh` (pas un service separe)
- Delai de reaction du kill switch = intervalle cron (max 30 min)

### 4.4 Securite et gestion des secrets

Tous les tokens (Notion, GitHub, Telegram) sont dans un fichier `.env` avec permissions 600 sur le VPS. Le health check en debut de cycle verifie la validite de chaque token avant de commencer. La session Claude Code est la plus fragile (peut expirer), d'ou le auth check dedié.

**Implications pour l'implementation**:
- Fonction `health_check_tokens()` dans `pipeline-runner.sh`
- Notification immediate si un token est invalide
- Documentation de la procedure de renouvellement des tokens

### 4.5 Configuration multi-projet

Un fichier `projects.json` mappe chaque projet a son repertoire local, son repo GitHub, son page ID Notion (dans la table "Projets"), et ses parametres par defaut (modele, flags, timeout). Ajouter un projet = ajouter une entree JSON avec le `notion_project_id` de la fiche projet existante.

### 4.6 Dependances inter-taches

Le pipeline gere les dependances via une relation "Bloque par" (self-relation dans la meme DB Notion). Quand une tache A bloque une tache B, le pipeline ignore B tant que A n'est pas "Termine". Le deblocage est naturel : au cycle cron suivant, la tache B est re-evaluee. Si A est "Termine" (PR mergee), B est executee normalement.

**Implications pour l'implementation**:
- `notion_query` enrichit chaque tache avec le statut de ses dependances
- `filter_blocked_tasks()` filtre les taches dont les dependances ne sont pas toutes "Termine"
- Le statut "Bloque" dans Notion est informatif (mis a jour par le pipeline pour visibilite)

### 4.7 Auto-merge a 3 niveaux

Le systeme d'auto-merge opere en 3 niveaux complementaires :

| Niveau | Mecanisme | Quand | Prerequis |
|--------|-----------|-------|-----------|
| 1 — Dependances | Relation "Bloque par" dans Notion | Toujours | Schema Notion avec relation self |
| 2 — GitHub auto-merge | `gh pr merge --auto --squash` | Apres creation PR (sauf flag `no_auto_merge`) | Settings repo: Allow auto-merge ON |
| 3 — PRs "safe" | Label `pipeline-safe` + GitHub Action auto-approve | Si tache Simple + SUCCESS + tests pass + 0 erreur + <=2 warnings | GitHub Action + Allow Actions to approve PRs |

**Cycle complet** :
1. Pipeline execute tache non-bloquee → cree PR → active auto-merge (niveau 2)
2. Si PR safe → label `pipeline-safe` → GitHub Action auto-approve + merge (niveau 3)
3. Sinon → attend approbation Edouard → GitHub merge auto apres CI (niveau 2)
4. Health check debut cycle suivant → detecte PR mergee → Notion "Termine"
5. Taches bloquees par cette tache → debloquees au cycle suivant (niveau 1)

### 4.8 Sync automatique spec→Notion (D12)

Le skill `/spec` ecrit directement les taches dans la base Notion "OpenClawTasks" via l'API (curl/jq, coherent avec D2). Apres generation des fichiers spec (index.md, task-XXX.md, PRD.json), `/spec` cree une page Notion par tache avec :
- Les **proprietes** mappees depuis le frontmatter des task files
- Le **contenu spec** (objectif, contexte, AC, steps) ecrit dans le body de la page Notion (coherent avec D1r)
- Les **dependances** comme relations entre pages Notion (coherent avec D9)

**Mapping spec→Notion** :

| Source (/spec) | Propriete Notion | Transformation |
|----------------|------------------|----------------|
| task frontmatter `title` | Name (title) | Direct |
| task frontmatter `complexity` S/M/L | Complexite (select) | S→Simple, M→Moyenne, L→Complexe |
| PRD.json `priority` | Priorite (select) | must-have→P1, should-have→P2, could-have→P3 |
| PRD.json `dependencies.depends_on` | Bloque par (relation) | Resolu apres creation de toutes les pages |
| PRD.json `meta.projectName` | Projet (relation) | Lookup dans projects.json → notion_project_id → relation page |
| task body (Objective, Context, AC, Steps) | Page body (blocks) | Markdown→Notion blocks via API |
| — | Statut | "A faire" (defaut) |
| — | Flags | Depuis brief ou config |

**Algorithme de sync** :
0. Resoudre le `notion_project_id` depuis `projects.json` pour le projet courant
1. Creer toutes les pages avec la relation Projet (+ collecter les page IDs retournes)
2. Mapper task-ID → page-ID
3. Patcher les relations "Bloque par" avec les page IDs resolus
4. Log: "{N} taches creees dans Notion pour {feature-slug}"

**Prerequis** : Variables d'environnement `NOTION_API_KEY` et `NOTION_DB_ID` configurees dans `.env` du projet ou du VPS.

**Gestion d'erreur** : Si Notion API indisponible, log WARNING et continuer (les fichiers spec locaux restent la source de verite). Le sync peut etre relance manuellement.

---

## 5. User Stories et Criteres d'Acceptation

### US1: Execution automatique d'une tache Notion

**Story**: As Edouard, I want the pipeline to automatically execute pre-qualified Notion tasks so that I can process 15-30 tasks per weekend without manual intervention.

**Priorite**: Must have

**Criteres d'acceptation**:
```gherkin
AC1: Tache simple executee avec succes
Given une tache "A faire" dans Notion avec un contenu spec (body Notion ou Spec Path valide)
And le quota Claude Code est disponible
When le cron declenche pipeline-runner.sh
Then la tache passe "En cours" dans Notion
And Claude Code execute implement-auto avec la spec
And une PR est creee sur GitHub
And la tache passe "En review" dans Notion avec le lien PR
And une notification Telegram est envoyee

AC2: Tache echouee geree proprement
Given une tache "A faire" dans Notion
When l'execution echoue (timeout, tests KO, hallucination)
Then le worktree est nettoye
And la tache passe "Echoue" dans Notion avec le message d'erreur
And une notification Telegram est envoyee avec la phase d'echec

AC3: Tache partielle
Given une tache dont certains composants reussissent et d'autres echouent
When implement-auto retourne PARTIAL
Then une PR draft est creee
And la tache passe "En review (partiel)" dans Notion
And la notification inclut le nombre de composants en echec
```

**Edge cases identifies**:
- Spec Path renseigne mais fichier inexistant → marquer FAILED + notifier "Spec not found: {path}"
- Body Notion vide ET Spec Path vide → marquer FAILED + notifier "No spec content: body empty and no Spec Path"
- Le repo projet n'existe pas sur le VPS → marquer FAILED + notifier "Project not found: {project}"
- Claude Code crash sans produire de JSON → fallback JSON genere par run-task.sh

---

### US2: Guards et securite du pipeline

**Story**: As Edouard, I want the pipeline to protect itself from failures so that it doesn't burn my quota or leave the system in an inconsistent state.

**Priorite**: Must have

**Criteres d'acceptation**:
```gherkin
AC1: Kill switch Telegram
Given le pipeline est en cours d'execution
When Edouard envoie /kill au bot Telegram
Then le pipeline s'arrete avant la prochaine tache (delai max = intervalle cron)
And une notification confirme l'arret

AC2: Health check post-crash
Given une tache "En cours" dans Notion dont le processus n'existe plus
When un nouveau cycle cron demarre
Then le health check detecte la tache orpheline
And le worktree est nettoye
And la tache passe "Echoue" avec le message "Interrupted: crash recovery"
And une notification est envoyee

AC3: Circuit breaker echecs consecutifs
Given 3 taches consecutives ont echoue
When le pipeline atteint la 4eme tache
Then le cycle s'arrete
And une notification "Pipeline en pause: 3 echecs consecutifs" est envoyee

AC4: Verrou anti-concurrence
Given un cycle pipeline est en cours
When le cron declenche un nouveau cycle
Then le nouveau cycle detecte le lockfile et quitte sans action
```

**Edge cases identifies**:
- Lockfile stale (processus mort mais lockfile existe) → verifier PID, nettoyer si mort
- Health check trouve 5 taches orphelines → les traiter toutes, pas seulement la premiere
- Notification Telegram echoue → log WARNING, continuer l'execution (notifications = confort)

---

### US3: Configuration et observabilite

**Story**: As Edouard, I want to configure the pipeline for multiple projects and monitor its activity so that I can diagnose issues Monday morning.

**Priorite**: Should have

**Criteres d'acceptation**:
```gherkin
AC1: Configuration multi-projet
Given un fichier projects.json avec 2 projets configures
When des taches de differents projets sont "A faire" dans Notion
Then le pipeline execute chaque tache dans le bon repertoire projet
And utilise les parametres par defaut du projet (modele, flags, timeout)

AC2: Dry-run mode
Given le flag --dry-run est passe a pipeline-runner.sh
When le pipeline s'execute
Then les taches sont listees mais pas executees
And aucune modification Notion n'est faite
And aucune notification n'est envoyee
And le log affiche "[DRY-RUN]" devant chaque action

AC3: Heartbeat notification
Given le pipeline termine un cycle
When au moins une tache a ete traitee
Then un resume est envoye via Telegram: taches traitees/reussies/echouees
```

**Edge cases identifies**:
- Projet inconnu dans Notion → ignorer la tache + notifier "Unknown project: {name}"
- projects.json corrompu → pipeline refuse de demarrer + notifier

---

### US4: Sync automatique spec→Notion

**Story**: As Edouard, I want `/spec` to automatically create tasks in Notion so that the pipeline backlog is populated without any manual step.

**Priorite**: Must have

**Criteres d'acceptation**:
```gherkin
AC1: Sync apres generation des specs
Given un brief traite par /spec generant 5 task files
And les variables NOTION_API_KEY et NOTION_DB_ID sont configurees
When /spec termine la generation
Then 5 pages sont creees dans la DB Notion "OpenClawTasks"
And chaque page a le titre, la priorite, la complexite et le projet remplis
And le body de chaque page contient la spec complete (objectif, AC, steps)
And le statut de chaque page est "A faire"

AC2: Dependances comme relations
Given les tasks task-002 et task-003 dependent de task-001
When /spec cree les pages Notion
Then les pages task-002 et task-003 ont une relation "Bloque par" pointant vers la page task-001

AC3: Notion indisponible
Given les variables Notion ne sont pas configurees ou l'API est indisponible
When /spec termine la generation
Then les fichiers spec locaux sont generes normalement
And un WARNING est affiche "Notion sync skipped: {raison}"
And aucune erreur ne bloque le workflow
```

**Edge cases identifies**:
- Tache deja existante dans Notion (meme nom + meme projet) → skip + warning "Task already exists: {name}"
- DB Notion n'a pas toutes les proprietes attendues → log ERROR pour les proprietes manquantes, creer ce qui est possible
- Plus de 100 taches dans un batch → paginer les creations (rate limit Notion: 3 req/s)

---

### US5: Dependances inter-taches

**Story**: As Edouard, I want to define task dependencies in Notion so that the pipeline executes tasks in the correct order.

**Priorite**: Must have

**Criteres d'acceptation**:
```gherkin
AC1: Tache bloquee ignoree
Given une tache B "A faire" avec "Bloque par" pointant vers tache A "En cours"
When le pipeline query les taches "A faire"
Then la tache B est filtree (non executee)
And la tache B passe en statut "Bloque" dans Notion

AC2: Tache debloquee automatiquement
Given une tache A "Termine" (PR mergee)
And une tache B "Bloque" dont l'unique dependance est A
When le prochain cycle cron demarre
Then la tache B est debloquee et executee normalement
```

**Edge cases identifies**:
- Dependance circulaire (A bloque B, B bloque A) → les deux restent "Bloque" indefiniment, notification warning
- Dependance vers tache "Echoue" → la tache reste "Bloque", notification "Blocked by failed task: {name}"
- Tache avec 3+ dependances → toutes doivent etre "Termine" pour debloquer

---

### US6: Auto-merge des PRs

**Story**: As Edouard, I want pipeline PRs to be auto-merged when safe so that dependent tasks can execute without waiting for my manual review.

**Priorite**: Should have

**Criteres d'acceptation**:
```gherkin
AC1: Auto-merge active par defaut
Given une PR creee par le pipeline
And le flag "no_auto_merge" n'est pas present
When handle_success termine
Then gh pr merge --auto --squash est execute
And le log indique "Auto-merge enabled for PR {url}"

AC2: PR safe auto-approuvee
Given une PR creee pour une tache Simple
And le JSON implement-auto indique SUCCESS + tests pass + 0 erreur + <=2 warnings
When le pipeline evalue la PR
Then le label "pipeline-safe" est ajoute a la PR
And la GitHub Action auto-approve et merge la PR
And Notion est mis a jour avec "Auto-merged: true"

AC3: PR non-safe attend approbation
Given une PR pour une tache Moyenne ou Complexe
When le pipeline evalue la PR
Then seul gh pr merge --auto est active (pas de label)
And la PR attend l'approbation d'Edouard pour merger
```

**Edge cases identifies**:
- GitHub Action echoue (permissions) → PR reste ouverte, log ERROR, pas de retry
- Flag no_auto_merge → ni gh pr merge --auto ni label, review 100% manuelle

---

## 6. Decisions et Orientations Techniques

| Decision | Rationale | Impact | Confiance |
|----------|-----------|--------|-----------|
| D1r: Specs dans Notion body (defaut), Git optionnel | Body Notion sans limite, 70+ pages testees, centralise | run-task.sh lit body OU fichier selon Spec Path | High |
| D2: API Notion en curl/jq pur | Portable, previsible, pas de dependance MCP | Scripts autonomes | High |
| D3: Telegram basique (notifs + kill) | V1 minimaliste, commandes avancees en V2 | SPEC-04 simple | High |
| D4: Quota V1 = reactif M2+M3 | Seuils proactifs speculatifs, reactif suffit | quota-checker.sh simplifie | High |
| D5: Specs dans docs/specs/pipeline/ | Repertoire dedie, clair, versionne | Convention multi-projet | High |
| D6: Telegram polling (getUpdates) | Pas de daemon, integre au cycle cron | Delai max = intervalle cron | High |
| D7: Export brainstorm→Notion = script manuel | Hors pipeline auto, outil de commodite | Composant optionnel | Medium |
| D8: Kill switch via getUpdates (pas daemon) | Simple, suffisant pour V1 weekend | Integre dans pipeline-runner.sh | High |
| D9: Dependances via relation "Bloque par" | Naturel dans Notion, pas de DAG externe | filter_blocked_tasks() dans pipeline-runner.sh | High |
| D10: Auto-merge GitHub natif | gh pr merge --auto --squash apres creation PR | Prerequis: Allow auto-merge ON dans settings repo | High |
| D11: PRs "safe" auto-approuvees via label | pipeline-safe + GitHub Action, zero intervention | Prerequis: GitHub Action + Allow Actions to approve PRs | High |
| D12: /spec sync direct vers Notion | Automatise backlog, zero etape manuelle, coherent D1r+D2 | /spec ecrit body + proprietes via curl/jq | High |
| D13: Projet = relation vers table Projets | Evite duplication select, fiches projet riches, navigation bidirectionnelle | projects.json inclut notion_project_id par projet | High |

### Decisions differees
- **Tracking proactif quota (M1)**: Differe apres calibration avec donnees reelles. A revisiter apres 3-4 weekends de production.
- **Commandes Telegram /status /pause /resume**: V2, si le besoin se confirme.
- **Pagination Notion**: Si le backlog depasse 100 taches "A faire" (improbable en V1).

### Choix architecturaux
- **Pattern retenu**: Scripts Bash orchestrateur (pipeline pattern) avec separation des responsabilites (runner/task/quota/notify)
- **Justification**: Bash + jq est le minimum viable pour de la "plomberie" systeme. Pas besoin de Python ou de framework. Les scripts sont portables et debuggables.

---

## 7. Priorisation MoSCoW

### Must Have (MVP) — ~65% effort

| # | Feature/Story | Effort estime | Dependance |
|---|---------------|---------------|------------|
| 1 | Schema Notion "OpenClawTasks" (SPEC-03) | S (2h) | - |
| 2 | notify.sh - wrapper Telegram (SPEC-04) | S (2-3h) | Bot Telegram cree |
| 3 | quota-checker.sh - reactif M2+M3 (SPEC-02) | S (2h) | - |
| 4 | run-task.sh - execution unitaire (SPEC-02) | M (3-4h) | #1, implement-auto |
| 5 | pipeline-runner.sh - boucle principale (SPEC-02) | M (4-5h) | #1, #2, #3, #4 |
| 5b | Dependances inter-taches (relation Notion) | S (2h) | #1 |
| 5c | Sync spec→Notion (dans /spec) | M (3-4h) | #1 |

### Should Have — ~20% effort

| # | Feature/Story | Effort estime | Dependance |
|---|---------------|---------------|------------|
| 6 | Dry-run mode (--dry-run) | S (2h) | #5 |
| 7 | Config multi-projet (projects.json) | S (2h) | #5 |
| 8 | Health check tokens (Notion, GitHub, Telegram) | S (1h) | #5 |
| 8b | Auto-merge niveau 2 (gh pr merge --auto) | S (1h) | #5 |
| 8c | Auto-merge niveau 3 (label + GitHub Action) | M (2-3h) | #5, GitHub Action deploye |
| 8d | Detection PRs mergees (health check) | S (2h) | #5, #8b |

### Could Have — ~15% effort

| # | Feature/Story | Effort estime | Dependance |
|---|---------------|---------------|------------|
| 9 | Log rotation (7 jours) | S (1h) | #5 |

### Won't Have (cette release)
- **Commandes Telegram avancees** (/status, /pause, /resume) — V2, complexite injustifiee pour V1
- **Tracking proactif quota (M1)** — Donnees insuffisantes pour calibrer les seuils
- **Parallelisme** — V2, le quota est une ressource partagee
- **Dashboard web** — Notion + Telegram suffisent pour un operateur unique
- **Auto-merge niveau 4** (merge toutes les PRs sans exception) — Trop risque, meme les PRs non-safe meritent un regard

---

## 8. Contraintes et Dependances

### Contraintes techniques

| Type | Contrainte | Impact |
|------|------------|--------|
| Stack | Bash + jq (pas de Python cote orchestrateur) | Scripts simples mais verbeux |
| Infra | VPS Ubuntu 24, user non-root `pipeline` | Permissions restrictives, pas de Docker |
| Quota | Claude Max 5x, fenetre glissante ~5h | Max ~15-30 taches/weekend |
| Headless | Claude Code via `claude -p` (pas d'interaction) | implement-auto doit etre 100% autonome |
| Multi-projet | Gardel (Django) + Symfony/React | Config par projet dans projects.json |

### Dependances externes

| Dependance | Type | SLA/Disponibilite | Fallback |
|------------|------|-------------------|----------|
| Notion API | Externe | 99.9% | Pipeline s'arrete + notifie |
| Claude Code CLI | Externe | Depends on Max plan | Auth check + cooldown |
| GitHub API (via gh) | Externe | 99.95% | Retry manuelle post-pipeline |
| Telegram Bot API | Externe | 99.9% | Log WARNING, pipeline continue sans notifs |
| GitHub Actions | Interne | Per-project | Workflow auto-merge-safe.yml dans chaque repo |

### Integrations requises
- **Notion API v2022-06-28**: Query (filter/sort), Update (properties)
- **Claude Code CLI**: `claude -p` avec `--output-format json`, `--allowedTools`, `--permission-mode bypassPermissions`
- **GitHub CLI (gh)**: `gh pr create`, `gh auth status`
- **Telegram Bot API**: `sendMessage`, `getUpdates`
- **Git**: worktree add/remove, fetch, push

---

## 9. Risques et Hypotheses

### Risques identifies

| Risque | Probabilite | Impact | Mitigation |
|--------|-------------|--------|------------|
| Session Claude Code expire pendant le weekend | Low | Bloquant | Auth check en debut de cycle + notification SSH |
| Quota epuise avant de traiter toutes les taches | Medium | Medium | Reactif M2+M3, le pipeline reprend au prochain cycle |
| Notion API change ou indisponible | Low | Bloquant | Version API fixee (2022-06-28), health check tokens |
| PR body trop long (limite GitHub ~65K chars) | Low | Low | Tronquer, renvoyer vers Feature Document |
| Conflit Git entre deux PRs sur meme fichier | Medium | Medium | Fan-out depuis main, humain decide l'ordre de merge |
| VPS reboot pendant execution | Low | Medium | Health check post-crash, cleanup worktree, recovery auto |
| Specs incorrectes (hallucination implement-auto) | Medium | Medium | Review humaine des PRs, Feature Document pour tracabilite |
| GitHub PAT expire | Medium | Bloquant | Health check tokens, notification, procedure de renouvellement |
| Auto-merge d'une PR bugguee (faux positif safe) | Low | High | Criteres stricts (Simple + SUCCESS + tests pass + 0 erreur), label visible dans PR |
| Dependance circulaire bloque des taches indefiniment | Low | Medium | Warning dans les logs + notification Telegram si tache "Bloque" depuis > 2 cycles |

### Hypotheses (Assumptions)
- **Claude Max 5x permet ~15-30 taches/weekend** — Si faux: ajuster max_tasks_per_run et intervalle cron
- **Les taches pre-qualifiees sont vraiment STANDARD** — Si faux: implement-auto echoue, tache marquee "Echoue" + review manuelle
- **Un seul operateur (Edouard) review les PRs** — Si faux: ajouter des reviewers GitHub dans la config
- **Le VPS est stable pendant le weekend** — Si faux: health check + recovery gere les interruptions

---

## 10. Plan d'Action Haut Niveau

| Phase | Livrables | Effort estime | Owner | Prerequis |
|-------|-----------|---------------|-------|-----------|
| 1. Setup Notion | DB "OpenClawTasks" avec 16 proprietes (schema detaille en section 4.1) | ~2h | Edouard | - |
| 1b. Sync spec→Notion | Integration API Notion dans /spec (curl/jq, creation pages + relations) | ~3-4h | Pipeline | Phase 1 |
| 2. Telegram Bot | Bot cree, notify.sh operationnel | ~2-3h | Edouard | BotFather Telegram |
| 3. Quota Checker | quota-checker.sh (M2+M3) | ~2h | Pipeline | - |
| 4. Run Task | run-task.sh (lecture hybride Notion body/Git) | ~4h | Pipeline | Phase 1 + implement-auto |
| 5. Pipeline Runner | pipeline-runner.sh (dependances + auto-merge) | ~5h | Pipeline | Phases 1-4 |
| 6. Config Multi-Projet | projects.json + integration | ~2h | Pipeline | Phase 5 |
| 7. GitHub Action | auto-merge-safe.yml + config repos | ~1-2h | Edouard | Phase 5 |
| 8. Detection Merge | Health check PRs mergees → Notion "Termine" | ~2h | Pipeline | Phases 5, 7 |
| 9. Test E2E | Dry-run + run reel avec dependances + auto-merge | ~3h | Edouard | Tout |

**Effort total estime**: ~26-31h (~5-6 jours)
**Chemin critique**: Phase 1 → Phase 4 → Phase 5 → Phase 7 → Phase 8 → Phase 9

### Quick Wins (impact eleve, effort faible)
1. Schema Notion (Phase 1) — Prerequis pour tout, faisable en 2h sur l'interface Notion
2. Bot Telegram (Phase 2) — BotFather + curl = bot fonctionnel en 30 min

### Investissements Strategiques (impact eleve, effort eleve)
1. pipeline-runner.sh (Phase 5) — Le coeur du systeme, concentre toute la logique de guards/recovery
2. Test E2E (Phase 7) — Le moment de verite, calibration des seuils avec donnees reelles

---

## 11. Mindmap de Synthese

```mermaid
mindmap
  root((Pipeline Orchestration))
    SPEC-02 Orchestrateur
      pipeline-runner.sh
        Verrou lockfile
        Kill switch check
        Health check recovery
        Boucle taches
        Circuit breaker 3 echecs
        Dependances filter_blocked
        Auto-merge 3 niveaux
        Detection PRs mergees
      run-task.sh
        Lecture hybride Notion body/Git
        Worktree fan-out
        Claude Code headless
        Parse JSON resultat
        Push + PR
      quota-checker.sh
        M2 Detection throttle
        M3 Cooldown 30min
    SPEC-03 Notion
      DB OpenClawTasks
        16 proprietes
        Spec dans body Notion defaut
        Spec Path Git optionnel
        Relation Bloque par
        7 statuts dont Bloque
      notion_query curl/jq
      notion_update PATCH
      Export brainstorm optionnel
      Sync depuis /spec
        Mapping frontmatter → proprietes
        Body spec → page content
        Relations dependances
    SPEC-04 Telegram
      notify.sh wrapper
      Kill switch getUpdates
      Heartbeat fin de cycle
    Auto-merge
      Niveau 2 gh pr merge --auto
      Niveau 3 label pipeline-safe
      GitHub Action auto-approve
      Detection merge health check
    Config
      projects.json
      .env secrets
      Health check tokens
    Securite
      Fichier .env chmod 600
      Tokens health check
      Pas de secrets dans logs
```

---

## 12. Score EMS Final

```
EMS Final: 76/100 [Mature]

Progression EMS
100 |
 90 | . . . . . . . . . . . . . . . . . . . .
 80 |                              *--- 76
 70 | . . . . . . . . . . . .+--+. . . . . .
 67 |                   +----+
 60 | . . . . . . . . . . . . . . . . . . . .
 57 |             +----+
 50 |
 42 |       +----+
 40 | . . . . . . . . . . . . . . . . . . . .
 20 | +----+
  0 +------+-----+-----+-----+-----+------
    Init  It.1  It.2  It.3  It.4  Fin

Axes finaux:
   Clarte       [=================...] 85/100 *
   Profondeur   [===============.....] 75/100
   Couverture   [==============......] 70/100
   Decisions    [================....] 78/100
   Actionab.    [===========.........] 55/100
```

**Evaluation globale**: Exploration mature avec 8 decisions verrouillees et un plan d'action sequencé. L'axe Actionabilite est le plus faible car les details d'implementation (code exact des fonctions utilitaires) sont du ressort de `/spec` et `/implement`, pas du brainstorm.

### Verification des Criteres de Succes

| Critere | Statut | Evidence |
|---------|--------|----------|
| 3 specs detaillees pour /implement | OK | Schema Notion, interfaces, contrats JSON definis |
| Interfaces entre SPEC-02/03/04 definies | OK | Contrats notion_query/update, notify, kill switch documentes |
| Gaps G1-G10 adresses | OK | D4 (G1/G3), D1 (G4), D8 (G7), cleanup (G10), auth check (G9) |
| Chaque composant testable isolement | Partiel | Dry-run mode prevu mais pas encore specifie en detail |

---

## 13. Pistes Non Explorees

| Sujet | Pourquoi non explore | Valeur potentielle | Prochaine etape |
|-------|----------------------|-------------------|-----------------|
| Parallelisme multi-taches | Explicitement V2 (quota partage) | High | Mesurer quota reel, evaluer faisabilite |
| Dashboard web monitoring | Notion + Telegram suffisent pour 1 operateur | Medium | Si equipe grandit |
| Tracking proactif quota (M1) | Seuils speculatifs, besoin donnees reelles | Medium | Calibrer apres 3-4 weekends |
| Auto-merge niveau 4 (sans exception) | V1 conserve review humaine pour non-safe | Low | Evaluer apres 3-4 weekends si taux faux-positif safe < 5% |
| Caching Notion (eviter re-queries) | Rate limit Notion largement suffisant | Low | Si latence problematique |
| Sync bidirectionnel Notion↔Git | V1 = push only (spec→Notion), pas de pull Notion→Git | Medium | Si besoin de modifier les specs dans Notion et retrouver les changements dans Git |
| Metriques de performance cumulees | Pas prioritaire V1 | Medium | Ajouter un dashboard Notion avec formules |

---

## 14. References

### Documents analyses
- **BRIEF-Pipeline-V3.md**: Architecture globale, 7 scenarios d'echec, 10 gaps identifies, budget tokens
- **SPEC-02-orchestrator.md**: Spec detaillee des 3 scripts Bash, contrat JSON implement-auto → orchestrateur

### Codebase verifiee
- **src/skills/implement-auto/**: 8 steps + 5 references, contrat JSON de sortie, circuit breaker 3 niveaux
- **src/skills/implement-auto/references/output-json-schema.md**: Schema JSON de sortie (status, metrics, phases, checks, errors, warnings)

### Recherches web
- Non effectuees (context suffisant avec les documents existants)

### Conversations passees referencees
- Session brainstorm implement-auto (EMS 86, completee le 2026-02-11) — Decisions D1-D7 sur le skill autonome

---

## 15. Prochaines Etapes

**Workflow recommande**:

| Etape | Skill | Action |
|-------|-------|--------|
| 1 | Manuel | Creer la DB Notion "OpenClawTasks" avec 16 proprietes |
| 1b | `/implement` | Implementer sync spec→Notion dans le skill /spec |
| 2 | `/implement` | Implementer SPEC-04 (notify.sh) |
| 3 | `/implement` | Implementer quota-checker.sh |
| 4 | `/implement` | Implementer run-task.sh (lecture hybride Notion/Git) |
| 5 | `/implement` | Implementer pipeline-runner.sh (dependances + auto-merge) |
| 6 | `/implement` | Config multi-projet + secrets |
| 7 | Manuel | Deployer GitHub Action + config repos |
| 8 | `/implement` | Detection merge + update Notion |
| 9 | Test E2E | Run pilote avec 3-5 taches Gardel (dont 1 avec dependance) |

**Routing de complexite**: STANDARD (10 phases, 26-31h estimees, multi-fichier)
**Skill suggere**: `/implement` pour chaque composant

**Commande suggeree**:
```
/implement notify-sh @brief-orchestrator-pipeline-20260211.md
```

---
