---
name: step-08-generate
description: Write brief and journal files to disk
prev_step: steps/step-07-validate.md
next_step: steps/step-09-report.md
---

# Step 08: Generate

> Write brief and journal files to disk.

## Trigger

- Previous step: `step-07-validate.md` completed
- Or: `--quick` mode skipped validation

## Inputs

| Input | Source | Required |
|-------|--------|----------|
| `brief_final` | From step-07 (or brief_v0 if quick) | Yes |
| `ems` | Session state | Yes |
| `decisions[]` | Session state | Yes |
| `open_threads[]` | Session state | No |
| `techniques_applied` | Session state | No |
| `edit_history` | From step-07 | No |
| `security_audit` | From step-06 | No |
| `--quick` flag | From step-00 | No |

## Protocol

### 1. Generate Slug and Paths

```python
slug = slugify(idea_refined)  # e.g., "auth-oauth-integration"
date = datetime.now().strftime("%Y%m%d")

output_dir = f"docs/briefs/{slug}/"
brief_path = f"{output_dir}brief-{slug}-{date}.md"
journal_path = f"{output_dir}journal-{slug}-{date}.md"
```

### 2. Create Output Directory

```bash
mkdir -p docs/briefs/{slug}/
```

### 3. Generate Brief (PRD v3.0 Format)

@../references/brief-format.md
@../references/journal-format.md

#### 3.1 SECTIONS OBLIGATOIRES (15 sections - toutes requises)

🔴 **CRITIQUE**: Le brief DOIT contenir TOUTES les 15 sections suivantes.
NE PAS simplifier, NE PAS sauter de sections.

| # | Section | Points critiques |
|---|---------|------------------|
| 1 | Contexte et Objectif | Question initiale, Périmètre IN/OUT, Critères succès |
| 2 | Synthèse Exécutive | Insight clé, Décisions principales, Routing |
| 3 | Personas et Scénarios | Au moins 1 persona avec table attributs + scénario narratif |
| 4 | Analyse et Conclusions | Thèmes majeurs avec implications implémentation |
| 5 | User Stories et AC | **FORMAT GHERKIN OBLIGATOIRE** + edge cases |
| 6 | Décisions Techniques | Table avec Rationale, Impact, Confiance |
| 7 | Priorisation MoSCoW | Must/Should/Could/Won't avec effort estimé |
| 8 | Contraintes et Dépendances | Techniques + Externes avec SLA/Fallback |
| 9 | Risques et Hypothèses | Probabilité/Impact + Mitigation |
| 10 | Plan d'Action | Phases séquentielles avec Owner/Prérequis |
| 11 | Mindmap de Synthèse | **MERMAID OBLIGATOIRE** |
| 12 | Score EMS Final | **GRAPHE ASCII OBLIGATOIRE** + Radar 5 axes |
| 13 | Pistes Non Explorées | Valeur potentielle + Prochaine étape |
| 14 | Références | Documents/Web/Conversations passées |
| 15 | Prochaines Étapes | Routing + Commande suggérée |

#### 3.2 Templates Critiques (inline - NE PAS SIMPLIFIER)

**Header du Brief**:
```markdown
# [Titre du Brainstorming]

> Généré le {date} - {iterations} itérations - Template: {template} - EMS final: {ems.global}/100
```

**Section 5 - Format Gherkin OBLIGATOIRE**:
```gherkin
AC1: [Titre du critère]
Given [précondition/contexte]
When [action utilisateur]
Then [résultat attendu]
And [résultat additionnel si applicable]
```

**Section 12 - Graphe EMS ASCII OBLIGATOIRE**:
```
EMS Final: {ems.global}/100 {status}

Progression EMS
100 |
 90 | . . . . . . . . . . . . . . . . . . . .
 80 |
 70 |          ●───────●
 60 | . . . . . . . . . . . . . . . . . . . .
 50 |    ●────●
 40 |
 30 | ●. . . . . . . . . . . . . . . . . . .
 20 |
  0 +----+-----+-----+-----+-----+-----+
    Init  It.1  It.2  It.3  ...  Fin

Axes finaux:
   Clarté       [████████░░] {clarity}/100
   Profondeur   [███████░░░] {depth}/100
   Couverture   [████████░░] {coverage}/100
   Décisions    [█████████░] {decisions}/100
   Actionab.    [████████░░] {actionability}/100
```

#### 3.3 Construction du Brief

Apply template from brief-format.md:
- Populate **ALL 15 sections** with session data
- Include complexity routing from step-06
- Inject security audit recommendations if available
- Use EMS history for section 12 graph

### 4. Validation Pré-Écriture (OBLIGATOIRE)

🔴 **AVANT d'appeler Write()**, vérifie que le brief contient:

```
CHECKLIST PRÉ-ÉCRITURE:
[ ] Header avec EMS final, iterations, template
[ ] 15 sections numérotées (1-15)
[ ] Section 1: Question initiale + Périmètre IN/OUT + Critères
[ ] Section 2: Insight clé en gras + Routing recommandé
[ ] Section 3: Au moins 1 persona avec table attributs
[ ] Section 5: Format Gherkin (Given/When/Then) pour CHAQUE AC
[ ] Section 5: Edge cases pour CHAQUE User Story
[ ] Section 7: 4 catégories MoSCoW (Must/Should/Could/Won't)
[ ] Section 9: Table avec Probabilité ET Impact
[ ] Section 11: Bloc mermaid mindmap
[ ] Section 12: Graphe ASCII progression EMS
[ ] Section 12: Radar 5 axes avec barres visuelles
[ ] Section 15: Commande suggérée avec slug
```

⛔ **SI sections manquantes**: ALERTE et COMPLÈTE avant écriture.
⛔ **NE PAS écrire un brief incomplet**.

### 5. Write Brief File

```python
Write(brief_path, brief_content)
```

### 6. Generate Journal (skip if --quick)

Apply template from journal-format.md:
- Populate iteration history with **all EMS progression data from ems.history**
- Include all decisions, open threads, and persona switches
- Add techniques applied and phase transitions
- Write to: `{journal_path}`

⛔ **Le journal DOIT contenir**:
- [ ] Progression EMS par itération (tableau)
- [ ] Décisions prises avec timestamps
- [ ] Open threads non résolus
- [ ] Persona switches (si applicable)
- [ ] Techniques appliquées (si applicable)

### 7. Write Journal File

```python
Write(journal_path, journal_content)
```

### 8. Update Session State

```json
{
  "generation_complete": true,
  "output_files": [
    "{brief_path}",
    "{journal_path}"
  ],
  "slug": "{slug}",
  "brief_sections_count": 15,
  "ems_final": "{ems.global}"
}
```

### 8.5 Finalize Session File (OBLIGATOIRE)

🔴 **CRITIQUE**: Marquer la session comme terminée dans le fichier JSON.

```
# Load session
session = JSON.parse(Read(session_path))

# Mark as completed
session.status = "completed"
session.timestamps.ended_at = NOW()
session.timestamps.last_update = NOW()

# Add output file references
session.output_files = [brief_path, journal_path]
IF file_exists(decisions_path):
  session.output_files.append(decisions_path)

session.generation_complete = true
session.ems_final = ems.global
session.brief_sections_count = 15

# Persist final state
Write(session_path, JSON.stringify(session, indent=2))

DISPLAY: "Session finalized: {session_id}"
```

### 8.6 Finalize Decisions File

Si le fichier decisions.md existe, mettre à jour le statut final:

```
IF file_exists(decisions_path):
  content = Read(decisions_path)

  # Update summary with final EMS
  content = update_summary(content, len(session.decisions), ems.global, iteration)

  # Add completion note
  completion_note = """
---

## Session Completed

| Attribute | Value |
|-----------|-------|
| **Final EMS** | {ems.global}/100 |
| **Total iterations** | {iteration} |
| **Brief generated** | {brief_path} |
| **Journal generated** | {journal_path} |
| **Completed at** | {NOW()} |
"""
  content = append_section(content, completion_note)

  Write(decisions_path, content)
```

## Outputs

| Output | Destination |
|--------|-------------|
| `brief-{slug}-{date}.md` | `docs/briefs/{slug}/` |
| `journal-{slug}-{date}.md` | `docs/briefs/{slug}/` |
| `decisions-{slug}.md` (finalized) | `docs/briefs/{slug}/` |
| Session JSON (completed) | `.claude/state/sessions/{session_id}.json` |
| `generation_complete` | Session state + JSON |
| `output_files` | Session state + JSON |

## Next Step

→ `step-09-report.md`

## Error Handling

| Error | Resolution |
|-------|------------|
| Directory creation fails | Try alternative path |
| Write permission denied | Warn user, output to console |
| File already exists | Add suffix (-v2, -v3) |
| Missing sections | STOP - Complete all 15 sections before write |
| EMS history empty | STOP - Run ems-evaluator first |
| No Gherkin AC | STOP - Reformat section 5 with Given/When/Then |

## Quality Gate

🔴 **NE JAMAIS générer un brief avec moins de 15 sections.**
🔴 **NE JAMAIS omettre le graphe EMS ASCII en section 12.**
🔴 **NE JAMAIS utiliser un format simplifié pour les User Stories.**
