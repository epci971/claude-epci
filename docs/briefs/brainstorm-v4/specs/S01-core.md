# Specification — S01: Core

> **Parent project**: brainstorm-v4.2
> **Spec ID**: S01
> **Estimated effort**: 4.5 jours
> **Dependencies**: —
> **Blocks**: S03

---

## 1. Context

Cette spec implémente les fondations du brainstormer v4.2:
- Persistence de session
- Navigation améliorée
- Energy checkpoints
- Nouveau format de questions

**Source**: `brief-brainstorm-v4.2-2026-01-06.md` — Sections 2.1, 2.3, 2.4, 2.5, 2.7

---

## 2. Scope

### Included

- Session continuation (save, continue-session, auto-detect)
- Commande `back` (retour 1 itération)
- Energy checkpoints (4 triggers, format hybride)
- Format 3-5 questions par itération avec suggestions A/B/C
- Confirmation agents [Y/n] avant @planner/@security
- Documentation session-format.md

### Excluded

- Bibliothèque de techniques (→ S02)
- Modes --random et --progressive (→ S03)
- Tests complets (→ S03)
- Parallélisation @Explore (→ S03)

---

## 3. Tasks

### 3.1 Session Continuation

- [ ] Créer `references/session-format.md` avec structure YAML
- [ ] Implémenter commande `save` dans brainstorm.md
- [ ] Implémenter logique auto-detect session au lancement
- [ ] Ajouter prompt de reprise "[1] Reprendre [2] Nouvelle"
- [ ] Stocker sessions dans `.project-memory/brainstorm-sessions/`

**Format session YAML:**
```yaml
session:
  id: "feature-auth-2026-01-06"
  slug: "feature-auth"
  status: "in_progress"
  phase: "divergent"
  ems: 45
  persona: "architecte"
  iteration: 3
  techniques_used: ["moscow", "5whys"]
  ideas:
    - id: 1
      content: "OAuth2 avec refresh tokens"
      score: 8
  history:
    - iteration: 1
      questions: [...]
      responses: [...]
      ems_delta: +15
  last_question: "..."
  created: "2026-01-06T10:30:00"
  updated: "2026-01-06T11:15:00"
```

### 3.2 Navigation Back

- [ ] Ajouter commande `back` dans la liste des commandes
- [ ] Implémenter restauration état précédent (EMS, questions, phase)
- [ ] Utiliser history de la session pour rollback
- [ ] Limiter à 1 step back (simple)

### 3.3 Energy Checkpoints

- [ ] Définir 4 triggers:
  - EMS atteint 50
  - EMS atteint 75
  - Itération >= 7 sans commande
  - Changement phase Divergent → Convergent
- [ ] Implémenter format hybride CLI + humain
- [ ] Ajouter commande `energy` pour forcer un check

**Format energy check:**
```
-------------------------------------------------------
⚡ ENERGY CHECK | EMS: 52/100 | Phase: 🔀 Divergent
-------------------------------------------------------
On a bien avancé sur l'exploration. Comment tu te sens?

[1] Continuer — Je suis dans le flow
[2] Pause — Sauvegarder et reprendre plus tard
[3] Accélérer — Passons à la convergence
[4] Pivoter — Je veux changer d'angle
-------------------------------------------------------
```

### 3.4 Format 3-5 Questions

- [ ] Modifier le breakpoint pour afficher 3-5 questions
- [ ] Conserver format A/B/C avec suggestions
- [ ] Adapter la logique d'itération (batch de questions)

**Nouveau format breakpoint:**
```
-------------------------------------------------------
🔀 DIVERGENT | 📐 Architecte | Iter 3 | EMS: 52/100 (+8)
-------------------------------------------------------
1. [Question 1]
   A) Option A  B) Option B  C) Option C
   → Suggestion: B

2. [Question 2]
   A) Option A  B) Option B  C) Option C
   → Suggestion: A

3. [Question 3]
   A) Option A  B) Option B  C) Option C

-> continue | dive [topic] | back | save | finish
-------------------------------------------------------
```

### 3.5 Confirmation Agents

- [ ] Modifier trigger @planner (EMS ≥70) pour demander confirmation
- [ ] Modifier trigger @security-auditor pour demander confirmation
- [ ] Format: `Lancer @planner? [Y/n]`

**Format confirmation:**
```
-------------------------------------------------------
🎯 EMS atteint 72 — Prêt pour un plan préliminaire?
   Lancer @planner? [Y/n]
-------------------------------------------------------
```

### 3.6 Mise à jour Documentation

- [ ] Mettre à jour SKILL.md avec nouvelles références
- [ ] Documenter nouvelles commandes dans brainstorm.md
- [ ] Ajouter section session dans SKILL.md

---

## 4. Acceptance Criteria

| ID | Criterion | Verification |
|----|-----------|--------------|
| S01-AC1 | Session save/restore fonctionne | Sauvegarder session, fermer, reprendre → état identique |
| S01-AC2 | Auto-detect session au lancement | Lancer /brainstorm avec session existante → prompt reprise |
| S01-AC3 | Commande back restaure l'état | Exécuter back → EMS et questions de l'itération précédente |
| S01-AC4 | Energy check à EMS 50 | Atteindre EMS 50 → checkpoint affiché |
| S01-AC5 | Energy check à EMS 75 | Atteindre EMS 75 → checkpoint affiché |
| S01-AC6 | Format 3-5 questions | Chaque itération affiche 3-5 questions avec A/B/C |
| S01-AC7 | Confirmation @planner | EMS ≥70 → demande confirmation avant lancement |
| S01-AC8 | Session YAML valide | Fichier .yaml généré conforme au format documenté |

---

## 5. Files Impacted

### Modifications

| Fichier | Changements |
|---------|-------------|
| `src/commands/brainstorm.md` | Commandes save/back/energy, format questions, confirmation agents, auto-detect |
| `src/skills/core/brainstormer/SKILL.md` | Référence session-format.md, nouvelles instructions |

### Créations

| Fichier | Description |
|---------|-------------|
| `src/skills/core/brainstormer/references/session-format.md` | Documentation format YAML session |

### Runtime

| Fichier | Description |
|---------|-------------|
| `.project-memory/brainstorm-sessions/[slug].yaml` | Sessions sauvegardées |

---

## 6. Source Reference

> Extraits de `brief-brainstorm-v4.2-2026-01-06.md`

### Section 2.1 — Format Questions
```
**Après (v4.2):** 3-5 questions par itération avec suggestions A/B/C
```

### Section 2.3 — Session Continuation
```
**Stockage:** `.project-memory/brainstorm-sessions/[slug].yaml`
**Commandes:** save, continue-session
**Auto-detection au lancement**
```

### Section 2.4 — Navigation
```
**Nouvelle commande back:** Revient à l'itération précédente
```

### Section 2.5 — Energy Checkpoints
```
**Triggers:** EMS 50, EMS 75, Iter >=7, Changement phase
**Format:** Hybride CLI + humain
```

### Section 2.7 — Agents
```
**NOUVEAU:** Confirmation avant lancement [Y/n]
```

---

*Generated by /decompose — Project: brainstorm-v4.2*
