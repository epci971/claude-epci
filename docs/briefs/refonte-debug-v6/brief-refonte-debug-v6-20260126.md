# Brief PRD v3.0 — Refonte Skill /debug v6

> **Date**: 2026-01-26
> **Auteur**: Brainstorm Session EPCI
> **EMS Final**: 81/100
> **Complexite**: STANDARD
> **Routing**: /spec -> /implement

---

## 1. Resume Executif

### Contexte

Le skill `/debug` v6 actuel est un skeleton de 52 LOC avec un placeholder "TODO: Implement in Phase 2+". La commande `/debug` v5.6 (553 LOC) contenait un workflow complet mais en format legacy non compatible avec l'architecture EPCI v6.

### Probleme

Le debugging "par tatonnement" est inefficace et conduit a des corrections non systematiques, sans capitalisation sur les bugs precedents.

### Solution

Migrer `/debug` v5.6 vers un skill EPCI v6 moderne integrant:
- **Tree of Thought (ToT)** avec hypotheses structurees et scoring
- **Routing adaptatif** (Trivial/Quick/Complex)
- **Recherche multi-sources** (Context7 -> WebSearch -> Perplexity)
- **Fallback automatique** entre hypotheses
- **Integration complete** avec core skills et subagents v6

### Valeur Attendue

- Reduction du temps de debug de 50-70% (benchmark industrie RCA)
- Capitalisation des patterns bug->cause via project-memory
- Approche scientifique reproducible

---

## 2. Decisions Architecturales

| ID | Decision | Choix Retenu | Justification |
|----|----------|--------------|---------------|
| D1 | Format Hypothese | Schema structure JSON | Permet scoring, ranking, et fallback automatise |
| D2 | Evaluation | Ranking comparatif (pairwise) | Plus stable que scoring absolu avec LLM modernes |
| D3 | Search Strategy | Best-First | Hypothese top confidence exploree en premier |
| D4 | Feedback Loop | project-memory | Stockage pattern->cause pour reutilisation |
| D5 | Research Layer | Multi-source cascade | Context7 -> WebSearch -> Perplexity (graceful degradation) |
| D6 | Output Format | Concise actionable | 2-3 hypotheses max, fix steps clairs |

---

## 3. Schema Hypothese (ToT)

```json
{
  "id": "H1",
  "hypothesis": "Cache returns stale data due to TTL misconfiguration",
  "confidence": 75,
  "rationale": "Recent config change in commit abc123 modified cache settings",
  "evidence": [
    "Stack trace shows CacheService.get() at line 42",
    "Similar bug #123 had same root cause"
  ],
  "testable_prediction": "Adding logging will show outdated timestamp in cached responses",
  "quick_check": "Add console.log in CacheService.get() before return",
  "files_to_investigate": [
    "src/services/CacheService.ts",
    "config/cache.yml"
  ],
  "status": "pending"
}
```

---

## 4. Workflow Detaille

### Step 0: Input Clarification (Conditionnel)

**Trigger**: `clarity_score < 0.6 AND NOT --no-clarify`
**Core skill**: `clarification-engine`
**Skip si**: Input = pure stack trace ou error code

### Phase 1: Diagnostic (OBLIGATOIRE)

#### 1.1 Gather Evidence

| Source | Donnees Collectees |
|--------|-------------------|
| Error | Message, stack trace complet |
| Reproduction | Steps, frequence (Always/Sometimes/Rare) |
| Changes | `git log --since="1 week" --oneline`, commits recents |
| History | `project-memory.recall_similar_bugs(error_pattern)` |

#### 1.2 Research (Multi-source)

```
RESEARCH PIPELINE:

1. Detect framework/library in error message
   |
   +-> Framework detected?
       |
       +-> YES: Query Context7 MCP
       |        "{error} {framework} {version}"
       |        |
       |        +-> results >= 3 AND confidence >= 60%?
       |            |
       |            +-> YES: Use results, continue
       |            +-> NO: Fallback to WebSearch
       |
       +-> NO: Skip to WebSearch

2. WebSearch fallback
   Query: "{error} site:stackoverflow.com OR site:github.com/issues"
   Filter: < 2 years, official docs prioritized
   |
   +-> results >= 5?
       |
       +-> YES: Use results, continue
       +-> NO: Propose Perplexity prompt

3. Perplexity (suggested, not auto)
   Mode: Deep Research si error rare/complexe
   Prompt template: "{error} {stack} root cause solution 2025 2026"
```

#### 1.3 Build Thought Tree (ToT)

1. Generate 3-4 hypotheses avec schema complet
2. Rank par confidence % (descending)
3. Chaque hypothese avec `testable_prediction` + `quick_check`
4. Marquer evidence sources

#### 1.4 Evaluate Routing

**Core skill**: `complexity-calculator`

| Route | Causes | LOC | Files | Uncertainty | Trigger |
|-------|--------|-----|-------|-------------|---------|
| TRIVIAL | 1 obvious | <10 | 1 | <5% | Typo, missing import |
| QUICK | 1 | <50 | 1-2 | <20% | Single component bug |
| COMPLEX | 2+ | >=50 | 3+ | >=20% | Multi-component, unclear |

**Rule**: >= 2 criteres COMPLEX -> Route COMPLEX

---

### Route A: Trivial

```
INPUT -> Diagnostic -> TRIVIAL detected
    |
    +-> Apply fix directly (no breakpoint)
    +-> Output inline summary
    +-> END

OUTPUT:
  +-- BUG FIXED (Trivial) --+
  | Cause: [cause]          |
  | Fix: [description]      |
  | File: path:line         |
  +-------------------------+
```

---

### Route B: Quick

```
INPUT -> Diagnostic -> QUICK detected
    |
    +-> Display simplified Thought Tree (top 2 hypotheses)
    +-> TDD Cycle (tdd-enforcer):
    |     RED: Write regression test
    |     GREEN: Implement fix
    |     VERIFY: Run tests
    +-> Output summary
    +-> END

OUTPUT:
  +-- BUG FIXED (Quick) ----+
  | Root Cause              |
  | [Hypothesis + evidence] |
  |                         |
  | Solution Applied        |
  | [Fix description]       |
  |                         |
  | Files Modified          |
  | - path (lines X-Y)      |
  |                         |
  | Verification: Pass      |
  +-------------------------+
```

---

### Route C: Complex

```
INPUT -> Diagnostic -> COMPLEX detected
    |
    +-> Generate Solution Scoring
    |     Multiple solutions ranked by:
    |     - Simplicity (25%)
    |     - Risk (25%)
    |     - Time (25%)
    |     - Maintainability (25%)
    |
    +-> BREAKPOINT (breakpoint-system type: diagnostic)
    |     Display: Root cause tree + Solutions ranked
    |     Ask: "Quelle solution implementer?"
    |     Options: [Solution 1] [Solution 2] [Details] [Cancel]
    |
    +-> User selects solution
    |
    +-> Implement with TDD
    |
    +-> Reviews (parallel):
    |     @code-reviewer (always)
    |     @security-auditor (if auth/security patterns)
    |     @qa-reviewer (if >= 3 tests added)
    |
    +-> Generate Debug Report (unless --no-report)
    |     Location: docs/debug/{slug}-{date}.md
    |
    +-> END

FALLBACK LOOP:
  IF prediction REJECTED during investigation:
    -> Mark hypothesis as "infirmed"
    -> Adjust confidence of remaining hypotheses
    -> Select next best hypothesis
    -> LOOP

  IF all hypotheses exhausted:
    -> Generate new hypotheses based on findings
    -> OR escalate to user with missing info questions
    -> OR suggest targeted Perplexity research
```

---

### Post-Debug

```
ALL ROUTES -> Post-Debug
    |
    +-> project-memory.store_pattern({
    |     error_pattern: "[pattern]",
    |     root_cause: "[cause]",
    |     solution: "[fix]",
    |     files: ["paths"],
    |     timestamp: "ISO8601"
    |   })
    |
    +-> Execute hook post-debug
    |     Data: mode, slug, cause, files, duration
    |
    +-> IF --commit flag:
          Write .epci-commit-context.json
          Suggest: "Run /commit to commit fix"
```

---

## 5. Integrations

### Core Skills

| Skill | Phase | Usage |
|-------|-------|-------|
| `clarification-engine` | Step 0 | Nettoyage input vocal/confus |
| `complexity-calculator` | Step 1.4 | Routing Trivial/Quick/Complex |
| `breakpoint-system` | Complex | Type "diagnostic" pour choix solution |
| `tdd-enforcer` | Quick/Complex | Cycle RED-GREEN-REFACTOR-VERIFY |
| `project-memory` | All | History lookup + pattern storage |

### Subagents

| Agent | Model | Trigger |
|-------|-------|---------|
| `@clarifier` | Haiku | --turbo mode, diagnostic rapide |
| `@code-reviewer` | Opus | Complex mode, toujours invoque |
| `@security-auditor` | Opus | Files match `**/auth/**`, `**/security/**`, keywords |
| `@qa-reviewer` | Sonnet | >= 3 tests ajoutes |

### MCP Servers

| Server | Usage | Fallback |
|--------|-------|----------|
| Context7 | Documentation lookup pour errors framework | WebSearch |
| Sequential | Multi-step reasoning (optional) | Native Claude thinking |

---

## 6. Flags

| Flag | Default | Description |
|------|---------|-------------|
| `--full` | off | Force Complex mode (skip routing) |
| `--turbo` | off | @clarifier Haiku, auto-apply best solution, skip breakpoint |
| `--no-report` | off | Complex mode sans Debug Report |
| `--no-clarify` | off | Skip input clarification |
| `--commit` | off | Prepare commit context apres fix |
| `--context <path>` | - | Link vers Feature Document existant |

### --turbo Mode Details

| Aspect | Standard | Turbo |
|--------|----------|-------|
| Diagnostic model | Sonnet | @clarifier (Haiku) |
| Thought tree | Full (3-4 H) | Simplified (top 2) |
| Solution selection | Multiple + scoring | Best only (auto-apply) |
| Breakpoint | Required (Complex) | Skipped |
| Confidence threshold | N/A | 70% (fallback si lower) |
| Report | Full Debug Report | Summary only |

---

## 7. Structure Fichiers

```
src/skills/debug/
+-- SKILL.md                      # Principal (~300-400 LOC)
+-- steps/
|   +-- step-00-clarify.md        # Input clarification
|   +-- step-01-evidence.md       # Gather evidence
|   +-- step-02-research.md       # Multi-source research
|   +-- step-03-thought-tree.md   # Build ToT hypotheses
|   +-- step-04-routing.md        # Evaluate & route
|   +-- step-05-trivial.md        # Route A
|   +-- step-06-quick.md          # Route B
|   +-- step-07-complex.md        # Route C
|   +-- step-08-post.md           # Post-debug
+-- references/
    +-- hypothesis-schema.md      # ToT JSON schema
    +-- routing-matrix.md         # Criteria matrix
    +-- research-workflow.md      # Context7 -> Web -> Perplexity
    +-- solution-scoring.md       # Scoring formula
    +-- debug-report-template.md  # Output template
    +-- examples.md               # 3 examples (1 per route)
```

---

## 8. Criteres de Succes

| Critere | Target | Mesure |
|---------|--------|--------|
| Routing accuracy | >90% | Bugs correctement routes |
| ToT compliance | 100% | Hypotheses suivent schema |
| Research fallback | Graceful | Fonctionne si MCP down |
| Regression tests | 100% | Chaque fix a un test |
| Memory integration | Active | Patterns stockes |
| User satisfaction | >4/5 | Feedback post-debug |

---

## 9. Hors Scope

- Debugging CSS/layout frontend-only
- Performance profiling (-> /improve)
- Refactoring (-> /refactor)
- Auto-commit du Debug Report
- Integration IDE (breakpoints visuels)

---

## 10. Risques et Mitigations

| Risque | Impact | Mitigation |
|--------|--------|------------|
| Context7 MCP indisponible | Medium | Pipeline multi-source avec fallback |
| Hypotheses toutes fausses | Medium | Boucle de generation + escalade user |
| Overhead Complex pour bugs simples | Low | Routing adaptatif strict |
| Tokens excessifs ToT | Low | Limiter a 4 hypotheses max |

---

## 11. Next Steps

1. **Run `/spec`** sur ce brief pour generer PRD.json + taches granulaires
2. **Run `/implement`** pour execution STANDARD avec phases EPCI
3. **Valider** avec `python src/scripts/validate_all.py`
4. **Commit** avec scope `(skills)`: `feat(skills): implement /debug v6 with ToT`

---

## 12. Sources

### Recherches Perplexity Integrees

1. **Tree of Thought Debugging** - Patterns ToT 2025-2026
2. **Automated Root Cause Analysis** - Methodes RCA AI-assisted
3. **Claude MCP / Context7** - Integration documentation lookup
4. **Scientific Method Debugging** - Approche hypothesis-driven

### Documents Analyses

- `/archive/5.6/commands/debug.md` - Commande legacy (553 LOC)
- `/docs/migration/50-60/epci-v6-brainstorm-report.md` - Architecture v6
- `/docs/migration/50-60/epci-v6-implementation-plan.md` - Plan implementation

---

*Brief genere par /brainstorm EPCI v6.0*
*EMS: 81/100 | Iterations: 3 | Date: 2026-01-26*
