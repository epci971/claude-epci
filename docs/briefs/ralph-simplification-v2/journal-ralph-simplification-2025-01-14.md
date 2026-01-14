# Journal d'Exploration — Ralph Simplification v2

> **Session** : 2025-01-14 | **EMS Final** : 85/100 | **Iterations** : 8

---

## Résumé de la session

Refonte complète du système Ralph Wiggum pour simplifier l'architecture et permettre la libération du contexte entre chaque story. La session a abouti à la suppression de 2 commandes et 1 agent, remplacés par une unique commande `/ralph-exec`.

---

## Chronologie des découvertes

### Iteration 1 — Analyse initiale

**Input utilisateur** : Refonte du système Ralph, trop compliqué avec /brief et /epci.

**Actions** :
- Exploration du codebase Ralph existant (@Explore)
- Lecture du prd.json actuel (45 stories)
- Analyse du PROMPT.md

**Découvertes** :
- Le système actuel route vers `/brief` → `/quick` ou `/epci`
- 45 user stories pour une intégration — trop granulaire
- PROMPT.md référence explicitement /quick et /epci (lignes 60-61)

### Iteration 2 — Recherche web

**Actions** :
- Recherche sur le plugin officiel Ralph Wiggum d'Anthropic
- Analyse du Ralph Orchestrator (mikeyobrien)
- Étude des patterns TDD dans Claude Code

**Découvertes** :
- Pattern officiel ultra-simple : `while :; do cat PROMPT.md | claude-code ; done`
- Completion promise : `<promise>COMPLETE</promise>`
- Le workflow "Explore, Plan, Code, Commit" est recommandé par Anthropic

### Iteration 3 — Clarification granularité

**Question** : Une story = une itération ?

**Décision** : Oui, pour libérer le contexte.

**Justification** : Chaque appel Claude séparé = contexte frais = pas de dépassement mémoire.

### Iteration 4 — Boucle Code-Test

**Question** : Comment gérer le cycle Code → Test ?

**Options analysées** :
- A) Boucle interne Claude (prompt instruction)
- B) Boucle shell explicite
- C) Hybride

**Décision** : Option A — Boucle interne avec max 5 tentatives.

**Justification** : Simple, tout dans une invocation, Claude voit l'erreur immédiatement.

### Iteration 5 — PROMPT.md vs Commande

**Question clé** : Un PROMPT.md peut-il utiliser des skills et agents ?

**Analyse** :
- PROMPT.md = texte statique, ne peut pas invoquer de skills
- Commande = accès aux agents (@planner, @implementer), skills, hooks

**Décision** : Créer une commande `/ralph-exec`.

### Iteration 6 — Analyse des commandes existantes

**Fichiers analysés** :
- `/ralph` (src/commands/ralph.md)
- `/cancel-ralph` (src/commands/cancel-ralph.md)
- `@ralph-executor` (src/agents/ralph-executor.md)

**Découvertes** :
- `/ralph` mode Hook jamais testé en production
- `@ralph-executor` ligne 82-103 : route explicitement vers /brief → /epci
- `/cancel-ralph` fait essentiellement ce que Ctrl+C fait

### Iteration 7 — Insight libération contexte

**Question utilisateur** : "Comment /ralph peut libérer le contexte si c'est une commande Claude ?"

**Insight majeur** :
- Si on lance `/ralph` (commande Claude), le contexte reste ouvert !
- Seul `./ralph.sh` (terminal bash) permet des appels séparés

**Décision pivot** : Supprimer `/ralph` complètement.

### Iteration 8 — Architecture finale

**Décision finale** :
- **GARDER** : `/decompose` (génère tout)
- **CRÉER** : `/ralph-exec` (workflow EPCT inline)
- **SUPPRIMER** : `/ralph`, `/cancel-ralph`, `@ralph-executor`

---

## Décisions clés

| # | Décision | Justification | Alternatives rejetées |
|---|----------|---------------|----------------------|
| 1 | Une story = une itération | Libération contexte | Toutes stories en bloc |
| 2 | Boucle Code-Test interne | Simplicité | Boucle shell explicite |
| 3 | Promise tag simple | `<promise>STORY_DONE</promise>` | RALPH_STATUS complexe |
| 4 | Commande /ralph-exec | Accès agents/skills | PROMPT.md statique |
| 5 | Supprimer /ralph | Ne libère pas le contexte | Simplifier /ralph |
| 6 | Supprimer /cancel-ralph | Ctrl+C suffit | Garder pour UX |

---

## Questions résolues

| Question | Réponse |
|----------|---------|
| Comment libérer le contexte ? | Lancer ralph.sh depuis le terminal, pas via /ralph |
| PROMPT.md ou commande ? | Commande pour accès aux agents |
| Quelle granularité ? | Une story par itération |
| Combien de tentatives Code-Test ? | 5 max (configurable) |
| Comment gérer les dépendances bloquantes ? | Skip et marquer blocked, continuer aux autres |
| Où stocker le workflow EPCT ? | Dans /ralph-exec (la commande) |

---

## Axes EMS (score final)

| Axe | Score | Commentaire |
|-----|-------|-------------|
| Clarté du problème | 95 | Très bien défini |
| Solution proposée | 90 | Architecture simple et cohérente |
| Faisabilité technique | 85 | Dépend de la libération contexte réelle |
| Couverture des cas | 80 | Cas d'erreur bien couverts |
| Documentation | 85 | Brief complet avec specs techniques |

**EMS Total** : 85/100

---

## Risques identifiés

| Risque | Probabilité | Impact | Mitigation |
|--------|-------------|--------|------------|
| `claude "/ralph-exec"` ne libère pas vraiment le contexte | Medium | High | Tester avec 3+ stories avant production |
| @planner/@implementer pas invocables depuis /ralph-exec | Low | Medium | Tester l'invocation subagents |
| prd.json corrompu en cas d'interruption | Low | Medium | Backup avant chaque modification |

---

## Apprentissages

1. **Simplicité > Fonctionnalités** : Le système v1 était trop ambitieux (45 stories, 2 modes, 3 commandes)

2. **Libération contexte = terminal** : Une commande Claude ne peut pas libérer son propre contexte

3. **PROMPT.md limité** : Un fichier texte ne peut pas invoquer de skills/agents

4. **Claude Code 2.1** : Hot-reload et fusion skills/commands simplifient l'approche

---

## Prochaines étapes recommandées

1. **Implémenter /ralph-exec** avec workflow EPCT inline
2. **Modifier /decompose** pour générer ralph.sh compatible
3. **Supprimer** `/ralph`, `/cancel-ralph`, `@ralph-executor`
4. **Tester** avec 3+ stories pour valider libération contexte
5. **Mettre à jour** CLAUDE.md et documentation

---

## Métriques de session

| Métrique | Valeur |
|----------|--------|
| Durée estimée | ~45 min |
| Iterations | 8 |
| Fichiers analysés | 12 |
| Recherches web | 4 |
| Agents invoqués | @Explore |
| Questions posées | 11 |

---

*Journal généré par /brainstorm — 2025-01-14*
