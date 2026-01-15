# Resume et Completion — Detail

> Reference pour `/quick` — Formats de sortie et hooks memoire

---

## Resume Final (MANDATORY)

**⚠️ OBLIGATOIRE:** Toujours afficher le message de completion.

### Generer le Contexte Commit

**Avant d'afficher la completion, generer `.epci-commit-context.json`:**

```json
{
  "source": "quick",
  "type": "feat|fix",
  "scope": "<module detecte>",
  "description": "<depuis description brief>",
  "files": ["<liste des fichiers modifies>"],
  "featureDoc": null,
  "breaking": false,
  "ticket": null
}
```

---

## Sortie Mode TINY

```markdown
┌─────────────────────────────────────────────────────────────────────┐
│ ✅ QUICK COMPLETE — TINY                                            │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│ Fichier modifie: `{chemin/vers/fichier.ext}`                       │
│ Changement: {description}                                          │
│ Lignes: +{X} / -{Y}                                                │
│                                                                     │
│ Temps total: {N}s                                                  │
│ Session: .project-memory/sessions/quick-{timestamp}.json           │
│                                                                     │
│ 📝 Contexte commit prepare → /commit                               │
│    (ou /commit --auto-commit pour commit direct)                   │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Sortie Mode SMALL

```markdown
┌─────────────────────────────────────────────────────────────────────┐
│ ✅ QUICK COMPLETE — SMALL                                           │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│ Fichiers modifies:                                                 │
│ ├── `{chemin/vers/fichier1.ext}` (+{X} / -{Y})                    │
│ ├── `{chemin/vers/fichier2.ext}` (+{Z} / -{W})                    │
│ └── `{chemin/vers/fichier3.ext}` (+{A} / -{B})                    │
│                                                                     │
│ Tests: {N} reussis                                                 │
│ Temps total: {N}s                                                  │
│ Session: .project-memory/sessions/quick-{timestamp}.json           │
│                                                                     │
│ 📝 Contexte commit prepare → /commit                               │
│    (ou /commit --auto-commit pour commit direct)                   │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Mise a Jour Memoire (MANDATORY)

**⚠️ CRITIQUE: Toujours executer ce hook apres affichage du message de completion.**

Apres chaque completion reussie de `/quick`, vous DEVEZ executer le hook `post-phase-3` pour sauvegarder l'historique de la feature:

```bash
python3 src/hooks/runner.py post-phase-3 --context '{
  "phase": "quick-complete",
  "feature_slug": "<brief-slug>",
  "complexity": "<TINY|SMALL>",
  "files_modified": ["<liste des fichiers modifies>"],
  "loc_added": <nombre>,
  "loc_removed": <nombre>,
  "estimated_time": null,
  "actual_time": "<duree en secondes>s",
  "commit_hash": null,
  "commit_status": "pending",
  "test_results": {"status": "<passed|skipped>", "count": <n>}
}'
```

**Pourquoi c'est obligatoire:**
- Met a jour `.project-memory/history/features/` avec l'enregistrement de la feature
- Active le suivi de velocite et la calibration
- Maintient l'historique des features pour la commande `/memory`
- Requis pour des metriques projet precises

**Note:** SI le flag `--no-hooks` est actif, ignorer cette etape.

---

## Finalisation Worktree (CONDITIONNEL)

**Condition:** Executer uniquement SI le repertoire courant est un worktree.

**Detection:**
```bash
# Verifier si dans un worktree (git-dir contient "worktrees")
git rev-parse --git-dir 2>/dev/null | grep -q "worktrees"
```

**SI dans un worktree:**

Afficher le prompt de finalisation worktree:
```
┌─────────────────────────────────────────────────────────────────────┐
│ 🌳 WORKTREE DETECTE                                                  │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│ Feature complete dans worktree: {slug}                              │
│                                                                     │
│ Pour merger dans develop et nettoyer:                               │
│   ./src/scripts/worktree-finalize.sh                                │
│                                                                     │
│ Pour abandonner le worktree:                                        │
│   ./src/scripts/worktree-abort.sh                                   │
│                                                                     │
│ Pour garder le worktree ouvert:                                     │
│   (aucune action requise)                                           │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

**SI PAS dans un worktree:** Ignorer cette section silencieusement.

---

*Reference Resume Completion — /quick command*
