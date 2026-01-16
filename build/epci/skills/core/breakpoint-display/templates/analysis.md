# Template: Analysis Breakpoint

## Overview

Breakpoint pour afficher analyse complète avec questions clarification, suggestions IA, et évaluation.

**Usage:** `/brief` Step 4

## Data Structure

```typescript
{
  type: "analysis",
  title: "ANALYSE DU BRIEF",
  data: {
    exploration: {
      stack: "{STACK}",
      files_impacted: {number},
      patterns: ["{pattern1}", "{pattern2}", ...],
      risks: ["{risk1}", "{risk2}", ...]
    },
    questions: [
      {
        tag: "{🛑|⚠️|ℹ️}",
        text: "{QUESTION}",
        suggestion: "{SUGGESTION}"
      },
      ...
    ],
    suggestions: {
      architecture: "{TEXT}",
      implementation: "{TEXT}",
      risks: "{TEXT}",
      stack_specific: "{TEXT}"
    },
    evaluation: {
      category: "{TINY|SMALL|STANDARD|LARGE}",
      files: {number},
      loc_estimate: {number},
      risk: "{LOW|MEDIUM|HIGH}",
      flags: ["{flag1}", "{flag2}", ...]
    },
    recommended_command: "{COMMAND}",
    worktree_tip: {true|false}  // Show worktree tip for STANDARD/LARGE
  },
  ask: {
    question: "{QUESTION}",
    header: "{HEADER}",
    options: [
      {label: "{LABEL}", description: "{DESCRIPTION}"},
      ...
    ]
  }
}
```

## Display Format

```
┌─────────────────────────────────────────────────────────────────────┐
│ ⏸️  ANALYSE DU BRIEF                                                │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│ 📊 EXPLORATION                                                      │
│ ├── Stack détecté: {stack}                                         │
│ ├── Fichiers impactés: {files}                                     │
│ ├── Patterns identifiés: {patterns}                                │
│ └── Risques détectés: {risks}                                      │
│                                                                     │
│ 📋 QUESTIONS DE CLARIFICATION                                       │
│                                                                     │
│ Q1: {tag} {question}                                                │
│     → Suggestion: {suggestion}                                      │
│                                                                     │
│ Q2: {tag} {question}                                                │
│     → Suggestion: {suggestion}                                      │
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
│ ├── Catégorie: {category}                                          │
│ ├── Fichiers: {files}                                              │
│ ├── LOC estimé: ~{loc}                                             │
│ ├── Risque: {risk}                                                 │
│ └── Flags: {flags}                                                 │
│                                                                     │
│ 🚀 COMMANDE RECOMMANDÉE: {command}                                 │
│                                                                     │
│ [If worktree_tip:]                                                  │
│ 💡 TIP: Worktree recommandé                                         │
│    Pour isoler cette feature dans un worktree:                      │
│      ./src/scripts/worktree-create.sh {slug}                        │
│      cd ~/worktrees/{project}/{slug}                                │
│      claude                                                         │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

Then invoke `AskUserQuestion` with options.

## Example: /brief Step 4

```typescript
{
  type: "analysis",
  title: "ANALYSE DU BRIEF",
  data: {
    exploration: {
      stack: "Symfony 6.3 + PostgreSQL + React",
      files_impacted: 8,
      patterns: ["Repository", "Service", "Controller", "React Components"],
      risks: ["Migration données users", "Breaking changes API existante"]
    },
    questions: [
      {
        tag: "🛑",
        text: "Quel provider OAuth utiliser ? (Google/GitHub/Custom)",
        suggestion: "Google OAuth 2.0 (standard + bien documenté)"
      },
      {
        tag: "⚠️",
        text: "Migrer les users existants ou créer nouveaux comptes ?",
        suggestion: "Migration progressive avec fallback password classique"
      },
      {
        tag: "ℹ️",
        text: "UI personnalisée pour le login ou redirect OAuth standard ?",
        suggestion: "Utiliser redirects OAuth standards (maintenance simple)"
      }
    ],
    suggestions: {
      architecture: "Utiliser FOSUserBundle + HWIOAuthBundle (standard Symfony)",
      implementation: "Créer UserProvider custom pour mapper OAuth claims → User entity",
      risks: "Tester rollback en cas d'échec OAuth + logs détaillés",
      stack_specific: "Configurer security.yaml avec firewall OAuth + garder firewall classique"
    },
    evaluation: {
      category: "STANDARD",
      files: 8,
      loc_estimate: 450,
      risk: "MEDIUM",
      flags: ["--think", "--uc"]
    },
    recommended_command: "/epci auth-oauth --think --uc",
    worktree_tip: true
  },
  ask: {
    question: "Comment souhaitez-vous procéder avec cette analyse ?",
    header: "🚀 Action",
    options: [
      {label: "Répondre questions", description: "Je fournis réponses clarification"},
      {label: "Valider suggestions (Recommended)", description: "J'accepte suggestions IA telles quelles"},
      {label: "Modifier suggestions", description: "Je veux changer certaines suggestions"},
      {label: "Lancer /epci", description: "Tout OK, passer implémentation"}
    ]
  }
}
```

## Response Handling

| Choix | Action |
|-------|--------|
| **Répondre questions** | Attendre réponses utilisateur, incorporer dans brief, réafficher breakpoint |
| **Valider suggestions** | Utiliser suggestions telles quelles, générer output (Step 5), réafficher avec éval mise à jour |
| **Modifier suggestions** | Attendre modifications, mettre à jour, réafficher breakpoint |
| **Lancer /epci** | Générer output (Step 5) puis exécuter commande recommandée |

**Note:** Après [1], [2], ou [3], mettre à jour analyse et réafficher breakpoint jusqu'à choix [4].

## Token Savings

**Avant:** ~450 tokens (ASCII box + questions + suggestions + eval)
**Après:** ~120 tokens (skill invocation)
**Gain:** 73%
