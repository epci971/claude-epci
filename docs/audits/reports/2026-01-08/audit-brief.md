# Audit Report — /brief

> **Date**: 2026-01-08
> **EPCI Version**: 4.5.0
> **Score Final**: 82/100
> **Auditor**: Claude (audit agent)

---

## Executive Summary

La commande `/brief` est le point d'entree unique du workflow EPCI. Elle presente une structure solide avec une bonne separation des etapes, une detection automatique des personas/MCP, et un systeme de reformulation pour les briefs vocaux. Cependant, quelques points d'amelioration existent: les hooks pre/post-brief documentes n'existent pas dans `hooks/active/`, et le mode --turbo pourrait beneficier d'une meilleure integration avec @clarifier.

**Score: 82/100** (Fixe: 81.35 + Adaptatif: 83.25)

---

## 1. Workflow Diagram

```mermaid
flowchart TB
    subgraph Step0["Step 0: Load Project Memory"]
        direction TB
        S0_START["Start /brief"]
        S0_SKILL["Skill: project-memory"]
        S0_CHECK{"Memory exists?"}
        S0_LOAD["Load context.json, conventions.json, settings.json"]
        S0_SKIP["Continue without context"]
    end

    subgraph Step1["Step 1: Exploration (MANDATORY)"]
        direction TB
        S1_HOOK["HOOK: pre-brief"]
        S1_AGENT["@Explore (thorough)"]
        S1_OUTPUT["Store: files, stack, patterns, risks"]
    end

    subgraph Step15["Step 1.5: Reformulation"]
        direction TB
        S15_CHECK{"Voice artifacts?"}
        S15_CLEAN["Clean brief: remove euh, hum, genre..."]
        S15_DETECT["Detect template: FEATURE/PROBLEM/DECISION"]
        S15_BP["BP: Reformulation Suggere"]
        S15_SKIP["Skip to Step 2"]
    end

    subgraph Step2["Step 2: Analysis (Internal)"]
        direction TB
        S2_QUESTIONS["Prepare 2-3 clarification questions"]
        S2_SUGGEST["Prepare AI suggestions"]
        S2_EVAL["Evaluate complexity: TINY/SMALL/STD/LARGE"]
        S2_PERSONA["Detect personas (score > 0.6)"]
        S2_MCP["Activate MCP based on personas"]
        S2_FLAGS["Auto-detect flags"]
    end

    subgraph Step3["Step 3: BREAKPOINT (MANDATORY)"]
        direction TB
        S3_BP["BP: Analyse du Brief"]
        S3_OPTS["Options: [1] Repondre [2] Valider [3] Modifier [4] Lancer"]
    end

    subgraph Step4["Step 4: Complexity Finalization"]
        direction TB
        S4_FINAL["Finalize TINY/SMALL/STANDARD/LARGE"]
        S4_AUTOFLAGS["Auto-activate flags based on thresholds"]
    end

    subgraph Step5["Step 5: Generate Output (MANDATORY)"]
        direction TB
        S5_CHECK{"Complexity?"}
        S5_INLINE["Inline Brief (TINY/SMALL)"]
        S5_FEATDOC["Feature Document (STD/LARGE)"]
        S5_HOOK["HOOK: post-brief"]
    end

    subgraph Step6["Step 6: Execute Command"]
        direction TB
        S6_ROUTING{"Route by complexity"}
        S6_QUICK["/quick"]
        S6_EPCI["/epci"]
        S6_LARGE["/epci --large"]
    end

    subgraph Step7["Step 7: Rules Suggestion"]
        direction TB
        S7_CHECK{".claude/ exists?"}
        S7_SUGGEST["Suggest /rules"]
        S7_END["End"]
    end

    S0_START --> S0_SKILL
    S0_SKILL --> S0_CHECK
    S0_CHECK -->|Yes| S0_LOAD
    S0_CHECK -->|No| S0_SKIP
    S0_LOAD --> S1_HOOK
    S0_SKIP --> S1_HOOK

    S1_HOOK --> S1_AGENT
    S1_AGENT --> S1_OUTPUT
    S1_OUTPUT --> S15_CHECK

    S15_CHECK -->|Yes: --rephrase OR artifacts| S15_CLEAN
    S15_CHECK -->|No: --no-rephrase OR clean| S15_SKIP
    S15_CLEAN --> S15_DETECT
    S15_DETECT --> S15_BP
    S15_BP -->|User validates| S2_QUESTIONS
    S15_SKIP --> S2_QUESTIONS

    S2_QUESTIONS --> S2_SUGGEST
    S2_SUGGEST --> S2_EVAL
    S2_EVAL --> S2_PERSONA
    S2_PERSONA --> S2_MCP
    S2_MCP --> S2_FLAGS
    S2_FLAGS --> S3_BP

    S3_BP --> S3_OPTS
    S3_OPTS -->|[1] Repondre| S3_BP
    S3_OPTS -->|[2] Valider| S3_BP
    S3_OPTS -->|[3] Modifier| S3_BP
    S3_OPTS -->|[4] Lancer| S4_FINAL

    S4_FINAL --> S4_AUTOFLAGS
    S4_AUTOFLAGS --> S5_CHECK

    S5_CHECK -->|TINY/SMALL| S5_INLINE
    S5_CHECK -->|STD/LARGE| S5_FEATDOC
    S5_INLINE --> S5_HOOK
    S5_FEATDOC --> S5_HOOK
    S5_HOOK --> S6_ROUTING

    S6_ROUTING -->|TINY| S6_QUICK
    S6_ROUTING -->|SMALL| S6_QUICK
    S6_ROUTING -->|STANDARD| S6_EPCI
    S6_ROUTING -->|LARGE| S6_LARGE

    S6_QUICK --> S7_CHECK
    S6_EPCI --> S7_CHECK
    S6_LARGE --> S7_CHECK

    S7_CHECK -->|No| S7_SUGGEST
    S7_CHECK -->|Yes| S7_END
    S7_SUGGEST --> S7_END

    style S3_BP fill:#ffd700
    style S15_BP fill:#ffd700
    style S1_AGENT fill:#90EE90
    style S1_HOOK fill:#DDA0DD
    style S5_HOOK fill:#DDA0DD
```

---

## 2. Component Inventory

### Skills (6 total)

| Skill Reference | Existe dans src/skills/ | Charge dans workflow | Status |
|-----------------|-------------------------|----------------------|--------|
| project-memory | OUI | OUI (Step 0) | OK |
| epci-core | OUI | OUI (implicit) | OK |
| architecture-patterns | OUI | OUI (exploration) | OK |
| flags-system | OUI | OUI (Step 4) | OK |
| mcp | OUI | OUI (Step 2) | OK |
| personas | OUI | OUI (Step 2) | OK |
| [stack-skill] | OUI (4 variants) | CONDITIONNEL (auto-detect) | OK |

### Agents (2 total)

| Agent Reference | Existe dans src/agents/ | Model documente | Model recommande | Status |
|-----------------|-------------------------|-----------------|------------------|--------|
| @Explore | N/A (natif Claude) | N/A | N/A | OK |
| @clarifier | OUI | haiku | haiku | OK |

### Hooks (2 total)

| Hook Type | Valide | Actif (hooks/active/) | Execute dans workflow | Status |
|-----------|--------|----------------------|----------------------|--------|
| pre-brief | OUI | NON | OUI (Step 1) | WARN |
| post-brief | OUI | NON | OUI (Step 5) | WARN |

> **Note**: Les hooks pre-brief et post-brief sont documentes dans la commande mais n'existent pas dans `src/hooks/active/`. Cela signifie qu'ils ne seront jamais executes.

### MCP Servers

| MCP Server | Documente | Condition activation | Status |
|------------|-----------|---------------------|--------|
| Context7 | OUI | `--c7` flag OR architect/backend/doc persona | OK |
| Sequential | OUI | `--seq` flag OR architect/backend/security persona | OK |
| Magic | OUI | `--magic` flag OR frontend persona | OK |
| Playwright | OUI | `--play` flag OR frontend/qa persona | OK |

---

## 3. Feature Catalog

### Arguments/Flags

| Flag | Type | Effet | Auto-activation | Status |
|------|------|-------|-----------------|--------|
| `--turbo` | boolean | Exploration rapide, max 2 questions, @clarifier | Si .project-memory/ existe + category != LARGE | OK |
| `--rephrase` | boolean | Force reformulation du brief | N/A (explicit only) | OK |
| `--no-rephrase` | boolean | Skip reformulation | N/A (explicit only) | OK |
| `--c7` | boolean | Active Context7 MCP | persona architect/doc/backend | OK |
| `--seq` | boolean | Active Sequential MCP | persona architect/backend/security | OK |

### Modes

| Mode | Description | Declencheur | Differences |
|------|-------------|-------------|-------------|
| Standard | Exploration complete, breakpoint complet | Default | Toutes etapes executees |
| Turbo | Exploration rapide, 2 questions max | `--turbo` | @clarifier, breakpoint compact |
| TINY optimized | Skip clarification, route directe | category == TINY | Auto `/quick --autonomous` |

### Outputs

| Output | Condition | Format | Chemin |
|--------|-----------|--------|--------|
| Inline Brief | TINY/SMALL | Markdown | (response) |
| Feature Document | STANDARD/LARGE | Markdown | `docs/features/<slug>.md` |
| Memory status | .project-memory/ exists | Display | (console) |

---

## 4. Verification Results

### Universal Checks

| ID | Check | Severity | Status | Notes |
|----|-------|----------|--------|-------|
| U001 | Frontmatter YAML valide | CRITICAL | OK | --- present, description, argument-hint, allowed-tools |
| U002 | description <= 1024 chars | HIGH | OK | 203 chars |
| U003 | allowed-tools liste presente | HIGH | OK | [Read, Write, Glob, Grep, Bash, Task] |
| U004 | argument-hint documente | MEDIUM | OK | `[brief] [--turbo] [--rephrase] [--no-rephrase] [--c7] [--seq]` |
| U010 | Skills references existent | CRITICAL | OK | 6/6 skills existent |
| U011 | Skills charges au bon moment | HIGH | OK | project-memory Step 0, autres selon besoin |
| U020 | Agents references existent | CRITICAL | OK | @Explore natif, @clarifier existe |
| U021 | Modeles agents corrects | HIGH | OK | @clarifier = haiku (correct) |
| U030 | Types hooks valides | HIGH | OK | pre-brief, post-brief format valide |
| U031 | Hooks correspondent aux actifs | MEDIUM | WARN | pre/post-brief n'existent pas dans active/ |
| U040 | MCP servers documentes | MEDIUM | OK | 4 servers avec conditions |
| U050 | Flags documentes | HIGH | OK | 5 flags dans argument-hint |
| U051 | Auto-activation documentee | MEDIUM | OK | Conditions explicites pour --turbo, MCP |

### Command-Specific Checks (/brief)

| ID | Check | Severity | Status | Notes |
|----|-------|----------|--------|-------|
| BR001 | @Explore avec thoroughness thorough | CRITICAL | OK | Step 1 documente |
| BR002 | project-memory charge Step 0 | HIGH | OK | Premiere action |
| BR003 | Reformulation evaluee Step 1.5 | HIGH | OK | Conditions skip/trigger documentees |
| BR010 | Detection personas score > 0.6 | HIGH | OK | Formule documentee |
| BR011 | MCP auto-activation | MEDIUM | OK | Matrice persona-MCP |
| BR012 | Stack auto-detecte | MEDIUM | OK | Via project-memory |
| BR013 | Flags suggeres | LOW | OK | Dans breakpoint |
| BR020 | Criteres complexite documentes | CRITICAL | OK | Tableau TINY/SMALL/STD/LARGE |
| BR021 | Routing /quick pour TINY/SMALL | HIGH | OK | Step 6 conditionnel |
| BR022 | Routing /epci pour STD/LARGE | HIGH | OK | Step 6 conditionnel |
| BR030 | Inline brief TINY/SMALL | HIGH | OK | Step 5 conditionnel |
| BR031 | Feature Document STD/LARGE | HIGH | OK | Step 5 avec Write tool |
| BR032 | Breakpoint Step 3 obligatoire | HIGH | OK | MANDATORY note |
| BR040 | Mode --turbo documente | MEDIUM | OK | Section dediee |
| BR041 | @clarifier en mode turbo | MEDIUM | WARN | Mentionne dans CLAUDE.md mais pas explicite dans brief.md |

---

## 5. Scoring

### Fixed Criteria (60%)

| Critere | Poids | Score /100 | Pondere | Justification |
|---------|-------|------------|---------|---------------|
| Efficacite | 20% | 80 | 16.0 | Workflow bien structure, 7 etapes avec breakpoints. TINY mode optimise. Overhead acceptable. |
| Robustesse | 15% | 85 | 12.75 | 2 breakpoints (Step 1.5 reformulation, Step 3 analysis), validation input, conditions explicites. |
| Maintenabilite | 15% | 75 | 11.25 | 540 lignes (OK), structure claire mais quelques sections denses. Separation concerns correcte. |
| Experience Dev | 15% | 85 | 12.75 | Breakpoints detailles, suggestions IA, options claires [1]-[4]. Messages explicites. |
| Tracabilite | 10% | 80 | 8.0 | Feature Document genere, Memory status affiche. Pas de logging explicite. |
| Flexibilite | 10% | 85 | 8.5 | 5 flags, mode turbo, personas auto, MCP auto. Bonne couverture. |
| Performance | 10% | 78 | 7.8 | @Explore peut etre lent, turbo mode ameliore. Tokens ~3500 (OK < 5000). |
| Adoption | 5% | 85 | 4.25 | Documentation claire, exemples reformulation, suggestions proactives. |
| **TOTAL FIXE** | 100% | | **81.30** | |

### Adaptive Criteria (40%)

| Critere | Poids | Score /100 | Pondere | Justification |
|---------|-------|------------|---------|---------------|
| precision_routing | 30% | 90 | 27.0 | Criteres complexite tres bien documentes, routing conditionnel clair. |
| detection_auto | 25% | 85 | 21.25 | Personas avec formule, MCP matrice, stack auto-detect. Tres complet. |
| efficacite_turbo | 25% | 75 | 18.75 | Mode documente mais @clarifier pas explicitement invoque dans brief.md. |
| qualite_brief | 20% | 80 | 16.0 | Structure brief complete, acceptance criteria, reformulation vocale. |
| **TOTAL ADAPTATIF** | 100% | | **83.00** | |

### Combined Score

**82/100** = (81.30 * 0.60) + (83.00 * 0.40) = 48.78 + 33.20 = **81.98 ≈ 82**

---

## 6. Qualitative Analysis

### Points Forts

| # | Point Fort | Impact | Evidence |
|---|-----------|--------|----------|
| 1 | Systeme de reformulation vocale (Step 1.5) | HIGH | Detection artefacts vocaux, templates FEATURE/PROBLEM/DECISION |
| 2 | Double breakpoint (reformulation + analyse) | HIGH | Step 1.5 et Step 3 obligatoires |
| 3 | Detection automatique personas avec scoring | HIGH | Formule documentee, seuil 0.6 explicite |
| 4 | Integration MCP complete avec matrice | MEDIUM | 4 serveurs, conditions par persona |
| 5 | Mode TINY optimise avec routing autonome | MEDIUM | Skip clarification, /quick --autonomous |
| 6 | Suggestion proactive /rules si .claude/ absent | LOW | Step 7 |

### Points Faibles

| # | Point Faible | Gravite | Impact | Evidence |
|---|-------------|---------|--------|----------|
| 1 | Hooks pre/post-brief documentes mais inexistants | HAUTE | Hooks jamais executes | Step 1, Step 5 vs hooks/active/ |
| 2 | @clarifier mentionne en turbo mais pas explicite | MOYENNE | Confusion implementation | Section --turbo vs CLAUDE.md |
| 3 | Pas de gestion d'erreur explicite | MOYENNE | Comportement si exploration echoue? | Absence try/catch ou fallback |
| 4 | Step 4 (Complexity Finalization) redondant | BASSE | Deja evalue en Step 2 | Step 2 vs Step 4 |
| 5 | Flags MCP (--magic, --play) non documentes dans argument-hint | BASSE | Incoherence documentation | argument-hint vs MCP section |

### Model Verification

| Agent | Model documente | Model recommande | Justification si different | Status |
|-------|-----------------|------------------|---------------------------|--------|
| @clarifier | haiku | haiku | - | OK |
| @Explore | N/A (natif) | N/A | Agent natif Claude Code | OK |

### Complexity Analysis

| Metrique | Valeur | Evaluation |
|----------|--------|------------|
| LOC (commande) | 540 | OK (< 1000) |
| Tokens estimes | ~3500 | OK (< 5000) |
| Nombre references externes | 8 | OK (< 20) |
| Profondeur nesting max | 3 | OK (< 4) |
| Nombre breakpoints | 2 | INFO |
| Nombre agents invoques | 2 | INFO |

### Analyse des Lourdeurs

| Element | Probleme | Suggestion |
|---------|----------|------------|
| Step 1.5 Reformulation | Section longue avec exemples | Deplacer exemples vers skill reference |
| Step 3 Breakpoint format | Template tres detaille (30+ lignes) | Externaliser dans skill breakpoint-metrics |
| Step 5 Feature Document | Template inline | Reference externe ou skill |

---

## 7. Version Coherence

### References croisees

| Source | Version/Compte | Status |
|--------|----------------|--------|
| CLAUDE.md (skills) | 25 skills mentionnes | brief reference 6 core + 1 stack = OK |
| CLAUDE.md (agents) | 12 agents | brief reference 1 (@clarifier) + 1 natif = OK |
| CLAUDE.md (commandes) | 11 commandes | /brief = OK |
| CLAUDE.md version | 4.5.0 | Sync |

### Elements obsoletes

| Element | Probleme | Action |
|---------|----------|--------|
| Hook pre-brief | Documente mais inexistant | Creer hook ou supprimer reference |
| Hook post-brief | Documente mais inexistant | Creer hook ou supprimer reference |

---

## 8. Recommendations

### Priorite Critique (immediate)

| # | Recommandation | Impact | Effort |
|---|----------------|--------|--------|
| 1 | Creer ou supprimer references aux hooks pre/post-brief | HIGH | LOW |

### Priorite Haute (prochain sprint)

| # | Recommandation | Impact | Effort |
|---|----------------|--------|--------|
| 1 | Expliciter invocation @clarifier dans section --turbo | HIGH | LOW |
| 2 | Ajouter gestion erreur si @Explore echoue | MEDIUM | MEDIUM |
| 3 | Ajouter --magic et --play dans argument-hint | MEDIUM | LOW |

### Priorite Moyenne (roadmap)

| # | Recommandation | Impact | Effort |
|---|----------------|--------|--------|
| 1 | Fusionner Step 2 et Step 4 (redondance complexite) | MEDIUM | MEDIUM |
| 2 | Externaliser templates longs vers skills references | MEDIUM | MEDIUM |
| 3 | Ajouter metriques de temps dans breakpoint | LOW | LOW |

### Priorite Basse (nice to have)

| # | Recommandation | Impact | Effort |
|---|----------------|--------|--------|
| 1 | Ajouter mode --dry-run pour preview sans execution | LOW | MEDIUM |
| 2 | Support pour brief depuis fichier externe (chemin) | LOW | LOW |

---

## Annexes

### A. Files Analyzed

**Command:**
- src/commands/brief.md (540 lines)

**Skills:**
- src/skills/core/project-memory/SKILL.md
- src/skills/core/epci-core/SKILL.md
- src/skills/core/architecture-patterns/SKILL.md
- src/skills/core/flags-system/SKILL.md
- src/skills/mcp/SKILL.md
- src/skills/personas/SKILL.md

**Agents:**
- src/agents/clarifier.md

**Configuration:**
- docs/audits/config/scoring-matrix.yaml
- docs/audits/config/command-checks.yaml
- CLAUDE.md

### B. Commands Used

```bash
# Date
date +%Y-%m-%d

# Line count
wc -l src/commands/brief.md

# Word count
cat src/commands/brief.md | wc -w

# Skills listing
find src/skills -name "SKILL.md"

# Agents listing
ls src/agents/*.md

# Hooks listing
ls -la src/hooks/active/

# Hook references
grep -r "(pre|post)-brief" src/hooks/
```

### C. Scoring Summary

```
Fixed Score:    81.30 / 100 (weight: 60%)
Adaptive Score: 83.00 / 100 (weight: 40%)
─────────────────────────────────────────
FINAL SCORE:    82 / 100 (Bon)

Interpretation: Ameliorations mineures recommandees
```
