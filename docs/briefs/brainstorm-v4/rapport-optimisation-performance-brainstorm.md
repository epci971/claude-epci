# RAPPORT D'OPTIMISATION PERFORMANCE — /brainstorm

> **Date** : 2026-01-06
> **Version analysee** : v4.2
> **Objectif** : Reduire la consommation tokens et ameliorer la performance

---

## 1. DIAGNOSTIC

### 1.1 Metriques actuelles

| Fichier | Lignes | Limite recommandee | Depassement |
|---------|--------|-------------------|-------------|
| `brainstorm.md` (commande) | **949** | 200 | **+375%** |
| `SKILL.md` (brainstormer) | 387 | 500 | OK |
| References (9 fichiers) | ~1500 | N/A | - |
| Agents (3) | 356 | N/A | - |
| **TOTAL** | **~3183** | - | - |

### 1.2 Analyse du contenu brainstorm.md

| Categorie | Lignes | % | Action recommandee |
|-----------|--------|---|-------------------|
| **CORE** (workflow principal) | ~150 | 16% | Garder |
| **CONDITIONAL** (--turbo, --random, --progressive) | ~300 | 32% | **Externaliser en references** |
| **HEAVY** (spike, techniques, energy) | ~200 | 21% | **Deleguer a agents** |
| **STATIC** (formats, exemples) | ~200 | 21% | **Externaliser** |
| **REDUNDANT** (duplique avec SKILL.md) | ~100 | 10% | **Supprimer** |

### 1.3 Problemes identifies

```
+-------------------------------------------------------------------+
|  CRITIQUE: Commande 4.7x au-dessus de la limite (949 vs 200)      |
|  CRITIQUE: Duplication commande <-> skill (~100 lignes)           |
|  MAJEUR: Context7 declare mais non utilise explicitement          |
|  MAJEUR: Modes conditionnels non externalises                     |
|  MINEUR: Agents sous-utilises (seulement @Explore, @planner)      |
+-------------------------------------------------------------------+
```

---

## 2. ARCHITECTURE CIBLE

### 2.1 Structure proposee

```
src/
+-- commands/
|   +-- brainstorm.md                    # <- REDUIRE a ~150 lignes
|
+-- commands/references/
|   +-- brainstorm-turbo-mode.md         # <- NOUVEAU (mode --turbo)
|   +-- brainstorm-random-mode.md        # <- NOUVEAU (mode --random)
|   +-- brainstorm-progressive-mode.md   # <- NOUVEAU (mode --progressive)
|   +-- brainstorm-spike-process.md      # <- NOUVEAU (processus spike)
|
+-- skills/core/brainstormer/
|   +-- SKILL.md                         # <- REDUIRE a ~200 lignes
|   +-- references/
|       +-- [existant - OK]
|
+-- agents/
    +-- clarifier.md                     # <- Existant (OK)
    +-- planner.md                       # <- Existant (OK)
    +-- security-auditor.md              # <- Existant (OK)
    +-- brainstorm-facilitator.md        # <- NOUVEAU (generation questions)
    +-- ems-evaluator.md                 # <- NOUVEAU (calcul EMS)
    +-- technique-advisor.md             # <- NOUVEAU (selection techniques)
```

### 2.2 Flux de delegation

```
brainstorm.md (point d'entree ~150 lignes)
     |
     +---> @references (modes conditionnels)
     |       +-- brainstorm-turbo-mode.md (si --turbo)
     |       +-- brainstorm-random-mode.md (si --random)
     |       +-- brainstorm-progressive-mode.md (si --progressive)
     |
     +---> Skills (progressive disclosure)
     |       +-- brainstormer/SKILL.md (~200 lignes)
     |             +-- references/ (chargees a la demande)
     |
     +---> Agents (contexte isole — economie tokens)
             +-- @Explore (codebase, existant)
             +-- @clarifier (questions turbo, existant)
             +-- @planner (plan convergent, existant)
             +-- @security-auditor (audit, existant)
             +-- @brainstorm-facilitator (questions iteratives, NOUVEAU)
             +-- @ems-evaluator (calcul EMS, NOUVEAU)
             +-- @technique-advisor (selection techniques, NOUVEAU)
```

---

## 3. NOUVEAUX AGENTS PROPOSES

### 3.1 @brainstorm-facilitator (Haiku)

**Raison** : La generation de 3-5 questions a chaque iteration consomme beaucoup de tokens dans le contexte principal. Un agent dedie isole ce travail.

```yaml
---
name: brainstorm-facilitator
description: >-
  Generates iteration questions for brainstorm sessions.
  Uses Haiku for speed. Returns 3-5 questions with A/B/C choices.
model: haiku
allowed-tools: [Read]
---

# Mission
Generer 3-5 questions de brainstorming avec choix A/B/C
basees sur le contexte actuel et les reponses precedentes.

# Input
- Brief actuel
- EMS actuel
- Phase (Divergent/Convergent)
- Historique questions/reponses

# Output
Questions formatees avec suggestions
```

**Economie estimee** : ~500 tokens/iteration x 5 iterations = **~2500 tokens/session**

### 3.2 @ems-evaluator (Haiku)

**Raison** : Le calcul EMS avec ses 5 axes est repetitif. Un agent dedie garantit la coherence et isole la logique.

```yaml
---
name: ems-evaluator
description: >-
  Calculates EMS score (5 axes) for brainstorm sessions.
  Uses Haiku for speed. Returns detailed scoring breakdown.
model: haiku
allowed-tools: [Read]
---

# Mission
Evaluer les 5 axes EMS et retourner le score composite.

# Input
- Etat actuel du brief
- Decisions prises
- Questions ouvertes

# Output
- Score par axe (Clarte, Profondeur, Couverture, Decisions, Actionnabilite)
- Score composite
- Delta depuis derniere evaluation
- Recommandations
```

**Economie estimee** : ~300 tokens/iteration x 5 iterations = **~1500 tokens/session**

### 3.3 @technique-advisor (Haiku)

**Raison** : La selection parmi 20 techniques et leur application peut etre deleguee.

```yaml
---
name: technique-advisor
description: >-
  Selects and applies brainstorming techniques based on context.
  Uses Haiku for speed. Reads technique library on demand.
model: haiku
allowed-tools: [Read]
---

# Mission
Recommander et appliquer des techniques de brainstorming
selon les axes EMS faibles et la phase courante.

# Input
- Scores EMS par axe
- Phase (Divergent/Convergent)
- Techniques deja utilisees

# Output
- Technique recommandee
- Questions types adaptees au contexte
```

**Economie estimee** : ~400 tokens quand invoque = **~400 tokens occasionnels**

---

## 4. EXTERNALISATIONS PROPOSEES

### 4.1 Fichiers references a creer

| Fichier | Contenu actuel dans brainstorm.md | Lignes |
|---------|----------------------------------|--------|
| `brainstorm-turbo-mode.md` | Section --turbo (L801-827) | ~30 |
| `brainstorm-random-mode.md` | Section --random (L829-862) | ~35 |
| `brainstorm-progressive-mode.md` | Section --progressive (L864-926) | ~65 |
| `brainstorm-spike-process.md` | Section Spike (L229-320) | ~90 |
| `brainstorm-energy-checkpoints.md` | Section Energy (L394-442) | ~50 |
| `brainstorm-session-commands.md` | Section Session Commands (L445-489) | ~45 |

**Total externalise** : ~315 lignes

### 4.2 Duplication a supprimer

La commande `brainstorm.md` duplique le workflow deja present dans `SKILL.md`:
- Question Format (lignes 140-201) -> deja dans SKILL.md
- Format Breakpoint (lignes 764-786) -> deja dans SKILL.md
- Anti-patterns -> deja dans SKILL.md

**Supprimer** : ~100 lignes de duplication

---

## 5. UTILISATION CONTEXT7

### 5.1 Situation actuelle

Context7 est mentionne dans la configuration mais **non utilise explicitement** dans le workflow :

```markdown
| **MCP** | Context7 (patterns architecture), Sequential (raisonnement complexe) |
```

### 5.2 Recommandations Context7

| Moment | Utilisation recommandee |
|--------|------------------------|
| Phase 1 (Initialisation) | Charger patterns architecture du framework detecte |
| Spike | Rechercher documentation technique de la lib concernee |
| @planner | Patterns d'implementation de la stack |
| @security-auditor | Best practices securite du framework |

**Implementation suggeree** :

```markdown
# Dans brainstorm.md
## Phase 1 — Initialisation

3. **Contexte technique (si --c7 ou auto-detect)**
   - Invoquer Context7 pour charger les patterns du framework detecte
   - Input: stack detected from @Explore
   - Output: architecture patterns, best practices

## Spike
...
2. **Documentation (si lib externe)**
   - Invoquer Context7 pour la documentation officielle
```

---

## 6. ESTIMATIONS D'ECONOMIE

### 6.1 Tokens par invocation

| Element | Avant | Apres | Economie |
|---------|-------|-------|----------|
| Commande brainstorm.md | ~3800 | ~600 | **-3200** |
| Skill SKILL.md | ~1550 | ~800 | **-750** |
| Questions iteratives (x5) | ~2500 | 0 (agent) | **-2500** |
| Calcul EMS (x5) | ~1500 | 0 (agent) | **-1500** |
| **TOTAL par session** | ~9350 | ~1400 | **-85%** |

### 6.2 Contexte preserve

L'utilisation d'agents Haiku pour les taches repetitives libere ~8000 tokens de contexte pour :
- Plus de contenu codebase
- Plus d'historique conversation
- Moins de risque de troncature

---

## 7. PLAN D'ACTION

### Phase 1 : Externalisations (Quick Wins) — ~2h

1. Creer `src/commands/references/brainstorm-turbo-mode.md`
2. Creer `src/commands/references/brainstorm-random-mode.md`
3. Creer `src/commands/references/brainstorm-progressive-mode.md`
4. Creer `src/commands/references/brainstorm-spike-process.md`
5. Modifier `brainstorm.md` pour referencer ces fichiers

### Phase 2 : Nouveaux Agents — ~3h

6. Creer `src/agents/brainstorm-facilitator.md`
7. Creer `src/agents/ems-evaluator.md`
8. Creer `src/agents/technique-advisor.md`
9. Modifier le workflow pour invoquer ces agents

### Phase 3 : Deduplication — ~1h

10. Supprimer contenu duplique de `brainstorm.md`
11. Reduire `SKILL.md` en externalisant vers references
12. Mettre a jour les liens

### Phase 4 : Context7 Integration — ~1h

13. Ajouter invocation Context7 en Phase 1
14. Ajouter invocation Context7 dans spike
15. Documenter les triggers d'activation

### Phase 5 : Validation — ~30min

16. Tester `/brainstorm` complet
17. Tester `/brainstorm --turbo`
18. Tester `/brainstorm --random`
19. Tester `/brainstorm --progressive`
20. Valider les economies tokens

---

## 8. RESUME

```
+------------------------------------------------------------------+
|  OBJECTIFS PERFORMANCE                                           |
+------------------------------------------------------------------+
|  brainstorm.md : 949 -> ~150 lignes (-84%)                       |
|  Tokens/session : ~9350 -> ~1400 (-85%)                          |
|  Contexte libere : +8000 tokens disponibles                      |
|  3 nouveaux agents Haiku (economie tokens)                       |
|  Context7 utilise explicitement                                  |
|  6 fichiers references crees (progressive disclosure)            |
+------------------------------------------------------------------+
```

---

## 9. FICHIERS ANALYSES

### 9.1 Commande principale
- `src/commands/brainstorm.md` (949 lignes)

### 9.2 Skill brainstormer
- `src/skills/core/brainstormer/SKILL.md` (387 lignes)
- `src/skills/core/brainstormer/references/brief-format.md` (263 lignes)
- `src/skills/core/brainstormer/references/ems-system.md` (150 lignes)
- `src/skills/core/brainstormer/references/frameworks.md` (225 lignes)
- `src/skills/core/brainstormer/references/personas.md` (182 lignes)
- `src/skills/core/brainstormer/references/session-format.md` (209 lignes)
- `src/skills/core/brainstormer/references/techniques/analysis.md` (172 lignes)
- `src/skills/core/brainstormer/references/techniques/breakthrough.md` (86 lignes)
- `src/skills/core/brainstormer/references/techniques/ideation.md` (137 lignes)
- `src/skills/core/brainstormer/references/techniques/perspective.md` (67 lignes)

### 9.3 Agents existants
- `src/agents/clarifier.md` (64 lignes)
- `src/agents/planner.md` (99 lignes)
- `src/agents/security-auditor.md` (193 lignes)

### 9.4 MCP Integration
- `src/skills/mcp/SKILL.md` (168 lignes)

---

*Rapport genere selon le Guide d'Optimisation des Commandes Claude Code v1.0*
