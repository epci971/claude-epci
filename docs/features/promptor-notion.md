# Feature Document — Commande /promptor avec MCP Notion

> **Complexité** : LARGE | **Estimation** : 8h | **Date** : 2025-12-31

---

## §1 — Functional Brief

### Objectif

Créer une commande `/promptor` dans le plugin EPCI Claude Code qui reproduit la logique métier du skill web code-promptor : transformer des dictées vocales ou textuelles en tâches structurées, puis les exporter directement vers Notion via le MCP officiel. L'outil servira de pense-bête rapide pour capturer des idées à la volée, indépendamment du workflow EPCI principal.

### Description

Le skill web code-promptor v2.1 offre une expérience de capture d'idées fluide : dictée → détection multi-tâches → génération de briefs formatés → export Notion. L'objectif est de porter cette expérience dans Claude Code en tirant parti :
- Du MCP Notion officiel (`@notionhq/notion-mcp-server`) pour l'export direct
- De la configuration locale `.claude/settings.local.json` pour les secrets
- De l'accès au codebase pour un contexte enrichi (optionnel)

### Stack identifiée

- **Plugin EPCI** : Commands (markdown) + Skills (markdown) + Python (hooks/scripts)
- **MCP existants** : Context7, Sequential, Magic, Playwright
- **MCP à ajouter** : Notion (`@notionhq/notion-mcp-server` v2.0.0)

### Fichiers source (code-promptor web)

| Fichier | Rôle |
|---------|------|
| `skills-web/code-promptor/SKILL.md` | Logique métier principale |
| `skills-web/code-promptor/references/multi-task-detection.md` | Algorithme détection |
| `skills-web/code-promptor/references/output-format.md` | 3 formats briefs |
| `skills-web/code-promptor/references/voice-cleaning.md` | Nettoyage dictée |
| `skills-web/code-promptor/references/subtask-templates.md` | Auto-génération sous-tâches |
| `skills-web/code-promptor/references/type-mapping.md` | Mapping types Notion |
| `skills-web/code-promptor/templates/checkpoint-format.md` | Formats d'affichage |
| `skills-web/code-promptor/config/notion-ids.md` | Configuration Notion |

### Fichiers cibles

| Fichier | Action |
|---------|--------|
| `src/commands/promptor.md` | Créer |
| `src/skills/promptor/SKILL.md` | Créer |
| `src/skills/promptor/references/*.md` | Créer (4 fichiers) |
| `src/skills/promptor/templates/*.md` | Créer (3 fichiers) |
| `src/skills/promptor/config/notion-mapping.md` | Créer |
| `src/mcp/config.py` | Modifier (ajouter notion) |
| `.claude/settings.local.json.example` | Créer |
| `CLAUDE.md` | Modifier (documenter) |

### Exigences fonctionnelles

- [FR1] : La commande `/promptor [texte]` génère un brief et l'exporte vers Notion en mode one-shot
- [FR2] : La commande `/promptor session` démarre un mode session avec projet verrouillé
- [FR3] : L'algorithme de détection multi-tâches (seuil 40 pts) segmente les dictées en tâches indépendantes
- [FR4] : Un checkpoint interactif affiche les tâches détectées avec commandes (ok, merge, edit, drop)
- [FR5] : Trois formats de brief adaptatifs : Quick fix (1h), Standard (4h), Major (8h)
- [FR6] : Les sous-tâches sont auto-générées selon le type et domaine détectés
- [FR7] : L'export Notion crée des pages avec mapping propriétés (Nom, Type, Temps estimé, État, DAY, Projet)
- [FR8] : La configuration Notion est lue depuis `.claude/settings.local.json`
- [FR9] : En cas d'erreur Notion, le brief est affiché en texte avec option retry

### Exigences non-fonctionnelles

- [NFR1] : Le MCP Notion doit être optionnel — la commande fonctionne sans (affichage brief uniquement)
- [NFR2] : Les tokens Notion ne doivent jamais apparaître dans les logs ou outputs
- [NFR3] : La latence de création Notion doit être < 3s par tâche
- [NFR4] : La commande doit supporter la dictée vocale (nettoyage hésitations)

### Contraintes techniques

- Le MCP Notion officiel utilise l'API 2025-09-03 avec `data_source_id` (pas `database_id`)
- Les propriétés Notion doivent matcher le schéma existant de la base Tâches
- Le fichier `.claude/settings.local.json` doit rester compatible avec la structure actuelle

### Technical Validation (Spikes)

**MCP Notion — GO ✅**
- Package : `@notionhq/notion-mcp-server` (officiel)
- Tools : `create-a-page`, `query-data-source`
- Auth : Variable `NOTION_TOKEN`

**Secrets Management — GO ✅**
- Fichier : `.claude/settings.local.json` (gitignored, permissions 600)
- Pattern validé et sécurisé

### Memory Summary

- **Conventions** : Commands en markdown, Skills avec SKILL.md + references/ + templates/
- **Patterns** : MCP config dans `src/mcp/config.py`, validation via scripts Python
- **Velocity** : N/A (première feature de ce type)

---

## §2 — Implementation Plan

### Approche MCP Notion

Le MCP Notion officiel (`@notionhq/notion-mcp-server`) est **externe** à EPCI :
- Configuré dans les settings Claude Code utilisateur
- Le skill promptor utilise les tools MCP si disponibles, sinon affichage texte
- Les secrets (token) sont dans `.claude/settings.local.json` ou variables env

### Mapping Source → Cible

| Fichier Source (skills-web/code-promptor/) | Fichier Cible | Action |
|---------------------------------------------|---------------|--------|
| `SKILL.md` | `src/skills/promptor/SKILL.md` | Adapter |
| `references/multi-task-detection.md` | `src/skills/promptor/references/multi-task-detection.md` | Porter |
| `references/output-format.md` | `src/skills/promptor/references/output-format.md` | Porter |
| `references/voice-cleaning.md` | `src/skills/promptor/references/voice-cleaning.md` | Porter |
| `references/subtask-templates.md` | `src/skills/promptor/references/subtask-templates.md` | Porter |
| `references/processing-rules.md` | `src/skills/promptor/references/processing-rules.md` | Porter |
| `references/type-mapping.md` | `src/skills/promptor/references/type-mapping.md` | Porter |
| `templates/brief-quickfix.md` | `src/skills/promptor/templates/brief-quickfix.md` | Porter |
| `templates/brief-standard.md` | `src/skills/promptor/templates/brief-standard.md` | Porter |
| `templates/brief-major.md` | `src/skills/promptor/templates/brief-major.md` | Porter |
| `templates/checkpoint-format.md` | `src/skills/promptor/templates/checkpoint-format.md` | Adapter CLI |
| `config/notion-ids.md` | `src/skills/promptor/config/notion-config.md` | Adapter |
| - | `src/commands/promptor.md` | Créer |
| - | `.claude/settings.local.json.example` | Créer |
| - | `CLAUDE.md` | Modifier |

**Total : 15 fichiers (13 créer, 1 modifier, 1 template)**

### Tasks

#### Phase 0: Préparation (15 min)
- [ ] **T0.1** Créer structure dossiers `src/skills/promptor/{references,templates,config}` (5 min)
- [ ] **T0.2** Créer `.claude/settings.local.json.example` avec section notion (10 min)

#### Phase 1: Skill Core (60 min)
- [ ] **T1.1** Créer `SKILL.md` structure et overview (15 min)
- [ ] **T1.2** Adapter decision tree et session mode pour CLI (15 min)
- [ ] **T1.3** Adapter section multi-task detection (10 min)
- [ ] **T1.4** Adapter section Notion integration pour CLI (10 min)
- [ ] **T1.5** Finaliser SKILL.md et valider cohérence (10 min)

#### Phase 2: References (75 min)
- [ ] **T2.1** Porter `multi-task-detection.md` (12 min)
- [ ] **T2.2** Porter `output-format.md` (12 min)
- [ ] **T2.3** Porter `voice-cleaning.md` (10 min)
- [ ] **T2.4** Porter `subtask-templates.md` (12 min)
- [ ] **T2.5** Porter `processing-rules.md` (15 min)
- [ ] **T2.6** Porter `type-mapping.md` (14 min)

#### Phase 3: Templates (45 min)
- [ ] **T3.1** Porter `brief-quickfix.md` (10 min)
- [ ] **T3.2** Porter `brief-standard.md` (10 min)
- [ ] **T3.3** Porter `brief-major.md` (10 min)
- [ ] **T3.4** Adapter `checkpoint-format.md` pour CLI (15 min)

#### Phase 4: Config (15 min)
- [ ] **T4.1** Créer `notion-config.md` — Schéma propriétés, mapping types (15 min)

#### Phase 5: Commande (45 min)
- [ ] **T5.1** Créer `src/commands/promptor.md` — Structure et configuration (15 min)
- [ ] **T5.2** Implémenter workflow one-shot dans commande (15 min)
- [ ] **T5.3** Implémenter workflow session dans commande (15 min)

#### Phase 6: Documentation et Validation (30 min)
- [ ] **T6.1** Mettre à jour `CLAUDE.md` — Sections 2, 4, 6 (10 min)
- [ ] **T6.2** Exécuter validation skill (5 min)
- [ ] **T6.3** Exécuter validation command (5 min)
- [ ] **T6.4** Test manuel workflow one-shot (5 min)
- [ ] **T6.5** Test manuel workflow session (5 min)

### Risks

| Risque | Prob. | Impact | Mitigation |
|--------|-------|--------|------------|
| MCP Notion non configuré | High | Medium | Fallback texte, guide setup |
| Tokens skill trop longs | Low | Medium | Validation limite 5000 |
| Format checkpoint CLI | Low | Low | Test et ajustement |

### Validation

- **@plan-validator**: APPROVED
  - Completeness: OK
  - Consistency: OK
  - Feasibility: OK
  - Quality: OK

### Estimation

| Phase | Durée |
|-------|-------|
| Phase 0 | 15 min |
| Phase 1 | 60 min |
| Phase 2 | 75 min |
| Phase 3 | 45 min |
| Phase 4 | 15 min |
| Phase 5 | 45 min |
| Phase 6 | 30 min |
| **Total** | **~5h30** |

---

## §3 — Implementation & Finalization

### Implementation Status

| Phase | Status | Notes |
|-------|--------|-------|
| Phase 0: Préparation | ✅ Complete | Dossiers créés, settings.local.json.example créé |
| Phase 1: Skill Core | ✅ Complete | SKILL.md créé avec decision tree, session mode, MCP integration |
| Phase 2: References | ✅ Complete | 6 fichiers portés (multi-task, output, voice, subtask, processing, type) |
| Phase 3: Templates | ✅ Complete | 4 fichiers (3 briefs + checkpoint-format CLI) |
| Phase 4: Config | ✅ Complete | notion-config.md avec mapping propriétés |
| Phase 5: Commande | ✅ Complete | promptor.md avec one-shot et session mode |
| Phase 6: Doc & Validation | ✅ Complete | CLAUDE.md mis à jour, validations passées |

### Files Created (15)

```
.claude/settings.local.json.example
src/skills/promptor/SKILL.md
src/skills/promptor/references/multi-task-detection.md
src/skills/promptor/references/output-format.md
src/skills/promptor/references/voice-cleaning.md
src/skills/promptor/references/subtask-templates.md
src/skills/promptor/references/processing-rules.md
src/skills/promptor/references/type-mapping.md
src/skills/promptor/templates/brief-quickfix.md
src/skills/promptor/templates/brief-standard.md
src/skills/promptor/templates/brief-major.md
src/skills/promptor/templates/checkpoint-format.md
src/skills/promptor/config/notion-config.md
src/commands/promptor.md
CLAUDE.md (modified)
```

### Validation Results

```
[SKILL] promptor: PASSED (6/6 checks)
  - Structure: Valid
  - YAML syntax: Valid
  - Name format: 'promptor' (8 chars)
  - Description: 528 chars
  - Token count: ~1760 tokens
  - References: Checked

[COMMAND] promptor.md: PASSED (5/5 checks)
  - File exists: OK
  - YAML frontmatter: Valid
  - Description: 236 chars
  - Allowed-tools: 5 tools
  - Content structure: ~1628 tokens
```

### Usage

```bash
# One-shot mode
/epci:promptor "il faudrait ajouter un bouton de logout dans le header"

# Session mode
/epci:promptor session
> première tâche dictée...
> deuxième tâche...
> done
```

### Next Steps

- Configurer MCP Notion dans l'environnement utilisateur (voir `.claude/settings.local.json.example`)
- Tester workflow complet avec export Notion réel
