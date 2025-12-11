# Guide Bonnes Pratiques Plugin Claude Code — Version EPCI

> **Version** : 1.0-lite  
> **Optimisé pour** : Plugin EPCI (base documentaire Claude Code)  
> **Source** : Guide complet (~185 Ko → ~30 Ko)

---

## TL;DR — Règles Essentielles

1. **Structure standard** : `.claude-plugin/plugin.json` + dossiers `commands/`, `agents/`, `skills/`, `hooks/`
2. **Manifest complet** : kebab-case, version sémantique, chemins relatifs `./`
3. **Un composant = un rôle** : ne pas mixer responsabilités
4. **Skills < 500 lignes** : progressive disclosure via références
5. **Descriptions précises** : "Use when X" + "Not for Y"
6. **Sécurité** : `allowed-tools` restrictif, pas de secrets en dur
7. **Tester le triggering** : explicite, implicite, hors périmètre
8. **Chemins Unix** : `/` partout, même Windows
9. **Versionner** : SemVer + changelog
10. **Modularité** : plusieurs plugins ciblés > 1 monolithe

---

## 1. Architecture Plugin

### Structure Standard

```
my-plugin/
├── .claude-plugin/
│   └── plugin.json        # Manifest (OBLIGATOIRE)
├── commands/              # Slash commands (.md)
├── agents/                # Subagents (.md)
├── skills/                # Skills (dossier/SKILL.md)
├── hooks/
│   └── hooks.json         # Configuration hooks
├── .mcp.json              # Serveurs MCP (optionnel)
└── scripts/               # Utilitaires
```

**Variables d'environnement** : `${CLAUDE_PLUGIN_ROOT}` = chemin absolu du plugin

### Manifest (plugin.json)

| Champ | Type | Description |
|-------|------|-------------|
| `name` | string | Identifiant kebab-case unique |
| `version` | string | SemVer (MAJOR.MINOR.PATCH) |
| `description` | string | Finalité du plugin |
| `author` | object | `{name, email, url}` |
| `homepage` | string | URL documentation |
| `license` | string | Ex: MIT, Apache-2.0 |
| `commands` | array | Chemins fichiers commandes |
| `agents` | array | Chemins fichiers agents |
| `hooks` | string | Chemin hooks.json |
| `mcpServers` | object | Config MCP |

**Règles** :
- Chemins relatifs commençant par `./`
- JSON valide (validator recommandé)
- Lister explicitement tous les composants

### Marketplace

```json
// marketplace.json
{
  "name": "mon-marketplace",
  "plugins": [
    {
      "name": "mon-plugin",
      "source": "./mon-plugin",
      "description": "Description courte"
    }
  ]
}
```

**Commandes** :
- `/plugin marketplace add <url>` — Ajouter marketplace
- `/plugin install <nom>` — Installer plugin

---

## 2. Slash Commands

### Structure Fichier (.md)

```yaml
---
description: Action courte en infinitif (~5-10 mots)
argument-hint: [param1] [param2]
allowed-tools: [Read, Grep, Bash(git:*)]
---

<objective>
But de la commande avec $ARGUMENTS
</objective>

<process>
1. Étape 1
2. Étape 2
3. Étape 3
</process>

<success_criteria>
- Critère de succès 1
- Critère de succès 2
</success_criteria>

<output>
- Fichiers générés/modifiés
</output>
```

### Balises Sémantiques

| Balise | Usage |
|--------|-------|
| `<objective>` | But global |
| `<context>` | État actuel, données |
| `<process>` / `<steps>` | Plan d'action |
| `<verification>` | Étapes vérification |
| `<output>` | Fichiers générés |
| `<success_criteria>` | Critères réussite |

### Arguments

- `$ARGUMENTS` — Tous les arguments
- `$1`, `$2`, ... — Arguments individuels
- `@fichier` — Inclure contenu fichier
- `!commande` — Inclure sortie commande shell

### allowed-tools (Sécurité)

```yaml
# Lecture seule
allowed-tools: [Read, Grep, Glob, LS]

# Git uniquement
allowed-tools: [Bash(git add:*), Bash(git commit:*), Bash(git push:*)]

# Développement
allowed-tools: [Read, Write, Edit, Bash(npm:*), Bash(yarn:*)]
```

**Pattern** : `Bash(command:*)` pour autoriser une famille de commandes

### Bonnes Pratiques

| ✅ Faire | ❌ Éviter |
|----------|----------|
| Nom explicite (`deploy.md`) | Nom vague (`helper.md`) |
| Description action infinitif | Description 1ère personne |
| Balises sémantiques structurées | Bloc de texte monolithique |
| Gérer arguments manquants | $ARGUMENTS vide = prompt confus |
| Limiter allowed-tools | Tout autoriser par défaut |

---

## 3. Subagents

### Définition

Instances Claude indépendantes avec contexte séparé pour délégation de tâches.

### Cas d'Usage

| Cas | Exemple |
|-----|---------|
| Parallélisation | Analyser plusieurs fichiers simultanément |
| Isolation contexte | Agent "Plan" → transmet plan au main agent |
| Spécialisation | Agent reviewer, debugger, test-writer |
| Tâches lourdes | Relire longs historiques sans surcharger main |

### Structure Fichier (.md)

```yaml
---
name: code-reviewer
description: Revue de code orientée qualité et sécurité
model: claude-sonnet  # optionnel
allowed-tools: [Read, Grep]
---

# Instructions Subagent

Tu es un expert en revue de code...
[Instructions spécialisées]
```

### Bonnes Pratiques

| ✅ Faire | ❌ Éviter |
|----------|----------|
| Tâche bien définie par agent | Agent fourre-tout |
| Outils limités à la mission | Tous les outils |
| Modèle adapté (Haiku pour tâches simples) | Opus pour tout |
| Retour synthétique au main agent | Retour verbeux |
| Autonomie (pas besoin user) | Dépendance utilisateur |

---

## 4. Hooks

### Événements Disponibles

| Événement | Déclencheur |
|-----------|-------------|
| `SessionStart` | Démarrage session Claude Code |
| `PreToolUse` | Avant exécution outil (Read, Write, Bash...) |
| `PostToolUse` | Après exécution outil |

### Structure (hooks.json)

```json
{
  "hooks": [
    {
      "event": "PreToolUse",
      "matcher": {
        "toolName": "Bash",
        "command": "rm *"
      },
      "action": {
        "type": "script",
        "script": "./scripts/confirm-delete.sh"
      }
    }
  ]
}
```

### Types d'Actions

| Type | Usage |
|------|-------|
| `script` | Exécuter script shell/Python |
| `block` | Bloquer l'action |
| `allow` | Autoriser explicitement |
| `modify` | Modifier paramètres |

### Bonnes Pratiques

| ✅ Faire | ❌ Éviter |
|----------|----------|
| Matchers précis (toolName + command) | Matcher trop large |
| Scripts idempotents (ré-exécutables) | Scripts avec effets de bord |
| Gestion erreurs dans scripts | Exit sans code retour |
| Logs pour diagnostic | Aucune trace |
| Chemins relatifs `./scripts/` | Chemins absolus |

### Sécurité Hooks

⚠️ Les hooks s'exécutent avec les permissions utilisateur. Auditer tout script avant déploiement.

---

## 5. Skills

### Définition

Compétences auto-déclenchées par matching sémantique avec la conversation.

### Emplacements

| Niveau | Chemin | Priorité |
|--------|--------|----------|
| Plugin | `plugin/skills/` | Haute |
| Projet | `.claude/skills/` | Moyenne |
| Personnel | `~/.claude/skills/` | Basse |

### Structure

```
mon-skill/
├── SKILL.md           # Fichier principal (<500 lignes)
├── REFERENCE.md       # Détails (chargé à la demande)
└── scripts/           # Utilitaires
```

### Frontmatter SKILL.md

```yaml
---
name: git-commit-composer
description: >-
  Guides commit message writing following Conventional Commits.
  Auto-invoke when user mentions commit, commit message, or git history.
  Do NOT load for merge commits or rebasing discussions.
allowed-tools: [Read, Write]
---
```

### Formule Description

```
[Capacité] + [Auto-invoke WHEN...] + [Do NOT load for...]
```

### Bonnes Pratiques

| ✅ Faire | ❌ Éviter |
|----------|----------|
| Description WHEN/WHEN NOT | Description vague |
| SKILL.md < 500 lignes | Fichier monolithique |
| Progressive disclosure (références) | Tout dans un fichier |
| Un skill = un thème | Skill fourre-tout |
| Tester activation réelle | Skill "théorique" jamais testé |
| Écrire à la 3ème personne | "I can help you..." |
| Vocabulaire cohérent | Termes alternants |

### Anti-patterns

- Description trop générique ("Provides information")
- Infos volatiles/datées dans le skill
- YAML avec tabulations (→ espaces)
- Pas de test d'activation

---

## 6. MCP (Model Context Protocol)

### Définition

Serveurs d'outils externes étendant les capacités Claude.

### Configuration (.mcp.json)

```json
{
  "mcpServers": {
    "mon-service": {
      "command": "node",
      "args": ["./mcp-server.js"],
      "env": {
        "API_KEY": "${MCP_API_KEY}"
      }
    }
  }
}
```

### Bonnes Pratiques

| ✅ Faire | ❌ Éviter |
|----------|----------|
| 1-3 MCP ciblés | Multiplier les MCP |
| Logging côté serveur | Aucune observabilité |
| Gestion indisponibilité | Crash si MCP down |
| Secrets en env vars | Credentials en dur |
| `--mcp-debug` pour diagnostic | Debug à l'aveugle |

---

## 7. Personas

### Définition

Profils de comportement prédéfinis (Architecte, Sécurité, Pédagogue...).

### Implémentation

| Méthode | Description |
|---------|-------------|
| Flags | `--persona-architect` sur commandes |
| Skills | Skill activé par mot-clé persona |
| Subagents | Agent dédié par persona (lourd) |

### Bonnes Pratiques

| ✅ Faire | ❌ Éviter |
|----------|----------|
| 5 personas bien distinctes | 15 personas similaires |
| Ligne directrice claire par persona | Chevauchements |
| Activation explicite | Changement implicite |
| Retour au mode neutre facile | Persona "sticky" |
| Une seule persona active | Cumul incontrôlé |

---

## 8. Erreurs Fréquentes

### Manifest

| Erreur | Solution |
|--------|----------|
| JSON invalide | Validator JSON |
| Chemins absolus | `./` relatifs |
| Nom avec espaces | kebab-case |
| Version incohérente | SemVer strict |

### Commands

| Erreur | Solution |
|--------|----------|
| Prompt non structuré | Balises sémantiques |
| allowed-tools vide (risqué) | Limiter au nécessaire |
| Arguments non gérés | Valeurs par défaut |

### Skills

| Erreur | Solution |
|--------|----------|
| Description floue | WHEN/WHEN NOT explicite |
| Fichier trop gros | Progressive disclosure |
| YAML tabs | Espaces uniquement |
| Non testé | Tester activation |

### Hooks

| Erreur | Solution |
|--------|----------|
| Matcher trop large | Préciser toolName + command |
| Script non portable | Tester multi-OS |
| Pas de gestion erreurs | Try/catch, codes retour |

### MCP

| Erreur | Solution |
|--------|----------|
| Credentials en dur | Variables environnement |
| Pas de logs | Logger côté serveur |
| Dépendance forcée | Gérer indisponibilité |

---

## 9. Checklist Déploiement

### Structure
- [ ] `.claude-plugin/plugin.json` présent et valide
- [ ] Dossiers standard (`commands/`, `agents/`, `skills/`, `hooks/`)
- [ ] Chemins relatifs (`./`)
- [ ] Noms kebab-case

### Manifest
- [ ] `name` unique
- [ ] `version` SemVer
- [ ] `description` claire
- [ ] Tous composants déclarés

### Commands
- [ ] Description action infinitif
- [ ] Balises sémantiques
- [ ] `allowed-tools` restrictif
- [ ] Arguments documentés

### Skills
- [ ] Description WHEN/WHEN NOT
- [ ] < 500 lignes
- [ ] YAML valide (espaces, pas tabs)
- [ ] Test activation

### Hooks
- [ ] Matchers précis
- [ ] Scripts idempotents
- [ ] Gestion erreurs
- [ ] Logs

### Sécurité
- [ ] Pas de credentials en dur
- [ ] Scripts audités
- [ ] `allowed-tools` minimal
- [ ] MCP sécurisés

### Tests
- [ ] Triggering explicite ✓
- [ ] Triggering implicite ✓
- [ ] Hors périmètre (pas faux positif) ✓
- [ ] Multi-plateforme (Linux/Mac/Windows)

---

## 10. Recommandations EPCI

### Intégration Méthodologie

| Phase EPCI | Composants Plugin |
|------------|-------------------|
| **Explore** | Skills contexte projet, subagent analyseur |
| **Plan** | Command `/plan`, skill architecture |
| **Code** | Commands `/build`, `/test`, hooks qualité |
| **Inspect** | Subagent reviewer, skill checklist |

### Patterns Recommandés

1. **Skills pour contexte persistant** — Charger automatiquement les conventions projet
2. **Commands pour actions explicites** — `/explore`, `/plan`, `/code`, `/inspect`
3. **Hooks pour garde-fous** — Validation avant commit, tests avant push
4. **Subagents pour parallélisation** — Analyse multi-fichiers, revue approfondie

### Architecture Suggérée

```
epci-plugin/
├── .claude-plugin/
│   └── plugin.json
├── commands/
│   ├── explore.md
│   ├── plan.md
│   ├── code.md
│   └── inspect.md
├── agents/
│   ├── analyzer.md
│   └── reviewer.md
├── skills/
│   ├── project-context/
│   │   └── SKILL.md
│   ├── coding-standards/
│   │   └── SKILL.md
│   └── quality-checklist/
│       └── SKILL.md
├── hooks/
│   └── hooks.json
└── scripts/
    └── validators/
```

---

## Références Officielles

| Ressource | URL |
|-----------|-----|
| Plugins Reference | `https://code.claude.com/docs/en/plugins-reference` |
| Slash Commands | `https://code.claude.com/docs/en/slash-commands` |
| Hooks Guide | `https://code.claude.com/docs/en/hooks-guide` |
| Sub-agents | `https://code.claude.com/docs/en/sub-agents` |
| Best Practices | `https://www.anthropic.com/engineering/claude-code-best-practices` |

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0-lite | 2025-12-11 | Version optimisée EPCI (~85% réduction) |

## Current: v1.0-lite

**Author** : Édouard | **Optimisation** : Claude | **Décembre 2025**
