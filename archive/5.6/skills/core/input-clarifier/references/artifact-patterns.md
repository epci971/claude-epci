# Voice Artifact Patterns

Reference des patterns à détecter pour le calcul du score de clarté.

---

## 1. Hesitation Markers (Marqueurs d'hésitation)

**Pénalité : -0.1 chacun**

### Français
| Pattern | Variantes |
|---------|-----------|
| euh | euh, euhm, euuuh |
| hum | hum, hmm, hmmm |
| hein | hein |
| ben | ben, beh, bah |
| attends | attends, attend, attends voir |

### Anglais (si input EN)
| Pattern | Variantes |
|---------|-----------|
| uh | uh, uhm, um |
| er | er, err |
| like | like (filler, not comparison) |

---

## 2. Filler Words (Mots de remplissage)

**Pénalité : -0.05 chacun**

### Français
| Pattern | Contexte |
|---------|----------|
| genre | "genre il marche pas" |
| tu vois | "tu vois ce que je veux dire" |
| tu sais | "tu sais le truc" |
| quoi | en fin de phrase "le bouton quoi" |
| en fait | "en fait c'est plutôt..." |
| du coup | "du coup ça marche pas" |
| voilà | "voilà c'est ça" |
| bon | "bon alors..." |
| donc | en début de phrase "donc euh" |
| alors | "alors le problème..." |
| un peu | "c'est un peu cassé" (vague) |
| vraiment | "vraiment bizarre" (emphase vide) |
| carrément | "carrément planté" |

### Mots vagues
| Pattern | Alternative suggérée |
|---------|---------------------|
| truc | [élément spécifique] |
| machin | [élément spécifique] |
| bidule | [élément spécifique] |
| chose | [élément spécifique] |
| là | [préciser localisation] |
| ça | [préciser référent] |

---

## 3. Self-Corrections (Auto-corrections)

**Pénalité : -0.1 chacun**

### Patterns de correction
| Pattern | Signification |
|---------|---------------|
| non | annule ce qui précède |
| pardon | correction à venir |
| enfin | reformulation |
| plutôt | alternative préférée |
| je veux dire | clarification |
| c'est-à-dire | précision |
| ou plutôt | correction |
| enfin non | annulation forte |
| enfin si | double correction |
| nan | annulation (oral) |
| non en fait | correction avec contexte |

### Règle de résolution
```
"X, enfin Y" → garder Y
"X, non Y" → garder Y  
"X, plutôt Y" → garder Y
"X, enfin non, Y" → garder Y
```

---

## 4. Incomplete Sentence Indicators

**Pénalité : -0.15**

### Patterns
| Indicateur | Exemple |
|------------|---------|
| Trailing `...` | "le bouton il..." |
| No main verb | "le formulaire là" |
| < 3 words after cleanup | "bouton cassé" |
| Sentence fragment | "quand je clique" (incomplet) |

### Détection
```python
def is_incomplete(sentence: str) -> bool:
    # After artifact removal
    cleaned = remove_artifacts(sentence)
    words = cleaned.split()
    
    # Too short
    if len(words) < 3:
        return True
    
    # Trailing ellipsis
    if cleaned.rstrip().endswith('...'):
        return True
    
    # No verb detected (simplified)
    verbs = ['est', 'sont', 'fait', 'marche', 'fonctionne', 'affiche', 'retourne']
    if not any(v in cleaned.lower() for v in verbs):
        return True
    
    return False
```

---

## 5. Contradiction Patterns

**Pénalité : -0.15**

### Patterns
| Pattern | Résolution |
|---------|------------|
| "X mais non Y" | garder Y |
| "X, enfin non" | ignorer X |
| "pas X, Y" | garder Y |
| "X ou Y, enfin Y" | garder dernier Y |

### Exemples
```
"le bouton, enfin non le formulaire" 
→ "le formulaire"

"ça marche, mais non en fait ça marche pas"
→ "ça ne marche pas"

"clique là, non pardon là-bas"
→ "clique là-bas"
```

---

## 6. Repetitions

**Pénalité : -0.1**

### Détection
Même phrase ou segment répété 2+ fois :

```
"le bouton le bouton ne marche pas"
→ "le bouton ne marche pas"

"il faut que, il faut que ça fonctionne"
→ "il faut que ça fonctionne"
```

---

## 7. Technical Content (Exclusions)

**Ne PAS pénaliser :**

### Patterns techniques à préserver
| Type | Exemples |
|------|----------|
| Error types | TypeError, ValueError, NullPointerException |
| Stack traces | "at line 42", "in function X" |
| Code snippets | `function()`, `variable_name` |
| File paths | `/src/components/Button.tsx` |
| HTTP codes | 404, 500, 503 |
| Technical terms | API, endpoint, callback, promise |

### Règle
```
IF input contains technical_pattern:
   Extract technical part
   Score only non-technical portions
   Preserve technical content in reformulation
```

---

## 8. Score Calculation Summary

```python
def calculate_clarity_score(input: str) -> float:
    score = 1.0
    
    # Count artifacts
    hesitations = count_patterns(input, HESITATION_MARKERS)
    fillers = count_patterns(input, FILLER_WORDS)
    corrections = count_patterns(input, SELF_CORRECTIONS)
    
    # Apply penalties
    score -= hesitations * 0.10
    score -= fillers * 0.05
    score -= corrections * 0.10
    
    # Structural penalties
    if is_incomplete(input):
        score -= 0.15
    if has_contradiction(input):
        score -= 0.15
    if has_repetition(input):
        score -= 0.10
    
    return max(0.0, score)
```

---

## 9. Quick Reference

| Category | Penalty | Examples |
|----------|---------|----------|
| Hesitations | -0.1 | euh, hum, ben |
| Fillers | -0.05 | genre, quoi, du coup, truc |
| Corrections | -0.1 | non, enfin, plutôt |
| Incomplete | -0.15 | trailing..., no verb |
| Contradiction | -0.15 | X enfin non Y |
| Repetition | -0.1 | X X Y |

**Threshold : 0.6**
- Score >= 0.6 → PASS
- Score < 0.6 → CLARIFY
