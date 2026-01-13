# PRD — Intégration Ralph Wiggum dans EPCI

| Metadata | Value |
|----------|-------|
| **Document ID** | PRD-2025-001 |
| **Version** | 3.0 |
| **Status** | Draft |
| **Owner** | Edouard |
| **Created** | 2025-01-13 |
| **Last Updated** | 2025-01-13 |
| **Slug** | ralph-wiggum-integration |
| **EMS Score** | 95/100 |
| **Template** | feature |

### Change History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2025-01-13 | EPCI Brainstormer | Initial generation from /brainstorm |
| 2.0 | 2025-01-13 | EPCI Brainstormer | Enrichi avec patterns librairie frankbria (circuit breaker, response analyzer, RALPH_STATUS, rate limiting) |
| 3.0 | 2025-01-13 | EPCI Brainstormer | Mode hybride: ajout Stop Hook (Anthropic officiel) + mode script (frankbria), /cancel-ralph, sélection intelligente |

---

## Executive Summary

**TL;DR** : Intégrer la méthodologie Ralph Wiggum dans EPCI pour permettre l'exécution autonome overnight de features complexes avec fresh context à chaque story.

| Aspect | Description |
|--------|-------------|
| **Problem** | `/orchestrate` actuel ne supporte pas le mode full autonome avec fresh context |
| **Solution** | Nouvelle commande `/ralph` + enrichissement `/decompose` avec génération prd.json |
| **Impact** | Exécution autonome de features complètes pendant la nuit (overnight coding) |
| **Target Launch** | TBD |

---

## Background & Strategic Fit

### Why Now?

- **Ralph Wiggum** est devenu le pattern de référence pour l'exécution autonome d'agents IA (validé par Anthropic, communauté active)
- Plugin officiel Anthropic disponible depuis fin 2025
- Résultats documentés impressionnants : MVP 50k$ pour 300$, langages de programmation créés en 30h AFK
- EPCI a déjà 80% de l'infrastructure nécessaire (DAG, journaling, validation)
- **Librairie de référence** : [frankbria/ralph-claude-code](https://github.com/frankbria/ralph-claude-code) v0.9.9 — 308 tests, patterns industriels matures (Circuit Breaker, Response Analyzer)

### Strategic Alignment

Cette feature s'aligne avec :
- [x] **Vision EPCI** : Automatisation maximale du workflow développement
- [x] **Pattern industrie** : Adoption du standard Ralph reconnu par la communauté
- [x] **Overnight coding** : Permettre le "ship code while you sleep"

---

## Problem Statement

### Current Situation

- `/orchestrate` exécute des specs en batch mais avec breakpoints interactifs
- Pas de mode full autonome pour exécution overnight
- Granularité trop large (1-5 jours/spec) pour itérations rapides
- Même context window = risque de bloat sur longues sessions

### Problem Definition

Les développeurs ne peuvent pas lancer une exécution autonome de features complexes et revenir le lendemain avec le travail terminé.

### Evidence & Data

- **Quantitative** : Ralph permet 50-100 itérations overnight vs 5-10 avec orchestrate supervisé
- **Qualitative** : Communauté rapporte des gains de productivité 10x sur projets adaptés

### Impact of Not Solving

- **Business** : Perte de productivité overnight, compétitivité réduite
- **User** : Frustration de ne pas pouvoir déléguer à l'agent pendant la nuit
- **Technical** : EPCI reste en retard sur les patterns modernes d'orchestration

---

## Goals

### Business Goals

- [ ] Permettre l'exécution autonome de features overnight (8-12h sans intervention)
- [ ] Réduire le coût par feature de 50% via parallélisation temporelle

### User Goals

- [ ] Lancer une commande avant de partir et retrouver le travail terminé le lendemain
- [ ] Conserver la traçabilité EPCI (Feature Documents) même en mode autonome

### Technical Goals

- [ ] Fresh context à chaque story (éviter le bloat)
- [ ] Intégration native avec /brief et /quick ou /epci
- [ ] Script shell externe pour robustesse (survit aux crashs Claude)
- [ ] Circuit Breaker pattern pour détecter stagnation et éviter boucles infinies
- [ ] Response Analyzer pour analyser les sorties Claude (JSON/text)
- [ ] Rate limiting intégré (100 calls/hour configurable)
- [ ] RALPH_STATUS block obligatoire pour communication structurée

---

## Non-Goals (Out of Scope v1)

| Exclusion | Raison | Future Version |
|-----------|--------|----------------|
| Multi-agent parallèle | Risque merge conflicts | v2 (branches séparées) |
| Notifications Slack/Email | Complexité intégration | v1.1 |
| Dashboard web temps réel | Hors scope CLI | v2 |
| Intégration CI/CD | Dépendance externe | v1.1 |
| tmux monitoring intégré | Nice-to-have, pas critique | v1.1 |
| Session expiration configurable | 24h par défaut suffisant | v1.1 |

---

## Personas

### Persona Primaire — Développeur Solo/Lead

- **Role**: Développeur senior ou lead technique travaillant sur des features complexes
- **Contexte**: Projets moyens à grands, besoin de productivité maximale, travaille souvent seul ou en petite équipe
- **Pain points**: Temps limité dans la journée, features qui traînent, supervision constante requise
- **Objectifs**: Déléguer l'implémentation de features bien spécifiées à l'agent pendant la nuit
- **Quote**: "Je veux lancer la feature avant de partir et la retrouver terminée demain matin"

### Persona Secondaire — Équipe Startup

- **Role**: Petite équipe (2-5 devs) avec contraintes de temps fortes
- **Contexte**: MVP à livrer rapidement, budget limité, besoin de vélocité
- **Pain points**: Pas assez de développeurs, features en backlog
- **Objectifs**: Multiplier la capacité de l'équipe avec l'IA overnight

---

## Stack Détecté

- **Framework**: Plugin EPCI (Markdown + Python)
- **Language**: Python 3 (scripts), Markdown (commandes, skills)
- **Patterns**: Commands, Skills, Subagents, Hooks
- **Outils**: Claude Code CLI, Bash scripting

---

## Exploration Summary

### Codebase Analysis

- **Structure**: Plugin EPCI avec src/ organisé par fonction
- **Architecture**: Commands → Skills → Subagents
- **Existant pertinent**: `/decompose`, `/orchestrate`, `@Explore`, skill `orchestrator-batch`

### Fichiers Potentiels

#### Commandes
| Fichier | Action | Notes |
|---------|--------|-------|
| `src/commands/ralph.md` | Create | Commande principale avec --mode hook\|script |
| `src/commands/cancel-ralph.md` | Create | Annulation boucle Ralph |
| `src/commands/decompose.md` | Modify | Ajouter flags --wiggum, --granularity |
| `src/commands/orchestrate.md` | Deprecate | Remplacé par /ralph |

#### Mode Hook (Anthropic officiel)
| Fichier | Action | Notes |
|---------|--------|-------|
| `src/hooks/ralph-stop-hook.sh` | Create | Stop hook qui intercepte les sorties |
| `src/templates/ralph/ralph-loop.local.md` | Create | Template fichier d'état YAML |

#### Mode Script (frankbria)
| Fichier | Action | Notes |
|---------|--------|-------|
| `src/scripts/ralph_loop.sh` | Create | Script bash principal |
| `src/scripts/lib/circuit_breaker.sh` | Create | Circuit Breaker pattern |
| `src/scripts/lib/response_analyzer.sh` | Create | Analyse réponses Claude |
| `src/scripts/lib/date_utils.sh` | Create | Utilitaires date cross-platform |
| `src/templates/ralph/PROMPT.md` | Create | Template prompt avec RALPH_STATUS |

#### Skills et Agents
| Fichier | Action | Notes |
|---------|--------|-------|
| `src/skills/core/ralph-converter/SKILL.md` | Create | Conversion specs → prd.json |
| `src/skills/core/ralph-analyzer/SKILL.md` | Create | Response Analyzer (JSON/text parsing) |
| `src/agents/ralph-executor.md` | Create | Subagent exécution stories (mode script) |

### Risques Identifiés

- **Medium** : Coûts tokens si mal configuré (mitigation: --max-iterations obligatoire)
- **Low** : Complexité intégration /brief + /quick dans subagent
- **Low** : Migration utilisateurs de /orchestrate vers /ralph

---

## User Stories

### US1 — Générer prd.json depuis /decompose

**En tant que** développeur,
**Je veux** que `/decompose --wiggum` génère un prd.json en plus des specs Markdown,
**Afin de** pouvoir utiliser le format Ralph standard.

**Acceptance Criteria:**
- [ ] Given un PRD Markdown, When je lance `/decompose --wiggum`, Then un fichier prd.json est généré avec les stories atomiques
- [ ] Given le flag `--granularity small`, When la décomposition s'exécute, Then chaque jour de travail génère 3-5 stories
- [ ] Given le flag `--wiggum`, When la génération termine, Then ralph.sh et prompt.md sont aussi générés

**Priorité**: Must-have
**Complexité**: M

---

### US2 — Script ralph.sh généré

**En tant que** développeur,
**Je veux** que `/decompose --wiggum` génère un script ralph.sh personnalisé,
**Afin de** pouvoir lancer la boucle autonome facilement.

**Acceptance Criteria:**
- [ ] Given la génération avec --wiggum, When elle termine, Then ralph.sh est exécutable
- [ ] Given ralph.sh, When je le lance, Then il boucle sur les stories passes=false
- [ ] Given une story complétée, When le commit est fait, Then prd.json est mis à jour avec passes=true

**Priorité**: Must-have
**Complexité**: M

---

### US3 — prompt.md intelligent

**En tant que** développeur,
**Je veux** que prompt.md soit pré-rempli selon mon stack détecté,
**Afin de** ne pas avoir à tout configurer manuellement.

**Acceptance Criteria:**
- [ ] Given un projet avec package.json, When prompt.md est généré, Then les commandes npm/pnpm sont pré-remplies
- [ ] Given un projet avec composer.json, When prompt.md est généré, Then les commandes PHP sont pré-remplies
- [ ] Given prompt.md généré, When je l'ouvre, Then des sections "À PERSONNALISER" sont clairement marquées

**Priorité**: Must-have
**Complexité**: S

---

### US4 — Subagent @ralph-executor

**En tant que** système Ralph,
**Je veux** un subagent dédié pour exécuter chaque story,
**Afin d'** encapsuler la logique /brief → /quick ou /epci.

**Acceptance Criteria:**
- [ ] Given une story à exécuter, When @ralph-executor est invoqué, Then il appelle /brief avec le contexte
- [ ] Given le résultat de /brief, When la complexité est TINY/SMALL, Then /quick --autonomous est appelé
- [ ] Given le résultat de /brief, When la complexité est STANDARD+, Then /epci --autonomous est appelé
- [ ] Given l'exécution terminée, When les tests passent, Then un Feature Document minimal est généré

**Priorité**: Must-have
**Complexité**: L

---

### US5 — Commande /ralph

**En tant que** développeur,
**Je veux** une commande `/ralph <specs-dir>` pour lancer l'exécution,
**Afin de** ne pas avoir à lancer le script shell manuellement.

**Acceptance Criteria:**
- [ ] Given un dossier avec prd.json, When je lance `/ralph`, Then l'exécution démarre
- [ ] Given le flag `--dry-run`, When je lance /ralph, Then le plan est affiché sans exécution
- [ ] Given le flag `--max-iterations 20`, When la limite est atteinte, Then l'exécution s'arrête proprement

**Priorité**: Must-have
**Complexité**: M

---

### US6 — Mode hybride (prd.json + specs contexte)

**En tant que** système Ralph,
**Je veux** que chaque story ait accès au contexte de sa spec parente,
**Afin d'** avoir le contexte métier riche pour l'implémentation.

**Acceptance Criteria:**
- [ ] Given une story US-005 appartenant à S02, When @ralph-executor s'exécute, Then S02.md est chargé comme contexte
- [ ] Given le contexte chargé, When /brief analyse, Then l'exploration est ciblée sur le périmètre de la spec

**Priorité**: Must-have
**Complexité**: M

---

### US7 — Sécurité configurable

**En tant que** développeur,
**Je veux** configurer le niveau de sécurité avec `--safety-level`,
**Afin de** contrôler les garde-fous selon mon contexte.

**Acceptance Criteria:**
- [ ] Given `--safety-level minimal`, When Ralph s'exécute, Then seul max-iterations est vérifié
- [ ] Given `--safety-level moderate`, When Ralph s'exécute, Then un warning s'affiche si pas de sandbox
- [ ] Given `--safety-level strict`, When Ralph s'exécute, Then .claude/settings.json sécurisé est généré

**Priorité**: Should-have
**Complexité**: S

---

### US8 — Dépréciation /orchestrate

**En tant que** mainteneur EPCI,
**Je veux** déprécier `/orchestrate` proprement,
**Afin de** migrer les utilisateurs vers `/ralph`.

**Acceptance Criteria:**
- [ ] Given un utilisateur qui lance /orchestrate, When la commande s'exécute, Then un warning de dépréciation s'affiche
- [ ] Given le warning, When il s'affiche, Then il suggère d'utiliser /ralph à la place
- [ ] Given la documentation, When elle est mise à jour, Then /orchestrate est marqué deprecated

**Priorité**: Should-have
**Complexité**: S

---

### US9 — Circuit Breaker Pattern

**En tant que** système Ralph,
**Je veux** un circuit breaker qui détecte la stagnation,
**Afin d'** éviter les boucles infinies et le gaspillage de tokens.

**Acceptance Criteria:**
- [ ] Given 3 boucles consécutives sans changement de fichiers, When le circuit breaker évalue, Then il passe en état HALF_OPEN
- [ ] Given état HALF_OPEN et toujours pas de progression, When le seuil est atteint, Then circuit passe en OPEN et exécution s'arrête
- [ ] Given état OPEN, When l'utilisateur lance `--reset-circuit`, Then circuit revient en CLOSED
- [ ] Given 5 boucles avec la même erreur répétée, When le circuit breaker évalue, Then il passe en OPEN
- [ ] Given progression détectée en HALF_OPEN, When des fichiers sont modifiés, Then circuit revient en CLOSED

**Priorité**: Must-have
**Complexité**: M

**Notes techniques:**
- Pattern basé sur Michael Nygard "Release It!"
- États: CLOSED (normal) → HALF_OPEN (monitoring) → OPEN (arrêt)
- Seuils configurables: CB_NO_PROGRESS_THRESHOLD=3, CB_SAME_ERROR_THRESHOLD=5

---

### US10 — Response Analyzer

**En tant que** système Ralph,
**Je veux** un analyseur de réponses Claude intelligent,
**Afin de** détecter automatiquement la complétion, les stuck loops, et le type de travail.

**Acceptance Criteria:**
- [ ] Given sortie Claude en JSON, When response_analyzer s'exécute, Then les champs structurés sont extraits (status, exit_signal, work_type)
- [ ] Given sortie Claude en texte, When le bloc RALPH_STATUS est présent, Then il est parsé pour extraire exit_signal
- [ ] Given même erreur dans les 3 dernières sorties, When detect_stuck_loop s'exécute, Then retourne true
- [ ] Given completion_indicators >= 2 ET EXIT_SIGNAL=true, When should_exit est évalué, Then retourne "project_complete"
- [ ] Given completion_indicators >= 2 MAIS EXIT_SIGNAL=false, When should_exit est évalué, Then continue (Claude explicite a priorité)

**Priorité**: Must-have
**Complexité**: M

**Notes techniques:**
- Dual-condition exit : completion_indicators + EXIT_SIGNAL explicite
- Confidence scoring pour évaluer la fiabilité de la détection
- Session management avec expiration 24h

---

### US11 — RALPH_STATUS Block obligatoire

**En tant que** système Ralph,
**Je veux** que Claude output un bloc RALPH_STATUS structuré à chaque fin d'itération,
**Afin d'** avoir une communication fiable et parsable entre Claude et le script.

**Acceptance Criteria:**
- [ ] Given template PROMPT.md généré, When il est créé, Then il contient la section RALPH_STATUS avec format obligatoire
- [ ] Given une itération Claude terminée, When la sortie est analysée, Then le bloc RALPH_STATUS est présent
- [ ] Given bloc RALPH_STATUS avec EXIT_SIGNAL=false, When completion patterns sont détectés, Then EXIT_SIGNAL a priorité (continue)
- [ ] Given bloc RALPH_STATUS avec STATUS=BLOCKED, When analysé, Then le circuit breaker est notifié

**Priorité**: Must-have
**Complexité**: S

**Format RALPH_STATUS:**
```
---RALPH_STATUS---
STATUS: IN_PROGRESS | COMPLETE | BLOCKED
TASKS_COMPLETED_THIS_LOOP: <number>
FILES_MODIFIED: <number>
TESTS_STATUS: PASSING | FAILING | NOT_RUN
WORK_TYPE: IMPLEMENTATION | TESTING | DOCUMENTATION | REFACTORING
EXIT_SIGNAL: false | true
RECOMMENDATION: <one line summary>
---END_RALPH_STATUS---
```

---

### US12 — Rate Limiting

**En tant que** développeur,
**Je veux** un rate limiting intégré avec gestion de la limite API 5h,
**Afin de** contrôler les coûts et éviter les erreurs API.

**Acceptance Criteria:**
- [ ] Given MAX_CALLS_PER_HOUR=100 (défaut), When la limite est atteinte, Then countdown jusqu'au reset horaire
- [ ] Given limite API 5h Anthropic atteinte, When détectée, Then proposer: [1] Attendre 60min [2] Arrêter
- [ ] Given flag `--calls 50`, When passé à /ralph, Then limite horaire ajustée
- [ ] Given reset horaire, When nouvelle heure commence, Then compteur remis à zéro automatiquement

**Priorité**: Should-have
**Complexité**: S

---

### US13 — Mode Stop Hook (Same Session)

**En tant que** développeur,
**Je veux** un mode Ralph utilisant un Stop Hook natif Claude Code,
**Afin de** garder le contexte de session et avoir une intégration plus simple.

**Acceptance Criteria:**
- [ ] Given `/ralph --mode hook`, When lancé, Then le stop-hook.sh est activé et intercepte les sorties
- [ ] Given une itération en cours, When Claude tente de sortir, Then le hook bloque et réinjecte le prompt
- [ ] Given fichier `.claude/ralph-loop.local.md`, When créé, Then il contient le frontmatter YAML (iteration, max_iterations, completion_promise)
- [ ] Given `<promise>COMPLETE</promise>` dans la sortie Claude, When détecté, Then la boucle s'arrête proprement
- [ ] Given max_iterations atteint, When vérifié par le hook, Then la boucle s'arrête avec message

**Priorité**: Must-have
**Complexité**: M

**Notes techniques:**
- Basé sur l'implémentation officielle Anthropic
- Fichier d'état: `.claude/ralph-loop.local.md` avec YAML frontmatter
- Lecture du transcript JSONL pour analyser les sorties
- Contexte préservé entre itérations (même session)

**Format fichier d'état:**
```yaml
---
iteration: 1
max_iterations: 50
completion_promise: "COMPLETE"
---
[Prompt original ici]
```

---

### US14 — Commande /cancel-ralph

**En tant que** développeur,
**Je veux** une commande `/cancel-ralph` pour annuler une boucle en cours,
**Afin de** pouvoir interrompre proprement sans Ctrl+C.

**Acceptance Criteria:**
- [ ] Given une boucle Ralph active, When `/cancel-ralph` est exécuté, Then le fichier d'état est supprimé
- [ ] Given pas de boucle active, When `/cancel-ralph` est exécuté, Then message "Aucune boucle Ralph active"
- [ ] Given annulation, When effectuée, Then message de confirmation avec stats (iterations effectuées)

**Priorité**: Must-have
**Complexité**: S

---

### US15 — Mode Script Externe (Fresh Context)

**En tant que** développeur,
**Je veux** un mode Ralph utilisant un script bash externe,
**Afin d'** avoir un fresh context à chaque itération pour les sessions overnight longues.

**Acceptance Criteria:**
- [ ] Given `/ralph --mode script`, When lancé, Then ralph_loop.sh est exécuté en externe
- [ ] Given une story complétée, When le script vérifie, Then nouvelle instance Claude est lancée (fresh context)
- [ ] Given crash Claude, When détecté, Then le script survit et peut reprendre avec --continue
- [ ] Given mode script, When actif, Then Circuit Breaker et Response Analyzer sont utilisés

**Priorité**: Must-have
**Complexité**: M

**Notes techniques:**
- Basé sur la librairie frankbria/ralph-claude-code
- Fresh context évite le bloat sur longues sessions
- Plus robuste pour overnight (survit aux crashs)
- Utilise prd.json pour le tracking des stories

---

### US16 — Sélection de mode intelligent

**En tant que** développeur,
**Je veux** que Ralph choisisse automatiquement le mode optimal selon le contexte,
**Afin de** ne pas avoir à spécifier manuellement.

**Acceptance Criteria:**
- [ ] Given `/ralph` sans flag mode, When durée estimée < 2h, Then mode hook par défaut
- [ ] Given `/ralph` sans flag mode, When durée estimée > 2h ou flag --overnight, Then mode script par défaut
- [ ] Given flag `--mode hook` explicite, When passé, Then force le mode hook
- [ ] Given flag `--mode script` explicite, When passé, Then force le mode script
- [ ] Given recommandation de mode, When affichée, Then explique pourquoi ce mode est suggéré

**Priorité**: Should-have
**Complexité**: S

**Règles de sélection automatique:**
| Contexte | Mode par défaut | Raison |
|----------|-----------------|--------|
| < 10 stories, < 2h estimé | hook | Contexte préservé, plus simple |
| > 10 stories, > 2h estimé | script | Fresh context, robustesse |
| Flag --overnight | script | Survit aux crashs, rate limiting |
| Flag --interactive | hook | Contexte préservé |

---

## Règles Métier

### Règles communes (tous modes)
- **RM1**: --max-iterations est obligatoire pour éviter les boucles infinies
- **RM2**: Un Feature Document doit être généré pour chaque story, même en mode /quick
- **RM3**: Rate limiting : max 100 calls/hour par défaut (configurable)

### Règles Mode Hook (same session)
- **RM4-H**: Le contexte est préservé entre itérations (même session Claude)
- **RM5-H**: Completion via `<promise>COMPLETE</promise>` tags
- **RM6-H**: État stocké dans `.claude/ralph-loop.local.md` (YAML frontmatter)
- **RM7-H**: Stop hook intercepte les sorties et réinjecte le prompt

### Règles Mode Script (fresh context)
- **RM4-S**: Chaque story a un fresh context (nouvelle instance Claude)
- **RM5-S**: Le prd.json est la source de vérité pour le tracking (passes: true/false)
- **RM6-S**: Le bloc RALPH_STATUS DOIT être présent à la fin de chaque réponse Claude
- **RM7-S**: EXIT_SIGNAL explicite a priorité sur les heuristiques de completion
- **RM8-S**: Circuit Breaker doit être en état CLOSED pour permettre l'exécution
- **RM9-S**: Le script ralph.sh doit être exécutable standalone (sans Claude actif)
- **RM10-S**: Session auto-reset sur: circuit breaker OPEN, Ctrl+C, project completion

---

## Cas Limites & Edge Cases

| Cas | Comportement attendu |
|-----|---------------------|
| prd.json n'existe pas | Erreur claire avec suggestion de lancer /decompose --wiggum |
| Toutes stories passes=true dès le départ | Output "COMPLETE" immédiatement |
| Story échoue après max-retries | Marquer "failed" dans prd.json, continuer avec la suivante |
| Ctrl+C pendant exécution | Checkpoint sauvegardé, session reset, reprise possible avec --continue |
| Conflit git | Arrêt propre, message explicite, intervention manuelle requise |
| Circuit Breaker OPEN | Afficher statut détaillé, suggestions de résolution, --reset-circuit requis |
| RALPH_STATUS absent de la sortie | Warning, fallback sur heuristiques textuelles |
| Même erreur 5x consécutives | Circuit Breaker → OPEN, arrêt avec diagnostic |
| Rate limit 100/h atteint | Countdown jusqu'au reset horaire, pas d'arrêt définitif |
| Limite API 5h Anthropic | Prompt user: [1] Attendre 60min [2] Arrêter |
| Session expirée (>24h) | Démarrer nouvelle session automatiquement |
| JSON malformé dans sortie Claude | Fallback sur parsing texte |
| EXIT_SIGNAL=false mais completion patterns | Continue (EXIT_SIGNAL explicite a priorité) |
| 3 boucles test-only consécutives | Exit avec raison "test_saturation" |

---

## Success Metrics

| Métrique | Baseline | Cible | Méthode de mesure |
|----------|----------|-------|-------------------|
| Stories complétées overnight | 0 (N/A) | 10-20/nuit | Logs prd.json |
| Taux de succès stories | N/A | >80% | passes=true / total |
| Coût moyen par story | ~10$ (orchestrate) | ~5-8$ | API billing |
| Temps setup utilisateur | N/A | <5 min | User testing |

---

## Contraintes Techniques Identifiées

| Contrainte | Impact | Mitigation |
|------------|--------|------------|
| Fresh context = pas de mémoire | Perte contexte entre stories | progress.txt + git history + session continuity |
| Exit code 2 requis par Ralph | Modification comportement CLI | RALPH_STATUS block + response analyzer |
| Coût tokens cumulé | Budget overnight | --max-iterations + rate limiting + alertes |
| Détection completion non fiable | Arrêt prématuré ou boucle infinie | Dual-condition (indicators + EXIT_SIGNAL) |
| Erreurs répétées = gaspillage | Tokens perdus | Circuit Breaker avec seuils configurables |
| API limite 5h Anthropic | Interruption forcée | Détection + prompt user wait/exit |
| Parsing sortie Claude variable | JSON ou texte selon config | Auto-détection format + fallback |
| Dépendance jq | Parsing JSON | Vérifier présence jq au setup |
| Dépendance tmux (optionnel) | Monitoring avancé | Fallback sans tmux pour v1 |

---

## Dépendances

- **Internes**: `/brief`, `/quick`, `/epci`, `/decompose`, skill `project-memory`
- **Externes**: Claude Code CLI (v2.0.76+), Bash 4.0+, jq (JSON processing), git
- **Optionnelles**: tmux (monitoring avancé v1.1)

---

## Assumptions

- [x] **Technical** : Claude Code supporte l'exécution via script externe (claude --print)
- [x] **Technical** : Exit code peut être contrôlé par l'agent
- [ ] **User** : Utilisateurs ont accès à un terminal Bash
- [ ] **Resources** : Budget API suffisant pour sessions overnight (~50-150$/session)

---

## Critères d'Acceptation Globaux

- [ ] Tests unitaires pour ralph-converter skill
- [ ] Test intégration /decompose --wiggum → /ralph
- [ ] Documentation utilisateur complète
- [ ] Exemple de projet fonctionnel dans docs/examples/

---

## Questions Ouvertes

- [ ] Faut-il un mode "simulation" pour tester sans consommer de tokens ?
- [ ] Quelle stratégie de retry par défaut ? (3 retries suggéré)

---

## FAQ

### Internal FAQ (Équipe)

**Q: Pourquoi remplacer /orchestrate plutôt que l'enrichir ?**
A: Ralph est le pattern validé par la communauté. Mieux vaut adopter le standard que maintenir deux systèmes parallèles.

**Q: Pourquoi un script shell externe plutôt qu'une boucle interne ?**
A: Le script shell survit aux crashs Claude, permet le fresh context, et suit le pattern Ralph original.

**Q: Comment gérer les stories qui échouent ?**
A: Retry configurable (défaut 3), puis marquage "failed" et passage à la suivante. Rapport final liste les échecs.

### External FAQ (Utilisateurs)

**Q: Combien coûte une session overnight ?**
A: Environ 3-8$ par story selon complexité, soit 50-150$ pour une feature complète de 20 stories.

**Q: Puis-je superviser l'exécution ?**
A: Oui, progress.txt et prd.json sont mis à jour en temps réel. Vous pouvez suivre la progression.

**Q: Que se passe-t-il si je coupe la connexion ?**
A: Le script ralph.sh s'arrête proprement. Relancez avec --continue pour reprendre.

---

## Estimation Préliminaire

| Métrique | Valeur |
|----------|--------|
| Complexité estimée | LARGE |
| Effort total | 10-12 jours |
| Fichiers impactés | ~17 |
| User Stories | 16 (11 Must-have, 5 Should-have) |
| Scripts Bash | 5 (ralph_loop.sh, circuit_breaker.sh, response_analyzer.sh, date_utils.sh, stop-hook.sh) |
| Modes | 2 (hook + script) |
| Risque global | Medium |

---

## Timeline & Milestones

### Target Launch

**Objectif** : TBD — À définir avec planning

### Key Milestones

| Milestone | Target Date | Owner | Status |
|-----------|-------------|-------|--------|
| PRD Review Complete | TBD | Edouard | Draft |
| Phase 1: Mode Hook (Stop Hook Anthropic) | TBD | Dev | Not Started |
| Phase 2: Mode Script (frankbria foundation) | TBD | Dev | Not Started |
| Phase 3: /decompose enrichi + prd.json | TBD | Dev | Not Started |
| Phase 4: Commande /ralph unifiée | TBD | Dev | Not Started |
| Phase 5: Sélection intelligente + polish | TBD | Dev | Not Started |
| Phase 6: Tests & Docs | TBD | Dev | Not Started |
| General Availability | TBD | All | Not Started |

### Phasing Strategy

**Phase 1 (Mode Hook)** : US13, US14 — Stop Hook (Anthropic) + /cancel-ralph
- Plus simple, permet de tester rapidement
- Basé sur l'implémentation officielle Anthropic

**Phase 2 (Mode Script Foundation)** : US9, US10, US11 — Circuit Breaker + Response Analyzer + RALPH_STATUS
- Scripts bash robustes pour mode overnight
- Basé sur frankbria/ralph-claude-code

**Phase 3 (Génération)** : US1, US2, US3, US15 — prd.json, ralph.sh, prompt.md, mode script complet
- Enrichissement /decompose
- Templates intelligents

**Phase 4 (Intégration)** : US4, US5, US6 — @ralph-executor, /ralph command, mode hybride
- Commande unifiée avec --mode hook|script
- Intégration /brief + /quick ou /epci

**Phase 5 (Polish)** : US7, US8, US12, US16 — Sécurité, dépréciation, rate limiting, sélection intelligente
- Auto-détection du meilleur mode
- Migration /orchestrate → /ralph

**Phase 6 (v1.1+)** : tmux monitoring, notifications, dashboard (Could-have)

---

## Risques (Pre-mortem)

| Risque | Probabilité | Impact | Mitigation |
|--------|-------------|--------|------------|
| Coûts overnight explosent | M | H | --max-iterations + rate limiting + circuit breaker |
| Stories trop complexes pour atomicité | M | M | Granularité configurable + validation @decompose-validator |
| Conflits git en multi-story | L | H | Un commit par story + branches feature |
| Adoption lente (habitude orchestrate) | L | L | Warning dépréciation + migration guide |
| Circuit Breaker trop sensible | M | M | Seuils configurables + logs détaillés |
| RALPH_STATUS non respecté par Claude | M | H | Validation dans prompt.md + fallback heuristiques |
| Complexité scripts Bash | M | M | Tests BATS + documentation inline |
| Dépendance jq non installée | L | H | Check au setup + message d'erreur clair |

---

## Références Techniques

### Librairie Mode Hook (Anthropic officiel)
- **Repository**: [anthropics/claude-plugins-official/ralph-loop](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/ralph-loop)
- **Approche**: Stop Hook qui intercepte les sorties
- **Fichiers clés à adapter**:
  - `hooks/stop-hook.sh` — Hook principal (~150 lignes)
  - `commands/ralph-loop.md` — Commande /ralph-loop
  - `commands/cancel-ralph.md` — Commande /cancel-ralph

### Librairie Mode Script (frankbria)
- **Repository**: [frankbria/ralph-claude-code](https://github.com/frankbria/ralph-claude-code)
- **Version**: v0.9.9
- **Tests**: 308 passing (100% pass rate)
- **Fichiers clés à adapter**:
  - `ralph_loop.sh` — Script principal (~1200 lignes)
  - `lib/circuit_breaker.sh` — Pattern Circuit Breaker
  - `lib/response_analyzer.sh` — Analyse réponses Claude
  - `templates/PROMPT.md` — Template avec RALPH_STATUS

### Patterns appliqués
- **Stop Hook** (Anthropic) — Intercepte sortie, réinjecte prompt, même session
- **Circuit Breaker** (Michael Nygard, "Release It!") — 3 états pour détecter stagnation
- **Dual-condition Exit** (frankbria) — completion indicators + explicit EXIT_SIGNAL
- **Completion Promise** (Anthropic) — `<promise>COMPLETE</promise>` tags
- **Session Continuity** (frankbria) — --continue flag avec expiration 24h

### Comparaison des modes

| Aspect | Mode Hook | Mode Script |
|--------|-----------|-------------|
| Contexte | Préservé (même session) | Fresh (nouvelle instance) |
| Robustesse crash | Faible | Forte |
| Complexité | ~150 lignes | ~1500 lignes |
| Use case | Sessions courtes (<2h) | Overnight (>2h) |
| Completion | `<promise>` tags | RALPH_STATUS block |

---

*PRD v3.0 — Mode hybride (Hook Anthropic + Script frankbria) — Prêt pour `/brief`*
*Détails du processus de brainstorming dans le Journal d'Exploration.*
