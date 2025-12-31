# EPCI Plugin — Claude Code Development Assistant

> **Version** : 4.2.0 | **Date** : Décembre 2024

---

## 1. Overview

EPCI (Explore → Plan → Code → Inspect) structure le développement en phases avec validation à chaque étape.

### Philosophie v4

| Principe            | Description                                                   |
| ------------------- | ------------------------------------------------------------- |
| **Simplicité**      | 10 commandes spécialisées                                     |
| **Modularité**      | Skills, Subagents, Hooks natifs                               |
| **Traçabilité**     | Feature Document comme fil rouge                              |
| **MCP Integration** | 4 serveurs externes (Context7, Sequential, Magic, Playwright) |

### Nouveautés v4.2

- **Renommage commandes** : Préfixe `epci-` supprimé (ex: `/epci:brief` au lieu de `/epci:epci-brief`)
- **MCP Integration** : Context7 (docs), Sequential (reasoning), Magic (UI), Playwright (E2E)
- **Auto-activation MCP** : Basée sur personas et contexte
- **Flags MCP** : `--c7`, `--seq`, `--magic`, `--play`, `--no-mcp`
- **6 Personas** : Architect, Frontend, Backend, Security, QA, Doc

---

## 2. Repository Structure

```
src/
├── agents/           # 6 subagents (code-reviewer, plan-validator, etc.)
├── commands/         # 10 commandes (brief, epci, quick, etc.)
├── hooks/            # Système hooks (runner.py, examples/, active/)
├── mcp/              # MCP Integration (config, activation, registry)
├── orchestration/    # Wave orchestration
├── scripts/          # Validation (validate_all.py, etc.)
├── settings/         # Configuration (flags.md)
└── skills/           # 23 skills
    ├── core/         # 13 skills fondamentaux
    ├── stack/        # 4 skills technologie (react, django, symfony, spring)
    ├── personas/     # Système personas
    ├── mcp/          # MCP skill
    └── factory/      # Component Factory (4 skills)

docs/                 # Documentation détaillée
build/                # Production v2.7 (référence)
archive/              # Versions dépréciées
```

---

## 3. Core Workflow

### Routing par complexité

```
Brief brut → /brief → Évaluation
                        │
       ┌────────────────┼────────────────┐
       ▼                ▼                ▼
  TINY/SMALL        STD/LARGE         SPIKE
    /quick            /epci           /spike
```

| Catégorie    | Critères                            | Workflow           |
| ------------ | ----------------------------------- | ------------------ |
| **TINY**     | 1 fichier, < 50 LOC                 | `/quick`           |
| **SMALL**    | 2-3 fichiers, < 200 LOC             | `/quick`           |
| **STANDARD** | 4-10 fichiers, tests requis         | `/epci` (3 phases) |
| **LARGE**    | 10+ fichiers, architecture complexe | `/epci --large`    |
| **SPIKE**    | Incertitude technique               | `/spike`           |

### Feature Document (STD/LARGE)

```markdown
# Feature Document — [Titre]

## §1 — Brief Fonctionnel ← /brief

## §2 — Plan d'Implémentation ← /epci Phase 1

## §3 — Implementation ← /epci Phases 2-3
```

---

## 4. Commands (10)

| Commande      | Rôle                                                        |
| ------------- | ----------------------------------------------------------- |
| `/brief`      | Point d'entrée unique — exploration, clarification, routing |
| `/epci`       | Workflow complet 3 phases (STD/LARGE)                       |
| `/quick`      | Workflow condensé (TINY/SMALL)                              |
| `/spike`      | Exploration time-boxée                                      |
| `/brainstorm` | Feature discovery avec personas                             |
| `/debug`      | Diagnostic bugs structuré                                   |
| `/decompose`  | Décomposition PRD en sous-specs                             |
| `/memory`     | Gestion mémoire projet                                      |
| `/learn`      | Gestion apprentissage                                       |
| `/create`     | Component Factory (skill\|command\|agent)                   |

---

## 5. Subagents (6)

| Subagent               | Rôle                       | Invoqué par     |
| ---------------------- | -------------------------- | --------------- |
| `@plan-validator`      | Valide plan avant Phase 2  | `/epci` Phase 1 |
| `@code-reviewer`       | Revue qualité code         | `/epci` Phase 2 |
| `@security-auditor`    | Audit OWASP (conditionnel) | `/epci` Phase 2 |
| `@qa-reviewer`         | Revue tests (conditionnel) | `/epci` Phase 2 |
| `@doc-generator`       | Génération documentation   | `/epci` Phase 3 |
| `@decompose-validator` | Valide décomposition PRD   | `/decompose`    |

---

## 6. Skills (23)

### Core (13)

`epci-core`, `architecture-patterns`, `code-conventions`, `testing-strategy`,
`git-workflow`, `flags-system`, `project-memory`, `brainstormer`,
`debugging-strategy`, `learning-optimizer`, `breakpoint-metrics`,
`clarification-intelligente`, `proactive-suggestions`

### Stack (4) — Auto-détectés

| Skill              | Détection                             |
| ------------------ | ------------------------------------- |
| `php-symfony`      | `composer.json`                       |
| `javascript-react` | `package.json` + react                |
| `python-django`    | `requirements.txt` / `pyproject.toml` |
| `java-springboot`  | `pom.xml` / `build.gradle`            |

### Personas (1) + MCP (1) + Factory (4)

---

## 7. Personas & MCP

### 6 Personas (auto-activation si score > 0.6)

| Persona      | Focus                     | Flag                  |
| ------------ | ------------------------- | --------------------- |
| 🏗️ Architect | System thinking, patterns | `--persona-architect` |
| 🎨 Frontend  | UI/UX, accessibility      | `--persona-frontend`  |
| ⚙️ Backend   | APIs, data integrity      | `--persona-backend`   |
| 🔒 Security  | OWASP, compliance         | `--persona-security`  |
| 🧪 QA        | Tests, coverage           | `--persona-qa`        |
| 📝 Doc       | Documentation             | `--persona-doc`       |

### 4 MCP Servers

| Server     | Function                  | Flags     |
| ---------- | ------------------------- | --------- |
| Context7   | Documentation librairies  | `--c7`    |
| Sequential | Raisonnement multi-étapes | `--seq`   |
| Magic      | Génération UI (21st.dev)  | `--magic` |
| Playwright | Tests E2E                 | `--play`  |

**Désactiver tous** : `--no-mcp`

---

## 8. Flags Universels

| Catégorie   | Flags                                           |
| ----------- | ----------------------------------------------- |
| Thinking    | `--think`, `--think-hard`, `--ultrathink`       |
| Compression | `--uc`, `--verbose`                             |
| Workflow    | `--safe`, `--no-hooks`, `--large`, `--continue` |
| Wave        | `--wave`, `--wave-strategy`                     |

**Auto-activation** :

- Fichiers > 10 → `--think-hard`
- Context > 75% → `--uc`
- Fichiers sensibles → `--safe`

---

## 9. Development Guidelines

### Conventions

| Élément   | Convention       | Exemple                |
| --------- | ---------------- | ---------------------- |
| Commandes | kebab-case.md    | `brief.md`             |
| Subagents | kebab-case.md    | `code-reviewer.md`     |
| Skills    | dossier/SKILL.md | `php-symfony/SKILL.md` |
| Scripts   | snake_case.py    | `validate_skill.py`    |

### Limites tokens

| Composant    | Limite        |
| ------------ | ------------- |
| Commandes    | < 5000 tokens |
| Skills       | < 5000 tokens |
| Subagents    | < 2000 tokens |
| Descriptions | ≤ 1024 chars  |

### Validation

```bash
# Valider tout
python src/scripts/validate_all.py

# Valider un composant spécifique
python src/scripts/validate_skill.py src/skills/core/epci-core/
python src/scripts/validate_command.py src/commands/brief.md
python src/scripts/validate_subagent.py src/agents/code-reviewer.md
```

---

## 10. Quick Reference

### Créer un composant

```bash
/epci:create skill mon-skill
/epci:create command ma-commande
/epci:create agent mon-agent
```

### Workflow type

```
1. /epci:brief "description feature"
2. → Routing automatique vers /epci:quick ou /epci:epci
3. → Validation via subagents
4. → Feature Document complété
```

### Documentation détaillée

| Sujet             | Fichier                                                  |
| ----------------- | -------------------------------------------------------- |
| Spec complète v3  | `docs/migration/27-30/epci-v3-complete-specification.md` |
| Component Factory | `docs/migration/27-30/epci-component-factory-spec-v3.md` |
| Best practices    | `docs/Guide_Bonnes_Pratiques_Claude_Code_EPCI.md`        |
| Hooks             | `src/hooks/README.md`                                    |
| Flags             | `src/settings/flags.md`                                  |
| MCP               | `src/skills/mcp/SKILL.md`                                |
| Personas          | `src/skills/personas/SKILL.md`                           |
