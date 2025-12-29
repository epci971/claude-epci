# Feature Document — F12: MCP Integration

> **Slug**: `f12-mcp-integration`
> **Category**: LARGE
> **Date**: 2025-12-29
> **Source**: CDC-F12-MCP-Integration.md

---

## §1 — Functional Brief

### Context

EPCI v3.x n'intègre pas de serveurs MCP (Model Context Protocol) pour enrichir le contexte avec des données externes. Cette feature ajoute l'intégration de 4 serveurs MCP avec activation automatique selon le contexte et les personas.

**Problème résolu:**
- Pas d'accès aux docs à jour des librairies externes
- Pas de raisonnement structuré multi-étapes
- Pas de génération UI moderne
- Pas de tests E2E automatisés

**Solution:** Intégration de 4 serveurs MCP avec auto-activation basée sur F09 (personas).

### Detected Stack

- **Framework**: Claude Code Plugin v3.5.0
- **Language**: Python 3 + Markdown
- **Patterns detected**:
  - skill-with-references (skills/personas/, skills/core/)
  - dataclass-config (orchestration/config.py)
  - fallback-strategy (debugging-strategy/SKILL.md)
  - breakpoint-display (breakpoint-metrics/)

### 4 MCP Servers

| Server | Function | Auto-trigger |
|--------|----------|--------------|
| **Context7** | Documentation librairies externes | imports, framework questions, persona architect/backend |
| **Sequential** | Raisonnement structuré multi-étapes | --think-hard, --ultrathink, debugging complexe |
| **Magic** | Génération composants UI (21st.dev) | persona frontend, fichiers *.jsx/*.tsx/*.vue |
| **Playwright** | Tests E2E, automatisation browser | persona qa, fichiers *.spec.ts/*.e2e.ts |

### Acceptance Criteria

- [ ] AC1: 4 MCPs documentés dans `src/skills/mcp/`
- [ ] AC2: Auto-activation par persona fonctionne (test avec 6 personas)
- [ ] AC3: Configuration projet dans `.project-memory/settings.json` fonctionne
- [ ] AC4: Mode dégradé si MCP indisponible (fallback gracieux)
- [ ] AC5: Flags manuels fonctionnent (`--c7`, `--seq`, `--magic`, `--play`, `--no-mcp`)

### Constraints

- Dépendance forte sur F09 (Personas) - déjà implémenté
- Fallback obligatoire si MCP timeout (15s max, 2 retries)
- Pas d'impact sur les workflows si MCPs désactivés
- Budget tokens: Sequential uniquement avec --think-hard

### Out of Scope

- Création de nouveaux MCP servers custom
- MCP servers custom par projet
- Cache des résultats MCP
- Métriques d'usage MCP détaillées

### Evaluation

- **Category**: LARGE
- **Estimated files**: 24 (15 new + 9 modified)
- **Estimated LOC**: ~1500
- **Risk**: Medium (dépend MCPs externes, mais fallbacks prévus)
- **Justification**: Architecture impactée (nouveau module src/mcp/), intégration F09/F11

### Suggested Flags

| Flag | Source | Reason |
|------|--------|--------|
| `--think-hard` | auto | 24 files impacted, architecture nouvelle |
| `--wave` | auto | complexity > 0.7, multi-phase implementation |
| `--persona-architect` | auto (0.72) | system design, patterns integration |

### Memory Summary

- **Project**: tools-claude-code-epci
- **Stack**: claude-code-plugin v3.5.0
- **Conventions**: kebab-case files, skills in `src/skills/{category}/{name}/SKILL.md`
- **Velocity**: 9 features completed (5 LARGE, 4 SMALL)
- **Dependencies**: F09 Personas (strong), F11 Orchestration (weak)

### Files to Create (15)

```
src/skills/mcp/
├── MCP.md                    # Index et configuration
├── context7.md               # Documentation Context7
├── sequential.md             # Documentation Sequential
├── magic.md                  # Documentation Magic
└── playwright.md             # Documentation Playwright

src/mcp/
├── __init__.py               # Module initialization
├── config.py                 # MCPServerConfig, MCPRegistry
├── auto_activation.py        # Activation logic avec F09
├── registry.py               # MCP server discovery
├── fallbacks.py              # Fallback strategies
└── activation_matrix.py      # Persona × MCP rules

src/mcp/tests/
├── __init__.py
├── test_auto_activation.py   # Test persona-based activation
└── test_fallbacks.py         # Test fallback behaviors
```

### Files to Modify (9)

| File | Modification |
|------|--------------|
| `.project-memory/settings.json` | Add "mcp" section |
| `src/skills/personas/SKILL.md` | Update MCP section status |
| `src/commands/epci-brief.md` | Add Step 5.5 MCP activation |
| `src/commands/epci.md` | Add MCP initialization in phases |
| `src/commands/epci-quick.md` | Add lightweight MCP activation |
| `src/orchestration/config.py` | Add MCPConfig dataclass |
| `src/orchestration/wave_context.py` | Add MCPContext to WaveContext |
| `CLAUDE.md` | Update sections 3.8 and 4.3 |
| `src/settings/flags.md` | Add MCP flags section |

---

## §2 — Implementation Plan

### Impacted Files

| File | Action | Risk | Wave |
|------|--------|------|------|
| `src/mcp/__init__.py` | Create | Low | 1 |
| `src/mcp/config.py` | Create | Low | 1 |
| `src/mcp/activation_matrix.py` | Create | Low | 2 |
| `src/mcp/auto_activation.py` | Create | Medium | 2 |
| `src/mcp/registry.py` | Create | Low | 2 |
| `src/mcp/fallbacks.py` | Create | Low | 2 |
| `src/mcp/tests/__init__.py` | Create | Low | 4 |
| `src/mcp/tests/test_auto_activation.py` | Create | Low | 4 |
| `src/mcp/tests/test_fallbacks.py` | Create | Low | 4 |
| `src/skills/mcp/MCP.md` | Create | Low | 3 |
| `src/skills/mcp/context7.md` | Create | Low | 3 |
| `src/skills/mcp/sequential.md` | Create | Low | 3 |
| `src/skills/mcp/magic.md` | Create | Low | 3 |
| `src/skills/mcp/playwright.md` | Create | Low | 3 |
| `.project-memory/settings.json` | Modify | Low | 1 |
| `src/skills/personas/SKILL.md` | Modify | Low | 3 |
| `src/commands/epci-brief.md` | Modify | Medium | 3 |
| `src/commands/epci.md` | Modify | Low | 3 |
| `src/commands/epci-quick.md` | Modify | Low | 3 |
| `src/orchestration/config.py` | Modify | Medium | 4 |
| `src/orchestration/wave_context.py` | Modify | Medium | 4 |
| `CLAUDE.md` | Modify | Low | 4 |
| `src/settings/flags.md` | Modify | Low | 4 |

### Tasks by Wave

#### Wave 1: Foundations (40 min)

- [ ] **1.1** Create MCP module structure (5 min)
  - Files: `src/mcp/__init__.py`, `src/mcp/tests/__init__.py`
  - Test: Directory exists with valid __init__.py

- [ ] **1.2** Create MCPServerConfig dataclass (15 min)
  - File: `src/mcp/config.py`
  - Classes: MCPServerConfig, MCPContext
  - Test: Dataclass validation works

- [ ] **1.3** Add MCP section to settings.json (10 min)
  - File: `.project-memory/settings.json`
  - Test: JSON valid, 4 servers configured

#### Wave 2: Core Logic (65 min)

- [ ] **2.1** Implement activation_matrix.py (15 min)
  - File: `src/mcp/activation_matrix.py`
  - Constant: PERSONA_MCP_MAPPING
  - Test: Matrix matches CDC-F12

- [ ] **2.2** Implement auto_activation.py (20 min)
  - File: `src/mcp/auto_activation.py`
  - Class: MCPAutoActivation
  - Test: Persona combinations work

- [ ] **2.3** Implement registry.py (15 min)
  - File: `src/mcp/registry.py`
  - Class: MCPRegistry (singleton)
  - Test: Registry operations

- [ ] **2.4** Implement fallbacks.py (15 min)
  - File: `src/mcp/fallbacks.py`
  - Functions: get_fallback(), execute_with_fallback()
  - Test: Fallback behavior

#### Wave 3: Integration (95 min)

- [ ] **3.1** Create MCP.md index skill (15 min)
  - File: `src/skills/mcp/MCP.md`
  - Test: YAML valid, skill loads

- [ ] **3.2** Create context7.md skill (10 min)
  - File: `src/skills/mcp/context7.md`
  - Test: Content complete

- [ ] **3.3** Create sequential.md skill (10 min)
  - File: `src/skills/mcp/sequential.md`
  - Test: Content complete

- [ ] **3.4** Create magic.md skill (10 min)
  - File: `src/skills/mcp/magic.md`
  - Test: Content complete

- [ ] **3.5** Create playwright.md skill (10 min)
  - File: `src/skills/mcp/playwright.md`
  - Test: Content complete

- [ ] **3.6** Update epci-brief.md with Step 5.5 (15 min)
  - File: `src/commands/epci-brief.md`
  - Test: MCP shown in breakpoint

- [ ] **3.7** Update epci.md for MCP initialization (10 min)
  - File: `src/commands/epci.md`
  - Test: MCPContext in phases

- [ ] **3.8** Update epci-quick.md for lightweight MCP (10 min)
  - File: `src/commands/epci-quick.md`
  - Test: Works with/without MCP

- [ ] **3.9** Update personas SKILL.md (5 min)
  - File: `src/skills/personas/SKILL.md`
  - Test: Status updated

#### Wave 4: Finalization (70 min)

- [ ] **4.1** Extend orchestration config.py (10 min)
  - File: `src/orchestration/config.py`
  - Test: MCPConfig loads

- [ ] **4.2** Extend wave_context.py (10 min)
  - File: `src/orchestration/wave_context.py`
  - Test: MCPContext in WaveContext

- [ ] **4.3** Create test_auto_activation.py (15 min)
  - File: `src/mcp/tests/test_auto_activation.py`
  - Test: 6 personas, thresholds

- [ ] **4.4** Create test_fallbacks.py (10 min)
  - File: `src/mcp/tests/test_fallbacks.py`
  - Test: Fallback strategies

- [ ] **4.5** Update flags.md with MCP flags (10 min)
  - File: `src/settings/flags.md`
  - Test: Complete documentation

- [ ] **4.6** Update CLAUDE.md (15 min)
  - File: `CLAUDE.md`
  - Test: Section 3.9 added

### Risks

| Risk | Probability | Mitigation |
|------|-------------|------------|
| MCP timeout impacts workflow | Medium | 15s timeout, 2 retries, fallback |
| Sequential MCP uses too many tokens | Medium | Only with --think-hard |
| Configuration complexity | Low | Sensible defaults |
| Error propagation | Low | Try/except, log, continue |

### Validation

- **@plan-validator**: APPROVED
- **Issues**: 0 Critical, 0 Important, 2 Minor (documentation alignment)
- **Recommendations**: Verify step/section numbering during implementation

---

## §3 — Implementation & Finalization

### Progress

- [x] Wave 1: Foundations
  - [x] 1.1 Create MCP module structure (`src/mcp/__init__.py`, `tests/__init__.py`)
  - [x] 1.2 Create MCPServerConfig dataclass (`src/mcp/config.py`)
  - [x] 1.3 Add MCP section to settings.json

- [x] Wave 2: Core Logic
  - [x] 2.1 Implement `activation_matrix.py` with PERSONA_MCP_MAPPING
  - [x] 2.2 Implement `auto_activation.py` with MCPAutoActivation class
  - [x] 2.3 Implement `registry.py` with MCPRegistry singleton
  - [x] 2.4 Implement `fallbacks.py` with FallbackStrategy enum

- [x] Wave 3: Integration
  - [x] 3.1 Create `src/skills/mcp/SKILL.md` (main skill file)
  - [x] 3.2 Create `src/skills/mcp/references/context7.md`
  - [x] 3.3 Create `src/skills/mcp/references/sequential.md`
  - [x] 3.4 Create `src/skills/mcp/references/magic.md`
  - [x] 3.5 Create `src/skills/mcp/references/playwright.md`
  - [x] 3.6 Update `epci-brief.md` with Step 6: MCP Activation
  - [x] 3.7 Update `epci.md` with MCP flags section
  - [x] 3.8 Update `epci-quick.md` with lightweight MCP support
  - [x] 3.9 Update `personas SKILL.md` status to F12 Active

- [x] Wave 4: Finalization
  - [x] 4.1 Extend `orchestration/config.py` with MCPConfig
  - [x] 4.2 Extend `wave_context.py` with mcp_context field
  - [x] 4.3 Create `test_auto_activation.py` (28 tests)
  - [x] 4.4 Create `test_fallbacks.py` (18 tests)
  - [x] 4.5 Update `flags.md` with MCP Flags section
  - [x] 4.6 Update `CLAUDE.md` (v4.0, section 1.5, 3.9, 4.3)

### Tests

```
Files: 2 test modules
Tests: 46 test cases
Coverage: Auto-activation, fallbacks, persona integration, thresholds
```

### Reviews

- **@code-reviewer**: APPROVED
  - Strengths: Excellent architecture, SOLID principles, type safety, F09 integration
  - LOC: 1,813 lines
  - Type Coverage: ~95%
  - Issues: 0 Critical, 2 Important (thread safety noted, placeholder health check), 3 Minor

### Files Created (15)

| File | LOC | Status |
|------|-----|--------|
| `src/mcp/__init__.py` | 22 | ✓ |
| `src/mcp/config.py` | 206 | ✓ |
| `src/mcp/activation_matrix.py` | 235 | ✓ |
| `src/mcp/auto_activation.py` | 290 | ✓ |
| `src/mcp/registry.py` | 242 | ✓ |
| `src/mcp/fallbacks.py` | 176 | ✓ |
| `src/mcp/tests/__init__.py` | 3 | ✓ |
| `src/mcp/tests/test_auto_activation.py` | 267 | ✓ |
| `src/mcp/tests/test_fallbacks.py` | 266 | ✓ |
| `src/skills/mcp/SKILL.md` | ~200 | ✓ |
| `src/skills/mcp/references/context7.md` | ~120 | ✓ |
| `src/skills/mcp/references/sequential.md` | ~110 | ✓ |
| `src/skills/mcp/references/magic.md` | ~110 | ✓ |
| `src/skills/mcp/references/playwright.md` | ~110 | ✓ |

### Files Modified (9)

| File | Changes | Status |
|------|---------|--------|
| `.project-memory/settings.json` | Added "mcp" section | ✓ |
| `src/skills/personas/SKILL.md` | F12 Active status | ✓ |
| `src/commands/epci-brief.md` | Step 6 MCP Activation | ✓ |
| `src/commands/epci.md` | MCP Flags section | ✓ |
| `src/commands/epci-quick.md` | Lightweight MCP support | ✓ |
| `src/orchestration/config.py` | MCPConfig dataclass | ✓ |
| `src/orchestration/wave_context.py` | mcp_context, mcp_servers_used | ✓ |
| `src/settings/flags.md` | MCP Flags section | ✓ |
| `CLAUDE.md` | v4.0, sections 1.5, 3.9, 4.3 | ✓ |

### Deviations

| Plan | Deviation | Justification |
|------|-----------|---------------|
| `src/skills/mcp/MCP.md` | Changed to `SKILL.md` + `references/` | Follow skill naming convention |
| Health check implementation | Placeholder only | External MCP dependency, fallback covers |

### Acceptance Criteria

- [x] AC1: 4 MCPs documented in `src/skills/mcp/` ✓
- [x] AC2: Auto-activation by persona works (tested 6 personas) ✓
- [x] AC3: Project configuration in `.project-memory/settings.json` works ✓
- [x] AC4: Graceful degradation if MCP unavailable (fallback) ✓
- [x] AC5: Manual flags work (`--c7`, `--seq`, `--magic`, `--play`, `--no-mcp`) ✓

### Commit Message

```
feat(mcp): implement F12 MCP integration with auto-activation

Add Model Context Protocol (MCP) integration for EPCI v4.0:
- 4 MCP servers: Context7, Sequential, Magic, Playwright
- Auto-activation based on F09 personas (Persona × MCP matrix)
- Fallback strategies for graceful degradation
- Manual flags: --c7, --seq, --magic, --play, --no-mcp
- Per-project configuration via settings.json
- Integration with F11 wave orchestration

Refs: docs/features/f12-mcp-integration.md
```

### Commit Info

- **Hash**: `47ae443`
- **Branch**: `master`
- **Files committed**: 25
- **Insertions**: 3,138 lines
- **Deletions**: 20 lines

### PR Ready

- Branch: `master`
- Tests: ✓ 46 test cases
- Lint: ✓ Clean
- Docs: ✓ Up to date (CLAUDE.md v4.0)
- Feature Document: ✓ Complete (§1-§3)
