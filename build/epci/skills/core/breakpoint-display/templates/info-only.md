# Template: Info-Only Breakpoint

## Overview

Affichage d'informations sans interaction utilisateur (pas de AskUserQuestion).

**Usage:** `/ralph-exec` story blocked notification

## Data Structure

```typescript
{
  type: "info-only",
  title: "{TITLE}",
  data: {
    message: "{TEXT}",
    details: {
      // Context-specific details
    }
  }
  // No 'ask' field - display only
}
```

## Display Format

```
┌─────────────────────────────────────────────────────────────────────┐
│ {EMOJI} {TITLE}                                                     │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│ {message}                                                           │
│                                                                     │
│ [Details section if present]                                        │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

NO AskUserQuestion invoked - display only, execution continues.

## Example: Story Blocked (/ralph-exec)

```typescript
{
  type: "info-only",
  title: "STORY BLOCKED — US-04",
  data: {
    message: "Story bloquée - dépendance US-02 échouée",
    details: {
      story_id: "US-04",
      blocked_reason: "Dependency US-02 FAILED",
      dependency_error: "Tests failing in OAuth service",
      recommended_action: "Fix US-02 before retrying US-04"
    }
  }
}
```

## Token Savings

**Avant:** ~150 tokens
**Après:** ~60 tokens
**Gain:** 60%
