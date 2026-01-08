# Documentation Anthropic - Référence Complète
# Système Plugins, Marketplace & Architecture Claude Code

*Documentation extraite des sources officielles Anthropic*
*Date : 12 Octobre 2025*

---

## 📚 Table des Matières

1. [Plugins](#plugins)
2. [Plugin Marketplaces](#plugin-marketplaces)
3. [Slash Commands Personnalisés](#slash-commands-personnalisés)
4. [Sub-Agents](#sub-agents)
5. [Hooks System](#hooks-system)
6. [Plugins Reference Technique](#plugins-reference-technique)

---

## 1. Plugins

### Qu'est-ce qu'un Plugin ?

Les plugins étendent Claude Code avec des fonctionnalités personnalisées :
- **Commands** - Slash commands personnalisées
- **Agents** - Agents spécialisés
- **Hooks** - Event handlers
- **MCP Servers** - Connexions outils externes

**Avantages** :
- Partage entre projets et équipes
- Installation depuis marketplaces
- Création locale pour besoins spécifiques

### Structure d'un Plugin

```
my-first-plugin/
├── .claude-plugin/
│   └── plugin.json          # Métadonnées plugin (requis)
├── commands/                 # Slash commands custom (optionnel)
│   └── hello.md
├── agents/                   # Agents spécialisés (optionnel)
│   └── helper.md
└── hooks/                    # Event handlers (optionnel)
    └── hooks.json
```

### Fichier `plugin.json` (Configuration Principale)

```json
{
  "name": "mon-plugin",
  "version": "1.0.0",
  "description": "Description du plugin",
  "author": {
    "name": "Votre Nom",
    "email": "votre@email.com",
    "url": "https://github.com/compte"
  },
  "homepage": "https://github.com/compte/mon-plugin",
  "repository": "https://github.com/compte/mon-plugin",
  "license": "MIT",
  "keywords": ["web-development", "automation"]
}
```

### Créer un Plugin

1. **Créer la structure de base**
```bash
mkdir my-first-plugin
cd my-first-plugin
mkdir -p .claude-plugin commands agents hooks
```

2. **Créer plugin.json**
```bash
cat > .claude-plugin/plugin.json <<EOF
{
  "name": "my-first-plugin",
  "version": "1.0.0",
  "description": "Mon premier plugin"
}
EOF
```

3. **Ajouter des composants** (commands, agents, hooks)

4. **Tester localement** avec un marketplace de développement

### Installation de Plugins

#### Méthode Interactive (Recommandée)
```bash
/plugin                          # Menu interactif
```

#### Méthode CLI Directe
```bash
/plugin marketplace add <url>    # Ajouter marketplace
/plugin install <nom-plugin>     # Installer plugin
```

### Gestion de Plugins

```bash
/plugin enable <nom>             # Activer plugin
/plugin disable <nom>            # Désactiver plugin
/plugin list                     # Lister plugins installés
/help                            # Voir commandes disponibles
```

### Best Practices

- ✅ Inclure documentation (README.md)
- ✅ Utiliser semantic versioning
- ✅ Tester complètement avant distribution
- ✅ Créer un marketplace pour partage facile

---

## 2. Plugin Marketplaces

### Qu'est-ce qu'un Marketplace ?

Un marketplace est un **fichier JSON** qui sert de catalogue pour plugins Claude Code.

**Fonctionnalités** :
- Découverte centralisée de plugins
- Gestion automatique des versions
- Distribution à l'échelle de l'équipe
- Sources de plugins flexibles

### Structure Marketplace

**Fichier** : `.claude-plugin/marketplace.json`

```json
{
  "name": "mon-marketplace",
  "owner": {
    "name": "Organisation",
    "email": "contact@org.com"
  },
  "description": "Marketplace pour plugins web dev",
  "plugins": [
    {
      "name": "mon-plugin",
      "source": "./",
      "description": "Plugin web development",
      "version": "1.0.0",
      "category": "Web Development",
      "author": {
        "name": "Auteur",
        "email": "auteur@email.com"
      },
      "homepage": "https://github.com/org/mon-plugin",
      "repository": "https://github.com/org/mon-plugin",
      "commands": [
        "./commands/analyze.md",
        "./commands/build.md"
      ],
      "agents": [
        "./agents/frontend.md"
      ]
    }
  ]
}
```

### Champs Marketplace

#### Requis
- `name` - Identifiant marketplace
- `owner` - Info mainteneur
- `plugins` - Liste plugins disponibles

#### Plugin Entry (minimum requis : `name`)
- `description` - Description plugin
- `version` - Version semantic
- `author` - Info auteur
- `homepage` - URL homepage
- `repository` - URL repository
- `commands` - Chemins vers commandes
- `agents` - Chemins vers agents

### Options de Source Plugin

1. **Chemins relatifs** (même repository)
```json
"source": "./"
"source": "./plugins/my-plugin"
```

2. **GitHub repositories**
```json
"source": "https://github.com/user/plugin"
```

3. **Git repositories**
```json
"source": "https://gitlab.com/company/plugin.git"
```

4. **Répertoires locaux** (développement)
```json
"source": "./local-dev-plugin"
```

### Ajouter un Marketplace

```bash
# GitHub repository
/plugin marketplace add owner/repo

# GitLab repository
/plugin marketplace add https://gitlab.com/company/plugins.git

# Répertoire local
/plugin marketplace add ./my-marketplace
```

### Installation depuis Marketplace

#### Interactive
```bash
/plugin                          # Naviguer et sélectionner
```

#### Direct
```bash
/plugin install plugin-name@marketplace-name
```

### Best Practices Marketplaces

- ✅ **Hébergement GitHub** (recommandé)
- ✅ **Versioning clair** (semantic versioning)
- ✅ **Documentation complète** pour chaque plugin
- ✅ **Validation JSON** avant distribution

### Troubleshooting

**Problèmes courants** :
- ❌ JSON formaté incorrectement
- ❌ Repository source inaccessible
- ❌ Fichiers manifest plugin manquants

---

## 3. Slash Commands Personnalisés

### Vue d'Ensemble

Les slash commands sont des **commandes personnalisées** définies en Markdown.

**Format** : `/<command-name> [arguments]`

### Types de Commands

#### 1. Project Commands
**Location** : `.claude/commands/`
- Partagées avec l'équipe
- Versionnées avec le projet

**Création** :
```bash
mkdir -p .claude/commands
echo "Analyze this code for performance issues:" > .claude/commands/optimize.md
```

#### 2. Personal Commands
**Location** : `~/.claude/commands/`
- Disponibles dans tous les projets
- Configuration personnelle

**Création** :
```bash
mkdir -p ~/.claude/commands
echo "Review code for security vulnerabilities:" > ~/.claude/commands/security-review.md
```

### Structure d'une Commande

**Fichier** : `commands/my-command.md`

```markdown
---
description: Brief command description
argument-hint: [expected arguments]
allowed-tools: Bash(git add:*), Bash(git commit:*)
model: sonnet
---

Command prompt content with instructions for Claude.

Use $ARGUMENTS to capture all arguments.
Use $1, $2, etc. for specific positional arguments.

## Context
Variables: {{argument}}

## Output Format
Expected format description
```

### Frontmatter Options

```yaml
---
description: "Command description"
argument-hint: "[commit message]"
allowed-tools: "Bash(git add:*), Bash(git commit:*)"
model: "sonnet|opus|haiku"
---
```

**Champs disponibles** :
- `description` - Description brève de la commande
- `argument-hint` - Décrire les arguments attendus
- `allowed-tools` - Outils permis pour cette commande
- `model` - Modèle AI à utiliser (sonnet, opus, haiku)

### Arguments

**Capture tous les arguments** :
```markdown
Use the following arguments: $ARGUMENTS
```

**Arguments positionnels** :
```markdown
First argument: $1
Second argument: $2
```

### Exemple Complet

**Fichier** : `.claude/commands/commit.md`

```markdown
---
allowed-tools: Bash(git add:*), Bash(git commit:*)
argument-hint: [commit message]
description: Create a git commit with structured message
---

Create a git commit following our team conventions.

## Instructions

1. Stage relevant files with `git add`
2. Create commit with message: $ARGUMENTS
3. Follow commit message format:
   - type(scope): description
   - body (optional)
   - footer (optional)

## Validation

- Message must be clear and descriptive
- Use conventional commit format
- Include issue number if applicable
```

### Features Avancées

**Bash commands** avec préfixe `!` :
```bash
/my-command !ls -la
```

**File references** avec préfixe `@` :
```bash
/my-command @src/main.ts
```

**Extended thinking** :
```bash
/my-command --think-hard
```

### Namespacing

Organiser commandes dans sous-répertoires :
```
.claude/commands/
├── git/
│   ├── commit.md       # /commit
│   └── review.md       # /review
└── build/
    ├── frontend.md     # /frontend
    └── backend.md      # /backend
```

Les noms de sous-répertoires apparaissent dans la description de la commande.

---

## 4. Sub-Agents

### Qu'est-ce qu'un Sub-Agent ?

Les sub-agents sont des **assistants AI spécialisés** avec :
- Context window séparé de la conversation principale
- System prompt personnalisable
- Expertise et objectif spécifiques
- Accès aux outils configurable

### Caractéristiques

**Avantages** :
- Préservent le contexte principal
- Permettent sessions plus longues
- Spécialisation par domaine
- Délégation intelligente

### Création de Sub-Agents

#### Méthode 1 : Interactive
```bash
/agents                          # Menu de création
```

#### Méthode 2 : Fichier Manuel

**Project-level** : `.claude/agents/`
**Personal-level** : `~/.claude/agents/`

**Fichier** : `.claude/agents/reviewer.md`

```markdown
---
description: Code reviewer specialist
subagent_type: qa-specialist
---

You are a code reviewer focused on:
- Code quality and maintainability
- Security vulnerabilities
- Performance optimization
- Best practices compliance

## Capabilities

- Static code analysis
- Security scanning
- Performance profiling
- Documentation validation

## MCP Servers

Primary: Sequential (systematic analysis)
Secondary: Context7 (best practices patterns)

## Quality Standards

- Follow SOLID principles
- Ensure test coverage ≥80%
- Check for common vulnerabilities
- Validate documentation completeness
```

#### Méthode 3 : CLI Configuration

```bash
claude --agents reviewer,debugger
```

### Options de Configuration

```yaml
name: "Code Reviewer"
description: "Analyzes code quality and security"
tools: ["Read", "Grep", "Sequential"]
model: "inherit|sonnet|opus|haiku"
```

**Champs** :
- `name` - Nom du sub-agent
- `description` - Description objectif
- `tools` - Outils accessibles
- `model` - Modèle AI à utiliser

### Subagent Types Disponibles

**Types natifs Claude Code** :
- `general-purpose` - Multi-domaine, recherche complexe
- `frontend-specialist` - UI/UX, React, Vue, accessibility
- `backend-specialist` - APIs, databases, architecture serveur
- `qa-specialist` - Testing, quality assurance, validation
- `devops-specialist` - CI/CD, infrastructure, déploiement
- `coordinator` - Orchestration multi-agents

### Patterns de Délégation

#### 1. Automatique
Claude assigne proactivement les tâches aux agents appropriés.

```bash
# Claude détecte automatiquement le besoin
User: "Review this code for security issues"
# → Active automatiquement security-agent
```

#### 2. Explicite
Invocation manuelle avec nom d'agent.

```bash
# Invocation explicite
User: "Use the code-reviewer subagent to analyze @src/"
```

### Exemples de Sub-Agents

#### Code Reviewer
```markdown
---
description: Code quality and security checker
subagent_type: qa-specialist
---

Specialized in code reviews with focus on:
- Code quality metrics
- Security vulnerabilities
- Performance bottlenecks
- Best practices compliance
```

#### Debugger
```markdown
---
description: Root cause analysis specialist
subagent_type: general-purpose
---

Expert in debugging with systematic approach:
- Reproduce issues
- Identify root causes
- Propose fixes
- Validate solutions
```

#### Data Scientist
```markdown
---
description: SQL and data analysis expert
subagent_type: backend-specialist
---

Handles data-related tasks:
- SQL query optimization
- Data analysis and visualization
- Database schema design
- Performance tuning
```

### Best Practices

- ✅ **Focus unique** - Un objectif par agent
- ✅ **System prompts détaillés** - Instructions claires
- ✅ **Limiter outils** - Accès minimal nécessaire
- ✅ **Version control** - Agents project-level dans git

### Features Avancées

#### Chaining Multiple Subagents
```
Main → Analyzer → Reviewer → Documenter
```

#### Dynamic Selection
Claude sélectionne automatiquement l'agent basé sur le contexte.

### Performance Note

> "Agents help preserve main context, enabling longer overall sessions"

Les sub-agents permettent de préserver le contexte principal et d'étendre la durée des sessions.

---

## 5. Hooks System

### Vue d'Ensemble

Les hooks sont des **commandes shell définies par l'utilisateur** qui s'exécutent à divers points du cycle de vie de Claude Code.

**Purpose** : Contrôle déterministe du comportement

### Hook Events Disponibles

#### 1. **PreToolUse**
S'exécute **avant** les appels d'outils (peut les bloquer)

**Use cases** :
- Validation avant modification
- Blocage opérations sensibles
- Logging préventif

#### 2. **PostToolUse**
S'exécute **après** complétion des appels d'outils

**Use cases** :
- Formatage automatique code
- Validation post-modification
- Notifications succès/échec

#### 3. **UserPromptSubmit**
S'exécute quand l'utilisateur soumet un prompt

**Use cases** :
- Validation input utilisateur
- Logging requêtes
- Context enrichment

#### 4. **Notification**
S'exécute lors d'envoi de notifications par Claude Code

**Use cases** :
- Notifications custom
- Alertes externes
- Logging notifications

#### 5. **Stop**
S'exécute quand Claude Code termine de répondre

**Use cases** :
- Nettoyage post-réponse
- Logging réponses
- Métriques performance

#### 6. **SubagentStop**
S'exécute à la fin des tâches de sub-agents

**Use cases** :
- Validation résultats agents
- Métriques délégation
- Handoff coordination

#### 7. **PreCompact**
S'exécute avant opérations de compactage

**Use cases** :
- Backup contexte
- Validation avant compression
- Métriques mémoire

#### 8. **SessionStart**
S'exécute au démarrage ou reprise de session

**Use cases** :
- Initialisation environnement
- Chargement configuration
- Logging session

#### 9. **SessionEnd**
S'exécute à la fin de session

**Use cases** :
- Cleanup ressources
- Sauvegarde état
- Métriques session

### Configuration Hooks

**Location** :
- User settings (global) : `~/.claude/hooks/hooks.json`
- Project settings : `.claude/hooks/hooks.json`

**Structure** :
```json
{
  "hooks": {
    "EventType": [
      {
        "matcher": "Tool1|Tool2",
        "hooks": [
          {
            "type": "command",
            "command": "script-or-command"
          }
        ]
      }
    ]
  }
}
```

### Exemples de Hooks

#### 1. Logging Bash Commands

**Purpose** : Logger toutes les commandes bash exécutées

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "jq -r '\"\\(.tool_input.command) - \\(.tool_input.description // \\\"No description\\\")\"' >> ~/.claude/bash-command-log.txt"
          }
        ]
      }
    ]
  }
}
```

#### 2. Auto-Formatting TypeScript

**Purpose** : Formater automatiquement fichiers TypeScript après modification

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|MultiEdit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "npx prettier --write \"$file_path\""
          }
        ]
      }
    ]
  }
}
```

#### 3. Git Pre-Commit Hook

**Purpose** : Valider code avant commit

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash(git commit:*)",
        "hooks": [
          {
            "type": "command",
            "command": "npm run lint && npm run test"
          }
        ]
      }
    ]
  }
}
```

#### 4. Notification Custom

**Purpose** : Envoyer notifications externes

```json
{
  "hooks": {
    "Notification": [
      {
        "matcher": "*",
        "hooks": [
          {
            "type": "command",
            "command": "osascript -e 'display notification \"$notification_content\" with title \"Claude Code\"'"
          }
        ]
      }
    ]
  }
}
```

### Use Cases Courants

1. **Formatage automatique**
   - Prettier, ESLint, Black, etc.

2. **Notifications custom**
   - Slack, Discord, email alerts

3. **Logging**
   - Commandes exécutées, modifications fichiers

4. **Feedback conventions**
   - Validation style code, naming conventions

5. **Blocage modifications sensibles**
   - Protection fichiers critiques

### Hook Components

#### 1. Event Type
Type d'événement à intercepter (PreToolUse, PostToolUse, etc.)

#### 2. Matcher
Quels outils/événements cibler
- `"*"` - Tous les outils
- `"Tool1|Tool2"` - Outils spécifiques
- `"Bash(git:*)"` - Bash avec pattern git

#### 3. Hook Command
Commande shell à exécuter

**Variables disponibles** :
- `$file_path` - Chemin fichier modifié
- `$tool_name` - Nom outil utilisé
- `$tool_input` - Input outil (JSON)
- `$notification_content` - Contenu notification

### Security Warning

> ⚠️ **IMPORTANT** : "Always review your hooks implementation before registering them"

Les hooks s'exécutent avec les credentials de votre environnement actuel.

**Best Practices** :
- ✅ Tester dans environnement isolé
- ✅ Valider commandes shell
- ✅ Limiter accès sensible
- ✅ Logger activité hooks

---

## 6. Plugins Reference Technique

### Composants Plugin

#### 1. Commands
- **Location** : `commands/`
- **Format** : Fichiers Markdown avec frontmatter
- **Integration** : Système de commandes Claude Code

#### 2. Agents
- **Location** : `agents/`
- **Format** : Fichiers Markdown décrivant sub-agents spécialisés
- **Invocation** : Automatique ou manuelle

#### 3. Hooks
- **Configuration** : `hooks/hooks.json`
- **Events** : PreToolUse, PostToolUse, UserPromptSubmit, etc.
- **Types** : command, validation, notification

#### 4. MCP Servers
- **Configuration** : `.mcp.json`
- **Purpose** : Connexion outils et services externes
- **Démarrage** : Automatique quand plugin activé

### Plugin Manifest (`plugin.json`)

#### Champs Requis
- `name` - Nom unique du plugin
- `version` - Version semantic (semver)

#### Metadata (Optionnels)
- `description` - Description courte
- `author` - Info auteur (name, email, url)
- `homepage` - URL homepage
- `repository` - URL repository
- `license` - Type de license (MIT, Apache, etc.)
- `keywords` - Mots-clés pour recherche

#### Component Paths
- `commands` - Tableau chemins vers commandes
- `agents` - Tableau chemins vers agents
- `hooks` - Chemin vers fichier hooks
- `mcpServers` - Configuration MCP servers

### Structure Complète Plugin Enterprise

```
enterprise-plugin/
├── .claude-plugin/
│   └── plugin.json                 # Manifest principal
├── commands/                       # Slash commands
│   ├── analyze.md
│   ├── deploy.md
│   └── review.md
├── agents/                         # Sub-agents spécialisés
│   ├── code-reviewer.md
│   ├── security-auditor.md
│   └── performance-optimizer.md
├── hooks/                          # Event handlers
│   └── hooks.json
├── .mcp.json                       # MCP servers config
├── scripts/                        # Helper scripts
│   ├── format.sh
│   └── validate.sh
├── README.md                       # Documentation
├── CHANGELOG.md                    # Historique versions
└── LICENSE                         # License file
```

### Exemple `plugin.json` Complet

```json
{
  "name": "enterprise-plugin",
  "version": "2.1.0",
  "description": "Enterprise development plugin with advanced workflows",
  "author": {
    "name": "Company Name",
    "email": "dev@company.com",
    "url": "https://company.com"
  },
  "homepage": "https://github.com/company/enterprise-plugin",
  "repository": "https://github.com/company/enterprise-plugin",
  "license": "MIT",
  "keywords": [
    "enterprise",
    "workflow",
    "automation",
    "security",
    "performance"
  ],
  "commands": [
    "./commands/analyze.md",
    "./commands/deploy.md",
    "./commands/review.md"
  ],
  "agents": [
    "./agents/code-reviewer.md",
    "./agents/security-auditor.md",
    "./agents/performance-optimizer.md"
  ],
  "hooks": "./hooks/hooks.json",
  "mcpServers": "./.mcp.json"
}
```

### Debugging Plugins

#### Activer Mode Debug
```bash
claude --debug
```

**Affiche** :
- Détails chargement plugins
- Erreurs parsing
- Warnings configuration

#### Problèmes Courants

1. **Plugin non chargé**
   - ❌ Syntax JSON invalide
   - ❌ Chemins fichiers incorrects
   - ❌ Structure répertoires manquante

2. **Commandes non reconnues**
   - ❌ Frontmatter incorrect
   - ❌ Fichiers non dans `commands/`
   - ❌ Plugin non activé

3. **Agents non disponibles**
   - ❌ Description manquante
   - ❌ Fichiers non dans `agents/`
   - ❌ Subagent type invalide

4. **Hooks non exécutés**
   - ❌ Permissions script insuffisantes
   - ❌ Matcher incorrect
   - ❌ Hooks.json invalide

#### Solutions Debugging

**Vérifier structure** :
```bash
tree .claude-plugin/
ls -la commands/
ls -la agents/
```

**Valider JSON** :
```bash
jq . .claude-plugin/plugin.json
jq . hooks/hooks.json
```

**Vérifier permissions** :
```bash
chmod +x scripts/*.sh
```

### Versioning

#### Semantic Versioning (semver)

Format : `MAJOR.MINOR.PATCH`

- **MAJOR** - Breaking changes
- **MINOR** - New features (backward compatible)
- **PATCH** - Bug fixes

**Exemples** :
- `1.0.0` - Release initiale
- `1.1.0` - Ajout features
- `1.1.1` - Bug fixes
- `2.0.0` - Breaking changes

#### CHANGELOG.md

**Format recommandé** :
```markdown
# Changelog

## [2.0.0] - 2025-10-12

### Added
- New security agent
- Performance optimization commands

### Changed
- Updated command syntax
- Improved agent delegation

### Fixed
- Hook execution bug
- Marketplace loading issue

### Breaking Changes
- Renamed command `/old` to `/new`
- Updated agent configuration format
```

---

## 📚 Ressources Supplémentaires

### Documentation Officielle
- **Claude Code Docs** : [docs.claude.com/claude-code](https://docs.claude.com/en/docs/claude-code)
- **GitHub** : [github.com/anthropics/claude-code](https://github.com/anthropics/claude-code)

### Pages Spécifiques
- **Plugins** : [docs.claude.com/en/docs/claude-code/plugins](https://docs.claude.com/en/docs/claude-code/plugins)
- **Plugin Reference** : [docs.claude.com/en/docs/claude-code/plugins-reference](https://docs.claude.com/en/docs/claude-code/plugins-reference)
- **Marketplaces** : [docs.claude.com/en/docs/claude-code/plugin-marketplaces](https://docs.claude.com/en/docs/claude-code/plugin-marketplaces)
- **Slash Commands** : [docs.claude.com/en/docs/claude-code/slash-commands](https://docs.claude.com/en/docs/claude-code/slash-commands)
- **Sub-Agents** : [docs.claude.com/en/docs/claude-code/sub-agents](https://docs.claude.com/en/docs/claude-code/sub-agents)
- **Hooks** : [docs.claude.com/en/docs/claude-code/hooks-guide](https://docs.claude.com/en/docs/claude-code/hooks-guide)

### Community
- **Discord Claude** - Support communautaire
- **GitHub Discussions** - Discussions techniques
- **GitHub Issues** - Bug reports et feature requests

---

*Document compilé depuis documentation officielle Anthropic*
*Pour informations les plus récentes, consulter [docs.claude.com](https://docs.claude.com)*
