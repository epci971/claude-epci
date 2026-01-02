# Voice Cleaning — Dictation Cleanup Rules

> Rules for cleaning voice transcriptions before processing

---

## Cleaning Pipeline

```
1. PRESERVE rupture markers (aussi, et puis, autre chose...)
2. REMOVE hesitations (euh, hum, uh, um...)
3. REMOVE obvious fillers (tu vois, genre, quoi...)
4. PROCESS corrections (keep corrected version only)
5. DEDUPLICATE repetitions (keep most complete)
6. NORMALIZE punctuation
```

---

## Artifacts to Remove

### Hesitations (Always Remove)

| French | English |
|--------|---------|
| euh, heu, hum, hmm, bah, ben | uh, um, er, erm, ah |

### Fillers (Usually Remove)

| French | English |
|--------|---------|
| tu vois, genre, quoi, voilà | you know, like, right |
| en fait, du coup, bon, bref | actually, so, well |

---

## Markers to PRESERVE

**Critical**: Keep all rupture markers during cleaning.

```
KEEP: "aussi", "et puis", "autre chose", "ah et", "sinon",
      "autrement", "à part ça", "au fait", "tiens"
```

---

## Self-Corrections

| Pattern | Before | After |
|---------|--------|-------|
| Explicit | "CSV, non pardon, JSON" | "JSON" |
| Implicit | "le fichier CSV... enfin JSON" | "le fichier JSON" |

**Markers**: "non", "plutôt", "en fait", "je veux dire", "pardon"

---

## Normalization Rules

### Tense

| Input | Output |
|-------|--------|
| "faudrait que" | "doit" |
| "on voudrait" | "le système doit" |
| "ça serait bien si" | "le système doit" |

### Voice

| Input | Output |
|-------|--------|
| "je veux" | "le système doit" |
| "tu peux" | "le système peut" |
| "on fait" | "le système réalise" |

---

## Examples

### Simple Cleanup

**Input**:
> "euh donc euh faudrait fixer le truc de login là tu vois"

**Output**:
> "Corriger le bug de login."

### With Correction

**Input**:
> "on va faire un export CSV, non pardon en fait plutôt JSON"

**Output**:
> "Créer un export au format JSON."

### With Multi-Task Markers

**Input**:
> "fixer le login et puis aussi ajouter l'export PDF"

**Output** (preserving markers):
> "Fixer le login. Et puis ajouter l'export PDF."

---

## Technical Terms to Preserve

- API names, product names
- Acronyms (REST, CRUD, SSO, JWT)
- Domain vocabulary
- Stack names (Symfony, React, Django)

**Never** translate or "correct" technical jargon.

---

## Quality Checklist

After cleaning:
- [ ] No hesitation sounds
- [ ] No obvious filler words
- [ ] Complete sentences
- [ ] Proper punctuation
- [ ] Technical terms preserved exactly
- [ ] Rupture markers preserved
