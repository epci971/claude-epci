# S03 — Integration workflows EPCI

| Metadata | Value |
|----------|-------|
| **Spec ID** | S03 |
| **Parent PRD** | worktree-integration |
| **Effort** | 2 jours |
| **Priority** | P1 (Must-have) / P2 (Should-have) |
| **Dependencies** | S01, S02 |
| **Status** | Pending |

---

## Objectif

Integrer les scripts worktree dans les workflows EPCI existants:
1. **(P1)** Appel automatique de finalize en fin de /epci et /quick
2. **(P2)** Suggestion de creation worktree dans /brief pour STANDARD/LARGE

## User Stories Sources

### US2 — Finaliser un worktree (integration)

**Acceptance Criteria**:
- [ ] Given j'ai termine /epci ou /quick, When la Phase 3 se termine, Then worktree-finalize.sh est appele automatiquement

### US4 — Suggestion dans /brief

**En tant que** developpeur EPCI,
**Je veux** voir une suggestion de creation worktree apres /brief,
**Afin de** savoir comment isoler ma feature.

---

## Scope

### Fichiers a modifier

| Fichier | Action | Description |
|---------|--------|-------------|
| `src/commands/epci.md` | Modify | Ajouter appel finalize en Phase 3 |
| `src/commands/quick.md` | Modify | Ajouter appel finalize en fin |
| `src/commands/brief.md` | Modify | Ajouter suggestion worktree |

### Hors scope

- Les scripts eux-memes (S01, S02)
- Nouveaux hooks

---

## Acceptance Criteria

### Integration /epci et /quick (P1 - Must-have)

- [ ] **AC1**: Given je suis dans un worktree et /epci Phase 3 termine, When le commit final est fait, Then worktree-finalize.sh est propose
- [ ] **AC2**: Given je suis dans un worktree et /quick termine, When le commit final est fait, Then worktree-finalize.sh est propose
- [ ] **AC3**: Given je ne suis PAS dans un worktree, When /epci ou /quick termine, Then pas d'appel finalize

### Suggestion /brief (P2 - Should-have)

- [ ] **AC4**: Given /brief detecte STANDARD ou LARGE, When le routing s'affiche, Then une suggestion worktree-create.sh est affichee
- [ ] **AC5**: Given /brief detecte TINY ou SMALL, When le routing s'affiche, Then pas de suggestion worktree

---

## Tasks

### Integration /epci (Phase 3)

- [ ] T1: Lire `src/commands/epci.md` pour comprendre la structure Phase 3
- [ ] T2: Ajouter detection "est-on dans un worktree?" en fin de Phase 3
- [ ] T3: Ajouter section conditionnelle proposant finalize
- [ ] T4: Documenter le comportement dans le command

### Integration /quick

- [ ] T5: Lire `src/commands/quick.md` pour comprendre la fin de workflow
- [ ] T6: Ajouter detection worktree en fin de workflow
- [ ] T7: Ajouter proposition finalize conditionnelle

### Suggestion /brief

- [ ] T8: Lire `src/commands/brief.md` pour localiser le breakpoint routing
- [ ] T9: Ajouter suggestion worktree dans le bloc STANDARD/LARGE
- [ ] T10: S'assurer que TINY/SMALL n'affichent pas la suggestion

### Tests

- [ ] T11: Tester /epci dans un worktree (finalize propose)
- [ ] T12: Tester /epci hors worktree (pas de finalize)
- [ ] T13: Tester /quick dans un worktree
- [ ] T14: Tester /brief avec routing STANDARD (suggestion affichee)
- [ ] T15: Tester /brief avec routing TINY (pas de suggestion)

---

## Technical Notes

### Detection worktree

```bash
# Verifier si on est dans un worktree
is_worktree() {
    local git_dir=$(git rev-parse --git-dir 2>/dev/null)
    [[ "$git_dir" == *".git/worktrees/"* ]]
}
```

Ou en checkant si le path courant est dans `~/worktrees/`.

### Modification /epci.md — Phase 3 fin

Ajouter apres le commit final:

```markdown
### Worktree Finalization (Conditional)

**Condition**: Execute only if current directory is a worktree.

**Detection**:
```bash
# Check if in worktree
git rev-parse --git-dir | grep -q "worktrees"
```

**If in worktree**:

Display:
```
+---------------------------------------------------------------------+
| WORKTREE DETECTED                                                   |
+---------------------------------------------------------------------+
|                                                                     |
| Feature complete dans worktree: {slug}                              |
|                                                                     |
| Pour merger dans develop et nettoyer:                               |
|   ./src/scripts/worktree-finalize.sh                                |
|                                                                     |
| Pour garder le worktree ouvert:                                     |
|   (aucune action requise)                                           |
|                                                                     |
+---------------------------------------------------------------------+
```

**If NOT in worktree**: Skip this section silently.
```

### Modification /brief.md — Routing block

Ajouter dans le bloc routing STANDARD/LARGE:

```markdown
| TIP: Worktree recommande                                            |
|                                                                     |
| Pour isoler cette feature dans un worktree:                         |
|   ./src/scripts/worktree-create.sh {slug}                           |
|   cd ~/worktrees/{project}/{slug}                                   |
|   claude                                                            |
```

---

## Definition of Done

- [ ] /epci propose finalize en fin de Phase 3 (si worktree)
- [ ] /quick propose finalize en fin (si worktree)
- [ ] /brief suggere worktree-create pour STANDARD/LARGE
- [ ] Aucune suggestion pour TINY/SMALL
- [ ] Documentation inline dans les commandes
