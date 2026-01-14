# Git Worktrees + Claude Code : Guide Complet pour le Développement Parallèle

## 📋 Vue d'ensemble

L'utilisation des **Git worktrees** avec **Claude Code** représente une évolution majeure dans les workflows de développement assisté par IA. Cette approche permet de transformer un développeur solo en un "chef d'orchestre" orchestrant plusieurs flux de développement IA en parallèle.

### Pourquoi cette combinaison est puissante

| Problème traditionnel | Solution avec Worktrees |
| --- | --- |
| Context switching coûteux (10-15 min) | Pas de stash, pas de changement de branche |
| Une seule tâche à la fois | Plusieurs features en parallèle |
| Conflits entre instances Claude | Isolation totale par worktree |
| Perte de contexte IA entre tâches | Contexte préservé par worktree |

---

## 🏗️ Architecture des Worktrees

### Concept fondamental

Un **Git worktree** permet d'avoir plusieurs répertoires de travail liés au même dépôt Git, chacun sur une branche différente.

```
/Users/edouard/projects/
├── mon-projet/                    # Worktree principal (main)
│   ├── .git/                      # Le vrai dépôt Git
│   ├── src/
│   └── [CLAUDE.md](http://CLAUDE.md)
├── mon-projet-feature-auth/       # Worktree feature A
│   ├── .git                       # Fichier (lien vers .git principal)
│   ├── src/
│   └── [CLAUDE.md](http://CLAUDE.md)
├── mon-projet-feature-api/        # Worktree feature B
│   ├── .git
│   ├── src/
│   └── [CLAUDE.md](http://CLAUDE.md)
└── mon-projet-hotfix-bug123/      # Worktree hotfix
    ├── .git
    ├── src/
    └── [CLAUDE.md](http://CLAUDE.md)
```

### Avantages clés

1. **Isolation totale** : Les fichiers de chaque worktree sont indépendants
2. **Partage du .git** : Économie d'espace (pas de clone complet)
3. **Historique commun** : Tous les commits sont visibles depuis n'importe quel worktree
4. **Sessions Claude indépendantes** : Chaque Claude garde son contexte

---

## 🚀 Mise en place initiale

### Commandes de base Git Worktree

```bash
# Créer un worktree avec nouvelle branche
git worktree add ../projet-feature-auth -b feature/auth main

# Créer un worktree sur branche existante
git worktree add ../projet-bugfix bugfix/issue-123

# Lister tous les worktrees
git worktree list

# Supprimer un worktree
git worktree remove ../projet-feature-auth

# Nettoyer les références orphelines
git worktree prune
```

### Structure de nommage recommandée

```bash
# Convention : {projet}-{type}-{description}
../mon-projet-feature-auth
../mon-projet-fix-login
../mon-projet-refactor-api
../mon-projet-hotfix-urgent
```

---

## ⚡ Intégration avec EPCI (Explore → Plan → Code → Inspect)

### Phase EXPLORE : Identification des tâches parallélisables

Avant de créer des worktrees, évalue le **potentiel de conflit** :

```markdown
## Analyse de parallélisation

### Stream A - Faible risque de conflit (Backend DB)
- [ ] Migration base de données
- [ ] Nouveaux modèles Eloquent/Entity

### Stream B - Risque moyen (Data Layer)
- [ ] Installation lib fetch
- [ ] Création hooks data

### Stream C - Faible risque (Frontend isolé)
- [ ] Nouveau composant React
- [ ] Tests unitaires UI

**Règle** : Ne jamais paralléliser des tâches qui touchent les mêmes fichiers !
```

### Phase PLAN : Script d'automatisation de création

### Script [worktree.sh](http://worktree.sh)

```bash
#!/bin/bash
# [worktree.sh](http://worktree.sh) - Création automatisée de worktree pour EPCI

set -e

BRANCH_NAME=$1
REPO_NAME=$(basename "$(git rev-parse --show-toplevel)")
WORKTREE_PATH="../${REPO_NAME}-${BRANCH_NAME}"

# 1. Vérifier que la branche n'existe pas
if git show-ref --verify --quiet "refs/heads/task/${BRANCH_NAME}"; then
    echo "❌ La branche task/${BRANCH_NAME} existe déjà"
    exit 1
fi

# 2. Créer le worktree
echo "📁 Création du worktree: ${WORKTREE_PATH}"
git worktree add "${WORKTREE_PATH}" -b "task/${BRANCH_NAME}" HEAD

# 3. Copier les fichiers d'environnement
echo "📋 Copie des fichiers de configuration..."
for file in .env .envrc .env.local; do
    if [ -f "$file" ]; then
        cp "$file" "${WORKTREE_PATH}/"
    fi
done

# 4. Copier [CLAUDE.md](http://CLAUDE.md) si présent
if [ -f "[CLAUDE.md](http://CLAUDE.md)" ]; then
    cp "[CLAUDE.md](http://CLAUDE.md)" "${WORKTREE_PATH}/"
fi

# 5. Créer le dossier .llm avec todo
mkdir -p "${WORKTREE_PATH}/.llm"

# 6. Si direnv est utilisé
if command -v direnv &> /dev/null && [ -f "${WORKTREE_PATH}/.envrc" ]; then
    direnv allow "${WORKTREE_PATH}"
fi

# 7. Si mise est utilisé
if command -v mise &> /dev/null; then
    mise trust "${WORKTREE_PATH}" 2>/dev/null || true
fi

echo "✅ Worktree créé: ${WORKTREE_PATH}"
echo "📍 Branche: task/${BRANCH_NAME}"
```

### Phase CODE : Commande Claude personnalisée

### .claude/commands/[worktree.md](http://worktree.md)

```markdown
---
argument-hint: branch-name
description: Créer un worktree Git pour développement parallèle
---

Créer un worktree Git dans un répertoire adjacent.

## Arguments

L'argument doit être un nom de tâche en kebab-case (ex: "auth-feature", "api-refactor").

L'utilisateur a passé: `$ARGUMENTS`

Si le texte est déjà en kebab-case, l'utiliser directement. Sinon, générer un nom approprié.

## Étapes

1. Lire le fichier .llm/[todo.md](http://todo.md) pour trouver la prochaine tâche non commencée `- [ ]`
2. Marquer cette tâche comme en cours: `- [>] Tâche <!-- worktree: nom-branche -->`
3. Exécuter: `bash scripts/[worktree.sh](http://worktree.sh) <branch-name>`
4. Créer `.llm/[todo.md](http://todo.md)` dans le nouveau worktree avec uniquement cette tâche
5. Ouvrir un nouvel onglet terminal dans le worktree
```

### Phase INSPECT : Script de validation pré-merge

```bash
#!/bin/bash
# [pre-merge-check.sh](http://pre-merge-check.sh) - Validation avant intégration

WORKTREE_PATH=$1

cd "$WORKTREE_PATH" || exit 1

echo "🔍 Vérification du worktree: $WORKTREE_PATH"

# 1. Vérifier qu'il n'y a pas de changements non commités
if ! git diff --quiet; then
    echo "❌ Changements non commités détectés"
    exit 1
fi

# 2. Exécuter les tests
echo "🧪 Exécution des tests..."
if [ -f "composer.json" ]; then
    composer test || exit 1
elif [ -f "package.json" ]; then
    npm test || exit 1
fi

# 3. Vérifier le linting
echo "🔧 Vérification du code..."
if [ -f "composer.json" ]; then
    composer lint || exit 1
elif [ -f "package.json" ]; then
    npm run lint || exit 1
fi

echo "✅ Worktree prêt pour merge"
```

---

## 🔀 Stratégies de Merge

### Stratégie 1 : Cherry-Pick (Recommandée pour worktrees)

C'est la stratégie la plus utilisée avec les worktrees Claude Code :

```bash
# Depuis le worktree principal (main)
cd ../mon-projet

# Lister les commits du worktree feature
git log --oneline task/feature-auth

# Cherry-pick les commits pertinents
git cherry-pick <commit-hash-1>
git cherry-pick <commit-hash-2>

# Ou cherry-pick d'une plage
git cherry-pick <oldest-hash>^..<newest-hash>
```

**Avantages** :

- Sélection précise des commits
- Évite les commits de merge
- Permet de rejeter les commits non voulus

**Script d'automatisation** :

```bash
#!/bin/bash
# [cherry-pick-worktree.sh](http://cherry-pick-worktree.sh)

WORKTREE_BRANCH=$1
TARGET_BRANCH=${2:-main}

# Récupérer les commits à cherry-pick
COMMITS=$(git log --oneline --reverse ${TARGET_BRANCH}..${WORKTREE_BRANCH} | awk '{print $1}')

echo "🍒 Cherry-picking depuis ${WORKTREE_BRANCH} vers ${TARGET_BRANCH}"

for commit in $COMMITS; do
    echo "  → Picking: $commit"
    git cherry-pick "$commit" || {
        echo "❌ Conflit sur $commit"
        echo "   Résoudre puis: git cherry-pick --continue"
        exit 1
    }
done

echo "✅ Cherry-pick terminé"
```

### Stratégie 2 : Rebase Before PR

Modèle recommandé pour garder un historique propre :

```bash
# Dans le worktree feature
cd ../mon-projet-feature-auth

# 1. S'assurer que main est à jour
git fetch origin main

# 2. Rebaser sur main
git rebase origin/main

# 3. Résoudre les conflits si nécessaire
# git add <fichiers>
# git rebase --continue

# 4. Push force (car historique réécrit)
git push --force-with-lease origin task/feature-auth
```

### Stratégie 3 : Merge classique avec squash

```bash
# Depuis main
cd ../mon-projet

# Merge avec squash (un seul commit)
git merge --squash task/feature-auth

# Commit avec message descriptif
git commit -m "feat(auth): Implement JWT authentication

- Add login/logout endpoints
- Add token refresh mechanism
- Add middleware authentication"
```

### Matrice de décision

| Situation | Stratégie recommandée |
| --- | --- |
| Feature isolée, peu de commits | Cherry-pick |
| Feature avec beaucoup de commits | Merge --squash |
| Besoin de garder l'historique | Rebase + merge fast-forward |
| Conflits potentiels nombreux | Merge classique |
| Expérimentation (peut être jetée) | Cherry-pick sélectif |

---

## 🛡️ Gestion des Conflits

### Prévention des conflits

1. **Synchronisation régulière avec main** :

```bash
# Dans chaque worktree, régulièrement
git fetch origin main
git rebase origin/main
```

1. **Analyse préalable des dépendances** :

```bash
# Voir les fichiers modifiés dans un worktree
git diff --name-only main..HEAD

# Comparer avec un autre worktree
git diff --name-only task/feature-a task/feature-b
```

1. **Règle d'or** : Ne jamais avoir deux worktrees qui modifient le même fichier

### Résolution des conflits

```bash
# Si conflit lors du cherry-pick
git cherry-pick <commit>
# CONFLICT (content): Merge conflict in src/file.php

# 1. Ouvrir le fichier et résoudre
# 2. Marquer comme résolu
git add src/file.php

# 3. Continuer le cherry-pick
git cherry-pick --continue

# OU abandonner si trop complexe
git cherry-pick --abort
```

### Stratégie "Fail Fast"

Inspirée du workflow de [motlin.com](http://motlin.com) :

> "Si les conflits semblent complexes à résoudre, je jette simplement le travail et remarque la tâche comme `[ ]` dans la todo list."
> 

```bash
# Abandonner un worktree problématique
git worktree remove ../mon-projet-feature-probleme --force
git branch -D task/feature-probleme

# Remarquer la tâche comme à faire
# Dans .llm/[todo.md](http://todo.md): changer [>] en [ ]
```

---

## 📊 Workflow Complet Multi-Worktrees

### Setup initial du projet

```bash
#!/bin/bash
# [setup-parallel-dev.sh](http://setup-parallel-dev.sh)

PROJECT_NAME="mon-projet"
TASKS=("feature-auth" "feature-api" "refactor-db")

# Créer le dossier de travail
mkdir -p ~/worktrees/${PROJECT_NAME}
cd ~/worktrees/${PROJECT_NAME}

# Cloner le projet principal
git clone [git@github.com](mailto:git@github.com):user/${PROJECT_NAME}.git main
cd main

# Créer les worktrees pour chaque tâche
for task in "${TASKS[@]}"; do
    ../scripts/[worktree.sh](http://worktree.sh) "$task"
done

echo "📁 Structure créée:"
ls -la ~/worktrees/${PROJECT_NAME}/
```

### Lancement parallèle des sessions Claude

```bash
#!/bin/bash
# [launch-claude-sessions.sh](http://launch-claude-sessions.sh)

WORKTREES_DIR=~/worktrees/mon-projet

# Lancer Claude dans chaque worktree avec délai
for dir in ${WORKTREES_DIR}/*/; do
    if [ "$dir" != "${WORKTREES_DIR}/main/" ]; then
        echo "🚀 Lancement Claude dans: $dir"
        
        # Ouvrir nouvel onglet iTerm
        osascript -e "tell application \"iTerm\"
            tell current window
                create tab with default profile
                tell current tab
                    tell current session
                        write text \"cd $dir && claude --dangerously-skip-permissions /todo\"
                    end tell
                end tell
            end tell
        end tell"
        
        # Délai pour éviter rate limiting API
        sleep 300  # 5 minutes
    fi
done
```

### Script de consolidation finale

```bash
#!/bin/bash
# [consolidate-worktrees.sh](http://consolidate-worktrees.sh)

PROJECT_DIR=~/worktrees/mon-projet/main
cd "$PROJECT_DIR"

# S'assurer d'être sur main à jour
git checkout main
git pull origin main

# Pour chaque worktree terminé
for branch in $(git branch | grep "task/"); do
    branch_name=$(echo "$branch" | tr -d ' ')
    
    echo "🔍 Vérification: $branch_name"
    
    # Vérifier si la branche a des commits à merger
    COMMITS=$(git log --oneline main..$branch_name | wc -l)
    
    if [ "$COMMITS" -gt 0 ]; then
        echo "  → $COMMITS commits à intégrer"
        
        # Tenter le cherry-pick
        git cherry-pick main..$branch_name --no-commit
        
        if [ $? -eq 0 ]; then
            git commit -m "feat: Integrate $branch_name"
            echo "  ✅ Intégré avec succès"
        else
            git cherry-pick --abort
            echo "  ⚠️ Conflits - À traiter manuellement"
        fi
    fi
done

echo ""
echo "📊 État final:"
git log --oneline -10
```

---

## 🧹 Maintenance et Nettoyage

### Script de nettoyage automatique

```bash
#!/bin/bash
# [cleanup-merged-worktrees.sh](http://cleanup-merged-worktrees.sh)

echo "🧹 Nettoyage des worktrees mergés..."

git worktree list | grep -v "$(git rev-parse --show-toplevel)" | while read worktree branch commit; do
    branch_name=$(echo $branch | sed 's/\[//g' | sed 's/\]//g')
    
    # Vérifier si la branche est mergée dans main
    if git branch --merged main | grep -q "$branch_name"; then
        echo "🗑️ Suppression worktree mergé: $worktree ($branch_name)"
        git worktree remove "$worktree"
        git branch -d "$branch_name"
    fi
done

# Nettoyer les références orphelines
git worktree prune

echo "✅ Nettoyage terminé"
```

### Bonnes pratiques de maintenance

1. **Limiter le nombre de worktrees actifs** : 3-5 maximum pour rester gérable
2. **Supprimer immédiatement après merge** : Ne pas laisser traîner
3. **Synchroniser régulièrement** : `git fetch` quotidien minimum
4. **Documenter les worktrees actifs** : Dans un fichier [WORKTREES.md](http://WORKTREES.md)

---

## ⚠️ Pièges à éviter

### 1. Worktrees imbriqués

```bash
# ❌ JAMAIS faire ça
cd mon-projet
git worktree add ./subdir/feature  # Worktree dans un worktree
```

### 2. Même branche dans deux worktrees

```bash
# Git l'empêche heureusement
git worktree add ../autre feature/auth
# fatal: 'feature/auth' is already checked out
```

### 3. Oublier les dépendances

```bash
# ✅ Toujours installer les dépendances dans chaque worktree
cd ../mon-projet-feature-auth
composer install  # ou npm install
```

### 4. Ne pas partager node_modules/vendor

```bash
# ⚠️ Risqué mais possible pour les dépendances read-only
ln -s ../../mon-projet/node_modules ./node_modules

# ✅ Meilleure option : utiliser pnpm qui partage automatiquement
pnpm install
```

---

## 🎯 Intégration avec EPCI 3.0

### Proposition d'extension EPCI pour worktrees

```yaml
# .epci/config.yaml
worktrees:
  enabled: true
  base_path: "../{project}-{task}"
  auto_setup:
    - copy: [".env", ".envrc", "[CLAUDE.md](http://CLAUDE.md)"]
    - run: "composer install --no-interaction"
  
  parallel_tasks:
    max_concurrent: 4
    delay_between_start: 300  # secondes
    
  merge_strategy: "cherry-pick"  # ou "rebase", "squash"
  
  cleanup:
    auto_remove_merged: true
    keep_days: 7
```

### Commandes EPCI suggérées

```bash
# Nouvelle commande /epci-worktree
/epci-worktree create feature-auth   # Crée worktree + lance EPCI dessus
/epci-worktree list                   # Liste les worktrees actifs
/epci-worktree merge feature-auth    # Lance le merge EPCI-style
/epci-worktree cleanup               # Nettoie les worktrees terminés
```

---

## 📚 Ressources complémentaires

- [Documentation officielle Git Worktree](https://git-scm.com/docs/git-worktree)
- [Claude Code Workflows - Anthropic](https://docs.anthropic.com/en/docs/claude-code/common-workflows)
- [motlin.com](http://motlin.com) [- Parallel Development with /worktree](https://motlin.com/blog/claude-code-worktree)
- [git-worktree-runner](https://github.com/coderabbitai/git-worktree-runner) - Outil CLI dédié

---

*Document généré le 07/01/2026 - Basé sur les recherches et meilleures pratiques actuelles*
