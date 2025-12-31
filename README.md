# EPCI Plugin — Claude Code

> **Version** : 4.4.0
> **License** : MIT
> **Last Audit** : 2024-12-31 (Score: 70/100)

EPCI (Explore → Plan → Code → Inspect) est un plugin Claude Code qui structure le développement logiciel en phases distinctes avec validation à chaque étape.

## Installation

1. Cloner le repository dans votre répertoire de plugins Claude Code :

    ```bash
    git clone https://github.com/epci/claude-epci.git ~/.claude/plugins/epci
    ```

2. Le plugin est automatiquement chargé au démarrage de Claude Code.

## Quick Start

### Premier Feature en 3 étapes

**Étape 1** — Démarrer avec `/epci:brief`

```
/epci:brief Ajouter une fonctionnalité de recherche utilisateurs
```

EPCI analyse votre codebase, pose des questions de clarification, évalue la complexité et vous route vers le workflow approprié.

**Étape 2** — Suivre le workflow recommandé

- **TINY/SMALL** → `/epci:quick` : Implémentation directe
- **STANDARD** → `/epci:epci` : 3 phases avec Feature Document
- **Incertain** → `/epci:spike` : Exploration time-boxée

**Étape 3** — Valider aux breakpoints
Chaque phase se termine par un breakpoint. Tapez `Continuer` pour avancer ou demandez des ajustements.

### Exemple complet (Feature STANDARD)

```bash
# 1. Brief
/epci:brief Ajouter un endpoint REST pour la recherche utilisateurs

# 2. EPCI évalue → STANDARD → crée Feature Document
#    Vous êtes routé vers /epci:epci

# 3. Phase 1: Planification
#    → Breakpoint: Valider le plan

# 4. Phase 2: Code
#    → Breakpoint: Review code

# 5. Phase 3: Finalisation
#    → Commit + PR ready
```

### Initialiser Project Memory (recommandé)

```bash
/epci:memory init
```

Cela active l'apprentissage continu, détecte votre stack et vos conventions.

## Commandes Principales

| Commande       | Description                                                        |
| -------------- | ------------------------------------------------------------------ |
| `/epci:brief`  | Point d'entrée — Exploration, clarification, évaluation complexité |
| `/epci:epci`   | Workflow complet 3 phases pour features STANDARD/LARGE             |
| `/epci:quick`  | Workflow EPCT condensé pour features TINY/SMALL                    |
| `/epci:commit` | Finalisation git avec contexte EPCI                                |
| `/epci:create` | Component Factory — Créer skills, commands, subagents              |

### Commandes Additionnelles

| Commande           | Description                                    |
| ------------------ | ---------------------------------------------- |
| `/epci:brainstorm` | Découverte de feature avec personas adaptatifs + spike intégré |
| `/epci:debug`      | Diagnostic structuré de bugs avec thought tree |
| `/epci:decompose`  | Décomposition de PRD/CDC en sous-specs         |
| `/epci:memory`     | Gestion de la mémoire projet + learning        |

## Workflow

```
Brief utilisateur
       │
       ▼
┌──────────────┐
│ /epci:brief  │  ← Point d'entrée unique
└──────┬───────┘
       │
       ├─► TINY/SMALL ──► /epci:quick ──┐
       │                                 │
       ├─► STANDARD ────► /epci:epci ───┼──► /epci:commit
       │                                 │
       └─► LARGE ───────► /epci:epci ───┘
                          --large
```

### Workflow Complet (STANDARD/LARGE)

```
/brainstorm (optionnel)
       │
       ▼
/brief → Feature Document §1
       │
       ▼
/epci Phase 1 → §2 (Plan validé par @plan-validator)
       │
       ▼
/epci Phase 2 → §3 (Code reviewé par @code-reviewer)
       │
       ▼
/epci Phase 3 → Documentation + contexte commit
       │
       ▼
/commit → Git commit + PR ready
```

## Features v4.4

### Nouveautés v4.4

- **9 subagents** : 6 core + 3 turbo (`@clarifier`, `@planner`, `@implementer`)
- **9 commandes** : Ajout de `/commit` pour finalisation git
- **Hooks obligatoires** : Garantie de mise à jour mémoire projet
- **Audit de cohérence** : Prompt réutilisable dans `docs/audits/`

### Commandes simplifiées (v4.2+)

Les commandes utilisent le format simplifié : `/epci:brief`, `/epci:quick`, etc.

### Personas (F09)

6 modes de pensée globaux avec auto-activation basée sur scoring :

- 🏗️ Architect — System thinking, patterns
- 🎨 Frontend — UI/UX, accessibility
- ⚙️ Backend — APIs, data integrity
- 🔒 Security — Threat modeling, OWASP
- 🧪 QA — Tests, edge cases
- 📝 Doc — Documentation, clarity

### MCP Integration (F12)

4 serveurs Model Context Protocol :

- **Context7** — Documentation librairies
- **Sequential** — Raisonnement multi-étapes
- **Magic** — Génération UI (21st.dev)
- **Playwright** — Tests E2E, browser automation

### Wave Orchestration (F11)

Exécution parallèle des agents via DAG pour features LARGE.

### Project Memory

Mémoire persistante par projet :

- Conventions et patterns détectés
- Historique des features
- Métriques de vélocité
- Apprentissage continu

## Flags

### Thinking

| Flag           | Effet               |
| -------------- | ------------------- |
| `--think`      | Analyse standard    |
| `--think-hard` | Analyse approfondie |
| `--ultrathink` | Analyse critique    |

### MCP

| Flag       | Effet                   |
| ---------- | ----------------------- |
| `--c7`     | Active Context7         |
| `--seq`    | Active Sequential       |
| `--magic`  | Active Magic            |
| `--play`   | Active Playwright       |
| `--no-mcp` | Désactive tous les MCPs |

### Personas

| Flag                  | Effet              |
| --------------------- | ------------------ |
| `--persona-architect` | Mode architecte    |
| `--persona-frontend`  | Mode frontend      |
| `--persona-backend`   | Mode backend       |
| `--persona-security`  | Mode sécurité      |
| `--persona-qa`        | Mode QA            |
| `--persona-doc`       | Mode documentation |

## Structure du Plugin

```
src/
├── commands/          # 9 commandes
├── agents/            # 9 subagents (6 core + 3 turbo)
├── skills/            # 23 skills
│   ├── core/         # 13 skills fondamentaux
│   ├── stack/        # 4 skills par technologie
│   ├── factory/      # 4 skills Component Factory
│   ├── mcp/          # 1 skill MCP Integration
│   └── personas/     # 1 skill Système de personas
├── hooks/            # Système de hooks
├── mcp/              # Module MCP Python
├── orchestration/    # Wave orchestration
└── project-memory/   # Gestion mémoire projet

docs/
├── audits/           # Audits de cohérence
├── briefs/           # Briefs features
└── features/         # Feature Documents
```

## Configuration

### Project Memory

Initialiser la mémoire projet :

```bash
/epci:memory init
```

### MCP (optionnel)

Configuration dans `.project-memory/settings.json` :

```json
{
    "mcp": {
        "enabled": true,
        "servers": {
            "context7": { "enabled": true },
            "sequential": { "enabled": true },
            "magic": { "enabled": true },
            "playwright": { "enabled": true }
        }
    }
}
```

## Documentation

- [CLAUDE.md](CLAUDE.md) — Documentation développeur complète
- [docs/](docs/) — Spécifications et guides

## Validation

Exécuter la suite de validation :

```bash
python3 src/scripts/validate_all.py
```

## Changelog

### v4.4.0 (2024-12)

- **Fusion learn → memory** : `/learn` supprimé, learning intégré dans `/memory`
- **Ajout `/commit`** : Commande dédiée pour finalisation git
- **3 nouveaux agents turbo** : `@clarifier`, `@planner`, `@implementer`
- **Hooks obligatoires documentés** : Section 11 dans CLAUDE.md
- **Fusion spike → brainstorm** : Exploration technique intégrée
- **Audit de cohérence** : Prompt d'audit dans `docs/audits/AUDIT_PROMPT.md`

### v4.2.0 (2024-12)

- Renommage des commandes : suppression du préfixe `epci-`
    - `/epci:epci-brief` → `/epci:brief`
    - `/epci:epci-quick` → `/epci:quick`
    - etc.

### v4.1.0 (2024-12)

- F13: Flag `--turbo` pour workflows 30-50% plus rapides

### v4.0.0 (2024-12)

- F12: MCP Integration (Context7, Sequential, Magic, Playwright)
- F11: Wave Orchestration pour features LARGE
- F09: Système de Personas avec auto-activation
- Nouvelles commandes: `/brainstorm`, `/debug`, `/decompose`

### v3.x

- F09: Personas système initial
- F08: Apprentissage continu
- F07: Orchestration multi-agents
- Refonte complète avec Component Factory et Project Memory

## License

MIT License - voir [LICENSE](LICENSE) pour plus de détails.
