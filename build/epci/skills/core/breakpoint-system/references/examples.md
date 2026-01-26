# Breakpoint Examples by Skill

Real-world usage examples for each EPCI skill that uses breakpoint-system.

## /brainstorm — ems-status

Display EMS progress during brainstorming iterations.

```typescript
@skill:breakpoint-system
  type: ems-status
  title: "BRAINSTORM STATUS"
  data: {
    phase: "DIVERGENT",
    iteration: 3,
    ems: {
      score: 65,
      delta: "+12",
      axes: {
        clarity: 80,
        depth: 60,
        coverage: 45,
        decisions: 75,
        actionability: 70
      },
      weak_axes: ["coverage"]
    },
    done: ["Cible identifiee", "Contraintes listees", "Stack validee"],
    open: ["Delais a preciser", "Integrations externes"],
    commands: ["continue", "dive", "back", "save", "finish"]
  }
  suggestions: [
    {
      pattern: "coverage-low",
      text: "Coverage a 45% - explorer perspectives stakeholders",
      priority: "P2",
      action: "technique six-hats"
    }
  ]
```

**Output:**
```
┌─────────────────────────────────────────────────────────────────────┐
│ [E] BRAINSTORM STATUS — Iteration 3                                 │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│ Phase: DIVERGENT                    EMS Score: 65/100 (+12)         │
│                                                                     │
│ ┌─ EMS Axes ─────────────────────────────────────────────────────┐ │
│ │ Clarity      ########-- 80%                                    │ │
│ │ Depth        ######---- 60%                                    │ │
│ │ Coverage     ####------ 45% [!]                                │ │
│ │ Decisions    #######--- 75%                                    │ │
│ │ Actionable   #######--- 70%                                    │ │
│ └────────────────────────────────────────────────────────────────┘ │
│                                                                     │
│ [ok] Done: Cible identifiee, Contraintes listees, Stack validee     │
│ [ ] Open: Delais a preciser, Integrations externes                  │
│                                                                     │
├─────────────────────────────────────────────────────────────────────┤
│ SUGGESTIONS PROACTIVES                                              │
│ [*] [P2] Coverage a 45% - explorer perspectives stakeholders        │
│    -> technique six-hats                                            │
├─────────────────────────────────────────────────────────────────────┤
│ Commands: continue | dive | back | save | finish                    │
└─────────────────────────────────────────────────────────────────────┘
```

---

## /brainstorm — validation

Validate brief before proceeding.

```typescript
@skill:breakpoint-system
  type: validation
  title: "VALIDATION DU BRIEF"
  data: {
    context: "Brief reformule apres clarification vocale",
    item_to_validate: {
      objectif: "Implementer authentification OAuth Google",
      contexte: "Application Symfony 6.3 existante avec users locaux",
      contraintes: "Migration progressive, pas de breaking changes API",
      success_criteria: "Login Google fonctionnel, users existants preserves"
    }
  }
  ask: {
    question: "Le brief vous convient-il ?",
    header: "Validation",
    options: [
      {label: "Valider (Recommended)", description: "Continuer vers exploration"},
      {label: "Modifier", description: "Je reformule moi-meme"},
      {label: "Annuler", description: "Arreter workflow"}
    ]
  }
```

**Output:**
```
┌─────────────────────────────────────────────────────────────────────┐
│ [V] VALIDATION DU BRIEF                                             │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│ Brief reformule apres clarification vocale                          │
│                                                                     │
│ - Objectif: Implementer authentification OAuth Google               │
│ - Contexte: Application Symfony 6.3 existante avec users locaux     │
│ - Contraintes: Migration progressive, pas de breaking changes API   │
│ - Criteres: Login Google fonctionnel, users existants preserves     │
│                                                                     │
│ ┌─ Options ──────────────────────────────────────────────────────┐ │
│ │  [A] Valider (Recommended) — Continuer vers exploration        │ │
│ │  [B] Modifier — Je reformule moi-meme                          │ │
│ │  [C] Annuler — Arreter workflow                                │ │
│ │  [?] Autre reponse...                                          │ │
│ └────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
```

---

## /spec — plan-review

Review generated PRD before finalization.

```typescript
@skill:breakpoint-system
  type: plan-review
  title: "PRD REVIEW — auth-oauth-google"
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
    skills_loaded: ["php-symfony", "security-patterns", "testing-strategy"],
    preview_next: {
      tasks: [
        {title: "Create OAuthController", time: "30min"},
        {title: "Implement GoogleAuthenticator", time: "45min"},
        {title: "Add UserProvider adapter", time: "30min"}
      ],
      remaining_tasks: 3
    },
    feature_doc_path: "docs/specs/auth-oauth-google.md"
  }
  ask: {
    question: "Comment souhaitez-vous proceder ?",
    header: "PRD Review",
    options: [
      {label: "Valider (Recommended)", description: "Generer PRD final et artifacts Ralph"},
      {label: "Modifier", description: "Ajuster avant generation"},
      {label: "Annuler", description: "Abandonner specification"}
    ]
  }
  suggestions: [
    {
      pattern: "security-auth",
      text: "Feature auth detectee - audit securite recommande",
      priority: "P1",
      action: "integrer security-patterns"
    }
  ]
```

---

## /implement — phase-transition

Transition between EPCI phases.

```typescript
@skill:breakpoint-system
  type: phase-transition
  title: "FIN PHASE EXPLORE"
  data: {
    phase_completed: "explore",
    phase_next: "plan",
    summary: {
      duration: "12min",
      tasks_completed: 1,
      files_modified: [],
      tests_status: "N/A"
    },
    checkpoint_created: {
      id: "ckpt-explore-001",
      resumable: true
    }
  }
  ask: {
    question: "Passer a la phase Plan ?",
    header: "Phase",
    options: [
      {label: "Continuer (Recommended)", description: "Passer a Plan"},
      {label: "Pause", description: "Sauvegarder et reprendre plus tard"},
      {label: "Annuler", description: "Abandonner le workflow"}
    ]
  }
```

**Output:**
```
┌─────────────────────────────────────────────────────────────────────┐
│ [>] FIN PHASE EXPLORE                                               │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│ TRANSITION DE PHASE                                                 │
│                                                                     │
│ Phase terminee: explore                                             │
│ Prochaine phase: plan                                               │
│                                                                     │
│ RESUME                                                              │
│ - Duree: 12min                                                      │
│ - Taches completees: 1                                              │
│ - Fichiers modifies: 0                                              │
│ - Tests: N/A                                                        │
│                                                                     │
│ CHECKPOINT                                                          │
│ ID: ckpt-explore-001                                                │
│ Resumable: Oui                                                      │
│                                                                     │
│ ┌─ Options ──────────────────────────────────────────────────────┐ │
│ │  [A] Continuer (Recommended) — Passer a Plan                   │ │
│ │  [B] Pause — Sauvegarder et reprendre plus tard                │ │
│ │  [C] Annuler — Abandonner le workflow                          │ │
│ │  [?] Autre reponse...                                          │ │
│ └────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
```

---

## /debug — diagnostic

Present root cause analysis and solution options.

```typescript
@skill:breakpoint-system
  type: diagnostic
  title: "DIAGNOSTIC — JWT Token Issue"
  data: {
    root_cause: "Token JWT expire non rafraichi automatiquement",
    confidence: 0.85,
    decision_tree: "AuthMiddleware -> TokenValidator -> JWTService.refresh() [FAIL]",
    solutions: [
      {id: "S1", title: "Implementer auto-refresh token", effort: "2h", risk: "Low"},
      {id: "S2", title: "Augmenter TTL token a 24h", effort: "15min", risk: "Medium"},
      {id: "S3", title: "Forcer re-login apres expiration", effort: "30min", risk: "Low"}
    ]
  }
  ask: {
    question: "Quelle solution implementer ?",
    header: "Solution",
    options: [
      {label: "S1: Auto-refresh (Recommended)", description: "2h, risque faible"},
      {label: "S2: Augmenter TTL", description: "15min, risque moyen"},
      {label: "S3: Forcer re-login", description: "30min, risque faible"}
    ]
  }
  suggestions: [
    {
      pattern: "jwt-best-practice",
      text: "Pattern refresh token recommande pour OAuth",
      priority: "P1",
      action: "voir RFC 6749 section 6"
    }
  ]
```

**Output:**
```
┌─────────────────────────────────────────────────────────────────────┐
│ [?] DIAGNOSTIC — JWT Token Issue                                    │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│ ROOT CAUSE ANALYSIS                                                 │
│                                                                     │
│ Cause identifiee: Token JWT expire non rafraichi automatiquement    │
│ Confiance: 85%                                                      │
│                                                                     │
│ Arbre de decision:                                                  │
│ AuthMiddleware -> TokenValidator -> JWTService.refresh() [FAIL]     │
│                                                                     │
│ SOLUTIONS PROPOSEES                                                 │
│ ┌──────┬───────────────────────────────┬────────┬────────┐         │
│ │ ID   │ Solution                      │ Effort │ Risque │         │
│ ├──────┼───────────────────────────────┼────────┼────────┤         │
│ │ S1   │ Implementer auto-refresh      │ 2h     │ Low    │         │
│ │ S2   │ Augmenter TTL token a 24h     │ 15min  │ Medium │         │
│ │ S3   │ Forcer re-login apres expir.  │ 30min  │ Low    │         │
│ └──────┴───────────────────────────────┴────────┴────────┘         │
│                                                                     │
├─────────────────────────────────────────────────────────────────────┤
│ SUGGESTIONS PROACTIVES                                              │
│ [!] [P1] Pattern refresh token recommande pour OAuth                │
│    -> voir RFC 6749 section 6                                       │
├─────────────────────────────────────────────────────────────────────┤
│ ┌─ Options ──────────────────────────────────────────────────────┐ │
│ │  [A] S1: Auto-refresh (Recommended) — 2h, risque faible        │ │
│ │  [B] S2: Augmenter TTL — 15min, risque moyen                   │ │
│ │  [C] S3: Forcer re-login — 30min, risque faible                │ │
│ │  [?] Autre reponse...                                          │ │
│ └────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
```

---

## /refactor — plan-review

Review refactoring plan before execution.

```typescript
@skill:breakpoint-system
  type: plan-review
  title: "REFACTOR PLAN — src/services/"
  data: {
    metrics: {
      complexity: "STANDARD",
      complexity_score: 5.8,
      files_impacted: 8,
      time_estimate: "1-2h",
      risk_level: "LOW",
      risk_description: "Tests complets existants"
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
    skills_loaded: ["refactoring-patterns"],
    preview_next: {
      tasks: [
        {title: "Extract AuthService from UserService", time: "30min"},
        {title: "Create TokenService", time: "20min"},
        {title: "Update imports across codebase", time: "15min"}
      ],
      remaining_tasks: 2
    },
    feature_doc_path: null
  }
  ask: {
    question: "Executer le plan de refactoring ?",
    header: "Refactor",
    options: [
      {label: "Executer (Recommended)", description: "Lancer refactoring step-by-step"},
      {label: "Modifier", description: "Ajuster le plan"},
      {label: "Annuler", description: "Abandonner refactoring"}
    ]
  }
```

---

## /factory — validation

Validate skill before generation.

```typescript
@skill:breakpoint-system
  type: validation
  title: "SKILL READY FOR GENERATION"
  data: {
    context: "Validation 12-point checklist passed",
    item_to_validate: {
      objectif: "Creer skill breakpoint-system",
      contexte: "Core skill pour EPCI v6.0",
      contraintes: "user-invocable: false, max 500 lines",
      success_criteria: "12/12 checks passed"
    }
  }
  ask: {
    question: "Generer le skill ?",
    header: "Generation",
    options: [
      {label: "Generer (Recommended)", description: "Creer tous les fichiers"},
      {label: "Modifier", description: "Ajuster le design"},
      {label: "Annuler", description: "Abandonner creation"}
    ]
  }
```

---

## /quick — validation (SMALL only)

Simple validation before quick implementation.

```typescript
@skill:breakpoint-system
  type: validation
  title: "QUICK VALIDATION"
  data: {
    context: "Tache SMALL detectee - validation rapide",
    item_to_validate: {
      objectif: "Ajouter validation email au formulaire",
      contexte: "Formulaire contact existant",
      contraintes: "< 30min implementation",
      success_criteria: "Email valide requis, message erreur clair"
    }
  }
  ask: {
    question: "Proceder a l'implementation ?",
    header: "Quick",
    options: [
      {label: "Go (Recommended)", description: "Implementer maintenant"},
      {label: "Annuler", description: "Ne pas implementer"}
    ]
  }
```
