# Mode --turbo

> Instructions obligatoires pour le mode turbo de /brief

---

## Règles du Mode Turbo

Quand le flag `--turbo` est actif, suivre ces règles:

### 1. Utiliser @clarifier (Haiku)

```
Invoquer @clarifier via Task tool avec model: haiku
Maximum 2 questions, suggestions incluses
Ignorer l'analyse profonde, focus sur ambiguïtés bloquantes
```

### 2. Utiliser @Explore avec Haiku

```
Invoquer @Explore via Task tool avec model: haiku
Focus: Scan rapide, identification fichiers uniquement
Ignorer: Analyse patterns approfondie (reporter à l'implémentation)
```

### 3. Maximum 2 Questions de Clarification

Focus uniquement sur les ambiguïtés bloquantes.

### 4. Auto-accepter les Suggestions (confiance > 0.7)

- Si les suggestions IA ont haute confiance, ignorer l'option [1]
- Présenter uniquement [2] Valider, [3] Modifier, [4] Lancer

### 5. Suggestion Automatique --turbo

Suggérer --turbo automatiquement si:
- `.project-memory/` existe (projet connu)
- Provient de `/brainstorm` avec EMS > 60
- Catégorie est STANDARD (pas LARGE)

### 6. Breakpoints Réduits

Format compact, étape de confirmation unique.

---

## Logique de Suggestion Turbo

```
IF .project-memory/ exists AND category != LARGE:
   Display: "💡 --turbo recommandé (projet connu)"
   Auto-add --turbo to recommended command
```

---

## Comportement Step 1 en Mode Turbo

- Auto-valider si brief propre (pas d'artefacts détectés)
- Affichage format compact
- Afficher breakpoint uniquement si > 3 artefacts vocaux détectés
