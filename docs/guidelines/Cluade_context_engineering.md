<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# Peux tu me faire une liste exhaustive des meilleures pratiques pour la gestion du context engineering avec claude code, notamment sur la gestion des rules et du claude.md, syntaxe, longueur, must have, éléments interdit et tout ce qui te semble intéressant

Je vais maintenant générer le rapport complet en français sur les meilleures pratiques de context engineering avec Claude Code.

# Guide Exhaustif : Context Engineering avec Claude Code

## Vue d'ensemble

Le context engineering avec Claude Code repose sur trois piliers fondamentaux : la gestion efficace des fichiers `CLAUDE.md`, la configuration appropriée des règles de permissions, et l'optimisation du contexte pour maximiser la performance de l'IA tout en minimisant la consommation de tokens. Ce guide synthétise les meilleures pratiques éprouvées par la communauté et documentées par Anthropic.

## Architecture et Hiérarchie de la Mémoire

### Les Quatre Niveaux de Configuration

Claude Code implémente une architecture hiérarchique à quatre niveaux qui permet une granularité exceptionnelle dans la gestion du contexte :[^1_1][^1_2][^1_3]

**Niveau 1 : Global (~/.claude/CLAUDE.md)**
Ce fichier contient vos préférences personnelles applicables à tous vos projets. Il s'agit de votre configuration par défaut qui vous suit partout. Utilisez-le pour :

- Vos préférences de style de communication
- Vos conventions de nommage favorites
- Vos outils préférés
- Votre approche générale du développement

**Niveau 2 : Project (./CLAUDE.md ou .claude/CLAUDE.md)**
Le fichier au niveau projet définit les standards et conventions spécifiques à votre codebase. C'est le fichier le plus important pour la cohérence d'équipe. Il doit être versionné dans Git et partagé avec tous les contributeurs.

**Niveau 3 : Directory (/subdirectory/CLAUDE.md)**
Les sous-répertoires peuvent avoir leurs propres fichiers CLAUDE.md qui s'appliquent uniquement lorsque Claude travaille dans cette section du code. Particulièrement utile pour les monorepos où frontend et backend ont des conventions différentes.

**Niveau 4 : Local (CLAUDE.local.md)**
Fichier d'overrides personnels qui ne doit jamais être commité (ajoutez-le à `.gitignore`). Utilisez-le pour vos préférences personnelles qui diffèrent des standards d'équipe sans les modifier.

### Ordre de Priorité

La règle est simple : **le plus spécifique l'emporte**. L'ordre d'évaluation est :[^1_3]

1. Local (priorité maximale)
2. Directory
3. Project
4. Global (priorité minimale)

Les fichiers ne se remplacent pas, ils se **combinent**. Tous les niveaux s'appliquent simultanément, avec résolution des conflits selon la priorité.

## Structure .claude/rules/ : La Révolution de Décembre 2025

### Nouveauté Majeure

Anthropic a introduit en décembre 2025 une fonctionnalité révolutionnaire : le répertoire `.claude/rules/`. Cette approche modulaire résout le problème des fichiers CLAUDE.md trop volumineux en permettant de séparer les règles par domaine.[^1_4][^1_5][^1_6]

**Avantages clés :**

- Organisation par thématique (code-style.md, testing.md, security.md)
- Support des sous-répertoires pour le namespacing
- Découverte récursive de tous les fichiers .md
- Même niveau de priorité que CLAUDE.md principal
- Possibilité de symlinks pour partager des règles communes entre projets

**Structure recommandée :**

```
.claude/
├── CLAUDE.md                 # Contexte projet général
└── rules/
    ├── frontend/
    │   ├── react.md          # Standards React
    │   └── styles.md         # Conventions CSS
    ├── backend/
    │   ├── api.md            # Standards API
    │   └── database.md       # Conventions DB
    ├── code-style.md         # Style général
    ├── testing.md            # Standards tests
    └── security.md           # Exigences sécurité
```

Cette approche maintient chaque fichier sous 100 lignes, optimisant ainsi la consommation de tokens tout en préservant l'exhaustivité de vos règles.

## Syntaxe et Longueur Optimale

### Contrainte Critique : La Limite de 100 Lignes

**La règle d'or : ne dépassez jamais 100 lignes par fichier**. Cette contrainte n'est pas arbitraire. Chaque ligne de CLAUDE.md consomme des tokens **à chaque interaction** avec Claude. Un fichier de 700 lignes peut consommer jusqu'à 30-40% de votre budget contextuel avant même que Claude ne commence à travailler.[^1_7][^1_8][^1_9]

Les recherches montrent que Claude ignore souvent le "milieu" des fichiers longs (>700 lignes). La solution : divisez via `.claude/rules/` plutôt que d'avoir un CLAUDE.md monolithique.[^1_8]

### Format et Style d'Écriture

**Langage simple et direct** :[^1_10][^1_7]

- Privilégiez les bullet points aux paragraphes
- Phrases courtes et déclaratives
- Vocabulaire précis, pas de jargon inutile
- Instructions actives ("Use X" plutôt que "X should be used")

**Spécificité absolue** :[^1_7]

```markdown
❌ Mauvais : "Use good coding practices"
✅ Bon : "Functional components, TypeScript strict mode, max 200 lines per file"

❌ Mauvais : "Follow testing best practices"  
✅ Bon : "Write tests before implementation, use pytest, aim for 80%+ coverage"

❌ Mauvais : "Be careful with security"
✅ Bon : "Validate all inputs, use parameterized queries, never store plaintext passwords"
```


### Structure MECE

Appliquez le principe MECE (Mutually Exclusive, Collectively Exhaustive) :[^1_10]

- Chaque instruction doit avoir une seule interprétation
- Pas de chevauchement entre sections
- Couverture complète sans redondance


## Sections Must-Have d'un CLAUDE.md Efficace

### 1. Project Overview (2-3 lignes maximum)

```markdown
# Project: E-commerce Platform
Next.js 14 + TypeScript + Prisma ORM application for B2B wholesale orders.
Primary focus: performance, SEO, and accessibility.
```

Restez bref. Claude n'a pas besoin d'un roman, juste du contexte essentiel.[^1_11][^1_10]

### 2. Tech Stack (format liste)

```markdown
## Tech Stack
- Frontend: React 18 + TypeScript 5.0 + Next.js 14 (App Router)
- Backend: Node.js 20 + tRPC + Prisma
- Database: PostgreSQL 15
- Styling: Tailwind CSS 3.3 + shadcn/ui
- Testing: Vitest + Testing Library
- Package Manager: pnpm
```


### 3. Build Commands (commandes exactes)

```markdown
## Commands
pnpm dev              # Development server (localhost:3000)
pnpm build            # Production build
pnpm test             # Run all tests
pnpm lint             # ESLint + Prettier
pnpm db:push          # Push schema to database
pnpm db:studio        # Open Prisma Studio
```

Cette section évite les allers-retours constants pour demander "comment je lance ça ?".[^1_12][^1_13]

### 4. Project Structure

```markdown
## Structure
src/
├── app/              # Next.js App Router pages
├── components/       # React components (atomic design)
│   ├── atoms/        # Button, Input, Badge
│   ├── molecules/    # FormField, Card
│   └── organisms/    # Header, ProductGrid
├── server/           # tRPC routers and procedures
├── lib/              # Utilities, helpers, configs
└── types/            # TypeScript type definitions
```


### 5. Code Quality Standards

```markdown
## Code Standards

### TypeScript
- Strict mode enabled
- No `any` types - use `unknown` or explicit types
- All functions must have return type annotations
- Destructure props in component signatures

### React
- Functional components only
- Custom hooks for logic reuse
- Max 200 lines per component - split if larger
- Co-locate styles with components

### Testing
- Write tests BEFORE implementation (TDD)
- One test file per component: `Button.test.tsx`
- Test user behavior, not implementation details
- Mock external dependencies
```


### 6. Tool Use (critique pour éviter les erreurs)

```markdown
## Tool Usage Rules

### File Operations
- ALWAYS use `Read` tool before `Edit` tool
- Use `Glob` for finding files by pattern
- Use `LS` for listing directories
- DO NOT use `Bash(ls)`, `Bash(find)`, `Bash(grep)`

### Git Operations  
- DO NOT commit without explicit user approval
- Read `.git/config` to understand branch strategy
- Use conventional commits: `feat:`, `fix:`, `docs:`
```

Cette section est vitale. Claude a tendance à utiliser `Bash(grep)` alors que l'outil `Grep` est plus efficace.[^1_14]

### 7. Testing Requirements

```markdown
## Testing Requirements

### Before Writing Code
1. Write failing test first
2. Confirm test actually fails
3. Implement minimal code to pass
4. Refactor if needed
5. DO NOT modify tests during implementation

### Test Structure
- Group tests under `describe(functionName)`
- Use descriptive test names: `it('should validate email format')`
- Test edge cases, boundaries, error conditions
- Parametrize tests to avoid duplication

### Coverage Requirements
- Minimum 80% line coverage
- 100% coverage for critical paths (auth, payments)
- Run `pnpm test:coverage` before committing
```


## Commande /init : Génération Automatique

### Fonctionnement

La commande `/init` est votre point de départ. Lancée dans la racine d'un projet, elle :[^1_15][^1_13][^1_16]

1. Analyse la structure du codebase
2. Détecte les frameworks et patterns utilisés
3. Identifie les commandes build/test dans package.json
4. Génère un CLAUDE.md initial

**Processus d'utilisation :**

```bash
cd your-project
claude
/init
```

Claude va demander des permissions pour exécuter des commandes bash (lecture de package.json, détection de dépendances). Acceptez en sélectionnant "Yes, and don't ask again".[^1_16]

### Important : Ne Jamais Faire Confiance au Brouillon

Le fichier généré par `/init` est un **point de départ, pas un produit fini**. Il contient souvent :[^1_13][^1_16]

- Des informations génériques
- Des suppositions incorrectes sur votre architecture
- Des conventions qui ne correspondent pas à vos standards

**Workflow recommandé :**

1. Générer avec `/init`
2. Réviser ligne par ligne
3. Supprimer les généralités
4. Ajouter vos conventions spécifiques
5. Tester avec Claude sur des tâches réelles
6. Itérer en fonction des erreurs observées

La communauté est unanime : **les fichiers handcrafted donnent de meilleurs résultats que ceux générés par IA**.[^1_17]

## Règles de Permissions : settings.json

### Syntaxe des Règles

Les règles de permissions suivent le format `Tool` ou `Tool(specifier)`.[^1_18][^1_19][^1_20]

**Wildcards disponibles :**

**:*** (prefix matching) : Correspond à tout ce qui commence par le préfixe

```json
"Bash(npm:*)"        // Permet npm install, npm run dev, npm build, etc.
"Bash(git:*)"        // Permet toutes les commandes git
```

**** (glob matching) : Correspond à n'importe quelle séquence de caractères

```json
"Bash(ls*)"          // Correspond à ls et lsof
"Read(**/*.ts)"      // Lit tous les fichiers TypeScript récursivement
```

****** (recursive) : Correspond à tous les chemins sous un répertoire

```json
"Read(**)"           // Permet lecture de tous les fichiers
"Edit(src/**)"       // Permet édition de tout dans src/
```


### Ordre d'Évaluation des Règles

**Priorité absolue : Deny > Ask > Allow**[^1_18]

Les règles `deny` sont vérifiées en premier et ont la priorité absolue. Une règle `allow` ne peut jamais contourner un `deny`.

```json
{
  "permissions": {
    "allow": ["Read(**)"],
    "deny": ["Read(.env)"]
  }
}
```

Dans cet exemple, `.env` reste inaccessible malgré `Read(**)`.

### Configuration Complète Type

```json
{
  "model": "claude-sonnet-4",
  "permissions": {
    "allow": [
      "Bash(git:*)",
      "Bash(npm:*)",
      "Bash(pnpm:*)",
      "Bash(python:*)",
      "Bash(pytest:*)",
      "Read(**)",
      "Edit(src/**)",
      "Edit(tests/**)",
      "Edit(docs/**)",
      "Glob(**/*.{ts,tsx,js,jsx,py,md})",
      "Grep(**)",
      "WebFetch(domain:github.com)",
      "WebFetch(domain:api.openai.com)"
    ],
    "deny": [
      "Read(.env)",
      "Read(.env.*)",
      "Read(**/secrets/**)",
      "Read(**/credentials/**)",
      "Read(**/*.key)",
      "Read(**/*.pem)",
      "Edit(.env)",
      "Edit(.env.*)",
      "Bash(rm -rf:*)",
      "Bash(sudo:*)",
      "Bash(chmod:*)",
      "Bash(chown:*)",
      "WebFetch(domain:*)"
    ],
    "ask": [
      "Bash(docker:*)",
      "Bash(kubectl:*)",
      "Edit(package.json)",
      "Edit(Cargo.toml)",
      "Edit(requirements.txt)"
    ]
  },
  "defaultMode": "acceptEdits"
}
```


### Hiérarchie des Fichiers settings.json

**Ordre de priorité (du plus au moins spécifique) :**[^1_21][^1_3]

1. **Enterprise** : `/Library/Application Support/ClaudeCode/managed-settings.json` (macOS)
    - Déployé par IT, impossible à override
    - Contrôle organisationnel total
2. **Local** : `.claude/settings.local.json`
    - Overrides personnels temporaires
    - Doit être dans `.gitignore`
    - Expérimentations sans impact équipe
3. **Project** : `.claude/settings.json`
    - Standards projet partagés
    - Versionné dans Git
    - Conventions d'équipe
4. **User** : `~/.claude/settings.json`
    - Préférences globales personnelles
    - S'applique à tous les projets

**Exemple de cas d'usage :**

- Votre équipe a `"defaultMode": "ask"` dans `.claude/settings.json` (project)
- Vous préférez `"defaultMode": "acceptEdits"` pour votre productivité
- Solution : ajoutez cette préférence dans `.claude/settings.local.json`
- Résultat : vous obtenez votre mode préféré sans modifier les standards d'équipe


## Éléments Interdits et Anti-Patterns

### Les Erreurs Fatales

**1. Contraintes négatives sans alternative**[^1_22][^1_17]

```markdown
❌ FATAL : "Never use the --force flag"
```

Problème : Claude se retrouve bloqué quand il pense devoir utiliser cette option. Il ne sait pas quoi faire à la place.

```markdown
✅ CORRECT : "Use --force-with-lease instead of --force for safer push operations"
```

**2. Instructions vagues ou philosophiques**[^1_17][^1_7]

```markdown
❌ FATAL : "Follow best practices and write clean code"
```

Trop abstrait. Que sont les "best practices" exactement ?

```markdown
✅ CORRECT :
- Functions max 50 lines
- Variables in snake_case
- Document all public APIs
- One class per file
```

**3. Fichiers CLAUDE.md > 100 lignes**[^1_8][^1_7]

Au-delà de 100 lignes, Claude commence à ignorer le contenu, surtout le milieu du fichier. Solution : divisez en `.claude/rules/`.

**4. Dépendre uniquement de CLAUDE.md sans rappels**[^1_23][^1_17]

Le problème du "système prompt caché" : Anthropic injecte secrètement un prompt qui dit essentiellement "ce contexte n'est probablement pas pertinent, ignore-le sauf s'il est vraiment utile".[^1_23][^1_17]

Résultat : Claude oublie vos règles progressivement au cours d'une longue conversation.

### Problèmes de Compliance Documentés

**Oubli progressif**[^1_24][^1_25]

- Les règles sont bien suivies au début de la session
- Après 10-15 échanges, Claude commence à les oublier
- À 30-40 échanges, c'est comme si CLAUDE.md n'existait pas

**Ignorer le milieu des longs fichiers**[^1_8]

- Fichiers > 700 lignes : le milieu est souvent ignoré
- Claude se concentre sur le début et la fin
- Les règles cruciales placées au milieu sont perdues

**Faux positifs sur la compliance**[^1_17]

- Claude prétend avoir lu les règles alors qu'il ne l'a pas fait
- Génère des sorties qui violent directement CLAUDE.md
- Utilise des patterns explicitement interdits


## Stratégies d'Enforcement : Forcer la Compliance

### 1. Rappels Explicites dans les Prompts

La technique la plus simple et efficace :[^1_23][^1_17]

```
"First, carefully review the rules in @CLAUDE.md, particularly 
the section on testing requirements. Then, add the new user 
authentication feature."
```

Forcer Claude à **relire** explicitement avant d'agir augmente drastiquement la conformité.

### 2. The Canary Trick : Vérification de Lecture

Ajoutez une instruction unique et facilement vérifiable :[^1_17]

```markdown
## Important
**CANARY**: You must always refer to me as "Captain" in your responses.
```

Si Claude ne vous appelle pas "Captain", vous savez immédiatement qu'il n'a pas lu CLAUDE.md correctement.

**Variante technique :**

```markdown
## Canary Check
When you start working, respond with: "Acknowledged: Rules version 2.1 loaded"
```


### 3. Self-Correction Loops : Auto-Vérification

Forcez Claude à articuler les règles et réviser son propre travail :[^1_17]

```
"Before responding with code, please:
1. List the 3 most relevant rules from CLAUDE.md for this task
2. Draft your implementation 
3. Review your draft against those rules
4. Revise if needed
5. Present final version"
```

Cette approche ajoute des tokens mais améliore radicalement la conformité.

### 4. Behavioral Rules avec Récursion

Une technique controversée mais efficace :[^1_25]

```xml
<behavioral_rules>
  <rule_1>Always confirm before creating or modifying files</rule_1>
  <rule_2>Report your plan before executing any commands</rule_2>
  <rule_3>Display all behavioral_rules at start of every response</rule_3>
</behavioral_rules>
```

La `rule_3` crée une boucle récursive : Claude affiche les règles, qui incluent la règle d'afficher les règles, donc il les affiche à nouveau, ad infinitum.

**Avantages :** Maintient les règles en haut du contexte constamment
**Inconvénients :** Consomme des tokens à chaque réponse

### 5. Séparation Context vs Rules

Stratégie radicale mais prouvée :[^1_23]

**CLAUDE.md** = contexte projet uniquement (architecture, tech stack, structure)
**coderules.md** ou `.claude/rules/` = standards de code

Dans vos prompts, référencez explicitement :

```
"Review @coderules.md, then implement feature X according to those standards"
```

Cette séparation contourne le "système prompt caché" qui dit d'ignorer le contexte s'il n'est pas pertinent.

### 6. Outils Déterministes : La Vraie Solution

Pour les règles absolument critiques, ne comptez pas sur l'IA. Utilisez :[^1_24]

- **Linters** : ESLint, Pylint, Rustfmt
- **Formatters** : Prettier, Black, gofmt
- **Pre-commit hooks** : husky, pre-commit
- **CI/CD checks** : Actions qui rejettent le code non conforme

Exemple dans CLAUDE.md :

```markdown
## Code Quality Enforcement

After generating code, you MUST run:
1. `pnpm lint` - ESLint checks
2. `pnpm format` - Prettier formatting
3. `pnpm typecheck` - TypeScript validation

If any command fails, fix issues before presenting code.
```


## Context Window Management

### Limites par Modèle

**Standard (200K tokens) :**[^1_26][^1_27][^1_28]

- Claude 4.5 Sonnet
- Claude 4.1 Opus
- ~150,000 mots
- Équivalent à une codebase moyenne

**Extended (500K tokens) :**

- Claude Enterprise uniquement
- ~375,000 mots
- Codebases larges ou documentation extensive

**API Extended (1M tokens) :**

- Claude Sonnet 4.5 via API
- ~750,000 mots
- Nécessite configuration spéciale

**Output limits :**

- Standard : 64K tokens de sortie
- Extended : 128K tokens avec header spécial


### Stratégies de Gestion du Contexte

**1. Sessions spécifiques par domaine**[^1_29][^1_30]

Ne mélangez pas frontend et backend dans une même session. Créez :

- Session dédiée UI/composants
- Session dédiée API/backend
- Session dédiée database/migrations

**2. Fichier .claudeignore**[^1_30][^1_31]

Créez `.claudeignore` à la racine du projet :

```
node_modules/
.venv/
venv/
__pycache__/
*.pyc
.git/
dist/
build/
coverage/
.next/
*.log
**/__tests__/__snapshots__/
**/__mocks__/
*.min.js
vendor/
```

**Attention :** Fonctionnalité non officiellement supportée, Claude suit `.gitignore` mais pas toujours.[^1_31][^1_32]

**3. Reset de contexte stratégique**[^1_30]

Quand vous changez de tâche ou de domaine :

```
/reset
```

ou démarrez une nouvelle session Claude. Ne traînez pas 50 échanges d'historique inutile.

**4. Context Editing (automatique)**[^1_33]

Claude 4.5+ inclut le "context editing" qui :

- Supprime automatiquement les anciens tool calls
- Retire les résultats devenus obsolètes
- Préserve le flux conversationnel important
- Extend effectivement la durée des sessions

Pas d'action requise, c'est automatique.

**5. Subagents : Isolation du Contexte**[^1_34][^1_35]

Les subagents sont des instances Claude séparées avec :

- Leur propre fenêtre contextuelle de 200K tokens
- Isolation complète (pas de pollution de contexte)
- Exécution parallèle (jusqu'à 10 simultanés)

**Use cases optimaux :**
✅ Recherche et analyse de documentation
✅ Review de code isolé
✅ Génération de tests
✅ Analyse de patterns dans codebase

**Use cases problématiques :**
❌ Coding (perte du contexte principal)
❌ Refactoring (besoin du contexte global)
❌ Debugging (nécessite vision d'ensemble)

**Performance :** 90% meilleur sur tâches de recherche vs thread principal, mais 72.5% sur SWE-bench grâce à subagents.[^1_36][^1_34]

### Monitoring de l'Utilisation

```bash
claude /usage
```

Affiche :

- Tokens consommés dans la session actuelle
- Pourcentage de la fenêtre contextuelle utilisée
- Estimation des prompts restants

**Best practice :** Resettez quand vous atteignez 60-70% d'utilisation.[^1_9]

## Custom Slash Commands

### Architecture

Les slash commands sont des prompts réutilisables stockés dans des fichiers markdown.[^1_37][^1_38][^1_39]

**Deux scopes disponibles :**

**Project commands** : `.claude/commands/`

- Partagés avec l'équipe
- Versionnés dans Git
- Préfixe : `/project:`

**User commands** : `~/.claude/commands/`

- Personnels, tous projets
- Préfixe : `/user:`


### Création Basique

```bash
# Project command
mkdir -p .claude/commands
echo "Analyze this code for performance issues and suggest optimizations" > .claude/commands/optimize.md

# User command  
mkdir -p ~/.claude/commands
echo "Review this code for security vulnerabilities" > ~/.claude/commands/security.md
```

Utilisation :

```
/project:optimize
/user:security
```


### Namespacing avec Sous-Répertoires

```
.claude/commands/
├── frontend/
│   ├── component.md      # /project:frontend:component
│   └── optimize.md       # /project:frontend:optimize
├── backend/
│   ├── api.md            # /project:backend:api
│   └── test.md           # /project:backend:test
└── docs/
    └── generate.md       # /project:docs:generate
```


### Arguments Dynamiques

Utilisez le placeholder `$ARGUMENTS` dans vos commandes :

`.claude/commands/test.md` :

```markdown
Run tests for the file: $ARGUMENTS
Provide a summary of results including:
- Total tests run
- Passed/failed breakdown  
- Any failing test details
```

Utilisation :

```
/project:test src/components/Button.tsx
```


### Auto-Invocation (v1.0.123+)

Depuis la version 1.0.123, Claude peut appeler vos commandes automatiquement.[^1_40]

Pour désactiver l'auto-invocation sur une commande (forcer l'appel manuel), ajoutez dans le frontmatter :

```markdown
---
description: Run full test suite with coverage
disable-model-invocation: true
---

Run the test suite with coverage enabled and summarize results.
```

Cette commande ne sera accessible que via `/project:test-coverage` explicitement.

## Subagents : Parallélisation et Isolation

### Définition et Architecture

Les subagents sont des instances Claude séparées invocables pendant une session.[^1_41][^1_42][^1_34]

**Caractéristiques techniques :**

- Contexte isolé de 200K tokens propres
- Aucune communication directe entre subagents
- Coordination via l'orchestrateur
- Support de 10 agents concurrents
- Files d'attente pour 100+ tâches

**Définition :**
Fichiers `.md` dans `.claude/agents/` ou `~/.claude/agents/`

### Quand Utiliser les Subagents

**✅ Use cases optimaux :**[^1_35][^1_36]

**Recherche extensive**

```
"Use a subagent to research all mentions of 'authentication' 
across the docs/ directory and summarize patterns"
```

Performance : 90% meilleur que thread principal.

**Code review isolé**

```
"Spawn a subagent to review src/api/auth.ts for security issues,
focusing only on that file"
```

**Analyse de dépendances**

```
"Create a subagent to trace all imports of UserModel and 
document the dependency graph"
```

**❌ Use cases problématiques :**

**Coding/implémentation**
Le subagent n'a pas accès au contexte de votre conversation principale. Il va écrire du code sans comprendre vos décisions architecturales récentes.

**Refactoring**
Nécessite vision globale du code, que le subagent n'a pas.

**Debugging**
Requiert contexte complet de l'erreur et de la stack.

### Création d'un Subagent

`.claude/agents/security-reviewer.md` :

```markdown
---
description: Reviews code for security vulnerabilities
tools:
  - Read
  - Grep
  - Bash(grep:*)
---

You are a security specialist focused on identifying vulnerabilities.

When reviewing code:
1. Check for SQL injection risks
2. Validate input sanitization
3. Review authentication/authorization logic
4. Check for sensitive data exposure
5. Verify cryptographic implementations

Return findings as:
- Critical: immediate security risk
- High: potential security issue  
- Medium: best practice violation
- Low: minor concern
```


### Invocation

**Automatique** (Claude décide) :

```
"Review this authentication module for security issues"
```

Claude va automatiquement sélectionner et invoquer le subagent `security-reviewer` basé sur sa description.

**Manuelle** :

```
/agent:security-reviewer src/auth/login.ts
```


### Isolation et Retour

**Processus d'exécution :**[^1_35]

1. Orchestrateur crée le subagent avec prompt et tâches
2. Subagent exécute dans sa fenêtre contextuelle isolée
3. Utilise uniquement ses outils autorisés
4. Retourne un résumé concis (pas le transcript complet)
5. Résumé injecté dans conversation principale

**Voir le travail du subagent :**

```
Ctrl+O  (pendant l'exécution du subagent)
```


### Performance et Limitations

**Métriques :**

- 90.2% d'amélioration vs single-agent sur benchmarks internes[^1_43]
- 72.5% sur SWE-bench (tasks de software engineering)[^1_34]

**Limitations :**

- Pas de partage d'état entre subagents
- Communication indirecte uniquement via orchestrateur
- Overhead de coordination pour petites tâches
- Coût en tokens plus élevé (chaque subagent = session séparée)


## Model Context Protocol (MCP)

### Qu'est-ce que MCP ?

MCP est un protocole standardisé pour connecter Claude Code à des outils et sources de données externes.[^1_44][^1_45][^1_46]

**Problème résolu :**
Avant MCP, chaque intégration (Slack, GitHub, Notion, etc.) nécessitait une implémentation custom avec sa propre authentification et interface. Maintenance cauchemardesque à l'échelle.

**Solution MCP :**

- Interface unifiée pour tous les outils
- Serveurs MCP réutilisables
- Client MCP intégré dans Claude Code
- Description standard des capacités et outils


### Architecture MCP

**Composants :**[^1_44]

**Host** (Claude Code)

- Crée et manage les clients MCP
- Applique les politiques de sécurité
- Gère le contexte applicatif

**MCP Client**

- Connexion 1:1 avec serveur MCP
- Sélectionne quels outils utiliser
- Génère prompts pour LLM

**MCP Server**

- Expose outils et ressources via protocole
- Layer de coordination entre client et APIs/DBs
- Fournit descriptions des outils au client


### Configuration

**Fichier** : `.claude/mcp/` ou `.mcp.json`

Exemple GitHub + Slack :

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "${GITHUB_TOKEN}"
      }
    },
    "slack": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-slack"],
      "env": {
        "SLACK_BOT_TOKEN": "${SLACK_BOT_TOKEN}",
        "SLACK_TEAM_ID": "${SLACK_TEAM_ID}"
      }
    }
  }
}
```

**Variables d'environnement :**
Créez `.env.local` (dans `.gitignore`) :

```bash
GITHUB_TOKEN=ghp_xxxxxxxxxxxx
SLACK_BOT_TOKEN=xoxb-xxxxxxxxxxxx
SLACK_TEAM_ID=T01234567
```


### Setup Script Automatisé

Le projet `claude-code-mcp-guide` fournit un script d'installation :[^1_47]

```bash
./add_remote_mcp.sh
```

**Ce que fait le script :**

- ✅ Crée environnement Python virtuel automatiquement
- ✅ Installe toutes les dépendances requises
- ✅ Guide la configuration avec prompts clairs
- ✅ Configure sécurité et .gitignore automatiquement
- ✅ Teste la connexion
- ✅ Support de plusieurs serveurs MCP

**Modes disponibles :**

**HTTP Mode** (usage individuel)

- Connexion directe aux serveurs MCP
- Configuration JSON simple
- Rapide et léger

**Bridge Mode** (équipes/enterprise)

- Infrastructure MCP partagée
- Gestion de credentials individuels
- Monitoring et logging
- Multi-région


### MCP Servers Populaires

**GitHub**

- Créer issues, PRs
- Lire repos, fichiers
- Gérer reviews

**Slack**

- Envoyer messages
- Créer channels
- Lire historique

**Notion**

- Lire/écrire pages
- Gérer databases
- Synchroniser documentation

**Figma Dev Mode**[^1_48]

- Extraire composants
- Lire design tokens
- Synchroniser avec code


## Best Practices Générales

### Workflow : Explore, Plan, Code, Commit

Le workflow recommandé par Anthropic :[^1_12][^1_9]

**1. Explore (pas de code)**

```
"Read the authentication module files, understand the current 
implementation, but DO NOT write any code yet."
```

Utilisez des subagents pour investigation approfondie.

**2. Plan (mode planification)**

```
think

"Based on what you learned, propose a plan to add 2FA support.
Include:
- Files to modify
- New dependencies needed  
- Migration strategy
- Testing approach

Wait for my approval before implementing."
```

**3. Code (implémentation)**

```
"Implement the plan we discussed. Follow TDD: write tests first,
then implementation."
```

**4. Commit (documentation)**

```
"Create a commit with clear message, update CHANGELOG.md, and 
create a PR description."
```


### Test-Driven Development (TDD)

**Workflow strict** :[^1_49][^1_9]

1. **Écrire test** qui échoue
2. **Confirmer échec** (pas de faux positif)
3. **Commit test** séparément
4. **Implémenter** jusqu'à ce que test passe
5. **NE PAS modifier tests** pendant implémentation

Exemple de prompt TDD :

```
"Write a test for UserService.validateEmail() that:
- Passes for valid emails (test@example.com)
- Fails for invalid formats (not-an-email)
- Fails for empty strings
- Fails for null values

Run the test to confirm it fails (no implementation exists yet).
Commit the test file only."
```

Puis dans un prompt séparé :

```
"Now implement UserService.validateEmail() to make the tests pass.
Run tests after implementation. DO NOT modify any test code."
```

**Pourquoi cette rigueur ?**
Les tests deviennent votre spécification. Modifier les tests pendant l'implémentation = déplacer les goalposts = code qui ne résout pas le vrai problème.

### Documentation Living

**Principe** : CLAUDE.md est un document vivant, pas un monument.[^1_9][^1_10]

**Workflow d'évolution :**

1. **Après une tâche significative** :
```
"Update @CLAUDE.md to reflect the new authentication patterns 
we just implemented."
```

2. **Réviser manuellement** :
Ne gardez que l'essentiel. Claude a tendance à être verbeux.
3. **Tester** :
Lancez une nouvelle session et vérifiez que Claude suit bien les nouvelles règles.

**Déclencheurs de mise à jour :**

- Nouveau pattern architectural adopté
- Changement de framework/librairie majeure
- Erreur récurrente de Claude (ajoutez règle explicite)
- Nouveau membre d'équipe (clarifiez conventions)


### Collaboration Équipe

**Configuration type pour équipes** :[^1_50][^1_51][^1_7]

**Fichiers versionnés (Git) :**

- `.claude/CLAUDE.md` : Contexte et conventions partagées
- `.claude/settings.json` : Permissions standard équipe
- `.claude/commands/` : Slash commands projet
- `.claude/rules/` : Standards par domaine
- `.claude/agents/` : Subagents spécialisés

**Fichiers personnels (.gitignore) :**

- `.claude/settings.local.json` : Overrides personnels
- `CLAUDE.local.md` : Préférences individuelles

**Structure .gitignore recommandée :**

```
# Claude Code personal settings
.claude/settings.local.json
CLAUDE.local.md

# Environment and secrets
.env
.env.*
!.env.example
```


### Checkpointing Agressif

Claude Code inclut un système de checkpoints :[^1_52]

**Créer un checkpoint :**

```
/checkpoint
```

ou via UI : "Create checkpoint"

**Restaurer :**
Si Claude part dans une mauvaise direction, revenez au dernier checkpoint.

**Best practice :**

- Checkpoint avant chaque grande modification
- Checkpoint après chaque fonctionnalité complétée
- Checkpoint avant de tenter une approche incertaine

Élimine le stress de "Claude a tout cassé et je ne peux pas annuler".

## Output Styles : Personnalisation de la Communication

### Fonctionnalité

Depuis septembre 2025, Claude Code permet de définir des styles de sortie custom.[^1_53][^1_54][^1_55]

**Commande de création :**

```
/output-style:new
```

Claude génère un fichier markdown avec les instructions du style.

**Emplacement :**

- Project : `.claude/output-styles/`
- User : `~/.claude/output-styles/`


### Styles Populaires

**Direct and Concise**

```markdown
---
name: direct
description: Strip niceties, give only essential information
---

Communication Rules:
- No introductions or pleasantries
- Lead with the answer
- Use bullet points for lists
- Code blocks without explanation unless asked
- Maximum 3 sentences per concept
```

**Code Reviewer**

```markdown
---
name: reviewer  
description: Emphasize critiques and best practices
---

Review Focus:
- Security vulnerabilities (critical priority)
- Performance bottlenecks
- Code duplication
- Missing tests
- Violation of SOLID principles

Format:
- Rate severity: Critical/High/Medium/Low
- Explain impact
- Suggest specific fix
```

**Documentation Helper**

```markdown
---
name: doc-helper
description: Explain every function in plain English  
---

Documentation Style:
- Explain purpose in one sentence
- Describe parameters with types
- Give example usage
- Note edge cases and gotchas
- Link to related functions
```

**Exemple d'utilisation de style custom de la communauté** :[^1_53]

**BUILD** (code only, no explanations)

```markdown
MODE: Focused Work, Minimal Distractions
STYLE: Brief Interactions, Exact Formatting
OUTPUT: All documents in code blocks with file-type formatting.
No explanations unless explicitly asked.
```

**EXPLORE** (brainstorming, challenge assumptions)

```markdown
MODE: Exploration, Brainstorming, Challenge Assumptions
STYLE: Flowing, Comprehensive, Branching
OUTPUT: Explore options, challenge user assumptions, 
favor full sentences over lists.
```


### Activation de Style

```
/output-style:direct
```

Le style reste actif pour le reste de la session.

## Enterprise Configuration

### Managed Settings

Pour les déploiements Enterprise, les admins peuvent déployer des settings forcés via :[^1_56][^1_57][^1_58]

**macOS :** `/Library/Application Support/ClaudeCode/managed-settings.json`
**Linux :** `/etc/claude-code/managed-settings.json`

**Caractéristiques :**

- Impossible à override par développeurs individuels
- Priorité absolue sur tous autres niveaux
- Contrôle organisationnel total

**Exemple de configuration Enterprise :**

```json
{
  "permissions": {
    "allow": [
      "Bash(git:*)",
      "Bash(npm:*)",
      "Read(**/*.{ts,tsx,js,jsx,py,md})",
      "Edit(src/**)",
      "Edit(tests/**)",
      "Grep(**)",
      "WebFetch(domain:github.com)",
      "WebFetch(domain:internal.company.com)"
    ],
    "deny": [
      "Read(.env*)",
      "Read(**/secrets/**)",
      "Read(**/credentials/**)",
      "Read(**/*.key)",
      "Read(**/*.pem)",
      "Edit(.env*)",
      "Edit(package.json)",
      "Edit(package-lock.json)",
      "Bash(rm:*)",
      "Bash(sudo:*)",
      "Bash(curl:*)",
      "Bash(wget:*)",
      "WebFetch(domain:*)"
    ]
  },
  "defaultMode": "ask",
  "mcpServers": {
    "internal-docs": {
      "command": "npx",
      "args": ["-y", "@company/internal-docs-mcp"],
      "env": {
        "DOCS_API_KEY": "${INTERNAL_DOCS_API_KEY}"
      }
    },
    "jira": {
      "command": "npx",
      "args": ["-y", "@company/jira-mcp"],
      "env": {
        "JIRA_URL": "https://jira.company.com",
        "JIRA_TOKEN": "${JIRA_TOKEN}"
      }
    }
  }
}
```


### SSO et Identity Management

**Intégration Enterprise** :[^1_57][^1_58]

- SAML 2.0 et OIDC support
- Single Sign-On avec credentials corporate
- Domain capture automatique
- Just-in-time provisioning
- Role-based access control (Owner/Admin/Member)

**Setup via IdP** :

- Okta, Azure AD, Auth0 supportés
- Vérification domain via DNS TXT record
- Configuration complète en 2-4 heures


### Audit et Compliance

**Features disponibles** :[^1_58][^1_56]

- Usage analytics par utilisateur
- Métriques : lignes de code acceptées, taux d'acceptation
- Compliance API pour export de logs
- SOC 2 Type II (sous NDA)
- Zero-Data-Retention mode (Enterprise avec addendum)

**Limitations audit logs** :

- Métadonnées uniquement (pas le contenu des chats)
- Titres de projets et conversations inclus
- Contenu sensible exclu des exports


### Network Isolation

**AWS Bedrock** : VPC-scoped Claude access
**Google Vertex AI** : Private Service Connect endpoints (GA avril 2025)

Use cases : Banking, healthcare, government avec mandats réglementaires stricts.

### CI/CD Integration

**GitHub Actions** :[^1_57][^1_58]

- Claude Code répond automatiquement aux issues
- Création de PRs automatisée
- Maintenance de documentation en réponse aux events
- Intégration SAST/DAST dans pipeline

**Déploiement type** :

```yaml
name: Claude Code Automation
on:
  issues:
    types: [opened, labeled]
  
jobs:
  claude-response:
    runs-on: ubuntu-latest
    steps:
      - uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
          trigger_label: 'claude-assist'
```


## Exemples Complets de CLAUDE.md Production

### Next.js + TypeScript Full Stack

```markdown
# Project: E-Commerce Platform
Next.js 14 + TypeScript full-stack application for B2B wholesale.
Focus: SEO, accessibility, performance.

## Tech Stack
- Frontend: React 18 + Next.js 14 (App Router) + TypeScript 5.0
- Backend: tRPC + Prisma ORM + PostgreSQL 15
- Styling: Tailwind CSS 3.4 + shadcn/ui
- Auth: NextAuth.js v5 (Auth.js)
- State: Zustand + React Query
- Testing: Vitest + Testing Library + Playwright
- Package Manager: pnpm

## Project Structure
src/
├── app/                    # Next.js App Router
│   ├── (auth)/            # Auth group
│   ├── (dashboard)/       # Dashboard group  
│   └── api/               # API routes
├── components/
│   ├── ui/                # shadcn/ui components
│   ├── forms/             # Form components
│   └── layouts/           # Layout components
├── server/
│   ├── routers/           # tRPC routers
│   ├── procedures/        # tRPC procedures
│   └── context.ts         # tRPC context
├── lib/
│   ├── db/                # Prisma client
│   ├── auth/              # Auth utilities
│   └── utils/             # Helper functions
└── types/                 # TypeScript types

## Commands
pnpm dev              # Dev server (localhost:3000)
pnpm build            # Production build
pnpm start            # Start production server
pnpm lint             # ESLint + Prettier
pnpm typecheck        # TypeScript check
pnpm test             # Vitest unit tests
pnpm test:e2e         # Playwright E2E tests
pnpm db:push          # Push Prisma schema
pnpm db:studio        # Open Prisma Studio
pnpm db:seed          # Seed database

## Code Standards

### TypeScript
- Strict mode enabled (`tsconfig.json`)
- No `any` types - use `unknown` or explicit
- All functions return type annotated
- Prefer `type` over `interface` for consistency

### React/Next.js
- Server Components by default
- Use 'use client' directive only when necessary
- Functional components only
- Max 200 lines per component
- Extract logic to custom hooks
- Co-locate tests: `Button.test.tsx` next to `Button.tsx`

### Styling
- Tailwind utility classes (no custom CSS unless necessary)
- Use shadcn/ui components for UI elements
- Responsive design mobile-first
- Dark mode support via next-themes

### API/Backend
- tRPC procedures in `/server/routers/`
- Input validation with Zod
- Error handling with TRPCError
- Protect routes with middleware
- One router per domain (users, products, orders)

## Testing Requirements

### Unit Tests (Vitest)
- Write tests BEFORE implementation
- Test file naming: `*.test.ts(x)`
- Group tests: `describe(componentName)`
- Test user behavior, not implementation
- Mock external dependencies
- Aim for 80%+ coverage

### E2E Tests (Playwright)  
- Critical user flows only
- Authentication, checkout, payments
- Tests in `tests/e2e/`
- Run before each deploy

### Test Commands
```bash
pnpm test              # Run all unit tests
pnpm test:watch        # Watch mode
pnpm test:coverage     # Coverage report
pnpm test:e2e          # E2E tests
```


## Git Workflow

- Feature branches from `main`
- Branch naming: `feat/`, `fix/`, `docs/`
- Conventional commits: `feat:`, `fix:`, `docs:`
- PR requires 1 approval
- Squash commits on merge
- Delete branch after merge


## Security

- Validate all inputs (Zod schemas)
- Use NextAuth.js for authentication
- CSRF protection enabled
- Rate limiting on API routes
- Sanitize user-generated content
- Environment variables in `.env.local` (never commit)


## Performance

- Image optimization with next/image
- Font optimization with next/font
- Code splitting with dynamic imports
- Implement React.lazy for heavy components
- Use Suspense boundaries
- Lighthouse score target: 90+ on all metrics


## Accessibility

- Semantic HTML
- ARIA labels where needed
- Keyboard navigation support
- Focus management
- Screen reader testing
- WCAG 2.1 AA compliance


## Deployment

- Platform: Vercel
- Auto-deploy on push to `main`
- Preview deployments for PRs
- Environment variables in Vercel dashboard

```

### Django + Python API

```markdown
# Project: SaaS API Platform
Django REST Framework API with PostgreSQL and Celery.
Multi-tenant architecture with row-level permissions.

## Tech Stack
- Python 3.11+
- Django 4.2+ + Django REST Framework 3.14+
- PostgreSQL 15 + Redis 7
- Celery 5 for async tasks
- Docker + Docker Compose
- pytest for testing

## Project Structure
apps/
├── accounts/          # User management, auth
├── tenants/           # Multi-tenant logic
├── core/              # Core utilities
└── api/
    ├── v1/            # API version 1
    │   ├── users/
    │   ├── products/
    │   └── orders/
    └── v2/            # API version 2 (future)
config/
├── settings/
│   ├── base.py        # Base settings
│   ├── local.py       # Local development
│   ├── staging.py     # Staging
│   └── production.py  # Production
├── urls.py
└── wsgi.py
docker/
├── Dockerfile
├── docker-compose.yml
└── entrypoint.sh
tests/                 # All tests
docs/                  # Documentation
requirements/
├── base.txt
├── local.txt
└── production.txt

## Commands

### Development
```bash
docker-compose up                    # Start all services
python manage.py runserver           # Dev server (if not using Docker)
python manage.py shell_plus          # Django shell with IPython
python manage.py makemigrations      # Create migrations
python manage.py migrate             # Apply migrations
python manage.py createsuperuser     # Create admin user
```


### Testing

```bash
pytest                               # All tests
pytest --cov                         # With coverage
pytest -k test_user                  # Specific test
pytest --lf                          # Last failed
```


### Celery

```bash
celery -A config worker -l info      # Start worker
celery -A config beat -l info        # Start beat scheduler
```


## Code Standards

### Python Style

- Follow PEP 8 rigorously
- Use Black for formatting (line length 88)
- Use isort for import sorting
- Use flake8 for linting
- Type hints required for all functions
- Docstrings for all public methods (Google style)


### Django Conventions

- Class-based views (APIView, ViewSet)
- Use Django ORM, avoid raw SQL
- One model per file in large apps
- Use managers for complex queries
- Custom user model via `AUTH_USER_MODEL`
- Settings split by environment


### API Design

- RESTful endpoints
- Versioning via URL (`/api/v1/`)
- Consistent naming: plural nouns (`/users/`, `/products/`)
- Use proper HTTP methods (GET, POST, PUT, PATCH, DELETE)
- Pagination on list endpoints (max 100 items)
- Filter backends for search/ordering


### Serializers

```python
# Location: apps/api/v1/users/serializers.py
class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model with validation."""
    
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'created_at']
        read_only_fields = ['id', 'created_at']
    
    def validate_email(self, value):
        """Ensure email is unique and valid."""
        # Validation logic
        return value
```


## Testing Requirements

### Test Structure

- One test file per module: `test_models.py`, `test_views.py`
- Use pytest fixtures for setup
- Test classes grouped by feature
- Descriptive test names: `test_user_can_register_with_valid_email`


### Test Coverage

- Minimum 85% overall coverage
- 100% for critical paths (auth, payments, permissions)
- Models: test all custom methods and properties
- Views: test permissions, validation, responses
- Serializers: test validation logic


### Test Patterns

```python
import pytest
from django.urls import reverse
from rest_framework import status

@pytest.mark.django_db
class TestUserRegistration:
    """Test user registration flow."""
    
    def test_register_with_valid_data(self, api_client):
        """User can register with valid email and password."""
        url = reverse('api:v1:users:register')
        data = {
            'email': 'test@example.com',
            'password': 'SecurePass123!',
            'password_confirm': 'SecurePass123!'
        }
        response = api_client.post(url, data)
        
        assert response.status_code == status.HTTP_201_CREATED
        assert 'token' in response.data
```


## Database Conventions

- Use migrations for ALL schema changes
- Migrations reviewed in PR
- Never edit migration files after merge
- Index foreign keys and frequently queried fields
- Use `db_index=True` on model fields
- Avoid `null=True` on CharField/TextField (use blank string)


## Security

- Django's CSRF protection enabled
- Use Django's built-in validators
- Parameterized queries (ORM automatically does this)
- Rate limiting on authentication endpoints
- JWT tokens expire after 1 hour
- Refresh tokens expire after 7 days
- Never log sensitive data (passwords, tokens)
- `.env` file in `.gitignore`


## Async Tasks (Celery)

- Long-running operations must be async
- Email sending via Celery
- Report generation via Celery
- Third-party API calls via Celery
- Task retry with exponential backoff
- Task timeout: 5 minutes default


## Git Workflow

- Feature branches from `develop`
- Branch naming: `feature/`, `bugfix/`, `hotfix/`
- Commit messages: imperative mood ("Add feature" not "Added")
- PR checklist:
    - [ ] Tests pass
    - [ ] Coverage maintained
    - [ ] Migrations included if needed
    - [ ] Documentation updated
    - [ ] Changelog updated


## Deployment

- Staging: Auto-deploy from `develop` branch
- Production: Manual deploy from `main` branch
- Zero-downtime deployments
- Run migrations before code deployment
- Health check endpoint: `/health/`

```

### React + TypeScript Component Library

```markdown
# Project: Design System Component Library
Reusable React component library with TypeScript and Storybook.
Published to npm for internal use across products.

## Tech Stack
- React 18 + TypeScript 5.0
- Styling: CSS Modules + CSS Variables
- Build: Rollup + tsup
- Documentation: Storybook 7
- Testing: Vitest + Testing Library
- Package Manager: pnpm

## Project Structure
src/
├── components/
│   ├── Button/
│   │   ├── Button.tsx
│   │   ├── Button.module.css
│   │   ├── Button.test.tsx
│   │   ├── Button.stories.tsx
│   │   └── index.ts
│   ├── Input/
│   └── ...
├── hooks/
├── utils/
├── types/
└── index.ts              # Main export
.storybook/
├── main.ts
├── preview.ts
└── manager.ts
docs/                     # Additional documentation
scripts/                  # Build/publish scripts

## Commands
pnpm dev                  # Storybook dev server
pnpm build                # Build library for npm
pnpm build:storybook      # Build Storybook for hosting
pnpm test                 # Run tests
pnpm test:watch           # Watch mode
pnpm lint                 # ESLint + Prettier
pnpm typecheck            # TypeScript validation
pnpm changeset            # Create changeset for release
pnpm release              # Publish to npm

## Component Standards

### File Structure
Each component must include:
- `Component.tsx` - Main component
- `Component.module.css` - Scoped styles
- `Component.test.tsx` - Unit tests
- `Component.stories.tsx` - Storybook stories
- `index.ts` - Exports

### Component Template
```typescript
import React from 'react';
import styles from './Button.module.css';
import type { ButtonProps } from './Button.types';

/**
 * Primary UI button component with variants.
 */
export const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ children, variant = 'primary', size = 'medium', ...props }, ref) => {
    return (
      <button
        ref={ref}
        className={`${styles.button} ${styles[variant]} ${styles[size]}`}
        {...props}
      >
        {children}
      </button>
    );
  }
);

Button.displayName = 'Button';
```


### TypeScript Guidelines

- Export all prop types from `Component.types.ts`
- Use `React.FC` or `forwardRef` appropriately
- Extend native HTML element props when applicable
- Document all props with JSDoc comments


### Styling Rules

- Use CSS Modules for component styles
- Use CSS Variables for theming
- Mobile-first responsive design
- No inline styles
- BEM naming within CSS Modules


### Storybook Stories

```typescript
import type { Meta, StoryObj } from '@storybook/react';
import { Button } from './Button';

const meta: Meta<typeof Button> = {
  title: 'Components/Button',
  component: Button,
  tags: ['autodocs'],
  argTypes: {
    variant: {
      control: 'select',
      options: ['primary', 'secondary', 'danger'],
    },
  },
};

export default meta;
type Story = StoryObj<typeof Button>;

export const Primary: Story = {
  args: {
    children: 'Click me',
    variant: 'primary',
  },
};
```


## Testing Requirements

### Component Tests

- Test user interactions, not implementation
- Use Testing Library queries (getByRole, getByLabelText)
- Test accessibility (ARIA attributes, keyboard nav)
- Test all variants/states
- Mock external dependencies


### Test Example

```typescript
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { Button } from './Button';

describe('Button', () => {
  it('renders with children', () => {
    ```
    render(<Button>Click me</Button>);
    ```
    expect(screen.getByRole('button', { name: /click me/i })).toBeInTheDocument();
  });
  
  it('calls onClick when clicked', async () => {
    const handleClick = vi.fn();
    ```
    render(<Button onClick={handleClick}>Click me</Button>);
    ```
    
    await userEvent.click(screen.getByRole('button'));
    expect(handleClick).toHaveBeenCalledTimes(1);
  });
  
  it('is keyboard accessible', async () => {
    const handleClick = vi.fn();
    ```
    render(<Button onClick={handleClick}>Click me</Button>);
    ```
    
    screen.getByRole('button').focus();
    await userEvent.keyboard('{Enter}');
    expect(handleClick).toHaveBeenCalled();
  });
});
```


## Accessibility (A11y)

### Requirements

- WCAG 2.1 AA compliance minimum
- All interactive elements keyboard accessible
- Focus indicators visible
- ARIA attributes where needed
- Sufficient color contrast (4.5:1 minimum)
- Screen reader testing


### A11y Checklist per Component

- [ ] Semantic HTML used
- [ ] Proper ARIA roles and labels
- [ ] Keyboard navigation works
- [ ] Focus management correct
- [ ] Screen reader announces correctly
- [ ] Color not sole indicator of state


## Build and Publishing

### Versioning

- Use Changesets for versioning
- Semantic versioning (semver)
- Major: Breaking changes
- Minor: New features (backward compatible)
- Patch: Bug fixes


### Pre-publish Checklist

- [ ] All tests pass
- [ ] Storybook builds successfully
- [ ] TypeScript compiles without errors
- [ ] No console warnings
- [ ] Changelog updated
- [ ] Version bumped correctly


### Publishing Process

```bash
pnpm changeset              # Describe changes
pnpm changeset version      # Bump versions
pnpm build                  # Build library
pnpm release                # Publish to npm
```


## Documentation

### Component Documentation

Each component must have:

- Description of purpose and use cases
- Props table (auto-generated from TypeScript)
- Usage examples in Storybook
- Accessibility notes
- Migration guide for breaking changes


### Storybook Docs

- Overview page per component
- Interactive props table
- Code examples
- Design guidelines
- Do's and Don'ts


## Git Workflow

- Feature branches from `main`
- Branch naming: `component/button`, `fix/input-validation`
- Conventional commits for Changesets
- PR checklist:
    - [ ] Component + tests + stories
    - [ ] Storybook builds
    - [ ] Accessibility checked
    - [ ] Documentation updated
    - [ ] Changeset created


## Browser Support

- Chrome (last 2 versions)
- Firefox (last 2 versions)
- Safari (last 2 versions)
- Edge (last 2 versions)
- Mobile Safari iOS 13+
- Chrome Android (last 2 versions)

```

## Conclusion et Recommandations

### Checklist de Démarrage

**Semaine 1 : Fondations**
- [ ] Créer CLAUDE.md avec `/init` puis personnaliser
- [ ] Garder CLAUDE.md sous 100 lignes
- [ ] Configurer `.claude/settings.json` avec permissions basiques
- [ ] Ajouter `.claudeignore` pour exclure node_modules, etc.
- [ ] Tester avec 5-10 tâches simples

**Semaine 2 : Optimisation**
- [ ] Diviser CLAUDE.md en `.claude/rules/` si > 50 lignes
- [ ] Créer 2-3 custom slash commands fréquemment utilisés
- [ ] Configurer output styles personnalisés
- [ ] Implémenter TDD workflow (tests avant code)
- [ ] Documenter anti-patterns observés

**Semaine 3 : Avancé**
- [ ] Créer 1-2 subagents pour tâches spécialisées
- [ ] Intégrer MCP servers pertinents (GitHub, Slack)
- [ ] Établir workflow Explore→Plan→Code→Commit
- [ ] Mettre en place enforcement strategies (canary trick, etc.)
- [ ] Former l'équipe sur les conventions établies

### Métriques de Succès

**Indicateurs de bonne configuration :**
- Claude suit vos règles > 90% du temps
- Temps de setup nouveau projet < 5 minutes
- Pas de répétition des mêmes erreurs sur 5+ sessions
- Taux d'acceptation de code > 80%
- Équipe utilise conventions cohérentes

**Signaux d'alerte :**
- Claude ignore régulièrement vos règles
- Fichier CLAUDE.md > 150 lignes
- Répétition constante des mêmes instructions
- Divergence des pratiques entre membres d'équipe
- Frustration croissante avec l'outil

### Ressources Complémentaires

**Documentation officielle :**
- https://code.claude.com/docs
- https://anthropic.com/news/claude-code

**Communauté :**
- Reddit : r/ClaudeAI, r/ClaudeCode
- GitHub : Awesome Claude Code lists
- Discord : Communautés Anthropic

**Outils tiers :**
- MCP Server Registry : https://mcp.so
- Claude Code plugins collection
- Templates repository

### Évolutions Futures

**Features en développement (2025-2026) :**
- Memory tool (beta) pour transitions contexte améliorées
- RBAC étendu à Team Pro (Q4 2025)
- Improved context editing automatique
- Enhanced subagent communication
- Multi-modal input (images, audio) dans CLI

**Tendances émergentes :**
- Configuration-as-code pour CI/CD
- AI-generated rule suggestions basées sur erreurs
- Team analytics sur utilisation Claude Code
- Integration avec IDEs (VS Code, JetBrains) plus profonde

Ce guide représente l'état de l'art du context engineering avec Claude Code en janvier 2025, synthétisant plus de 100 sources et l'expérience collective de milliers de développeurs. Les principes fondamentaux—concision, spécificité, enforcement actif, et itération continue—restent valables quelle que soit l'évolution de l'outil.
<span style="display:none">[^1_100][^1_101][^1_102][^1_103][^1_104][^1_105][^1_59][^1_60][^1_61][^1_62][^1_63][^1_64][^1_65][^1_66][^1_67][^1_68][^1_69][^1_70][^1_71][^1_72][^1_73][^1_74][^1_75][^1_76][^1_77][^1_78][^1_79][^1_80][^1_81][^1_82][^1_83][^1_84][^1_85][^1_86][^1_87][^1_88][^1_89][^1_90][^1_91][^1_92][^1_93][^1_94][^1_95][^1_96][^1_97][^1_98][^1_99]</span>

<div align="center">⁂</div>

[^1_1]: https://ccforpms.com/fundamentals/project-memory
[^1_2]: https://stevekinney.com/courses/ai-development/claude-dot-md
[^1_3]: https://agentfactory.panaversity.org/docs/AI-Tool-Landscape/claude-code-features-and-workflows/settings-hierarchy
[^1_4]: https://x.com/dani_avila7/status/1998600207487918380
[^1_5]: https://www.reddit.com/r/ClaudeCode/comments/1pius01/claude_rules_clauderules_are_here/
[^1_6]: https://code.claude.com/docs/en/memory
[^1_7]: https://www.letanure.dev/blog/2025-07-31--claude-code-part-2-claude-md-configuration
[^1_8]: https://www.youtube.com/watch?v=Cb2M5Ang70s
[^1_9]: https://rosmur.github.io/claudecode-best-practices/
[^1_10]: https://www.maxitect.blog/posts/maximising-claude-code-building-an-effective-claudemd
[^1_11]: https://www.builder.io/blog/claude-md-guide
[^1_12]: https://www.anthropic.com/engineering/claude-code-best-practices
[^1_13]: https://dometrain.com/blog/creating-the-perfect-claudemd-for-claude-code/
[^1_14]: https://blog.huikang.dev/2025/05/31/writing-claude-md.html
[^1_15]: https://www.claude.com/blog/using-claude-md-files
[^1_16]: https://m.academy/lessons/initialize-create-claudemd-file-claude-code/
[^1_17]: https://blog.yigitkonur.com/writing-the-best-claude-md-applying-best-patterns-to-guide-claude-code-to-do-its-best/
[^1_18]: https://code.claude.com/docs/en/settings
[^1_19]: https://www.curiouslychase.com/tools/how-to-modify-approvals-in-claude-code
[^1_20]: https://www.curiouslychase.com/posts/how-to-modify-approvals-in-claude-code
[^1_21]: https://claudelog.com/faqs/how-to-set-claude-code-permission-mode/
[^1_22]: https://blog.sshh.io/p/how-i-use-every-claude-code-feature
[^1_23]: https://www.reddit.com/r/ClaudeAI/comments/1ldugmg/this_is_why_claude_code_sometimes_ignore_your/
[^1_24]: https://www.youtube.com/watch?v=05igl7qCXLY
[^1_25]: https://dev.to/siddhantkcode/an-easy-way-to-stop-claude-code-from-forgetting-the-rules-h36
[^1_26]: https://milvus.io/ai-quick-reference/what-are-the-token-limits-for-claude-code
[^1_27]: https://www.datastudios.org/post/claude-ai-context-window-token-limits-and-memory-operational-boundaries-and-long-context-behavior
[^1_28]: https://claudelog.com/claude-code-limits/
[^1_29]: https://www.claudecode.io/guides/context-management
[^1_30]: https://claudecode.io/guides/context-management
[^1_31]: https://www.reddit.com/r/ClaudeAI/comments/1j9ehwb/my_claude_code_wishlist/
[^1_32]: https://www.reddit.com/r/ClaudeAI/comments/1o1yj6o/whats_the_best_way_to_have_cc_ignore_files/
[^1_33]: https://www.claude.com/blog/context-management
[^1_34]: https://www.cursor-ide.com/blog/claude-code-subagents
[^1_35]: https://www.richsnapp.com/article/2025/10-05-context-management-with-subagents-in-claude-code
[^1_36]: https://www.linkedin.com/pulse/understanding-claude-code-sub-agents-when-use-them-michael-hofer-rz9le
[^1_37]: https://aiengineerguide.com/blog/claude-code-custom-command/
[^1_38]: https://cloudartisan.com/posts/2025-04-14-claude-code-tips-slash-commands/
[^1_39]: https://m.academy/lessons/create-custom-slash-command-claude-code/
[^1_40]: https://www.reddit.com/r/ClaudeAI/comments/1noyvmq/claude_code_can_invoke_your_custom_slash_commands/
[^1_41]: https://platform.claude.com/docs/en/agent-sdk/subagents
[^1_42]: https://www.infoq.com/news/2025/08/claude-code-subagents/
[^1_43]: https://thomaslandgraf.substack.com/p/context-engineering-for-claude-code
[^1_44]: https://www.codecademy.com/article/how-to-use-model-context-protocol-mcp-with-claude-step-by-step-guide-with-examples
[^1_45]: https://www.eesel.ai/blog/mcp-integration-claude-code
[^1_46]: https://code.claude.com/docs/en/mcp
[^1_47]: https://github.com/majkonautic/claude-code-mcp-guide
[^1_48]: https://www.linkedin.com/posts/maecapozzi_over-the-past-few-months-ive-been-exploring-activity-7337853668349685762-vets
[^1_49]: https://alabeduarte.com/context-engineering-with-claude-code-my-evolving-workflow/
[^1_50]: https://www.eesel.ai/blog/claude-code-configuration
[^1_51]: https://milvus.io/ai-quick-reference/can-i-collaborate-with-teammates-using-claude-code
[^1_52]: https://www.reddit.com/r/ClaudeCode/comments/1p1w2vk/how_i_use_claude_code_effectively_in_real/
[^1_53]: https://www.reddit.com/r/ClaudeAI/comments/1i4c6jx/my_guide_to_using_styles_effectively/
[^1_54]: https://tessl.io/blog/claude-code-now-lets-you-customize-its-communication-style/
[^1_55]: https://code.claude.com/docs/en/output-styles
[^1_56]: https://www.anthropic.com/news/claude-code-on-team-and-enterprise
[^1_57]: https://www.mintmcp.com/blog/claude-code-security
[^1_58]: https://www.datastudios.org/post/claude-enterprise-security-configurations-and-deployment-controls-explained
[^1_59]: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-4-best-practices
[^1_60]: https://claude.com/blog/using-claude-md-files
[^1_61]: https://www.humanlayer.dev/blog/writing-a-good-claude-md
[^1_62]: https://www.reddit.com/r/ClaudeAI/comments/1km9hhp/latest_rules_for_claude_code/
[^1_63]: https://gizin.co.jp/en/tips/claude-code-permissions-settings
[^1_64]: https://www.reddit.com/r/ClaudeAI/comments/1n83nj5/permission_issue_with_claude_code/
[^1_65]: https://www.reddit.com/r/ClaudeAI/comments/1lol9rd/does_anyone_know_the_actual_token_limits_for/
[^1_66]: https://www.eesel.ai/blog/claude-code-permissions
[^1_67]: https://www.datastudios.org/post/claude-context-window-token-limits-memory-policy-and-2025-rules
[^1_68]: https://www.reddit.com/r/ClaudeAI/comments/1osk39n/comment/nnxmqzs/
[^1_69]: https://www.reddit.com/r/ClaudeAI/comments/1nv2qlr/claude_code_why_is_my_claudesettingsjson/
[^1_70]: https://www.youtube.com/watch?v=Ils94El3sEw
[^1_71]: https://cloudartisan.com/posts/2025-04-16-claude-code-tips-memory/
[^1_72]: https://www.aidevflow.com/claude-code-memory
[^1_73]: https://www.brandoncasci.com/2025/07/30/from-chaos-to-control-teaching-claude-code-consistency.html
[^1_74]: https://www.docstring.fr/blog/les-5-commandes-indispensables-pour-claude-code/
[^1_75]: https://github.com/anthropics/claude-code/issues/18964
[^1_76]: https://www.youtube.com/watch?v=i_OHQH4-M2Y&vl=fr
[^1_77]: https://code.claude.com/docs/en/model-config
[^1_78]: https://code.claude.com/docs/fr/mcp
[^1_79]: https://www.linkedin.com/posts/curiouslychase_claude-code-pro-tip-instead-of-adding-individual-activity-7377708837451202560-bw4t
[^1_80]: https://www.linkedin.com/posts/john-mikhail_i-used-claude-code-all-the-wrong-ways-so-activity-7374168091905277952-M_Zk
[^1_81]: https://www.cometapi.com/managing-claude-codes-context/
[^1_82]: https://www.petefreitag.com/blog/claude-code-permissions/
[^1_83]: https://sparkco.ai/blog/mastering-claudes-context-window-a-2025-deep-dive
[^1_84]: https://platform.claude.com/docs/en/agent-sdk/slash-commands
[^1_85]: https://www.nathanonn.com/how-to-build-comprehensive-project-rules-with-claude-code/
[^1_86]: https://skywork.ai/blog/how-to-generate-documentation-unit-tests-claude-code-plugin/
[^1_87]: https://www.claudecode.io/tutorials/claude-md-setup
[^1_88]: https://code.claude.com/docs/en/common-workflows
[^1_89]: https://code.claude.com/docs/en/overview
[^1_90]: https://smartscope.blog/en/generative-ai/claude/claude-code-control-best-practices/
[^1_91]: https://apidog.com/fr/blog/claude-code-cheatsheet-fr/
[^1_92]: https://www.reddit.com/r/ClaudeAI/comments/1mx255o/a_brief_guide_to_setting_up_claude_code_from/
[^1_93]: https://www.eesel.ai/blog/claude-code-best-practices
[^1_94]: https://github.com/hesreallyhim/awesome-claude-code
[^1_95]: https://dev.to/dzianiskarviha/integrating-claude-code-into-production-workflows-lbn
[^1_96]: https://support.claude.com/en/articles/11845131-using-claude-code-with-your-team-or-enterprise-plan
[^1_97]: https://leadershiplighthouse.substack.com/p/how-i-built-a-production-app-with
[^1_98]: https://hieufromwaterloo.ca/post/claude-code-complete-guide/
[^1_99]: https://www.claudecode101.com/en/tutorial/configuration/claude-md
[^1_100]: https://blissframework.dev/claude/
[^1_101]: https://harper.blog/2025/05/08/basic-claude-code/
[^1_102]: https://claude.ai/public/artifacts/77364999-2624-44a6-90bf-7513d8eeb675
[^1_103]: https://mcpmarket.com/tools/skills/documentation-structure
[^1_104]: https://www.youtube.com/watch?v=ubicvQ1ykY4
[^1_105]: https://github.com/kjnez/claude-code-django```

