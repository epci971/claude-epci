---
description: >-
  Cancel a running Ralph loop. Removes the state file and stops
  autonomous execution gracefully. Use when you need to interrupt
  an overnight session or take manual control.
argument-hint: "[--force]"
allowed-tools: [Read, Write, Bash]
---

# EPCI Cancel Ralph

## Overview

Cancels an active Ralph Wiggum loop by removing the state file and
updating the session status. This provides a clean way to interrupt
autonomous execution without using Ctrl+C.

**Use case**: Stop an overnight session to review progress, fix an issue,
or take manual control of implementation.

## Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `--force` | Skip confirmation prompt | false |

## Process

### Step 1: Check for Active Loop

```
IF NOT exists(.claude/ralph-loop.local.md):
   ╔══════════════════════════════════════════════════════════════╗
   ║ ℹ️  Aucune boucle Ralph active                                ║
   ╠══════════════════════════════════════════════════════════════╣
   ║ Le fichier .claude/ralph-loop.local.md n'existe pas.         ║
   ║                                                              ║
   ║ Pour démarrer une boucle Ralph:                              ║
   ║ → /ralph <specs-dir>                                         ║
   ╚══════════════════════════════════════════════════════════════╝
   EXIT
```

### Step 2: Read Current State

Extract from state file:
- Current iteration
- Stories completed
- Total stories
- Mode (hook or script)

### Step 3: Confirmation (unless --force)

```
┌─────────────────────────────────────────────────────────────────────┐
│ ⚠️  ANNULATION BOUCLE RALPH                                         │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│ Session active:                                                     │
│ ├── Mode: {hook|script}                                            │
│ ├── Itération: {current}/{max}                                     │
│ ├── Stories: {completed}/{total}                                   │
│ └── Démarrée: {started_at}                                         │
│                                                                     │
│ Voulez-vous vraiment annuler cette boucle ?                        │
│ (Les changements déjà commités seront conservés)                   │
│                                                                     │
├─────────────────────────────────────────────────────────────────────┤
│ [Y] Confirmer    [n] Annuler                                       │
└─────────────────────────────────────────────────────────────────────┘
```

### Step 4: Cancel Loop

1. Update state file status to CANCELLED
2. Remove state file (or archive to .claude/ralph-loop.cancelled.md)
3. Display summary

```
┌─────────────────────────────────────────────────────────────────────┐
│ ✅ BOUCLE RALPH ANNULÉE                                             │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│ Résumé de la session:                                              │
│ ├── Itérations effectuées: {count}                                 │
│ ├── Stories complétées: {completed}                                │
│ ├── Durée: {duration}                                              │
│ └── Commits: {commit_count}                                        │
│                                                                     │
│ Les changements commités ont été conservés.                        │
│ Pour reprendre: /ralph <specs-dir> --continue                      │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

## Mode Script

For script mode (`--mode script`), this command also:
- Sends SIGTERM to ralph_loop.sh process if running
- Updates circuit breaker state to OPEN
- Saves checkpoint for --continue

## Error Handling

| Error | Action |
|-------|--------|
| State file corrupted | Force remove, warn user |
| Process not responding | Kill -9 after 5s timeout |
| Permission denied | Suggest sudo or check permissions |

## See Also

- `/ralph` — Start autonomous execution
- `/orchestrate` — Legacy batch execution (deprecated)
