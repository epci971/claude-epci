# Output Template Reference

> Complete Markdown template for meeting minutes output

---

## Full Template — Meeting Transcription

```markdown
# 📋 Compte-rendu — [Titre/Sujet/Date]

**Type** : [Type de réunion détecté]  
**Participants** : [Liste des intervenants identifiés]

---

## 🎯 Synthèse exécutive

- [Point essentiel 1]
- [Point essentiel 2]
- [Point essentiel 3]
- [Point essentiel 4 si pertinent]
- [Point essentiel 5 si pertinent]

---

## 📌 Contexte

[Description du contexte de la réunion : pourquoi elle a lieu, quel est le cadre, les enjeux. 2-4 phrases.]

---

## 💬 Points abordés

### [Sujet 1]

[Développement exhaustif du premier sujet discuté. Inclure les positions exprimées, les échanges clés, les nuances.]

### [Sujet 2]

[Développement exhaustif du deuxième sujet...]

### [Sujet N]

[Continuer pour chaque sujet majeur abordé]

---

## ✅ Décisions prises

- [Décision 1 - claire et actionnable]
- [Décision 2]
- [Décision N]

---

## 📝 Actions à mener

| Responsable | Action | Échéance |
|-------------|--------|----------|
| [Nom] | [Description claire et complète de l'action] | [Date ou -] |
| [Nom] | [Action 2] | [Date ou -] |
| [Nom] | [Action N] | [Date ou -] |

> ⚠️ Cette section doit être la plus exhaustive possible. Chaque engagement évoqué doit y figurer.

---

## ⚠️ Points de vigilance

- [Risque ou blocage potentiel 1]
- [Sujet sensible 2]
- [Dépendance critique 3]

---

## ❓ Questions ouvertes

- [Question non résolue 1]
- [Sujet à approfondir 2]
- [Point nécessitant clarification 3]

---

## 💬 Verbatims clés

> "[Citation importante mot pour mot]" — [Nom du participant]

> "[Autre citation notable]" — [Nom]

---
```

---

## Template Variations

### Concise Version (on request)

```markdown
# 📋 [Titre] — [Date]

**Participants** : [Liste]

## 🎯 Synthèse
[3-5 bullet points]

## 📝 Actions
| Qui | Quoi | Quand |
|-----|------|-------|

## ⚠️ Points d'attention
[Si pertinent]
```

### Detailed Version (on request)

Use full template + add:
- Timestamps if available
- Extended quotes
- Detailed participant contributions
- Cross-references to previous meetings

---

## Section Guidelines

### 🎯 Synthèse exécutive

**Purpose**: Allow reader to understand meeting outcomes in 30 seconds

**Rules**:
- 3-5 bullet points maximum
- Start with most important outcome
- Include key decisions and critical actions
- No details, just headlines
- Written for someone who won't read the rest

**Example**:
```markdown
## 🎯 Synthèse exécutive

- Budget Q1 validé à 150K€ avec réserve de 10%
- Lancement prévu le 15 janvier, go/no-go le 10
- Marie pilote le workstream technique, Pierre la comm
- Risque identifié sur les délais fournisseur
- Prochaine réunion de suivi le 20 décembre
```

---

### 📌 Contexte

**Purpose**: Frame the meeting for future readers

**Include**:
- Why this meeting happened
- Key stakeholders involved
- Relevant background
- Link to previous discussions if applicable

**Length**: 2-4 sentences

---

### 💬 Points abordés

**Purpose**: Comprehensive record of discussion

**Rules**:
- Use subheadings for distinct topics
- Be exhaustive — don't summarize away important nuances
- Include different viewpoints expressed
- Note disagreements or debates
- Preserve the flow of discussion when relevant

---

### ✅ Décisions prises

**Purpose**: Clear record of what was agreed

**Rules**:
- One decision per bullet
- Use active, clear language
- Include conditions if any ("sous réserve de...")
- Note who made or approved the decision if relevant

---

### 📝 Actions à mener

**Purpose**: Actionable task list for follow-up

**Rules**:
- **CRITICAL**: Capture EVERY action mentioned
- One action per row
- Clear ownership (name, not "someone")
- Specific description (not "handle the thing")
- Deadline or "-" if none specified
- Include implicit commitments

**Table format**:
```markdown
| Responsable | Action | Échéance |
|-------------|--------|----------|
```

---

### ⚠️ Points de vigilance

**Purpose**: Flag risks and concerns

**Include**:
- Explicit risks mentioned
- Dependencies identified
- Concerns raised by participants
- Potential blockers
- Sensitive topics requiring care

**Skip if**: Nothing was flagged

---

### ❓ Questions ouvertes

**Purpose**: Track unresolved items

**Include**:
- Questions asked but not answered
- Topics deferred for later
- Items needing research
- Decisions pending external input

**Skip if**: All questions were resolved

---

### 💬 Verbatims clés

**Purpose**: Preserve important exact quotes

**When to include**:
- Strong statements that matter
- Commitments that need exact wording
- Notable insights or concerns
- Potentially controversial statements

**Format**: Always attribute with participant name

**Skip if**: No particularly notable quotes

---

## Formatting Rules

### Markdown Hygiene

- Use `##` for main sections, `###` for subsections
- Blank line before and after headers
- Blank line before and after tables
- Consistent emoji usage (one per section header)
- No trailing spaces

### Table Formatting

```markdown
| Column 1 | Column 2 | Column 3 |
|----------|----------|----------|
| Data | Data | Data |
```

- Align pipes visually when possible
- Use `-` for empty cells, not blank

### Lists

- Use `-` for unordered lists
- Consistent indentation
- No numbered lists except for explicit sequences

---

## URL/Article Template

```markdown
# 📄 Résumé — [Article Title]

**Source** : [URL]  
**Date** : [Publication date if available]  
**Auteur** : [Author if available]

---

## 🎯 Points clés

- [Key point 1]
- [Key point 2]
- [Key point 3]

---

## 📌 Contexte

[What the article is about, why it matters]

---

## 💬 Contenu détaillé

### [Section 1]
[Summary of section]

### [Section 2]
[Summary of section]

---

## 💡 À retenir

[Key takeaways, implications, relevance]

---
```

---

## PDF/Document Template

```markdown
# 📄 Résumé — [Document Title]

**Type** : [Document type: rapport, présentation, spec...]  
**Pages** : [Number if relevant]

---

## 🎯 Synthèse

[3-5 bullet points summarizing the document]

---

## 📌 Objectif du document

[What the document aims to achieve]

---

## 💬 Contenu principal

### [Section 1]
[Summary]

### [Section 2]
[Summary]

---

## 📝 Éléments actionnables

[If the document contains action items, recommendations, or next steps]

---
```
