# Feature Document — Intégration Perplexity Research

> **Slug**: `perplexity-integration`
> **Category**: STANDARD
> **Date**: 2026-01-20

---

## §1 — Functional Brief

### Context

Créer un système de recherche externe via Perplexity Pro (human-in-the-loop) pour compléter Context7 et WebSearch quand les résultats sont insuffisants. Claude détecte le besoin de recherche, affiche un breakpoint avec prompt prêt à copier, l'utilisateur fait la recherche dans Perplexity, colle les résultats, Claude intègre.

### Detected Stack

- **Framework**: Plugin EPCI Claude Code v5.3.10
- **Language**: Markdown (skills/commands), Python (scripts)
- **Patterns**: Skill modular (SKILL.md + references/), @skill: invocation, AskUserQuestion breakpoints

### Acceptance Criteria

- [ ] Skill `perplexity-research` créé avec triggers détection (library, bug, architecture, best-practices, market)
- [ ] Nouveau type breakpoint `research-prompt` fonctionnel dans breakpoint-display
- [ ] `/brief` modifié — Step 2.1 research optionnel après @Explore
- [ ] `/debug` modifié — Step 1.2 étendu avec perplexity fallback
- [ ] `/brainstorm` modifié — Phase 1 (market) + Phase 2 (axes faibles)
- [ ] CLAUDE.md mis à jour (35 skills)
- [ ] Validation scripts passent (`validate_skill.py`, `validate_command.py`)

### Constraints

- Pas d'API — workflow manuel (copier prompt, coller résultats)
- Réutiliser breakpoint-display existant (token-efficient ~80 tokens/breakpoint)
- Backward compatible — recherche optionnelle, commandes fonctionnent sans

### Out of Scope

- Intégration API Perplexity (pas disponible/pas d'abonnement API)
- Automatisation complète du workflow recherche
- Nouveaux hooks pre/post-research

### Evaluation

- **Category**: STANDARD
- **Estimated files**: 10 (5 créations + 5 modifications)
- **Estimated LOC**: ~1500-1800
- **Risk**: MEDIUM (breakpoint type validation, state persistence, blocking behavior)
- **Justification**: Plus de 4 fichiers, intégration multi-commandes, nouveau skill avec références

### Suggested Flags

| Flag           | Source | Reason                    |
| -------------- | ------ | ------------------------- |
| `--think-hard` | auto   | 10 fichiers impactés      |

### Memory Summary

- **Project**: tools-claude-code-epci
- **Stack**: claude-code-plugin v5.3.10
- **Conventions**: kebab-case files, SKILL.md + references/, 5000 tokens max/skill
- **Velocity**: 17 features completed

---

## §2 — Implementation Plan

### Atomic Tasks (2-15 min each)

| # | Task | Time | Files | Description |
|---|------|------|-------|-------------|
| **Phase A: Skill perplexity-research** |
| T1 | Créer SKILL.md structure de base | 10min | Create `perplexity-research/SKILL.md` | Frontmatter + Overview + MANDATORY EXECUTION |
| T2 | Ajouter logique de détection triggers | 15min | Edit `perplexity-research/SKILL.md` | Triggers matrix + conditions |
| T3 | Ajouter génération de prompts | 15min | Edit `perplexity-research/SKILL.md` | Prompt templates par catégorie |
| T4 | Créer triggers.md reference | 10min | Create `perplexity-research/references/triggers.md` | Matrice détaillée par commande |
| T5 | Créer prompt-templates.md reference | 15min | Create `perplexity-research/references/prompt-templates.md` | 6 templates (library, bug, arch, etc.) |
| **Phase B: Type breakpoint research-prompt** |
| T6 | Créer template research-prompt.md | 10min | Create `breakpoint-display/templates/research-prompt.md` | Data structure + display format |
| T7 | Ajouter type dans SKILL.md table | 5min | Edit `breakpoint-display/SKILL.md` | Ajouter ligne type research-prompt |
| T8 | Ajouter ASCII template | 10min | Edit `breakpoint-display/references/execution-templates.md` | Template ASCII copyable |
| **Phase C: Modifier /brief** |
| T9 | Ajouter Step 2.1 dans brief.md | 10min | Edit `commands/brief.md` | Invocation conditionnelle après @Explore |
| **Phase D: Modifier /debug** |
| T10 | Étendre Step 1.2 dans debug.md | 10min | Edit `commands/debug.md` | Fallback Perplexity après Context7 |
| **Phase E: Modifier /brainstorm** |
| T11 | Ajouter Phase 1 research (market) | 10min | Edit `commands/brainstorm.md` | Research marché après @Explore |
| T12 | Ajouter Phase 2 research (axes faibles) | 10min | Edit `commands/brainstorm.md` | Research ciblée si EMS < 50 |
| **Phase F: Documentation** |
| T13 | Mettre à jour CLAUDE.md | 5min | Edit `CLAUDE.md` | Skills count 34 → 35 |
| **Phase G: Validation** |
| T14 | Valider skill perplexity-research | 5min | Bash | `python src/scripts/validate_skill.py` |
| T15 | Valider commandes modifiées | 5min | Bash | `python src/scripts/validate_command.py` × 3 |

**Total: 15 tasks, ~2h30 estimé**

### Dependencies Graph

```
T1 → T2 → T3 → T4 → T5
            ↓
T6 → T7 → T8
            ↓
      ┌─────┼─────┐
      ↓     ↓     ↓
     T9    T10   T11 → T12
      └─────┼─────┘
            ↓
           T13
            ↓
      T14 → T15
```

### Fichiers impactés (résumé)

| Action | Fichier | LOC estimé |
|--------|---------|-----------|
| **CREATE** | `src/skills/core/perplexity-research/SKILL.md` | 400 |
| **CREATE** | `src/skills/core/perplexity-research/references/triggers.md` | 200 |
| **CREATE** | `src/skills/core/perplexity-research/references/prompt-templates.md` | 300 |
| **CREATE** | `src/skills/core/breakpoint-display/templates/research-prompt.md` | 100 |
| **MODIFY** | `src/skills/core/breakpoint-display/SKILL.md` | +20 |
| **MODIFY** | `src/skills/core/breakpoint-display/references/execution-templates.md` | +40 |
| **MODIFY** | `src/commands/brief.md` | +30 |
| **MODIFY** | `src/commands/debug.md` | +25 |
| **MODIFY** | `src/commands/brainstorm.md` | +50 |
| **MODIFY** | `CLAUDE.md` | +5 |

**Total: 4 créations + 6 modifications = 10 fichiers, ~1170 LOC**

### Test Plan

| Test | Commande | Critère |
|------|----------|---------|
| Skill structure | `validate_skill.py src/skills/core/perplexity-research/` | PASS |
| Commands syntax | `validate_command.py src/commands/brief.md` | PASS |
| Commands syntax | `validate_command.py src/commands/debug.md` | PASS |
| Commands syntax | `validate_command.py src/commands/brainstorm.md` | PASS |
| Breakpoint type | Manual: Invoke research-prompt in test | ASCII displays correctly |

### Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    NOUVEAU SKILL                                 │
│              perplexity-research/SKILL.md                        │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │ • Logique de détection du besoin de recherche               ││
│  │ • Génération de prompts Perplexity optimisés                ││
│  │ • Indication Deep Research (oui/non)                        ││
│  │ • Patterns de recherche par contexte                        ││
│  └─────────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼ invoque
┌─────────────────────────────────────────────────────────────────┐
│                 BREAKPOINT-DISPLAY (existant)                    │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │ NOUVEAU TYPE: research-prompt                               ││
│  │ • Affiche contexte + prompt copyable                        ││
│  │ • Indique mode (Standard / Deep Research)                   ││
│  │ • AskUserQuestion: [Rechercher] / [Pas nécessaire]          ││
│  └─────────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼ utilisé par
┌─────────────────────────────────────────────────────────────────┐
│            COMMANDES EPCI (modification)                         │
│  • /brief   → Step 2.1 (après @Explore)                         │
│  • /debug   → Step 1.2 (Research fallback)                      │
│  • /brainstorm → Phase 1 + Phase 2 (itérations)                 │
└─────────────────────────────────────────────────────────────────┘
```

### Triggers Matrix

| Contexte | Trigger | Mode recommandé |
|----------|---------|-----------------|
| Librairie inconnue | Package non dans Context7 | Standard |
| Bug complexe | Erreur rare, peu de résultats web | Deep Research |
| Architecture | Patterns distribués, microservices | Deep Research |
| Best practices | Framework récent, nouvelles versions | Standard |
| Analyse concurrentielle | `--competitive` flag | Deep Research |
| Incertitude technique | `/brainstorm` avec EMS < 50 | Standard |

---

## §3 — Implementation & Finalization

### Implementation Summary

| Phase | Status | Files |
|-------|--------|-------|
| **Phase A**: Skill perplexity-research | ✅ Complete | 3 files created |
| **Phase B**: Type breakpoint research-prompt | ✅ Complete | 1 file created, 2 modified |
| **Phase C**: Modifier /brief | ✅ Complete | 1 file modified |
| **Phase D**: Modifier /debug | ✅ Complete | 1 file modified |
| **Phase E**: Modifier /brainstorm | ✅ Complete | 1 file modified |
| **Phase F**: Documentation CLAUDE.md | ✅ Complete | 1 file modified |
| **Phase G**: Validation | ✅ Complete | All scripts pass |

### Files Created

1. `src/skills/core/perplexity-research/SKILL.md` — Main skill (~2112 tokens)
2. `src/skills/core/perplexity-research/references/triggers.md` — Triggers matrix by command
3. `src/skills/core/perplexity-research/references/prompt-templates.md` — 6 prompt templates
4. `src/skills/core/breakpoint-display/templates/research-prompt.md` — New breakpoint type

### Files Modified

1. `src/skills/core/breakpoint-display/SKILL.md` — Added research-prompt to types table
2. `src/skills/core/breakpoint-display/references/execution-templates.md` — Added ASCII template
3. `src/commands/brief.md` — Added Step 2.1 Perplexity research
4. `src/commands/debug.md` — Added Step 1.2.1 Perplexity fallback
5. `src/commands/brainstorm.md` — Added Phase 1 market research + Phase 2 targeted research
6. `CLAUDE.md` — Updated version to 5.3.11, skills count to 35

### Validation Results

```
perplexity-research: PASSED (6/6 checks)
brief.md: PASSED (5/5 checks)
debug.md: PASSED (5/5 checks)
brainstorm.md: PASSED (5/5 checks)
```

### Key Features Implemented

1. **Human-in-the-loop workflow**: No API needed, user copies prompt to Perplexity
2. **Smart triggers**: Auto-detect when research is useful (library_unknown, bug_complex, etc.)
3. **Mode recommendation**: Standard vs Deep Research based on query complexity
4. **Integration points**: 3 commands support Perplexity research
5. **Backward compatible**: Commands work without research (optional feature)

### Commit Context

Ready for commit with message:
```
feat(skills): add perplexity-research skill for external research integration

- Create perplexity-research skill with SKILL.md + references/
- Add research-prompt breakpoint type to breakpoint-display
- Integrate in /brief (Step 2.1), /debug (Step 1.2.1), /brainstorm (Phase 1+2)
- Human-in-the-loop workflow: prompt generation, no API needed
- Support Standard and Deep Research modes
- Update CLAUDE.md to v5.3.11 (35 skills, 10 breakpoint types)
```
