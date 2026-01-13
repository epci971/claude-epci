# Journal d'Exploration — Intégration Ralph Wiggum dans EPCI

> **Feature**: Intégration Ralph Wiggum dans EPCI
> **Date**: 2025-01-13
> **Iterations**: 11 (9 brainstorm + 2 analyses librairies)

---

## Résumé

Brainstorming pour intégrer la méthodologie Ralph Wiggum (boucle continue d'agent) dans le plugin EPCI. L'exploration a couvert la décomposition PRD → prd.json, l'enrichissement de `/decompose`, la création d'une nouvelle commande `/ralph` remplaçant `/orchestrate`, et l'intégration avec le workflow EPCI existant (/brief → /quick ou /epci).

---

## Progression EMS

| Iteration | Score | Delta | Focus |
|-----------|-------|-------|-------|
| Init | 25 | - | Cadrage initial, lecture doc technique Ralph |
| 1 | 30 | +5 | Exploration codebase (decompose, orchestrate) |
| 2 | 40 | +10 | Recherche web Ralph, schéma prd.json |
| 3 | 48 | +8 | Granularité stories configurable |
| 4 | 50 | +2 | Script shell généré par projet |
| 5 | 58 | +8 | Structure prompt.md (template intelligent) |
| 6 | 62 | +4 | Clarification prompt.md = cerveau Ralph |
| 7 | 70 | +8 | Intégration /brief + /quick/epci, subagent |
| 8 | 80 | +10 | Décision majeure: remplacer /orchestrate par /ralph |
| 9 | 85 | +5 | Validation complétude, finalisation |
| 10 | 92 | +7 | Analyse librairie frankbria/ralph-claude-code |
| 11 | 95 | +3 | Analyse librairie Anthropic officielle, mode hybride |

---

## EMS Final Détaillé (v3.0)

| Axe | Score |
|-----|-------|
| Clarté | 97/100 |
| Profondeur | 95/100 |
| Couverture | 98/100 |
| Décisions | 95/100 |
| Actionnabilité | 90/100 |

---

## Métadonnées Brainstormer

| Métrique | Valeur |
|----------|--------|
| Version | v4.9 |
| Template | feature |
| Techniques appliquées | Architecture comparison, Web research |
| Durée exploration | ~45min |
| Persona actif | Architecte |
| Phase finale | Convergent |

---

## Décisions Clés

### Décision 1 — Approche Hybrid Mode

- **Contexte**: Comment intégrer Ralph dans EPCI ?
- **Options considérées**:
  - A) Full Ralph Mode (commande indépendante)
  - B) Hybrid Mode (enrichir existant)
  - C) Enhanced Decompose seulement
- **Choix**: B — Hybrid Mode
- **Justification**: Réutilise l'infrastructure existante (DAG, journaling), moins de duplication

### Décision 2 — Granularité configurable

- **Contexte**: Quelle taille pour les stories Ralph ?
- **Options considérées**:
  - A) ~15-30 min ultra-atomique
  - B) ~1-2 heures micro-feature
  - C) Configurable via flag
- **Choix**: C — Configurable `--granularity [micro|small|standard]`
- **Justification**: Projets différents = besoins différents

### Décision 3 — Output /decompose dual

- **Contexte**: Que génère /decompose --wiggum ?
- **Options considérées**: Markdown seul, JSON seul, les deux
- **Choix**: Les deux — Markdown specs (1-5j) + prd.json (30min-2h)
- **Justification**: Specs Markdown = contexte humain riche, prd.json = exécution atomique

### Décision 4 — Mode exécution hybride

- **Contexte**: Comment Ralph utilise les fichiers ?
- **Options considérées**: prd.json seul, hybride, modes séparés
- **Choix**: Hybride — prd.json pour tâches + specs.md pour contexte
- **Justification**: Best of both worlds

### Décision 5 — Script shell généré par projet

- **Contexte**: Comment gérer ralph.sh ?
- **Options considérées**: Script externe, intégré EPCI, commande Claude
- **Choix**: Script généré par projet dans specs/
- **Justification**: Personnalisation par projet, transparence, pattern Ralph original

### Décision 6 — prompt.md intelligent + personnalisable

- **Contexte**: Comment structurer prompt.md ?
- **Options considérées**: Générique, personnalisable, intelligent, combinaison
- **Choix**: D — Template intelligent + personnalisable
- **Justification**: Détection auto du stack + sections à personnaliser

### Décision 7 — Sécurité configurable

- **Contexte**: Quels garde-fous pour mode overnight ?
- **Options considérées**: Minimal, modéré, strict, configurable
- **Choix**: Configurable `--safety-level`
- **Justification**: Flexibilité selon contexte utilisateur

### Décision 8 — Subagent @ralph-executor

- **Contexte**: Comment intégrer /brief + /quick/epci dans la boucle ?
- **Options considérées**: Dans prompt.md, dans ralph.sh, subagent, flag /quick
- **Choix**: C — Subagent @ralph-executor
- **Justification**: Encapsulation propre, réutilisable, logique complexe isolée

### Décision 9 — Routing brief → quick/epci

- **Contexte**: Toutes stories via /quick ou routing intelligent ?
- **Choix**: Routing intelligent comme aujourd'hui
- **Justification**: Certaines stories peuvent être STANDARD+, traçabilité Feature Document

### Décision 10 — Remplacer /orchestrate par /ralph

- **Contexte**: Que faire de /orchestrate ?
- **Options considérées**: Enrichir, cohabitation, remplacer
- **Choix**: A — Remplacer (déprécier /orchestrate)
- **Justification**: Ralph = pattern industrie validé, une seule commande = moins de confusion

---

## Deep Dives

### Deep Dive — Format prd.json Ralph

- **Iteration**: 2
- **Résumé**: Recherche web + fetch GitHub snarktank/ralph pour schéma exact
- **Conclusion**:
  ```json
  {
    "branchName": "string",
    "userStories": [{
      "id": "string",
      "title": "string",
      "passes": false,
      "priority": number,
      "acceptanceCriteria": "string"
    }]
  }
  ```

### Deep Dive — Différences orchestrate vs Ralph

- **Iteration**: 3-4
- **Résumé**: Comparaison granularité, context, boucle, overnight
- **Conclusion**: Ralph = fresh context + script externe + granularité fine. EPCI = breakpoints + même session + specs larges

### Deep Dive — Intégration /brief dans Ralph

- **Iteration**: 7
- **Résumé**: Discussion sur réutilisation des commandes EPCI dans la boucle Ralph
- **Conclusion**: @ralph-executor encapsule /brief → /quick ou /epci avec Feature Document forcé

---

## Frameworks Appliqués

### Comparaison Architecture — Iteration 3

| Aspect | /orchestrate | Ralph | Choix retenu |
|--------|-------------|-------|--------------|
| Granularité | 1-5 jours | 30min-2h | Ralph |
| Context | Même session | Fresh | Ralph |
| Script | Interne | Externe shell | Ralph |
| Tracking | INDEX.md | prd.json | Hybride |

---

## Questions Résolues

| Question | Réponse | Iteration |
|----------|---------|-----------|
| Comment décomposer PRD → JSON ? | /decompose --wiggum génère les deux | 3 |
| Utiliser /decompose existant ? | Oui, enrichir avec flags | 3 |
| /brief + /epci dans Ralph ? | Oui, via @ralph-executor | 7 |
| Que faire de /orchestrate ? | Déprécier, remplacer par /ralph | 8 |
| Quel prompt pour Ralph ? | prompt.md intelligent + personnalisable | 6 |

---

## Recherches Externes

| Source | Insight clé |
|--------|-------------|
| [GitHub snarktank/ralph](https://github.com/snarktank/ralph) | Schéma prd.json officiel |
| [paddo.dev/blog/ralph-wiggum](https://paddo.dev/blog/ralph-wiggum-autonomous-loops/) | Exit code 2, fresh context |
| [aihero.dev tips](https://www.aihero.dev/tips-for-ai-coding-with-ralph-wiggum) | Best practices stories atomiques |
| [VentureBeat](https://venturebeat.com/technology/how-ralph-wiggum-went-from-the-simpsons-to-the-biggest-name-in-ai-right-now) | Contexte adoption industrie |
| [GitHub frankbria/ralph-claude-code](https://github.com/frankbria/ralph-claude-code) | Librairie officielle v0.9.9 avec 308 tests |

---

## Iteration 10 — Analyse Librairie Officielle

### Deep Dive — Librairie frankbria/ralph-claude-code

- **Date**: 2025-01-13
- **Source**: Librairie locale `/docs/librairies/ralph-claude-code-main/`
- **Version**: v0.9.9

**Éléments critiques identifiés et ajoutés au PRD v2.0:**

| Élément | Description | User Story |
|---------|-------------|------------|
| Circuit Breaker | Pattern 3 états (CLOSED/HALF_OPEN/OPEN) | US9 |
| Response Analyzer | Parsing JSON/text, confidence scoring | US10 |
| RALPH_STATUS Block | Format structuré obligatoire | US11 |
| Rate Limiting | 100 calls/hour + gestion limite 5h | US12 |
| Dual-condition Exit | completion_indicators + EXIT_SIGNAL | US10 |

### Décisions Supplémentaires (v2.0)

### Décision 11 — Intégrer Circuit Breaker Pattern

- **Contexte**: Comment éviter les boucles infinies de manière robuste ?
- **Options considérées**:
  - A) Simple max-iterations
  - B) Circuit Breaker pattern complet (3 états)
  - C) Combinaison des deux
- **Choix**: C — Circuit Breaker + max-iterations
- **Justification**: Le pattern industriel (Michael Nygard) détecte la stagnation intelligemment

### Décision 12 — RALPH_STATUS Block obligatoire

- **Contexte**: Comment communiquer de manière fiable entre Claude et le script ?
- **Options considérées**:
  - A) Heuristiques textuelles seules
  - B) JSON output format
  - C) RALPH_STATUS block structuré
- **Choix**: C — RALPH_STATUS block (comme librairie officielle)
- **Justification**: Format simple à parser, explicite, avec EXIT_SIGNAL qui a priorité

### Décision 13 — Dual-condition Exit

- **Contexte**: Quand arrêter la boucle ?
- **Options considérées**:
  - A) Heuristiques seules (completion patterns)
  - B) EXIT_SIGNAL seul
  - C) Dual-condition (indicators + EXIT_SIGNAL)
- **Choix**: C — Dual-condition
- **Justification**: Évite les arrêts prématurés quand Claude dit explicitement "continue"

### Décision 14 — Rate Limiting intégré

- **Contexte**: Comment gérer les limites API ?
- **Options considérées**:
  - A) Pas de rate limiting (laisser l'API rejeter)
  - B) Rate limiting basique
  - C) Rate limiting + gestion limite 5h
- **Choix**: C — Rate limiting complet
- **Justification**: Meilleure UX, countdown visible, gestion gracieuse limite 5h

---

## Iteration 11 — Analyse Librairie Anthropic Officielle

### Deep Dive — Plugin ralph-loop Anthropic

- **Date**: 2025-01-13
- **Source**: [anthropics/claude-plugins-official/ralph-loop](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/ralph-loop)

**Découverte majeure**: L'approche officielle Anthropic est **fondamentalement différente** de frankbria:

| Aspect | frankbria (Mode Script) | Anthropic (Mode Hook) |
|--------|------------------------|----------------------|
| Mécanisme | Script bash externe | Stop Hook natif |
| Contexte | Fresh à chaque itération | Préservé (même session) |
| Completion | RALPH_STATUS block | `<promise>` tags |
| Complexité | ~1500 lignes | ~150 lignes |
| Robustesse | Survit aux crashs | Perd état si crash |

### Décision 15 — Mode Hybride

- **Contexte**: Quelle approche adopter ?
- **Options considérées**:
  - A) Mode Hook seul (Anthropic officiel)
  - B) Mode Script seul (frankbria)
  - C) Mode hybride (les deux)
- **Choix**: C — Mode hybride
- **Justification**: Flexibilité maximale, chaque mode a ses use cases

### Décision 16 — Sélection intelligente de mode

- **Contexte**: Comment choisir automatiquement le bon mode ?
- **Options considérées**:
  - A) Toujours demander à l'utilisateur
  - B) Défaut fixe avec override
  - C) Sélection intelligente basée sur contexte
- **Choix**: C — Sélection intelligente
- **Justification**: UX optimale, < 2h → hook, > 2h → script

### Nouvelles User Stories ajoutées (v3.0)

| US | Titre | Priorité |
|----|-------|----------|
| US13 | Mode Stop Hook (Same Session) | Must-have |
| US14 | Commande /cancel-ralph | Must-have |
| US15 | Mode Script Externe (Fresh Context) | Must-have |
| US16 | Sélection de mode intelligent | Should-have |

---

## Outputs Générés

| Fichier | Description |
|---------|-------------|
| `PRD-ralph-wiggum-integration-2025-01-13.md` | PRD v3.0 complet avec 16 User Stories (mode hybride) |
| `journal-ralph-wiggum-integration-2025-01-13.md` | Ce journal |

---

*Journal généré automatiquement par Brainstormer v4.9*
*Mis à jour avec analyse librairies frankbria + Anthropic — Iterations 10-11*
