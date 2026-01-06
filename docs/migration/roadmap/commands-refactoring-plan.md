# Plan de Refactorisation des Commandes EPCI

> **Date**: 2025-01-05
> **Status**: À implémenter
> **Priorité**: Optimisation maintenance

---

## 1. État actuel

### Références existantes (`src/commands/references/`)

| Fichier | Lignes | Description |
|---------|--------|-------------|
| `breakpoints.md` | 102 | Templates de breakpoints |
| `hooks.md` | 74 | Référence hooks |
| `turbo-mode.md` | 82 | Spécifications mode turbo |
| `commit-context.md` | 67 | Schéma contexte commit |

### Inventaire des commandes

| Commande | Lignes | Duplication |
|----------|--------|-------------|
| `epci.md` | 725 | Forte |
| `quick.md` | 582 | Forte |
| `brainstorm.md` | 580 | Forte |
| `decompose.md` | 529 | Forte |
| `debug.md` | 455 | Forte |
| `memory.md` | 458 | Légère |
| `brief.md` | 438 | Forte |
| `commit.md` | 398 | Utilise références |
| `rules.md` | 343 | Légère |
| `promptor.md` | 289 | Standalone |
| `create.md` | 224 | Standalone |

---

## 2. Contenu dupliqué identifié

### A. Memory Loading (10 commandes, ~160 lignes)

**Pattern répété:**
```markdown
### Step 0: Load Project Memory
Skill: `project-memory`
Load project context from `.project-memory/` directory...
```

**Commandes concernées:** brief, epci, quick, debug, decompose, brainstorm, rules, memory

**→ Créer:** `references/memory-loading.md`

---

### B. Hook Execution (66 occurrences, ~320 lignes)

**Patterns répétés:**
```markdown
🪝 Execute `pre-<phase>` hooks (if configured in `hooks/active/`)

🪝 Execute `post-phase-X` hooks (if configured)
python3 src/hooks/runner.py post-phase-X --context '{...}'
```

**Commandes concernées:** brief, epci (26×), quick (8×), debug (3×), commit (8×), brainstorm, decompose, create

**→ Étendre:** `references/hooks.md` avec:
- Signatures des hook points
- Schéma de contexte par type de hook
- Règles hooks obligatoires vs optionnels

---

### C. Thinking Modes (9 commandes, 40 occurrences, ~96 lignes)

**Pattern répété:**
```markdown
| Flag | Effect | Auto-Trigger |
|------|--------|--------------|
| `--think` | Standard analysis (~4K tokens) | 3-10 files |
| `--think-hard` | Deep analysis (~10K tokens) | >10 files |
| `--ultrathink` | Critical analysis (~32K tokens) | Never (explicit) |
```

**Commandes concernées:** brief, epci, quick, debug, brainstorm, decompose, commit, promptor, rules

**→ Créer:** `references/thinking-modes.md` avec:
- Spécifications globales des modes
- Seuils d'auto-activation
- Sélection modèle par commande
- Règles d'escalade

---

### D. Turbo Mode (7 commandes, 59 occurrences, ~180 lignes)

**Variations par commande:**
- `/brief --turbo`: Haiku exploration, 2 questions max, auto-accept >0.7
- `/epci --turbo`: @planner, @implementer, reviews parallèles
- `/quick --turbo`: @implementer, skip review optionnel, auto-commit
- `/debug --turbo`: Haiku diagnostic, solution unique, skip breakpoint si >70%

**→ Étendre:** `references/turbo-mode.md` avec:
- Matrice comportement turbo par commande
- Invocations subagents turbo
- Comparaison turbo vs standard
- Précédence flags turbo + autres

---

### E. Persona Activation (4 commandes, 18 occurrences, ~60 lignes)

**Pattern répété:**
```markdown
### Persona Detection (F09)
Score = (keywords × 0.4) + (files × 0.4) + (stack × 0.2)
If score > 0.6: Auto-activate persona
If score 0.4-0.6: Suggest persona in breakpoint
```

**Commandes concernées:** brief, epci, brainstorm

**→ Créer:** `references/persona-activation.md` avec:
- Algorithme de scoring unifié
- Sélection persona par commande
- Mode 3-personas brainstorm (Architecte/Sparring/Pragmatique)
- Seuils d'activation et formats d'affichage

---

### F. MCP Activation (6 commandes, 29 occurrences, ~100 lignes)

**Pattern répété:**
```markdown
Based on activated personas, determine MCP servers to activate:
- Check keyword triggers in brief text
- Check file pattern triggers in impacted files
- Check flag triggers
```

**Commandes concernées:** brief, epci, quick, debug, brainstorm, decompose

**→ Créer:** `references/mcp-activation.md` avec:
- Matrice auto-activation MCP par persona
- Triggers keywords/file patterns
- Recommandations MCP par commande
- Comportement override flags

---

### G. Flag Auto-Detection (8 commandes, ~105 lignes)

**Patterns répétés:**

1. Seuils de complexité:
```markdown
| Condition | Threshold | Flag |
| Files impacted | 3-10 | --think |
| Files impacted | >10 | --think-hard |
```

2. Patterns fichiers sensibles:
```markdown
**/auth/** **/security/** **/payment/**
**/password/** **/api/v*/admin/**
```

3. Précédence flags:
```markdown
| Combination | Result |
| --turbo + --large | Warning, --large wins |
```

**→ Créer:** `references/flag-system.md` avec:
- Taxonomie unifiée des flags
- Seuils d'auto-activation
- Liste patterns sensibles (réutilisable)
- Matrice de précédence globale

---

### H. Breakpoint Templates (6 commandes, ~150 lignes)

**Templates existants (non centralisés):**
- Step 3 Breakpoint (brief.md): ~60 lignes
- Phase 1 Breakpoint (epci.md): ~43 lignes
- Phase 2 Breakpoint (epci.md): ~33 lignes
- Lightweight Breakpoint (quick.md): ~13 lignes
- Pre-commit Breakpoint (commit.md): ~30 lignes
- Debug Diagnostic Breakpoint (debug.md): ~23 lignes

**→ Étendre:** `references/breakpoints.md` avec:
- Tous les templates concrets (6-8 types)
- Calcul métriques par commande
- Patterns options/choix
- Priorités affichage contenu conditionnel

---

### I. Complexity Matrix (7 commandes, ~60 lignes)

**Pattern répété:**
```markdown
| Criteria | TINY | SMALL | STANDARD | LARGE | SPIKE |
| Files | 1 | 2-3 | 4-10 | 10+ | ? |
| Estimated LOC | <50 | <200 | <1000 | 1000+ | ? |
| Risk | None | Low | Medium | High | Unknown |
```

**→ Créer:** `references/complexity-matrix.md` avec:
- Définitions unifiées TINY/SMALL/STANDARD/LARGE/SPIKE
- Implications par commande (routing, flags, subagents)
- Triggers d'escalade

---

## 3. Économie estimée

| Métrique | Valeur |
|----------|--------|
| Lignes extractibles | ~1 430 lignes |
| % des commandes | 28% |
| Nouvelles références | ~800 lignes |
| **Gain net** | **~630 lignes (12.5%)** |

---

## 4. Roadmap d'implémentation

### Phase 1 — HIGH Priority (Plus grand impact)

| # | Action | Impact |
|---|--------|--------|
| 1 | Créer `references/memory-loading.md` | 10 duplications |
| 2 | Étendre `references/hooks.md` | 66 occurrences |
| 3 | Créer `references/thinking-modes.md` | 40 occurrences |
| 4 | Étendre `references/turbo-mode.md` | 59 occurrences |

### Phase 2 — MEDIUM Priority

| # | Action | Impact |
|---|--------|--------|
| 5 | Créer `references/persona-activation.md` | 18 occurrences |
| 6 | Créer `references/mcp-activation.md` | 29 occurrences |
| 7 | Créer `references/flag-system.md` | 8 fichiers |
| 8 | Étendre `references/breakpoints.md` | 6 templates |

### Phase 3 — LOW Priority (Nice to have)

| # | Action | Impact |
|---|--------|--------|
| 9 | Créer `references/complexity-matrix.md` | 7 fichiers |
| 10 | Créer `references/subagent-invocation.md` | 5 fichiers |
| 11 | Créer `references/error-escalation.md` | 3 fichiers |
| 12 | Créer `references/question-patterns.md` | 2 fichiers |

---

## 5. Contenu à NE PAS extraire

✅ **Garder dans chaque commande:**
- Logique workflow spécifique (Phase 1/2/3, étapes EPCT)
- Flags spécifiques à la commande
- Subagents/routing uniques
- Formats de sortie propres au but de la commande

---

## 6. Checklist d'implémentation

Pour chaque référence créée:

- [ ] Créer le fichier `references/<name>.md`
- [ ] Extraire le contenu commun des commandes
- [ ] Remplacer par `→ See references/<name>.md` dans chaque commande
- [ ] Valider avec `python src/scripts/validate_command.py`
- [ ] Tester que les commandes fonctionnent toujours

---

## 7. Notes

- Les références sont chargées automatiquement quand référencées
- Garder chaque référence < 500 lignes pour performance
- Utiliser des ancres markdown pour liens précis: `references/hooks.md#post-phase-3`
