# Component: Flags Block

## Overview

Composant réutilisable pour afficher flags actifs avec sources (auto/user).

**Usage:** `plan-review`

## Input Structure

```typescript
{
  active: ["{flag1}", "{flag2}", ...],
  sources: {
    "{flag1}": "{SOURCE}",
    "{flag2}": "{SOURCE}",
    ...
  }
}
```

## Display Format

```
│ FLAGS: {flag1} ({source1}) | {flag2} ({source2}) | ...             │
```

## Example

```typescript
Input:
{
  active: ["--think", "--uc"],
  sources: {
    "--think": "auto: 12 files",
    "--uc": "auto: context 78%"
  }
}

Output:
│ FLAGS: --think (auto: 12 files) | --uc (auto: context 78%)         │
```

## Example: User-provided Flags

```typescript
Input:
{
  active: ["--think-hard", "--safe", "--verbose"],
  sources: {
    "--think-hard": "user",
    "--safe": "auto: auth files detected",
    "--verbose": "user"
  }
}

Output:
│ FLAGS: --think-hard (user) | --safe (auto: auth files) | --verbose (user) │
```

## Position in Breakpoint

This block appears at the very top, right after the title:

```
┌─────────────────────────────────────────────────────────────────────┐
│ ⏸️  BREAKPOINT PHASE 1 — Plan Validé                                │
├─────────────────────────────────────────────────────────────────────┤
│ FLAGS: --think (auto: 12 files) | --uc (auto: context 78%)         │
├─────────────────────────────────────────────────────────────────────┤
│ [Rest of breakpoint content...]                                     │
```

## Conditional Display

Only display if there are active flags. If no flags, omit this block entirely.
