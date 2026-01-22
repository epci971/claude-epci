# 📚 Guide Exhaustif : Slash Commands, Skills & Subagents avec Claude Code

*Last updated: January 2026 – Basé sur les meilleures pratiques officielles Anthropic et Claude Code*

---

## Table des matières

1. [Vue d'ensemble](#vue-densemble)
2. [Slash Commands / Skills (Différence & Terminologie)](#slash-commands--skills)
3. [Best Practices Détaillées](#best-practices-détaillées)
4. [Structure SKILL.md Complète](#structure-skillmd-complète)
5. [Subagents : Concepts & Invocation](#subagents--concepts--invocation)
6. [Interactions entre Skills, Subagents & Commands](#interactions-entre-skills-subagents--commands)
7. [Exemples Concrets](#exemples-concrets)
8. [Anti-patterns à Éviter](#anti-patterns-à-éviter)
9. [Matrice Décisionnelle](#matrice-décisionnelle)
10. [Checklist de Qualité](#checklist-de-qualité)

---

## Vue d'ensemble

Claude Code a fusionné **slash commands** et **skills** en une seule système cohérent (2025-2026). Voici les trois briques principales :

| Concept | Rôle | Portée | Déclenchement |
|---------|------|--------|----------------|
| **Slash Command / Skill** | Encapsuler procédures & standards opérationnels | Local, session actuelle | Vous ou Claude automatiquement |
| **Subagent** | Déléguer tâches spécialisées avec contexte isolé | Isolé, parallélisable | Appel explicite ou automatique |
| **Project (CLAUDE.md)** | Contexte persistant et connaissances long-terme | Projet-wide | Toujours chargé |

---

## Slash Commands & Skills

### Terminologie : Unification Moderne

**Avant 2025** : Distinction entre `/commands` (fichiers `.claude/commands/`) et Skills
**Depuis 2025** : **Fusion complète** – Les deux créent des `/slash-commands` exécutables

```
Ancien chemin: ~/.claude/commands/review.md    → crée /review
Nouveau chemin: ~/.claude/skills/review/SKILL.md → crée /review (même résultat)
```

**À savoir** :
- Les deux systèmes coexistent et fonctionnent de la même façon
- Les skills offrent **plus de fonctionnalités** (context: fork, hooks, allowed-tools, subagents)
- **Recommandation officielle** : Préférer `.claude/skills/` pour les nouvelles créations

### Scope & Localisation

```
~/.claude/skills/ma-skill/SKILL.md           → Personal (tous les projets)
./.claude/skills/ma-skill/SKILL.md           → Project (ce projet seulement)
Managed settings                             → Enterprise (org-wide)
<plugin>/skills/ma-skill/SKILL.md            → Plugin (avec plugin)
```

**Ordre de priorité en cas de conflit** : Enterprise > Personal > Project > Plugin

---

## Best Practices Détaillées

### 1️⃣ **Longueur & Taille Optimale**

#### SKILL.md body (contenu markdown)
- **Recommandation officielle** : **< 500 lignes**
- **Pratique** : 100-300 lignes pour clarté maximale
- **Au-delà** : Utiliser progressive disclosure (voir section 5)

#### Description (frontmatter)
- **Longueur** : 1-3 phrases (50-150 mots max)
- **Style** : Indicatif + cas d'usage naturels
- **Clés de succès** : Inclure des **trigger words** (termes que l'utilisateur dirait naturellement)

```yaml
# ✅ BON - Spécifique & richement tagged
description: >
  Analyzer des pull requests GitHub en détail. Montre diffs, code changes, 
  commentaires. Utilise pour code review, vérifier changements, évaluer qualité PR.
  Trigger: PR review, pull request, code changes, diff analysis.

# ❌ MAUVAIS - Trop vague
description: "Outils pour code review"
```

#### Argument-hint (optionnel)
```yaml
argument-hint: "[pr-number]"                    # Unique argument
argument-hint: "[filename] [format]"            # Multiple arguments
argument-hint: "[issue-id] [priority]"          # Positional params
```

### 2️⃣ **Syntaxe & Frontmatter Obligatoire**

#### Structure de base (YAML frontmatter)

```yaml
---
name: ma-skill
description: Ce que fait cette skill et quand l'utiliser
disable-model-invocation: false  # Claude peut l'invoquer auto
user-invocable: true             # Visible dans le menu /
argument-hint: "[param]"         # Suggestion autocomplete
allowed-tools: Read, Grep        # Outils autorisés
model: sonnet                    # Optionnel : modèle spécifique
context: fork                    # Optionnel : isolation subagent
agent: Explore                   # Type subagent (si context: fork)
---

# Contenu markdown ici...
```

#### Frontmatter référence complète

| Champ | Required? | Type | Défaut | Notes |
|-------|-----------|------|--------|-------|
| `name` | Non | string | nom du répertoire | Lowercase, max 64 chars, `-` ok |
| `description` | **Recommended** | string | 1er paragraphe | Claude l'utilise pour trigger |
| `argument-hint` | Non | string | none | Affichage autocomplete |
| `disable-model-invocation` | Non | boolean | false | `true` = vous seul |
| `user-invocable` | Non | boolean | true | `false` = Claude seul |
| `allowed-tools` | Non | list | inherit | `Read, Grep, Bash, etc.` |
| `model` | Non | string | inherit | `sonnet`, `haiku`, ou full ID |
| `context` | Non | enum | none | `fork` = isolé subagent |
| `agent` | Non | string | general-purpose | Type subagent (Explore, Plan) |
| `hooks` | Non | object | none | PreToolUse, PostToolUse, Stop |

### 3️⃣ **Style & Ton**

#### Pour la description
```yaml
# ✅ STYLE RECOMMANDÉ
description: >
  Analyzes code and suggests refactoring opportunities. Use when reviewing code, 
  identifying technical debt, planning improvements. Keywords: refactor, optimize, 
  improve code quality, technical debt.

# ✅ OK - Variante plus personnelle
description: >
  My team's testing framework. Covers unit tests, integration tests, 
  and mock patterns. Invoke when writing tests or setting up test infrastructure.
```

#### Pour le contenu
- **Soyez explicite** : "Étapes à suivre", "Checklist", "Règles strictes"
- **Évitez l'ambiguïté** : Préférer listes à prose dense
- **Incluez des exemples** : Montrez format attendu
- **Signalez les pièges** : "⚠️ Attention: ..." / "❌ Ne pas ..."

```markdown
---
name: code-review
description: Review pull requests with attention to security and performance
---

## Processus de Review (À SUIVRE DANS L'ORDRE)

1. **Lire le contexte PR**
   - Titre et description PR
   - Quelle issue est résolue?
   
2. **Analyser les changes**
   - Fichiers modifiés
   - Lignes ajoutées/supprimées
   - Risques potentiels

3. **Checklist sécurité**
   - ❌ SQL injection ?
   - ❌ XSS ?
   - ❌ Fuite données sensibles ?

4. **Feedback constructif**
   - Poser questions plutôt que juger
   - Suggérer alternatives
```

### 4️⃣ **Obligations & Interdictions**

#### ✅ Obligations

| Obligation | Raison | Exemple |
|-----------|--------|---------|
| **SKILL.md must exist** | Point d'entrée requis | Toute skill doit avoir ce fichier |
| **Name doit être unique** | Évite les collisions | `pr-reviewer` pas `my-skill` |
| **Description explicite** | Claude s'en sert pour trigger | Inclure cas d'usage & trigger words |
| **Instructions claires** | Pas d'ambiguïté | "Étapes dans cet ordre exactement" |
| **Tester avant commit** | Évite surprises | `/skill-name` pour tester |

#### ❌ Interdictions

| Interdiction | Pourquoi | Anti-exemple |
|-------------|----------|--------------|
| **Pas de localStorage/sessionStorage** | SecurityError en sandbox | `localStorage.setItem()` → 💥 |
| **Pas de frontmatter malformé** | Crash parser | `name: my-skill` sans `---` |
| **Pas d'arguments sans handling** | Perte d'info | Si vous acceptez args, utiliser `$ARGUMENTS` |
| **Pas de descriptions génériques** | Claude ne trigger pas | "Aide utile" au lieu de "Refactor code" |
| **Pas d'autre langage frontmatter** | YAML only | JSON ou TOML → parse error |
| **Pas de fichiers non-référencés** | Confusion Claude | Ajouter sub-fichier sans le lier dans SKILL.md |

### 5️⃣ **Gestion des Fichiers Volumineux (Progressive Disclosure)**

Quand contenu > 400 lignes, utiliser **progressive disclosure** :

```
ma-skill/
├── SKILL.md              # Entrée courte (100-200 lignes max)
│   └── Liens vers: reference.md, examples.md
├── reference.md          # Détails complets (chargé à la demande)
├── examples.md           # Cas d'usage (chargé à la demande)
├── templates/
│   └── template.md       # Templates (chargé si besoin)
└── scripts/
    └── helper.py         # Scripts (exécutés, pas chargés)
```

**Dans SKILL.md** :
```markdown
## Ressources supplémentaires

- Pour détails techniques complets, voir [reference.md](reference.md)
- Pour exemples d'utilisation, voir [examples.md](examples.md)
- Pour templates prêts à l'emploi, voir [templates/](templates/)
```

**Résultat** : SKILL.md reste léger, details chargés on-demand (économise contexte)

### 6️⃣ **Substitutions Dynamiques**

#### Variables disponibles

```yaml
$ARGUMENTS        # Tout ce qui suit /skill-name
$1, $2, ...       # Arguments positionnels (usage rare)
${CLAUDE_SESSION_ID}  # Session actuelle (logging, files)
```

#### Exemples

```yaml
---
name: fix-issue
description: Fix a specific GitHub issue
argument-hint: "[issue-number]"
---

Fix GitHub issue #$ARGUMENTS following our coding standards:

1. Read issue #$ARGUMENTS from GitHub
2. Understand the requirements
3. Implement the fix
4. Write tests
5. Create commit mentioning issue #$ARGUMENTS
```

**Quand vous tapez** `/fix-issue 123`, Claude voit : "Fix GitHub issue #123 ..."

#### Cas spécial : Si pas de $ARGUMENTS
```yaml
# Si skill n'utilise pas $ARGUMENTS, claude ajoute:
# ARGUMENTS: <ce que vous avez tapé>
```

### 7️⃣ **Injections Dynamiques Avancées (!command)**

Exécuter shell commandes avant d'envoyer à Claude :

```yaml
---
name: pr-summary
description: Summarize a pull request with live data
context: fork
agent: Explore
allowed-tools: Bash(gh:*)
---

## PR Context (Live Data)

- PR Diff: !`gh pr diff`
- PR Comments: !`gh pr view --comments`
- Changed Files: !`gh pr diff --name-only`

## Task

Summarize this PR highlighting the key changes...
```

**Mécanique** :
1. `!`commande"` s'exécute **avant** que Claude le voie
2. Output remplace le placeholder
3. Claude reçoit le rendu final avec données réelles

**Contraintes** :
- Doit être déterministe (même commande = même output)
- Timeout ~ 10s typiquement
- À utiliser pour contexte live (PR diffs, logs) pas statique (docs)

---

## Structure SKILL.md Complète

### Template Minimal

```yaml
---
name: analyze-performance
description: Analyze code performance and suggest optimizations. Use when reviewing performance issues, profiling results, or optimizing slow functions.
disable-model-invocation: false
user-invocable: true
---

# Performance Analysis Skill

When analyzing code performance:

1. **Identify bottlenecks**
   - Time complexity analysis
   - Memory allocation patterns
   - I/O operations

2. **Profile results**
   - Read provided profiling data
   - Highlight hotspots
   - Quantify impact

3. **Suggest optimizations**
   - Algorithm improvements
   - Data structure changes
   - Caching strategies

4. **Validate assumptions**
   - Explain trade-offs
   - Benchmark impact
   - Risk assessment
```

### Template Avancé (avec fichiers supports)

```yaml
---
name: architecture-review
description: Review system architecture for scalability, security, reliability. Use when evaluating new services, assessing architectural changes, or planning system redesigns.
user-invocable: true
disable-model-invocation: false
allowed-tools: Read, Grep
---

# Architecture Review Skill

## Quick Review Checklist

- [ ] Scalability: Can this handle 10x growth?
- [ ] Security: Are we protecting sensitive data?
- [ ] Reliability: Single points of failure?
- [ ] Maintainability: Can others understand it?

## Detailed Process

For detailed review framework, see [FRAMEWORK.md](FRAMEWORK.md).

For real-world examples, see [EXAMPLES.md](EXAMPLES.md).

## Your Task

Analyze the architecture and provide:
1. Executive summary (1 paragraph)
2. Strengths (3-5 points)
3. Risks (3-5 points)
4. Recommendations (prioritized action items)
```

### Template avec Context Fork (Subagent)

```yaml
---
name: deep-research
description: Deeply research a topic with full codebase exploration. Use when you need comprehensive understanding of a complex system or unfamiliar codebase.
context: fork
agent: Explore
disable-model-invocation: false
---

# Deep Research Task

Research $ARGUMENTS comprehensively:

## Phase 1: Discover
- Use Glob to find relevant files
- Look for patterns in structure
- Identify key entry points

## Phase 2: Analyze
- Read critical files
- Trace function flows
- Document relationships

## Phase 3: Summarize
- Synthesize findings
- Create mental map
- Highlight key insights

## Output Format
- Project structure overview
- Key components & relationships
- Main workflows
- Unresolved questions
```

### Template avec Hooks (Gouvernance)

```yaml
---
name: secure-deployment
description: Deploy to production with security checks. Require code review and tests before deployment.
disable-model-invocation: true
allowed-tools: Bash(deploy:*)
hooks:
  PreToolUse:
    - name: "check-tests"
      tool: "Bash"
      condition: "deploy" # Avant deploy
      action: "Run test suite and require 100% pass"
    - name: "audit-changes"
      tool: "Bash"
      action: "List all changes and require confirmation"
---

# Secure Deployment

⚠️ **PRODUCTION DEPLOYMENT** ⚠️

This skill requires:
1. All tests passing
2. Code review approval
3. Manual confirmation

Proceed only if all conditions met.

## Deployment Steps

1. Run full test suite
2. Build production artifacts
3. Verify no breaking changes
4. Deploy to staging first
5. Health checks
6. Deploy to production
7. Monitor for issues
```

---

## Subagents : Concepts & Invocation

### Qu'est-ce qu'un Subagent?

**Subagent** = Mini-Claude spécialisé avec:
- Contexte isolé (pas d'accès à conversation principale)
- Rôle défini (description claire)
- Outils restreints (least privilege)
- System prompt personnalisé (instructions)
- Possibilité de charger des Skills
- Modèle spécifique (optionnel)

### Quand utiliser?

| Cas d'usage | Raison | Exemple |
|-----------|--------|---------|
| **Tâches parallèles** | Traiter indépendamment | Recherche + analyse + audit simultanés |
| **Contexte isolé** | Éviter pollution mémoire | Lire docs confidentielles sans leak |
| **Permissions restreintes** | Sécurité | Read-only review vs write access |
| **Expertise spécialisée** | Role focus | Tech reviewer vs business reviewer |
| **Tâches bruyantes** | Éviter distraction | Deep exploration sans spammer main thread |

### Types de Subagents Intégrés

```yaml
Explore    # Read-only, optimisé pour exploration codebase
Plan       # Planification, stratégie, décomposition tâches
general-purpose  # Default, capacités complètes
```

### Invocation de Subagents

#### Méthode 1 : Depuis Skill avec `context: fork`

```yaml
---
name: audit-security
description: Audit code security in isolated context
context: fork
agent: Explore          # Read-only agent
---

Audit the security of $ARGUMENTS:
1. Find all security-sensitive code
2. Check for common vulnerabilities
3. Report findings with evidence
```

**Résultat** : Tâche exécutée dans contexte isolé Explore, sans pollution

#### Méthode 2 : Explicite dans main conversation

```
Je veux que tu utilises un subagent pour investiguer la perf.
@performance-investigator, analyse ce code
```

(Syntax exact dépend de votre setup Claude Code)

#### Méthode 3 : Subagents avec Skills préchargées

**Créer subagent personnalisé** :

```
~/.claude/agents/security-reviewer/AGENT.md:

---
name: security-reviewer
description: Specialized security code reviewer
model: sonnet
skills:
  - security-guidelines     # Précharge cette skill
  - owasp-checklist         # Et celle-ci
allowed-tools: Read, Grep   # Outils limités
---

You are a security-focused code reviewer...
```

**Invoquer** : Claude peut auto-invoquer si description match, ou vous: `@security-reviewer`

### Configuration Subagent Minimale

```yaml
---
name: researcher
description: Research topics deeply with document analysis
model: sonnet
skills:
  - research-framework
allowed-tools: Read, Glob, Grep
---

# You are a dedicated researcher

Your role is to:
1. Find authoritative sources
2. Extract key information
3. Synthesize findings
4. Highlight gaps

Follow research-framework skill for methodology.
```

---

## Interactions entre Skills, Subagents & Commands

### Architecture complète

```
┌─────────────────────────────────────────────────────────┐
│                  MAIN CONVERSATION                      │
│  (Your context, Claude's reasoning, interaction loop)   │
└──────────┬──────────────────────────────────────────────┘
           │
    ┌──────┴──────┐
    │             │
    ▼             ▼
┌─────────┐  ┌──────────────────────────┐
│ SKILLS  │  │ SUBAGENTS (Isolated)     │
│         │  │                          │
│ /skill1 │  │ ┌─ Deep exploration      │
│ /skill2 │  │ ├─ Parallel processing   │
│ /skill3 │  │ └─ Restricted tools      │
└─────────┘  │                          │
             │ Subagents can load       │
             │ and use Skills           │
             └──────────────────────────┘
             
    ▼
┌──────────────────────┐
│ TOOLS & ENVIRONMENT  │
│ (Bash, Read, Write)  │
└──────────────────────┘
```

### Flux d'invocation

#### Scénario 1 : Skill seule
```
/pr-review
  ↓
SKILL.md loaded
  ↓
Claude follows instructions inline
  ↓
Main conversation continues
```

#### Scénario 2 : Skill + Subagent via context: fork
```
/deep-analysis
  ↓
context: fork detected
  ↓
New isolated context created
  ↓
Subagent (Explore) runs task
  ↓
Results summarized back to main
```

#### Scénario 3 : Subagent avec Skills préchargées
```
@security-reviewer invoked (auto ou manual)
  ↓
Subagent loaded with:
  - Custom system prompt
  - Preloaded skills
  - Restricted tools
  ↓
Executes task independently
  ↓
Reports findings to main thread
```

#### Scénario 4 : Skill invoke autre Skill (indirect)
```
/main-skill
  ↓
Instructions référencent "use helper-skill framework"
  ↓
Claude loads helper-skill si pertinent
  ↓
Combine instructions
```

**Note** : Interaction directe skill-à-skill est indirecte (via Claude)

### Données flux entre composants

```
Main Conversation
  ├─→ CLAUDE.md (available)
  ├─→ @mention subagent
  │   └─→ Subagent receives:
  │       ├─ Task description
  │       ├─ Preloaded skills
  │       ├─ CLAUDE.md
  │       └─ Tool permissions
  │   └─→ Returns: Summary
  │
  └─→ /invoke skill
      └─ Skill receives:
          ├─ $ARGUMENTS if provided
          ├─ Context (files you mention)
          ├─ Current conversation
          └─ Tool permissions
```

---

## Exemples Concrets

### Exemple 1 : Skill Simple (Code Review)

**Chemin** : `~/.claude/skills/review-pr/SKILL.md`

```yaml
---
name: review-pr
description: Review pull requests for code quality, tests, documentation, performance, and security. Use when reviewing PRs, checking code changes, or evaluating quality. Trigger words: PR review, pull request, code review, changes, diff.
argument-hint: "[pr-number-or-link]"
disable-model-invocation: false
user-invocable: true
allowed-tools: Read, Bash(gh:*)
---

# Pull Request Review Skill

## Review Checklist (Must Cover All)

### Code Quality
- [ ] Code follows project conventions
- [ ] No obvious bugs or logic errors
- [ ] Function names are clear
- [ ] Comments where needed
- [ ] Complexity reasonable

### Testing
- [ ] Tests added for new functionality
- [ ] Tests are comprehensive
- [ ] Edge cases covered
- [ ] No skipped tests

### Documentation
- [ ] README updated if needed
- [ ] API docs current
- [ ] Changelog entry added
- [ ] Comments for complex logic

### Performance & Security
- [ ] No SQL injection vulnerabilities
- [ ] No XSS if web-related
- [ ] No hardcoded secrets
- [ ] Performance acceptable
- [ ] No memory leaks

## Output Format

Provide feedback as:

```
## Summary
[1-2 sentence summary]

## Strengths
- [good point 1]
- [good point 2]

## Issues (Priority Order)
### Critical
- [issue 1]
- [issue 2]

### Minor
- [nitpick 1]

## Suggestions
[Constructive feedback]
```

## Usage

/review-pr <pr-number>
```

**Utilisez** : `/review-pr 123` ou `/review-pr https://github.com/org/repo/pull/456`

---

### Exemple 2 : Skill Avancée avec Progressive Disclosure

**Structure** :
```
~/.claude/skills/architecture-review/
├── SKILL.md
├── FRAMEWORK.md
├── SECURITY-CHECKLIST.md
├── EXAMPLES.md
└── scripts/
    └── diagram-generator.py
```

**SKILL.md** :
```yaml
---
name: architecture-review
description: >
  Comprehensive system architecture review covering scalability, security, 
  reliability, maintainability, and cost. Use when evaluating new services, 
  assessing redesigns, or planning infrastructure. Keywords: architecture, 
  design review, system redesign, scalability, service design.
allowed-tools: Read, Grep
---

# Architecture Review

## Quick Assessment (Always Do First)

1. **What is the system?** (2-3 sentences)
2. **Scale & load expectations?**
3. **Critical business requirements?**
4. **Known constraints?**

## Detailed Review

For comprehensive review framework, see [FRAMEWORK.md](FRAMEWORK.md)

For security-specific checklist, see [SECURITY-CHECKLIST.md](SECURITY-CHECKLIST.md)

For real examples, see [EXAMPLES.md](EXAMPLES.md)

## Output Format

Generate structured report:
- Executive Summary
- Architecture Diagram (ASCII)
- Component Analysis
- Risk Assessment
- Recommendations (prioritized)
```

**FRAMEWORK.md** (chargé on-demand) :
```markdown
# Complete Architecture Review Framework

## Scalability Review
- Database: Horizontal sharding needed? Query patterns?
- Caching: Where are hot spots? TTL strategy?
- Load balancing: Stateless services?
- CDN: Static assets distributed?

## Security Review
- Authentication: Method? Tokens secure?
- Authorization: RBAC or ABAC?
- Data protection: Encryption at rest/in transit?
- Secrets management: Rotation? Storage?

[... 200+ lines de détails ...]
```

**Invocation** :
```
/architecture-review

Claude lit SKILL.md court (contexte économisé),
puis charge FRAMEWORK.md si besoin analyse détaillée
```

---

### Exemple 3 : Skill avec Context Fork (Subagent)

```yaml
---
name: deep-research
description: >
  Research complex topics with isolated context. Thoroughly explores codebase, 
  traces flows, builds understanding. Use for unfamiliar systems, architecture 
  understanding, or deep dives. Trigger: learn, understand, trace, flow, deep dive.
context: fork
agent: Explore
disable-model-invocation: false
allowed-tools: Read, Glob, Grep
---

# Deep Research Task

Research $ARGUMENTS with comprehensive understanding.

## Phase 1: Discovery (Files & Structure)
- Use Glob to find related files
- Build mental map of organization
- Identify entry points and main flows

## Phase 2: Analysis (Code & Logic)
- Read key files
- Trace execution flow
- Document relationships
- Note patterns and conventions

## Phase 3: Synthesis
- Create overall architecture understanding
- Explain key workflows
- List open questions
- Suggest learning path for others

## Output
Provide:
1. **Architecture Overview** (ASCII diagram)
2. **Key Components** (what each does, relationships)
3. **Main Workflows** (step-by-step flows)
4. **Unresolved Questions** (gaps in understanding)
5. **Learning Path** (how to explain to new engineer)
```

**Résultat** : Recherche approfondie en contexte isolé, ne bloque pas main thread

---

### Exemple 4 : Skill avec Injection Dynamique

```yaml
---
name: github-sync
description: Synchronize with GitHub. Fetches PRs, issues, discussions. Use to get latest project status, review activity, plan sprints.
context: fork
agent: Explore
allowed-tools: Bash(gh:*), Bash(jq:*)
---

# GitHub Project Sync

## Current Project Data (Live)

- Open PRs: !`gh pr list --state open --json title,author,url`
- Recent issues: !`gh issue list --state open --json title,labels,url | jq '.[] | select(.labels[] | .name == "bug")'`
- Project velocity: !`gh pr list --state closed --limit 30 --json mergedAt`
- Team status: !`gh pr list --state open --json author,title`

## Task

Based on the live data above:

1. **Current Status**: What's in flight? What's blocked?
2. **Blockers**: Any critical issues delaying progress?
3. **Review Load**: PR queue healthy?
4. **Recommendations**: Priorities for sprint?

## Output Format
- Status summary (1 paragraph)
- Issues by priority
- PRs by review status
- Recommended next 5 tasks
```

**Avantage** : Données réelles à chaque exécution, pas stale

---

### Exemple 5 : Subagent Personnalisé

**Chemin** : `~/.claude/agents/test-architect/AGENT.md`

```yaml
---
name: test-architect
description: >
  Specialized test strategy and architecture consultant. Designs test suites, 
  coverage strategies, and testing frameworks. Use when building new test infrastructure, 
  improving coverage, or redesigning test organization.
model: sonnet
skills:
  - test-framework-guide
  - coverage-strategies
  - testing-best-practices
allowed-tools: Read, Grep, Bash(test:*)
---

# You are a Test Architect

Your expertise:
- Designing comprehensive test suites
- Balancing unit/integration/e2e
- Achieving optimal coverage
- Optimizing test performance
- Preventing flaky tests

## Your Standards

### Test Pyramid
- 70% unit tests (fast, isolated)
- 20% integration tests (components)
- 10% e2e tests (critical flows)

### Coverage Goals
- Minimum 80% code coverage
- 100% on critical paths
- 100% on security code

### Best Practices
- Follow AAA pattern (Arrange, Act, Assert)
- One assertion per test where possible
- Clear test names describing scenario
- Avoid test interdependencies
- Mock external dependencies

## Your Role

When asked about tests:
1. Analyze current test situation
2. Identify gaps and weaknesses
3. Design improved architecture
4. Provide step-by-step implementation
5. Include metrics for success
```

**Invocation** :
```
@test-architect, design tests for this new payment module

ou

Claude auto-invokes si conversation about testing
```

---

### Exemple 6 : Interaction Skills + Subagents

```
Main request: "Analyze this system's performance issues"

┌─────────────────────────────────────────┐
│ Main Claude evaluates situation         │
│ → Recognizes need for multiple angles   │
└────────────────┬────────────────────────┘
                 │
        ┌────────┴────────┐
        ▼                 ▼
   ┌─────────────┐  ┌──────────────────┐
   │ /perf-audit │  │@perf-analyzer    │
   │ (Skill)     │  │(Subagent)        │
   └─────────────┘  │                  │
        │            │ • Isolated       │
        │            │ • Deep analysis  │
        │            │ • Profiling      │
        │            └──────────────────┘
        │                    │
        │ (peut charger)     │
        │ ↓                  │
        │ /perf-conventions  │
        │ (autre Skill)      │
        │                    │
        └────────┬───────────┘
                 │
        ┌────────▼──────────┐
        │ Main synthesizes  │
        │ recommendations   │
        └───────────────────┘
```

---

## Anti-patterns à Éviter

### ❌ Anti-pattern 1 : Description trop vague

```yaml
# ❌ MAUVAIS
description: "Helpful code assistant"

# ✅ BON
description: >
  Optimize database queries for performance. Analyzes slow queries, suggests 
  indexes, rewrites SQL. Trigger: query performance, slow SQL, database optimization.
```

**Problème** : Claude ne sait pas quand l'invoquer

### ❌ Anti-pattern 2 : Skill trop grande

```markdown
---
name: everything
description: Does everything
---

# This skill covers:
- Code review (200 lines)
- Testing strategy (200 lines)
- Documentation (200 lines)
- Deployment (200 lines)
- Performance (200 lines)
...
(1000+ lignes totales)
```

**Problème** : Pas de focus, contexte pollué

**Solution** : Diviser en 5 skills spécialisées

### ❌ Anti-pattern 3 : Pas de handling d'arguments

```yaml
---
name: fix-issue
description: Fix GitHub issues
---

Fix the GitHub issue.

# ❌ Problem: N'utilise pas $ARGUMENTS
```

**Solution** :
```yaml
Fix GitHub issue $ARGUMENTS according to our standards.
```

### ❌ Anti-pattern 4 : Subagent pour tout

```
Utiliser context: fork pour CHAQUE skill
```

**Problème** : Overhead de contexte, perte conversation

**Solution** : Fork only si:
- Exploration bruyante (deep dive)
- Isolation requise (confidentiel)
- Tâche complètement indépendante

### ❌ Anti-pattern 5 : Description = instructions

```yaml
# ❌ MAUVAIS
description: "Step 1: read file. Step 2: parse. Step 3: output."

# ✅ BON
description: "Parse configuration files and validate syntax. Use when analyzing configs or validating deployment files."
```

**Problème** : Description pour routing, pas instructions détaillées

### ❌ Anti-pattern 6 : Frontmatter mal formé

```yaml
# ❌ Parse error
name: my-skill
description: ...
# Missing opening ---

# ❌ Wrong syntax
{name: "my-skill", ...}     # JSON not YAML
```

**Solution** : Toujours vérifier structure YAML

### ❌ Anti-pattern 7 : Outils trop restrictifs

```yaml
allowed-tools: Read   # ❌ Trop restrictif, peut pas faire tests
allowed-tools: "*"    # ❌ Trop permissif, risque sécurité

# ✅ Balanced
allowed-tools: Read, Bash(test:*)
```

### ❌ Anti-pattern 8 : Noms ambigus

```yaml
# ❌ Ambigus
name: helper
name: utils
name: process

# ✅ Clair
name: test-generator
name: pr-analyzer
name: config-validator
```

---

## Matrice Décisionnelle

### Quand utiliser Skill vs Subagent vs Project vs MCP?

```
┌─────────────────────────────────────────────────────────────────┐
│                        MATRICE DÉCISIONNELLE                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│ Besoin: Encapsuler PROCÉDURE/STANDARD/SOP                       │
│ └─→ SKILL (ou SKILL + context:fork si isolé)                    │
│     Exemple: Code review checklist, deployment process          │
│                                                                   │
│ Besoin: Stockage CONTEXTE LONG-TERME (docs, config, history)    │
│ └─→ PROJECT (CLAUDE.md + fichiers de contexte)                  │
│     Exemple: Architecture docs, team conventions                │
│                                                                   │
│ Besoin: Connecter système EXTERNE (GitHub, Slack, DB)          │
│ └─→ MCP (protocole de connectivité)                             │
│     Exemple: Fetch live PR data, sync with Slack                │
│                                                                   │
│ Besoin: Isoler TÂCHE SPÉCIALISÉE (parallèle, permissions)       │
│ └─→ SUBAGENT (@name ou context:fork dans skill)                 │
│     Exemple: Recherche profonde, review sécurité, audit         │
│                                                                   │
│ Besoin: INSTRUCTION TEMPORAIRE (une-off, expérimentale)         │
│ └─→ CONVERSATION DIRECTE (pas de skill)                         │
│     Exemple: "Could you please..."                              │
│                                                                   │
│ Besoin: Plusieurs de ces briques ensemble?                      │
│ └─→ ARCHITECTURE COMPOSÉE                                       │
│     Skill → charge Project + MCP + invoques Subagent            │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

### Tableau comparatif rapide

| Besoin | Skill | Subagent | Project | MCP |
|--------|-------|----------|---------|-----|
| Procédure réutilisable | ✅ | ❌ | ❌ | ❌ |
| Contexte long-terme | ❌ | ❌ | ✅ | ❌ |
| Tâche isolée/parallèle | ⚠️ (fork) | ✅ | ❌ | ❌ |
| Connecter externe | ❌ | ❌ | ❌ | ✅ |
| Données live | ⚠️ (! injection) | ✅ | ❌ | ✅ |
| Permissions restreintes | ✅ (allowed-tools) | ✅ | ❌ | ❌ |
| Rapidité activation | ✅ | ⚠️ | ✅ | ❌ |
| Riche customization | ✅ | ✅ | ✅ | ⚠️ |

---

## Checklist de Qualité

### ✅ Avant de committer une Skill

- [ ] **Structure valide**
  - [ ] SKILL.md existe
  - [ ] YAML frontmatter correct (testé avec: `cat SKILL.md | head -20`)
  - [ ] Fermé avec `---` final
  
- [ ] **Naming**
  - [ ] `name:` unique dans projet + personnel
  - [ ] Lowercase, hyphens ok, max 64 chars
  - [ ] Évite noms génériques (pas "helper", "utils")
  
- [ ] **Description**
  - [ ] 1-3 phrases (50-150 mots)
  - [ ] Inclut cas d'usage & trigger words
  - [ ] Testée avec `/skill-name` auto-invocation
  - [ ] Claude la trouve avec `What skills available?`
  
- [ ] **Contenu**
  - [ ] < 500 lignes (ou progressive disclosure si plus)
  - [ ] Instructions claires & step-by-step
  - [ ] Exemples de output format si pertinent
  - [ ] Checklist ou règles strictes si données sensibles
  
- [ ] **Arguments**
  - [ ] Si accepte args: `$ARGUMENTS` utilisé ou explication
  - [ ] `argument-hint` fourni
  - [ ] Testé avec: `/skill-name test-arg`
  
- [ ] **Fichiers supports**
  - [ ] Tous référencés dans SKILL.md
  - [ ] Pas de "orphelin files"
  - [ ] Path relatif correct
  
- [ ] **Sécurité**
  - [ ] Pas localStorage/sessionStorage
  - [ ] `allowed-tools` set si restreint
  - [ ] Règles d'entrée explicites si données sensibles
  
- [ ] **Context Fork** (si applicable)
  - [ ] `context: fork` + `agent:` spécifié
  - [ ] Task clear & self-contained
  - [ ] Output format défini
  
- [ ] **Testée**
  - [ ] `/skill-name` fonctionne
  - [ ] `/skill-name with-args` fonctionne si applicable
  - [ ] Output approche attendu
  - [ ] Edge cases testés
  
### ✅ Avant de reviewer une PR avec Skills

- [ ] Skill description match actually does?
- [ ] Pas d'over-loading dans une skill
- [ ] Évite duplication avec autres skills
- [ ] Progressive disclosure utilisée si 300+ lignes
- [ ] Frontmatter fields pertinents présents
- [ ] Security constraints respected

---

## Tips Avancés & Astuces

### 💡 Tip 1 : Discoverable Descriptions

```yaml
# ❌ Peu découvrable
description: "Code review"

# ✅ Très découvrable - Beaucoup de trigger words
description: >
  Code review and analysis. Review pull requests, check code changes, 
  examine diffs, verify quality, assess design, evaluate performance, 
  check security, validate tests, ensure documentation. Use when 
  reviewing PRs, changes, or evaluating code quality. Trigger words: 
  review, PR, pull request, code quality, assessment, check, analysis.
```

### 💡 Tip 2 : Skill Composing (Skills utilisant autres Skills)

```yaml
---
name: full-pr-review
description: Complete PR review including code, tests, and security
---

## Code Review

See: code-review-framework skill for checklist

## Test Review

See: test-quality-framework skill for standards

## Security Review

See: security-checklist skill for vulnerabilities
```

Claude chargerait automatiquement ces frameworks si référencés

### 💡 Tip 3 : Template-based Skills

```
my-skill/
├── SKILL.md
└── templates/
    ├── report-template.md
    ├── checklist-template.md
    └── architecture-template.md
```

**Dans SKILL.md** :
```markdown
## Output Templates

Use one of these templates:
- [Report template](templates/report-template.md)
- [Checklist template](templates/checklist-template.md)
```

### 💡 Tip 4 : Session-aware Logging

```yaml
---
name: task-logger
description: Log activities for audit and learning
---

Task execution logged to: `logs/${CLAUDE_SESSION_ID}.log`

This session ID: `${CLAUDE_SESSION_ID}`
```

Utile pour tracer exécutions cross-sessions

### 💡 Tip 5 : Model Selection per Skill

```yaml
---
name: quick-lint
model: haiku  # ✅ Fast for simple checks
---

---
name: architecture-analysis
model: sonnet  # ✅ Reasoning power for complex analysis
---
```

Économiser tokens sur tâches rapides

### 💡 Tip 6 : Conditional Tool Access

```yaml
allowed-tools: Read, Grep, Bash(lint:*)
# ✅ Claude peut: Read files, Grep, run linting
# ❌ Claude ne peut pas: Write, deploy, execute arbitrary Bash
```

### 💡 Tip 7 : Skills comme "Reference Material"

```yaml
---
name: api-conventions
description: API design patterns and conventions
user-invocable: false  # ❌ Not a command
disable-model-invocation: false  # ✅ Auto-loaded by Claude
---

# API Conventions

When Claude is writing APIs, it auto-loads this reference
```

---

## Résumé des Best Practices Clés

```
╔══════════════════════════════════════════════════════════════════╗
║                 BEST PRACTICES EN UN COUP D'ÉIL                  ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                   ║
║ 1. LONGUEUR                                                       ║
║    • SKILL.md body: < 500 lignes                                 ║
║    • Description: 1-3 phrases avec trigger words                 ║
║                                                                   ║
║ 2. SYNTAXE                                                        ║
║    • YAML frontmatter entre --- ---                              ║
║    • `name:` unique et lowercase                                 ║
║    • `description:` obligatoire (recommandé)                     ║
║                                                                   ║
║ 3. STYLE                                                          ║
║    • Instructions claires & step-by-step                         ║
║    • Exemples d'output format                                    ║
║    • Checklist si critère validation                             ║
║                                                                   ║
║ 4. ARGUMENTS                                                      ║
║    • Utiliser $ARGUMENTS si accepte params                       ║
║    • Fournir argument-hint pour autocomplete                     ║
║                                                                   ║
║ 5. PROGRESSIVE DISCLOSURE                                        ║
║    • SKILL.md court (100-300 lignes)                             ║
║    • Fichiers supports pour détails (reference.md)               ║
║    • Linker depuis SKILL.md                                      ║
║                                                                   ║
║ 6. SUBAGENTS                                                      ║
║    • Utiliser context:fork pour isolation                        ║
║    • Spécifier agent: type (Explore, Plan)                       ║
║    • Limiter tools avec allowed-tools                            ║
║                                                                   ║
║ 7. SÉCURITÉ                                                       ║
║    • Pas localStorage/sessionStorage                             ║
║    • Définir allowed-tools explicitement                         ║
║    • Valider inputs sensibles                                    ║
║                                                                   ║
║ 8. TESTAGE                                                        ║
║    • Tester /skill-name avant commit                             ║
║    • Vérifier auto-invocation (si souhaité)                      ║
║    • Tester avec arguments si applicable                         ║
║                                                                   ║
╚══════════════════════════════════════════════════════════════════╝
```

---

## Ressources Officielles

- **Claude Code Docs** : https://code.claude.com/docs/en/slash-commands
- **Anthropic Engineering Blog** : Claude Code best practices
- **Official Repo** : github.com/anthropics/prompt-eng (examples)
- **Community Guide** : Multiple contribut patterns

---

**Questions?** Ce guide couvre la majorité des cas. Pour patterns edge-case, consulter la documentation officielle Claude Code.

**Version** : 2026-01-21 basée sur Claude Code stable release
