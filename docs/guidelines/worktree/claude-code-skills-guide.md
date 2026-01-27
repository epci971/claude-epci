# Claude Code : Créer des Commandes Personnalisées (Skills) avec Automatisation Git

## Table des matières
1. [Structure d'une Skill](#structure)
2. [Exécution Shell & Git](#execution-shell)
3. [Système de Hooks](#hooks)
4. [Tâches Longues en Arrière-Plan](#taches-longues)
5. [Gestion du Contexte de Travail](#contexte-travail)
6. [Exemples de Skills Git/GitHub](#exemples-git)
7. [Orchestration Multi-Étapes](#orchestration)
8. [Bonnes Pratiques](#bonnes-pratiques)

---

## <a id="structure"></a>1. Structure d'une Skill Claude Code Personnalisée

### 1.1 Répertoires et Localisation

Une skill se compose d'un répertoire avec au minimum un fichier `SKILL.md` :

```
~/.claude/skills/git-workflow/          # Skill personnelle (tous les projets)
├── SKILL.md                             # Fichier principal (obligatoire)
├── reference.md                         # Documentation détaillée (optionnel)
├── examples.md                          # Exemples d'utilisation (optionnel)
├── templates/                           
│   └── pr-template.md
└── scripts/                             
    ├── analyze-history.sh
    ├── validate-commit.py
    └── orchestrate-workflow.py

.claude/skills/git-workflow/            # Skill au niveau projet
├── SKILL.md
└── scripts/
    └── local-git-automation.sh
```

**Priorité de résolution** : Enterprise > Personal > Project > Plugin

### 1.2 Structure du fichier SKILL.md

Chaque skill commence par un **YAML frontmatter** (entre `---`) suivi du contenu markdown :

```yaml
---
name: git-workflow-automation
description: "Automate complex git workflows: explore repo history, plan changes, implement with git branches, test, and create PRs. Use when doing multi-step development tasks or managing git workflows."
context: fork                            # (optionnel) Isolate in subagent
agent: Plan                              # (optionnel) Agent type: Explore, Plan, general-purpose
disable-model-invocation: true           # (optionnel) Manual invocation only
user-invocable: true                     # (optionnel) Show in / menu
allowed-tools: "Read,Grep,Bash(git:*),Bash(gh:*)"  # Outils autorisés
hooks:                                   # (optionnel) Scoped hooks
  PostToolUse:
    - matcher: "Bash"
      hooks:
        - type: "command"
          command: "./.claude/hooks/validate-git.sh"
---

# Git Workflow Automation

Your skill instructions here...

## Resources
- [Reference guide](reference.md)
- [Examples](examples.md)
```

### 1.3 Frontmatter Fields

| Champ | Obligatoire | Description |
|-------|-------------|-------------|
| `name` | Non | Identificateur de la skill (kebab-case, max 64 caractères) |
| `description` | Recommandé | Quand utiliser la skill. Claude utilise ceci pour l'activation auto. |
| `argument-hint` | Non | Indice d'autocomplétion. Ex: `[issue-number]` |
| `disable-model-invocation` | Non | `true` = invocation manuelle seulement (via `/skill-name`) |
| `user-invocable` | Non | `false` = cachée du menu `/` mais Claude peut l'invoquer |
| `allowed-tools` | Non | Outils accessibles sans permission. Ex: `"Bash(git:*),Read,Grep"` |
| `model` | Non | Modèle spécifique pour cette skill |
| `context` | Non | `fork` = exécute isolée dans un subagent |
| `agent` | Non | Type d'agent: `Explore`, `Plan`, `general-purpose` |
| `hooks` | Non | Hooks scoped à cette skill |

### 1.4 Variables de Substitution

Dans le contenu markdown, utilisez :

| Variable | Description |
|----------|-------------|
| `$ARGUMENTS` | Tous les arguments passés à la skill |
| `$ARGUMENTS[0]`, `$0` | Premier argument |
| `$ARGUMENTS[1]`, `$1` | Deuxième argument, etc. |
| `${CLAUDE_SESSION_ID}` | ID de session unique |

**Exemple** :
```yaml
---
name: fix-github-issue
description: Fix a GitHub issue by number
---

Fix GitHub issue #$0 following team standards:

1. Read the issue
2. Plan the fix
3. Implement changes
4. Write tests
5. Create commit with message referencing #$0
```

Utilisation : `/fix-github-issue 123`

---

## <a id="execution-shell"></a>2. Exécution de Commandes Shell (Git, GitHub CLI)

### 2.1 Restrictions des Outils

Le champ `allowed-tools` contrôle strictement quels outils Claude peut utiliser **sans demander permission** :

```yaml
---
name: git-explorer
description: Explore git history and branches
allowed-tools: "Bash(git:*),Read,Grep"
---
```

**Pattern matching disponibles** :

```yaml
# ✅ Git uniquement
allowed-tools: "Bash(git:*)"

# ✅ GitHub CLI uniquement  
allowed-tools: "Bash(gh:*)"

# ✅ Git ET GitHub CLI
allowed-tools: "Bash(git:*),Bash(gh:*)"

# ❌ MAUVAIS - Trop large
allowed-tools: "Bash"

# ✅ Combinaisons courantes pour git workflows
allowed-tools: "Bash(git:*),Bash(gh:*),Read,Grep,Edit"

# ✅ Lecture seule + git
allowed-tools: "Bash(git:*),Read,Grep,Glob"
```

### 2.2 Injection de Contexte Dynamique

Utilisez la syntaxe `!`command`` pour injecter des résultats shell **avant** que Claude ne voie le contenu :

```yaml
---
name: pr-summarizer
description: Summarize the current pull request
context: fork
agent: Explore
allowed-tools: "Bash(gh:*)"
---

## PR Context

**Diff:**
!`gh pr diff`

**Comments:**
!`gh pr view --json comments -q '.comments[].body'`

**Changed files:**
!`gh pr diff --name-only`

## Your task
Summarize this PR in 3 bullet points, highlighting key changes.
```

**Execution flow** :
1. Chaque `!`command`` s'exécute immédiatement (AVANT que Claude voit le contenu)
2. Le résultat remplace le placeholder
3. Claude reçoit le contenu complètement rendu avec vraies données

### 2.3 Contrôle du Contexte Bash

Claude maintient le contexte bash **au sein d'une skill** :

```yaml
---
name: multi-step-git-task
allowed-tools: "Bash(git:*),Read"
---

1. Check current branch:
   `git branch -v`

2. Create feature branch from results above:
   `git checkout -b feature/my-feature`

3. See files changed from main:
   `git diff --name-only main`

4. Create directory for changes:
   `mkdir -p src/features && cd src/features`

5. Read existing files in this directory:
   The `pwd` from step 4 is active, so file reads will be from src/features/
```

**Important** : La session bash persiste dans une seule exécution de skill. Entre appels de skills, le contexte est réinitialisé.

### 2.4 Pattern : Orchestration Git Manuelle vs Automatique

```yaml
---
name: semi-automated-git
description: Manual git workflow with validation
allowed-tools: "Bash(git:*),Read,Edit"
disable-model-invocation: true
---

## Manual Git Workflow

1. **Branch creation** - You control the branch name:
   \`cd $HOME/project && git checkout -b user/$0\`

2. **Stage and review changes**:
   \`git status\`
   \`git diff\`

3. **Claude validates**:
   - Read modified files
   - Check against team standards
   - Suggest fixes
   
4. **You decide on commit**:
   \`git add .\`
   \`git commit -m "feat: $1"\`
```

---

## <a id="hooks"></a>3. Système de Hooks Claude Code

### 3.1 Événements Disponibles

Les hooks s'enregistrent au niveau projet (`~/.claude/settings.json`) ou skill :

| Événement | Moment | Utilisé pour |
|-----------|--------|-------------|
| `PreToolUse` | AVANT l'exécution d'un outil | Validation, blocage, feedback |
| `PostToolUse` | APRÈS l'exécution d'un outil | Formatting, validation, logging |
| `PreCompact` | AVANT compactage de contexte | Nettoyage préalable |
| `PermissionRequest` | Quand permission demandée | Auto-allow/deny selon règles |
| `UserPromptSubmit` | Avant traitement du prompt | Injection de contexte |
| `Notification` | Quand notification envoyée | Redirect vers système de notif |
| `Stop` | Fin de réponse Claude | Cleanup, reporting |
| `SubagentStop` | Fin d'une tâche subagent | Collecte de résultats |
| `Setup` | Initialisation Claude Code | Configuration spéciale |
| `SessionStart` | Début de session | Setup initial |
| `SessionEnd` | Fin de session | Cleanup, logging |

### 3.2 Configuration des Hooks

**Niveau projet** (`.claude/settings.json`) :

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit",
        "hooks": [
          {
            "type": "command",
            "command": "npx prettier --write $FILE_PATH"
          }
        ]
      }
    ],
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "./.claude/hooks/validate-git-command.sh"
          }
        ]
      }
    ]
  }
}
```

**Niveau skill** (SKILL.md frontmatter) :

```yaml
---
name: auto-format-on-change
hooks:
  PostToolUse:
    - matcher: "Write|Edit"
      hooks:
        - type: "command"
          command: "python3 ./.claude/hooks/auto-format.py"
---
```

### 3.3 Accès aux Données du Hook

Les hooks reçoivent un objet JSON via `stdin` contenant le contexte :

```bash
#!/bin/bash
# Hook script example

input=$(cat)
echo "$input" | jq .

# Extract specific fields:
tool_used=$(echo "$input" | jq -r '.tool')
file_path=$(echo "$input" | jq -r '.tool_input.file_path')
command=$(echo "$input" | jq -r '.tool_input.command')
```

**Exemple complet** : Hook de validation git

```bash
#!/usr/bin/env bash
# .claude/hooks/validate-git-command.sh

set -e

input=$(cat)
command=$(echo "$input" | jq -r '.tool_input.command // empty')

# Block dangerous git operations
if echo "$command" | grep -qE "^git (push|force-push|reset.*--hard|rebase.*-f)"; then
  echo "❌ Dangerous git command blocked: $command"
  echo "Use /review before running this command"
  exit 2  # Exit code 2 = BLOCK operation
fi

echo "✓ Git command allowed: $command"
exit 0
```

### 3.4 Hook PostToolUse pour Orchestration

Pour les workflows multi-étapes, utilisez PostToolUse avec `context: fork` :

```yaml
---
name: full-git-workflow
context: fork
agent: Plan
disabled-model-invocation: true
hooks:
  PostToolUse:
    - matcher: "Bash"
      hooks:
        - type: "command"
          command: |
            #!/bin/bash
            input=$(cat)
            exit_code=$(echo "$input" | jq -r '.tool_exit_code')
            if [ "$exit_code" -ne 0 ]; then
              echo "⚠️ Command failed, stopping workflow"
              exit 2
            fi
---

# Full Git Workflow

1. **Explore** - Read project structure and git history
2. **Plan** - Determine optimal branch and change strategy
3. **Implement** - Create branch and make changes
4. **Validate** - Run tests
5. **Create PR** - Push and create GitHub PR

Each step depends on the previous succeeding.
```

---

## <a id="taches-longues"></a>4. Lancer des Tâches Longues en Arrière-Plan

### 4.1 Pattern : Subagent avec Context Fork

Pour les tâches qui prennent du temps, utilisez `context: fork` :

```yaml
---
name: deep-code-analysis
description: Run comprehensive code analysis in background
context: fork
agent: Explore
allowed-tools: "Bash(find:*),Bash(grep:*),Read,Glob,Grep"
disable-model-invocation: false
---

## Deep Code Analysis Task

Analyze the entire codebase:

1. Find all TypeScript files:
   \`find . -name "*.ts" -not -path "*/node_modules/*"\`

2. Analyze imports and dependencies:
   \`grep -r "^import\|^export" --include="*.ts" .\`

3. Identify unused exports:
   \`grep -r "^export " --include="*.ts" . | sort -u > /tmp/exports.txt\`
   \`grep -r "from.*" --include="*.ts" . | sort -u > /tmp/imports.txt\`

4. Compare and report orphaned exports

Provide a detailed report with:
- Total files analyzed
- Critical imports
- Potential dead code
- Recommendations
```

**Exécution** :
- Claude crée un contexte isolé (fork)
- Reçoit le contenu comme prompt
- Utilise l'agent `Explore` (read-only)
- Les résultats sont rapportés et intégrés

### 4.2 Bash Background Execution

Pour lancer vraiment en arrière-plan :

```bash
#!/bin/bash
# Run a task asynchronously

nohup python3 -u ./long-running-analysis.py > /tmp/analysis.log 2>&1 &
echo $! > /tmp/analysis.pid

echo "Analysis started (PID: $(cat /tmp/analysis.pid))"
echo "Check progress: tail -f /tmp/analysis.log"
```

Puis dans la skill :

```yaml
---
name: start-async-analysis
disabled-model-invocation: true
allowed-tools: "Bash"
---

Start a long-running analysis:

\`bash ./.claude/scripts/start-analysis.sh\`

The process runs independently. You can check status:

\`
test -f /tmp/analysis.pid && echo "Running (PID: $(cat /tmp/analysis.pid))" || echo "Not running"
\`

Check results:
\`
tail -20 /tmp/analysis.log
\`

Wait for completion:
\`
[ -f /tmp/analysis.pid ] && wait $(cat /tmp/analysis.pid) && echo "Done" || echo "Not running"
\`
```

---

## <a id="contexte-travail"></a>5. Gestion du Contexte de Travail (Répertoires, Worktrees)

### 5.1 Changements de Répertoire dans une Skill

Le contexte bash persiste **au sein d'une skill exécution unique** :

```yaml
---
name: monorepo-package-edit
description: Edit a specific package in a monorepo
allowed-tools: "Bash(git:*),Read,Edit,Glob"
---

## Monorepo Package Workflow

Argument: package name (e.g., `/monorepo-package-edit api`)

1. **Navigate to package**:
   \`cd packages/$0\`
   \`pwd\`

2. **Check status**:
   \`git status\`

3. **Read package.json**:
   The current directory is \`packages/$0\`, so:
   \`cat package.json\`

4. **Make edits**:
   Files edited will be relative to \`packages/$0\`

5. **Verify changes**:
   \`git diff\`
```

### 5.2 Worktrees Git

Pour travailler avec plusieurs branches en parallèle :

```yaml
---
name: git-worktree-manager
description: Create and manage git worktrees for parallel development
allowed-tools: "Bash(git:*),Read"
disable-model-invocation: true
---

## Git Worktree Management

### Create new worktree:
\`
git worktree add -b feature/$1 ../worktree-$1
cd ../worktree-$1
pwd
\`

### List worktrees:
\`git worktree list\`

### Remove worktree:
\`
cd <original-dir>
git worktree remove ../worktree-$0
\`

### Switch between worktrees:
\`
cd ../worktree-$0
git status
\`

The working directory persists within this skill execution.
```

### 5.3 Pattern : Skills pour Différentes Branches

```yaml
---
name: feature-editor
description: Edit feature branch with worktree isolation
allowed-tools: "Bash(git:*),Edit,Read"
---

Work on feature branch $0:

1. Create isolated worktree:
   \`git worktree add -b feat/$0 ../wt-$0\`
   \`cd ../wt-$0 && pwd\`

2. Get parent directory path for reference:
   PARENT: \`cd ../.. && pwd\`

3. Edit files:
   Make your edits here in the worktree

4. Commit changes:
   \`git add . && git commit -m "feat: $0"\`

5. Return to main repo:
   \`cd ../.. && git worktree remove ../wt-$0\`
   \`git log --oneline main | head -1\`
```

---

## <a id="exemples-git"></a>6. Exemples de Skills Intégrant Git/GitHub

### 6.1 Git History Explorer

```yaml
---
name: git-history-explorer
description: Explore git history to answer questions about code changes, authorship, and feature development timeline
allowed-tools: "Bash(git:*),Read,Grep"
context: fork
agent: Explore
---

# Git History Explorer

Analyze the git history to answer questions about:
- Feature timeline
- Author contributions
- Commit patterns
- Branch strategies

## Available commands
- \`git log --oneline --graph --all\` - Full history
- \`git log -S "keyword" --oneline\` - Find commits changing specific code
- \`git blame <file>\` - See who changed each line
- \`git show <commit>\` - Detailed commit info
- \`git diff <commit1> <commit2>\` - Compare versions

Question to answer: $ARGUMENTS
```

### 6.2 GitHub PR Manager

```yaml
---
name: gh-pr-manager
description: Create, review, and manage GitHub pull requests
allowed-tools: "Bash(gh:*),Read,Grep"
disable-model-invocation: true
argument-hint: "[action] [arguments]"
---

## GitHub PR Manager

Actions: create, review, list, merge, close

### Create PR:
\`/gh-pr-manager create "feature title" "description"\`

\`gh pr create --title "$0" --body "$1"\`

### Review current PR:
\`gh pr view\`
\`gh pr view --json commits,comments\`

### List open PRs:
\`gh pr list --state open\`

### Merge PR:
\`gh pr merge $0 --squash\`

### Close PR:
\`gh pr close $0\`
```

### 6.3 Commit Message Generator

```yaml
---
name: commit-composer
description: Generate semantic commit messages based on staged changes
allowed-tools: "Bash(git:*),Read,Grep"
context: fork
agent: Explore
---

# Semantic Commit Composer

Analyze staged changes and suggest a proper semantic commit message.

## Step 1: Review changes
\`git diff --staged\`

## Step 2: Categorize changes
Based on the diff, determine:
- Type: feat, fix, refactor, docs, test, perf, ci, style, chore
- Scope: area of codebase affected
- Breaking change: yes/no

## Step 3: Suggest message format
[type]([scope]): [subject]

[body]

[footer]

Follow conventional commits standard (https://www.conventionalcommits.org/)
```

### 6.4 Multi-Step Git Workflow (Explore → Plan → Code → Test → PR)

```yaml
---
name: full-feature-workflow
description: Complete feature development workflow from exploration to PR creation
context: fork
agent: Plan
allowed-tools: "Bash(git:*),Bash(gh:*),Read,Edit,Grep"
disable-model-invocation: false
---

# Full Feature Development Workflow

Argument: feature name (e.g., `/full-feature-workflow user-auth`)

## Phase 1: Explore (Read-only Analysis)

\`git log --oneline --graph -20\`
\`git branch -a\`

Understand:
- Current project structure
- Existing patterns
- Related branches

## Phase 2: Plan

Based on exploration:
- Design the feature
- Identify files to modify
- Plan testing strategy
- List implementation steps

## Phase 3: Implement

\`git checkout -b feat/$0\`

Create and edit necessary files. Ensure:
- Code follows project patterns
- New functionality is clear
- Comments explain why not how

## Phase 4: Test

\`npm test -- --changed\`

Verify:
- All tests pass
- No regressions
- New functionality works

## Phase 5: Create PR

\`
git add .
git commit -m "feat: $0"
git push origin feat/$0
gh pr create --title "Feature: $0" --body "Implements $0 functionality"
\`

Provide PR link and summary.
```

---

## <a id="orchestration"></a>7. Orchestration Multi-Étapes

### 7.1 Pattern : Sequential Execution avec Context Fork

```yaml
---
name: code-audit-workflow
description: Run multi-stage code audit
context: fork
agent: Plan
allowed-tools: "Bash(find:*),Read,Grep,Glob"
---

# Code Audit Workflow

## Stage 1: Collect Metrics

\`
find . -name "*.ts" -not -path "*/node_modules/*" | wc -l
\`

\`
find . -name "*.test.ts" -not -path "*/node_modules/*" | wc -l
\`

## Stage 2: Analyze Dependencies

\`grep -r "^import\|^export" --include="*.ts" . | head -50\`

## Stage 3: Check Code Quality Issues

\`grep -r "TODO\|FIXME\|HACK" --include="*.ts" . | wc -l\`

## Stage 4: Generate Report

Summarize:
- Codebase size
- Test coverage ratio
- Dependency complexity
- Technical debt indicators
- Recommendations for improvement
```

### 7.2 Pattern : Orchestration via PostToolUse Hooks

```yaml
---
name: ci-like-workflow
disabled-model-invocation: true
hooks:
  PostToolUse:
    - matcher: "Bash"
      hooks:
        - type: "command"
          command: |
            #!/bin/bash
            data=$(cat)
            exit_code=$(echo "$data" | jq -r '.tool_exit_code')
            if [ "$exit_code" -ne 0 ]; then
              echo "::error::Step failed with exit code $exit_code"
              exit 2
            fi
---

# CI-Like Workflow

1. **Install dependencies**:
   \`npm ci\`

2. **Lint**:
   \`npm run lint\`
   (Hook validates exit code)

3. **Unit tests**:
   \`npm test\`
   (Hook validates exit code)

4. **Build**:
   \`npm run build\`
   (Hook validates exit code)

5. **Report**:
   All steps completed successfully!
```

### 7.3 Subagent Delegation Pattern

```yaml
---
name: code-review-orchestrator
disabled-model-invocation: true
---

# Code Review Orchestration

Use specialized subagents for different review aspects:

## Syntax Check
/review-syntax

## Performance Review
/review-performance

## Security Audit
/review-security

## Documentation Review
/review-documentation

Aggregate findings and provide consolidated review.
```

---

## <a id="bonnes-pratiques"></a>8. Bonnes Pratiques pour Skills Git/GitHub

### 8.1 Conception

✅ **DO** :
- Utiliser `description` précise et keyword-friendly
- Déclarer `allowed-tools` de façon restrictive
- Penser au contexte d'invocation (auto vs manual)
- Segmenter les responsabilités (une skill = une tâche)

❌ **DON'T** :
- Utiliser `allowed-tools: "Bash"` (trop large)
- Mélanger read-only et write operations dans une skill
- Ignorer les fichiers de support (reference.md, examples.md)

### 8.2 Exécution Shell

✅ **DO** :
- Utiliser `!`command`` pour injecter du contexte dynamique
- Valider les résultats bash avant continuation
- Utiliser `set -e` dans les scripts d'orchestration
- Tester les hooks avec `/hooks` et vérifier `~/.claude/settings.json`

❌ **DON'T** :
- Lancer des commandes longues sans feedback
- Supposer le contexte bash persiste entre skills
- Utiliser `git push` sans confirmation
- Oublier les sorties de secours (exit codes)

### 8.3 Git Workflow Best Practices

✅ **DO** :
- Créer des branches feature avec convention claire (`feat/`, `fix/`, `refactor/`)
- Utiliser conventional commits
- Employer worktrees pour travail parallèle
- Documenter le workflow dans CLAUDE.md

❌ **DON'T** :
- Force push sans raison
- Commitn'importe quoi sans message sémantique
- Mélanger features dans une même branche
- Oublier de stagner avant commit

### 8.4 Context Management

✅ **DO** :
- Utiliser `context: fork` pour isolation
- Choisir l'agent approprié (`Explore` pour read-only, `Plan` pour analyse)
- Partager l'état entre étapes via `!`command``
- Documenter les dépendances entre étapes

❌ **DON'T** :
- Supposer l'ordre d'exécution sans `context: fork`
- Lancer des subagents sans clear prompt
- Ignorer les résultats de subagent

### 8.5 Sécurité

✅ **DO** :
- Bloquer les commandes dangereuses avec hooks `PreToolUse`
- Utiliser `Bash(git:*)` au lieu de `Bash`
- Implémenter des validations dans `.claude/hooks/`
- Auditer les changements avant push

❌ **DON'T** :
- Permettre à Claude de `git push` sans validation
- Ignorer `exit 2` dans les hooks (=block)
- Passer des credentials dans les commandes
- Autoriser les reset/rebase forcés

### 8.6 Debugging & Logging

✅ **DO** :
- Utiliser `${CLAUDE_SESSION_ID}` pour logging
- Implémenter des hooks PostToolUse pour logging
- Vérifier les configurations avec `/hooks`
- Garder `.claude/bash-command-log.txt` pour audit

❌ **DON'T** :
- Oublier les logs en production
- Ignorer les exit codes
- Supposer les commandes réussissent silencieusement

---

## Ressources Supplémentaires

### Documentation Officielle (2025-2026)
- **Claude Code Skills** : https://code.claude.com/docs/en/skills
- **Claude Code Hooks** : https://code.claude.com/docs/en/hooks-guide
- **Slash Commands** : https://code.claude.com/docs/en/slash-commands

### Communauté & Articles
- **Claude Agent Skills Deep Dive** : Lee Hanchung (Oct 2025)
- **Skills Auto-Activation via Hooks** : Paddo Dev (Nov 2025)
- **Claude Code Best Practices** : Anthropic Engineering (Apr 2025)

### Patterns Validés en Production
- **SuperClaude** : 20.1k⭐ - 30+ commandes personnalisées
- **Claude-Flow** : Multi-agent orchestration
- **Hook-based Skill Activation** : File pattern matching

---

**Dernière mise à jour** : January 2026  
**Sources** : Documentation officielle Anthropic + Retours développeurs 2025-2026