---
description: >-
  Unified Git commit command for EPCI workflows. Centralizes commit logic
  for /epci, /quick, and /debug. Supports context-rich mode (via JSON) and
  standalone mode (degraded). Follows Conventional Commits format.
argument-hint: "[--auto-commit] [--amend] [--no-hooks] [--dry-run]"
allowed-tools: [Read, Write, Bash, Glob]
---

# EPCI Commit — Unified Git Commit

## Overview

Centralized commit command that:
- Handles commits for `/epci`, `/quick`, and `/debug` workflows
- Works standalone for manual commits
- Follows Conventional Commits format
- Integrates with EPCI hooks system

## Modes

| Mode | Condition | Behavior |
|------|-----------|----------|
| **Context-rich** | `.epci-commit-context.json` present | Uses context, proposes message |
| **Degraded** | No context file | Detects modified files, asks for type + description |

## Arguments

| Flag | Effect | Default |
|------|--------|---------|
| `--auto-commit` | Skip breakpoint, commit directly | Off |
| `--amend` | Amend the last commit | Off |
| `--no-hooks` | Skip pre/post-commit hooks | Off |
| `--dry-run` | Show what would be done without executing | Off |

## Configuration

| Element | Value |
|---------|-------|
| **Thinking** | `think` (default) |
| **Skills** | git-workflow |
| **Subagents** | None |

## Context File Schema

**Location:** `.epci-commit-context.json` (project root)

```json
{
  "source": "epci|quick|debug",
  "type": "feat|fix|refactor|docs|style|test|chore|perf|ci",
  "scope": "module-name",
  "description": "what was done",
  "files": ["file1.ts", "file2.ts"],
  "featureDoc": "path/to/feature-doc.md",
  "breaking": false,
  "ticket": "JIRA-123"
}
```

---

## Process

### Step 1: Detect Mode

Check for context file:

```bash
if [ -f ".epci-commit-context.json" ]; then
  # Context-rich mode
else
  # Degraded mode
fi
```

---

### Step 2a: Context-Rich Mode

**If `.epci-commit-context.json` exists:**

1. **Read context file:**
   ```bash
   cat .epci-commit-context.json
   ```

2. **Generate commit message** from context:
   ```
   {type}({scope}): {description}

   - {detail from files list}

   Refs: {featureDoc}
   {ticket if present}
   ```

3. **Handle breaking changes:**
   - If `breaking: true` → Add `!` after type: `feat(scope)!: description`
   - Add `BREAKING CHANGE:` footer

4. **Proceed to Step 3** (Breakpoint)

---

### Step 2b: Degraded Mode (Standalone)

**If no context file:**

1. **Detect modified files:**
   ```bash
   git status --porcelain
   ```

2. **If no changes detected:**
   ```
   ⚠️ Aucun fichier modifié détecté.
   
   Utilisez `git add <files>` pour stager vos modifications,
   ou lancez `/commit` depuis un workflow EPCI.
   ```
   → Stop workflow

3. **Ask user for commit details:**
   ```
   📝 MODE STANDALONE — Informations requises
   
   Fichiers modifiés détectés:
   - {file1}
   - {file2}
   
   Veuillez fournir:
   1. Type: feat|fix|refactor|docs|style|test|chore|perf|ci
   2. Scope (optionnel): module ou composant concerné
   3. Description: résumé impératif (ex: "add user validation")
   ```

4. **Generate commit message** from user input

5. **Proceed to Step 3** (Breakpoint)

---

### Step 3: BREAKPOINT PRE-COMMIT

**⚠️ MANDATORY unless `--auto-commit` flag is active.**

**🪝 Execute `pre-commit` hooks** (unless `--no-hooks`):

```bash
python3 src/hooks/runner.py pre-commit --context '{
  "phase": "commit",
  "source": "<source>",
  "files_modified": [...],
  "commit_message": "<prepared message>",
  "pending_commit": true
}'
```

**Display breakpoint:**

```
┌─────────────────────────────────────────────────────────────────────┐
│ ⏸️  BREAKPOINT — Validation Commit                                  │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│ 📝 MESSAGE DE COMMIT                                                │
│ ┌─────────────────────────────────────────────────────────────────┐ │
│ │ {TYPE}({SCOPE}): {DESCRIPTION}                                  │ │
│ │                                                                 │ │
│ │ - {DETAIL_1}                                                    │ │
│ │ - {DETAIL_2}                                                    │ │
│ │                                                                 │ │
│ │ Refs: {FEATURE_DOC}                                             │ │
│ └─────────────────────────────────────────────────────────────────┘ │
│                                                                     │
│ 📋 RÉSUMÉ                                                           │
│ ├── Source: {epci|quick|debug|standalone}                          │
│ ├── Fichiers: {FILE_COUNT}                                         │
│ └── Mode: {normal|amend|dry-run}                                   │
│                                                                     │
├─────────────────────────────────────────────────────────────────────┤
│ Options:                                                            │
│   • Tapez "Commiter" → Exécuter git commit                         │
│   • Tapez "Modifier" → Éditer le message de commit                 │
│   • Tapez "Annuler" → Abandonner le commit                         │
└─────────────────────────────────────────────────────────────────────┘
```

**If `--auto-commit` active:** Skip breakpoint, proceed directly to Step 4.

**If `--dry-run` active:** Display what would be done, then stop.

---

### Step 4: Execute Commit

**Based on user choice or auto-commit:**

#### If "Commiter" (or --auto-commit)

1. **Stage files** (if not already staged):
   ```bash
   git add <files from context or detected>
   ```

2. **Execute commit:**
   ```bash
   # Normal mode
   git commit -m "<prepared message>"
   
   # If --amend
   git commit --amend -m "<prepared message>"
   ```

3. **Capture commit hash:**
   ```bash
   git rev-parse --short HEAD
   ```

4. **Proceed to Step 5** (Post-commit)

#### If "Modifier"

1. Ask user for new message (type, scope, description)
2. Update prepared message
3. Return to breakpoint display

#### If "Annuler"

1. Display cancellation message
2. Keep context file (user may retry)
3. Stop workflow

---

### Step 5: Post-Commit Actions

**🪝 Execute `post-commit` hooks** (unless `--no-hooks`):

```bash
python3 src/hooks/runner.py post-commit --context '{
  "phase": "commit",
  "source": "<source>",
  "commit_hash": "<hash>",
  "branch": "<current branch>",
  "files_committed": [...]
}'
```

---

### Step 6: Cleanup

**After successful commit:**

1. **Delete context file:**
   ```bash
   rm -f .epci-commit-context.json
   ```

2. **Display success message**

---

## Output

### Success

```
┌─────────────────────────────────────────────────────────────────────┐
│ ✅ COMMIT RÉUSSI                                                    │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│ Hash: {COMMIT_HASH}                                                │
│ Branch: {BRANCH}                                                   │
│ Message: {TYPE}({SCOPE}): {DESCRIPTION}                            │
│                                                                     │
│ Fichiers committés:                                                │
│ ├── {file1} (+{X} / -{Y})                                         │
│ ├── {file2} (+{Z} / -{W})                                         │
│ └── {file3} (+{A} / -{B})                                         │
│                                                                     │
│ 🧹 Contexte nettoyé (.epci-commit-context.json supprimé)           │
│                                                                     │
│ Prochaine étape: git push / Créer PR                               │
└─────────────────────────────────────────────────────────────────────┘
```

### Cancelled

```
┌─────────────────────────────────────────────────────────────────────┐
│ ⚠️ COMMIT ANNULÉ                                                    │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│ Le commit a été annulé par l'utilisateur.                          │
│                                                                     │
│ Le fichier de contexte a été conservé.                             │
│ Relancez /commit quand vous êtes prêt.                             │
└─────────────────────────────────────────────────────────────────────┘
```

### Dry Run

```
┌─────────────────────────────────────────────────────────────────────┐
│ 🔍 DRY RUN — Simulation                                            │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│ Commande qui serait exécutée:                                      │
│ git add {files}                                                    │
│ git commit -m "{message}"                                          │
│                                                                     │
│ Fichiers qui seraient committés:                                   │
│ ├── {file1}                                                        │
│ ├── {file2}                                                        │
│ └── {file3}                                                        │
│                                                                     │
│ Aucune modification effectuée.                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Error Handling

### Git Errors

| Error | Suggestion |
|-------|------------|
| `nothing to commit` | Vérifiez que les fichiers sont stagés (`git add`) |
| `not a git repository` | Initialisez un repo (`git init`) ou vérifiez le chemin |
| `merge conflict` | Résolvez les conflits avant de commiter |
| `commit failed` | Vérifiez les hooks pre-commit, permissions |

**Display format:**

```
┌─────────────────────────────────────────────────────────────────────┐
│ ❌ ERREUR GIT                                                       │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│ {error message}                                                    │
│                                                                     │
│ 💡 Suggestion: {suggestion}                                        │
│                                                                     │
│ Le fichier de contexte a été conservé.                             │
│ Corrigez l'erreur puis relancez /commit.                           │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Integration with Workflows

### From /epci

`/epci` Phase 3 generates context and suggests:
```
→ Contexte commit préparé. Lancez /commit pour finaliser.
```

### From /quick

`/quick` generates context at completion:
```
Pour commiter: /commit
```

With `--turbo`: suggests `/commit --auto-commit`

### From /debug

`/debug --commit` generates context after fix:
```
Fix appliqué → /commit pour finaliser
```

---

## Conventional Commits Reference

| Type | Usage |
|------|-------|
| `feat` | New feature |
| `fix` | Bug fix |
| `docs` | Documentation only |
| `style` | Formatting (no code change) |
| `refactor` | Code restructuring |
| `test` | Adding/modifying tests |
| `chore` | Maintenance tasks |
| `perf` | Performance improvement |
| `ci` | CI/CD changes |

**Format:** `type(scope): description`

**Breaking change:** `type(scope)!: description` + `BREAKING CHANGE:` footer
