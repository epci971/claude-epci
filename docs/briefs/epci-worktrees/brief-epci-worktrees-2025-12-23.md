# Brief Fonctionnel — EPCI Worktrees Integration

> **Genere par**: Brainstormer v3.0
> **Template**: feature
> **EMS Final**: 85/100
> **Date**: 2025-12-23
> **Slug**: epci-worktrees

---

## Contexte

Les workflows EPCI (STANDARD/LARGE) impliquent des modifications significatives du codebase sur plusieurs phases. Actuellement, toutes les modifications s'effectuent dans le repertoire principal, ce qui empeche:
- L'execution de plusieurs workflows EPCI en parallele
- L'isolation des changements experimentaux
- La possibilite de continuer le developpement pendant qu'un workflow EPCI est en cours

Git worktrees permet de creer des copies de travail isolees partageant le meme historique git. L'integration dans EPCI automatiserait la creation/gestion de ces espaces de travail.

## Objectif

Integrer le systeme de git worktrees dans EPCI pour permettre l'execution de chaque workflow STANDARD/LARGE dans un espace de travail isole, avec:
- Creation automatique du worktree au demarrage
- Setup automatique de l'environnement (npm install, etc.)
- Cleanup assiste en fin de workflow
- Fallback gracieux si worktree impossible

## Stack Detecte

- **Framework**: claude-code-plugin v3.5.0
- **Language**: Markdown (skills/commands) + Python (scripts)
- **Patterns**: skill-pattern, command-pattern, hook-pattern
- **Outils**: git worktree, package managers (npm/yarn/pip/cargo)

## Specifications Fonctionnelles

### SF1 — Creation automatique du worktree

A l'execution de `/epci-brief` pour une feature STANDARD/LARGE, si `worktree.enabled = true`:

1. Detecter le nom du projet (`basename $(git rev-parse --show-toplevel)`)
2. Generer le slug depuis le titre de la feature
3. Creer la branche: `feature/<slug>`
4. Creer le worktree: `git worktree add ../<project>-feature-<slug> -b feature/<slug>`
5. Enregistrer dans `.project-memory/worktrees.json`
6. Afficher confirmation avec chemin absolu

**Contraintes**:
- Si branche existe: demander confirmation de reutilisation
- Si worktree dir existe avec meme branche: reutiliser sans recreer
- Si erreur: fallback sur repo principal avec warning

### SF2 — Setup automatique de l'environnement

Apres creation du worktree, si `worktree.autoSetup = true`:

1. Detecter le package manager (priorite conventions.json, sinon auto-detect)
2. Executer la commande appropriee:
   - `package-lock.json` → `npm install`
   - `yarn.lock` → `yarn install`
   - `pnpm-lock.yaml` → `pnpm install`
   - `requirements.txt` → `pip install -r requirements.txt`
   - `Cargo.toml` → `cargo build`
   - `go.mod` → `go mod download`
3. Si `worktree.runTestsOnSetup = true`: lancer les tests de base
4. Timeout 60s avec fallback

**Contraintes**:
- Override possible via `conventions.json > setupCommand`
- Logs explicites en cas d'echec
- Ne pas bloquer le workflow si setup echoue

### SF3 — Tracking des worktrees actifs

Maintenir un fichier `.project-memory/worktrees.json`:

```json
{
  "active": [
    {
      "slug": "user-auth",
      "branch": "feature/user-auth",
      "path": "../myproject-feature-user-auth",
      "absolutePath": "/home/user/projects/myproject-feature-user-auth",
      "createdAt": "2025-12-23T10:30:00Z",
      "phase": "phase-2",
      "featureDoc": "docs/features/user-auth.md"
    }
  ]
}
```

**Reconciliation**: Au demarrage de tout workflow EPCI, comparer avec `git worktree list` et nettoyer les entrees orphelines.

### SF4 — Affichage contexte dans breakpoints

Chaque breakpoint EPCI doit afficher le contexte worktree:

```
┌─────────────────────────────────────────────────────────────────────┐
│ ⏸️  BREAKPOINT PHASE 2 — Code Implemente                            │
├─────────────────────────────────────────────────────────────────────┤
│ 📍 WORKTREE: ../myproject-feature-user-auth                        │
│ 🌿 BRANCH: feature/user-auth                                       │
├─────────────────────────────────────────────────────────────────────┤
│ ...                                                                 │
```

### SF5 — Cleanup assiste en fin de workflow

Au breakpoint final de Phase 3, si worktree actif:

```
┌─────────────────────────────────────────────────────────────────────┐
│ 🧹 WORKTREE CLEANUP                                                 │
├─────────────────────────────────────────────────────────────────────┤
│ Worktree: ../myproject-feature-user-auth                           │
│ Branch: feature/user-auth                                          │
│ Cree: 2025-12-23 10:30                                             │
│ Fichiers modifies: 12                                              │
├─────────────────────────────────────────────────────────────────────┤
│ Options:                                                            │
│   [1] Supprimer worktree + garder branche (recommande)             │
│   [2] Supprimer worktree + supprimer branche                       │
│   [3] Garder worktree (cleanup manuel plus tard)                   │
└─────────────────────────────────────────────────────────────────────┘
```

### SF6 — Commande /epci:cleanup

Nouvelle commande pour gestion batch des worktrees:

```
/epci:cleanup
```

Fonctionnalites:
- Lister tous les worktrees EPCI actifs
- Afficher age et derniere activite
- Proposer suppression selective ou batch
- Reconcilier worktrees.json avec `git worktree list`

### SF7 — Gestion du --continue

Quand `/epci --continue` est invoque:

1. Lire worktrees.json pour le slug courant
2. Verifier que le worktree existe (`git worktree list`)
3. Si existe: cd automatique dans le worktree
4. Si n'existe plus: continuer dans repo principal avec warning

## Regles Metier

- **RM1**: Worktree desactive par defaut (`enabled: false`)
- **RM2**: Feature Document toujours dans le repo principal (pas dans worktree)
- **RM3**: Branche prefixee `feature/` par defaut, configurable
- **RM4**: Maximum 5 worktrees actifs simultanement (warning au-dela)
- **RM5**: Worktree inactif > 7 jours → notification au prochain /epci-brief

## Cas Limites & Edge Cases

| Cas | Comportement attendu |
|-----|---------------------|
| Branche existe deja | Demander confirmation reutilisation |
| Worktree dir existe (meme branche) | Reutiliser, skip creation |
| Worktree dir existe (autre branche) | Abort avec message explicite |
| Setup timeout > 60s | Warning + proposer skip |
| Git worktree non supporte | Fallback repo principal |
| Disque plein | Abort avec message explicite |
| Meme slug 2x en 24h | Demander confirmation |

## Hors Scope (v1)

- Integration CI/CD (worktrees locaux uniquement)
- Sync automatique avec remote
- Merge automatique de la branche
- Support worktrees imbriques
- GUI/visualisation des worktrees

## Contraintes Techniques Identifiees

| Contrainte | Impact | Mitigation |
|------------|--------|------------|
| Git version < 2.5 | Worktrees non supportes | Detection version + fallback |
| Windows paths | Comportement different `../` | Utiliser paths absolus internement |
| Sparse checkout | Incompatible worktrees | Detecter et warn |

## Dependances

- **Internes**:
  - `epci-brief.md` (point de creation)
  - `epci.md` (breakpoints + cleanup)
  - `project-memory/` (settings, worktrees.json)
  - `git-workflow/` skill (patterns git)

- **Externes**:
  - Git >= 2.5
  - Package managers (npm, yarn, pip, cargo, etc.)

## Criteres d'Acceptation

- [ ] Setting `worktree.enabled` dans settings.json
- [ ] Creation worktree automatique si enabled + STANDARD/LARGE
- [ ] Auto-detection package manager et setup
- [ ] Fallback gracieux si creation echoue
- [ ] Tracking dans worktrees.json
- [ ] Affichage contexte worktree dans breakpoints
- [ ] Cleanup assiste en Phase 3
- [ ] Commande /epci:cleanup fonctionnelle
- [ ] --continue detecte et utilise worktree existant
- [ ] Reconciliation worktrees.json ↔ git worktree list

## Questions Ouvertes

> Aucune — tous les points ont ete clarifies pendant l'exploration.

## Estimation Preliminaire

| Metrique | Valeur |
|----------|--------|
| Complexite estimee | STANDARD |
| Fichiers impactes | 6 (3 create, 3 modify) |
| Risque | Medium |

---

## Risques (Pre-mortem)

| Risque | Score | Mitigation |
|--------|-------|------------|
| Worktrees orphelins s'accumulent | 6 | /epci:cleanup + reminder 7 jours |
| Setup echoue silencieusement | 6 | Timeout + logs + fallback auto |
| Confusion chemin relatif | 6 | Afficher contexte dans tous breakpoints |
| Desync worktrees.json ↔ git | 4 | Auto-reconciliation au demarrage |
| Overhead percu trop eleve | 4 | Desactive par defaut, doc claire |

---

## EMS Final

Score: 85/100 🎯

| Axe | Score |
|-----|-------|
| Clarte | 90/100 |
| Profondeur | 85/100 |
| Couverture | 85/100 |
| Decisions | 90/100 |
| Actionnabilite | 75/100 |

---

## Metadonnees Brainstormer

| Metrique | Valeur |
|----------|--------|
| Iterations | 6 |
| EMS Final | 85/100 |
| Template | feature |
| Frameworks utilises | Pre-mortem |
| Duree exploration | ~15min |

---

*Brief pret pour EPCI — Commande suggeree: `/epci-brief` ou `/epci`*
