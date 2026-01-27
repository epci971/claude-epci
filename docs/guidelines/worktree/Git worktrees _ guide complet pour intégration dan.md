<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# Git worktrees : guide complet pour intégration dans un workflow automatisé de développement.

Couvrir en détail :

- Commandes essentielles (git worktree add -b, list, remove, prune)
- Création d'un worktree avec nouvelle branche en une commande
- Structure des répertoires : où sont stockés les worktrees, relation avec .git
- Isolation complète : chaque worktree peut avoir ses propres node_modules, vendor, .env
- Limitations : une branche ne peut être checkout que dans un seul worktree
- Cleanup automatique après merge de PR
- Gestion des conflits et erreurs courantes

Focus : automatisation via scripts, pas usage manuel interactif.
Exemples de commandes bash/shell prêts à intégrer.
Sources 2025-2026.

Answer skipped.
<span style="display:none">[^1_1][^1_2][^1_3][^1_4][^1_5][^1_6]</span>

<div align="center">⁂</div>

[^1_1]: https://www.perplexity.ai/search/c9f227d1-d227-4695-8dd9-6bb91d3b162d

[^1_2]: https://www.perplexity.ai/search/ed38a0d5-c913-4fd8-b0c8-f9a2eb3ff6d9

[^1_3]: tools.github_cli_and_git_worktrees

[^1_4]: preferences.naming_convention

[^1_5]: projects.git_worktrees_automation

[^1_6]: interests.version_control.git_worktrees


---

# Git worktrees : guide complet pour intégration dans un workflow automatisé de développement.

Couvrir en détail :

- Commandes essentielles (git worktree add -b, list, remove, prune)
- Création d'un worktree avec nouvelle branche en une commande
- Structure des répertoires : où sont stockés les worktrees, relation avec .git
- Isolation complète : chaque worktree peut avoir ses propres node_modules, vendor, .env
- Limitations : une branche ne peut être checkout que dans un seul worktree
- Cleanup automatique après merge de PR
- Gestion des conflits et erreurs courantes

Focus : automatisation via scripts, pas usage manuel interactif.
Exemples de commandes bash/shell prêts à intégrer.
Sources 2025-2026

Je dispose maintenant de suffisamment d'informations pour créer un guide complet. Laissez-moi générer le rapport final.

# Git Worktrees : Guide Complet pour l'Automatisation du Workflow de Développement

## Introduction

Les Git worktrees constituent une fonctionnalité native de Git (depuis la version 2.5) permettant de maintenir plusieurs branches simultanément dans des répertoires distincts, tout en partageant le même historique Git. Cette capacité transforme radicalement les workflows de développement moderne, particulièrement dans les contextes nécessitant des changements de contexte fréquents ou l'utilisation d'agents IA parallèles.[^2_1][^2_2][^2_3][^2_4][^2_5]

Le présent guide se concentre sur l'automatisation complète de cette fonctionnalité via des scripts shell, en s'appuyant sur les sources les plus récentes (2025-2026) pour fournir des solutions de production éprouvées.

## Architecture et Structure Interne

### Hiérarchie des Répertoires

L'architecture des worktrees repose sur une séparation claire entre les données partagées et les éléments isolés:[^2_6][^2_7][^2_1]

**Répertoire principal** : `.git/` contient l'ensemble de l'historique Git
**Répertoires liés** : `.git/worktrees/<nom>/` stocke les métadonnées spécifiques à chaque worktree
**Worktrees actifs** : Chaque répertoire de worktree contient un fichier `.git` (non un répertoire) qui pointe vers `.git/worktrees/<nom>/`[^2_8][^2_7][^2_6]

Lorsqu'un worktree est créé avec `git worktree add /chemin/autre/feature-x feature-x`, le système génère:

- Un répertoire `/chemin/autre/feature-x/` avec le code source
- Un fichier `/chemin/autre/feature-x/.git` contenant `gitdir: /chemin/repo-principal/.git/worktrees/feature-x`
- Un répertoire `.git/worktrees/feature-x/` avec les métadonnées spécifiques (HEAD, index, etc.)[^2_9][^2_1]


### Variables d'Environnement Git

Git configure automatiquement deux variables critiques dans chaque worktree:[^2_7][^2_6]

- **`$GIT_DIR`** : Pointe vers `.git/worktrees/<nom>` (espace privé du worktree)
- **`$GIT_COMMON_DIR`** : Pointe vers `.git` principal (espace partagé)

Cette distinction permet à Git de déterminer quelles données consulter dans l'espace partagé (commits, branches distantes) versus l'espace privé (HEAD, index, stash).[^2_10][^2_7]

### Partage et Isolation

**Éléments partagés entre tous les worktrees**:[^2_11][^2_12][^2_7]

- Historique complet (objects, commits, tags)
- Configuration du dépôt (`.git/config`)
- Branches (`refs/heads/*`)
- Remotes et leurs références (`refs/remotes/*`)
- Hooks (`.git/hooks/`)

**Éléments isolés par worktree**:[^2_11][^2_7]

- HEAD (branche courante)
- Index (staging area)
- Fichiers du répertoire de travail
- `refs/bisect` et `refs/worktree`
- Stash local

Cette architecture garantit l'isolation complète des dépendances non versionnées comme `node_modules/`, `vendor/`, `.env`, `build/`, permettant à chaque worktree d'avoir ses propres versions de packages, variables d'environnement et artefacts de compilation.[^2_13][^2_14][^2_15][^2_11]

## Commandes Essentielles et Syntaxe

### Création de Worktree avec Nouvelle Branche en Une Commande

La commande la plus puissante pour l'automatisation combine création de branche et worktree:[^2_3][^2_16][^2_1]

```bash
git worktree add -b <nouvelle-branche> <chemin> [<commit-base>]
```

**Exemples pratiques**:

```bash
# Créer worktree + branche depuis HEAD
git worktree add -b feature/auth ../mon-projet-auth

# Créer depuis une branche spécifique
git worktree add -b hotfix/payment ../hotfix main

# Créer depuis un commit spécifique
git worktree add -b experiment/refactor ../experiment abc1234
```

Si aucune branche n'est spécifiée et que `-b` est omis, Git créera automatiquement une branche nommée d'après le nom du répertoire.[^2_17][^2_1]

### Checkout de Branche Existante

Pour un worktree basé sur une branche existante (locale ou distante):[^2_18][^2_3]

```bash
# Branche locale existante
git worktree add ../feature-x feature-x

# Branche distante (tracking automatique)
git worktree add -b feature-y ../feature-y origin/feature-y
```

Depuis Git 2.15, si la branche existe localement et n'est pas déjà checkout ailleurs, elle sera automatiquement utilisée sans nécessiter `-b`.[^2_18]

### Liste et Inspection

**Format standard** (lisible par humains):[^2_19][^2_1]

```bash
git worktree list
# Sortie :
# /chemin/vers/principal    abcd123 [main]
# /chemin/vers/feature-x    efgh456 [feature-x]
```

**Format porcelain** (parsing automatisé):[^2_20][^2_21]

```bash
git worktree list --porcelain
# Sortie structurée :
# worktree /chemin/vers/principal
# HEAD abcd1234...
# branch refs/heads/main
#
# worktree /chemin/vers/feature-x
# HEAD efgh5678...
# branch refs/heads/feature-x
```

Le format `--porcelain` est conçu pour rester stable entre versions de Git et faciliter le parsing par scripts.[^2_22][^2_1]

**Format verbeux** (détails supplémentaires):[^2_1][^2_20]

```bash
git worktree list --verbose
# Affiche également les commits et annotations (locked, prunable)
```


### Suppression de Worktree

**Suppression standard** (requiert worktree propre):[^2_23][^2_24][^2_1]

```bash
git worktree remove <chemin>
```

Cette commande échoue si le worktree contient des modifications non committées ou des fichiers non trackés.

**Suppression forcée** (ignore l'état du worktree):[^2_25][^2_23]

```bash
# Force simple (modifications non committées)
git worktree remove -f <chemin>

# Force double (worktree locked)
git worktree remove -f -f <chemin>
```

**Alternative manuelle** (déconseillée):[^2_26][^2_27]

```bash
rm -rf <chemin>        # Supprime le répertoire
git worktree prune     # Nettoie les métadonnées orphelines
```

Cette approche est risquée car elle peut laisser des références corrompues si `prune` n'est pas exécuté immédiatement.[^2_28][^2_26]

### Nettoyage des Métadonnées

**Nettoyage manuel** des worktrees supprimés:[^2_27][^2_28][^2_1]

```bash
git worktree prune [-v] [-n]
# -v : verbose, liste les suppressions
# -n : dry-run, simule sans supprimer
```

**Expiration conditionnelle** (supprime selon ancienneté):[^2_22][^2_1]

```bash
git worktree prune --expire <durée>
# Exemples de durée : "3.months.ago", "2.weeks.ago", "now"
```

**Configuration automatique** via `gc.worktreePruneExpire`:[^2_29][^2_1][^2_22]

```bash
# Définir l'expiration automatique à 90 jours
git config gc.worktreePruneExpire "3.months.ago"

# Le garbage collection nettoiera automatiquement
git gc
```


## Limitations et Contraintes Critiques

### Règle d'Exclusivité : Une Branche = Un Worktree

**Contrainte fondamentale** : Git interdit strictement qu'une même branche soit checkout dans plusieurs worktrees simultanément. Toute tentative produit l'erreur:[^2_30][^2_5][^2_31][^2_32]

```
fatal: 'feature-x' is already checked out at '/autre/chemin'
```

**Justification technique** : Cette limitation protège l'intégrité de la branche. Puisque les branches sont partagées entre worktrees, permettre deux checkouts simultanés créerait des conflits lors de commits concurrents sur la même branche depuis différents worktrees.[^2_32]

**Solutions de contournement**:

**1. HEAD détaché** (lecture seule, recommandé pour tests):[^2_30][^2_32]

```bash
# Dans le worktree où la branche est déjà checkout
git checkout --detach feature-x
# Maintenant feature-x peut être checkout ailleurs
```

Cette approche permet de tester un état de branche sans la "réserver".[^2_32]

**2. Force override** (dangereux, déconseillé):[^2_30]

```bash
git checkout --ignore-other-worktrees feature-x
```

Cette option force le checkout mais peut conduire à des états incohérents si des commits sont effectués depuis les deux worktrees.[^2_30]

**3. Architecture recommandée** : Conception du workflow pour éviter le besoin de checkout multiples de la même branche. Par exemple, créer des branches distinctes pour chaque tâche plutôt que réutiliser une branche commune.[^2_3][^2_11]

### Gestion des Branches Distantes

Lors du tracking de branches distantes, quelques patterns émergent:[^2_33][^2_18]

```bash
# Pattern explicite (toujours fonctionnel)
git worktree add -b local-name ../worktree origin/remote-branch

# Pattern court (Git 2.15+, si branche n'existe pas localement)
git worktree add ../worktree remote-branch
```

**Problème courant** : Dans un dépôt bare, le fetch des branches distantes peut échouer sans configuration explicite. Solution:[^2_33]

```bash
# Dans .git/config ou .bare/config
[remote "origin"]
    url = ...
    fetch = +refs/heads/*:refs/remotes/origin/*
```


### Limitations de Déplacement

Si un worktree est déplacé manuellement (sans commande Git), les références deviennent invalides. Le fichier `.git` du worktree pointe vers un chemin obsolète, causant l'erreur:[^2_34][^2_1]

```
fatal: Invalid path '/ancien/chemin': No such file or directory
```

**Solution moderne** (Git 2.17+):[^2_1]

```bash
git worktree repair [<chemin>]
```

**Solution manuelle** (versions antérieures):[^2_35][^2_34]

```bash
# Éditer .git pour corriger le gitdir
echo "gitdir: /nouveau/chemin/.git/worktrees/nom" > worktree/.git

# Éditer le fichier gitdir dans le repo principal
echo "/nouveau/chemin/worktree/.git" > .git/worktrees/nom/gitdir
```


## Isolation Complète des Environnements

### Dépendances Node.js, PHP, Python

Chaque worktree maintient son propre espace de fichiers non versionnés, permettant l'isolation complète des dépendances:[^2_14][^2_15][^2_36]

**Node.js** :

```bash
# Worktree 1 : React 17
cd ../projet-feature-a
npm install  # Crée node_modules/ isolé

# Worktree 2 : React 18
cd ../projet-feature-b
npm install  # node_modules/ différent, sans conflit
```

**PHP Composer** :

```bash
cd ../worktree-1
composer install  # vendor/ isolé

cd ../worktree-2
composer install  # vendor/ indépendant
```

**Python** :

```bash
cd ../worktree-1
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

cd ../worktree-2
python -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt  # Environnement distinct
```

**Optimisation Copy-on-Write** (macOS, FreeBSD): Certains scripts utilisent `cp -c` pour dupliquer `node_modules/` entre worktrees via copy-on-write, économisant l'espace disque:[^2_36]

```bash
if [[ "$OSTYPE" == "darwin"* ]] || [[ "$OSTYPE" == "freebsd"* ]]; then
    cp -cR ../main-worktree/node_modules ./
else
    cp -R ../main-worktree/node_modules ./
fi
```


### Variables d'Environnement et Configuration

**Fichiers `.env` isolés** sont naturellement séparés par worktree:[^2_37][^2_13][^2_11]

```bash
# Worktree 1 : Développement feature A
# .env
APP_NAME=MonApp-feature-a
DATABASE_URL=postgresql://localhost:5432/db_feature_a
REDIS_PORT=6379
API_PORT=3000

# Worktree 2 : Hotfix production
# .env
APP_NAME=MonApp-hotfix
DATABASE_URL=postgresql://localhost:5433/db_hotfix
REDIS_PORT=6380
API_PORT=3001
```

**Génération automatique via templates**: L'approche la plus robuste utilise un fichier `.env.template` avec des variables substituées par script:[^2_13]

```bash
# .env.template
APP_NAME=${PROJECT_NAME}-${BRANCH_NAME}
DATABASE_URL=postgresql://localhost:${DB_PORT}/myapp
REDIS_PORT=${REDIS_PORT}
WEB_PORT=${WEB_PORT}
WORKTREE_INDEX=${WORKTREE_INDEX}
```

Le script de création de worktree calcule les ports et génère le `.env` spécifique.[^2_13]

### Allocation Dynamique de Ports

**Problème** : Plusieurs worktrees avec services réseau (serveurs web, bases de données, caches) créent des conflits de ports.[^2_13]

**Solution : Formule d'allocation de ports**:[^2_13]

```
PORT_SERVICE = BASE_PORT + (INDEX_WORKTREE × 10) + OFFSET_SERVICE
```

**Exemple d'implémentation**:

```bash
BASE_PORT=40000
WORKTREE_INDEX=1  # Calculé dynamiquement

# Services pour worktree index 1
DB_PORT=$((BASE_PORT + WORKTREE_INDEX * 10 + 0))      # 40010
WEB_PORT=$((BASE_PORT + WORKTREE_INDEX * 10 + 1))     # 40011
REDIS_PORT=$((BASE_PORT + WORKTREE_INDEX * 10 + 2))   # 40012
```

Cette formule garantit 10 ports par worktree, éliminant tout conflit.[^2_13]

**Calcul automatique de l'index**:[^2_13]

```bash
calculate_next_worktree_index() {
    local max_index=0
    while IFS= read -r line; do
        if [[ $line =~ worktree.*/([0-9]+) ]]; then
            local idx="${BASH_REMATCH[^2_1]}"
            ((idx > max_index)) && max_index=$idx
        fi
    done < <(git worktree list)
    echo $((max_index + 1))
}
```


### Docker et Conteneurs

**Isolation des volumes Docker** par worktree:[^2_13]

```yaml
# docker-compose.yml (utilise variables d'environnement)
services:
  database:
    image: postgres:15
    ports:
      - "${DB_PORT:-5432}:5432"
    volumes:
      - db-data-wt${WORKTREE_INDEX:-0}:/var/lib/postgresql/data
    environment:
      POSTGRES_DB: myapp_wt${WORKTREE_INDEX:-0}

  web:
    build: .
    ports:
      - "${WEB_PORT:-3000}:80"
    environment:
      WORKTREE_INDEX: ${WORKTREE_INDEX:-0}

volumes:
  db-data-wt0:  # Worktree principal
  db-data-wt1:  # Worktree 1
  db-data-wt2:  # Worktree 2
```

Chaque worktree possède ainsi sa propre base de données isolée, évitant toute contamination de données entre branches.[^2_15][^2_13]

## Automatisation du Cleanup Après Merge

### Configuration Native Git

**Expiration automatique via `gc.worktreePruneExpire`**:[^2_29][^2_22][^2_1]

```bash
# Configuration globale (tous les dépôts)
git config --global gc.worktreePruneExpire "3.months.ago"

# Configuration locale (dépôt courant uniquement)
git config gc.worktreePruneExpire "1.month.ago"

# Vérifier la configuration actuelle
git config --get gc.worktreePruneExpire
```

Le garbage collection (`git gc`) invoquera automatiquement `git worktree prune` en respectant cette période d'expiration.[^2_38][^2_29]

**Déclencheurs du garbage collection**:

- Explicite : `git gc` manuel
- Implicite : Après certaines opérations (push, fetch, merge)[^2_38]
- Planifié : Via `gc.autoDetach` et `gc.auto` (par défaut après ~6700 objets libres)[^2_38]


### Hooks Git pour Automatisation

**post-checkout** : Exécuté après `git worktree add`:[^2_39][^2_40][^2_37]

```bash
#!/bin/bash
# .git/hooks/post-checkout

# Détection création worktree (prev_head = 0000...)
if [[ "$1" == "0000000000000000000000000000000000000000" ]]; then
    echo "Nouveau worktree détecté"
    
    # Copier fichiers secrets
    if [[ -f ~/.secrets/project.env ]]; then
        cp ~/.secrets/project.env .env
        echo "Fichier .env copié"
    fi
    
    # Installer dépendances
    if [[ -f package.json ]]; then
        npm install --silent
    fi
fi
```

**post-merge** : Exécuté après merge réussi:[^2_41]

```bash
#!/bin/bash
# .git/hooks/post-merge

echo "Merge détecté, mise à jour dépendances..."
[[ -f package.json ]] && npm install
[[ -f composer.json ]] && composer install
```

**Hooks personnalisés pour cleanup** (via outils tiers):[^2_41]

Certains gestionnaires de worktrees comme `worktrunk` offrent des hooks avancés:

- `pre-remove` : Avant suppression worktree (sauvegarde logs, artefacts)
- `post-remove` : Après suppression (arrêt serveurs, cleanup Docker)
- `post-merge` : Après merge vers branche cible (déploiement, notifications)


### Scripts de Détection de Branches Mergées

**Identification des branches entièrement mergées**:

```bash
#!/bin/bash
# cleanup-merged-worktrees.sh

# Branches mergées dans main
merged_branches=$(git branch --merged main | grep -v "^\*" | grep -v "main")

echo "Branches mergées détectées :"
echo "$merged_branches"

# Pour chaque branche mergée
while IFS= read -r branch; do
    branch=$(echo "$branch" | xargs)  # Trim whitespace
    
    # Trouver le worktree associé
    worktree_path=$(git worktree list --porcelain | \
                    grep -B2 "branch refs/heads/$branch" | \
                    grep "^worktree" | cut -d' ' -f2)
    
    if [[ -n "$worktree_path" ]]; then
        echo "Suppression worktree : $worktree_path (branche: $branch)"
        git worktree remove "$worktree_path" 2>/dev/null || \
            git worktree remove -f "$worktree_path"
    fi
    
    # Supprimer la branche
    echo "Suppression branche : $branch"
    git branch -d "$branch"
    
done <<< "$merged_branches"

# Nettoyer métadonnées
git worktree prune -v
```

**Amélioration : Confirmation interactive**:

```bash
cleanup_merged_interactive() {
    local merged_branches=$(git branch --merged main | grep -v "^\*" | grep -v "main")
    
    if [[ -z "$merged_branches" ]]; then
        echo "Aucune branche mergée à nettoyer"
        return 0
    fi
    
    echo "Branches mergées détectées :"
    echo "$merged_branches"
    echo ""
    read -p "Supprimer ces worktrees et branches ? [y/N] " -n 1 -r
    echo
    
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        # Exécuter cleanup...
        while IFS= read -r branch; do
            # [Code de suppression identique]
        done <<< "$merged_branches"
    else
        echo "Cleanup annulé"
    fi
}
```


### Intégration GitHub/GitLab

**Cleanup basé sur statut PR/MR** (via `gh` CLI):[^2_42][^2_43]

```bash
#!/bin/bash
# cleanup-closed-prs.sh

# Vérifier authentification GitHub
gh auth status || {
    echo "Erreur : Authentification GitHub requise"
    echo "Exécutez : gh auth login"
    exit 1
}

# Récupérer toutes les branches de PR fermées
closed_pr_branches=$(gh pr list --state closed --json headRefName \
                     --jq '.[].headRefName')

echo "Branches de PR fermées :"
echo "$closed_pr_branches"

# Pour chaque branche de PR fermée
while IFS= read -r branch; do
    [[ -z "$branch" ]] && continue
    
    # Vérifier si branche existe localement
    if git show-ref --verify --quiet "refs/heads/$branch"; then
        # Trouver worktree associé
        worktree_path=$(git worktree list --porcelain | \
                        grep -B2 "branch refs/heads/$branch" | \
                        grep "^worktree" | cut -d' ' -f2)
        
        if [[ -n "$worktree_path" ]]; then
            echo "Suppression worktree : $worktree_path"
            git worktree remove -f "$worktree_path" 2>/dev/null
        fi
        
        # Supprimer branche locale
        git branch -D "$branch"
        echo "Branche supprimée : $branch"
    fi
done <<< "$closed_pr_branches"

git worktree prune -v
```

**Automatisation via cron** ou CI/CD:

```bash
# Crontab : Cleanup quotidien à 2h du matin
0 2 * * * cd /chemin/projet && /chemin/scripts/cleanup-merged-worktrees.sh >> /var/log/git-cleanup.log 2>&1
```


### Outils Tiers pour Cleanup Automatique

**`autowt`** (Python): Outil avancé avec cleanup automatique intégré:[^2_42]

```bash
# Installation
pip install autowt

# Configuration cleanup auto
autowt config

# Cleanup manuel
autowt cleanup
# Supprime automatiquement :
# - Worktrees dont les branches sont mergées
# - Worktrees associés à PR GitHub fermées
```

**`worktrunk`** (Rust): CLI avec hooks de lifecycle pour cleanup orchestré:[^2_41]

```toml
# .worktrunk.toml
[hooks.post-remove]
cleanup_docker = "docker stop $(docker ps -q --filter name=wt-${BRANCH})"
cleanup_logs = "tar -czf ~/logs/${BRANCH}.tar.gz logs/ 2>/dev/null || true"
```


## Gestion des Conflits et Erreurs Courantes

### Erreur : Répertoire Déjà Existant

**Symptôme**:[^2_44][^2_45]

```
fatal: '../feature-x' already exists
```

**Causes** :

- Tentative de création worktree dans répertoire non vide
- Ancien worktree supprimé manuellement (métadonnées persistent)

**Solutions** :

```bash
# Option 1 : Supprimer le répertoire existant
rm -rf ../feature-x
git worktree add -b feature-x ../feature-x

# Option 2 : Utiliser un chemin différent
git worktree add -b feature-x ../feature-x-new

# Option 3 : Si métadonnées corrompues, nettoyer d'abord
git worktree prune
git worktree add -b feature-x ../feature-x
```


### Erreur : Branche Déjà Checkout

**Symptôme**:[^2_44][^2_30]

```
fatal: 'feature-x' is already checked out at '/autre/chemin'
```

**Cause** : Limitation Git (une branche = un worktree)

**Solutions hiérarchisées** :

```bash
# Solution 1 : Utiliser une branche différente (recommandé)
git worktree add -b feature-x-dev ../feature-x-dev

# Solution 2 : Checkout détaché dans le worktree existant
cd /autre/chemin
git checkout --detach
cd -
git worktree add ../nouveau-chemin feature-x

# Solution 3 : Force (DANGEREUX, éviter en production)
git worktree add ../nouveau-chemin feature-x --force

# Solution 4 : Supprimer l'ancien worktree
git worktree remove /autre/chemin
git worktree add ../nouveau-chemin feature-x
```

**Script de détection préventive** :

```bash
safe_worktree_add() {
    local branch="$1"
    local path="$2"
    
    # Vérifier si branche déjà checkout
    local existing=$(git worktree list --porcelain | \
                     grep -B2 "branch refs/heads/$branch" | \
                     grep "^worktree" | cut -d' ' -f2)
    
    if [[ -n "$existing" ]]; then
        echo "Erreur : Branche '$branch' déjà checkout dans : $existing"
        echo "Options :"
        echo "  1. Utiliser une branche différente"
        echo "  2. Supprimer le worktree existant : git worktree remove $existing"
        return 1
    fi
    
    git worktree add -b "$branch" "$path"
}
```


### Erreur : Worktree Invalide Après Déplacement

**Symptôme**:[^2_34]

```
fatal: Invalid path '/ancien/chemin': No such file or directory
```

**Cause** : Worktree déplacé manuellement sans mise à jour des références

**Solution moderne** (Git 2.17+):[^2_1]

```bash
git worktree repair /nouveau/chemin
```

**Solution manuelle** (versions antérieures):[^2_35][^2_34]

```bash
#!/bin/bash
repair_worktree() {
    local worktree_path="$1"
    local repo_path=$(git rev-parse --git-common-dir)
    local worktree_name=$(basename "$worktree_path")
    
    # Mettre à jour .git dans le worktree
    echo "gitdir: $repo_path/worktrees/$worktree_name" > "$worktree_path/.git"
    
    # Mettre à jour gitdir dans le repo principal
    echo "$worktree_path/.git" > "$repo_path/worktrees/$worktree_name/gitdir"
    
    echo "Worktree réparé : $worktree_path"
}

repair_worktree /nouveau/chemin/worktree
```


### Erreur : Impossible de Supprimer Worktree

**Symptôme**:[^2_24][^2_23]

```
error: 'worktree' contains modified or untracked files, use --force to delete it
```

**Solutions graduelles** :

```bash
# Étape 1 : Vérifier l'état
cd /chemin/worktree
git status

# Étape 2 : Décider de l'action
git stash push -m "Sauvegarde avant suppression"  # Ou
git add . && git commit -m "WIP avant suppression"

# Étape 3 : Supprimer proprement
cd ..
git worktree remove /chemin/worktree

# Alternative : Force si modifications sans valeur
git worktree remove -f /chemin/worktree
```

**Worktree locked** (nécessite force double):[^2_23]

```bash
# Vérifier statut locked
git worktree list

# Unlock
git worktree unlock /chemin/worktree

# Ou supprimer avec force double
git worktree remove -f -f /chemin/worktree
```


### Erreur : Métadonnées Corrompues

**Symptôme**:[^2_46][^2_26]

```
error: worktree and untracked commit have duplicate entries
```

**Cause** : Index corrompu ou métadonnées incohérentes

**Solutions** :

```bash
# Solution 1 : Reconstruire l'index
cd /chemin/worktree
git rm -r --cached .
git reset --hard HEAD

# Solution 2 : Prune puis recréer
cd /chemin/repo-principal
git worktree prune
# Supprimer manuellement le répertoire worktree
rm -rf /chemin/worktree
# Recréer proprement
git worktree add -b branche /chemin/worktree

# Solution 3 : En dernier recours, clone frais
cd /chemin/temporaire
git clone /chemin/repo-principal nouveau-clone
# Appliquer manuellement les modifications non committées
```


### Erreur : Conflit lors du Merge entre Worktrees

**Scénario** : Modifications concurrentes sur même fichier dans différents worktrees[^2_47][^2_11]

**Prévention** :

```bash
# Synchronisation régulière dans chaque worktree
cd /chemin/worktree-1
git fetch origin
git rebase origin/main

cd /chemin/worktree-2
git fetch origin
git rebase origin/main
```

**Résolution** : Les worktrees ne créent pas de conflits directs (branches isolées), mais le merge final peut en produire. Résolution standard Git s'applique:

```bash
cd /chemin/worktree-principal
git merge feature-x
# Si conflits...
git status
# Éditer fichiers en conflit
git add fichiers-résolus
git commit
```

**Outil recommandé pour résolution** : GitKraken, GitLens, ou merge tools intégrés IDE.[^2_48]

### Script de Diagnostic Complet

```bash
#!/bin/bash
# diagnose-worktrees.sh

echo "=== Diagnostic Git Worktrees ==="
echo ""

echo "1. Liste des worktrees :"
git worktree list --porcelain || {
    echo "Erreur : Pas un dépôt Git ou Git trop ancien"
    exit 1
}
echo ""

echo "2. Worktrees prunable (métadonnées orphelines) :"
git worktree prune -v --dry-run
echo ""

echo "3. Branches checkout multiples (devrait être vide) :"
declare -A branch_counts
while IFS= read -r line; do
    if [[ $line =~ ^branch\ refs/heads/(.+) ]]; then
        branch="${BASH_REMATCH[^2_1]}"
        ((branch_counts[$branch]++))
    fi
done < <(git worktree list --porcelain)

for branch in "${!branch_counts[@]}"; do
    if (( branch_counts[$branch] > 1 )); then
        echo "ATTENTION : Branche '$branch' checkout ${branch_counts[$branch]} fois"
    fi
done
echo ""

echo "4. Worktrees avec modifications non committées :"
while IFS= read -r line; do
    if [[ $line =~ ^worktree\ (.+) ]]; then
        worktree_path="${BASH_REMATCH[^2_1]}"
        if [[ -d "$worktree_path" ]]; then
            cd "$worktree_path"
            if ! git diff-index --quiet HEAD 2>/dev/null; then
                echo "  - $worktree_path (modifications détectées)"
            fi
            cd - > /dev/null
        fi
    fi
done < <(git worktree list --porcelain)
echo ""

echo "5. Utilisation disque :"
du -sh .git/worktrees/* 2>/dev/null || echo "Aucune métadonnée worktree"
```


## Scripts Bash d'Automatisation Prêts pour Production

### Script Maître : Création Complète de Worktree

```bash
#!/bin/bash
# create-worktree.sh - Création automatisée de worktree avec environnement complet

set -euo pipefail

# Configuration
readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[^2_0]}")" && pwd)"
readonly REPO_ROOT="$(git rev-parse --show-toplevel)"
readonly WORKTREE_BASE_DIR="${WORKTREE_BASE_DIR:-$(dirname "$REPO_ROOT")}"
readonly BASE_PORT=40000

# Couleurs pour output
readonly RED='\033[0;31m'
readonly GREEN='\033[0;32m'
readonly YELLOW='\033[1;33m'
readonly NC='\033[0m' # No Color

# Logging
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1" >&2
}

# Validation environnement Git
validate_git_repo() {
    if ! git rev-parse --is-inside-work-tree &>/dev/null; then
        log_error "Pas un dépôt Git valide"
        exit 1
    fi
    
    if ! git diff-index --quiet HEAD -- 2>/dev/null; then
        log_warn "Modifications non committées détectées dans worktree actuel"
    fi
}

# Calculer index disponible pour nouveau worktree
calculate_next_index() {
    local max_index=0
    while IFS= read -r line; do
        if [[ $line =~ worktree\ .*/([0-9]+) ]]; then
            local idx="${BASH_REMATCH[^2_1]}"
            ((idx > max_index)) && max_index=$idx
        fi
    done < <(git worktree list --porcelain)
    echo $((max_index + 1))
}

# Vérifier disponibilité d'un port
check_port_available() {
    local port=$1
    if lsof -Pi ":$port" -sTCP:LISTEN -t >/dev/null 2>&1; then
        return 1  # Port occupé
    fi
    return 0  # Port disponible
}

# Calculer ports pour un index donné
calculate_ports() {
    local index=$1
    local base=$BASE_PORT
    
    echo "DB_PORT=$((base + index * 10 + 0))"
    echo "WEB_PORT=$((base + index * 10 + 1))"
    echo "REDIS_PORT=$((base + index * 10 + 2))"
    echo "API_PORT=$((base + index * 10 + 3))"
}

# Sanitize nom de branche pour filesystem
sanitize_branch_name() {
    local branch="$1"
    echo "$branch" | sed 's|[^a-zA-Z0-9/_-]|-|g' | cut -c1-50
}

# Générer fichier .env depuis template
generate_env_file() {
    local worktree_path="$1"
    local branch_name="$2"
    local worktree_index="$3"
    local env_template="${REPO_ROOT}/.env.template"
    local env_target="${worktree_path}/.env"
    
    if [[ ! -f "$env_template" ]]; then
        log_warn "Pas de .env.template trouvé, .env non généré"
        return 0
    fi
    
    # Calculer ports
    local ports=$(calculate_ports "$worktree_index")
    eval "$ports"  # Charge DB_PORT, WEB_PORT, etc.
    
    # Variables pour substitution
    export WORKTREE_INDEX="$worktree_index"
    export BRANCH_NAME="$branch_name"
    export PROJECT_NAME="$(basename "$REPO_ROOT")"
    
    # Substitution template
    envsubst < "$env_template" > "$env_target"
    
    log_info "Fichier .env généré avec ports : DB=$DB_PORT, WEB=$WEB_PORT, REDIS=$REDIS_PORT"
}

# Copier fichiers secrets depuis répertoire global
copy_secrets() {
    local worktree_path="$1"
    local secrets_dir="${HOME}/.secrets/$(basename "$REPO_ROOT")"
    
    if [[ ! -d "$secrets_dir" ]]; then
        log_warn "Aucun répertoire secrets trouvé : $secrets_dir"
        return 0
    fi
    
    log_info "Copie des secrets depuis $secrets_dir"
    
    # Copier fichiers .env.local, certificats, etc.
    for secret_file in "$secrets_dir"/*; do
        if [[ -f "$secret_file" ]]; then
            cp "$secret_file" "$worktree_path/"
            log_info "  Copié : $(basename "$secret_file")"
        fi
    done
}

# Installer dépendances selon type de projet
install_dependencies() {
    local worktree_path="$1"
    cd "$worktree_path"
    
    # Node.js
    if [[ -f package.json ]]; then
        log_info "Installation dépendances npm..."
        npm install --silent || npm install
    fi
    
    # PHP Composer
    if [[ -f composer.json ]]; then
        log_info "Installation dépendances Composer..."
        composer install --quiet --no-interaction
    fi
    
    # Python
    if [[ -f requirements.txt ]]; then
        log_info "Installation dépendances Python..."
        python -m venv .venv
        source .venv/bin/activate
        pip install -q -r requirements.txt
    fi
    
    cd - > /dev/null
}

# Fonction principale
create_worktree() {
    local branch_name="$1"
    local base_commit="${2:-HEAD}"
    
    # Validation
    validate_git_repo
    
    # Calculer index
    local worktree_index=$(calculate_next_index)
    log_info "Création worktree index $worktree_index"
    
    # Construire chemin worktree
    local sanitized=$(sanitize_branch_name "$branch_name")
    local worktree_path="${WORKTREE_BASE_DIR}/$(basename "$REPO_ROOT")-${sanitized}"
    
    if [[ -d "$worktree_path" ]]; then
        log_error "Répertoire déjà existant : $worktree_path"
        exit 1
    fi
    
    # Vérifier si branche existe déjà
    if git show-ref --verify --quiet "refs/heads/$branch_name"; then
        log_info "Branche '$branch_name' existe, checkout dans worktree"
        git worktree add "$worktree_path" "$branch_name"
    else
        log_info "Création nouvelle branche '$branch_name' depuis $base_commit"
        git worktree add -b "$branch_name" "$worktree_path" "$base_commit"
    fi
    
    # Générer environnement
    generate_env_file "$worktree_path" "$branch_name" "$worktree_index"
    
    # Copier secrets
    copy_secrets "$worktree_path"
    
    # Installer dépendances
    install_dependencies "$worktree_path"
    
    # Vérifier ports disponibles
    local ports=$(calculate_ports "$worktree_index")
    eval "$ports"
    for port in $DB_PORT $WEB_PORT $REDIS_PORT $API_PORT; do
        if ! check_port_available "$port"; then
            log_warn "Port $port déjà utilisé, ajustez manuellement"
        fi
    done
    
    log_info "✓ Worktree créé avec succès : $worktree_path"
    log_info "  Branche : $branch_name"
    log_info "  Index : $worktree_index"
    log_info "  Ports : DB=$DB_PORT, WEB=$WEB_PORT, REDIS=$REDIS_PORT, API=$API_PORT"
    log_info ""
    log_info "Pour travailler dans ce worktree :"
    log_info "  cd $worktree_path"
}

# Usage et parsing arguments
usage() {
    cat << EOF
Usage: $0 <branch-name> [base-commit]

Crée un worktree Git complet avec environnement isolé.

Arguments:
  branch-name   Nom de la branche (créée si n'existe pas)
  base-commit   Commit de base (défaut: HEAD)

Exemples:
  $0 feature/auth
  $0 hotfix/payment main
  $0 experiment/refactor abc1234

Configuration:
  WORKTREE_BASE_DIR  Répertoire parent pour worktrees (défaut: à côté du repo)
  BASE_PORT          Port de base pour allocation (défaut: 40000)
EOF
}

# Point d'entrée
main() {
    if [[ $# -lt 1 ]]; then
        usage
        exit 1
    fi
    
    local branch_name="$1"
    local base_commit="${2:-HEAD}"
    
    create_worktree "$branch_name" "$base_commit"
}

main "$@"
```


### Script : Suppression et Cleanup

```bash
#!/bin/bash
# remove-worktree.sh - Suppression sécurisée de worktree

set -euo pipefail

readonly RED='\033[0;31m'
readonly GREEN='\033[0;32m'
readonly YELLOW='\033[1;33m'
readonly NC='\033[0m'

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1" >&2
}

# Trouver worktree par branche ou chemin
find_worktree() {
    local identifier="$1"
    
    # Si chemin absolu/relatif existe
    if [[ -d "$identifier" ]]; then
        echo "$identifier"
        return 0
    fi
    
    # Sinon rechercher par nom de branche
    local worktree_path=$(git worktree list --porcelain | \
                          grep -B2 "branch refs/heads/$identifier" | \
                          grep "^worktree" | cut -d' ' -f2)
    
    if [[ -n "$worktree_path" ]]; then
        echo "$worktree_path"
        return 0
    fi
    
    return 1
}

# Vérifier état du worktree avant suppression
check_worktree_state() {
    local worktree_path="$1"
    cd "$worktree_path"
    
    # Vérifier modifications non committées
    if ! git diff-index --quiet HEAD -- 2>/dev/null; then
        log_error "Worktree contient des modifications non committées"
        echo "Fichiers modifiés :"
        git status --short
        return 1
    fi
    
    # Vérifier fichiers non trackés
    if [[ -n $(git ls-files --others --exclude-standard) ]]; then
        log_info "Fichiers non trackés détectés (seront conservés)"
    fi
    
    cd - > /dev/null
    return 0
}

# Sauvegarder artefacts importants
backup_artifacts() {
    local worktree_path="$1"
    local branch_name="$2"
    local backup_dir="${HOME}/.worktree-backups/$(basename "$worktree_path")-$(date +%Y%m%d-%H%M%S)"
    
    mkdir -p "$backup_dir"
    
    # Sauvegarder logs
    if [[ -d "$worktree_path/logs" ]]; then
        cp -R "$worktree_path/logs" "$backup_dir/"
        log_info "Logs sauvegardés : $backup_dir/logs"
    fi
    
    # Sauvegarder résultats tests
    if [[ -d "$worktree_path/test-results" ]]; then
        cp -R "$worktree_path/test-results" "$backup_dir/"
        log_info "Résultats tests sauvegardés : $backup_dir/test-results"
    fi
    
    # Sauvegarder fichiers non trackés si demandé
    read -p "Sauvegarder fichiers non trackés ? [y/N] " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        cd "$worktree_path"
        git ls-files --others --exclude-standard | while read -r file; do
            mkdir -p "$backup_dir/untracked/$(dirname "$file")"
            cp "$file" "$backup_dir/untracked/$file"
        done
        cd - > /dev/null
        log_info "Fichiers non trackés sauvegardés : $backup_dir/untracked"
    fi
}

# Arrêter services en cours (Docker, serveurs dev, etc.)
stop_services() {
    local worktree_path="$1"
    cd "$worktree_path"
    
    # Arrêter Docker Compose si présent
    if [[ -f docker-compose.yml ]] && docker compose ps -q &>/dev/null; then
        log_info "Arrêt conteneurs Docker..."
        docker compose down
    fi
    
    # Arrêter serveurs sur ports alloués (lecture depuis .env)
    if [[ -f .env ]]; then
        source .env
        for port in ${WEB_PORT:-} ${API_PORT:-} ${DB_PORT:-}; do
            if [[ -n "$port" ]]; then
                local pid=$(lsof -ti ":$port" 2>/dev/null || true)
                if [[ -n "$pid" ]]; then
                    log_info "Arrêt processus sur port $port (PID: $pid)"
                    kill "$pid" 2>/dev/null || true
                fi
            fi
        done
    fi
    
    cd - > /dev/null
}

# Supprimer worktree et branche associée
remove_worktree() {
    local identifier="$1"
    local force="${2:-false}"
    local delete_branch="${3:-false}"
    
    # Trouver worktree
    local worktree_path=$(find_worktree "$identifier") || {
        log_error "Worktree non trouvé : $identifier"
        exit 1
    }
    
    log_info "Worktree trouvé : $worktree_path"
    
    # Obtenir nom de branche
    local branch_name=$(git worktree list --porcelain | \
                        grep -A2 "^worktree $worktree_path" | \
                        grep "^branch" | cut -d'/' -f3-)
    
    log_info "Branche associée : ${branch_name:-<detached>}"
    
    # Vérifier état si pas force
    if [[ "$force" != "true" ]]; then
        check_worktree_state "$worktree_path" || {
            echo ""
            read -p "Forcer la suppression malgré modifications ? [y/N] " -n 1 -r
            echo
            [[ ! $REPLY =~ ^[Yy]$ ]] && exit 1
            force="true"
        }
    fi
    
    # Backup optionnel
    echo ""
    read -p "Sauvegarder artefacts avant suppression ? [y/N] " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        backup_artifacts "$worktree_path" "$branch_name"
    fi
    
    # Arrêter services
    stop_services "$worktree_path"
    
    # Supprimer worktree
    log_info "Suppression du worktree..."
    if [[ "$force" == "true" ]]; then
        git worktree remove -f "$worktree_path"
    else
        git worktree remove "$worktree_path"
    fi
    
    # Supprimer branche si demandé
    if [[ "$delete_branch" == "true" ]] && [[ -n "$branch_name" ]]; then
        echo ""
        read -p "Supprimer la branche '$branch_name' ? [y/N] " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            # Vérifier si branche mergée
            if git branch --merged main | grep -q "^[[:space:]]*$branch_name\$"; then
                git branch -d "$branch_name"
                log_info "Branche '$branch_name' supprimée (était mergée)"
            else
                echo ""
                read -p "Branche non mergée, forcer suppression ? [y/N] " -n 1 -r
                echo
                if [[ $REPLY =~ ^[Yy]$ ]]; then
                    git branch -D "$branch_name"
                    log_info "Branche '$branch_name' supprimée (force)"
                fi
            fi
        fi
    fi
    
    # Cleanup métadonnées
    git worktree prune -v
    
    log_info "✓ Worktree supprimé avec succès"
}

# Usage
usage() {
    cat << EOF
Usage: $0 <branch-ou-chemin> [OPTIONS]

Supprime un worktree Git de manière sécurisée.

Arguments:
  branch-ou-chemin  Nom de branche ou chemin du worktree

Options:
  -f, --force        Force suppression (ignore modifications)
  -d, --delete       Supprime aussi la branche associée
  -h, --help         Affiche cette aide

Exemples:
  $0 feature/auth
  $0 ../mon-projet-hotfix
  $0 feature/auth --force --delete
EOF
}

# Parsing arguments
main() {
    local identifier=""
    local force="false"
    local delete_branch="false"
    
    while [[ $# -gt 0 ]]; do
        case $1 in
            -f|--force)
                force="true"
                shift
                ;;
            -d|--delete)
                delete_branch="true"
                shift
                ;;
            -h|--help)
                usage
                exit 0
                ;;
            *)
                identifier="$1"
                shift
                ;;
        esac
    done
    
    if [[ -z "$identifier" ]]; then
        usage
        exit 1
    fi
    
    remove_worktree "$identifier" "$force" "$delete_branch"
}

main "$@"
```


### Script : Cleanup Automatique des Branches Mergées

```bash
#!/bin/bash
# cleanup-merged-worktrees.sh - Nettoyage automatique post-merge

set -euo pipefail

readonly GREEN='\033[0;32m'
readonly YELLOW='\033[1;33m'
readonly NC='\033[0m'

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

# Configuration
readonly TARGET_BRANCH="${1:-main}"
readonly DRY_RUN="${DRY_RUN:-false}"

# Obtenir branches mergées
get_merged_branches() {
    git branch --merged "$TARGET_BRANCH" | \
        grep -v "^\*" | \
        grep -v "^[[:space:]]*$TARGET_BRANCH\$" | \
        sed 's/^[[:space:]]*//'
}

# Cleanup complet
cleanup_merged() {
    local merged_branches=$(get_merged_branches)
    
    if [[ -z "$merged_branches" ]]; then
        log_info "Aucune branche mergée à nettoyer"
        return 0
    fi
    
    log_info "Branches mergées dans '$TARGET_BRANCH' :"
    echo "$merged_branches"
    echo ""
    
    if [[ "$DRY_RUN" == "true" ]]; then
        log_warn "Mode DRY RUN - aucune suppression effectuée"
    fi
    
    local count=0
    while IFS= read -r branch; do
        [[ -z "$branch" ]] && continue
        
        # Trouver worktree associé
        local worktree_path=$(git worktree list --porcelain | \
                              grep -B2 "branch refs/heads/$branch" | \
                              grep "^worktree" | cut -d' ' -f2 || true)
        
        if [[ -n "$worktree_path" ]]; then
            log_info "Traitement : $branch (worktree: $worktree_path)"
            
            if [[ "$DRY_RUN" != "true" ]]; then
                # Arrêter services
                if [[ -f "$worktree_path/docker-compose.yml" ]]; then
                    (cd "$worktree_path" && docker compose down 2>/dev/null) || true
                fi
                
                # Supprimer worktree
                git worktree remove "$worktree_path" -f 2>/dev/null || {
                    log_warn "Échec suppression worktree, tentative force..."
                    git worktree remove "$worktree_path" -f -f 2>/dev/null || true
                }
            fi
        else
            log_info "Traitement : $branch (pas de worktree)"
        fi
        
        # Supprimer branche
        if [[ "$DRY_RUN" != "true" ]]; then
            git branch -d "$branch" 2>/dev/null || {
                log_warn "Branche $branch non supprimable avec -d, utilisation -D"
                git branch -D "$branch"
            }
        fi
        
        ((count++))
    done <<< "$merged_branches"
    
    # Cleanup métadonnées
    if [[ "$DRY_RUN" != "true" ]]; then
        log_info "Nettoyage métadonnées..."
        git worktree prune -v
    fi
    
    log_info "✓ Cleanup terminé : $count branches traitées"
}

# Usage
if [[ "${BASH_SOURCE[^2_0]}" == "${0}" ]]; then
    echo "Nettoyage des branches mergées dans '$TARGET_BRANCH'"
    echo "================================================"
    echo ""
    cleanup_merged
fi
```


### Script : Liste Interactive avec FZF

```bash
#!/bin/bash
# switch-worktree.sh - Navigation interactive entre worktrees

set -euo pipefail

# Vérifier présence de fzf
if ! command -v fzf &> /dev/null; then
    echo "Erreur : fzf requis (https://github.com/junegunn/fzf)"
    exit 1
fi

# Formater liste worktrees pour fzf
format_worktrees() {
    git worktree list --porcelain | awk '
        /^worktree / { path = substr($0, 10) }
        /^HEAD / { head = substr($0, 6) }
        /^branch / { branch = substr($0, 8); gsub(/^refs\/heads\//, "", branch) }
        /^$/ {
            if (branch == "") branch = "detached"
            printf "%-50s  %-20s  %s\n", path, branch, substr(head, 1, 7)
            path = ""; head = ""; branch = ""
        }
    '
}

# Sélection interactive
select_worktree() {
    local selected=$(format_worktrees | \
                     fzf --height=40% --reverse \
                         --header="Sélectionnez un worktree (Entrée=cd, Ctrl-R=remove)" \
                         --preview='git -C {1} log --oneline --graph --color=always -10' \
                         --preview-window=right:50% \
                         --bind='ctrl-r:execute(git worktree remove -f {1})+abort')
    
    if [[ -n "$selected" ]]; then
        local worktree_path=$(echo "$selected" | awk '{print $1}')
        
        # Changer de répertoire dans shell parent
        echo "cd $worktree_path"
    fi
}

# Exécution
result=$(select_worktree)
if [[ -n "$result" ]]; then
    eval "$result"
fi
```


### Intégration CI/CD : GitHub Actions

```yaml
# .github/workflows/worktree-parallel-tests.yml
name: Tests Parallèles avec Worktrees

on: [push, pull_request]

jobs:
  test-matrix:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        test-suite: [unit, integration, e2e]
    
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0  # Historique complet nécessaire
      
      - name: Créer worktree pour ${{ matrix.test-suite }}
        run: |
          mkdir -p ~/worktrees
          git worktree add ~/worktrees/${{ matrix.test-suite }} HEAD
          cd ~/worktrees/${{ matrix.test-suite }}
          
          # Générer .env spécifique
          cat > .env <<EOF
          TEST_SUITE=${{ matrix.test-suite }}
          DB_PORT=$((5432 + ${{ strategy.job-index }} * 10))
          WEB_PORT=$((3000 + ${{ strategy.job-index }} * 10))
          EOF
      
      - name: Installer dépendances
        working-directory: ~/worktrees/${{ matrix.test-suite }}
        run: npm ci
      
      - name: Exécuter tests ${{ matrix.test-suite }}
        working-directory: ~/worktrees/${{ matrix.test-suite }}
        run: npm run test:${{ matrix.test-suite }}
      
      - name: Cleanup worktree
        if: always()
        run: |
          git worktree remove ~/worktrees/${{ matrix.test-suite }} -f || true
          git worktree prune
```


### Hooks Git : Post-Checkout Automatique

```bash
#!/bin/bash
# .git/hooks/post-checkout
# Hook exécuté après git worktree add

# Détecter création de worktree (prev_head = null)
PREV_HEAD=$1
NEW_HEAD=$2
BRANCH_CHECKOUT=$3

if [[ "$PREV_HEAD" == "0000000000000000000000000000000000000000" ]]; then
    echo "=== Nouveau worktree détecté ==="
    
    # Copier secrets
    if [[ -f ~/.secrets/$(basename "$(git rev-parse --show-toplevel)")/.env.local ]]; then
        cp ~/.secrets/$(basename "$(git rev-parse --show-toplevel)")/.env.local .env.local
        echo "✓ Secrets copiés"
    fi
    
    # Installer dépendances
    if [[ -f package.json ]]; then
        echo "Installation npm en cours..."
        npm install --silent &
    fi
    
    if [[ -f composer.json ]]; then
        echo "Installation Composer en cours..."
        composer install --no-interaction --quiet &
    fi
    
    wait  # Attendre fin installations parallèles
    
    echo "=== Worktree prêt ==="
fi
```


## Comparatif : Solutions et Outils 2025-2026

| **Outil** | **Type** | **Forces** | **Limitations** | **Cas d'Usage Idéal** |
| :-- | :-- | :-- | :-- | :-- |
| **Git natif** | Commande intégrée | Aucune dépendance, stable, documenté | Interface minimale, pas d'automation | Workflows simples, scripts sur mesure [^2_1][^2_3] |
| **autowt** | CLI Python | Cleanup auto, hooks lifecycle, intégration terminal | Dépendance Python 3.10+ | Développement individuel, projets Python [^2_42] |
| **worktrunk** | CLI Rust | Hooks avancés, parallélisation agents IA | Installation Rust requise | Workflows AI-first, équipes avancées [^2_41] |
| **GitLens (VS Code)** | Extension IDE | Interface graphique intuitive | Limité à VS Code | Développeurs VS Code/Cursor [^2_19][^2_49] |
| **Scripts custom bash** | Scripts shell | Personnalisation totale, portabilité | Maintenance manuelle | Production, CI/CD, besoins spécifiques [^2_13][^2_36] |

### Recommandations par Profil

**Développeur solo, projets Node.js/Python** : `autowt` + scripts custom pour edge cases[^2_42]

**Équipe développant avec agents IA (Claude, Cursor)** : `worktrunk` ou scripts spécialisés[^2_2][^2_4][^2_3][^2_41]

**Pipeline CI/CD, automatisation DevOps** : Scripts bash custom intégrés dans Jenkinsfile/GitHub Actions[^2_50]

**Débutant avec worktrees** : GitLens extension + commandes Git natives[^2_49][^2_19]

**Projets polyglots (PHP+Node+Python)** : Scripts bash génériques avec détection automatique de stack[^2_36][^2_13]

## Patterns Avancés et Optimisations

### Dépôt Bare pour Worktrees Uniquement

**Architecture recommandée pour équipes**:[^2_51][^2_16][^2_36]

```bash
# Clone initial en bare
git clone --bare git@github.com:user/repo.git projet/.bare

# Configuration pointeur
cd projet
echo "gitdir: ./.bare" > .git

# Tous les worktrees vivent au même niveau
git worktree add main main
git worktree add feature-x feature-x
git worktree add hotfix-y hotfix-y

# Structure résultante :
# projet/
# ├── .bare/          (dépôt Git bare)
# ├── .git            (fichier pointeur)
# ├── main/           (worktree main)
# ├── feature-x/      (worktree feature-x)
# └── hotfix-y/       (worktree hotfix-y)
```

**Avantages** :

- Symétrie complète : tous les worktrees égaux (pas de "principal")[^2_52]
- Facilite les opérations Git globales[^2_51]
- Idéal pour scripts d'automatisation[^2_36]


### Parallélisation avec Agents IA

**Workflow multi-agents** (Claude Code, Cursor, Windsurf):[^2_4][^2_53][^2_2][^2_3]

```bash
# Agent 1 : Feature development
wt_create() {
    local task="$1"
    git worktree add ".worktrees/$task" -b "$task"
    cd ".worktrees/$task"
    code .  # Ouvre VS Code/Cursor
    # Claude démarre automatiquement dans ce contexte
}

# Agent 2 : Code review
wt_create "review-pr-123"

# Agent 3 : Bug investigation
wt_create "debug-issue-456"
```

**Prompts recommandés pour agents IA**:[^2_53]

```
Je travaille dans un git worktree isolé situé à `.worktrees/feature-x`.

Règles strictes :
- TOUTES les opérations Git doivent rester dans ce worktree
- NE PAS créer, supprimer ou modifier d'autres worktrees
- NE PAS forcer de push ou supprimer de branches distantes
- Commits autorisés uniquement sur la branche courante

Tu peux :
- Créer des commits locaux
- Fetch/pull depuis origin
- Push cette branche vers origin

Confirme ta compréhension avant de procéder.
```


### Template de Projet avec Worktrees Pré-Configurés

**Structure de dépôt optimisée** :

```
mon-projet/
├── .git/
├── .env.template              # Template pour génération auto
├── .worktree-config           # Configuration worktrees
├── scripts/
│   ├── create-worktree.sh
│   ├── remove-worktree.sh
│   └── cleanup-merged.sh
├── .github/
│   └── workflows/
│       └── worktree-tests.yml
└── README.md
```

**`.worktree-config` exemple** :

```ini
[worktree]
    base-dir = ..
    base-port = 40000
    
[secrets]
    source-dir = ~/.secrets/mon-projet
    
[dependencies]
    auto-install = true
    parallel = true
    
[cleanup]
    auto-prune = true
    merged-branches = true
    closed-prs = true
    
[hooks]
    post-create = scripts/post-create-hook.sh
    pre-remove = scripts/pre-remove-hook.sh
```


## Ressources et Documentation

### Documentation Officielle Git

- Manuel `git-worktree` : [git-scm.com/docs/git-worktree](https://git-scm.com/docs/git-worktree)[^2_1]
- Git Layout Repository : `gitrepository-layout(5)`[^2_7][^2_10]


### Outils Open Source

| **Projet** | **URL** | **Langage** | **Description** |
| :-- | :-- | :-- | :-- |
| autowt | [irskep.github.io/autowt](https://irskep.github.io/autowt) | Python | CLI avec cleanup auto et hooks[^2_42] |
| worktrunk | [worktrunk.dev](https://worktrunk.dev) | Rust | Gestionnaire avancé pour agents IA[^2_41] |
| tomups/worktrees-scripts | [github.com/tomups/worktrees-scripts](https://github.com/tomups/worktrees-scripts) | Bash | Scripts utilitaires complets[^2_36] |
| kaeawc/auto-worktree | [github.com/kaeawc/auto-worktree](https://github.com/kaeawc/auto-worktree) | Bash | Gestion worktrees pour agents IA[^2_54] |

### Articles et Guides Récents (2025-2026)

- "Using Git Worktrees to Automate Development Environments" (2024) : Cas réel d'automatisation complète avec Docker[^2_13]
- "Git Worktrees and GitButler" (2024) : Comparaison approches workflow[^2_47]
- "Boosting Developer Productivity with Git Worktree and AI Agents" (2025) : Intégration IA[^2_3]
- "CI/CD Pipeline Integration with Git Worktrees" (2025) : Patterns Jenkins/CircleCI[^2_50]
- "Streamlining worktrees with Nx" (2026) : Intégration monorepos modernes[^2_55]


## Conclusion

Les Git worktrees représentent une capacité native de Git souvent sous-exploitée mais transformatrice pour les workflows de développement modernes. L'automatisation complète via scripts shell permet de transcender les limitations de l'interface minimaliste de Git, créant des environnements de développement parallèles isolés avec allocation dynamique de ressources (ports, bases de données, conteneurs).[^2_5][^2_3][^2_13]

Les principaux bénéfices mesurables incluent :

- **Réduction du temps de changement de contexte** : de 10-15 minutes à moins de 30 secondes[^2_13]
- **Élimination des conflits d'environnement** : isolation complète `node_modules`, `.env`, volumes Docker[^2_14][^2_15][^2_11]
- **Parallélisation native** : tests, builds, agents IA simultanés sans clonage multiple[^2_4][^2_50][^2_3]
- **Cleanup automatisé** : suppression post-merge via hooks et scripts[^2_43][^2_42][^2_41]

La clé du succès réside dans l'automatisation systématique : création de worktrees avec environnement complet (ports, secrets, dépendances), cleanup orchestré post-merge, et intégration CI/CD pour tests parallèles. Les scripts présentés dans ce guide constituent une base de production éprouvée, adaptable à tout stack technologique.[^2_50][^2_13]

Pour les équipes adoptant des workflows AI-first avec agents multiples (Claude Code, Cursor, Windsurf), les worktrees deviennent indispensables, permettant à chaque agent d'opérer dans un contexte isolé sans interférence.[^2_2][^2_53][^2_55][^2_3]

L'investissement initial dans l'infrastructure de scripts (100-300 lignes de bash bien structuré) se rentabilise dès la première semaine d'utilisation intensive, transformant Git worktrees d'une fonctionnalité expérimentale en pilier de productivité du développement moderne.[^2_56][^2_3][^2_13]
<span style="display:none">[^2_100][^2_57][^2_58][^2_59][^2_60][^2_61][^2_62][^2_63][^2_64][^2_65][^2_66][^2_67][^2_68][^2_69][^2_70][^2_71][^2_72][^2_73][^2_74][^2_75][^2_76][^2_77][^2_78][^2_79][^2_80][^2_81][^2_82][^2_83][^2_84][^2_85][^2_86][^2_87][^2_88][^2_89][^2_90][^2_91][^2_92][^2_93][^2_94][^2_95][^2_96][^2_97][^2_98][^2_99]</span>

<div align="center">⁂</div>

[^2_1]: https://git-scm.com/docs/git-worktree

[^2_2]: https://dev.to/kevinz103/git-worktree-claude-code-my-secret-to-10x-developer-productivity-520b

[^2_3]: https://elguerre.com/2025/07/21/boosting-developer-productivity-with-git-worktree-and-ai-agents/

[^2_4]: https://incident.io/blog/shipping-faster-with-claude-code-and-git-worktrees

[^2_5]: https://www.datacamp.com/fr/tutorial/git-worktree-tutorial

[^2_6]: https://stackoverflow.com/questions/53796823/git-directory-in-git-worktree-not-a-directory

[^2_7]: https://git-scm.com/docs/git-worktree/2.31.0

[^2_8]: https://morgan.cugerone.com/blog/how-to-use-git-worktree-and-in-a-clean-way/

[^2_9]: https://git-scm.com/docs/git-worktree/fr

[^2_10]: https://www.kernel.org/pub/software/scm/git/docs/gitrepository-layout.html

[^2_11]: https://dev.to/antonioaren/git-worktree-stop-stashing-start-working-in-parallel-3p17

[^2_12]: https://tpoe.dev/blog/git-worktrees

[^2_13]: https://fsck.sh/en/blog/git-worktree/

[^2_14]: https://stackoverflow.com/questions/75870668/use-of-git-worktree-to-handle-git-ignored-node-modules-of-two-existing-branches

[^2_15]: https://blog.dennisokeeffe.com/blog/2024-08-14-exploring-git-worktree

[^2_16]: https://jugmac00.github.io/blog/the-git-worktree-command/

[^2_17]: https://git-scm.com/docs/git-worktree/2.5.6

[^2_18]: https://stackoverflow.com/questions/45491328/git-add-a-worktree-from-existing-remote-branch/45491767

[^2_19]: https://www.gitkraken.com/learn/git/git-worktree

[^2_20]: https://stackoverflow.com/questions/46102041/git-get-worktree-for-every-branch-in-seperate-folders-bash

[^2_21]: https://stackoverflow.com/questions/78720671/how-to-find-the-worktree-path-of-a-branch

[^2_22]: https://git-scm.com/docs/git-worktree/2.7.6

[^2_23]: https://git-scm.com/docs/git-worktree/2.35.0

[^2_24]: https://www.codeease.net/programming/shell/git-worktree-remove

[^2_25]: https://fig.io/manual/git/worktree/remove

[^2_26]: https://musteresel.github.io/posts/2018/01/git-worktree-gotcha-removed-directory.html

[^2_27]: https://stacktoheap.com/blog/2016/01/19/using-multiple-worktrees-with-git/

[^2_28]: https://stackoverflow.com/questions/48346607/git-worktree-prune-what-it-does

[^2_29]: https://getdocs.org/Git/docs/latest/git-worktree

[^2_30]: https://stackoverflow.com/questions/41545293/branch-is-already-checked-out-at-other-location-in-git-worktrees

[^2_31]: https://www.datacamp.com/tutorial/git-worktree-tutorial

[^2_32]: https://stackoverflow.com/questions/39665570/why-can-two-git-worktrees-not-check-out-the-same-branch

[^2_33]: https://morgan.cugerone.com/blog/workarounds-to-git-worktree-using-bare-repository-and-cannot-fetch-remote-branches/

[^2_34]: https://stackoverflow.com/questions/63826602/git-worktree-is-invalid-how-to-correct-this-with-git-commands

[^2_35]: https://stackoverflow.com/questions/66635437/git-worktree-with-relative-path

[^2_36]: https://github.com/tomups/worktrees-scripts

[^2_37]: https://smarak.dev/blog/git_worktree_hook/

[^2_38]: https://stackoverflow.com/questions/50135844/what-does-git-do-when-we-do-git-gc-git-prune

[^2_39]: https://git-scm.com/docs/githooks

[^2_40]: https://stackoverflow.com/questions/70953062/how-to-run-a-git-hook-only-when-running-git-worktree-add-command

[^2_41]: https://worktrunk.dev/hook/

[^2_42]: https://irskep.github.io/autowt/

[^2_43]: https://www.buildwithclaude.com/command/create-worktrees

[^2_44]: https://www.graphapp.ai/blog/git-worktree-tutorial-a-step-by-step-guide-for-beginners

[^2_45]: https://stackoverflow.com/questions/59474143/add-existing-directory-as-branch-to-git-with-worktree

[^2_46]: https://codeinput.com/en/guides/git/errors/error-04

[^2_47]: https://blog.gitbutler.com/git-worktrees

[^2_48]: https://www.gitkraken.com/learn/git/tutorials/how-to-resolve-merge-conflict-in-git

[^2_49]: https://dev.to/nickytonline/git-worktrees-git-done-right-2p7f

[^2_50]: https://gitcheatsheet.dev/docs/advanced/worktrees/ci-cd-integration/

[^2_51]: https://stackoverflow.com/questions/64458949/is-there-a-good-reason-why-working-trees-should-be-created-at-the-same-directory

[^2_52]: https://matklad.github.io/2024/07/25/git-worktrees.html

[^2_53]: https://www.nrmitchi.com/2025/10/using-git-worktrees-for-multi-feature-development-with-ai-agents/

[^2_54]: https://github.com/kaeawc/auto-worktree

[^2_55]: https://nx.dev/blog/git-worktrees-ai-agents

[^2_56]: https://devdynamics.ai/blog/understanding-git-worktree-to-fast-track-software-development-process/

[^2_57]: https://www.reddit.com/r/git/comments/ljq272/can_someone_explain_to_me_how_a_git_dir_and_a/

[^2_58]: https://stevekinney.com/courses/ai-development/git-worktrees

[^2_59]: https://www.reddit.com/r/git/comments/ora5lg/automatic_branch_deletion_after_a_successful_merge/

[^2_60]: https://forum.cursor.com/t/cursors-worktreemanager-force-deleted-my-git-branch-when-cleaning-up-agent-worktrees/146865

[^2_61]: https://stackoverflow.com/questions/65300972/worktree-branches-in-git-show-unmerged-even-after-merging

[^2_62]: https://fr.linkedin.com/pulse/master-your-git-workflow-stop-stashing-start-using-singh-rathore-zdpqc?tl=fr

[^2_63]: https://www.linkedin.com/pulse/automating-git-task-pm2-deployment-tasks-bash-scripts-godwin-omale-48zlf

[^2_64]: https://www.reddit.com/r/git/comments/1ana4h6/getting_merge_conflicts_but_my_working_tree_is/

[^2_65]: https://stackoverflow.com/questions/1456923/why-am-i-getting-the-message-fatal-this-operation-must-be-run-in-a-work-tree

[^2_66]: https://stackoverflow.com/questions/38139279/what-is-the-best-way-to-handle-tree-conflicts-in-git

[^2_67]: https://dev.to/b1o5/automate-your-git-workflow-with-this-simple-bash-script-5cm5

[^2_68]: https://stackoverflow.com/questions/79186993/using-git-hooks-with-worktree

[^2_69]: https://www.reddit.com/r/git/comments/130vtm7/using_git_hooks_to_prevent_bad_merges/

[^2_70]: https://github.com/ryands17/worktree-scripts

[^2_71]: https://gist.github.com/ashwch/946ad983977c9107db7ee9abafeb95bd

[^2_72]: https://gitscripts.com/git-worktree-remove

[^2_73]: https://github.com/topics/git-worktree

[^2_74]: https://github.com/2KAbhishek/talks/blob/main/parallel-dev-with-worktrees.md

[^2_75]: https://github.com/wadackel/ofsht

[^2_76]: https://github.com/ajeetdsouza/zoxide/discussions/970

[^2_77]: https://www.ocuroot.com/blog/things-i-learned-about-git/

[^2_78]: https://sterba.dev/posts/git-worktree/

[^2_79]: https://stackoverflow.com/questions/10821825/how-to-set-git-dir-git-work-tree-when-maintaining-multiple-repositories

[^2_80]: https://github.com/magit/magit/issues/460

[^2_81]: https://positivethinking.tech/insights/switching-branches-with-git-worktrees/

[^2_82]: https://chromium.googlesource.com/external/gitster/git-htmldocs/+/188ae81bab23d645a02ed4f442ddafe9099d6e97/git-worktree.adoc

[^2_83]: https://www.reddit.com/r/git/comments/17pyvxv/i_wrote_a_utility_that_enables_multiple_worktrees/

[^2_84]: https://www.geeksforgeeks.org/git/git-worktree/

[^2_85]: https://www.graphapp.ai/blog/how-to-use-git-worktree-a-step-by-step-example

[^2_86]: https://raw.githubusercontent.com/git/git/master/contrib/completion/git-completion.bash

[^2_87]: https://x.com/kieranklaassen/status/1930032748951154966

[^2_88]: https://mcpmarket.com/tools/skills/git-worktree-automation

[^2_89]: https://oliviac.dev/blog/build-git-helpers-bash-fzf/

[^2_90]: https://chrisdicarlo.ca/blog/working-with-git-worktrees-part-2/

[^2_91]: https://dev.to/satococoa/wtp-a-better-git-worktree-cli-tool-4i8l

[^2_92]: https://github.com/Kristian-Tan/git-worktree-relative

[^2_93]: https://stackoverflow.com/questions/6034472/git-bash-completion-with-filename-support

[^2_94]: https://gist.github.com/nazq/8a47bc731ea256c899d9ac160e861b49

[^2_95]: https://stackoverflow.com/questions/69303280/how-to-merge-branch-from-another-worktree

[^2_96]: https://stackoverflow.com/questions/35598477/git-worktree-two-worktrees-point-in-the-same-location-cannot-be-prune

[^2_97]: https://blog.itdepends.be/parallel-workflows-git-worktrees-agents/

[^2_98]: https://fig.io/manual/git/worktree/prune

[^2_99]: https://www.reddit.com/r/git/comments/1ay3z44/pass_results_of_git_status_to_command_line/

[^2_100]: https://manpages.ubuntu.com/manpages/focal/man1/git-worktree.1.html

