# Transcription Patterns Reference

> Common artifacts to identify and clean in audio transcriptions

---

## Filler Words (French)

### High-frequency fillers (always remove)
```
euh, heu, euhm, hum, hmm
ben, bah, beh
donc euh, et euh, mais euh
voilà, voilà voilà
en fait, en fait euh
du coup, du coup euh
genre, genre euh
quoi, enfin quoi
tu vois, vous voyez
```

### Context-dependent fillers (remove when meaningless)
```
bon (when not expressing judgment)
alors (when not indicating sequence)
donc (when not expressing consequence)
enfin (when not correcting)
```

---

## Filler Words (English)

### High-frequency fillers (always remove)
```
uh, um, uhm, er, erm
like, you know, I mean
so uh, and uh, but uh
basically, actually (when overused)
right, okay, yeah (when not answering)
kind of, sort of (when vague)
```

---

## False Starts & Repetitions

### Pattern: Word repetition
```
Input:  "Je je je voulais vous dire"
Output: "Je voulais vous dire"
```

### Pattern: Phrase restart
```
Input:  "On pourrait peut-être... enfin on devrait plutôt faire..."
Output: "On devrait plutôt faire..."
```

### Pattern: Self-correction
```
Input:  "Le projet sera livré lundi, non en fait mardi"
Output: "Le projet sera livré mardi"
```

### Pattern: Thought reformulation
```
Input:  "C'est important de... comment dire... c'est essentiel de bien tester"
Output: "C'est essentiel de bien tester"
```

---

## Verbal Tics

### Discourse markers to clean
```
"comment dire"
"je veux dire"
"si vous voulez"
"disons que"
"on va dire"
"quelque part"
```

### Hedging expressions (simplify or remove)
```
"un petit peu" → (remove or keep depending on context)
"plus ou moins" → (remove if vague)
"en quelque sorte" → (remove)
"d'une certaine manière" → (remove)
```

---

## Transcription Errors

### Common speech-to-text mistakes (French)
| Heard as | Likely meant |
|----------|--------------|
| "ces" / "ses" / "c'est" / "s'est" | Context-dependent |
| "a" / "à" | Context-dependent |
| "ou" / "où" | Context-dependent |
| "voir" / "voire" | Context-dependent |
| "censé" / "sensé" | Usually "censé" |

### Homophones to verify
```
"ça" vs "sa"
"ce" vs "se"
"leur" vs "leurs"
"quand" vs "quant" vs "qu'en"
"quelque" vs "quel que"
```

---

## Cleaning Priority

### Level 1: Always clean (automatic)
- Filler words with no semantic value
- Pure repetitions
- Incomplete false starts

### Level 2: Clean with judgment
- Self-corrections (keep final version)
- Hedging (simplify)
- Discourse markers (remove if cluttering)

### Level 3: Preserve
- Intentional emphasis through repetition
- Meaningful hesitation (expressing uncertainty on purpose)
- Quoted speech patterns

---

## Examples

### Raw transcription
```
"Donc euh je voulais je voulais vous faire un petit retour sur la réunion 
d'hier. En fait euh on a parlé du projet, du projet Symfony là, et euh 
voilà le client il est plutôt content, enfin il est content quoi. 
Du coup on va pouvoir avancer sur la phase 2 je pense."
```

### Cleaned version
```
"Je voulais vous faire un retour sur la réunion d'hier. On a parlé du 
projet Symfony et le client est content. On va pouvoir avancer sur 
la phase 2."
```

### Preserved meaning
- Meeting feedback intent ✓
- Symfony project reference ✓
- Client satisfaction ✓
- Phase 2 progression ✓
