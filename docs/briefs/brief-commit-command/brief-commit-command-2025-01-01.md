# Brief Fonctionnel — Commande `/commit` unifiée

> **Date** : 2025-01-01
> **Source** : Brainstorm session
> **EMS Final** : 75/100

---

## 1. Contexte

Actuellement, la logique de commit est **dupliquée** entre `/epci` (Phase 3) et `/quick`, tandis que `/debug` n'a pas de commit intégré. Cette fragmentation pose des problèmes de maintenance et d'incohérence.

## 2. Objectif

Créer une commande `/commit` unifiée qui :
- Centralise toute la logique de commit Git
- Est appelable par `/epci`, `/quick` et `/debug`
- Peut être invoquée standalone par l'utilisateur

## 3. Spécifications Fonctionnelles

### 3.1 Invocation

| Mode | Description |
|------|-------------|
| **Intégré** | Proposé automatiquement en fin de workflow `/epci`, `/quick`, `/debug --commit` |
| **Standalone** | Lancé manuellement via `/commit` |

### 3.2 Contexte de Communication

**Fichier pont** : `.epci-commit-context.json` (racine du projet)

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

### 3.3 Modes de Fonctionnement

| Mode | Condition | Comportement |
|------|-----------|--------------|
| **Contexte riche** | `.epci-commit-context.json` présent | Utilise le contexte, propose message |
| **Dégradé** | Pas de fichier contexte | Détecte fichiers modifiés, demande type + description |

### 3.4 Breakpoint PRE-COMMIT

- **Par défaut** : Affiche le message proposé, attend confirmation
- **Bypass** : Si flag `--turbo` ou `--auto-commit` → commit direct

### 3.5 Message de Commit

- **Génération hybride** : Le workflow appelant propose un message dans le contexte
- `/commit` peut le modifier si l'utilisateur le souhaite
- Format : Conventional Commits (`type(scope): description`)

### 3.6 Hooks

Réutilisation des hooks existants :
- `pre-commit` → Avant exécution git commit
- `post-commit` → Après commit réussi

### 3.7 Cleanup

- Suppression de `.epci-commit-context.json` après commit réussi
- Évite les commits accidentels avec un vieux contexte

### 3.8 Gestion des Erreurs

- Afficher l'erreur git clairement
- Proposer des suggestions de résolution
- Laisser l'utilisateur décider de la suite

## 4. Modifications des Workflows Existants

### 4.1 `/epci` (Phase 3)

- Supprimer la logique de commit inline
- Générer `.epci-commit-context.json` avec contexte complet
- Proposer : "Lancer /commit pour finaliser ?"

### 4.2 `/quick`

- Supprimer la logique de commit inline
- Générer `.epci-commit-context.json`
- En mode `--turbo` : appeler `/commit --auto-commit`

### 4.3 `/debug`

- Ajouter flag `--commit` optionnel
- Si activé : générer contexte JSON + proposer `/commit`

## 5. Flags Supportés

| Flag | Effet |
|------|-------|
| `--auto-commit` | Skip breakpoint, commit direct |
| `--amend` | Amend le dernier commit |
| `--no-hooks` | Skip pre/post-commit hooks |
| `--dry-run` | Affiche ce qui serait fait sans exécuter |

## 6. Fichiers à Créer/Modifier

| Action | Fichier |
|--------|---------|
| **Créer** | `src/commands/commit.md` |
| **Modifier** | `src/commands/epci.md` (Phase 3) |
| **Modifier** | `src/commands/quick.md` |
| **Modifier** | `src/commands/debug.md` |
| **Optionnel** | `src/skills/core/git-workflow/SKILL.md` (si enrichissement) |

## 7. Critères de Succès

- [ ] `/commit` fonctionne en standalone (mode dégradé)
- [ ] `/commit` fonctionne avec contexte JSON
- [ ] `/epci` délègue le commit à `/commit`
- [ ] `/quick` délègue le commit à `/commit`
- [ ] `/debug --commit` fonctionne
- [ ] Hooks pre/post-commit déclenchés
- [ ] Cleanup du fichier JSON après commit

## 8. Exploration Summary

| Élément | Détail |
|---------|--------|
| **Stack** | Markdown commands, Python hooks |
| **Patterns** | Conventional Commits, Breakpoints, Hooks system |
| **Skill existant** | `git-workflow` (standards, pas d'exécution) |
| **Fichiers candidats** | `src/commands/commit.md` (nouveau), `epci.md`, `quick.md`, `debug.md` |

---

> **Prochaine étape** : `/brief` avec ce document pour lancer l'implémentation
