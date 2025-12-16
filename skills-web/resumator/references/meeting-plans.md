# Meeting Plans Reference

> Structured plans for different meeting types

---

## Plan Selection Logic

```
1. Scan content for type indicators
2. Match to closest plan type
3. If no clear match → use Generic plan
4. Adapt sections based on actual content (skip empty, add if needed)
```

---

## Plan 1: Steering / Decision Meeting

**Indicators**: "décision", "valider", "arbitrer", "budget", "deadline", "go/no-go", "validation"

### Structure

```markdown
## 📌 Contexte
[Why this meeting, what needs to be decided]

## 🎯 Problématique
[Core issue or question requiring decision]

## 💡 Solutions discutées
[Options presented and analyzed]

## ✅ Décisions prises
[Clear list of what was decided]

## 📝 Actions à mener
| Responsable | Action | Échéance |
|-------------|--------|----------|

## ⚠️ Points de vigilance
[Risks, dependencies, blockers identified]
```

---

## Plan 2: Information Meeting

**Indicators**: "informer", "présenter", "update", "point", "avancement", announcement language

### Structure

```markdown
## 📌 Contexte
[Meeting purpose and scope]

## 📢 Informations clés
[Main announcements and updates, organized by topic]

## ⚠️ Points de vigilance
[Items requiring attention or follow-up]

## ❓ Questions ouvertes
[Unresolved questions raised during meeting]

## 📝 Actions à mener
| Responsable | Action | Échéance |
|-------------|--------|----------|
```

---

## Plan 3: Brainstorming

**Indicators**: "idées", "propositions", "explorer", "brainstorm", creative/exploratory language

### Structure

```markdown
## 📌 Contexte
[Topic being explored, objectives]

## 💡 Idées évoquées
[All ideas mentioned, grouped thematically if possible]

## ⭐ Pistes retenues
[Ideas selected for further exploration]

## 🚫 Pistes écartées
[Ideas dismissed and why, if discussed]

## 📝 Prochaines étapes
| Responsable | Action | Échéance |
|-------------|--------|----------|
```

---

## Plan 4: Training / Workshop

**Indicators**: "formation", "atelier", "exercice", "apprendre", learning objectives, pedagogical structure

### Structure

```markdown
## 🎯 Objectifs de la session
[Learning goals, expected outcomes]

## 📚 Contenu traité
[Topics covered, organized by section]

## ❓ Questions posées
[Questions from participants with answers if provided]

## 📌 Points clés à retenir
[Key takeaways, summary of learning]

## 📝 Prochaines étapes
| Responsable | Action | Échéance |
|-------------|--------|----------|
```

---

## Plan 5: Individual Review / 1:1

**Indicators**: One-on-one context, "feedback", "évaluation", "objectifs", performance language

### Structure

```markdown
## 📌 Contexte
[Purpose of the review, period covered]

## 💬 Feedback échangé
[Key feedback points discussed]

## ⭐ Points forts
[Strengths identified]

## 📈 Axes d'amélioration
[Areas for development]

## 🎯 Objectifs définis
[Goals set for next period]

## 📝 Actions à mener
| Responsable | Action | Échéance |
|-------------|--------|----------|
```

---

## Plan 6: Generic (Fallback)

**Use when**: No clear meeting type detected, mixed content, or unusual format

### Structure

```markdown
## 📌 Contexte
[Meeting background and purpose]

## 💬 Points abordés
[Topics discussed, organized logically]

## ✅ Décisions prises
[Any decisions made]

## 📝 Actions à mener
| Responsable | Action | Échéance |
|-------------|--------|----------|

## ⚠️ Points de vigilance
[Issues flagged, concerns raised]

## ❓ Questions ouvertes
[Unresolved items]
```

---

## Adaptation Guidelines

### Adding Sections

Add sections if content warrants:
- **💬 Verbatims clés**: If notable quotes were made
- **📊 Chiffres mentionnés**: If specific numbers/metrics discussed
- **📅 Dates clés**: If timeline discussed
- **👥 Parties prenantes**: If stakeholder mapping relevant

### Removing Sections

Skip sections that would be empty:
- Don't include "Questions ouvertes" if none were raised
- Don't include "Points de vigilance" if none identified
- Never skip "Actions à mener" — include even if empty with note "Aucune action identifiée"

### Merging Sections

Combine sections if content overlaps:
- "Décisions" + "Actions" can merge if decisions directly imply actions
- "Points de vigilance" + "Questions ouvertes" can merge into "Points d'attention"

---

## Action Item Extraction Rules

### What Counts as an Action Item

✅ Include:
- Explicit assignments: "Jean va faire X"
- Commitments: "Je m'en occupe"
- Deadlines mentioned: "pour vendredi"
- Requests: "Peux-tu vérifier Y?"
- Implicit tasks: If someone says "il faudrait que..." and context implies they'll do it

❌ Exclude:
- Vague intentions without ownership: "On devrait penser à..."
- Past actions: "J'ai déjà fait X"
- Questions without assignment: "Qui pourrait s'en charger?" (unless answered)

### Deadline Handling

| Mentioned | Format |
|-----------|--------|
| Specific date | "15 décembre" |
| Relative | "Demain", "Semaine prochaine" |
| Vague | "Rapidement", "Dès que possible" |
| None | "-" (dash, not empty) |

### Responsibility Attribution

- Use names when clearly stated
- Use role if name unknown: "Responsable technique"
- Use "Équipe" for collective actions
- Use "À définir" if unassigned
