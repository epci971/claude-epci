---
name: breakpoint-display
description: >-
  Système unifié pour l'affichage de breakpoints interactifs avec validation
  utilisateur via AskUserQuestion. Centralise tous les formats de breakpoints
  EPCI pour cohérence, économie tokens (73% réduction), et maintenabilité.
  Use when: Afficher un breakpoint dans une commande (/brief, /epci, /decompose, etc.).
  Not for: Affichage simple sans interaction utilisateur (utiliser print direct).
applicable-to: ["ALL_COMMANDS_WITH_BREAKPOINTS"]
integration: ["AskUserQuestion", "breakpoint-metrics"]
---

# Breakpoint Display — Unified Interactive Breakpoints

## Overview

Skill centralisé pour afficher des breakpoints interactifs avec validation utilisateur native via `AskUserQuestion`. Remplace les choix textuels manuels par une UI native Claude Code.

**Bénéfices :**
- 📉 **73% réduction tokens** : ~300 tokens/breakpoint → ~80 tokens
- 🎨 **UX native** : Boutons cliquables vs input textuel
- 🔄 **Cohérence** : Format unifié pour 9 commandes
- 🛠️ **Maintenabilité** : 1 skill vs 9 implémentations
- ✨ **Évolutivité** : Nouveaux types facilement ajoutés

## Supported Breakpoint Types

| Type | Usage | AskUserQuestion | Template |
|------|-------|-----------------|----------|
| **validation** | Choix simple (Valider/Modifier/Annuler) | ✅ Oui | @templates/validation.md |
| **plan-review** | Métriques + validations agents + preview | ✅ Oui | @templates/plan-review.md |
| **analysis** | Questions + suggestions + évaluation | ✅ Oui | @templates/analysis.md |
| **decomposition** | Table specs + menu modifications | ✅ Oui (2-level) | @templates/decomposition.md |
| **diagnostic** | Root cause + solutions ranked | ✅ Oui | @templates/diagnostic.md |
| **interactive-plan** | DAG + reorder + skip options | ✅ Oui | @templates/interactive-plan.md |
| **lightweight** | Auto-continue avec timeout 3s | ⚠️ Optionnel | @templates/lightweight.md |
| **info-only** | Display metrics sans interaction | ❌ Non | @templates/info-only.md |

## Usage Pattern

```typescript
// Pattern général dans une commande
@skill:breakpoint-display
  type: {TYPE}
  title: "{TITLE}"
  data: {
    // Type-specific data structure
  }
  ask: {
    question: "{QUESTION}"
    header: "{HEADER}"  // Max 12 chars
    multiSelect: {true|false}
    options: [
      {label: "{LABEL}", description: "{DESCRIPTION}"},
      ...
    ]
  }
```

## Examples by Type

### Type: validation

Simple 2-4 choix (Valider/Modifier/Annuler).

```typescript
@skill:breakpoint-display
  type: validation
  title: "VALIDATION DU BRIEF"
  data: {
    original_brief: "{text}",
    reformulated: {true|false},
    reformulated_brief: {
      objectif: "...",
      contexte: "...",
      contraintes: "...",
      success_criteria: "..."
    }
  }
  ask: {
    question: "Le brief vous convient-il ?"
    header: "📝 Validation"
    options: [
      {label: "Valider (Recommended)", description: "Continuer vers exploration"},
      {label: "Modifier", description: "Je reformule moi-même"},
      {label: "Annuler", description: "Arrêter workflow"}
    ]
  }
```

### Type: plan-review

Métriques + validations agents + preview prochaine phase.

```typescript
@skill:breakpoint-display
  type: plan-review
  title: "PHASE 1 — Plan Validé"
  data: {
    metrics: {
      complexity: "STANDARD",
      complexity_score: 6.2,
      files_impacted: 12,
      time_estimate: "2-3h",
      risk_level: "MEDIUM",
      risk_description: "Auth changes require careful testing"
    },
    validations: {
      plan_validator: {
        verdict: "APPROVED",
        completeness: "OK",
        consistency: "OK",
        feasibility: "OK",
        quality: "OK"
      }
    },
    skills_loaded: ["testing-strategy", "php-symfony", "security-patterns"],
    preview_phase_2: {
      tasks: [
        {title: "Create User entity", time: "30min"},
        {title: "Implement auth service", time: "1h"},
        {title: "Add tests", time: "45min"}
      ],
      remaining_tasks: 5
    },
    feature_doc_path: "docs/features/auth-oauth.md"
  }
  ask: {
    question: "Comment souhaitez-vous procéder ?"
    header: "🚀 Phase 2"
    options: [
      {label: "Continuer (Recommended)", description: "Passer à Phase 2 Implémentation"},
      {label: "Modifier plan", description: "Réviser plan avant implémentation"},
      {label: "Voir détails", description: "Afficher Feature Document complet"},
      {label: "Annuler", description: "Abandonner workflow"}
    ]
  }
```

### Type: analysis

Questions clarification + suggestions + évaluation.

```typescript
@skill:breakpoint-display
  type: analysis
  title: "ANALYSE DU BRIEF"
  data: {
    exploration: {
      stack: "Symfony 6.3 + PostgreSQL",
      files_impacted: 8,
      patterns: ["Repository", "Service", "Controller"],
      risks: ["Migration données", "Breaking changes API"]
    },
    questions: [
      {tag: "🛑", text: "Quel provider OAuth ? (Google/GitHub/Custom)", suggestion: "Google OAuth 2.0"},
      {tag: "⚠️", text: "Migrer users existants ?", suggestion: "Migration progressive avec fallback"},
      {tag: "ℹ️", text: "UI personnalisée ?", suggestion: "Utiliser OAuth redirects standards"}
    ],
    suggestions: {
      architecture: "Utiliser FOSUserBundle + HWIOAuthBundle",
      implementation: "Créer UserProvider custom pour mapping OAuth",
      risks: "Tester rollback en cas d'échec OAuth",
      stack_specific: "Configurer security.yaml avec firewall OAuth"
    },
    evaluation: {
      category: "STANDARD",
      files: 8,
      loc_estimate: 450,
      risk: "MEDIUM",
      flags: ["--think", "--uc"]
    },
    recommended_command: "/epci --think --uc"
  }
  ask: {
    question: "Comment souhaitez-vous procéder avec cette analyse ?"
    header: "🚀 Action"
    options: [
      {label: "Répondre questions", description: "Je fournis réponses clarification"},
      {label: "Valider suggestions (Recommended)", description: "J'accepte suggestions IA telles quelles"},
      {label: "Modifier suggestions", description: "Je veux changer certaines suggestions"},
      {label: "Lancer /epci", description: "Tout OK, passer implémentation"}
    ]
  }
```

### Type: decomposition

Table specs + menu modifications multi-niveau.

```typescript
@skill:breakpoint-display
  type: decomposition
  title: "VALIDATION DÉCOUPAGE"
  data: {
    source_file: "prd-migration.md",
    analysis: {
      lines: 450,
      total_effort: 23,
      structure: "5 phases, 12 steps"
    },
    specs: [
      {id: "S01", title: "Auth Base", effort: 3, priority: "-", deps: "-", status: "Pending"},
      {id: "S02", title: "OAuth Integration", effort: 5, priority: "-", deps: "S01", status: "Pending"},
      {id: "S03", title: "User Migration", effort: 2, priority: "-", deps: "S01", status: "Pending"}
    ],
    parallelization: 2,
    optimized_duration: 15,
    sequential_duration: 23,
    alerts: ["S02 effort élevé - considérer split"],
    validator_verdict: "APPROVED with minor suggestions"
  }
  ask: {
    question: "Le découpage vous convient-il ?"
    header: "📋 Découpage"
    options: [
      {label: "Valider (Recommended)", description: "Générer fichiers sous-specs"},
      {label: "Modifier", description: "Ajuster découpage avant génération"},
      {label: "Annuler", description: "Abandonner décomposition"}
    ]
  }
```

**Si choix "Modifier", afficher sous-menu :**

```typescript
@skill:breakpoint-display (second-level)
  type: decomposition-modify
  title: "MODIFICATION DÉCOUPAGE"
  ask: {
    question: "Que souhaitez-vous modifier ?"
    header: "🔧 Modifier"
    multiSelect: true
    options: [
      {label: "Fusionner specs", description: "Ex: Fusionner S04 et S05"},
      {label: "Découper spec", description: "Ex: Découper S07 en 2 parties"},
      {label: "Renommer", description: "Ex: S03 → Modèles Fondamentaux"},
      {label: "Changer dépendances", description: "Ex: S06 ne dépend plus de S03"},
      {label: "Ajuster estimation", description: "Ex: S08 = 3 jours au lieu de 5"}
    ]
  }
```

## Reusable Components

Le skill utilise des composants réutilisables pour cohérence :

| Component | File | Usage |
|-----------|------|-------|
| **Metrics Block** | @components/metrics-block.md | Complexité, fichiers, temps, risque |
| **Validations Block** | @components/validations-block.md | Verdicts agents (@plan-validator, etc.) |
| **Preview Block** | @components/preview-block.md | Preview tâches prochaine phase |
| **Flags Block** | @components/flags-block.md | Flags actifs avec sources (auto/user) |

## AskUserQuestion Integration

### Headers (max 12 characters)

Pattern utilisé dans `/brainstorm` (référence) :

```typescript
"📝 Validation"  // 12 chars
"🚀 Action"      // 8 chars
"🚀 Phase 2"     // 10 chars
"📋 Découpage"   // 12 chars
"🔧 Modifier"    // 10 chars
"💡 Diagnostic"  // 13 chars → "💡 Solution" (11 chars)
"🔄 Transition"  // 12 chars
```

### Options with (Recommended)

```typescript
{
  label: "Valider (Recommended)",
  description: "Continuer vers exploration"
}
```

Convention : Le premier choix est `(Recommended)` si c'est le chemin par défaut.

### MultiSelect Mode

```typescript
multiSelect: true,
options: [
  {label: "Option 1", description: "..."},
  {label: "Option 2", description: "..."}
]
```

Utilisé pour sélections multiples simultanées (ex: techniques brainstorm, modifications décomposition).

## Display Logic

### Step 1: Render Data Section

Utiliser le composant approprié selon le type :

- **validation** : Brief original + reformulé (si applicable)
- **plan-review** : @components/metrics-block + @components/validations-block + @components/preview-block
- **analysis** : Exploration + Questions + Suggestions + Évaluation
- **decomposition** : Table specs + Parallelization + Alerts
- **diagnostic** : Root cause + Solutions ranked
- **interactive-plan** : DAG Mermaid + Specs table
- **lightweight** : Minimal info + "Auto-continue dans 3s..."
- **info-only** : Metrics seulement

### Step 2: Call AskUserQuestion

Si le type a `ask` défini (tous sauf `info-only` et `lightweight`), invoquer `AskUserQuestion` :

```typescript
AskUserQuestion({
  questions: [{
    question: data.ask.question,
    header: data.ask.header,
    multiSelect: data.ask.multiSelect || false,
    options: data.ask.options.map(opt => ({
      label: opt.label,
      description: opt.description
    }))
  }]
})
```

### Step 3: Handle Response

Retourner la réponse au workflow appelant pour traitement.

## Token Savings

| Type | Avant (ASCII box) | Après (skill) | Gain |
|------|-------------------|---------------|------|
| validation | ~250 tokens | ~70 tokens | 72% |
| plan-review | ~350 tokens | ~90 tokens | 74% |
| analysis | ~450 tokens | ~120 tokens | 73% |
| decomposition | ~300 tokens | ~85 tokens | 72% |
| diagnostic | ~280 tokens | ~75 tokens | 73% |
| interactive-plan | ~320 tokens | ~95 tokens | 70% |
| lightweight | ~100 tokens | ~40 tokens | 60% |
| info-only | ~150 tokens | ~60 tokens | 60% |

**Moyenne : 73% réduction tokens**

## Migration Guide

Voir @references/migration-guide.md pour guide détaillé commande par commande.

**Ordre recommandé :**
1. `/brief` (2 breakpoints : validation + analysis)
2. `/epci` (2 breakpoints : plan-review × 2)
3. `/decompose` (1 breakpoint : decomposition)
4. `/commit` (1 breakpoint : validation)
5. `/debug` (1 breakpoint : diagnostic)
6. `/orchestrate` (1 breakpoint : interactive-plan)
7. `/save-plan` (1 breakpoint : validation)
8. `/quick` (1 breakpoint : lightweight)
9. `/ralph-exec` (1 breakpoint : info-only)

## Error Handling

| Erreur | Action |
|--------|--------|
| Type inconnu | Afficher erreur + liste types supportés |
| Données manquantes | Afficher warning + utiliser defaults |
| AskUserQuestion échoue | Fallback vers input textuel legacy |
| Header > 12 chars | Tronquer avec warning |

## Technical Notes

- **Encoding:** UTF-8 pour emojis et caractères spéciaux
- **Line width:** Max 73 chars pour ASCII boxes (compatibilité terminal)
- **Emojis:** Utiliser codes unicode standards
- **Versioning:** v1.0.0 (aligns with EPCI v5.3.3)

## References

- AskUserQuestion Guide: @references/askuserquestion-guide.md
- Migration Guide: @references/migration-guide.md
- Brainstorm Implementation: @src/commands/brainstorm.md (reference model)
- Component Templates: @components/
- Type Templates: @templates/

## Examples in Production

After migration, commands will use:

```bash
# /brief Step 4
@skill:breakpoint-display type:analysis ...

# /epci Phase 1
@skill:breakpoint-display type:plan-review title:"PHASE 1 — Plan Validé" ...

# /decompose
@skill:breakpoint-display type:decomposition ...
```

**See individual command files for full usage examples after migration.**
