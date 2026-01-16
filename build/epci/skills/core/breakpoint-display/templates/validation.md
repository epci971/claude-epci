# Template: Validation Breakpoint

## Overview

Simple validation avec 2-4 choix (Valider/Modifier/Annuler).

**Usage:** `/brief` Step 1, `/commit` pre-commit, `/save-plan` confirmation

## Data Structure

```typescript
{
  type: "validation",
  title: "{TITLE}",
  data: {
    // Context-specific data
    original: "{original_content}",
    modified: {true|false},
    modified_content: {
      // Modified version if applicable
    },
    detection_info: {
      // Optional detection metadata
    }
  },
  ask: {
    question: "{QUESTION}",
    header: "{HEADER}",  // Max 12 chars
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
│ {EMOJI} {TITLE}                                                     │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│ 📄 ORIGINAL                                                         │
│ {original_content}                                                  │
│                                                                     │
│ [If modified:]                                                      │
│ 📊 DÉTECTION                                                        │
│ {detection_info}                                                    │
│                                                                     │
│ ✨ MODIFIED                                                         │
│ {modified_content}                                                  │
│                                                                     │
│ [If NOT modified:]                                                  │
│ ✅ Pas de modification nécessaire                                   │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

Then invoke `AskUserQuestion` with options.

## Example: Brief Validation (/brief Step 1)

```typescript
{
  type: "validation",
  title: "VALIDATION DU BRIEF",
  data: {
    original: "ajouter auth google oauth truc machin euh voila",
    modified: true,
    detection_info: {
      artefacts_vocaux: 3,
      type_detected: "FEATURE"
    },
    modified_content: {
      objectif: "Implémenter authentification OAuth 2.0 avec Google",
      contexte: "Application Symfony existante avec users en base",
      contraintes: "Compatibilité users existants, migration progressive",
      success_criteria: "Login Google fonctionnel + tests E2E"
    }
  },
  ask: {
    question: "Le brief vous convient-il ?",
    header: "📝 Validation",
    options: [
      {label: "Valider (Recommended)", description: "Continuer vers exploration"},
      {label: "Modifier", description: "Je reformule moi-même"},
      {label: "Annuler", description: "Arrêter workflow"}
    ]
  }
}
```

## Example: Commit Validation (/commit)

```typescript
{
  type: "validation",
  title: "VALIDATION COMMIT",
  data: {
    original: "git status output...",
    modified: false,
    commit_info: {
      files_changed: 8,
      insertions: 234,
      deletions: 12,
      message: "feat(auth): implement OAuth Google integration\n\nAdd OAuth provider, user mapping, tests"
    }
  },
  ask: {
    question: "Valider ce commit ?",
    header: "🔧 Commit",
    options: [
      {label: "Commiter (Recommended)", description: "Créer commit avec ce message"},
      {label: "Modifier message", description: "Changer message commit"},
      {label: "Annuler", description: "Ne pas commiter"}
    ]
  }
}
```

## Token Savings

**Avant:** ~250 tokens (ASCII box + options textuelles)
**Après:** ~70 tokens (skill invocation)
**Gain:** 72%
