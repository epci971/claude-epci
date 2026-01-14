# Journal d'Exploration — Worktree Integration EPCI

> **Feature**: Worktree Integration EPCI
> **Date**: 2026-01-14
> **Iterations**: 4

---

## Resume

Exploration de l'integration des Git worktrees dans le plugin EPCI. Apres recherche web et analyse du codebase existant, convergence vers une solution simple : 3 scripts bash (create/finalize/abort) avec suggestions dans /brief et appel automatique en fin de workflow /epci et /quick. Scope limite aux features STANDARD/LARGE.

## Progression EMS

| Iteration | Score | Delta | Focus |
|-----------|-------|-------|-------|
| Init | 22 | - | Cadrage initial, recherche web |
| 1 | 38 | +16 | Trigger et finalize definis |
| 2 | 52 | +14 | Configuration technique |
| 3 | 68 | +16 | Path, base branch, setup |
| Final | 78 | +10 | Abandon handling, tracking |

## EMS Final Detaille

| Axe | Score | Poids |
|-----|-------|-------|
| Clarte | 90/100 | 25% |
| Profondeur | 70/100 | 20% |
| Couverture | 80/100 | 20% |
| Decisions | 85/100 | 20% |
| Actionnabilite | 75/100 | 15% |

## Metadonnees Brainstormer

| Metrique | Valeur |
|----------|--------|
| Version | v5.2 |
| Template | feature |
| Techniques appliquees | Aucune (flow naturel) |
| Duree exploration | ~15min |

## Sources Web

- [Git Worktree Documentation](https://git-scm.com/docs/git-worktree)
- [Git Worktree Best Practices](https://gist.github.com/ChristopherA/4643b2f5e024578606b9cd5d2e6815cc)
- [Using Git Worktrees with AI Agents](https://www.nrmitchi.com/2025/10/using-git-worktrees-for-multi-feature-development-with-ai-agents/)
- [Git Worktrees for Fun and Profit](https://blog.safia.rocks/2025/09/03/git-worktrees/)

## Document Existant Analyse

- `/home/epci/apps/claude-epci/docs/guidelines/worktrees.md` - Guide complet pre-existant (620 lignes)

## Decisions Cles

### Decision 1 — Architecture 3 scripts vs Hooks

- **Contexte**: Choisir entre integration via hooks EPCI ou scripts independants
- **Options considerees**: (A) 4 hooks Python, (B) 2 scripts bash, (C) 3 scripts bash
- **Choix**: C - 3 scripts bash (create, finalize, abort)
- **Justification**: Plus simple, decouples du workflow EPCI, utilisables manuellement

### Decision 2 — Trigger worktree-create

- **Contexte**: Comment declencher la creation du worktree
- **Options considerees**: (A) Auto dans /brief, (B) Hook post-brief, (C) Manuel avec suggestion
- **Choix**: C - Manuel avec suggestion dans /brief
- **Justification**: Controle utilisateur, pas de side-effect automatique

### Decision 3 — Trigger worktree-finalize

- **Contexte**: Quand declencher la finalisation
- **Options considerees**: (A) Dans /commit, (B) Fin /epci et /quick, (C) Manuel
- **Choix**: B - Fin /epci et /quick (auto)
- **Justification**: /commit n'est pas obligatoire, fin de workflow = moment logique

### Decision 4 — Path des worktrees

- **Contexte**: Ou creer physiquement les worktrees
- **Options considerees**: (A) Adjacent au projet, (B) Sous-dossier ./worktrees/, (C) ~/worktrees/
- **Choix**: C - ~/worktrees/{projet}/{slug}/
- **Justification**: Centralise, propre, pas de .gitignore

### Decision 5 — Scope

- **Contexte**: Quelles operations supportent les worktrees
- **Options considerees**: (A) Toutes, (B) Features + debug, (C) Features STANDARD/LARGE uniquement
- **Choix**: C - Features STANDARD/LARGE uniquement
- **Justification**: Debug/hotfix = petits fix rapides sur develop

### Decision 6 — Gestion conflits

- **Contexte**: Comportement en cas de conflit lors du merge
- **Options considerees**: (A) Resolution auto, (B) Ouvrir mergetool, (C) Abort + message
- **Choix**: C - Abort + message
- **Justification**: Safe, l'utilisateur garde le controle

### Decision 7 — Tracking worktrees

- **Contexte**: Faut-il un fichier de tracking custom
- **Options considerees**: (A) JSON custom, (B) Dans .project-memory/, (C) git worktree list
- **Choix**: C - git worktree list (natif Git)
- **Justification**: Pas de duplication, commande standard

## Questions Resolues

| Question | Reponse | Iteration |
|----------|---------|-----------|
| Trigger create? | Manuel + suggestion /brief | 1 |
| Trigger finalize? | Auto fin /epci et /quick | 1 |
| Scope debug/hotfix? | Exclus (develop direct) | 1 |
| Actions finalize? | Merge develop + supprimer worktree | 2 |
| Gestion conflits? | Abort + message | 2 |
| Location scripts? | src/scripts/ | 2 |
| Path worktrees? | ~/worktrees/{projet}/{slug}/ | 3 |
| Branche base? | develop | 3 |
| Fichiers a copier? | .env, .envrc | 3 |
| Abandon worktree? | Script worktree-abort.sh | 4 |
| Tracking? | git worktree list (natif) | 4 |

---

*Journal genere automatiquement par Brainstormer v5.2*
