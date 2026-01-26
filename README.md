# EPCI Plugin — Claude Code

> **Version** : 6.0.0
> **License** : MIT
> **Last Audit** : 2025-01-26 (Score: 85/100)

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

## Skills Principaux

Depuis Claude Code 2.1.19, les skills sont auto-invocables via `/skill-name`.

| Skill          | Description                                                        |
| -------------- | ------------------------------------------------------------------ |
| `/brainstorm`  | Découverte de feature avec personas adaptatifs + spike intégré     |
| `/spec`        | Création de spécifications (PRD/CDC)                               |
| `/implement`   | Workflow complet 3 phases pour features STANDARD/LARGE             |
| `/quick`       | Workflow condensé pour features TINY/SMALL                         |
| `/debug`       | Diagnostic structuré de bugs avec thought tree                     |
| `/improve`     | Amélioration de code existant                                      |
| `/refactor`    | Restructuration de code                                            |
| `/factory`     | Component Factory — Créer skills et subagents                      |

### Skills Additionnels

| Skill                 | Description                                    |
| --------------------- | ---------------------------------------------- |
| `/ralph`              | Exécution autonome overnight avec circuit breaker |
| `/decompose`          | Décomposition de PRD/CDC en sous-specs         |
| `/memory`             | Gestion de la mémoire projet + learning        |
| `/rules`              | Génération .claude/rules/ conventions projet   |
| `/promptor`           | Voice-to-brief + export Notion                 |

## Workflow

```
Brief utilisateur
       │
       ▼
┌──────────────┐
│ /brainstorm  │  ← Exploration optionnelle
└──────┬───────┘
       │
       ▼
┌──────────────┐
│   /spec      │  ← Création spécifications
└──────┬───────┘
       │
       ├─► TINY/SMALL ──► /quick ──────┐
       │                                │
       └─► STANDARD ────► /implement ──┘
                                        │
                                        ▼
                                   Code + Tests
```

### Workflow Complet (STANDARD/LARGE)

```
/brainstorm (optionnel)
       │
       ▼
/spec → PRD/CDC créé
       │
       ▼
/implement Phase 1 → Plan validé par @plan-validator
       │
       ▼
/implement Phase 2 → Code reviewé par @code-reviewer
       │
       ▼
/implement Phase 3 → Documentation + Tests
       │
       ▼
Git commit + PR ready
```

## Features v6.0.0

### Nouveautés v6.0.0 — Skills Auto-Invocables

- **Suppression des commandes** : Les skills sont maintenant directement invocables via `/skill-name`
- **Architecture simplifiée** : Plus de couche de redirection commands → skills
- **Factory amélioré** : Ne génère plus de fichiers de commandes
- **Validation allégée** : Script de validation simplifié (3 étapes au lieu de 4)

### Ralph Wiggum Integration (v5.1)

- **`/ralph` skill** : Exécution autonome overnight avec boucle itérative
- **Circuit Breaker** : Pattern 3 états pour détection automatique des boucles bloquées
- **RALPH_STATUS Block** : Format structuré de communication avec double condition de sortie
- **Deux modes** : Hook (même session, <2h) et Script (contexte frais, overnight)

### Sécurité

- **Input validation** : Protection injection dans response_analyzer.sh
- **File locking** : flock pour opérations atomiques dans circuit_breaker.sh
- **Rate limiting** : 100 appels/heure configurable

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
├── agents/            # 16 subagents (7 core + 3 turbo + 5 brainstorm + 1 ralph)
├── skills/            # 30 skills
│   ├── core/         # 18 skills fondamentaux
│   ├── stack/        # 5 skills par technologie
│   ├── factory/      # 4 skills Component Factory
│   ├── mcp/          # 1 skill MCP Integration
│   ├── personas/     # 1 skill Système de personas
│   └── promptor/     # 1 skill Voice-to-brief
├── scripts/          # Scripts Python et bash
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

### v6.0.0 (2025-01) — Current

- **Suppression des commandes** : Skills auto-invocables via Claude Code 2.1.19
- **Architecture simplifiée** : Plus de couche commands/
- **Factory allégé** : Ne génère plus de commandes
- **Validation simplifiée** : 3 étapes au lieu de 4
- **Totaux** : 16 agents, 30 skills

### v5.1.0 (2025-01)

- **Ralph Wiggum Integration** : Exécution autonome overnight
- **Nouveaux skills** : `ralph-analyzer`, `ralph-converter`
- **Nouvel agent** : `@ralph-executor`
- **Circuit Breaker** : Pattern robustesse pour détection stagnation
- **Sécurité** : Input validation, file locking avec flock

### v5.0.0 (2025-01)

- **`/orchestrate`** : Orchestration batch avec DAG, priority sorting
- **Chaîne complète** : `/brainstorm` → `/decompose` → `/orchestrate`
- **Nouveau skill** : `orchestrator-batch`

### v4.9.x (2024-12)

- **Brainstorm v5.0** : Expert panel, party orchestrator, rule clarifier
- **Native Plan Integration** : Import plan Claude Code natif
- **Auto-techniques** : Sélection automatique basée sur axes EMS faibles

### v4.4.0 (2024-12)

- **Fusion learn → memory** : `/learn` supprimé, learning intégré dans `/memory`
- **Ajout `/commit`** : Commande dédiée pour finalisation git
- **3 nouveaux agents turbo** : `@clarifier`, `@planner`, `@implementer`

### v4.x

- MCP Integration (Context7, Sequential, Magic, Playwright)
- Wave Orchestration pour features LARGE
- Système de Personas avec auto-activation
- Commandes: `/brainstorm`, `/debug`, `/decompose`

### v3.x

- Component Factory et Project Memory
- Orchestration multi-agents
- Apprentissage continu

## License

MIT License - voir [LICENSE](LICENSE) pour plus de détails.
