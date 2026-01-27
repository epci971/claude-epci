# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- **Script deploy.py**: Nouveau script de déploiement pour copier `src/` → `build/epci/` avec validation intégrée
  - Exclusions automatiques: `__pycache__/`, `*.pyc`, `tests/`
  - Import direct de `validate.py` pour validation post-copie
  - Vérification cohérence des versions (plugin.json vs README.md)
  - Rollback automatique si validation échoue
  - CLI: `--dry-run`, `--force`, `--verbose`, `--skip-version-check`
  - Exit codes explicites (0=success, 1=validation, 2=copy, 3=version)

## [5.6.0] - 2026-01-20

### Added

- **Skip [E][P] pour /quick avec plan natif**: Détection automatique → exécution directe [C][T]
- **Phase [PRE] dans /quick**: Nouvelle phase de détection avant [E]
- **Extraction tâches intelligente**: Supporte checkboxes, listes numérotées, headers, bullets
- **Exemple Fast Path**: Nouvel exemple dans documentation quick.md

### Changed

- **SMALL par défaut pour plan natif**: Plan natif implique complexité minimale → Sonnet
- **Workflow D mis à jour**: Documentation CLAUDE.md reflète le fast path
- **Diagramme workflow /quick**: Nouveau diagramme avec bifurcation [PRE]

## [5.5.0] - 2026-01-20

### Changed

- **Auto-détection plans natifs**: Suppression du flag `--from-native-plan`, détection automatique basée sur chemin `docs/plans/` ou frontmatter `saved_at`
- **Algorithme unifié**: `is_native_plan()` partagé entre `/brief`, `/epci` et `/quick`
- **Routing avec contexte**: Passage via `@<path>` au lieu de flag explicite
- **3 commandes mises à jour**: `/brief` (Step 0.5), `/epci` (Step 0.5), `/quick` (Phase [E])
- **Documentation renommée**: `native-plan-import.md` → `native-plan-detection.md`
- **Workflow simplifié**: `/save-plan` → `/brief @docs/plans/...` (ou direct `/epci`/`/quick`)

## [5.4.0] - 2026-01-19

### Added

- **Nouveau skill `perplexity-research`**: Recherche externe via Perplexity Pro (human-in-the-loop)
- **Nouveau type breakpoint `research-prompt`**: Affiche prompt copyable avec mode Standard/Deep Research
- **Intégration `/brief`**: Step 2.1 propose recherche si librairie externe ou architecture complexe
- **Intégration `/debug`**: Step 1.2.1 propose recherche si Context7/WebSearch insuffisants
- **Intégration `/brainstorm`**: Phase 1 (market analysis) + Phase 2 (axes faibles)
- **35 Skills**: Total passe de 34 à 35 skills
- **10 types breakpoints**: Ajout de `research-prompt` au système breakpoint-display

## [5.3.10] - 2026-01-18

### Fixed

- **Fix critique `/brief`**: Correction du bug où `/brief` basculait en mode plan natif au lieu de générer un Feature Document
- **Garde anti-plan-natif**: Nouvelle box ASCII de vérification obligatoire dans Step 5 de `/brief`
- **Règle globale CLAUDE.md**: Protection anti-EnterPlanMode ajoutée dans `~/.claude/CLAUDE.md`
- **Routing restauré**: Step 6 (routing vers `/quick` ou `/epci`) s'exécute correctement après Step 5

## [5.3.8] - 2026-01-17

### Changed

- **Intégration `complexity-calculator`**: Calcul complexité centralisé intégré dans `/brief`, `/quick`, `/decompose`, `/ralph-exec`
- **Intégration `tdd-workflow`**: Cycle TDD standardisé intégré dans `/epci`, `/quick`, `/ralph-exec`
- **Suggestions proactives par défaut**: `/brainstorm` affiche maintenant les suggestions automatiquement
- **Nouveau flag `--no-suggest`**: Remplace `--suggest` pour désactiver les suggestions (par défaut activées)
- **Références skills unifiées**: Toutes les commandes référencent les skills via `@skill:` invocations

## [5.3.7] - 2026-01-16

### Added

- **Discovery Mode pour /brainstorm**: Flag `--suggest` pour suggestions proactives
- **12 patterns discovery**: Catalogue de suggestions contextuelles (arch, security, ems-based)
- **Champ `suggestions[]`**: Nouveau champ dans breakpoint-display pour suggestions
- **Nouveau skill `complexity-calculator`**: Calcul centralisé complexité TINY/SMALL/STANDARD/LARGE
- **Nouveau skill `tdd-workflow`**: Cycle TDD standardisé RED-GREEN-REFACTOR-VERIFY
- **34 Skills**: Total passe de 32 à 34 skills

### Changed

- **Documentation clarifiée**: `input-clarifier` vs `clarification-intelligente` mieux documentés

## [5.3.6] - 2026-01-16

### Changed

- **Migration complète breakpoint-display**: Toutes les commandes EPCI utilisent maintenant le skill centralisé
- **6 commandes migrées**: `/debug`, `/decompose`, `/orchestrate`, `/commit`, `/save-plan`, `/quick`
- **12 breakpoints au total**: Tous migrés vers `@skill:breakpoint-display`
- **~70% économie tokens moyenne**: Breakpoints uniformisés via skill centralisé
- **Cohérence UI totale**: Toutes les commandes EPCI avec boutons natifs AskUserQuestion

## [5.3.5] - 2026-01-15

### Changed

- **Migration `/brainstorm` vers `breakpoint-display`**: 6 breakpoints migrés vers skill centralisé
- **Nouveau template `ems-status`**: Affichage EMS 5 axes avec barres de progression pour brainstorm
- **9 types de breakpoints**: validation, plan-review, analysis, decomposition, diagnostic, interactive-plan, lightweight, info-only, ems-status
- **~57% économie tokens**: Breakpoints brainstorm via skill au lieu de ASCII boxes manuelles
- **Cohérence UI complète**: `/brief`, `/epci` et `/brainstorm` utilisent maintenant le même système

## [5.3.4] - 2026-01-15

### Added

- **Nouveau skill `breakpoint-display`**: Système unifié pour affichage breakpoints interactifs
- **73% réduction tokens**: ~300 tokens/breakpoint → ~80 tokens via skill centralisé
- **AskUserQuestion natif**: UI Claude Code native avec boutons cliquables vs choix textuels
- **8 types de breakpoints**: validation, plan-review, analysis, decomposition, diagnostic, interactive-plan, lightweight, info-only
- **4 composants réutilisables**: metrics-block, validations-block, preview-block, flags-block
- **Migration /brief et /epci**: 4 breakpoints migrés vers nouveau système (Step 1, Step 4, BP1, BP2)
- **32 Skills**: Total des skills EPCI passe de 31 à 32

## [5.3.0] - 2026-01-15

### Added

- **Nouvelle commande `/save-plan`**: Sauvegarde les plans natifs Claude Code dans le projet
- **Auto-détection du plan**: Détecte automatiquement le dernier plan dans `~/.claude/plans/`
- **Auto-génération du slug**: Génère un slug intelligent basé sur le contenu du plan
- **Horodatage complet**: Format `<slug>-<YYYYMMDD-HHmmss>.md` pour éviter les collisions
- **Frontmatter YAML**: Métadonnées ajoutées (saved_at, source, slug, auto_detected)
- **Breakpoint de confirmation**: Validation du slug avant sauvegarde
- **14 commandes**: Total des commandes EPCI passe de 13 à 14

## [5.2.3] - 2026-01-15

### Added

- **New agent**: `@statusline-setup` for Claude Code status line configuration

### Changed

- **File references**: Added `@` syntax rule in CLAUDE.md (Section 9)
  - All file references must use `@path` instead of backticks or markdown links
  - Corrected 28 occurrences across 5 command files

### Fixed

- **plugin.json**: Added missing `statusline-setup.md` agent (16 agents total)
- **Subagents count**: Updated from 15 to 16 in CLAUDE.md

## [5.2.0] - 2026-01-15

### Added

- **Nouvelle commande `/ralph-exec`**: Exécute UNE story avec EPCT inline (sans routing vers /brief ou /epci)

### Changed

- **Suppression `/ralph` et `/cancel-ralph`**: Remplacés par workflow plus simple
- **Suppression `@ralph-executor`**: Logique migrée dans `/ralph-exec`
- **Libération contexte**: Chaque appel `claude "/ralph-exec"` = contexte frais
- **Promise tag simplifié**: `<promise>STORY_DONE</promise>` pour détection complétion
- **ralph.sh mis à jour**: Appelle `/ralph-exec` au lieu de PROMPT.md
- **Brainstorm v5.2**: Breakpoint display improvements
  - ASCII box format (`┌─ │ ├─ └─`) instead of simple dashes
  - EMS 5-axis visual progress bars (`████████░░`)
  - `[WEAK]` markers on axes < 50
  - EMS progression history visible at checkpoints
  - Mandatory `ems_history` tracking in session_state
  - Journal corrected to use only standard axes

- **References reorganization**: Command-specific subdirectories
  - New structure: `references/brainstorm/`, `references/epci/`, etc.
  - Migrated 16 existing reference files to new structure
  - Created 3 new reference files: commands.md, flags.md, completion-summary.md
  - Changelog consolidated in root CHANGELOG.md

## [5.1.2] - 2026-01-XX

### Added

- **Génération automatique backlog.md**: `/decompose` génère maintenant automatiquement le backlog table
- **Génération automatique prd.json**: Plus besoin de flag, toujours généré
- **Deux niveaux de granularité**: Sub-specs (1-5 jours) + Stories (1-2h) dans backlog

## [5.1.0] - 2026-01-XX

### Changed

- **Brainstorm v5.1**: Native question system
  - AskUserQuestion native tool integration (interactive QCM UI)
  - Maximum 3 questions per iteration (reduced from 5)
  - Priority headers: `🛑 Critical`, `⚠️ Important`, `ℹ️ Info`
  - Visual recommendations: `(Recommended)` in option labels
  - Separated breakpoint: Status as text, questions via AskUserQuestion
  - @technique-advisor returns JSON, main thread handles display

## [5.0.0] - 2026-01-XX

### Added

- **Brainstorm v5.0**: PRD Industry Standards v3.0
  - Executive Summary, Problem Statement, Goals/Non-Goals sections
  - Timeline & Milestones, FAQ, Assumptions, Appendix sections
  - `--competitive` flag for Competitive Analysis section
  - Finalization Checkpoint lowered to EMS >= 70 (blocking)
  - No automatic finalization — always requires explicit user choice

## [4.9.1] - 2026-01-XX

### Added

- **Flag `--from-native-plan <file>`**: Import du plan natif Claude Code comme base pour Phase 1
- **Exploration conditionnelle**: @Explore automatique si §1 manquant lors de l'import
- **Copie automatique pour traçabilité**: Plan natif archivé dans Feature Document §2
- **Raffinement intelligent**: Phase 1 raffine le plan natif au lieu de repartir de zéro
- **Workflow hybride**: `/epci` peut maintenant fonctionner avec ou sans `/brief` préalable

## [4.9.0] - 2026-01-XX

### Added

- **3 nouveaux agents**: `@expert-panel`, `@party-orchestrator`, `@rule-clarifier` pour brainstorming v5.0
- **Nouveau skill**: `input-clarifier` pour validation entrées utilisateur
- **Finalization Checkpoint obligatoire**: À EMS >= 70, checkpoint bloquant avec choix explicite

### Changed

- **Brainstorm v4.9**: Finalization Checkpoint
  - Mandatory checkpoint at EMS >= 85 (blocking)
  - No automatic finalization — explicit user choice required

## [4.8.1] - 2026-01-XX

### Changed

- **Finalization Checkpoint**: EMS >= 85 pour déclencher checkpoint (ajusté depuis 70)

## [4.8.0] - 2026-01-XX

### Added

- **Brainstorm v4.8**: Auto-technique system
  - Auto-selection of techniques based on weak EMS axes (< 50)
  - Mix of techniques when 2+ axes weak
  - Explicit transition check Divergent → Convergent
  - Preview @planner/@security in Convergent phase
  - Post-brainstorm hook documented

## [4.7.0] - 2026-01-06

### Added

- **Brainstorm v4.3 Optimization**: Major performance refactoring
  - 6 new reference files in `src/commands/references/` for modular documentation
  - 2 new Haiku agents: `@ems-evaluator` (EMS scoring), `@technique-advisor` (technique selection)
  - New brainstorm modes: `--random`, `--progressive`
  - Integrated spike process via `spike [duration] [question]` command
  - Session commands: `status`, `technique`, `finish`, `batch`
  - Energy checkpoints with automatic EMS evaluation

### Changed

- **Refactored `/brainstorm` command**: 949 → 164 lines (-83% tokens)
- **Refactored `brainstormer` skill**: 387 → 193 lines (-50% tokens)
- **Updated subagent count**: 10 → 12 agents (added @ems-evaluator, @technique-advisor)

## [4.6.0] - 2026-01-XX

### Changed

- **Inversion reformulation/exploration**: La reformulation est maintenant AVANT l'exploration dans `/brief`
- **Breakpoint validation obligatoire**: Toujours afficher un breakpoint après reformulation
- **Hooks pre-brief et post-brief actifs**: Nouveaux hooks pour traçabilité complète
- **Fusion Analysis + Complexity**: Step 2 et Step 4 fusionnées pour éliminer la redondance
- **@clarifier explicite**: Invocation @clarifier (Haiku) documentée dans mode --turbo
- **Gestion erreur @Explore**: Fallback documenté si exploration échoue

## [4.5.0] - 2026-01-XX

### Added

- **Brainstorming v4.1 — SuperPowers Integration**
  - One-at-a-Time Questions: Une question à la fois avec choix multiples A/B/C
  - Section-by-Section Validation: Validation incrémentale du brief
  - @planner in Brainstorm: Plan préliminaire automatique en phase Convergent
  - @security-auditor in Brainstorm: Analyse sécurité conditionnelle si auth/payment détectés
  - Nouvelles commandes brainstorm: `batch`, `plan-preview`, `security-check`
  - Nouveaux flags: `--no-security`, `--no-plan`

## [4.4.0] - 2026-01-XX

### Added

- **Ajout `/commit`**: Commande dédiée pour finalisation git avec contexte EPCI
- **3 nouveaux agents turbo**: `@clarifier`, `@planner`, `@implementer` pour modes rapides

### Changed

- **Fusion learn → memory**: `/learn` supprimé, learning intégré dans `/memory` via subcommands `learn status|reset|calibrate`
- **Hooks obligatoires documentés**: Section 11 ajoutée pour garantir la mise à jour mémoire

## [4.3.0] - 2026-01-XX

### Changed

- **Fusion spike → brainstorm**: `/spike` supprimé, exploration technique intégrée dans `/brainstorm` via commande `spike [duration] [question]`

## [4.2.0] - 2024-12-31

### Changed

- **Command Renaming**: Removed redundant `epci-` prefix from all commands
    - `/epci:epci-brief` → `/epci:brief`
    - `/epci:epci-quick` → `/epci:quick`
    - `/epci:epci-spike` → `/epci:spike`
    - `/epci:epci-debug` → `/epci:debug`
    - `/epci:epci-decompose` → `/epci:decompose`
    - `/epci:epci-memory` → `/epci:memory`
    - `/epci:epci-learn` → `/epci:learn`
- Updated all internal references in commands, agents, skills, hooks, and documentation
- Maintained `/epci:epci` as the main workflow command (unchanged)
- Maintained `/epci:brainstorm` and `/epci:create` (already without prefix)

### Technical Details

- Renamed 7 command files in `src/commands/`
- Updated `plugin.json` with new command paths
- Updated all cross-references in 9 agent files, 15+ skill files, 4 hook files
- Updated `CLAUDE.md`, `README.md`, and `src/settings/flags.md`
- Version bumped to 4.2.0

## [3.0.0] - 2024-12

### Added

- Complete rewrite from v2.7 to v3.0 with simplified architecture
- 5 core commands: `/epci-brief`, `/epci`, `/epci-quick`, `/epci-spike`, `/epci:create`
- 5 custom subagents: plan-validator, code-reviewer, security-auditor, qa-reviewer, doc-generator
- 13 skills system: 5 core, 4 stack-specific, 4 factory skills
- Component Factory system for creating new skills, commands, and agents
- Feature Document pattern for STANDARD/LARGE features
- Unified entry point via `/epci-brief` with intelligent routing

### Changed

- Simplified from 12 commands to 5 commands
- Consolidated routing from 5 levels to 3 workflows
- Replaced custom flags/personas with native Claude Code features
- Enhanced subagent integration with conditional activation

### Removed

- v2.7 commands: epci-discover, epci-0-briefing, epci-micro, epci-soft, epci-hotfix
- Custom flags and personas systems (replaced by native Claude Code)
- Pre-stage workflows (integrated into epci-brief)

### Migration

- `epci-discover` → `epci-brief`
- `epci-0-briefing` → `epci-brief`
- `epci-micro` → `epci-quick` (TINY mode)
- `epci-soft` → `epci-quick` (SMALL mode)
- `epci-1-analyse` → `epci` Phase 1
- `epci-2-code` → `epci` Phase 2
- `epci-3-finalize` → `epci` Phase 3
