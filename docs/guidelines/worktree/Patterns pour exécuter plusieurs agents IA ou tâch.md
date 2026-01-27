<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# Patterns pour exécuter plusieurs agents IA ou tâches de développement en parallèle.

Contexte : lancer plusieurs features en parallèle, chacune dans son worktree, avec son instance de traitement.

Rechercher :

- Tmux/screen pour sessions parallèles avec Claude Code
- GNU parallel pour orchestration de tâches
- Patterns de queue/job pour tâches de développement
- Synchronisation et reporting de plusieurs tâches concurrentes
- Gestion des ressources (CPU, mémoire) avec plusieurs instances

Focus développeur solo gérant plusieurs features simultanément.

Tu peux te donner un gros boost en traitant chaque feature comme un “mini‑projet” isolé (worktree + session + instance d’IA), avec une petite couche d’orchestration pour lancer, monitorer et tuer tout ça proprement.[^1_1]

## Organisation des worktrees + tmux

Idée de base : 1 feature = 1 worktree = 1 session tmux nommée, préconfigurée avec tes fenêtres/panes (serveur, tests, Claude Code/CLI, logs…).[^1_2][^1_3]
Exemple de script `dev-feature` :

```bash
#!/usr/bin/env bash
set -euo pipefail

TICKET="$1"                # ex: ABC-123
DESC="${2:-description}"   # ex: add-login
BRANCH="feature/${TICKET}-${DESC}"
WT_DIR="../worktrees/${TICKET}"
SESSION="${TICKET}"

# 1. Worktree + branche
if [ ! -d "$WT_DIR" ]; then
  git worktree add -b "$BRANCH" "$WT_DIR" origin/main
fi

# 2. Session tmux idempotente
tmux has-session -t "$SESSION" 2>/dev/null || {
  tmux new-session  -d -s "$SESSION" -c "$WT_DIR" -n "editor"
  tmux new-window      -t "$SESSION" -c "$WT_DIR" -n "server"
  tmux new-window      -t "$SESSION" -c "$WT_DIR" -n "tests"
  tmux new-window      -t "$SESSION" -c "$WT_DIR" -n "ai"
  tmux send-keys -t "$SESSION:server" "npm run dev" C-m
}

tmux attach -t "$SESSION"
```

Ce pattern “script → session template” est classique pour gérer plusieurs projets/sessions tmux en parallèle.[^1_2][^1_4][^1_5]

## Sessions parallèles + Claude / agents

Tu peux garder un “main” tmux pour ton infra perso, et une session par feature où tu ouvres Claude Code / autre agent sur le worktree correspondant.[^1_3][^1_1]

Quelques patterns utiles côté multi‑agents / IA :

- 1 onglet/instance IA par feature, même contexte git, prompts standardisés (template “dev assistant pour feature X”).[^1_1]
- “Parallel preparation with checkpoints” : à la fin d’une phase (implémentation, refacto), tu ouvres une nouvelle conversation IA pour review/tests/doc pendant que tu passes à la feature suivante.[^1_1]
- Réserver les sub‑agents aux tâches vraiment séparables (review sécurité, perf, doc) au lieu de multiplier les “gros” agents qui se marchent dessus.[^1_6][^1_1]


## Orchestration shell avec GNU parallel

Pour tout ce qui est tâches batch sur plusieurs worktrees (tests, lint, build, migrations de schémas…), `gnu parallel` est parfait.[^1_7][^1_8]

Exemple : lancer les tests pour toutes les features actives :

```bash
#!/usr/bin/env bash
set -euo pipefail

_WORKTREES=(ABC-123 DEF-456 XYZ-789)

printf '%s\n' "${_WORKTREES[@]}" \
  | parallel -j4 --eta "cd ../worktrees/{}/project && pnpm test"
```

Points clés à exploiter :

- `-j+0` pour “nombre de jobs = nombre de CPU” ou fixer `-j4` si tu veux garder des ressources pour l’IDE/IA.[^1_9][^1_7]
- `--eta`, `--progress` pour du reporting clair en ligne de commande.[^1_9][^1_7]
- `--results` ou redirection vers des fichiers par feature (`logs/{}/tests.log`) pour centraliser le reporting.[^1_7]

Tu peux aussi wrapper tes opérations récurrentes (lint, build, e2e) dans des fonctions shell et les passer à `parallel`.[^1_7]

## Pattern “job queue” local pour tâches de dev

Si tu veux séparer “je planifie les tâches” / “je les exécute”, tu peux te faire une mini‑queue locale plutôt que partir direct sur Kafka/RabbitMQ.[^1_10]

Quelques options pragmatiques pour un solo dev :

- Fichier `jobs.txt` + `parallel` : chaque ligne = “commande à exécuter + worktree”, puis `parallel --joblog joblog.txt < jobs.txt`.[^1_7]
- Un script `enqueue-job` qui ajoute une tâche (ex : “rebuild docs feature ABC-123”) dans un fichier, et un `job-runner` qui lit ça en boucle et exécute avec `parallel --pipe`.[^1_7]
- Si tu veux aller un cran plus loin (Node), une lib de queue simple type Bee‑Queue sur Redis pour orchestrer des jobs de build/tests sur plusieurs projets.[^1_11][^1_10]

Pattern conceptuel : state durable (fichier/DB) + exécuteur idempotent qui lit la queue, exécute, marque “done/failed” et loggue le résultat.[^1_11][^1_10]

## Synchronisation, reporting et ressources

Pour ne pas te cramer le CPU/RAM en multicouche (plusieurs worktrees + IA + navigateurs) :

- Limite stricte de jobs parallèles pour les tâches lourdes (`parallel -j 2` pour build/tests).[^1_9][^1_7]
- Réserve 1–2 cœurs pour l’IDE/agents IA (ne jamais saturer tous les cœurs avec `parallel`).[^1_12]
- Utilise les joblogs de `parallel` (`--joblog log.txt`) pour suivre durée/exit code par tâche et identifier les jobs qui plombent la machine.[^1_7]

Pour la synchro entre tâches parallèles :

- Regrouper la sortie par job pour garder des logs lisibles (comportement par défaut de `parallel`, sinon `--line-buffer`/`-u` selon le besoin).[^1_7]
- Standardiser les chemins de logs par feature (`../worktrees/TICKET/.logs/*`), et faire un petit script “dashboard” qui affiche l’état de chaque feature (branche, PR ouverte ?, derniers tests, erreurs récentes).[^1_1][^1_7]

Si tu veux, je peux te proposer un mini “starter kit” :

- un script `feature-start` (worktree + tmux + IA),
- un `feature-status` (tableau des features avec état tests/build/PR),
- un `feature-run-all` basé sur `gnu parallel`.
<span style="display:none">[^1_13][^1_14][^1_15][^1_16][^1_17][^1_18][^1_19]</span>

<div align="center">⁂</div>

[^1_1]: tools.github_cli_and_git_worktrees

[^1_2]: projects.git_worktrees_automation

[^1_3]: https://www.webuild-ai.com/insights/five-workflow-patterns-to-multiply-your-development-capacity-with-ai-coding-assistants

[^1_4]: preferences.branch_naming_convention

[^1_5]: https://zolmok.org/tmux-multiple-projects-sessions/

[^1_6]: https://www.hostmycode.in/tutorials/use-tmux-for-managing-multiple-server-sessions

[^1_7]: https://stackoverflow.com/questions/54628034/how-can-i-create-multiple-tmux-sessions-containing-windows-from-command-line

[^1_8]: https://martinwood.org/managing-multiple-projects-with-tmuxinator

[^1_9]: https://www.perplexity.ai/search/f80481c2-2754-489a-9a0f-05011be1cb03

[^1_10]: https://www.gnu.org/software/parallel/parallel_examples.html

[^1_11]: https://www.gnu.org/software/parallel/parallel_tutorial.html

[^1_12]: https://gist.github.com/drmalex07/de8ff1379a560f6d84a0d863e60ae378

[^1_13]: https://news.ycombinator.com/item?id=43993982

[^1_14]: https://github.com/bee-queue/bee-queue

[^1_15]: https://blog.ronin.cloud/gnu-parallel/

[^1_16]: https://dev.to/iamadhee/tmux-multitasking-with-your-command-line-36of

[^1_17]: https://www.lullabot.com/articles/multiple-terminal-panes-tmux

[^1_18]: https://stackoverflow.com/questions/56263335/job-queue-with-job-affinity

[^1_19]: https://www.youtube.com/watch?v=-LyODsypGHI

