# Journal d'Exploration: Refonte /quick

> **Session ID**: brainstorm-refonte-quick-20260126
> **Date**: 2026-01-26
> **Duree**: ~25 minutes
> **EMS Final**: 76/100

---

## Chronologie

### Phase 1: Initialisation (0-5 min)

**Documents analyses:**
- `docs/migration/50-60/epci-v6-brainstorm-report.md` - Architecture EPCI v6 complete
- `docs/migration/50-60/epci-v6-implementation-plan.md` - Plan avec addendum memoire legere
- `archive/5.6/commands/quick.md` - Version v5.6 du workflow EPCT (introuvable)
- `src/skills/quick/SKILL.md` - Version actuelle v6
- `src/skills/implement/SKILL.md` - Workflow /implement pour comparaison
- `src/agents/implementer.md` - Subagent @implementer
- `src/agents/planner.md` - Subagent @planner

**Contexte extrait:**
- EPCI v6 = 8 user skills + 6 core skills
- /quick actuel = workflow simplifie E-P-C+T-M
- /implement = workflow complet avec 7 steps
- Memoire legere v6.0.4 = index.json enrichi

### Phase 2: Clarification (5-10 min)

**Questions posees:**

1. **Input mode**: Plan-only strict vs Plan-first + fallback vs Agnostique
   - Reponse: **Plan-first + fallback** (prefere plan natif mais accepte text)

2. **Format memoire**: index.json vs MEMORY.md vs Les deux
   - Reponse: **index.json enrichi** (deja implemente v6.0.4)

3. **Subagents**: Minimal vs Standard vs Full access vs Aucun
   - Reponse: **Minimal** (@implementer seulement)

4. **Stack skills**: Auto-detection vs Flag explicite vs Jamais
   - Reponse: **Auto-detection** (detection automatique)

5. **Documentation**: Update only vs Generation complete vs Skip
   - Reponse: **Update only** (CHANGELOG/README si impact)

### Phase 3: Reformulation Brief (10-12 min)

**Brief valide:**
- /quick = suite naturelle du mode plan Claude Code
- Workflow simplifie vs /implement
- Integration stack skills + memoire legere

**Workflow propose:**
```
Plan natif -> Skip E-P -> [C] -> [T] -> [D?] -> [M]
Text       -> Mini-E-P -> [C] -> [T] -> [D?] -> [M]
```

### Phase 4: Recherches Perplexity (12-20 min)

**5 recherches lancees:**

1. **Plan-first Workflow**
   - Insight: Plan = vrai doc (checklist + sections), scope 20-30 min
   - Impact: Confirme approche plan-only, structure plan definie

2. **TDD AI Automation**
   - Insight: Test-as-prompt, modes separes, garde-fous automatiques
   - Impact: @implementer suit cycle strict Red-Green (pas refactor)

3. **Stack Detection**
   - Insight: Registre declaratif, root first, scoring confidence
   - Impact: Pattern de detection avec thresholds

4. **Feature Memory**
   - Insight: MD pour narratif, JSON pour index
   - Impact: Valide index.json, prevoir projection MD si besoin

5. **Subagent Delegation**
   - Insight: Single agent pour "mostly write"
   - Impact: Confirme @implementer only pour /quick

### Phase 5: Convergence (20-25 min)

**EMS Progression:**
| Iteration | Clarity | Depth | Coverage | Decisions | Actionability | Global |
|-----------|---------|-------|----------|-----------|---------------|--------|
| Initial   | 40      | 20    | 20       | 20        | 20            | 24     |
| Post-clarif | 60    | 40    | 55       | 70        | 45            | 52     |
| Post-research | 80  | 70    | 75       | 85        | 70            | 76     |

---

## Decisions Prises

| # | Decision | Options Considerees | Choix | Justification |
|---|----------|---------------------|-------|---------------|
| D1 | Input mode | Plan-only, Plan-first+fallback, Agnostique | Plan-first+fallback | Flexibilite sans sacrifier UX |
| D2 | Format memoire | index.json, MEMORY.md, Les deux | index.json | Deja implemente, pas de fichier supp |
| D3 | Subagents | Minimal, Standard, Full, Aucun | Minimal | Single agent pour "mostly write" |
| D4 | Stack skills | Auto-detect, Flag, Jamais | Auto-detect | UX fluide, detection fiable |
| D5 | Documentation | Update, Generate, Skip | Update only | Minimal overhead, /implement pour full |
| D6 | TDD mode | Full RGR, Red-Green only, Skip | Red-Green only | Vitesse > perfection pour /quick |
| D7 | Plan structure | Libre, Structure imposee | Structure imposee | Parsing fiable, qualite plan |

---

## Patterns Techniques Identifies

### Pattern 1: Plan Detection

```python
# Priorite: chemin conventionnel > frontmatter > heuristique
def is_native_plan(path):
    if ".claude/plans/" in path: return True
    if has_frontmatter_saved_at(path): return True
    return False
```

### Pattern 2: Stack Scoring

```python
# Signals then rules: manifest > deps > dirs > heuristic
STACK_SIGNATURES = {
    "python-django": {
        "files": ["manage.py"],
        "deps": {"requirements.txt": "django"},
        "confidence_base": 0.9
    }
}
```

### Pattern 3: TDD Simplifie

```python
# Red-Green-Verify (pas Refactor pour /quick)
def tdd_cycle(task):
    write_failing_test()  # RED
    write_minimal_impl()  # GREEN
    verify_all_tests()    # VERIFY
    # REFACTOR: SKIP
```

### Pattern 4: Memory Enrichi

```json
// index.json entry
{
  "id": "...",
  "summary": "1-2 phrases",
  "modified_files": ["..."],
  "test_count": N
}
```

---

## Questions Ouvertes

| # | Question | Statut | Resolution |
|---|----------|--------|------------|
| Q1 | Gestion des plans mal formates | Resolue | Validation structure + fallback parsing |
| Q2 | Escalade mid-workflow | Resolue | Re-eval apres E, suggestion /implement |
| Q3 | Multi-stack projets | Reportee | Extension future (hors scope) |
| Q4 | Integration CI/CD | Reportee | Hors scope ce CDC |

---

## Techniques Appliquees

1. **Clarification progressive** - Questions one-at-a-time pour decisions claires
2. **Recherche externe** - 5 prompts Perplexity pour valider patterns
3. **Comparaison structuree** - /quick vs /implement table
4. **EMS tracking** - Suivi progression 5 axes

---

## Metriques Session

| Metrique | Valeur |
|----------|--------|
| Iterations | 3 |
| Questions posees | 7 |
| Decisions prises | 7 |
| Recherches Perplexity | 5 |
| Documents analyses | 8 |
| EMS initial | 24 |
| EMS final | 76 |
| Delta EMS | +52 |
| Duree totale | ~25 min |

---

## Recommandation Chaining

**Complexite evaluee**: STANDARD
- LOC estimees: 200-400
- Fichiers: 4-6 (SKILL.md + 3 references + tests)
- Dependances: core skills, stack skills, @implementer

**Routing suggere**: `/spec` -> `/implement`

```bash
# Prochaine etape
/spec @docs/briefs/refonte-quick/brief-refonte-quick-20260126.md
```

---

*Journal genere par brainstorm EPCI v6.0*
