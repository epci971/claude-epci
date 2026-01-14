# PRD — Worktree Integration EPCI

| Metadata | Value |
|----------|-------|
| **Document ID** | PRD-2026-001 |
| **Version** | 1.0 |
| **Status** | Draft |
| **Owner** | EPCI Team |
| **Created** | 2026-01-14 |
| **Last Updated** | 2026-01-14 |
| **Slug** | worktree-integration |
| **EMS Score** | 78/100 |
| **Template** | feature |

### Change History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-01-14 | EPCI Brainstormer | Initial generation from /brainstorm |

---

## Executive Summary

**TL;DR** : Integrer les Git worktrees dans EPCI via 3 scripts bash pour isoler le developpement de features dans des repertoires separes.

| Aspect | Description |
|--------|-------------|
| **Problem** | Context switching couteux et risque de conflits entre features en parallele |
| **Solution** | 3 scripts (create/finalize/abort) + suggestions dans /brief et appel auto en fin de workflow |
| **Impact** | Isolation totale des features, workflow plus propre, compatibilite multi-agents |
| **Target Launch** | TBD |

---

## Background & Strategic Fit

### Why Now?

Les agents IA (Claude Code, Aider, Cursor) permettent desormais de travailler sur plusieurs features en parallele. Les worktrees sont la solution native Git pour supporter ce workflow. Incident.io rapporte 4-5 agents Claude en parallele avec worktrees.

### Strategic Alignment

Cette feature s'aligne avec :
- [x] **Vision Produit** : EPCI = workflow structure, worktrees = isolation propre
- [x] **Position Marche** : Support multi-agents = avantage competitif

---

## Problem Statement

### Current Situation

Actuellement, le developpement EPCI se fait sur une seule branche. Pour travailler sur plusieurs features :
- Context switch via `git stash` (perte de contexte)
- Commits incomplets forces
- Risque de modifications croisees entre features

### Problem Definition

L'isolation des features en developpement n'est pas automatisee dans EPCI, ce qui rend le travail parallele fragile et error-prone.

### Evidence & Data

- **Quantitative** : 10-15 min de setup a chaque context switch (source: recherche web)
- **Qualitative** : Worktrees mentionnes comme best practice pour Claude Code (multiple sources 2025)

### Impact of Not Solving

- **Business** : Productivite reduite sur projets multi-features
- **User** : Frustration lors des context switches
- **Technical** : Commits pollues, branches sales

---

## Goals

### Business Goals

- [ ] Permettre le developpement parallele de 3-5 features simultanement

### User Goals

- [ ] Creer un worktree en une commande (< 30s)
- [ ] Finaliser un worktree sans intervention manuelle complexe

### Technical Goals

- [ ] Zero modification des commandes EPCI existantes (integration par suggestion/hook)
- [ ] Scripts POSIX-compatible (bash)

---

## Non-Goals (Out of Scope v1)

**Explicitement NON inclus dans cette version** :

| Exclusion | Raison | Future Version |
|-----------|--------|----------------|
| Support hotfix/debug | Petits fix = develop direct | Non prevu |
| Tracking JSON custom | git worktree list suffit | Non prevu |
| UI graphique | CLI suffisant | v2 si demande |
| Merge strategies (rebase, squash) | Merge simple d'abord | v2 |

---

## Personas

### Persona Primaire — Developpeur EPCI

- **Role**: Developpeur utilisant le plugin EPCI pour Claude Code
- **Contexte**: Projets avec plusieurs features en parallele, workflow /brief -> /epci
- **Pain points**: Context switch couteux, branches polluees, perte de focus
- **Objectifs**: Isoler chaque feature dans son propre espace de travail
- **Quote**: "Je veux lancer une nouvelle feature sans casser celle en cours"

---

## Stack Detecte

- **Framework**: Plugin Claude Code (Markdown + Python)
- **Language**: Bash (scripts), Python (hooks optionnels)
- **Patterns**: Commands EPCI, Skills, Hooks system
- **Outils**: Git, Git worktree

## Exploration Summary

### Codebase Analysis

- **Structure**: Monorepo EPCI plugin
- **Architecture**: Commands (Markdown) + Scripts (Python) + Hooks
- **Test patterns**: pytest pour scripts Python

### Fichiers Potentiels

| Fichier | Action probable | Notes |
|---------|-----------------|-------|
| `src/scripts/worktree-create.sh` | Create | Script creation worktree |
| `src/scripts/worktree-finalize.sh` | Create | Script merge + cleanup |
| `src/scripts/worktree-abort.sh` | Create | Script cleanup sans merge |
| `src/commands/brief.md` | Modify | Ajouter suggestion worktree |
| `src/commands/epci.md` | Modify | Appel finalize en Phase 3 |
| `src/commands/quick.md` | Modify | Appel finalize en fin |

### Risques Identifies

- **Medium** : Conflits Git lors du merge (mitigation: abort + message)
- **Low** : Worktrees orphelins (mitigation: git worktree prune)

---

## User Stories

### US1 — Creer un worktree

**En tant que** developpeur EPCI,
**Je veux** creer un worktree isole pour une feature,
**Afin de** travailler sans impacter les autres branches.

**Acceptance Criteria:**
- [ ] Given je suis sur le repo EPCI, When je lance `./src/scripts/worktree-create.sh mon-slug`, Then un worktree est cree dans `~/worktrees/{projet}/mon-slug/`
- [ ] Given le worktree est cree, When je verifie, Then une branche `feature/mon-slug` existe depuis `develop`
- [ ] Given des fichiers .env existent, When le worktree est cree, Then ils sont copies dans le worktree

**Priorite**: Must-have
**Complexite**: M

### US2 — Finaliser un worktree

**En tant que** developpeur EPCI,
**Je veux** merger automatiquement mon worktree dans develop,
**Afin de** integrer ma feature sans manipulation Git complexe.

**Acceptance Criteria:**
- [ ] Given j'ai termine /epci ou /quick, When la Phase 3 se termine, Then worktree-finalize.sh est appele automatiquement
- [ ] Given le merge reussit, When finalize termine, Then le worktree est supprime
- [ ] Given un conflit existe, When finalize echoue, Then un message clair indique comment resoudre manuellement

**Priorite**: Must-have
**Complexite**: M

### US3 — Abandonner un worktree

**En tant que** developpeur EPCI,
**Je veux** supprimer un worktree sans merger,
**Afin de** annuler proprement une feature abandonnee.

**Acceptance Criteria:**
- [ ] Given j'ai un worktree actif, When je lance `worktree-abort.sh mon-slug`, Then le worktree est supprime
- [ ] Given j'ai une branche feature/mon-slug, When abort termine, Then la branche est supprimee

**Priorite**: Must-have
**Complexite**: S

### US4 — Suggestion dans /brief

**En tant que** developpeur EPCI,
**Je veux** voir une suggestion de creation worktree apres /brief,
**Afin de** savoir comment isoler ma feature.

**Acceptance Criteria:**
- [ ] Given /brief detecte STANDARD ou LARGE, When le routing s'affiche, Then une suggestion worktree-create.sh est affichee
- [ ] Given /brief detecte TINY ou SMALL, When le routing s'affiche, Then pas de suggestion worktree

**Priorite**: Should-have
**Complexite**: S

---

## Regles Metier

- **RM1**: Les worktrees sont crees uniquement pour features STANDARD/LARGE (pas debug/hotfix)
- **RM2**: La branche de base est toujours `develop` (GitFlow)
- **RM3**: En cas de conflit merge, abort et message (pas de resolution auto)
- **RM4**: Les fichiers .env/.envrc sont copies automatiquement dans le worktree

## Cas Limites & Edge Cases

| Cas | Comportement attendu |
|-----|---------------------|
| Worktree deja existant pour ce slug | Erreur + message "worktree existe deja" |
| Branche develop inexistante | Erreur + message "branche develop requise" |
| Fichiers non commites dans worktree | Erreur finalize + message "commiter d'abord" |
| Dossier ~/worktrees/ inexistant | Creation automatique |

## Success Metrics

| Metrique | Baseline | Cible | Methode de mesure |
|----------|----------|-------|-------------------|
| Temps creation worktree | N/A | < 30s | Timing script |
| Taux succes finalize | N/A | > 90% | Logs |

---

## User Flow

### Current Experience (As-Is)

```
/brief "feature"
       |
       v
  Routing STANDARD
       |
       v
  /epci sur branche actuelle
       |
       v
  Risque: modifications croisees
```

### Proposed Experience (To-Be)

```
/brief "feature"
       |
       v
  Routing STANDARD
       |
       v
  Suggestion: ./src/scripts/worktree-create.sh slug
       |
       v (manuel)
  cd ~/worktrees/projet/slug && claude
       |
       v
  /epci (isole)
       |
       v (auto)
  worktree-finalize.sh → merge develop + cleanup
```

### Key Improvements

| Pain Point Actuel | Solution Proposee | Impact |
|-------------------|-------------------|--------|
| Context switch couteux | Worktree isole | -10 min/switch |
| Branches polluees | Feature isolee | Code plus propre |
| Conflits multi-features | Isolation totale | Zero conflit pendant dev |

---

## Contraintes Techniques Identifiees

| Contrainte | Impact | Mitigation |
|------------|--------|------------|
| Git worktree = meme branche interdite dans 2 worktrees | Faible | Git le gere nativement |
| Dossier worktree doit etre hors du repo | Moyen | Path ~/worktrees/ |

## Dependances

- **Internes**: /brief (suggestion), /epci + /quick (appel finalize)
- **Externes**: Git >= 2.5 (worktree support)

## Assumptions

- [x] **Technical** : Git 2.5+ disponible (worktree support)
- [x] **Technical** : Branche `develop` existe dans le repo
- [x] **User** : Utilisateur comprend le concept worktree (ou suit la doc)
- [x] **Resources** : Scripts bash POSIX-compatible

---

## Criteres d'Acceptation Globaux

- [ ] Scripts executables (chmod +x)
- [ ] Messages d'erreur clairs en francais
- [ ] Pas de modification destructive sans confirmation
- [ ] Compatible Linux/macOS (POSIX)

## Questions Ouvertes

- [ ] Faut-il supporter Windows (Git Bash) ?
- [ ] Notification post-finalize (email/slack) ?

## FAQ

### Internal FAQ (Equipe)

**Q: Pourquoi 3 scripts et pas une seule commande EPCI ?**
A: Simplicite et decouplage. Les scripts sont independants du workflow EPCI et peuvent etre utilises manuellement.

**Q: Pourquoi ~/worktrees/ et pas ./worktrees/ ?**
A: Evite d'avoir un sous-dossier git dans le repo, plus propre pour .gitignore.

**Q: Et si develop n'existe pas ?**
A: Le script echoue avec un message clair. L'utilisateur doit creer develop d'abord.

### External FAQ (Utilisateurs)

**Q: Dois-je utiliser les worktrees pour toutes mes features ?**
A: Non, uniquement recommande pour STANDARD/LARGE. TINY/SMALL peuvent rester sur develop.

**Q: Puis-je avoir plusieurs worktrees en parallele ?**
A: Oui, c'est le cas d'usage principal. Chaque feature = un worktree.

---

## Estimation Preliminaire

| Metrique | Valeur |
|----------|--------|
| Complexite estimee | SMALL |
| Fichiers impactes | ~6 |
| Risque global | Low |

---

## Timeline & Milestones

### Target Launch

**Objectif** : TBD

### Key Milestones

| Milestone | Target Date | Owner | Status |
|-----------|-------------|-------|--------|
| PRD Review Complete | TBD | EPCI Team | In Progress |
| Scripts Development | TBD | Dev | Not Started |
| Integration /brief | TBD | Dev | Not Started |
| Integration /epci + /quick | TBD | Dev | Not Started |
| Documentation | TBD | Dev | Not Started |

### Phasing Strategy

**Phase 1 (MVP)** : US1 + US2 + US3 (3 scripts fonctionnels)
**Phase 2** : US4 (integration suggestions /brief)
**Phase 3** : Integration auto fin /epci et /quick

---

## Risques (Pre-mortem)

| Risque | Probabilite | Impact | Mitigation |
|--------|-------------|--------|------------|
| Conflits Git lors merge | Medium | Medium | Abort + message clair |
| Worktrees orphelins | Low | Low | git worktree prune |
| Utilisateur oublie de finalize | Medium | Low | Documentation + suggestion |

---

*PRD pret pour EPCI — Lancer `/brief` avec ce contenu.*
*Details du processus de brainstorming dans le Journal d'Exploration.*
