# Output Format — Brief Structure Reference

> Complete specification for PROMPTOR brief output

---

## Standard Mode Structure

Every standard brief follows this exact structure. All sections are **mandatory**. Use explicit absence markers when information is not available.

---

### Header (Metadata)

```markdown
<!-- PROMPTOR_META
confidence: high|medium|low
mode: standard
source_complexity: short|medium|long
extraction_gaps: 0|1-2|3+
-->
```

**Confidence determination**:
- **high**: Clear single intent + ≥2 explicit FR + no contradictions
- **medium**: Clear intent + some gaps OR resolved contradictions
- **low**: Vague intent OR major gaps OR unresolved ambiguities

---

### Section 1: Feature Title

```markdown
# [Concise Descriptive Title]
```

**Rules**:
- Short and descriptive (5-10 words max)
- Reformulation of main intent
- No person names, no transcript references
- Action-oriented when possible

**Examples**:
- ✅ "Module de gestion des factures avec synchronisation API"
- ✅ "Dashboard temps réel pour KPIs commerciaux"
- ❌ "Ce que Jean veut pour le projet X"
- ❌ "Feature demandée dans le transcript"

---

### Section 2: Objective

```markdown
## Objective

[2-4 sentences describing the purpose]
```

**Rules**:
- Answers "What is this for? Why build it?"
- Reflects **final version** of intent (if changed during transcript)
- No implementation details
- Written in present tense, neutral voice

**Template**:
```
Cette fonctionnalité vise à [GOAL]. Elle permettra de [BENEFIT 1] et [BENEFIT 2]. 
Le besoin principal est de [CORE NEED].
```

---

### Section 3: Description

```markdown
## Description

[1-3 short paragraphs]
```

**Content**:
- Context in which the feature operates
- High-level functioning overview
- Key elements mentioned narratively
- **Not** a copy of the transcript

**Rules**:
- Factual, no speculation
- Third person, neutral tone
- Connects objective to requirements

---

### Section 4: Functional Requirements

```markdown
## Functional Requirements

- [FR1] [Observable behavior description]
- [FR2] [Observable behavior description]
- [FR3] [Observable behavior description]
```

**If none explicitly mentioned**:
```markdown
## Functional Requirements

- Aucun FR explicitement mentionné dans la source.
```

**FR Criteria** (must meet ALL):
1. Describes **observable behavior** (what system does)
2. **Explicitly stated** or **directly deductible**
3. Testable (can verify if implemented)

**FR Categories**:
| Type | Examples |
|------|----------|
| CRUD | "L'utilisateur peut créer/lire/modifier/supprimer..." |
| Business rules | "Le système calcule X selon la formule Y" |
| Interactions | "Un clic sur Z déclenche l'action W" |
| Integrations | "Les données sont synchronisées avec le système X" |

---

### Section 5: Non-Functional Requirements

```markdown
## Non-Functional Requirements

- [NFR1] [Quality attribute description]
- [NFR2] [Quality attribute description]
```

**If none explicitly mentioned**:
```markdown
## Non-Functional Requirements

- Aucun NFR explicitement mentionné dans la source.
```

**NFR Categories**:
| Category | Examples |
|----------|----------|
| Performance | "Temps de réponse < 2 secondes" |
| Security | "Authentification requise", "Données chiffrées" |
| UX | "Interface responsive", "Accessible WCAG 2.1" |
| Reliability | "Disponibilité 99.9%", "Sauvegarde automatique" |
| Scalability | "Supporte 1000 utilisateurs simultanés" |

---

### Section 6: Constraints & Technical Context

```markdown
## Constraints & Technical Context

- [Stack or technology constraint]
- [External system constraint]
- [Data format constraint]
- [Business/regulatory constraint]
```

**If none explicitly mentioned**:
```markdown
## Constraints & Technical Context

- Aucune contrainte technique ou métier explicitement mentionnée.
```

**Constraint Types**:
| Type | Examples |
|------|----------|
| Stack | "Symfony 7", "React 18", "PostgreSQL" |
| External systems | "API bancaire X", "ERP existant" |
| Data | "Format CSV requis", "Max 10 Mo par fichier" |
| Business | "Conformité RGPD", "Process interne Y" |
| Timeline | "Livraison avant Q2" (if explicitly stated) |

---

### Section 7: Important Notes

```markdown
## Important Notes

- [Secondary idea or future consideration]
- [Abandoned alternative (if useful context)]
- [Explicit "to be defined later" items]
```

**If none applicable**:
```markdown
## Important Notes

- Aucune note complémentaire spécifique.
```

**What goes here**:
- Secondary intents (not primary objective)
- Ideas marked as "optional", "later", "maybe"
- Abandoned approaches (only if provides useful context)
- Explicit uncertainties from source

---

## Compact Mode Structure

For transcripts < 100 words with single clear intent:

```markdown
<!-- PROMPTOR_META
confidence: high|medium|low
mode: compact
-->

# [Title]

## Objective

[2-3 sentences]

## Quick Notes

- [Key point 1]
- [Key point 2]
- Or: Aucune note complémentaire.
```

---

## Formatting Rules

### General
- Markdown format, valid syntax
- Headings with `##` (except title with `#`)
- Lists with `- ` (hyphen + space)
- No emojis in body content
- No bold/italic abuse

### Language
- Match source language
- Mixed source → French structure, English technical terms preserved
- Professional register, no colloquialisms

### Absence Markers
Always use these exact phrases:
- `Aucun FR explicitement mentionné dans la source.`
- `Aucun NFR explicitement mentionné dans la source.`
- `Aucune contrainte technique ou métier explicitement mentionnée.`
- `Aucune note complémentaire spécifique.`

---

## Anti-Patterns to Avoid

| Anti-Pattern | Problem | Correct Approach |
|--------------|---------|------------------|
| "Le transcript mentionne..." | References source | Write self-contained content |
| "L'utilisateur souhaite..." | References person | "La fonctionnalité vise à..." |
| Inventing FR not mentioned | Scope creep | Mark as absent |
| Combining multiple features | Confusion | One brief per intent |
| Keeping contradictions | Ambiguity | Latest version wins |
| Meta-commentary | Noise | Facts only |
