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

# 🚀 WD Framework v2.0

**Intelligent Web Development Framework**
*avec 22 commandes, 11 AI personas et 5 agents spécialisés*

---
*Présentation Claude Code France - Octobre 2025*
*Para CC-France*

---

# 📊 Vue d'ensemble

## Qu'est-ce que WD Framework ?

Un **framework d'intelligence artificielle** pour Claude Code qui transforme le développement web en workflow automatisé et intelligent.

<div class="columns">

### 🎯 Composants Clés
- **22 commandes spécialisées**
- **11 AI Personas** avec auto-activation
- **5 agents experts** (Task tool)
- **4 serveurs MCP** intégrés
- **Système d'orchestration complet**

### ⚡ Avantages
- **30-50%** meilleurs résultats
- **40-70%** gain de temps
- **3-5x** plus rapide avec MCP
- **30-50%** réduction tokens

</div>

---

# 🎨 Architecture du Framework

```
WD Framework v2.0.1
├── 📋 22 Commandes Spécialisées
│   ├── Development (4) - build, implement, design, migrate
│   ├── Planning (4) - brainstorm, workflow, estimate, task
│   ├── Analysis (4) - analyze, review, troubleshoot, explain
│   ├── Quality (2) - improve, cleanup
│   └── Testing, Documentation, Workflow, Git, ERP, Meta...
│
├── 🤖 11 AI Personas (auto-activation)
│   ├── Technical Specialists (5) - architect, frontend, backend, security, performance
│   ├── Process & Quality (4) - analyzer, qa, refactorer, devops
│   └── Knowledge (2) - mentor, scribe
│
├── 🔧 5 Agents Spécialisés (Task tool)
│   ├── wd-frontend-agent - UI/UX + Magic MCP
│   ├── wd-backend-agent - APIs + Context7
│   ├── wd-security-agent - Vulnérabilités + Sequential
│   ├── wd-test-agent - E2E + Playwright
│   └── wd-docs-agent - Documentation + Context7
│
└── 🌐 4 Serveurs MCP
    ├── Context7 - Documentation officielle
    ├── Sequential - Analyse complexe
    ├── Magic - Génération UI
    └── Playwright - Tests E2E cross-browser
```

---

# 📋 Les 22 Commandes

<div class="columns">

### 🛠️ Development (4)
- `/wd:build` - Build avec détection framework
- `/wd:implement` - Implémentation features
- `/wd:design` - Architecture & design
- `/wd:migrate` - Migration frameworks

### 📊 Planning (4)
- `/wd:brainstorm` - Génération idées
- `/wd:workflow` - Workflows structurés
- `/wd:estimate` - Estimations basées données
- `/wd:task` - Gestion projets long-terme

### 🔍 Analysis (4)
- `/wd:analyze` - Analyse multi-dimensionnelle
- `/wd:review` - Code review complet
- `/wd:troubleshoot` - Résolution problèmes
- `/wd:explain` - Explications détaillées

</div>

---

# 📋 Les 22 Commandes (suite)

<div class="columns">

### ✨ Quality (2)
- `/wd:improve` - Améliorations basées preuves
- `/wd:cleanup` - Nettoyage dette technique

### 🧪 Testing (2)
- `/wd:test` - Stratégie test complète
- `/wd:benchmark` - Tests performance

### 📚 Documentation (1)
- `/wd:document` - Génération docs

### 🚀 Workflow (1)
- `/wd:finalize` - Finalisation + git

</div>

---

# 📋 Les 22 Commandes (fin)

<div class="columns">

### 🔄 Version Control (1)
- `/wd:git` - Assistant git workflows

### 🏢 ERP (1)
- `/orvi-agent` - Gestion bugs Orvi ERP

### 🎯 Meta (3)
- `/wd:index` - Catalogue commandes
- `/wd:load` - Chargement contexte
- `/wd:spawn` - Orchestration tâches

</div>

**Total : 22 commandes** pour couvrir tous les aspects du développement web moderne

---

# 🤖 Les 11 AI Personas

## Spécialistes Techniques (5)

<div class="columns">

### 🏗️ `--persona-architect`
- **Focus** : Architecture long-terme
- **Priorité** : Maintenabilité > Scalabilité
- **MCP** : Sequential (primaire)
- **Commandes** : analyze, estimate, design

### 🎨 `--persona-frontend`
- **Focus** : UX & Accessibilité
- **Priorité** : User needs > A11y > Perf
- **MCP** : Magic (primaire)
- **Budgets** : <3s load, WCAG 2.1 AA

### ⚙️ `--persona-backend`
- **Focus** : Fiabilité & Data integrity
- **Priorité** : Reliability > Security > Perf
- **MCP** : Context7 (primaire)
- **SLA** : 99.9% uptime

</div>

---

# 🤖 Les 11 AI Personas (suite)

<div class="columns">

### 🛡️ `--persona-security`
- **Focus** : Threat modeling
- **Priorité** : Security > Compliance
- **MCP** : Sequential (analysis)
- **Framework** : Zero Trust, Defense in Depth

### ⚡ `--persona-performance`
- **Focus** : Optimisation metrics-driven
- **Priorité** : Measure first > Critical path
- **MCP** : Playwright (metrics)
- **Budgets** : <3s 3G, <500ms API

</div>

---

# 🤖 Les 11 AI Personas (Process & Quality)

<div class="columns">

### 🔍 `--persona-analyzer`
- **Focus** : Root cause analysis
- **Priorité** : Evidence > Systematic
- **MCP** : Sequential (investigation)

### ✅ `--persona-qa`
- **Focus** : Quality assurance
- **Priorité** : Prevention > Detection
- **MCP** : Playwright (testing)

### 🧹 `--persona-refactorer`
- **Focus** : Code quality
- **Priorité** : Simplicity > Maintainability
- **MCP** : Sequential (analysis)

### 🚀 `--persona-devops`
- **Focus** : Infrastructure automation
- **Priorité** : Automation > Observability
- **MCP** : Sequential (planning)

</div>

---

# 🤖 Les 11 AI Personas (Knowledge)

<div class="columns">

### 📚 `--persona-mentor`
- **Focus** : Transfert de connaissance
- **Priorité** : Understanding > Teaching
- **MCP** : Context7 (resources)
- **Style** : Scaffolding progressif

### ✍️ `--persona-scribe=lang`
- **Focus** : Documentation professionnelle
- **Priorité** : Clarity > Audience needs
- **MCP** : Context7 (patterns)
- **Langues** : en, fr, es, de, ja, zh, pt, it, ru, ko

</div>

**Auto-activation basée sur** : Keywords (30%), Context (40%), User history (20%), Performance (10%)

---

# 🔧 Les 5 Agents Spécialisés

## Délégation via Task Tool de Claude Code

<div class="columns">

### 🎨 `wd-frontend-agent`
**Subagent** : frontend-specialist
- UI/UX moderne + React/Vue
- Accessibilité WCAG 2.1 AA
- Design systems
- **MCP** : Magic → Context7 → Playwright

### ⚙️ `wd-backend-agent`
**Subagent** : backend-specialist
- APIs RESTful/GraphQL
- Database optimization
- Auth/Authorization
- **MCP** : Context7 → Sequential → Playwright

### 🛡️ `wd-security-agent`
**Subagent** : qa-specialist (security)
- Vulnerability assessment
- Threat modeling
- Compliance (OWASP, SOC2)
- **MCP** : Sequential → Context7 → Playwright

</div>

---

# 🔧 Les 5 Agents Spécialisés (suite)

<div class="columns">

### 🧪 `wd-test-agent`
**Subagent** : qa-specialist
- E2E testing cross-browser
- Performance benchmarking
- Coverage analysis
- **MCP** : Playwright → Sequential → Context7

### 📚 `wd-docs-agent`
**Subagent** : general-purpose (docs)
- Documentation technique
- API docs generation
- Multi-langue
- **MCP** : Context7 → Sequential → Magic

</div>

---

# 🎯 Patterns de Coordination Multi-Agents

## 3 Stratégies d'Orchestration

### 🔀 **Parallel** - Analyse indépendante
```
/wd:review --comprehensive
→ [security-agent | performance-agent | quality-agent]
→ Agrégation résultats unifiée
```

### ➡️ **Sequential** - Pipeline dépendant
```
/wd:implement → /wd:test → /wd:document
→ backend-agent → test-agent → docs-agent
→ Préservation contexte entre agents
```

### 🌳 **Hierarchical** - Projets complexes
```
/wd:migrate React → Vue
→ coordinator (central)
  ├─ frontend-agent
  ├─ test-agent
  └─ docs-agent
```

---

# 🌐 Intégration MCP Servers

<div class="columns">

### 📖 Context7
**Documentation officielle**
- Lookup bibliothèques
- Patterns frameworks
- Standards localisation
- **Cache** : 2-5K tokens/query

### 🧠 Sequential
**Analyse complexe**
- Multi-step reasoning
- Architecture review
- Debugging systématique
- **Budgets** : 4K → 32K tokens

</div>

---

# 🌐 Intégration MCP Servers (suite)

<div class="columns">

### ✨ Magic
**Génération UI**
- Composants modernes
- Design systems (21st.dev)
- WCAG compliance
- **Frameworks** : React, Vue, Angular

### 🎭 Playwright
**Tests E2E cross-browser**
- Chrome, Firefox, Safari, Edge
- Visual regression
- Performance metrics
- **Parallel** : Multi-browser simultané

</div>

---

# 🧠 Système d'Orchestration Intelligent

## 10 Fichiers de Configuration (.claude/)

<div class="columns">

### 📚 Core Files
1. **CLAUDE.md** - Entry point
2. **COMMANDS.md** - Référence 22 commandes (NEW v2.0.1)
3. **ORCHESTRATOR.md** - Routing intelligent (605 lignes)
4. **PERSONAS.md** - 11 personas (467 lignes)
5. **AGENTS.md** - 5 agents (281 lignes)

### ⚙️ Configuration
6. **FLAGS.md** - Système flags (285 lignes)
7. **MCP.md** - Intégration serveurs (278 lignes)
8. **MODES.md** - Modes opérationnels (309 lignes)
9. **PRINCIPLES.md** - Principes dev (160 lignes)
10. **RULES.md** - Règles opérationnelles (65 lignes)

</div>

**Total : 2,742 lignes** de documentation orchestration

---

# 🎯 Master Routing Table

## Auto-Activation Intelligente

| Pattern | Complexity | Auto-Activates | Confidence |
|---------|------------|----------------|------------|
| "analyze architecture" | complex | architect + --ultrathink + Sequential | 95% |
| "create component" | simple | frontend + Magic + --uc | 90% |
| "implement API" | moderate | backend + --seq + Context7 | 92% |
| "implement UI" | simple | frontend + Magic + --c7 | 94% |
| "security audit" | complex | security + --ultrathink + Sequential | 95% |
| "optimize performance" | complex | performance + --think-hard + Playwright | 90% |
| "write documentation" | moderate | scribe + Context7 | 95% |
| "improve iteratively" | moderate | refactorer + --seq + loop | 90% |

**Scoring** : Pattern match (40%), Historical success (30%), Context (20%), Resources (10%)

---

# 🚀 Wave Orchestration

## Exécution Multi-Stage pour Opérations Complexes

### 🌊 Qu'est-ce que Wave Mode ?
Exécution en plusieurs vagues avec intelligence composée et amélioration progressive

### ⚡ Auto-Activation
```yaml
conditions:
  - complexity >= 0.7
  - files > 20
  - operation_types > 2

strategies:
  - progressive: Amélioration incrémentale
  - systematic: Analyse méthodique
  - adaptive: Configuration dynamique
  - enterprise: Orchestration >100 fichiers
```

### 📊 Résultats
- **30-50%** meilleurs résultats vs. exécution simple
- Validation progressive à chaque vague
- Rollback capability intégrée

---

# 📊 Métriques de Performance

<div class="columns">

### ⚡ Vitesse
- **Wave orchestration** : +30-50% qualité
- **Agent delegation** : -40-70% temps
- **MCP coordination** : 3-5x plus rapide
- **Token efficiency** : -30-50% avec --uc

### ✅ Qualité
- **8-step validation cycle**
- **≥80%** couverture unit tests
- **≥70%** couverture integration
- **WCAG 2.1 AA** minimum
- **99.9%** uptime backend

</div>

---

# 📊 Métriques de Performance (suite)

<div class="columns">

### 🎯 Auto-Activation
- **Personas** : 70-95% confidence
- **Agents** : 75-90% auto-delegate
- **MCP servers** : Context-aware
- **Wave mode** : Complexity-based

### 📈 Resource Management
- **Green** (0-60%) : Full operations
- **Yellow** (60-75%) : Optimization
- **Orange** (75-85%) : Warnings
- **Red** (85-95%) : Efficiency modes
- **Critical** (95%+) : Emergency protocols

</div>

---

# 💡 Exemples d'Utilisation

## Cas d'Usage Réels

### 🎨 Développement Frontend
```bash
/wd:implement LoginComponent --agent wd-frontend-agent --magic
```
→ Auto-activates: frontend persona + Magic MCP
→ Génère composant React avec accessibilité WCAG 2.1 AA
→ Tests Playwright automatiques

### ⚙️ API Backend
```bash
/wd:implement UserAuthAPI --agent wd-backend-agent --validate
```
→ Auto-activates: backend + security personas + Context7
→ RESTful API avec JWT authentication
→ Tests sécurité + validation données

---

# 💡 Exemples d'Utilisation (suite)

### 🔍 Code Review Complet
```bash
/wd:review --comprehensive --agents security,performance,quality
```
→ Multi-agent parallel execution
→ 3 rapports spécialisés agrégés
→ Recommandations prioritaires

### 🚀 Migration Framework
```bash
/wd:migrate React Vue --strategy comprehensive --agents all
```
→ Coordination hiérarchique
→ Frontend + Test + Docs agents
→ Validation progressive

---

# 💡 Exemples d'Utilisation (fin)

### 🧪 Performance Benchmark
```bash
/wd:benchmark --metrics all --export report.json
```
→ Core Web Vitals + Accessibility + SEO
→ Playwright multi-browser
→ Rapport visuel exporté

### ✅ Finalisation Projet
```bash
/wd:finalize "Add user authentication system"
```
→ Update docs + lint + type + build
→ Git commit message généré
→ Push automatique si gates pass

---

# 🎯 Modes Opérationnels

<div class="columns">

### 📋 Task Management
- TodoRead/TodoWrite (session)
- /task (multi-session)
- /spawn (meta-orchestration)
- /loop (itératif)
- **States** : pending, in_progress, completed, blocked

### 🧠 Introspection
- Reasoning analysis
- Action sequence review
- Meta-cognitive assessment
- Framework compliance check
- **Activation** : --introspect flag

### ⚡ Token Efficiency
- Symbol system optimisé
- Abbreviations contextuelles
- Compression adaptative (5 niveaux)
- **Activation** : --uc flag
- **Gain** : 30-50% tokens

</div>

---

# 🏗️ Quality Gates

## 8-Step Validation Cycle

1. **Syntax** - Language parsers + Context7 validation
2. **Type** - Sequential analysis + type compatibility
3. **Lint** - Context7 rules + quality analysis
4. **Security** - Sequential + OWASP compliance
5. **Test** - Playwright E2E + ≥80% unit / ≥70% integration
6. **Performance** - Sequential benchmarking + optimization
7. **Documentation** - Context7 patterns + completeness
8. **Integration** - Playwright + deployment validation

**Automation** : CI/CD integration + intelligent monitoring + evidence generation

---

# 📦 Installation & Mise à Jour

## Installation Initiale

```bash
# 1. Ajouter le marketplace
/plugin marketplace add https://github.com/Para-FR/wd-framework

# 2. Installer le plugin
/plugin install wd

# 3. Redémarrer Claude Code
```

## Mise à Jour (v2.0.1)

```bash
# 1. Update marketplace
/plugin marketplace update wd-marketplace

# 2. Update plugin
/plugin update wd

# 3. Redémarrer Claude Code
```

---

# 🔧 Configuration Avancée

## Flags Disponibles

<div class="columns">

### 🧠 Thinking
- `--think` (4K tokens)
- `--think-hard` (10K)
- `--ultrathink` (32K)

### 🌐 MCP
- `--c7` / `--context7`
- `--seq` / `--sequential`
- `--magic`
- `--play` / `--playwright`
- `--all-mcp` / `--no-mcp`

### 🤖 Personas
- `--persona-architect`
- `--persona-frontend`
- `--persona-backend`
- `--persona-security`
- `--persona-performance`
- etc. (11 disponibles)

</div>

---

# 🔧 Configuration Avancée (suite)

<div class="columns">

### 🔀 Agents
- `--agent wd-frontend-agent`
- `--agents frontend,backend,test`
- `--multi-agent parallel|sequential|hierarchical`
- `--delegate files|folders|auto`

### 🌊 Wave
- `--wave-mode auto|force|off`
- `--wave-strategy progressive|systematic|adaptive|enterprise`
- `--wave-delegation files|folders|tasks`

### ⚙️ Optimization
- `--uc` / `--ultracompressed`
- `--validate`
- `--safe-mode`
- `--loop`
- `--iterations [n]`

</div>

---

# 📚 Documentation Complète

## Ressources Disponibles

### 📖 Documentation Principale
- **README.md** - Vue d'ensemble + Getting Started
- **ORCHESTRATION.md** - Guide complet orchestration
- **CHANGELOG.md** - Historique versions

### 🔍 Référence Technique
- **CLAUDE.md** - Entry point framework
- **COMMANDS.md** - Référence 22 commandes
- **PERSONAS.md** - 11 AI personas détaillées
- **AGENTS.md** - 5 agents spécialisés
- **FLAGS.md** - Système flags complet

### ⚙️ Configuration
- **MCP.md** - Intégration serveurs
- **ORCHESTRATOR.md** - Routing intelligent
- **MODES.md** - Modes opérationnels

---

# 🎓 Ressources & Liens

<div class="columns">

### 🔗 Liens Officiels
- **Repository** : [github.com/Para-FR/wd-framework](https://github.com/Para-FR/wd-framework)
- **Latest Release** : [v2.0.1](https://github.com/Para-FR/wd-framework/releases/tag/v2.0.1)
- **Changelog** : [CHANGELOG.md](https://github.com/Para-FR/wd-framework/blob/master/CHANGELOG.md)
- **Marketplace** : wd-marketplace plugin

### 📞 Support
- **Issues** : GitHub Issues
- **Community** : Claude Code France
- **Author** : Para CC-France
- **License** : MIT

</div>

---

# 🚀 Roadmap & Future

## Prochaines Évolutions

### 🎯 Court Terme (v2.1)
- Amélioration coordination multi-agents
- Nouveaux patterns wave orchestration
- Cache MCP optimisé
- Métriques performance détaillées

### 🔮 Moyen Terme (v2.x)
- Intégration nouveaux MCP servers
- Personas additionnels (AI-ML, Mobile)
- Agents spécialisés supplémentaires
- Templates projets pré-configurés

### 🌟 Long Terme (v3.0)
- Machine learning pour auto-optimization
- Collaboration temps-réel multi-agents
- Plugins ecosystem extensible
- Integration CI/CD natives

---

# 🎯 Points Clés à Retenir

## Le WD Framework c'est :

1. **🤖 Intelligence Collective** : 11 personas + 5 agents + 4 MCP servers
2. **📋 22 Commandes Spécialisées** : Couvrant tout le cycle dev
3. **⚡ Performance** : 30-50% meilleurs résultats, 40-70% gain temps
4. **🧠 Auto-Activation** : Routing intelligent basé contexte
5. **🌊 Wave Orchestration** : Multi-stage pour opérations complexes
6. **✅ Quality Gates** : 8-step validation cycle
7. **📚 Documentation Complète** : 2,742 lignes d'orchestration
8. **🔧 Hautement Configurable** : Flags, modes, stratégies
9. **🎯 Production-Ready** : Testé, validé, optimisé
10. **🆓 Open Source** : MIT License, community-driven

---

# 💡 Démo Live

## Essayons Ensemble !

### 🎨 Scénario 1 : Création Composant Frontend
```bash
/wd:implement DashboardCard --agent wd-frontend-agent
```

### ⚙️ Scénario 2 : API Backend Sécurisée
```bash
/wd:implement UserAuthAPI --validate --think
```

### 🔍 Scénario 3 : Code Review Complet
```bash
/wd:review --comprehensive --agents security,performance,quality
```

### 🚀 Scénario 4 : Finalisation Projet
```bash
/wd:finalize "Implement authentication system"
```

---

<!-- _class: lead -->

# 🙏 Merci !

## Questions & Discussion

**WD Framework v2.0.1**
*Intelligent Web Development Framework*

---

**🔗 Ressources**
- Repository : [github.com/Para-FR/wd-framework](https://github.com/Para-FR/wd-framework)
- Latest Release : [v2.0.1](https://github.com/Para-FR/wd-framework/releases/tag/v2.0.1)
- Marketplace : wd-marketplace plugin

---

**📧 Contact**
- Para CC-France
- contact@cc-france.org

---

*Présentation créée avec ❤️ pour Claude Code France*
*Octobre 2025*
