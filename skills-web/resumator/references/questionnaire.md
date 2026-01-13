# Questionnaire de configuration

## Présentation standard

Après réception des sources, TOUJOURS afficher :

```
📊 Resumator v3 — Configuration

1️⃣ Type de traitement ?
   a. 📋 Réunion — Compte-rendu structuré
   b. 🔬 Étude — Recherche approfondie  
   c. 📰 Veille — Synthèse d'actualités
   d. 📖 Formation — Extraction pédagogique
   e. ⚖️ Comparatif — Analyse comparative
   f. 🔧 Technique — Documentation tech
   g. 📊 Audit — Analyse critique

2️⃣ Niveau de détail ? (1-5)
   1. ⚡ Flash — TL;DR en 5 lignes
   2. 📋 Résumé — Points clés (~500-800 mots)
   3. 📊 Détaillé — Analyse complète (~1500-2500 mots)
   4. 📚 Approfondi — + contexte (~3000-5000 mots)
   5. 🔬 Exhaustif — Recherche maximale (5000+ mots)

💡 Raccourci : tape "a3" pour Réunion/Détaillé ou "b5" pour Étude/Exhaustive
```

## Raccourcis acceptés

### Format combiné (recommandé)
| Input | Interprétation |
|-------|----------------|
| `a3` | Réunion + Détaillé |
| `b5` | Étude + Exhaustif |
| `c4` | Veille + Approfondi |
| `d2` | Formation + Résumé |
| `e3` | Comparatif + Détaillé |
| `f5` | Technique + Exhaustif |
| `g4` | Audit + Approfondi |

### Format textuel
| Input | Interprétation |
|-------|----------------|
| "réunion détaillé" | a3 |
| "étude exhaustive" | b5 |
| "veille approfondie" | c4 |
| "comparatif" | e3 (défaut niveau 3) |
| "audit complet" | g5 |

### Niveau seul (si type évident)
| Input | Condition | Interprétation |
|-------|-----------|----------------|
| `3` | Transcript avec noms | Réunion niveau 3 |
| `5` | Multiple URLs | Étude niveau 5 |

## Valeurs par défaut

Si l'utilisateur ne précise pas :
- **Type par défaut** : Réunion (a) si transcript avec participants, sinon demander
- **Niveau par défaut** : 3 (Détaillé)

## Cas particuliers

### Demande explicite sans questionnaire
Si l'utilisateur dit clairement ce qu'il veut :
- "Fais-moi un CR de cette réunion" → a3 direct
- "Étude exhaustive sur X" → b5 direct
- "Compare A et B en détail" → e3 direct

### Reformulation si incompris
```
Je n'ai pas compris ta sélection. 
Peux-tu préciser avec un raccourci (ex: "b5") ou en toutes lettres ?
```

## Matrice Type × Niveau

| Type | Niv 1 | Niv 2 | Niv 3 | Niv 4 | Niv 5 |
|------|-------|-------|-------|-------|-------|
| 📋 Réunion | TL;DR | CR minimal | CR standard | CR + contexte | CR exhaustif |
| 🔬 Étude | Synthèse | Résumé | Analyse | Recherche | Recherche max |
| 📰 Veille | Headlines | Brief | Synthèse | Analyse | Dossier complet |
| 📖 Formation | Concepts | Guide rapide | Guide | Parcours | Parcours complet |
| ⚖️ Comparatif | Tableau | Résumé F/W | Analyse | Matrice | Dossier décision |
| 🔧 Technique | Quick ref | Résumé | Doc standard | Doc complète | Spec exhaustive |
| 📊 Audit | Score | Points clés | Analyse | Audit complet | Audit + plan |
