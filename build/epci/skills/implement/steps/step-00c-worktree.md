---
name: step-00c-worktree
description: Optional worktree creation for parallel development
prev_step: steps/step-00-init.md
next_step: steps/step-01-explore.md
conditional_next:
  - condition: "worktree declined or skipped"
    step: steps/step-01-explore.md
---

# Step 00c: Worktree Setup

## Reference Files

- `scripts/worktree-create.sh` - Creates worktree with branch
- `scripts/worktree-status.sh` - Checks worktree status (JSON)
- `scripts/worktree-finalize.sh` - Removes worktree on completion

## MANDATORY EXECUTION RULES (READ FIRST):

- 🔴 NEVER force worktree creation (opt-in only)
- 🔴 NEVER skip existing worktree detection
- ✅ ALWAYS check worktree status first
- ✅ ALWAYS update state.json with worktree metadata
- ✅ ALWAYS change directory to worktree if created
- 💭 FOCUS on enabling parallel development without friction

## EXECUTION PROTOCOLS:

### 1. Check Existing Worktree

Before presenting options, check if a worktree already exists:

EXECUTE Bash({
  command: "./scripts/worktree-status.sh {feature-slug}",
  description: "Check worktree status"
})

Parse JSON result from script:
- Script returns: `{"exists": bool, "path": string, "branch": string, "clean": bool}`

Decision logic:
- If `exists == false`: Go to **Main Breakpoint** (offer to create)
- If `exists == true`: Check state.json `state.worktree.status`:
  - If `state.worktree.status == "active"`: Go to **Resume Breakpoint**
  - If `state.worktree.status == "abandoned"` or missing: Go to **Main Breakpoint** (offer to recreate)

**Note:** `worktree-status.sh` reports filesystem/git state (`exists`, `clean`).
`state.worktree.status` tracks lifecycle (`active`, `merged`, `abandoned`).

### 2. Main Breakpoint (New Worktree)

Present opt-in choice for worktree creation.

AFFICHE cette boite:


┌─────────────────────────────────────────────────────────────────────┐
│ WORKTREE SETUP                                                      │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│ Feature: {feature-slug}                                             │
│ Complexity: {complexity}                                            │
│ Current worktree: None                                              │
│                                                                     │
│ Worktree enables parallel development of multiple features.         │
│ Path: ../worktrees/{feature-slug}/                                  │
│ Branch: feature/{feature-slug}                                      │
│                                                                     │
├─────────────────────────────────────────────────────────────────────┤
│ ┌─ Options ──────────────────────────────────────────────────────┐ │
│ │  [A] Create worktree (Recommended) - Isolated development      │ │
│ │  [B] Skip worktree - Work in main repo                         │ │
│ │  [?] Autre reponse...                                          │ │
│ └────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘


APPELLE AskUserQuestion({
  questions: [{
    question: "Utiliser un worktree pour cette feature?",
    header: "Worktree",
    multiSelect: false,
    options: [
      { label: "Create worktree (Recommended)", description: "Isolated development, parallel work possible" },
      { label: "Skip worktree", description: "Work in main repo, simpler but no parallel features" }
    ]
  }]
})

⏸️ ATTENDS la reponse utilisateur avant de continuer.

### 3. Resume Breakpoint (Existing Active Worktree)

If worktree exists and is active:


┌─────────────────────────────────────────────────────────────────────┐
│ WORKTREE DETECTED                                                   │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│ Feature: {feature-slug}                                             │
│ Existing worktree: {worktree.path}                                  │
│ Branch: {worktree.branch}                                           │
│ Status: {clean/dirty}                                               │
│                                                                     │
├─────────────────────────────────────────────────────────────────────┤
│ ┌─ Options ──────────────────────────────────────────────────────┐ │
│ │  [A] Resume in worktree (Recommended) - Continue work          │ │
│ │  [B] Recreate worktree - Start fresh                           │ │
│ │  [C] Skip worktree - Work in main repo instead                 │ │
│ │  [?] Autre reponse...                                          │ │
│ └────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘


APPELLE AskUserQuestion({
  questions: [{
    question: "Un worktree existe déjà. Que souhaitez-vous faire?",
    header: "Worktree",
    multiSelect: false,
    options: [
      { label: "Resume in worktree (Recommended)", description: "Continue work in existing worktree" },
      { label: "Recreate worktree", description: "Delete and recreate fresh worktree" },
      { label: "Skip worktree", description: "Work in main repo instead" }
    ]
  }]
})

⏸️ ATTENDS la reponse utilisateur avant de continuer.

### 4. Execute Worktree Creation

IF user selected "Create worktree":

EXECUTE Bash({
  command: "./scripts/worktree-create.sh {feature-slug}",
  description: "Create worktree for feature"
})

On success:
1. Update state.json with worktree metadata:
```json
{
  "worktree": {
    "enabled": true,
    "path": "../worktrees/{feature-slug}",
    "branch": "feature/{feature-slug}",
    "status": "active",
    "created_at": "{ISO-8601}"
  }
}
```

2. Change working directory to worktree path
3. Log success message

### 5. Skip Worktree

IF user selected "Skip worktree":

1. Update state.json:
```json
{
  "worktree": {
    "enabled": false
  }
}
```

2. Continue in main repo

## CONTEXT BOUNDARIES:

- This step expects: Validated STANDARD+ complexity, feature-slug
- This step produces: Worktree created (or skipped), state updated, working directory set

## OUTPUT FORMAT:

### If worktree created:
```
## Worktree Created

Feature: {feature-slug}
Path: ../worktrees/{feature-slug}/
Branch: feature/{feature-slug}

Working directory changed to worktree.
Proceeding to Explore phase...
```

### If worktree skipped:
```
## Worktree Skipped

Feature: {feature-slug}
Working in main repository.

Proceeding to Explore phase...
```

## NEXT STEP TRIGGER:

After worktree decision (create or skip), proceed to `step-01-explore.md`.
