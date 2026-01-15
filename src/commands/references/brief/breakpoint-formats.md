# Formats des Breakpoints

> Templates ASCII box pour les breakpoints de /brief

---

## Breakpoint Step 1: Validation du Brief

```
┌─────────────────────────────────────────────────────────────────────┐
│ 📝 VALIDATION DU BRIEF                                              │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│ 📄 BRIEF ORIGINAL                                                   │
│ "{raw_brief}"                                                       │
│                                                                     │
│ [Si reformulé:]                                                     │
│ 📊 DÉTECTION                                                        │
│ ├── Artefacts vocaux: {COUNT} trouvés                              │
│ ├── Type détecté: {FEATURE|PROBLEM|DECISION}                       │
│ └── Reformulation: OUI                                             │
│                                                                     │
│ ✨ BRIEF REFORMULÉ                                                  │
│ ┌─────────────────────────────────────────────────────────────────┐ │
│ │ **Objectif**: {goal}                                            │ │
│ │ **Contexte**: {context}                                         │ │
│ │ **Contraintes**: {constraints}                                  │ │
│ │ **Critères de succès**: {success_criteria}                      │ │
│ └─────────────────────────────────────────────────────────────────┘ │
│                                                                     │
│ [Si NON reformulé:]                                                 │
│ ✅ Brief propre — pas de reformulation nécessaire                   │
│                                                                     │
├─────────────────────────────────────────────────────────────────────┤
│ OPTIONS:                                                            │
│   [1] Valider → Continuer vers l'exploration                       │
│   [2] Modifier → Je reformule moi-même                             │
│   [3] Annuler → Arrêter le workflow                                │
└─────────────────────────────────────────────────────────────────────┘
```

### Actions utilisateur Step 1

| Choix | Action |
|-------|--------|
| **[1] Valider** | Stocker brief validé, procéder au Step 2 |
| **[2] Modifier** | Attendre input utilisateur, mettre à jour brief, réafficher breakpoint |
| **[3] Annuler** | Arrêter workflow |

---

## Breakpoint Step 4: Analyse du Brief

```
┌─────────────────────────────────────────────────────────────────────┐
│ ⏸️  BREAKPOINT — ANALYSE DU BRIEF                                   │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│ 📊 EXPLORATION                                                      │
│ ├── Stack détecté: {STACK}                                         │
│ ├── Fichiers impactés: {FILE_COUNT}                                │
│ ├── Patterns identifiés: {PATTERNS}                                │
│ └── Risques détectés: {RISK_COUNT}                                 │
│                                                                     │
│ 📋 QUESTIONS DE CLARIFICATION                                       │
│                                                                     │
│ Q1: {TAG_1} {question_1}                                            │
│     → Suggestion: {suggestion_1}                                    │
│                                                                     │
│ Q2: {TAG_2} {question_2}                                            │
│     → Suggestion: {suggestion_2}                                    │
│                                                                     │
│ Q3: {TAG_3} {question_3}                                            │
│     → Suggestion: {suggestion_3}                                    │
│                                                                     │
│ Légende: 🛑 Critique (obligatoire) | ⚠️ Important | ℹ️ Optionnel    │
│                                                                     │
│ 💡 SUGGESTIONS IA                                                   │
│                                                                     │
│ Architecture:                                                       │
│   • {architecture_suggestion}                                       │
│                                                                     │
│ Implémentation:                                                     │
│   • {implementation_suggestion}                                     │
│                                                                     │
│ Risques à considérer:                                               │
│   • {risk_suggestion}                                               │
│                                                                     │
│ Best practices {stack}:                                             │
│   • {stack_suggestion}                                              │
│                                                                     │
│ 📈 ÉVALUATION                                                       │
│ ├── Catégorie: {CATEGORY}                                          │
│ ├── Fichiers: {FILE_COUNT}                                         │
│ ├── LOC estimé: ~{LOC}                                             │
│ ├── Risque: {RISK_LEVEL}                                           │
│ └── Flags: {FLAGS}                                                 │
│                                                                     │
│ 🚀 COMMANDE RECOMMANDÉE: {COMMAND} {FLAGS}                         │
│                                                                     │
│ [Si STANDARD ou LARGE:]                                             │
│ 💡 TIP: Worktree recommandé                                         │
│    Pour isoler cette feature dans un worktree:                      │
│      ./src/scripts/worktree-create.sh {slug}                        │
│      cd ~/worktrees/{project}/{slug}                                │
│      claude                                                         │
│                                                                     │
├─────────────────────────────────────────────────────────────────────┤
│ OPTIONS:                                                            │
│                                                                     │
│   [1] Répondre aux questions                                        │
│       → Je fournis mes réponses aux questions de clarification     │
│                                                                     │
│   [2] Valider les suggestions                                       │
│       → J'accepte les suggestions IA telles quelles                │
│                                                                     │
│   [3] Modifier les suggestions                                      │
│       → Je veux changer certaines suggestions                      │
│                                                                     │
│   [4] Lancer {COMMAND} {FLAGS}                                      │
│       → Tout est OK, on passe à l'implémentation                   │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### Actions utilisateur Step 4

| Choix | Action |
|-------|--------|
| **[1] Répondre** | Attendre réponses utilisateur, incorporer dans brief, réafficher breakpoint |
| **[2] Valider** | Utiliser suggestions telles quelles, générer output (Step 5), réafficher breakpoint avec éval mise à jour |
| **[3] Modifier** | Attendre modifications, mettre à jour suggestions, réafficher breakpoint |
| **[4] Lancer** | Générer output (Step 5) puis exécuter commande recommandée |

**Après [1], [2], ou [3]**: Mettre à jour analyse et réafficher breakpoint jusqu'à choix [4].
**Après [4]**: Procéder au Step 5 (générer output) puis Step 6 (exécuter commande).
