# Voice Cleaning — Dictation Cleanup Rules

> Rules for cleaning voice transcriptions before processing

---

## Overview

Voice dictations contain artifacts that must be cleaned before extraction. The goal is to normalize speech into clear, professional text while preserving meaning.

---

## Artifact Categories

### 1. Hesitations (Always Remove)

| Language | Artifacts |
|----------|-----------|
| French | euh, heu, hum, hmm, bah, ben, beh |
| English | uh, um, uhm, er, erm, ah |

**Regex pattern**:
```regex
\b(euh|heu|hum|hmm|bah|ben|uh|um|er|erm)\b
```

### 2. Filler Words (Usually Remove)

| French | English |
|--------|---------|
| tu vois | you know |
| genre | like |
| quoi | right |
| voilà | so/there |
| en fait | actually |
| du coup | so |
| bon | well |
| bref | anyway |
| enfin | well/I mean |
| c'est-à-dire | that is |

**Note**: "en fait" and "actually" may indicate correction — check context before removing.

### 3. Discourse Markers (Context-Dependent)

| Marker | Keep if... | Remove if... |
|--------|------------|--------------|
| "donc" | Logical conclusion | Just filler |
| "alors" | Temporal marker | Just filler |
| "bon" | Marks decision | Just pause |
| "voilà" | Marks completion | Just filler |

### 4. Repetitions (Deduplicate)

**Before**: "il faut, il faut que, il faut que le système..."
**After**: "il faut que le système..."

**Pattern**: Keep the most complete version of repeated starts.

### 5. False Starts (Keep Corrected Version)

**Before**: "on va faire un... non plutôt on fait une API REST"
**After**: "on fait une API REST"

**Markers**: "non", "plutôt", "en fait", "je veux dire", "pardon"

### 6. Self-Corrections

| Pattern | Before | After |
|---------|--------|-------|
| Explicit | "CSV, non pardon, JSON" | "JSON" |
| Implicit | "le fichier CSV... enfin JSON" | "le fichier JSON" |
| Hesitant | "peut-être CSV? non JSON" | "JSON" |

---

## Cleaning Pipeline

```
┌─────────────────────────────────────────┐
│ 1. PRESERVE rupture markers             │
│    (aussi, et puis, autre chose...)     │
└─────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────┐
│ 2. REMOVE hesitations                   │
│    (euh, hum, uh, um...)                │
└─────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────┐
│ 3. REMOVE obvious fillers               │
│    (tu vois, genre, quoi...)            │
└─────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────┐
│ 4. PROCESS corrections                  │
│    Keep corrected version only          │
└─────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────┐
│ 5. DEDUPLICATE repetitions              │
│    Keep most complete version           │
└─────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────┐
│ 6. NORMALIZE punctuation                │
│    Add periods, capitalize              │
└─────────────────────────────────────────┘
```

---

## Preservation Rules

### Always Preserve

| Category | Examples | Reason |
|----------|----------|--------|
| Technical terms | API, REST, CRUD, JSON | Domain accuracy |
| Product names | Symfony, React, Notion | Proper nouns |
| Numbers | "2 secondes", "3 fichiers" | Specifications |
| Rupture markers | "aussi", "et puis" | Multi-task detection |
| Emphasis markers | "important", "prioritaire" | Intent ranking |

### Never Modify

- Quoted strings (file names, error messages)
- Code snippets or commands
- URLs or paths
- Acronyms and abbreviations
- Foreign language terms intentionally used

---

## Normalization Rules

### Sentence Structure

**From**: "donc euh le truc là pour les factures tu vois faudrait que ça marche quoi"
**To**: "Le système de facturation doit fonctionner correctement."

Rules:
1. Add explicit subject (not "ça" → "le système")
2. Use formal verbs (not "marche" → "fonctionne")
3. Complete sentences with punctuation
4. Remove demonstratives without antecedent ("le truc là")

### Tense Normalization

| Input | Output |
|-------|--------|
| "faudrait que" | "doit" |
| "on voudrait" | "le système doit" |
| "ça serait bien si" | "le système doit" |
| "j'aimerais que" | "le système doit" |

### Voice Normalization

| Input | Output |
|-------|--------|
| "je veux" | "le système doit" |
| "tu peux" | "le système peut" |
| "on fait" | "le système réalise" |
| "l'utilisateur il clique" | "l'utilisateur clique" |

---

## Examples

### Example 1: Simple Cleanup

**Input**:
> "euh donc euh faudrait fixer le truc de login là tu vois c'est cassé depuis hier quoi"

**Output**:
> "Corriger le bug de login qui est cassé depuis hier."

### Example 2: With Correction

**Input**:
> "on va faire un export CSV, non pardon en fait plutôt JSON c'est mieux et euh voilà quoi"

**Output**:
> "Créer un export au format JSON."

### Example 3: Complex Cleaning

**Input**:
> "alors euh le dashboard là tu vois euh faut qu'il affiche les KPIs genre le chiffre d'affaires et tout ça et puis euh aussi faudrait les graphiques tu vois des trucs visuels quoi"

**Output**:
> "Le dashboard doit afficher les KPIs (chiffre d'affaires) et des graphiques visuels."

### Example 4: With Multi-Task Markers

**Input**:
> "donc euh fixer le login et puis aussi euh ajouter l'export PDF et puis euh ah et refacto le service auth"

**Output** (preserving markers):
> "Fixer le login. Et puis ajouter l'export PDF. Et puis refacto le service auth."

→ Multi-task detection will then segment on "et puis"

---

## Edge Cases

### Intentional Informal Language

If user says "le truc" but clearly means a specific thing mentioned earlier:
- **Don't** replace with generic term
- **Do** replace with the specific term from context

### Code-Switching (FR/EN mix)

Keep English technical terms as-is:
> "faut fixer le bug dans le controller" → "Corriger le bug dans le controller."

### Incomplete Thoughts

If a thought is cut off:
- Keep what's clear
- Mark as LOW confidence if critical info missing

### Emotional Expressions

Remove frustration expressions but note urgency:
> "c'est vraiment n'importe quoi ce bug là ça fait 3 jours" 
> → "Bug présent depuis 3 jours." (Note: urgent)

---

## Quality Indicators

After cleaning, the text should:

- [ ] Have no hesitation sounds
- [ ] Have no obvious filler words
- [ ] Have complete sentences
- [ ] Have proper punctuation
- [ ] Preserve all technical terms exactly
- [ ] Preserve rupture markers for multi-task detection
- [ ] Be readable as professional text
