# Journal Brainstorm — Commande `/commit` unifiée

> **Date** : 2025-01-01
> **Durée** : 4 itérations
> **EMS Final** : 75/100

---

## Historique des Itérations

### Iteration 1 — Cadrage Initial
**Phase** : Divergent | **Persona** : Architecte | **EMS** : 25/100

**Exploration codebase** :
- `/epci` : commit intégré en Phase 3 avec breakpoint
- `/quick` : commit intégré avec auto-commit en turbo
- `/debug` : pas de commit natif
- Skill `git-workflow` existe (standards, pas d'exécution)

**Questions posées** :
1. Invocation → **Réponse : c)** Dual (proposé + standalone)
2. Contexte transmis → **Réponse : b)** Contexte complet
3. Breakpoint → **Réponse : b)** Skip si turbo/auto-commit
4. Scope debug → **Réponse : c)** Optionnel via flag

---

### Iteration 2 — Architecture
**Phase** : Divergent | **Persona** : Architecte | **EMS** : 45/100

**Décisions actées** :
- `/commit` callable standalone OU proposé par workflows
- Contexte complet transmis (Feature Doc, type, scope)
- Breakpoint skip si `--turbo` ou `--auto-commit`
- `/debug` → flag `--commit` optionnel

**Questions posées** :
1. Format contexte → **Réponse : b)** Fichier JSON temporaire
2. Mode standalone → **Réponse : c)** Intelligent (JSON ou dégradé)
3. Génération message → **Réponse : c)** Hybride
4. Hooks → **Réponse : a)** Réutiliser existants

---

### Iteration 3 — Convergence
**Phase** : Convergent | **Persona** : Architecte | **EMS** : 65/100

**Structure JSON définie** :
```json
{
  "source": "epci|quick|debug",
  "type": "feat|fix|...",
  "scope": "module-name",
  "description": "what was done",
  "files": ["..."],
  "featureDoc": "path/...",
  "breaking": false,
  "ticket": "JIRA-123"
}
```

**Décisions actées** :
- Mode dégradé : minimal (type + description)
- Erreurs : afficher + suggestions
- Cleanup : supprimer JSON après commit

---

### Iteration 4 — Validation Finale
**Phase** : Convergent | **Persona** : Architecte | **EMS** : 75/100

**Question utilisateur** : "Pourquoi JSON vs Feature Document ?"

**Réponse** :
- Feature Doc = Markdown, difficile à parser
- `/quick` et `/debug` n'ont pas toujours de Feature Doc
- JSON = bridge universel, léger, éphémère

**Stockage décidé** : `.epci-commit-context.json` à la racine projet

---

## Décisions Clés

| Sujet | Décision | Raison |
|-------|----------|--------|
| Invocation | Dual (intégré + standalone) | Flexibilité maximale |
| Format contexte | JSON temporaire | Universel, parsable |
| Breakpoint | Conditionnel | UX adaptative |
| Debug commit | Flag optionnel | Non-intrusif |
| Cleanup | Suppression après commit | Évite vieux contexte |

## Points Non Résolus

*Aucun — brief prêt pour implémentation*

---

## Métriques

| Métrique | Valeur |
|----------|--------|
| Itérations | 4 |
| EMS Départ | 25/100 |
| EMS Final | 75/100 |
| Questions résolues | 12 |
| Fichiers identifiés | 5 |
