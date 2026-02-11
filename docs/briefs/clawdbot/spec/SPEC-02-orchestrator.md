# SPEC-02 — Script Orchestrateur

> PRD — Pipeline de développement semi-automatisé V3
> Version: 1.0 | Date: 2026-02-11
> Auteur: Edouard (spécification brainstorm)
> Consommateur: Scripts Bash exécutés via cron OpenClaw
> Réf. brief: BRIEF-Pipeline-V3

---

## §0 — Metadata

| Champ | Valeur |
|-------|--------|
| Composant | Scripts orchestrateur : `pipeline-runner.sh`, `run-task.sh`, `quota-checker.sh` |
| Langage | Bash + jq (pas de Python requis pour l'orchestrateur) |
| Dépendances | OpenClaw (cron), Claude Code CLI, GitHub CLI (`gh`), Notion API, jq |
| Environnement | VPS Linux (Ubuntu 24), user non-root dédié `pipeline` |
| Priorité | P0 — Colonne vertébrale du pipeline |
| Complexité | STANDARD |
| Effort estimé | 1-2 jours |
| Gaps adressés | G1 (quota checker), G2 (tri complexité), G3 (monitoring tokens), G4 (base branch), G7 (health check), G9 (auth session), G10 (rollback/cleanup) |

---

## §1 — Contexte & Objectif

### Contexte

Le pipeline semi-automatisé connecte Notion (source des tâches) à Claude Code (exécuteur) via un orchestrateur sur VPS. L'orchestrateur est la pièce maîtresse qui coordonne l'ensemble du flux sans intervention humaine.

Le skill `implement-auto` (SPEC-01) traite UNE tâche à la fois et produit un JSON structuré. L'orchestrateur est responsable de tout ce qui entoure cette exécution : sélection des tâches, gestion du quota, worktree/push/PR, notifications, recovery.

### Objectif

Trois scripts principaux + fichiers de configuration :

1. **`pipeline-runner.sh`** — Lancé par cron OpenClaw. Orchestre le cycle complet : health check, sélection tâches, boucle d'exécution, heartbeat.
2. **`run-task.sh`** — Exécute UNE tâche : prompt Claude Code → parse JSON résultat → push → PR.
3. **`quota-checker.sh`** — Vérifie l'état du quota Claude Code avant de lancer une tâche. Trois méthodes : tracking interne, détection throttle réactive, cooldown post-throttle.

### Ce que l'orchestrateur n'est PAS

- **Pas un agent IA** — c'est du Bash/jq pur, pas d'intelligence, juste de la plomberie
- **Pas responsable de la qualité du code** — c'est SPEC-01 (implement-auto) + review humaine
- **Pas un scheduler avancé** — il repose sur cron OpenClaw pour le déclenchement
- **Pas un système de deploy** — il s'arrête à la PR

### Architecture d'ensemble

```
Cron OpenClaw (toutes les 10-60 min)
    │
    ▼
pipeline-runner.sh
    │
    ├── 1. Verrou anti-concurrence (lockfile + trap)
    │
    ├── 2. Kill switch check (fichier sentinelle /tmp/pipeline-kill)
    │
    ├── 3. Auth check Claude Code (prompt minimal "Reply OK")
    │
    ├── 4. Health check (recovery post-crash)
    │   └── Détecter tâches "En cours" sans processus actif → marquer "Échoué"
    │
    ├── 5. Query Notion : tâches "À faire", triées par priorité puis complexité
    │
    ├── 6. Pour chaque tâche (séquentiel) :
    │   │
    │   ├── 6a. Kill switch re-check
    │   │
    │   ├── 6b. quota-checker.sh → suffisant ?
    │   │   ├── Oui → continuer
    │   │   └── Non → arrêter le cycle
    │   │
    │   ├── 6c. Update Notion → "En cours" + notif 🚀
    │   │
    │   ├── 6d. run-task.sh {task-id} {project} {spec} {flags}
    │   │
    │   └── 6e. Traitement résultat :
    │       ├── SUCCESS → push + PR + Notion "En review" + notif ✅
    │       ├── PARTIAL → push + PR draft + Notion "En review (partiel)" + notif ⚠️
    │       └── FAILED  → cleanup + Notion "Échoué" + notif ❌
    │
    ├── 7. Heartbeat notification (résumé progression)
    │
    └── 8. Fin du cycle (release lockfile)
```

---

## §2 — Spécifications Fonctionnelles

### 2.1 pipeline-runner.sh

#### Configuration

```bash
# pipeline.conf — Configuration du pipeline
PIPELINE_DIR="/srv/pipeline"
PROJECTS_DIR="/srv/projects"
NOTION_DATABASE_ID="xxx-xxx-xxx"        # Base "Dev Tasks" (voir SPEC-03)
NOTION_API_KEY="${NOTION_API_KEY}"       # Variable d'environnement
MAX_TASKS_PER_RUN=5                      # Max tâches par exécution cron
MAX_CONSECUTIVE_FAILURES=3               # Pause après N échecs consécutifs
TASK_TIMEOUT_SECONDS=1200                # 20 minutes par tâche
CLAUDE_MODEL="sonnet"                    # Modèle par défaut
NOTIFICATION_CHANNEL="telegram"          # telegram | discord
LOG_DIR="/srv/pipeline/logs"
STATE_DIR="/srv/pipeline/state"
LOCKFILE="/tmp/pipeline-runner.lock"
KILLSWITCH_FILE="/tmp/pipeline-kill"     # Créé par SPEC-04 (kill switch Telegram)
```

#### Verrou d'exécution (anti-concurrence)

Le cron peut se déclencher pendant qu'un cycle précédent tourne encore. Le lockfile empêche deux instances simultanées :

```bash
# Empêcher deux instances simultanées
if [ -f "$LOCKFILE" ]; then
  PID=$(cat "$LOCKFILE")
  if kill -0 "$PID" 2>/dev/null; then
    log "Pipeline already running (PID $PID). Exiting."
    exit 0
  else
    log "Stale lockfile found (PID $PID dead). Removing."
    rm "$LOCKFILE"
  fi
fi
echo $$ > "$LOCKFILE"
trap "rm -f $LOCKFILE" EXIT
```

Le `trap EXIT` garantit que le lockfile est nettoyé même en cas de crash, SIGTERM, ou exit prématuré.

#### Kill switch check

Avant toute action, et avant chaque tâche :

```bash
check_killswitch() {
  if [ -f "$KILLSWITCH_FILE" ]; then
    log "Kill switch activated. Stopping pipeline."
    notify "🛑 Pipeline arrêté par kill switch"
    rm -f "$KILLSWITCH_FILE"  # Consommer le signal
    exit 0
  fi
}
```

Le fichier sentinelle est créé par le bot Telegram (SPEC-04) quand l'utilisateur envoie `/kill`. Le runner le vérifie en entrée de cycle et avant chaque nouvelle tâche.

#### Auth check Claude Code (Gap G9)

```bash
check_claude_auth() {
  # 1. Vérifier que Claude Code est dans le PATH
  if ! command -v claude &>/dev/null; then
    notify "🔴 Claude Code non installé ou non dans PATH"
    exit 1
  fi

  # 2. Tester avec un prompt minimal (coût négligeable)
  result=$(timeout 30 claude -p "Reply with just: OK" --output-format json 2>&1)
  exit_code=$?

  if [ $exit_code -ne 0 ] || echo "$result" | grep -qi "authentication\|unauthorized\|login\|expired"; then
    notify "🔴 Session Claude Code expirée. Reconnexion nécessaire:\nssh pipeline@vps 'claude login'"
    exit 1
  fi

  log "Claude Code auth: OK"
}
```

L'auth Claude Code (plan Max) utilise un token de session qui peut expirer. Si ça arrive un samedi soir, le pipeline s'arrête et notifie. La reconnexion est manuelle (`claude login` en SSH). C'est un cas rare mais bloquant.

#### Health check — Recovery post-crash (Gap G7)

Au démarrage de chaque cycle, détecter les tâches qui étaient "En cours" mais dont le processus n'existe plus (crash VPS, reboot, OOM kill) :

```bash
health_check() {
  log "Running health check..."

  # 1. Chercher tâches "En cours" dans Notion
  in_progress_tasks=$(notion_query "En cours")

  # 2. Pour chaque tâche "En cours" :
  echo "$in_progress_tasks" | jq -c '.[]' | while read -r task; do
    task_id=$(echo "$task" | jq -r '.id')
    task_title=$(echo "$task" | jq -r '.title')
    project=$(echo "$task" | jq -r '.project')
    pid_file="/tmp/pipeline-task-${task_id}.pid"

    if [ -f "$pid_file" ]; then
      pid=$(cat "$pid_file")
      if kill -0 "$pid" 2>/dev/null; then
        # Processus encore actif → ne rien faire
        log "Task '$task_title' still running (PID $pid)"
        continue
      fi
    fi

    # Processus mort ou pas de PID file → tâche interrompue
    log "Task '$task_title' was interrupted (no active process)"

    # Cleanup worktree sale
    project_dir="${PROJECTS_DIR}/${project}"
    cleanup_worktree "$project_dir" "$task_id"

    # Marquer "Échoué" dans Notion avec log explicatif
    notion_update "$task_id" \
      --status "Échoué" \
      --log "Interrupted: process not found (crash/reboot recovery at $(date -u +%FT%TZ))"

    # Notifier
    notify "❌ Tâche '${task_title}' interrompue (recovery post-crash)"

    # Cleanup PID file
    rm -f "$pid_file"
  done

  log "Health check complete"
}
```

#### Tri des tâches (Gap G2)

```bash
# Trier par : priorité (P0 > P1 > P2) puis complexité croissante (simple → complexe)
# Stratégie : les tâches simples d'abord pour maximiser le throughput avant épuisement quota
tasks=$(notion_query "À faire" | jq 'sort_by(.priority_score, .complexity_score)')
```

Le champ `complexity_score` est un nombre dans Notion (voir SPEC-03) : simple=1, moyenne=2, complexe=3. Le champ `priority_score` : P0=0, P1=1, P2=2, P3=3.

Les tâches P0 passent toujours en premier. À priorité égale, les plus simples passent d'abord (maximise le nombre de tâches traitées avant un éventuel épuisement du quota).

#### Boucle principale

```bash
main() {
  source pipeline.conf

  # Guards initiaux
  check_killswitch
  check_claude_auth
  health_check

  # Récupérer les tâches triées
  tasks=$(notion_query "À faire" | jq 'sort_by(.priority_score, .complexity_score)')
  task_count=$(echo "$tasks" | jq 'length')

  if [ "$task_count" -eq 0 ]; then
    log "No tasks to process. Exiting."
    exit 0
  fi

  log "Found $task_count tasks to process (max $MAX_TASKS_PER_RUN per run)"

  consecutive_failures=0
  tasks_processed=0
  tasks_succeeded=0
  tasks_failed=0

  echo "$tasks" | jq -c '.[]' | while read -r task; do

    # Guard: kill switch (re-check avant chaque tâche)
    check_killswitch

    # Guard: max tâches par run
    if [ $tasks_processed -ge $MAX_TASKS_PER_RUN ]; then
      log "Max tasks per run reached ($MAX_TASKS_PER_RUN). Stopping."
      break
    fi

    # Guard: échecs consécutifs
    if [ $consecutive_failures -ge $MAX_CONSECUTIVE_FAILURES ]; then
      log "Too many consecutive failures ($consecutive_failures). Pausing pipeline."
      notify "⏸️ Pipeline en pause : $consecutive_failures échecs consécutifs"
      break
    fi

    # Guard: quota check
    if ! ./quota-checker.sh; then
      quota_status=$(./quota-checker.sh 2>&1 || true)
      log "Quota insufficient: $quota_status. Waiting for next cycle."
      notify "⏳ Pipeline en attente de quota ($quota_status)"
      break
    fi

    # Extraire métadonnées de la tâche
    task_id=$(echo "$task" | jq -r '.id')
    task_title=$(echo "$task" | jq -r '.title')
    project=$(echo "$task" | jq -r '.project')
    spec=$(echo "$task" | jq -r '.spec_content')
    flags=$(echo "$task" | jq -r '.pipeline_flags // ""')

    log "Starting task '$task_title' (project: $project, flags: $flags)"

    # Update Notion → "En cours"
    notion_update "$task_id" \
      --status "En cours" \
      --started_at "$(date -u +%FT%TZ)"

    # Notifier démarrage
    notify "🚀 Tâche '${task_title}' démarrée (projet: ${project})"

    # Enregistrer dans le tracking quota
    register_quota_task "$task_id"

    # Lancer run-task.sh avec timeout
    timeout $TASK_TIMEOUT_SECONDS ./run-task.sh "$task_id" "$project" "$spec" "$flags" \
      > "${LOG_DIR}/task-${task_id}.log" 2>&1
    exit_code=$?

    # Parser résultat
    result_file="/tmp/pipeline-result-${task_id}.json"
    if [ -f "$result_file" ]; then
      status=$(jq -r '.status' "$result_file")
    elif [ $exit_code -eq 124 ]; then
      status="TIMEOUT"
    else
      status="FAILED"
    fi

    # Traiter résultat
    case "$status" in
      SUCCESS)
        handle_success "$task_id" "$result_file"
        consecutive_failures=0
        tasks_succeeded=$((tasks_succeeded + 1))
        log "Task '$task_title' completed: SUCCESS"
        ;;
      PARTIAL)
        handle_partial "$task_id" "$result_file"
        consecutive_failures=0  # Partial n'est pas un échec complet
        tasks_succeeded=$((tasks_succeeded + 1))
        log "Task '$task_title' completed: PARTIAL"
        ;;
      FAILED|TIMEOUT)
        handle_failure "$task_id" "$result_file" "$status"
        consecutive_failures=$((consecutive_failures + 1))
        tasks_failed=$((tasks_failed + 1))
        log "Task '$task_title' completed: $status"
        ;;
    esac

    tasks_processed=$((tasks_processed + 1))

    # Cleanup PID file
    rm -f "/tmp/pipeline-task-${task_id}.pid"
    rm -f "/tmp/pipeline-result-${task_id}.json"
  done

  # Heartbeat de fin de cycle
  send_heartbeat "$tasks_processed" "$tasks_succeeded" "$tasks_failed"

  log "Cycle complete: $tasks_processed processed, $tasks_succeeded succeeded, $tasks_failed failed"
}

main "$@"
```

#### handle_success

```bash
handle_success() {
  local task_id="$1"
  local result_file="$2"

  branch=$(jq -r '.branch' "$result_file")
  feature_slug=$(jq -r '.feature_slug' "$result_file")
  project_dir=$(get_project_dir "$task_id")

  # 1. Push la branche
  cd "$project_dir"
  git push origin "$branch"

  # 2. Créer la PR
  pr_title="[Pipeline] ${feature_slug}"
  pr_body=$(generate_pr_body "$result_file")
  pr_url=$(gh pr create \
    --base main \
    --head "$branch" \
    --title "$pr_title" \
    --body "$pr_body")

  # 3. Update Notion
  notion_update "$task_id" \
    --status "En review" \
    --pr_url "$pr_url" \
    --branch "$branch" \
    --tokens_cost "$(jq -r '.metrics.duration_seconds' "$result_file")" \
    --log "Pipeline SUCCESS — PR: $pr_url"

  # 4. Notifier
  notify "✅ Tâche '${feature_slug}' terminée\n→ PR: $pr_url"
}
```

#### handle_partial

```bash
handle_partial() {
  local task_id="$1"
  local result_file="$2"

  branch=$(jq -r '.branch' "$result_file")
  feature_slug=$(jq -r '.feature_slug' "$result_file")
  project_dir=$(get_project_dir "$task_id")
  warnings=$(jq -r '.warnings | join(", ")' "$result_file")
  components_failed=$(jq -r '.metrics.components_failed' "$result_file")
  components_total=$(jq -r '.metrics.components_total' "$result_file")

  # Push + PR draft
  cd "$project_dir"
  git push origin "$branch"
  pr_url=$(gh pr create \
    --base main \
    --head "$branch" \
    --title "[Pipeline][PARTIAL] ${feature_slug}" \
    --body "$(generate_pr_body "$result_file")" \
    --draft)

  # Update Notion
  notion_update "$task_id" \
    --status "En review (partiel)" \
    --pr_url "$pr_url" \
    --branch "$branch" \
    --log "Pipeline PARTIAL ($components_failed/$components_total failed): $warnings"

  # Notifier
  notify "⚠️ Tâche '${feature_slug}' partielle ($components_failed composants en échec)\n→ PR draft: $pr_url\nWarnings: $warnings"
}
```

#### handle_failure (Gap G10 — Cleanup)

```bash
handle_failure() {
  local task_id="$1"
  local result_file="$2"
  local status="$3"

  if [ -f "$result_file" ]; then
    errors=$(jq -r '.errors | join(", ")' "$result_file")
    phase=$(jq -r '.phases_failed[0] // "unknown"' "$result_file")
    feature_slug=$(jq -r '.feature_slug' "$result_file")
  else
    errors="No result file produced (${status})"
    phase="unknown"
    feature_slug="$task_id"
  fi

  # Cleanup worktree (force) — Gap G10
  project_dir=$(get_project_dir "$task_id")
  cleanup_worktree "$project_dir" "$task_id"

  # Update Notion avec log détaillé
  notion_update "$task_id" \
    --status "Échoué" \
    --log "Pipeline $status (phase: $phase): $errors"

  # Notifier avec détail
  notify "❌ Tâche '${feature_slug}' échouée\nStatus: $status\nPhase: $phase\nErreur: $errors"
}
```

#### generate_pr_body

Le body de la PR est généré à partir du JSON résultat. Il donne une vue complète du travail effectué par le pipeline :

```bash
generate_pr_body() {
  local result_file="$1"
  local feature_doc=$(jq -r '.feature_doc' "$result_file")
  local status=$(jq -r '.status' "$result_file")

  cat << EOF
## 🤖 Auto-generated by Pipeline

**Status**: ${status}
**Feature**: $(jq -r '.feature_slug' "$result_file")
**Branch**: $(jq -r '.branch' "$result_file")

### Metrics

| Metric | Value |
|--------|-------|
| Files created | $(jq -r '.metrics.files_created' "$result_file") |
| Files modified | $(jq -r '.metrics.files_modified' "$result_file") |
| Tests added | $(jq -r '.metrics.tests_added' "$result_file") |
| Tests passing | $(jq -r '.metrics.tests_passing' "$result_file") |
| Coverage | $(jq -r '.metrics.coverage_percent' "$result_file")% |
| Components | $(jq -r '.metrics.components_succeeded' "$result_file")/$(jq -r '.metrics.components_total' "$result_file") |
| Duration | $(jq -r '.metrics.duration_seconds' "$result_file")s |

### Checks

| Check | Status |
|-------|--------|
| Tests | $(jq -r '.checks.tests' "$result_file") |
| Lint | $(jq -r '.checks.lint' "$result_file") |
| Typecheck | $(jq -r '.checks.typecheck' "$result_file") |

### Warnings
$(jq -r '.warnings | if length == 0 then "None" else map("- " + .) | join("\n") end' "$result_file")

### Feature Document
See: \`${feature_doc}\`

### Phases completed
$(jq -r '.phases_completed | map("✅ " + .) | join("\n")' "$result_file")
$(jq -r '.phases_failed | if length > 0 then map("❌ " + .) | join("\n") else "" end' "$result_file")

---
⚠️ **Review required** — This PR was generated by an automated pipeline.
Please review the code, tests, and Feature Document before merging.
EOF
}
```

**Note** : si le body dépasse 65K caractères (limite GitHub), il est tronqué avec un renvoi vers le Feature Document pour les détails.

---

### 2.2 run-task.sh

Script d'exécution d'UNE tâche. Appelé par pipeline-runner.sh. Ce script est le pont entre l'orchestrateur et Claude Code.

```bash
#!/bin/bash
set -euo pipefail

TASK_ID="$1"
PROJECT="$2"
SPEC_CONTENT="$3"       # Contenu de la spec (pas un path)
FLAGS="${4:-}"           # Flags optionnels (--validate-plan, --with-review)

source pipeline.conf

PROJECT_DIR="${PROJECTS_DIR}/${PROJECT}"
BRANCH="feature/${TASK_ID}"
RESULT_FILE="/tmp/pipeline-result-${TASK_ID}.json"
PID_FILE="/tmp/pipeline-task-${TASK_ID}.pid"
SPEC_FILE="/tmp/pipeline-spec-${TASK_ID}.md"

# Enregistrer PID pour recovery (G7)
echo $$ > "$PID_FILE"
trap "rm -f $PID_FILE" EXIT

# Écrire spec dans fichier temporaire
echo "$SPEC_CONTENT" > "$SPEC_FILE"

# S'assurer qu'on est dans le bon répertoire projet
cd "$PROJECT_DIR"

# Fetch latest main (base pour le worktree fan-out — G4)
git fetch origin main

# Construire le prompt pour implement-auto
PROMPT="$(cat << PROMPT_EOF
Lis et exécute le skill .claude/commands/implement-auto/SKILL.md

Feature slug: ${TASK_ID}
Spec: @${SPEC_FILE}
Flags: ${FLAGS}

Mode: autonomous — no interaction, no breakpoints
Output: JSON to ${RESULT_FILE}
PROMPT_EOF
)"

# Lancer Claude Code en mode headless
claude -p "$PROMPT" \
  --model "${CLAUDE_MODEL:-sonnet}" \
  --allowedTools "Bash,Read,Write,Edit,Glob,Grep,Task" \
  --permission-mode bypassPermissions \
  --output-format json \
  --cwd "$PROJECT_DIR" \
  2>&1 | tee "${LOG_DIR}/claude-${TASK_ID}.log"

EXIT_CODE=${PIPESTATUS[0]}

# Vérifier que le résultat JSON existe
if [ ! -f "$RESULT_FILE" ]; then
  # Claude Code n'a pas produit de résultat JSON → créer un fallback
  cat > "$RESULT_FILE" << FALLBACK_EOF
{
  "status": "FAILED",
  "feature_slug": "${TASK_ID}",
  "branch": "${BRANCH}",
  "worktree_finalized": false,
  "feature_doc": null,
  "metrics": {
    "files_created": 0,
    "files_modified": 0,
    "tests_added": 0,
    "tests_passing": 0,
    "coverage_percent": 0,
    "duration_seconds": 0,
    "components_total": 0,
    "components_succeeded": 0,
    "components_failed": 0
  },
  "phases_completed": [],
  "phases_failed": ["unknown"],
  "checks": { "tests": "skipped", "lint": "skipped", "typecheck": "skipped" },
  "errors": ["Claude Code did not produce result file (exit code: ${EXIT_CODE})"],
  "warnings": []
}
FALLBACK_EOF
fi

# Cleanup spec temporaire
rm -f "$SPEC_FILE"

exit $EXIT_CODE
```

**Stratégie de base branch (Gap G4)**

Chaque worktree est créé depuis `origin/main` (stratégie "fan-out"). C'est implement-auto (step-00-init) qui exécute `worktree-create.sh`, mais run-task.sh fait le `git fetch origin main` en amont pour garantir que la base est à jour.

Pourquoi fan-out : les tâches sont indépendantes (pré-qualifiées). Si deux tâches modifient le même fichier, c'est un problème de spécification, pas d'orchestration. Le conflit sera visible au merge de la PR → l'humain décide l'ordre.

Alternative rejetée : chaîner les branches (task-2 depuis branch de task-1). Trop fragile : si task-1 échoue, toute la chaîne est bloquée.

---

### 2.3 quota-checker.sh

Claude Code ne fournit pas d'API directe de consultation du quota. La stratégie est pragmatique : tracking interne + détection réactive.

```bash
#!/bin/bash
# quota-checker.sh — Vérifie si on peut lancer une tâche
# Exit 0 = OK, Exit 1 = quota insuffisant

source pipeline.conf

QUOTA_STATE_FILE="${STATE_DIR}/quota.json"

# Initialiser le state file si absent
if [ ! -f "$QUOTA_STATE_FILE" ]; then
  echo '{"tasks":[],"last_throttle":0,"plan":"max_5x","sessions_per_window_limit":27}' > "$QUOTA_STATE_FILE"
fi

current_time=$(date +%s)
window_start=$((current_time - 18000))  # 5h = 18000 secondes
```

#### Méthode 1 : Tracking interne (proactif)

```bash
# Compter les tâches dans la fenêtre glissante de 5h
tasks_in_window=$(jq "[.tasks[] | select(.started_at > $window_start)] | length" "$QUOTA_STATE_FILE")

# Seuil conservateur basé sur le plan Max 5x
# Estimation : ~45 sessions Sonnet par fenêtre 5h
# Garde-fou à 60% : 27 sessions
# Chaque tâche EPCI ≈ 1 session + 1-2 subagents = ~2-3 sessions
MAX_SESSIONS_PER_WINDOW=27
SESSIONS_PER_TASK=3

available_sessions=$((MAX_SESSIONS_PER_WINDOW - tasks_in_window * SESSIONS_PER_TASK))

if [ $available_sessions -le $SESSIONS_PER_TASK ]; then
  echo "QUOTA_LOW"
  exit 1
fi
```

#### Méthode 2 : Détection de throttle réactive

```bash
# Si la dernière tâche a été throttlée (pattern dans les logs Claude Code)
last_task_log=$(ls -t "${LOG_DIR}/claude-*.log" 2>/dev/null | head -1)
if [ -n "$last_task_log" ] && grep -q "rate_limit\|quota_exceeded\|too_many_requests\|429" "$last_task_log" 2>/dev/null; then
  echo "QUOTA_THROTTLED"
  # Enregistrer le moment du throttle
  jq ".last_throttle = $current_time" "$QUOTA_STATE_FILE" > /tmp/quota.tmp && mv /tmp/quota.tmp "$QUOTA_STATE_FILE"
  exit 1
fi
```

#### Méthode 3 : Cooldown post-throttle

```bash
# Si throttle détecté il y a moins de 30 minutes, attendre
last_throttle=$(jq -r '.last_throttle // 0' "$QUOTA_STATE_FILE")
if [ $((current_time - last_throttle)) -lt 1800 ]; then
  remaining=$((1800 - (current_time - last_throttle)))
  echo "QUOTA_COOLDOWN (${remaining}s remaining)"
  exit 1
fi

echo "QUOTA_OK"
exit 0
```

#### Tracking des sessions

Chaque lancement de tâche est enregistré par `register_quota_task` (appelé depuis pipeline-runner.sh) :

```json
{
  "tasks": [
    { "task_id": "auth-login", "started_at": 1739280000, "sessions_estimated": 3 },
    { "task_id": "user-profile", "started_at": 1739281200, "sessions_estimated": 2 }
  ],
  "last_throttle": 0,
  "plan": "max_5x",
  "sessions_per_window_limit": 27
}
```

**Note importante** : ces estimations sont approximatives. Le vrai filet de sécurité est la **détection de throttle réactive** (Méthode 2). Si Claude Code retourne une erreur de quota, on arrête et on attend. Le tracking interne est un garde-fou proactif pour éviter de gaspiller des cycles.

Les seuils (`sessions_per_window_limit`, `SESSIONS_PER_TASK`) devront être calibrés après les premiers runs réels.

---

### 2.4 Fonctions utilitaires

```bash
# notion_query — Wrapper pour l'API Notion
# Retourne un JSON array des tâches avec les champs normalisés
notion_query() {
  local status="$1"
  curl -s "https://api.notion.com/v1/databases/${NOTION_DATABASE_ID}/query" \
    -H "Authorization: Bearer ${NOTION_API_KEY}" \
    -H "Notion-Version: 2022-06-28" \
    -H "Content-Type: application/json" \
    -d "{
      \"filter\": { \"property\": \"Statut\", \"select\": { \"equals\": \"${status}\" } },
      \"sorts\": [
        { \"property\": \"Priorité\", \"direction\": \"ascending\" },
        { \"property\": \"Complexité Score\", \"direction\": \"ascending\" }
      ]
    }" | jq '[.results[] | {
      id: .id,
      title: .properties.Name.title[0].plain_text,
      project: .properties.Projet.select.name,
      spec_content: .properties["Spec PRD"].rich_text[0].plain_text,
      priority: .properties.Priorité.select.name,
      priority_score: (if .properties.Priorité.select.name == "P0" then 0
                       elif .properties.Priorité.select.name == "P1" then 1
                       elif .properties.Priorité.select.name == "P2" then 2
                       else 3 end),
      complexity: .properties.Complexité.select.name,
      complexity_score: (.properties["Complexité Score"].number // 2),
      pipeline_flags: (.properties.Flags.multi_select | map(.name) | join(" "))
    }]'
}

# notion_update — Met à jour une tâche Notion
notion_update() {
  local task_id="$1"
  shift
  # Parse arguments : --status, --pr_url, --branch, --log, --started_at, --tokens_cost
  # Construit le body JSON dynamiquement
  # Appel API Notion PATCH sur /v1/pages/${task_id}
  # (implémentation détaillée : mapping propriétés Notion, voir SPEC-03)
}

# cleanup_worktree — Nettoyage forcé d'un worktree (Gap G10)
cleanup_worktree() {
  local project_dir="$1"
  local task_id="$2"
  local worktree_path="${project_dir}/worktrees/feature-${task_id}"

  if [ -d "$worktree_path" ]; then
    log "Cleaning up worktree: $worktree_path"
    cd "$project_dir"
    git worktree remove "$worktree_path" --force 2>/dev/null || true
    # Ne pas supprimer la branche — peut contenir du travail partiel
    # récupérable manuellement si nécessaire
  fi
}

# get_project_dir — Résout le répertoire projet depuis la config
get_project_dir() {
  local task_id="$1"
  # Lookup dans la config ou dans le résultat Notion
  echo "${PROJECTS_DIR}/${project}"
}

# register_quota_task — Enregistre une tâche dans le tracking quota
register_quota_task() {
  local task_id="$1"
  local current_time=$(date +%s)
  jq ".tasks += [{\"task_id\": \"${task_id}\", \"started_at\": ${current_time}, \"sessions_estimated\": 3}]" \
    "$QUOTA_STATE_FILE" > /tmp/quota.tmp && mv /tmp/quota.tmp "$QUOTA_STATE_FILE"
}

# send_heartbeat — Notification résumé de fin de cycle
send_heartbeat() {
  local processed="$1"
  local succeeded="$2"
  local failed="$3"
  notify "💓 Heartbeat — Cycle terminé\nTraitées: ${processed}\nSuccès: ${succeeded}\nÉchecs: ${failed}\nHeure: $(date -u +%H:%M)"
}

# notify — Wrapper notification (délègue à SPEC-04)
notify() {
  local message="$1"
  # Appel au script de notification (SPEC-04)
  # Fallback : écrire dans le log si notification échoue
  ./notify.sh "$message" 2>/dev/null || log "NOTIFY_FAILED: $message"
}

# log — Logging structuré avec timestamp
log() {
  echo "[$(date -u +%FT%TZ)] [pipeline] $*" | tee -a "${LOG_DIR}/pipeline.log"
}
```

---

## §3 — Spécifications Techniques

### 3.1 Arborescence fichiers sur le VPS

```
/srv/pipeline/
├── pipeline-runner.sh          # Script principal (cron)
├── run-task.sh                 # Exécuteur de tâche unitaire
├── quota-checker.sh            # Vérificateur de quota
├── notify.sh                   # Wrapper notifications (SPEC-04)
├── pipeline.conf               # Configuration
├── state/
│   ├── quota.json              # Tracking quota glissant
│   └── run-history.json        # Historique des runs (optionnel, debug)
├── logs/
│   ├── pipeline.log            # Log principal orchestrateur
│   ├── task-{id}.log           # Log du run-task.sh (stdout/stderr)
│   └── claude-{id}.log         # Log brut de Claude Code (pour debug/throttle detection)
└── tmp/
    ├── pipeline-runner.lock    # Verrou anti-concurrence
    ├── pipeline-kill           # Fichier sentinelle kill switch (créé par SPEC-04)
    ├── pipeline-task-{id}.pid  # PID du processus run-task (pour recovery G7)
    ├── pipeline-spec-{id}.md   # Spec temporaire (copiée depuis Notion)
    └── pipeline-result-{id}.json  # Résultat JSON (produit par implement-auto)

/srv/projects/
├── gardel/                     # Projet Django
│   ├── CLAUDE.md               # Config Claude Code pour ce projet
│   ├── .claude/
│   │   ├── commands/
│   │   │   ├── implement/      # Skill interactif existant
│   │   │   └── implement-auto/ # Nouveau skill autonome (SPEC-01)
│   │   └── state/
│   ├── worktrees/              # Créés/supprimés par le pipeline
│   │   └── feature-{slug}/     # Un worktree par tâche en cours
│   └── docs/features/          # Feature Documents générés
├── projet-symfony/             # Autre projet
│   └── ...
└── ...
```

### 3.2 User Unix et permissions

```bash
# User dédié pipeline (pas root)
sudo useradd -m -s /bin/bash pipeline
sudo usermod -aG docker pipeline  # Si Docker nécessaire pour les tests

# Permissions restrictives
chown -R pipeline:pipeline /srv/pipeline
chown -R pipeline:pipeline /srv/projects
chmod 700 /srv/pipeline/*.sh       # Exécutable uniquement par pipeline
chmod 600 /srv/pipeline/pipeline.conf  # Config sensible (API keys)

# Claude Code installé et authentifié pour l'user pipeline
su - pipeline -c "npm install -g @anthropic/claude-code"
su - pipeline -c "claude login"  # Auth initiale (interactive, une seule fois)

# GitHub CLI authentifié
su - pipeline -c "gh auth login"  # Avec un token PAT ayant les droits repo
```

### 3.3 Cron OpenClaw

```yaml
# OpenClaw workflow definition
name: pipeline-cron
description: >
  Lance le pipeline de développement semi-automatisé.
  Fréquence adaptable : weekend agressif, semaine conservateur.
trigger:
  type: cron
  schedule: "*/30 * * * *"  # Toutes les 30 minutes (à ajuster)
  # Alternatives :
  # "*/10 * * * 6-0"  → Toutes les 10 min le weekend
  # "0 */2 * * 1-5"   → Toutes les 2h en semaine

action:
  type: shell
  command: "/srv/pipeline/pipeline-runner.sh"
  user: pipeline
  timeout: 3600  # 1h max par cycle
  env:
    - NOTION_API_KEY=${NOTION_API_KEY}
    - GITHUB_TOKEN=${GITHUB_TOKEN}
```

### 3.4 Dépendances système

| Outil | Version | Utilisation |
|-------|---------|-------------|
| bash | 5.x | Scripts orchestrateur |
| jq | 1.6+ | Parsing JSON (Notion API, résultats implement-auto) |
| curl | 7.x | Appels API Notion |
| git | 2.x | Worktrees, push, branches |
| gh | 2.x | GitHub CLI — création de PRs |
| claude | latest | Claude Code CLI — exécution implement-auto |
| timeout | coreutils | Guard timeout par tâche |

---

## §4 — Critères d'acceptation

### Infrastructure

- [ ] `pipeline-runner.sh` s'exécute sans erreur en l'absence de tâches Notion (cycle vide = exit propre)
- [ ] Le verrou (lockfile) empêche deux instances simultanées
- [ ] Le trap EXIT nettoie le lockfile même en cas de crash
- [ ] Le cron OpenClaw déclenche le pipeline toutes les 30 minutes
- [ ] Les logs sont écrits dans des fichiers séparés et horodatés

### Guards & Sécurité

- [ ] Le kill switch arrête le pipeline immédiatement (fichier sentinelle)
- [ ] Le health check détecte et marque les tâches interrompues après crash/reboot
- [ ] L'auth check détecte une session Claude Code expirée et notifie
- [ ] Le pipeline s'arrête après 3 échecs consécutifs
- [ ] Le pipeline s'arrête si le quota est insuffisant (3 méthodes)
- [ ] Le timeout de 20 minutes par tâche est respecté

### Exécution des tâches

- [ ] Le tri priorité + complexité fonctionne (P0 simple en premier)
- [ ] `run-task.sh` produit un JSON résultat même si Claude Code crash (fallback)
- [ ] Le worktree est créé depuis `origin/main` à jour (fan-out)
- [ ] Une tâche SUCCESS génère : push + PR + Notion "En review" + notification ✅
- [ ] Une tâche PARTIAL génère : push + PR draft + Notion "En review (partiel)" + notification ⚠️
- [ ] Une tâche FAILED génère : cleanup worktree + Notion "Échoué" + notification ❌
- [ ] Le body de la PR contient les métriques, checks, warnings, et lien Feature Document

### Quota

- [ ] `quota-checker.sh` détecte un throttle dans les logs Claude Code (pattern matching)
- [ ] Le cooldown post-throttle est respecté (30 minutes)
- [ ] Le tracking interne comptabilise les tâches dans la fenêtre glissante 5h

---

## §5 — Risques et Mitigations

| # | Risque | Probabilité | Impact | Mitigation |
|---|--------|------------|--------|------------|
| R1 | Quota estimation incorrecte (trop conservateur → peu de tâches traitées) | Haute | Moyen | Ajuster les seuils après quelques runs réels. Commencer large et réduire. |
| R2 | Quota estimation incorrecte (trop laxiste → throttle fréquent) | Moyenne | Moyen | Détection réactive (grep logs) + cooldown 30min. Le throttle n'est pas destructif, juste bloquant. |
| R3 | Session Claude Code expire pendant le weekend | Faible | Bloquant | Auth check en début de cycle + notification immédiate + procédure SSH documentée. |
| R4 | PR body trop long (GitHub limite ~65K chars) | Faible | Faible | Tronquer si nécessaire, renvoyer vers le Feature Document. |
| R5 | Notion API rate limit (trop de updates par cycle) | Faible | Moyen | Max 5 tâches par cycle = ~15-20 appels API max. Bien en dessous de la limite Notion (3 requests/second). |
| R6 | `git push` échoue (branche protégée ou conflit) | Moyenne | Moyen | Vérifier settings GitHub en amont : branches `feature/*` non protégées. En cas d'échec, marquer FAILED + notifier. |
| R7 | Conflit entre deux PRs sur même fichier | Moyenne | Moyen | Body PR inclut la liste des fichiers. L'humain décide l'ordre de merge. |
| R8 | Claude Code ne produit pas le JSON résultat | Moyenne | Moyen | Fallback JSON dans run-task.sh. La tâche est marquée FAILED avec les logs Claude disponibles. |
| R9 | VPS instable (reboot fréquents) | Faible | Moyen | Health check robuste. Le pipeline reprend au prochain cycle cron. Les worktrees sales sont nettoyés. |

---

## §6 — Hors scope

| Élément | Spec / Raison |
|---------|---------------|
| Skill implement-auto | SPEC-01 |
| Structure base Notion + export brainstorm | SPEC-03 |
| Bot Telegram + heartbeat + kill switch (implémentation) | SPEC-04 |
| Auto-merge des PRs | Hors scope V1 — review humaine obligatoire |
| Exécution parallèle de tâches | Hors scope V1 — exploration V2 |
| Dashboard web de monitoring | Hors scope V1 — Notion + Telegram suffisent |
| Continuous deployment | Hors scope — pipeline s'arrête à la PR |

---

## Annexe A — Diagramme de séquence complet

```
OpenClaw Cron              pipeline-runner.sh          run-task.sh         Claude Code          Notion             GitHub           Telegram
     │                           │                        │                    │                  │                  │                 │
     │──── trigger ──────────────▶│                        │                    │                  │                  │                 │
     │                           │                        │                    │                  │                  │                 │
     │                           │── check lockfile       │                    │                  │                  │                 │
     │                           │── check killswitch     │                    │                  │                  │                 │
     │                           │── check claude auth ───┼────────────────────▶ "Reply OK" ──────│                  │                 │
     │                           │◀─ OK ─────────────────┼────────────────────│                  │                  │                 │
     │                           │                        │                    │                  │                  │                 │
     │                           │── health check ────────┼────────────────────┼──── query ──────▶│                  │                 │
     │                           │◀─ orphaned tasks ──────┼────────────────────┼──── update ─────▶│                  │                 │
     │                           │                        │                    │                  │                  │                 │
     │                           │── query "À faire" ─────┼────────────────────┼──── query ──────▶│                  │                 │
     │                           │◀─ sorted tasks ────────┼────────────────────┼──────────────────│                  │                 │
     │                           │                        │                    │                  │                  │                 │
     │                           │── foreach task:        │                    │                  │                  │                 │
     │                           │   ├── quota check      │                    │                  │                  │                 │
     │                           │   ├── notion "En cours"┼────────────────────┼──── update ─────▶│                  │                 │
     │                           │   ├── notify 🚀 ───────┼────────────────────┼──────────────────┼──────────────────┼────── send ────▶│
     │                           │   │                    │                    │                  │                  │                 │
     │                           │   ├── run-task.sh ────▶│                    │                  │                  │                 │
     │                           │   │                    │── git fetch main   │                  │                  │                 │
     │                           │   │                    │── claude -p ──────▶│ implement-auto   │                  │                 │
     │                           │   │                    │◀─ result.json ─────│                  │                  │                 │
     │                           │   │◀── exit code ──────│                    │                  │                  │                 │
     │                           │   │                    │                    │                  │                  │                 │
     │                           │   ├── parse result     │                    │                  │                  │                 │
     │                           │   ├── git push ────────┼────────────────────┼──────────────────┼──── push ───────▶│                 │
     │                           │   ├── gh pr create ────┼────────────────────┼──────────────────┼──── PR ─────────▶│                 │
     │                           │   ├── notion update ───┼────────────────────┼──── update ─────▶│                  │                 │
     │                           │   └── notify ✅ ────────┼────────────────────┼──────────────────┼──────────────────┼────── send ────▶│
     │                           │                        │                    │                  │                  │                 │
     │                           │── heartbeat 💓 ─────────┼────────────────────┼──────────────────┼──────────────────┼────── send ────▶│
     │                           │                        │                    │                  │                  │                 │
     │                           │── release lockfile     │                    │                  │                  │                 │
     │◀──── exit ────────────────│                        │                    │                  │                  │                 │
```
