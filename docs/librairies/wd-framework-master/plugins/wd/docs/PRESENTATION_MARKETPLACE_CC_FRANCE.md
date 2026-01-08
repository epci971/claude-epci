---
marp: true
theme: default
class: invert
paginate: true
backgroundColor: #1a1a1a
color: #ffffff
style: |
  section {
    background-color: #1a1a1a;
    color: #ffffff;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  }
  h1 {
    color: #D97757;
    font-size: 3.5em;
    font-weight: 700;
    margin-bottom: 0.5em;
  }
  h2 {
    color: #D97757;
    font-size: 2.5em;
    margin-bottom: 0.5em;
  }
  h3 {
    color: #B58663;
    font-size: 1.8em;
  }
  strong {
    color: #D97757;
  }
  code {
    background-color: #2d2d2d;
    padding: 0.2em 0.4em;
    border-radius: 3px;
    color: #D97757;
  }
  pre {
    background-color: #2d2d2d;
    border-radius: 8px;
    padding: 1em;
  }
  ul {
    line-height: 1.8;
  }
  li {
    margin-bottom: 0.5em;
  }
  .columns {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 2em;
  }
  .highlight {
    background: linear-gradient(135deg, #D97757 0%, #B58663 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    font-weight: 700;
  }
---

<!-- _class: lead -->

# 🔌 Claude Code
# Marketplace & Plugins

**Créer et Distribuer vos Propres Extensions**

---
*Présentation Claude Code France - Octobre 2025*
*Para CC-France*

---

# 📋 Au Programme

1. **Introduction** - Pourquoi des plugins ?
2. **Architecture** - Comment ça marche ?
3. **Marketplace** - Système de distribution
4. **Création** - Développer votre plugin
5. **Publication** - Partager avec la communauté
6. **Exemple Réel** - WD Framework
7. **Best Practices** - Conseils et astuces
8. **Démonstration** - Live coding
9. **Q&A** - Vos questions

---

# 🎯 Pourquoi des Plugins ?

## Le Problème

<div class="columns">

### ❌ Sans Plugins
- Configuration manuelle répétitive
- Commandes custom dispersées
- Pas de partage communautaire
- Réinventer la roue à chaque projet
- Pas de versioning des workflows

### ✅ Avec Plugins
- Installation en une commande
- Commandes prêtes à l'emploi
- Marketplace communautaire
- Réutilisation et partage
- Versioning et mises à jour

</div>

---

# 🎯 Cas d'Usage Plugins

## Exemples Concrets

### 🛠️ Développement
- **Frameworks spécifiques** - React, Vue, Angular workflows
- **Langages** - Python, Rust, Go best practices
- **Outils** - Docker, Kubernetes, CI/CD automation

### 🏢 Entreprise
- **Standards internes** - Guidelines et templates d'équipe
- **Intégrations** - ERP, CRM, systèmes propriétaires
- **Workflows métier** - Processus spécifiques industrie

### 🎓 Éducation
- **Tutoriels interactifs** - Guides pas-à-pas
- **Templates étudiants** - Projets préconfigurés
- **Code reviews** - Feedback automatisé

---

# 🏗️ Architecture Claude Code

## Vue d'Ensemble du Système

```
Claude Code Architecture
│
├── 🧠 Claude AI Core
│   ├── Native Tools (Read, Write, Edit, Bash, etc.)
│   ├── Task Tool (Sub-agents)
│   └── MCP Servers (Context7, Sequential, Magic, Playwright)
│
├── 🔌 Plugin System
│   ├── Local Plugins (~/.claude/plugins/)
│   ├── Marketplace Plugins (repos GitHub)
│   └── Plugin Manager (/plugin commands)
│
├── 📦 Marketplace System
│   ├── Marketplace Repositories (GitHub)
│   ├── Plugin Discovery & Installation
│   └── Update Management
│
└── 💬 User Interface
    ├── Chat Interface
    ├── Slash Commands (/command)
    └── Agent Invocations (@agent)
```

---

# 🔌 Qu'est-ce qu'un Plugin ?

## Définition

Un **plugin Claude Code** est un ensemble de fichiers structurés qui étend les capacités de Claude avec :

<div class="columns">

### 📋 Composants Principaux
- **Slash commands** personnalisées
- **Agents spécialisés** (Task tool)
- **Configuration** orchestration
- **Documentation** intégrée
- **Métadonnées** versioning

### 🎯 Objectifs
- **Réutilisabilité** - DRY principle
- **Partageabilité** - Open source
- **Maintenabilité** - Versioning
- **Découvrabilité** - Marketplace
- **Qualité** - Best practices

</div>

---

# 📁 Structure d'un Plugin

## Anatomie Complète

```
mon-plugin/
├── .claude-plugin/                    # Métadonnées plugin
│   ├── plugin.json                    # Configuration principale
│   └── marketplace.json               # Info marketplace (optionnel)
│
├── commands/                          # Slash commands
│   ├── analyze.md                     # /mon-plugin:analyze
│   ├── build.md                       # /mon-plugin:build
│   └── deploy.md                      # /mon-plugin:deploy
│
├── agents/                            # Agents spécialisés (optionnel)
│   ├── frontend.md                    # Agent frontend
│   └── backend.md                     # Agent backend
│
├── .claude/                           # Orchestration (optionnel)
│   ├── CLAUDE.md                      # Entry point
│   ├── RULES.md                       # Règles opérationnelles
│   └── PRINCIPLES.md                  # Principes dev
│
└── README.md                          # Documentation utilisateur
```

---

# 📋 plugin.json - Configuration

## Fichier Principal du Plugin

```json
{
  "name": "mon-plugin",
  "version": "1.0.0",
  "description": "Description courte du plugin",
  "author": {
    "name": "Votre Nom",
    "email": "votre@email.com",
    "url": "https://github.com/votre-compte"
  },
  "homepage": "https://github.com/votre-compte/mon-plugin",
  "repository": "https://github.com/votre-compte/mon-plugin",
  "license": "MIT",
  "keywords": [
    "web-development",
    "react",
    "typescript"
  ]
}
```

---

# 📋 marketplace.json - Distribution

## Configuration Marketplace (Optionnel)

```json
{
  "name": "mon-marketplace",
  "owner": {
    "name": "Votre Organisation",
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

---

# 💬 Slash Commands

## Créer une Commande Personnalisée

### Fichier : `commands/analyze.md`

```markdown
---
description: Analyze codebase for issues and improvements
arguments:
  - name: target
    description: File or directory to analyze
    required: false
---

You are analyzing the codebase for potential issues.

## Instructions

1. Use Grep to search for common anti-patterns
2. Use Read to examine file structure
3. Provide actionable recommendations
4. Focus on: security, performance, maintainability

## Context

Target: {{target || "current directory"}}
Focus on web development best practices.
```

---

# 💬 Slash Commands - Syntaxe

## Structure d'une Commande

<div class="columns">

### 📝 Front Matter (YAML)
```yaml
---
description: "Command description"
arguments:
  - name: target
    description: "Argument desc"
    required: false
flags:
  - name: verbose
    description: "Verbose output"
---
```

### 📖 Prompt Body (Markdown)
```markdown
# Instructions pour Claude

1. Étape 1
2. Étape 2
3. Étape 3

## Context
Variables: {{argument}}

## Output Format
Format attendu
```

</div>

---

# 🤖 Agents Spécialisés

## Délégation via Task Tool

### Fichier : `agents/frontend.md`

```markdown
---
description: Frontend development specialist
subagent_type: frontend-specialist
---

You are a frontend development specialist with expertise in:
- Modern UI frameworks (React, Vue, Angular)
- Accessibility (WCAG 2.1 AA)
- Performance optimization
- Design systems integration

## Capabilities

- Component creation with best practices
- Responsive design implementation
- Cross-browser compatibility
- Performance budgets enforcement

## MCP Servers

Primary: Magic (UI generation)
Secondary: Context7 (framework patterns)
```

---

# 🤖 Types d'Agents Disponibles

## Subagent Types Claude Code

<div class="columns">

### 🎯 Agents Disponibles
- **general-purpose**
  Multi-domain, recherche complexe

- **frontend-specialist**
  UI/UX, React, Vue, accessibility

- **backend-specialist**
  APIs, databases, architecture serveur

- **qa-specialist**
  Testing, quality assurance, validation

- **devops-specialist**
  CI/CD, infrastructure, déploiement

- **coordinator**
  Orchestration multi-agents

### 💡 Quand Utiliser
- Tasks nécessitant expertise spécifique
- Délégation parallèle (gain temps)
- Coordination workflows complexes
- Spécialisation domaine technique

</div>

---

# 🏪 Système Marketplace

## Comment ça Fonctionne ?

### 📦 Distribution via GitHub

```
1. 📝 Développer Plugin
   └── Structure + commandes + documentation

2. 🔖 Tag Version
   └── git tag v1.0.0 && git push --tags

3. 🚀 Release GitHub
   └── gh release create v1.0.0

4. 📢 Publier Marketplace
   └── Repository public GitHub accessible

5. 👥 Utilisateurs Installent
   └── /plugin marketplace add <url>
   └── /plugin install <name>
```

---

# 🏪 Types de Distribution

<div class="columns">

### 📦 Plugin Standalone
```bash
# Repository unique
github.com/user/mon-plugin

# Installation directe
/plugin install \
  github.com/user/mon-plugin
```

### 🏬 Marketplace Multi-Plugins
```bash
# Repository marketplace
github.com/org/marketplace

# Ajout marketplace
/plugin marketplace add \
  github.com/org/marketplace

# Installation plugin
/plugin install plugin-name
```

</div>

---

# 🔧 Commandes Plugin Manager

## Gestion des Plugins

```bash
# 🏬 MARKETPLACE
/plugin marketplace list                    # Lister marketplaces
/plugin marketplace add <url>               # Ajouter marketplace
/plugin marketplace update <name>           # Update marketplace
/plugin marketplace remove <name>           # Supprimer marketplace

# 🔌 PLUGINS
/plugin list                                # Lister plugins installés
/plugin install <name>                      # Installer plugin
/plugin update <name>                       # Mettre à jour plugin
/plugin uninstall <name>                    # Désinstaller plugin
/plugin info <name>                         # Info détaillées plugin

# 🔍 RECHERCHE
/plugin search <query>                      # Rechercher plugins
/plugin show <name>                         # Afficher détails
```

---

# 🎓 Tutoriel : Créer Votre Plugin

## Étape 1 : Initialiser Structure

```bash
# Créer structure de base
mkdir mon-plugin && cd mon-plugin
mkdir -p .claude-plugin commands agents .claude

# Créer plugin.json
cat > .claude-plugin/plugin.json <<EOF
{
  "name": "mon-plugin",
  "version": "1.0.0",
  "description": "Mon premier plugin Claude Code",
  "author": {
    "name": "Mon Nom",
    "email": "mon@email.com"
  },
  "homepage": "https://github.com/moi/mon-plugin",
  "repository": "https://github.com/moi/mon-plugin",
  "license": "MIT",
  "keywords": ["development", "automation"]
}
EOF
```

---

# 🎓 Tutoriel : Créer Votre Plugin

## Étape 2 : Créer Première Commande

```bash
# Créer commande /mon-plugin:hello
cat > commands/hello.md <<'EOF'
---
description: Say hello with custom message
arguments:
  - name: name
    description: Name to greet
    required: false
---

Generate a friendly greeting message.

## Instructions

1. Greet the user: {{name || "World"}}
2. Add a fun fact about Claude Code plugins
3. Suggest trying other commands in this plugin

Be enthusiastic and helpful!
EOF
```

---

# 🎓 Tutoriel : Créer Votre Plugin

## Étape 3 : Documentation

```bash
# Créer README.md
cat > README.md <<'EOF'
# Mon Plugin

Description de votre plugin.

## Installation

\`\`\`bash
/plugin install github.com/moi/mon-plugin
\`\`\`

## Commandes

- \`/mon-plugin:hello [name]\` - Say hello

## Exemples

\`\`\`bash
/mon-plugin:hello Claude
\`\`\`

## License

MIT
EOF
```

---

# 🎓 Tutoriel : Créer Votre Plugin

## Étape 4 : Git & GitHub

```bash
# Initialiser git
git init
git add .
git commit -m "Initial commit: Mon Plugin v1.0.0"

# Créer repository GitHub
gh repo create mon-plugin --public --source=. --push

# Créer tag et release
git tag v1.0.0
git push origin v1.0.0
gh release create v1.0.0 \
  --title "Mon Plugin v1.0.0" \
  --notes "Première version !"
```

---

# 🎓 Tutoriel : Créer Votre Plugin

## Étape 5 : Tester l'Installation

```bash
# Dans Claude Code

# Installer directement depuis GitHub
/plugin install github.com/votre-compte/mon-plugin

# Vérifier installation
/plugin list

# Tester la commande
/mon-plugin:hello Claude

# Si modifications, mettre à jour
/plugin update mon-plugin
```

---

# 📦 Exemple Réel : WD Framework

## Cas d'Usage Complet

### 🎯 Objectif
Framework intelligent pour développement web avec :
- 22 commandes spécialisées
- 11 AI personas avec auto-activation
- 5 agents experts
- Système d'orchestration complet

### 📊 Résultats
- **2,742 lignes** d'orchestration
- **+40-70%** gain de temps
- **+30-50%** meilleurs résultats
- **Community adoption** - CC France

---

# 📦 WD Framework : Structure

## Architecture Complète

```
wd-framework/
├── .claude-plugin/
│   ├── plugin.json                    # v2.0.1
│   └── marketplace.json               # wd-marketplace
│
├── commands/                          # 22 commandes
│   ├── analyze.md, build.md, implement.md
│   ├── improve.md, test.md, document.md
│   └── ... (16 autres)
│
├── agents/                            # 5 agents
│   ├── frontend.md, backend.md
│   ├── security.md, test.md, docs.md
│
├── .claude/                           # Orchestration (10 fichiers)
│   ├── CLAUDE.md, COMMANDS.md, ORCHESTRATOR.md
│   ├── PERSONAS.md, AGENTS.md, FLAGS.md
│   └── MCP.md, MODES.md, PRINCIPLES.md, RULES.md
│
└── README.md, CHANGELOG.md, ORCHESTRATION.md
```

---

# 📦 WD Framework : plugin.json

```json
{
  "name": "wd",
  "version": "2.0.1",
  "description": "Intelligent web development framework with 22 specialized commands, 5 expert agents, 11 AI personas, and complete orchestration system",
  "author": {
    "name": "Para CC-France",
    "email": "contact@cc-france.org",
    "url": "https://github.com/Para-FR"
  },
  "homepage": "https://github.com/Para-FR/wd-framework",
  "repository": "https://github.com/Para-FR/wd-framework",
  "license": "MIT",
  "keywords": [
    "webdev", "web-development", "react", "nextjs",
    "vue", "typescript", "frontend", "backend",
    "fullstack", "claude-code"
  ]
}
```

---

# 📦 WD Framework : Commande Exemple

### `commands/implement.md` (Simplifié)

```markdown
---
description: Feature and code implementation with intelligent persona activation
arguments:
  - name: feature-description
    description: Description of feature to implement
    required: true
flags:
  - name: type
    description: Implementation type (component|api|service|feature)
  - name: framework
    description: Target framework (react|vue|angular|nextjs)
---

You are implementing a new feature with intelligent routing.

## Auto-Activation

Based on context, activate appropriate:
- **Persona**: Frontend, Backend, or Architect
- **MCP Servers**: Context7 (patterns), Magic (UI), Sequential (logic)
- **Agents**: Use Task tool for specialized delegation

## Instructions

1. Analyze requirements and complexity
2. Select optimal tools and approach
3. Implement with best practices
4. Validate with quality gates
```

---

# 📦 WD Framework : Agent Exemple

### `agents/frontend.md` (Simplifié)

```markdown
---
description: Frontend development specialist with Magic MCP integration
subagent_type: frontend-specialist
---

You are a frontend development specialist.

## Expertise
- Modern UI frameworks (React, Vue, Angular)
- Accessibility (WCAG 2.1 AA compliance)
- Performance optimization (Core Web Vitals)
- Design system integration

## MCP Servers
- **Primary**: Magic - UI component generation
- **Secondary**: Context7 - Framework patterns
- **Tertiary**: Playwright - User interaction testing

## Auto-Activation Triggers
- Keywords: component, UI, React, Vue, responsive, accessibility
- File patterns: *.jsx, *.tsx, *.vue, *.css, *.scss
- Commands: /wd:build, /wd:design, /wd:implement (frontend context)

## Quality Standards
- WCAG 2.1 AA minimum compliance
- <3s load time on 3G networks
- <500KB initial bundle size
```

---

# 📦 WD Framework : Installation

## Pour les Utilisateurs

```bash
# Méthode 1 : Via Marketplace (Recommandé)
/plugin marketplace add https://github.com/Para-FR/wd-framework
/plugin install wd

# Méthode 2 : Installation Directe
/plugin install https://github.com/Para-FR/wd-framework

# Vérifier installation
/plugin list
# → wd v2.0.1 ✅

# Tester une commande
/wd:analyze @src/

# Mettre à jour
/plugin marketplace update wd-marketplace
/plugin update wd
```

---

# 📦 WD Framework : Utilisation

## Exemples Concrets

```bash
# Analyse de codebase
/wd:analyze @src/ --focus security

# Implémentation composant
/wd:implement LoginForm --type component --framework react

# Build projet
/wd:build --optimize

# Review code
/wd:review @src/auth/ --comprehensive

# Tests performance
/wd:benchmark --metrics all

# Finalisation
/wd:finalize "Add authentication system"
```

---

# 📦 WD Framework : Métriques

## Impact Réel

<div class="columns">

### ⚡ Performance
- **+30-50%** meilleurs résultats (wave)
- **+40-70%** gain de temps (agents)
- **3-5x** plus rapide (MCP)
- **-30-50%** tokens (compression)

### 📊 Adoption
- **2,742 lignes** documentation
- **22 commandes** spécialisées
- **11 personas** auto-activées
- **5 agents** experts
- **4 MCP** intégrés
- **Community** CC France

</div>

---

# 🎯 Best Practices

## Créer un Plugin de Qualité

### 📋 Structure
- ✅ **Nommage clair** - Descriptif et mémorable
- ✅ **Versioning semantic** - Suivre semver.org
- ✅ **Documentation complète** - README + exemples
- ✅ **Metadata riches** - keywords, description, author

### 💬 Commandes
- ✅ **Noms explicites** - Action + contexte
- ✅ **Arguments optionnels** - Defaults intelligents
- ✅ **Validation inputs** - Gestion erreurs
- ✅ **Output structuré** - Format cohérent

---

# 🎯 Best Practices (suite)

## Qualité et Maintenance

### 🧪 Testing
- ✅ **Tester manuellement** - Avant publication
- ✅ **Cas limites** - Edge cases et erreurs
- ✅ **Documentation exemples** - Testés et fonctionnels

### 🔄 Maintenance
- ✅ **CHANGELOG** - Historique versions clair
- ✅ **Issues GitHub** - Support utilisateurs
- ✅ **Releases régulières** - Corrections et features
- ✅ **Breaking changes** - Communiquer clairement

---

# 🎯 Best Practices (fin)

## Communauté et Distribution

### 🌐 Open Source
- ✅ **License claire** - MIT recommandé
- ✅ **Contributing guide** - Accueillir contributions
- ✅ **Code of conduct** - Environnement sain

### 📢 Promotion
- ✅ **README attrayant** - Badges, screenshots
- ✅ **Exemples concrets** - Use cases réels
- ✅ **Marketplace listing** - Catégories appropriées
- ✅ **Community feedback** - Amélioration continue

---

# ⚠️ Pièges à Éviter

<div class="columns">

### ❌ Erreurs Communes

**Structure**
- Paths relatifs dans plugin.json
- Commandes sans description
- Versioning incohérent

**Commandes**
- Prompts trop complexes
- Manque de validation
- Output non structuré

**Documentation**
- README incomplet
- Pas d'exemples
- Installation non testée

### ✅ Solutions

**Structure**
- Paths absolus ou relatifs à root
- Descriptions claires partout
- Suivre semver strictement

**Commandes**
- Prompts concis et clairs
- Valider tous les inputs
- Format cohérent outputs

**Documentation**
- README complet avec exemples
- Use cases documentés
- Tester installation fraîche

</div>

---

# 🔍 Debugging Plugins

## Résolution Problèmes Courants

```bash
# Plugin non trouvé après installation
/plugin list                    # Vérifier présence
ls ~/.claude/plugins/           # Check filesystem

# Commande non reconnue
/plugin info mon-plugin         # Vérifier metadata
cat ~/.claude/plugins/mon-plugin/.claude-plugin/plugin.json

# Mise à jour qui ne fonctionne pas
/plugin marketplace update mon-marketplace
/plugin update mon-plugin
# Redémarrer Claude Code

# Voir logs Claude Code
# → Ouvrir DevTools (si interface web)
# → Check console pour erreurs

# Réinstallation propre
/plugin uninstall mon-plugin
/plugin install mon-plugin
```

---

# 🚀 Roadmap Système Plugins

## Évolutions Futures

### 🎯 Court Terme
- **Plugin templates** - Générateurs scaffolding
- **Testing framework** - Automatisation tests plugins
- **Plugin registry** - Catalogue central officiel
- **Metrics dashboard** - Analytics usage plugins

### 🔮 Moyen Terme
- **Dependency management** - Plugins dépendant d'autres
- **Plugin hooks** - Système événements
- **Versioning avancé** - Compatibility matrix
- **Marketplace UI** - Interface graphique découverte

### 🌟 Long Terme
- **Plugin SDK** - Outils développement avancés
- **Ecosystem marketplace** - Multiple registries
- **Plugin monetization** - Modèles économiques
- **Enterprise features** - Private registries

---

# 💡 Idées de Plugins

## Inspirations pour CC France

### 🛠️ Développement
- **Framework-specific** - Django, FastAPI, NestJS workflows
- **Testing** - Pytest, Jest, Cypress automation
- **Database** - PostgreSQL, MongoDB, Redis helpers

### 🏢 Entreprise
- **Agile tools** - Jira, Linear, GitHub Projects integration
- **Code review** - Automated PR reviews
- **Documentation** - API docs, Swagger, OpenAPI generation

### 🎓 Éducation & Community
- **Learning paths** - Tutoriels interactifs
- **Code challenges** - LeetCode, HackerRank integration
- **Templates** - Project starters (MERN, JAMstack, etc.)

---

# 📚 Ressources

## Documentation Officielle

### 🔗 Claude Code
- **Docs** : [docs.claude.com/claude-code](https://docs.claude.com/claude-code)
- **GitHub** : [github.com/anthropics/claude-code](https://github.com/anthropics/claude-code)
- **Community** : Discord Claude

### 📖 Exemples
- **WD Framework** : [github.com/Para-FR/wd-framework](https://github.com/Para-FR/wd-framework)
- **Plugin Template** : À venir
- **Best Practices** : Guide communautaire

### 🎓 Tutoriels
- **Création plugin** : Documentation officielle
- **Marketplace setup** : GitHub guides
- **Advanced features** : MCP integration, agents

---

# 💡 Démo Live

## Créons un Plugin Ensemble !

### 🎯 Objectif
Créer un plugin simple "python-helper" avec :
- Commande `/python:lint` - Linting Python files
- Commande `/python:test` - Run pytest with coverage
- Agent Python spécialisé

### 📝 Étapes
1. Structure de base
2. Créer les 2 commandes
3. Créer l'agent
4. Publier sur GitHub
5. Installer et tester

**Allons-y ! 🚀**

---

# 🎯 Récapitulatif

## Points Clés

1. **🔌 Plugins** = Extensions Claude Code réutilisables
2. **🏪 Marketplace** = Distribution GitHub-based
3. **📁 Structure** = .claude-plugin/ + commands/ + agents/
4. **💬 Commandes** = Markdown avec front matter YAML
5. **🤖 Agents** = Task tool avec subagent_type
6. **📦 Distribution** = Git tags + GitHub releases
7. **🔧 Installation** = /plugin install <url|name>
8. **✅ Best Practices** = Documentation, testing, versioning
9. **📊 Exemple** = WD Framework (22 commands, 5 agents)
10. **🚀 Future** = Plugin SDK, registry central, ecosystem

---

# 🌟 Votre Tour !

## Challenge pour CC France

### 🎯 Créez Votre Premier Plugin

**Mission** : D'ici 2 semaines
1. Identifier un besoin récurrent dans vos workflows
2. Créer un plugin avec 2-3 commandes
3. Le publier sur GitHub
4. Le partager avec CC France

**Support** :
- Documentation : docs.claude.com
- Exemple : WD Framework
- Community : Discord CC France

**Prix** :
- 🥇 Meilleur plugin voté par la communauté
- 🎖️ Reconnaissance officielle
- 🚀 Promotion dans la newsletter

---

<!-- _class: lead -->

# 🙏 Merci !

## Questions & Discussion

**Créez, Partagez, Innovez**
*avec Claude Code Plugins & Marketplace*

---

**🔗 Ressources**
- WD Framework : [github.com/Para-FR/wd-framework](https://github.com/Para-FR/wd-framework)
- Documentation : [docs.claude.com/claude-code](https://docs.claude.com/claude-code)
- Community : Discord CC France

---

**📧 Contact**
- Para CC-France
- contact@cc-france.org

---

*Présentation créée avec ❤️ pour Claude Code France*
*Octobre 2025 - Let's build the ecosystem together! 🚀*
