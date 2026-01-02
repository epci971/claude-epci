---
description: >-
  Transform voice dictations into structured Notion tasks. Supports one-shot
  and session modes with multi-task detection. Generates briefs (1h/4h/8h)
  and exports directly to Notion via API. Standalone tool, independent from
  EPCI workflow.
argument-hint: "[dictation] | session"
allowed-tools: [Read, Glob, Grep, Write, Bash]
---

# /promptor — Dictation to Notion Tasks

## Overview

Transform raw voice dictations or text into structured development briefs
and export them directly to Notion. Standalone pense-bête tool.

## Usage

```bash
# One-shot mode
/promptor fixer le bug de login qui ne fonctionne plus depuis hier

# Session mode
/promptor session
```

## Configuration

| Element | Value |
|---------|-------|
| **Thinking** | `think` |
| **Skills** | promptor |
| **Notion** | API directe via Bash/curl |

### Notion Setup

Configure in `.claude/settings.local.json`:

```json
{
  "notion": {
    "token": "ntn_xxx",
    "tasks_database_id": "xxx",
    "default_project_id": "xxx"
  }
}
```

See `.claude/settings.local.json.example` for template.

---

## Process

### Mode Detection

```
/promptor session     → SESSION MODE (multi-dictation)
/promptor [text]      → ONE-SHOT MODE (single dictation)
```

### One-Shot Mode

1. **Receive dictation** from command argument
2. **Clean** voice artifacts (hesitations, fillers)
3. **Detect** mono vs multi-task
4. **If multi-task**: Show checkpoint, wait for user choice
5. **Generate** brief(s) based on complexity
6. **Export** to Notion (if configured)
7. **Display** confirmation or brief text

### Session Mode

1. **Initialize** session
   ```
   🎯 **Session Promptor active**
   
   Mode: Traitement en série
   Export: Notion (si configuré)
   
   Envoyez votre première dictée.
   ```

2. **For each dictation**:
   - Clean → Detect → Checkpoint (if multi) → Generate → Export
   - Reset context for next dictation

3. **End session** with "fin session":
   ```
   📊 **Résumé session Promptor**
   
   | # | Tâche | Type | Temps |
   |---|-------|------|-------|
   | 1 | ... | ... | ... |
   
   ✅ {n} tâches créées | ⏱️ Total: {h}h
   ```

---

## Multi-Task Detection

### Algorithm

1. **Clean** dictation (preserve rupture markers)
2. **Segment** on markers ("aussi", "et puis", "autre chose", etc.)
3. **Score** each segment for independence (threshold: 40)
4. **Decide**: ≥2 segments with score ≥40 → MULTI-TASK

### Checkpoint Display

```
📋 **{n} tâches détectées**

┌───┬─────────────────────────┬──────────┬────────────┬───────┐
│ # │ Titre suggéré           │ Type     │ Complexité │ Temps │
├───┼─────────────────────────┼──────────┼────────────┼───────┤
│ 1 │ [Title]                 │ [Type]   │ [Level]    │ [h]h  │
└───┴─────────────────────────┴──────────┴────────────┴───────┘

📖 Commandes: ok | ok 1,2 | merge 1,2 | edit N "x" | drop N
```

### Checkpoint Commands

| Command | Action |
|---------|--------|
| `ok` | Generate all briefs |
| `ok 1,2` | Generate only selected |
| `merge 1,2` | Combine into single task |
| `edit N "x"` | Change title of task N |
| `drop N` | Remove task N |

---

## Brief Generation

### Complexity Detection

| Level | Criteria | Time |
|-------|----------|------|
| **Quick fix** | <50 words, corrective verb | 1h |
| **Standard** | 50-200 words, clear scope | 4h |
| **Major** | >200 words, multi-component | 8h |

### Brief Structure

```markdown
# [Action Verb] [Object]

📦 **[Complexity]** | ⏱️ [Time] | 🎯 Confidence: [Level]

## Objectif
[Purpose and benefit]

## Description (Standard/Major only)
[Context and functioning]

## Exigences fonctionnelles
- [FR list]

## Plan d'implémentation (Standard/Major only)
1. **[Phase]**
   - [ ] Subtask

## Notes
- [Notes or "Aucune note complémentaire."]
```

→ See skill `promptor` for full templates

---

## Notion Export

### When Configured

After generating brief:
1. Create page in tasks database via API (curl)
2. Map properties (Nom, Type, Temps estimé, DAY, Projet)
3. Add page content (children blocks)
4. Display confirmation with link

### When Not Configured

Display brief as formatted text with message:
```
📋 Brief prêt — Copier dans Notion manuellement
```

### On Error

```
⚠️ **Erreur Notion** — {message}

[Brief displayed for manual copy]

🔄 `retry` pour réessayer | `skip` pour continuer
```

---

## Session Commands

| Command | Action |
|---------|--------|
| `status` | Show session state |
| `fin session` | End and show summary |

---

## Critical Rules

1. **Never ask questions** — Produce brief with available info
2. **Never invent requirements** — Mark absent if not mentioned
3. **Never reference source** — Brief is self-contained
4. **Each dictation = isolated context** — No pollution between inputs
5. **Later wins** — Last stated version overrides earlier

---

## Examples

### One-Shot Bug Fix

```
User: /promptor fixer le bug login qui crash depuis la mise à jour

Claude: 
# Corriger le crash du login après mise à jour

📦 **Quick fix** | ⏱️ 1h | 🎯 Confidence: HIGH

## Objectif
Corriger le crash du module de login qui survient depuis 
la dernière mise à jour.

## Contexte
Le problème est apparu suite à une mise à jour récente.

## Correction attendue
- Identifier la cause du crash dans le module login
- Appliquer le correctif
- Vérifier le fonctionnement

## Notes
- Aucune note complémentaire.

═══════════════════════════════════════════════════════════════════
✅ Tâche créée : [Corriger le crash...](notion_link)
📂 Projet: Default | 🏷️ Type: Bloquant | ⏱️ 1h
═══════════════════════════════════════════════════════════════════
```

### Multi-Task Detection

```
User: /promptor il faut fixer le login et aussi ajouter l'export PDF

Claude:
📋 **2 tâches détectées** [confiance: HAUTE]

┌───┬──────────────────────────────┬───────────┬────────────┬───────┐
│ # │ Titre suggéré                │ Type      │ Complexité │ Temps │
├───┼──────────────────────────────┼───────────┼────────────┼───────┤
│ 1 │ Corriger le bug de login     │ Bloquant  │ Quick fix  │ 1h    │
│ 2 │ Implémenter l'export PDF     │ Evolution │ Standard   │ 4h    │
└───┴──────────────────────────────┴───────────┴────────────┴───────┘

📝 Segments extraits:
   1 ← "fixer le login"
   2 ← "ajouter l'export PDF"

📖 Commandes: ok | merge 1,2 | edit N "x" | drop N

User: ok

Claude: [Generates both briefs and exports to Notion]
```

---

## Limitations

- No clarifying questions (produces with available info)
- No modification of existing Notion tasks
- No integration with EPCI workflow
- Standalone pense-bête tool only
