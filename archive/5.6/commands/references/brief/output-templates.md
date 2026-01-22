# Templates de Sortie

> Templates pour les outputs générés par /brief

---

## TINY/SMALL: Brief Inline

Générer un brief structuré directement dans la réponse (pas de fichier créé):

```markdown
# Functional Brief — [Title]

## Context

[Résumé du besoin en 2-3 phrases]

## Detected Stack

[Stack identifié par @Explore]

## Target Files

- `path/to/file.ext` (action: Create/Modify)

## Acceptance Criteria

- [ ] Critère 1 (mesurable)
- [ ] Critère 2 (mesurable)

## Memory Summary

[Si .project-memory/ existe, inclure contexte clé:]

- **Project**: [nom projet depuis context.json]
- **Conventions**: [conventions clés depuis conventions.json]
- **Patterns**: [patterns pertinents si présents]

## Category: [TINY|SMALL]

## Suggested Flags

- [flag] (auto/recommended) — si détectés

→ Launch `/quick`
```

---

## STANDARD/LARGE: Feature Document

**OBLIGATOIRE:** Utiliser le **Write tool** (PAS EnterPlanMode, PAS mode plan natif) pour créer `docs/features/<slug>-<YYYYMMDD-HHmmss>.md`

```markdown
# Feature Document — [Title]

> **Slug**: `<slug>`
> **Category**: [STANDARD|LARGE]
> **Date**: [YYYY-MM-DD]

---

## §1 — Functional Brief

### Context

[Résumé du besoin]

### Detected Stack

- **Framework**: [détecté]
- **Language**: [détecté]
- **Patterns**: [patterns détectés]

### Acceptance Criteria

- [ ] Critère 1 (mesurable)
- [ ] Critère 2 (mesurable)

### Constraints

- [Contrainte technique]
- [Autre contrainte si applicable]

### Out of Scope

- [Exclusion explicite 1]
- [Exclusion explicite 2]

### Evaluation

- **Category**: [STANDARD|LARGE]
- **Estimated files**: X
- **Estimated LOC**: ~Y
- **Risk**: [Low|Medium|High]
- **Justification**: [Raison de catégorisation]

### Suggested Flags

| Flag           | Source | Reason              |
| -------------- | ------ | ------------------- |
| `--think-hard` | auto   | >10 files impacted  |
| `--safe`       | auto   | auth files detected |
| `--wave`       | auto   | complexity > 0.7    |

### Memory Summary

[Si .project-memory/ existe, inclure contexte chargé au Step 0:]

- **Project**: [nom projet]
- **Stack**: [stack détecté depuis context.json]
- **Conventions**: [conventions clés]
- **Velocity**: [features_completed count, si disponible]

---

## §2 — Implementation Plan

[À compléter par /epci Phase 1]

---

## §3 — Implementation & Finalization

[À compléter par /epci Phases 2-3]
```

---

## CRITIQUE: Feature Document vs Mode Plan Natif

**NE PAS** utiliser le mode plan natif de Claude Code pour les Feature Documents EPCI.

| ❌ INCORRECT | ✅ CORRECT |
|--------------|-----------|
| EnterPlanMode tool | Write tool |
| `~/.claude/plans/` | `docs/features/<slug>-<YYYYMMDD-HHmmss>.md` |
| Plan natif Claude Code | Feature Document EPCI |

**Raison**: Les Feature Documents EPCI sont des fichiers persistants dans le repo git pour traçabilité, pas des plans temporaires Claude Code.

---

## Validation du Path

```
IF output_path contains ".claude/plans":
   ╔══════════════════════════════════════════════════════════════╗
   ║ ❌ ERROR: Wrong Output Path                                   ║
   ╠══════════════════════════════════════════════════════════════╣
   ║ Feature Documents must be saved in docs/features/             ║
   ║ NOT in ~/.claude/plans/                                       ║
   ║                                                               ║
   ║ → Use Write tool with path: docs/features/<slug>-<ts>.md      ║
   ╚══════════════════════════════════════════════════════════════╝
   RETRY with correct path
```

**Exigences du path**:
- Path DOIT être `docs/features/<slug>-<YYYYMMDD-HHmmss>.md` (dans répertoire projet)
- Path NE DOIT PAS être `~/.claude/plans/` ou `.claude/plans/`
- Tool DOIT être Write, PAS EnterPlanMode
- Le timestamp utilise le format ISO: année-mois-jour-heure-minute-seconde
