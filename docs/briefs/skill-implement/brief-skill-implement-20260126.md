# Brief — Skill /implement v6 Refonte

> **Version**: 1.0
> **Date**: 2026-01-26
> **EMS Final**: 82/100
> **Template**: feature
> **Auteur**: Brainstorm EPCI v6.0

---

## 1. Contexte

### 1.1 Situation Actuelle

Le skill `/implement` existe dans EPCI v6.0 avec :
- Structure steps/ (00-07)
- Workflow EPCI de base (E-P-C-I-M)
- Intégration partielle des core skills

### 1.2 Problème

L'intégration des **stack skills** et des **core skills** n'est pas suffisamment documentée ni contraignante. Le skill manque de :
- Section dédiée documentant l'utilisation obligatoire des bonnes pratiques
- Injection automatique des conventions de stack
- Architecture multi-agents optimisée (parallèle vs séquentiel)
- Patterns TDD modernes pour AI-assisted development

### 1.3 Objectif

Refondre le skill `/implement` pour EPCI v6.0 avec :
1. **Intégration obligatoire** des stack skills (auto-inject rules)
2. **Utilisation systématique** des 6 core skills
3. **Section dédiée** "Stack & Core Skills Integration" dans SKILL.md
4. **Architecture multi-agents** avec parallel fan-out et critic synthesis
5. **TDD strict** avec pre-code check et tdd-enforcer

---

## 2. Décisions Validées

| # | Domaine | Décision | Justification |
|---|---------|----------|---------------|
| D1 | Stack Skills | Auto-inject rules | Les rules-templates du stack détecté sont injectées automatiquement |
| D2 | Input Insuffisant | Clarify inline | clarification-engine pose 2-3 questions pour enrichir |
| D3 | TDD Rigueur | Strict TDD | RED-GREEN-REFACTOR obligatoire, coverage 80% |
| D4 | Documentation | Triple couverture | Section dédiée + MANDATORY RULES + Steps explicites |
| D5 | Breakpoints | 4 breakpoints | E (findings), P (validation), C (progress LARGE), I (review) |
| D6 | Format Section | Tableau + Mermaid | Clarté visuelle + référence tabulaire |
| D7 | Security/QA | Conditionnel intelligent | security-auditor si auth, qa-reviewer si >5 tests |
| D8 | Lien /spec | Lecture PRD.json | Charger index.md + PRD.json automatiquement |
| D9 | Mode Turbo | Oui, réduit | 1 breakpoint, parallel reviews, skip E si plan fourni |
| D10 | Reviews | Parallel fan-out + Critic | Reviews en parallèle puis synthèse |
| D11 | TDD Hook | Pre-code check | "Test rouge existe? Sinon générer tests d'abord" |
| D12 | Agent Context | Stack conventions héritées | Tous les agents reçoivent le contexte stack |
| D13 | Checkpoint | Format enrichi | history, variables, metadata dans state.json |

---

## 3. Architecture Cible

### 3.1 Workflow Complet

```
┌─────────────────────────────────────────────────────────────────────────┐
│                     /IMPLEMENT WORKFLOW v6 REFONTE                       │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  INIT (step-00)                                                          │
│  ├─ Input detection (@plan, @spec, slug-only)                            │
│  ├─ Stack detection → load rules-templates                               │
│  ├─ Complexity routing (TINY/SMALL → /quick)                             │
│  └─ Clarify inline si clarity < 60%                                      │
│     └─ BREAKPOINT: Input validation                                      │
│                                                                          │
│  EXPLORE [E] (step-01)                                                   │
│  ├─ Read-only codebase analysis                                          │
│  ├─ Pattern detection (conventions, architecture)                        │
│  └─ Load project-memory context                                          │
│     └─ BREAKPOINT: Exploration findings                                  │
│                                                                          │
│  PLAN [P] (step-02)                                                      │
│  ├─ PRD.json parsing si fourni                                           │
│  ├─ Task decomposition (15-30 min atomic)                                │
│  ├─ DAG des dépendances                                                  │
│  └─ @plan-validator (Opus)                                               │
│     └─ BREAKPOINT: Plan validation                                       │
│                                                                          │
│  CODE [C] (step-03)                                                      │
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │ PRE-CHECK: Test rouge existe? Sinon → générer tests d'abord      │   │
│  ├──────────────────────────────────────────────────────────────────┤   │
│  │ TDD CYCLE (per task):                                             │   │
│  │   RED    → Write failing test (tdd-enforcer validates)            │   │
│  │   GREEN  → Minimal code to pass                                   │   │
│  │   REFACTOR → Clean up (stack conventions applied)                 │   │
│  │   VERIFY → Full test suite                                        │   │
│  └──────────────────────────────────────────────────────────────────┘   │
│     └─ BREAKPOINT (LARGE only): Code progress checkpoint                 │
│                                                                          │
│  INSPECT [I] (step-04)                                                   │
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │ PARALLEL FAN-OUT:                                                 │   │
│  │   @code-reviewer (Opus) ─┐                                        │   │
│  │   @security-auditor* ────┼─→ Critic/Synthesizer                   │   │
│  │   @qa-reviewer* ─────────┘                                        │   │
│  │                                                                   │   │
│  │ * = Conditionnel (auth patterns / >5 tests / LARGE)               │   │
│  ├──────────────────────────────────────────────────────────────────┤   │
│  │ CRITIC SYNTHESIS:                                                 │   │
│  │   → Merge findings, dedupe, resolve conflicts                     │   │
│  │   → Severity classification (Critical/Important/Minor)            │   │
│  │   → Auto-fix Minor, Human decision for Critical                   │   │
│  └──────────────────────────────────────────────────────────────────┘   │
│     └─ BREAKPOINT: Review approval                                       │
│                                                                          │
│  DOCUMENT (step-05)                                                      │
│  └─ @doc-generator (Sonnet)                                              │
│  └─ Update Feature Document                                              │
│                                                                          │
│  FINISH (step-06)                                                        │
│  └─ Final validation                                                     │
│  └─ Commit context generation                                            │
│                                                                          │
│  MEMORY [M] (step-07)                                                    │
│  └─ Generate summary (1-2 sentences)                                     │
│  └─ Collect modified_files, test_count                                   │
│  └─ Update index.json (state-manager)                                    │
│  └─ Hook post-implement                                                  │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

### 3.2 Input Detection

```
INPUT
├── @.claude/plans/*.md → PLAN-FIRST workflow
│   └─ Native Claude Code plan, skip E-P, go directly to CODE
├── @docs/specs/*.md → SPEC-FIRST workflow
│   └─ Spec exists, do minimal planning then CODE
│   └─ Load PRD.json si présent
└── feature-slug only → FULL workflow (E-P-C-I-M)
    └─ Full Explore + Plan phases first
    └─ Clarify inline si clarity < 60%
```

### 3.3 Complexity Routing

| Complexity | LOC | Files | Workflow |
|------------|-----|-------|----------|
| TINY | < 50 | 1-2 | → /quick (step-00b-turbo) |
| SMALL | 50-200 | 1-3 | → /quick (step-00b-turbo) |
| STANDARD | 200-500 | 2-5 | → Full EPCI |
| LARGE | 500+ | 5+ | → Full EPCI + security + 4 breakpoints |

---

## 4. Stack & Core Skills Integration

### 4.1 Stack Skills (Auto-injected)

| Stack | Detection | Rules Injected | Phase Usage |
|-------|-----------|----------------|-------------|
| python-django | `manage.py`, django in requirements | backend-django, testing-pytest, api-drf | C, I |
| javascript-react | react in package.json | frontend-react, testing-vitest, state-management | C, I |
| php-symfony | symfony in composer.json | backend-symfony, testing-phpunit, security-symfony | C, I |
| java-springboot | spring-boot in pom.xml/gradle | backend-spring, testing-junit, security-spring | C, I |
| frontend-editor | tailwind.config.* | styling-tailwind, accessibility | C |

**Injection Protocol**:
1. Detection en phase INIT via patterns fichiers
2. Chargement des rules-templates dans le contexte global
3. Transmission aux sub-agents (@code-reviewer, @security-auditor, etc.)
4. Application pendant phases CODE et INSPECT

### 4.2 Core Skills (Auto-triggered)

| Core Skill | Trigger | Phase | Purpose |
|------------|---------|-------|---------|
| state-manager | Always | INIT, M | Create/update feature state, checkpoints |
| complexity-calculator | Always | INIT | Routing decision (→ /quick ou full EPCI) |
| project-memory | Always | E | Load conventions, patterns, velocity calibration |
| clarification-engine | If clarity < 60% | INIT | Inline clarification (2-3 questions max) |
| tdd-enforcer | Always | C | Validate TDD cycle compliance, pre-code check |
| breakpoint-system | At phase transitions | E, P, C*, I | Interactive checkpoints (* = LARGE only) |

### 4.3 Integration Flow

```mermaid
graph TD
    INIT[INIT] --> |stack detection| STACK[Load Stack Skills]
    INIT --> |load state| SM[state-manager]
    INIT --> |complexity check| CC[complexity-calculator]

    STACK --> E[EXPLORE]
    SM --> E
    CC --> |STANDARD/LARGE| E
    CC --> |TINY/SMALL| QUICK[→ /quick]

    E --> |load context| PM[project-memory]
    PM --> P[PLAN]

    P --> |validate| PV[@plan-validator]
    PV --> C[CODE]

    C --> |enforce| TDD[tdd-enforcer]
    TDD --> |stack conventions| IMPL[Implementation]

    IMPL --> I[INSPECT]
    I --> |parallel| CR[@code-reviewer]
    I --> |parallel, conditional| SA[@security-auditor]
    I --> |parallel, conditional| QA[@qa-reviewer]

    CR --> SYNTH[Critic Synthesis]
    SA --> SYNTH
    QA --> SYNTH

    SYNTH --> D[DOCUMENT]
    D --> F[FINISH]
    F --> M[MEMORY]
    M --> SM
```

---

## 5. Multi-Agent Architecture

### 5.1 Review Orchestration Pattern

Basé sur les recherches 2025-2026 : **Parallel fan-out + Critic synthesis**

```
                    ┌─────────────────┐
                    │   Orchestrator  │
                    │  (main thread)  │
                    └────────┬────────┘
                             │
            ┌────────────────┼────────────────┐
            │                │                │
            ▼                ▼                ▼
    ┌───────────────┐ ┌───────────────┐ ┌───────────────┐
    │ @code-reviewer│ │@security-audit│ │  @qa-reviewer │
    │    (Opus)     │ │    (Opus)*    │ │   (Sonnet)*   │
    └───────┬───────┘ └───────┬───────┘ └───────┬───────┘
            │                │                │
            │    PARALLEL    │                │
            └────────────────┼────────────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │     Critic      │
                    │   Synthesizer   │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ Unified Review  │
                    │    Report       │
                    └─────────────────┘

* = Conditionnel
```

### 5.2 Conditional Agent Triggers

| Agent | Trigger Condition |
|-------|-------------------|
| @code-reviewer | Always |
| @security-auditor | Files match `**/auth/**`, `**/security/**`, `**/api/**`, keywords: password, secret, jwt, oauth |
| @qa-reviewer | >5 test files OR complexity LARGE OR integration/E2E tests detected |

### 5.3 Critic Synthesis Rules

1. **Merge findings** from all reviewers
2. **Deduplicate** similar issues
3. **Classify severity**: Critical / Important / Minor
4. **Auto-fix**: Minor issues (formatting, naming)
5. **Human decision**: Critical issues (security, architecture)
6. **Generate unified report** with actionable items

---

## 6. TDD Workflow Enrichi

### 6.1 Pre-Code Check (Nouveau)

Avant toute implémentation :

```
IF no failing test exists for current task:
  → Generate test skeleton based on acceptance criteria
  → Run test to confirm RED state
  → Only then proceed to GREEN phase
```

### 6.2 TDD Cycle avec tdd-enforcer

```
┌─────────────────────────────────────────────────────────────────┐
│                    TDD CYCLE (per task)                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  1. PRE-CHECK                                                    │
│     └─ tdd-enforcer: "Test rouge existe?"                        │
│     └─ Si non → générer test basé sur AC                         │
│                                                                  │
│  2. RED                                                          │
│     └─ Write failing test                                        │
│     └─ tdd-enforcer: validate test fails for right reason        │
│                                                                  │
│  3. GREEN                                                        │
│     └─ Minimal implementation                                    │
│     └─ Stack conventions applied (from rules-templates)          │
│     └─ tdd-enforcer: validate test passes                        │
│                                                                  │
│  4. REFACTOR                                                     │
│     └─ Clean up without changing behavior                        │
│     └─ Apply patterns from project-memory                        │
│     └─ tdd-enforcer: validate all tests still pass               │
│                                                                  │
│  5. VERIFY                                                       │
│     └─ Run full test suite                                       │
│     └─ Coverage check (target: 80%)                              │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 7. State Management Enrichi

### 7.1 Checkpoint Format (state.json)

```json
{
  "$schema": "https://epci.dev/schemas/feature-state-v2.json",
  "feature_id": "auth-oauth-google",
  "version": 2,

  "lifecycle": {
    "status": "in_progress",
    "current_phase": "code",
    "current_step": "step-03-code",
    "completed_phases": ["explore", "plan"],
    "completed_steps": ["step-00-init", "step-01-explore", "step-02-plan"],
    "created_at": "2026-01-26T10:00:00Z",
    "last_update": "2026-01-26T14:30:00Z",
    "created_by": "/implement",
    "last_updated_by": "/implement"
  },

  "spec": {
    "prd_json": "docs/specs/auth-oauth-google/auth-oauth-google.prd.json",
    "prd_md": "docs/specs/auth-oauth-google/index.md",
    "complexity": "STANDARD",
    "total_tasks": 6,
    "estimated_minutes": 180
  },

  "execution": {
    "tasks": {
      "completed": ["US-001", "US-002"],
      "current": "US-003",
      "pending": ["US-004", "US-005", "US-006"],
      "failed": []
    },
    "tdd_cycles": 12,
    "last_error": null
  },

  "artifacts": {
    "feature_doc": "docs/features/auth-oauth-google.md",
    "test_files": ["tests/integration/oauth.test.ts"],
    "modified_files": ["src/auth/oauth.ts", "src/auth/types.ts"]
  },

  "history": [
    {"phase": "explore", "action": "codebase_scan", "timestamp": "..."},
    {"phase": "plan", "action": "plan_validated", "timestamp": "..."}
  ],

  "variables": {
    "stack_detected": "javascript-react",
    "rules_loaded": ["frontend-react", "testing-vitest"],
    "reviews_pending": ["code", "security"]
  },

  "metadata": {
    "breakpoints_shown": 2,
    "clarifications_asked": 1,
    "errors_encountered": 0
  },

  "checkpoints": [
    {
      "id": "ckpt-001",
      "phase": "plan",
      "step": "step-02-plan",
      "timestamp": "2026-01-26T11:00:00Z",
      "git_ref": "abc123",
      "resumable": true
    }
  ],

  "improvements": []
}
```

---

## 8. Mode Turbo (--turbo)

### 8.1 Différences vs Mode Standard

| Aspect | Standard | Turbo |
|--------|----------|-------|
| Breakpoints | 4 (E, P, C*, I) | 1 (pre-commit only) |
| Reviews | Sequential then parallel | All parallel |
| Explore phase | Full | Skip si @plan fourni |
| Plan phase | Full + @plan-validator | Minimal |
| Auto-fix | Minor only | Minor + Important |
| Model for implementation | Opus | Sonnet (@implementer) |

### 8.2 Turbo Workflow

```
IF --turbo flag:
  → Skip E if @plan provided
  → Minimal P (no @plan-validator)
  → All reviews in parallel (single Task call)
  → Auto-fix Important issues
  → Single breakpoint (pre-commit)
  → Use @implementer (Sonnet) for speed
```

---

## 9. Fichiers a Modifier/Creer

### 9.1 Modifications SKILL.md

| Section | Action |
|---------|--------|
| Frontmatter | Mettre a jour description |
| MANDATORY RULES | Ajouter regles stack skills |
| Workflow Overview | Enrichir avec 4 breakpoints |
| **NEW: Stack & Core Skills Integration** | Ajouter section complete |
| Decision Tree | Ajouter turbo mode |
| Steps | Mettre a jour liens |

### 9.2 Modifications Steps

| Fichier | Modifications |
|---------|---------------|
| step-00-init.md | Stack detection, clarification inline |
| step-03-code.md | Pre-code check TDD, stack conventions |
| step-04-review.md | Parallel fan-out, critic synthesis |
| step-04b-security.md | Conditional trigger documentation |
| step-04c-qa.md | Conditional trigger documentation |

### 9.3 Nouvelles References

| Fichier | Contenu |
|---------|---------|
| references/stack-integration.md | Detail injection rules-templates |
| references/multi-agent-review.md | Parallel fan-out + critic pattern |
| references/turbo-mode.md | Documentation mode turbo |

---

## 10. Criteres d'Acceptation

### 10.1 Fonctionnels

- [ ] Stack skills auto-detectes et rules injectees
- [ ] Core skills invoques aux bons moments
- [ ] Section "Stack & Core Skills Integration" presente dans SKILL.md
- [ ] 4 breakpoints fonctionnels (E, P, C*, I)
- [ ] Pre-code check TDD avant implementation
- [ ] Reviews en parallele avec synthese
- [ ] Mode turbo fonctionnel
- [ ] State enrichi avec history, variables, metadata

### 10.2 Documentation

- [ ] SKILL.md mis a jour avec toutes les sections
- [ ] Steps mis a jour avec invocations explicites
- [ ] References ajoutees
- [ ] Mermaid diagram present

### 10.3 Qualite

- [ ] Validation passe (`python src/scripts/validate_all.py`)
- [ ] Tokens < 5000 pour SKILL.md
- [ ] Coherence avec /spec et /quick
- [ ] Tests manuels reussis

---

## 11. Contraintes

| Contrainte | Valeur | Raison |
|------------|--------|--------|
| Tokens SKILL.md | < 5000 | Limite plugin |
| Breakpoints max | 4 | Eviter friction |
| Clarification questions | 3 max | Eviter surcharge |
| TDD coverage | 80% | Qualite code |
| Reviews parallel | 3 agents max | Performance |
| Turbo breakpoint | 1 seul | Rapidite |

---

## 12. Risques

| Risque | Impact | Mitigation |
|--------|--------|------------|
| Stack detection incorrecte | Medium | Fallback patterns, allow manual override |
| Reviews trop longs | Medium | Timeouts, mode turbo |
| State corruption | High | Validation JSON schema, backups |
| Breakpoint fatigue | Low | Mode turbo, skip option |
| TDD trop rigide | Low | Mode turbo assouplit |

---

## 13. Routing Suggere

**Complexity estimee**: STANDARD (200-500 LOC, 3-5 fichiers)

**Workflow recommande**: `/spec` puis `/implement`

**Prochaine etape**: Executer `/spec skill-implement @docs/briefs/skill-implement/brief-skill-implement-20260126.md`

---

*Document genere par Brainstorm EPCI v6.0*
*EMS Final: 82/100 | Iterations: 4 | Recherches Perplexity: 5*
