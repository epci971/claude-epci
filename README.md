# EPCI Plugin — Claude Code

> **Version** : 4.2.0
> **License** : MIT

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
| `/epci:quick`  | Workflow condensé pour features TINY/SMALL                         |
| `/epci:spike`  | Exploration time-boxée pour incertitudes techniques                |
| `/epci:create` | Component Factory — Créer skills, commands, subagents              |

### Commandes Additionnelles

| Commande           | Description                                    |
| ------------------ | ---------------------------------------------- |
| `/epci:brainstorm` | Découverte de feature avec personas adaptatifs |
| `/epci:debug`      | Diagnostic structuré de bugs avec thought tree |
| `/epci:decompose`  | Décomposition de PRD/CDC en sous-specs         |
| `/epci:memory`     | Gestion de la mémoire projet                   |
| `/epci:learn`      | Gestion du système d'apprentissage continu     |

## Workflow

```
Brief utilisateur
       │
       ▼
┌──────────────┐
│ /epci:brief  │  ← Point d'entrée unique
└──────┬───────┘
       │
       ├─► TINY/SMALL ──► /epci:quick
       │
       ├─► STANDARD ────► /epci:epci (3 phases)
       │
       ├─► LARGE ───────► /epci:epci --large
       │
       └─► SPIKE ───────► /epci:spike
```

## Features v4.2

### Renommage commandes (v4.2)

Les commandes ont été simplifiées : le préfixe `epci-` a été supprimé.

- `/epci:epci-brief` → `/epci:brief`
- `/epci:epci-quick` → `/epci:quick`
- `/epci:epci-spike` → `/epci:spike`
- etc.

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
├── commands/          # 10 commandes
├── agents/            # 6 subagents custom
├── skills/            # 23 skills
│   ├── core/         # Skills fondamentaux
│   ├── stack/        # Skills par technologie
│   ├── factory/      # Component Factory
│   ├── mcp/          # MCP Integration
│   └── personas/     # Système de personas
├── hooks/            # Système de hooks
├── mcp/              # Module MCP Python
├── orchestration/    # Wave orchestration
└── project-memory/   # Gestion mémoire projet
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

### v4.2.0 (2024-12)

- Renommage des commandes : suppression du préfixe `epci-`
    - `/epci:epci-brief` → `/epci:brief`
    - `/epci:epci-quick` → `/epci:quick`
    - `/epci:epci-spike` → `/epci:spike`
    - `/epci:epci-debug` → `/epci:debug`
    - `/epci:epci-decompose` → `/epci:decompose`
    - `/epci:epci-memory` → `/epci:memory`
    - `/epci:epci-learn` → `/epci:learn`

### v4.1.0 (2024-12)

- F13: Flag `--turbo` pour workflows 30-50% plus rapides

### v4.0.0 (2024-12)

- F12: MCP Integration (Context7, Sequential, Magic, Playwright)
- F11: Wave Orchestration pour features LARGE
- F09: Système de Personas avec auto-activation
- Nouvelles commandes: `/brainstorm`, `/debug`, `/decompose`

### v3.2.0

- F09: Personas système initial
- F08: Apprentissage continu
- F07: Orchestration multi-agents

### v3.0.0

- Refonte complète avec 5 commandes principales
- Component Factory
- Project Memory

## License

MIT License - voir [LICENSE](LICENSE) pour plus de détails.
