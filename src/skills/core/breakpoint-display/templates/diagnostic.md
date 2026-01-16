# Template: Diagnostic Breakpoint

## Overview

Breakpoint pour afficher diagnostic avec root cause et solutions ranked.

**Usage:** `/debug` Step C.2

## Data Structure

```typescript
{
  type: "diagnostic",
  title: "DIAGNOSTIC COMPLETE",
  data: {
    bug_description: "{TEXT}",
    root_cause: {
      category: "{CATEGORY}",
      explanation: "{TEXT}",
      affected_files: ["{file1}", "{file2}", ...]
    },
    solutions: [
      {
        rank: 1,
        title: "{TITLE}",
        description: "{TEXT}",
        effort: "{EFFORT}",
        risk: "{RISK}",
        recommended: true
      },
      ...
    ],
    additional_info: "{TEXT}" || null
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

## Example

```typescript
{
  type: "diagnostic",
  title: "DIAGNOSTIC COMPLETE",
  data: {
    bug_description: "Users can't login after OAuth migration",
    root_cause: {
      category: "Configuration Error",
      explanation: "OAuth callback URL mismatch in security.yaml",
      affected_files: ["config/packages/security.yaml", "src/Security/OAuthAuthenticator.php"]
    },
    solutions: [
      {
        rank: 1,
        title: "Fix callback URL in config",
        description: "Update security.yaml with correct callback route",
        effort: "5min",
        risk: "LOW",
        recommended: true
      },
      {
        rank: 2,
        title: "Revert to password auth",
        description: "Temporary rollback to investigate",
        effort: "2min",
        risk: "LOW",
        recommended: false
      }
    ],
    additional_info: "Check OAuth provider console for registered callbacks"
  },
  ask: {
    question: "Quelle solution souhaitez-vous appliquer ?",
    header: "💡 Solution",
    options: [
      {label: "Solution 1 (Recommended)", description: "Fix callback URL in config"},
      {label: "Solution 2", description: "Revert to password auth"},
      {label: "Voir détails", description: "Afficher plus d'informations"},
      {label: "Annuler", description: "Investiguer manuellement"}
    ]
  }
}
```

## Token Savings

**Avant:** ~280 tokens
**Après:** ~75 tokens
**Gain:** 73%
