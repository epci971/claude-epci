# Backlog — Worktree Integration EPCI

| Metadata | Value |
|----------|-------|
| **PRD Source** | worktree-integration |
| **Generated** | 2026-01-14 |
| **Granularity** | small (30-60 min) |
| **Total Stories** | 12 |

---

## Vue d'ensemble

| ID | Story | Spec | Type | Cx | Pri | Deps | Status |
|----|-------|------|------|----|----|------|--------|
| US-001 | Setup script worktree-create.sh | S01 | Script | S | P1 | - | ⬜ |
| US-002 | Validation arguments et prerequis | S01 | Logic | S | P1 | US-001 | ⬜ |
| US-003 | Creation worktree avec branche | S01 | Logic | M | P1 | US-002 | ⬜ |
| US-004 | Copie fichiers .env | S01 | Logic | S | P1 | US-003 | ⬜ |
| US-005 | Setup script worktree-finalize.sh | S02 | Script | S | P1 | US-004 | ⬜ |
| US-006 | Detection contexte et validation | S02 | Logic | M | P1 | US-005 | ⬜ |
| US-007 | Merge et cleanup worktree | S02 | Logic | M | P1 | US-006 | ⬜ |
| US-008 | Gestion conflits merge | S02 | Logic | M | P1 | US-007 | ⬜ |
| US-009 | Setup script worktree-abort.sh | S02 | Script | S | P1 | US-005 | ⬜ |
| US-010 | Cleanup force sans merge | S02 | Logic | S | P1 | US-009 | ⬜ |
| US-011 | Integration /epci et /quick | S03 | Task | M | P1 | US-007 | ⬜ |
| US-012 | Suggestion worktree dans /brief | S03 | Task | S | P2 | US-004 | ⬜ |

---

## Par Spec

### S01 — Script worktree-create (4 stories)

| ID | Story | Type | Cx | Pri | Status |
|----|-------|------|----|----|--------|
| US-001 | Setup script worktree-create.sh | Script | S | P1 | ⬜ |
| US-002 | Validation arguments et prerequis | Logic | S | P1 | ⬜ |
| US-003 | Creation worktree avec branche | Logic | M | P1 | ⬜ |
| US-004 | Copie fichiers .env | Logic | S | P1 | ⬜ |

### S02 — Scripts finalize & abort (6 stories)

| ID | Story | Type | Cx | Pri | Status |
|----|-------|------|----|----|--------|
| US-005 | Setup script worktree-finalize.sh | Script | S | P1 | ⬜ |
| US-006 | Detection contexte et validation | Logic | M | P1 | ⬜ |
| US-007 | Merge et cleanup worktree | Logic | M | P1 | ⬜ |
| US-008 | Gestion conflits merge | Logic | M | P1 | ⬜ |
| US-009 | Setup script worktree-abort.sh | Script | S | P1 | ⬜ |
| US-010 | Cleanup force sans merge | Logic | S | P1 | ⬜ |

### S03 — Integration workflows (2 stories)

| ID | Story | Type | Cx | Pri | Status |
|----|-------|------|----|----|--------|
| US-011 | Integration /epci et /quick | Task | M | P1 | ⬜ |
| US-012 | Suggestion worktree dans /brief | Task | S | P2 | ⬜ |

---

## Statistiques

| Metrique | Valeur |
|----------|--------|
| Total stories | 12 |
| P1 (Must-have) | 11 |
| P2 (Should-have) | 1 |
| Complexite S | 7 |
| Complexite M | 5 |
| Complexite L | 0 |
| Parallelisables | 2 (US-009 // US-006) |
| Chemin critique | US-001 → US-002 → US-003 → US-004 → US-005 → US-006 → US-007 → US-011 |

---

## Par Priorite

### P1 — Must-have (11 stories)

| ID | Story | Spec | Cx |
|----|-------|------|----|
| US-001 | Setup script worktree-create.sh | S01 | S |
| US-002 | Validation arguments et prerequis | S01 | S |
| US-003 | Creation worktree avec branche | S01 | M |
| US-004 | Copie fichiers .env | S01 | S |
| US-005 | Setup script worktree-finalize.sh | S02 | S |
| US-006 | Detection contexte et validation | S02 | M |
| US-007 | Merge et cleanup worktree | S02 | M |
| US-008 | Gestion conflits merge | S02 | M |
| US-009 | Setup script worktree-abort.sh | S02 | S |
| US-010 | Cleanup force sans merge | S02 | S |
| US-011 | Integration /epci et /quick | S03 | M |

### P2 — Should-have (1 story)

| ID | Story | Spec | Cx |
|----|-------|------|----|
| US-012 | Suggestion worktree dans /brief | S03 | S |

---

## Legende

### Status
| Symbole | Signification |
|---------|---------------|
| ⬜ | Pending |
| 🔄 | In Progress |
| ✅ | Completed |
| ❌ | Blocked |
| ⏭️ | Skipped |

### Complexite (Cx)
| Code | Duree estimee |
|------|---------------|
| S | < 45 min |
| M | 45-90 min |
| L | > 90 min |

### Type
| Code | Description |
|------|-------------|
| Script | Creation fichier script |
| Logic | Implementation logique |
| API | Endpoint ou integration |
| UI | Interface utilisateur |
| Test | Tests automatises |
| Task | Tache generale |
