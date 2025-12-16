# Feature Document — F05: Clarification Intelligente

> **Slug**: `f05-clarification-intelligente`
> **Category**: STANDARD
> **Date**: 2025-12-16
> **CDC Source**: docs/migration/30-31/cdc/CDC-F05-Clarification-Intelligente.md

---

## §1 — Functional Brief

### Context

La phase de clarification dans `/epci-brief` pose actuellement des questions génériques identiques pour tous les projets. Cette feature transforme cette phase en une **conversation contextuelle intelligente** qui:
- Analyse le contexte projet via Project Memory (F04)
- Détecte les features similaires passées
- Génère des questions spécifiques et pertinentes (max 3)
- S'adapte à la persona active (F09, quand disponible)

### Detected Stack

- **Framework**: Claude Code Plugin (EPCI v3.5)
- **Language**: Python 3 + Markdown
- **Patterns**: Command pattern, Skill pattern, Project Memory integration
- **Dependencies**: F04 (Project Memory) ✅ DONE, F09 (Personas) ❌ NOT YET

### Identified Files

| File | Action | Risk | Description |
|------|--------|------|-------------|
| `src/project-memory/clarification_analyzer.py` | Create | Low | Keyword extraction, domain detection |
| `src/project-memory/similarity_matcher.py` | Create | Medium | Feature similarity scoring |
| `src/project-memory/question_generator.py` | Create | Medium | Question templates and generation |
| `src/project-memory/manager.py` | Modify | Low | Add query methods for similarity |
| `src/commands/epci-brief.md` | Modify | Medium | Update Step 2 to use intelligent clarification |
| `src/skills/core/clarification-intelligente/SKILL.md` | Create | Low | Skill documentation |

### Acceptance Criteria

- [ ] AC1: Questions contextuelles générées basées sur l'historique
- [ ] AC2: Maximum 3 questions par itération
- [ ] AC3: Références aux features passées dans les questions (si similaires trouvées)
- [ ] AC4: Adaptation à la persona active (stubbed pour F09)
- [ ] AC5: Suggestions de réponses par défaut basées sur l'historique

### Constraints

- Pas de dépendances externes (NLP libraries) — utiliser matching simple
- Compatible avec Project Memory existant (F04)
- Interface préparée pour F09 (Personas) même si pas encore implémenté
- Maximum 3 questions par itération, 3 itérations max

### Out of Scope

- Clarification vocale / audio
- Clarification multi-utilisateurs
- Apprentissage automatique des questions (F08)
- Interface graphique de clarification
- Implémentation complète de F09 (Personas)

### Evaluation

- **Category**: STANDARD
- **Estimated files**: 6
- **Estimated LOC**: ~550
- **Risk**: Medium
- **Justification**: Multiple new modules, integration with existing Project Memory, testable independently

### Suggested Flags

| Flag | Source | Reason |
|------|--------|--------|
| `--think` | auto | 6 files impacted, algorithmic complexity |

---

## §2 — Implementation Plan

### Impacted Files

| File | Action | Risk | LOC |
|------|--------|------|-----|
| `src/project-memory/clarification_analyzer.py` | Create | Low | ~150 |
| `src/project-memory/similarity_matcher.py` | Create | Medium | ~100 |
| `src/project-memory/question_generator.py` | Create | Medium | ~200 |
| `src/project-memory/manager.py` | Modify | Low | +50 |
| `src/commands/epci-brief.md` | Modify | Medium | +30 |
| `src/skills/core/clarification-intelligente/SKILL.md` | Create | Low | ~50 |
| `src/project-memory/tests/test_clarification.py` | Create | Low | ~100 |

### Tasks

#### Wave 1: Core Modules (Foundation)

1. [ ] **Create clarification_analyzer.py — Dataclasses** (10 min)
   - File: `src/project-memory/clarification_analyzer.py`
   - Define `BriefAnalysis`, `DomainInfo`, `GapInfo` dataclasses
   - Define domain constants (AUTH, API, UI, DATA, INFRA, etc.)

2. [ ] **Create clarification_analyzer.py — Keyword extraction** (10 min)
   - Function: `extract_keywords(brief: str) -> List[str]`
   - Tokenize, normalize, filter stopwords
   - Return significant keywords

3. [ ] **Create clarification_analyzer.py — Domain detection** (10 min)
   - Function: `detect_domain(keywords: List[str]) -> DomainInfo`
   - Map keywords to domains using pattern matching
   - Return domain with confidence score

4. [ ] **Create clarification_analyzer.py — Gap analysis** (10 min)
   - Function: `identify_missing_info(brief: str, domain: str) -> List[GapInfo]`
   - Check required info per domain
   - Return list of missing information categories

5. [ ] **Create similarity_matcher.py — Core** (10 min)
   - File: `src/project-memory/similarity_matcher.py`
   - Function: `calculate_jaccard_similarity(set1, set2) -> float`
   - Function: `normalize_text(text: str) -> Set[str]`

6. [ ] **Create similarity_matcher.py — Feature matching** (10 min)
   - Function: `find_similar_features(features: List[FeatureHistory], keywords: List[str], threshold: float) -> List[Tuple[str, float]]`
   - Score each feature against keywords
   - Return sorted list above threshold

#### Wave 2: Manager Integration

7. [ ] **Add similarity methods to manager.py** (10 min)
   - File: `src/project-memory/manager.py`
   - Method: `get_all_feature_metadata() -> List[Dict]`
   - Method: `find_similar_features(keywords, threshold) -> List[Tuple]`
   - Method: `get_patterns_for_domain(domain) -> List[str]`
   - Include graceful degradation (return empty list if data unavailable)

#### Wave 3: Question Generator

8. [ ] **Create question_generator.py — Templates** (10 min)
   - File: `src/project-memory/question_generator.py`
   - Define `QuestionType` enum (REUSE, TECHNICAL, SCOPE, INTEGRATION, PRIORITY)
   - Define `Question` dataclass with template, default suggestion

9. [ ] **Create question_generator.py — Template system** (15 min)
   - Define templates per question type
   - Include placeholders for feature names, patterns, etc.
   - FR/EN support structure

10. [ ] **Create question_generator.py — Generation logic** (15 min)
    - Function: `generate_questions(brief: str, context: Dict, similar_features: List) -> List[Question]`
    - Apply algorithm from CDC §3.3
    - Return max 3 questions with suggestions

11. [ ] **Create question_generator.py — Persona adapter stub** (10 min)
    - Function: `adapt_to_persona(questions: List[Question], persona: Optional[str]) -> List[Question]`
    - Stub implementation (returns questions unchanged when persona=None)
    - Define `PersonaAdapter` interface contract with docstring:
      ```python
      # F09 integration point: When personas implemented, will:
      # - backend: Focus on reliability, performance, queues
      # - frontend: Focus on UX, accessibility, animations
      # - security: Focus on auth, validation, OWASP
      # - architect: Focus on patterns, scalability, design
      ```
    - Include graceful degradation if persona module unavailable

#### Wave 4: Integration & Documentation

12. [ ] **Create clarification-intelligente skill** (10 min)
    - File: `src/skills/core/clarification-intelligente/SKILL.md`
    - Document the clarification system
    - Include usage examples

13. [ ] **Update epci-brief.md Step 2** (15 min)
    - File: `src/commands/epci-brief.md`
    - Replace generic clarification with intelligent system
    - Add Project Memory context loading
    - Invoke question generator

#### Wave 5: Tests & Validation

14. [ ] **Create test infrastructure** (5 min)
    - File: `src/project-memory/tests/__init__.py`
    - File: `src/project-memory/tests/conftest.py`
    - Set up test fixtures for Project Memory mock

15. [ ] **Create test_clarification.py — Analyzer tests** (10 min)
    - File: `src/project-memory/tests/test_clarification.py`
    - Test keyword extraction
    - Test domain detection

16. [ ] **Create test_clarification.py — Matcher tests** (10 min)
    - Test similarity calculation
    - Test feature matching with mock data

17. [ ] **Create test_clarification.py — Generator tests** (10 min)
    - Test question generation
    - Test max 3 questions constraint
    - Test suggestion generation

18. [ ] **Create integration test** (10 min)
    - Test complete clarification flow (analyzer → matcher → generator)
    - Test with mock Project Memory data
    - Verify max 3 questions constraint end-to-end
    - Test graceful degradation when Project Memory unavailable

19. [ ] **Run validation scripts** (5 min)
    - Execute `python src/scripts/validate_skill.py`
    - Execute tests
    - Verify no regressions

### Dependencies

| Dependency | Status | Impact |
|------------|--------|--------|
| F04 Project Memory | ✅ Ready | Provides feature history, patterns |
| F09 Personas | ❌ Stub | Persona adapter stubbed |
| manager.py dataclasses | ✅ Exists | FeatureHistory available |

### Risks

| Risk | Probability | Mitigation |
|------|-------------|------------|
| Similarity too simple | Medium | Design for upgrade, use Jaccard as baseline |
| F09 not ready | N/A | Clean stub interface with documented contract |
| Question quality | Low | Use CDC examples as templates |
| Integration breaks epci-brief | Low | Minimal changes, test thoroughly |
| Project Memory unavailable | Low | Graceful degradation returns generic questions |

### Validation

- **@plan-validator**: APPROVED (after revision)
  - Completeness: ✅ All AC criteria addressed
  - Consistency: ✅ No circular dependencies
  - Feasibility: ✅ Test infrastructure added
  - Quality: ✅ Integration test + error handling added

---

## §3 — Implementation

### Progress

- [x] Task 1-4 — Create clarification_analyzer.py (dataclasses, keywords, domain, gaps)
- [x] Task 5-6 — Create similarity_matcher.py (Jaccard, feature matching)
- [x] Task 7 — Add similarity methods to manager.py
- [x] Task 8-11 — Create question_generator.py (templates, generation, persona stub)
- [x] Task 12 — Create clarification-intelligente skill
- [x] Task 13 — Update epci-brief.md Step 2
- [x] Task 14 — Create test infrastructure
- [x] Task 15-18 — Create tests (analyzer, matcher, generator, integration)
- [x] Task 19 — Run validation scripts

### Tests

```bash
# Analyzer test
$ python3 src/project-memory/clarification_analyzer.py "Ajouter notifications"
Keywords: ['ajouter', 'notifications']
Domain: notification (confidence: 0.25)

# Matcher test
$ python3 src/project-memory/similarity_matcher.py "notification email"
Found 3 matches: email-notifications (0.6), user-profile (0.3), ...

# Generator test
$ python3 src/project-memory/question_generator.py "Ajouter notifications"
Questions (3):
1. [reuse] Feature similaire trouvée...
2. [technical] Quels canaux de notification...
3. [scope] Quel est le périmètre exact...
```

### Validation

```bash
$ python3 src/scripts/validate_skill.py src/skills/core/clarification-intelligente/
RESULT: PASSED (6/6 checks)
```

### Files Created/Modified

| File | Action | LOC | Status |
|------|--------|-----|--------|
| `src/project-memory/clarification_analyzer.py` | Created | 380 | ✅ |
| `src/project-memory/similarity_matcher.py` | Created | 180 | ✅ |
| `src/project-memory/question_generator.py` | Created | 420 | ✅ |
| `src/project-memory/manager.py` | Modified | +100 | ✅ |
| `src/commands/epci-brief.md` | Modified | +50 | ✅ |
| `src/skills/core/clarification-intelligente/SKILL.md` | Created | 120 | ✅ |
| `src/project-memory/tests/__init__.py` | Created | 2 | ✅ |
| `src/project-memory/tests/conftest.py` | Created | 90 | ✅ |
| `src/project-memory/tests/test_clarification.py` | Created | 350 | ✅ |

**Total**: ~1700 LOC (exceeds estimate of ~550 due to comprehensive tests)

### Reviews

- **Module validation**: All 3 modules execute correctly
- **Skill validation**: PASSED 6/6 checks
- **Integration**: epci-brief.md updated with F05 system

### Deviations

| Planned | Actual | Justification |
|---------|--------|---------------|
| ~550 LOC | ~1700 LOC | More comprehensive tests and detailed templates |
| 7 files | 9 files | Added test infrastructure (conftest.py, __init__.py) |

### Acceptance Criteria Verification

- [x] AC1: Questions contextuelles générées basées sur l'historique ✅
- [x] AC2: Maximum 3 questions par itération ✅ (enforced in code)
- [x] AC3: Références aux features passées dans les questions ✅
- [x] AC4: Adaptation à la persona active (stubbed) ✅
- [x] AC5: Suggestions de réponses par défaut ✅

---

## §4 — Finalization

### Commit

```
feat(clarification): add intelligent clarification system (F05)

- Add clarification_analyzer.py for keyword extraction and domain detection
- Add similarity_matcher.py for Jaccard-based feature matching
- Add question_generator.py for context-aware question generation (max 3)
- Extend manager.py with find_similar_features() and get_patterns_for_domain()
- Update epci-brief.md Step 2 with intelligent clarification flow
- Add clarification-intelligente skill documentation
- Add comprehensive test suite for all modules

Refs: docs/features/f05-clarification-intelligente.md
```

**Commit hash**: `6a83df0`
**Files changed**: 10
**Insertions**: +2618 lines

### Documentation

- Feature Document: `docs/features/f05-clarification-intelligente.md` ✅
- Skill documentation: `src/skills/core/clarification-intelligente/SKILL.md` ✅
- Command updated: `src/commands/epci-brief.md` Step 2 ✅

### Status

| Check | Status |
|-------|--------|
| All tests pass | ✅ |
| Skill validation | ✅ PASSED 6/6 |
| Feature Document complete | ✅ |
| Commit created | ✅ |

### Next Steps

1. **F09 Integration**: When Personas system is implemented, update `adapt_to_persona()` in question_generator.py
2. **F08 Learning**: Consider adding feedback loop to improve question quality based on user responses
3. **Performance**: If feature history grows large, consider indexing for faster similarity matching
