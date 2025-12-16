# Feature Document — Refonte Exploration EPCI-Brief

> **Slug**: `refonte-exploration-epci-brief`
> **Catégorie**: STANDARD
> **Date**: 2024-12-16

---

## §1 — Brief Fonctionnel

### Contexte

Le workflow EPCI actuel présente une redondance dans la phase d'exploration : `epci-brief` effectue une exploration "medium" pour qualifier et router, puis `epci` Phase 1 refait une exploration via `@Plan` pour planifier. Cette double passe est inefficace et peut créer des incohérences.

La refonte vise à centraliser toute l'exploration dans `epci-brief`, qui devient le point unique de collecte d'informations sur le codebase. Les commandes en aval (`epci`, `epci-quick`) reçoivent un brief enrichi et n'explorent plus.

### Stack Détecté

- **Type**: Plugin Claude Code (Markdown commands/skills/agents)
- **Langage**: Markdown + YAML frontmatter
- **Scripts**: Python (validation)
- **Structure**: `src/commands/`, `src/skills/`, `src/agents/`

### Fichiers Impactés

| Fichier | Action | Risque | Description |
|---------|--------|--------|-------------|
| `src/commands/epci-brief.md` | Modifier | Medium | Enrichir exploration + génération §1 Feature Doc |
| `src/commands/epci.md` | Modifier | Medium | Supprimer exploration Phase 1, lire §1 existant |
| `src/commands/epci-quick.md` | Modifier | Low | Supprimer Quick Analysis, recevoir brief |
| `CLAUDE.md` | Modifier | Low | Mettre à jour documentation workflow |

### Critères d'Acceptation

- [ ] `epci-brief` effectue une exploration complète (thorough) via `@Explore`
- [ ] `epci-brief` génère le Feature Document avec §1 rempli (pour STANDARD/LARGE)
- [ ] `epci-brief` génère un brief inline structuré (pour TINY/SMALL, sans Feature Doc)
- [ ] `epci` Phase 1 lit le §1 existant sans ré-explorer
- [ ] `epci` Phase 1 passe directement à la planification (génération §2)
- [ ] `epci-quick` reçoit le brief et implémente directement (pas de Quick Analysis)
- [ ] Les modes de pensée sont optimisés selon le workflow
- [ ] Aucune régression sur les fonctionnalités existantes

### Contraintes

- **Rétrocompatibilité** : Le format du Feature Document ne change pas (§1-§4)
- **Performance** : L'exploration thorough dans `epci-brief` doit rester raisonnable
- **Modifications dans `src/`** : Ne pas toucher à `build/` (v2.7 de référence)

### Hors Scope

- Modification des subagents (`@plan-validator`, `@code-reviewer`, etc.)
- Modification des skills
- Modification de `epci-spike` (workflow déjà distinct)
- Refonte du système de hooks

### Évaluation

| Critère | Valeur |
|---------|--------|
| Catégorie | STANDARD |
| Fichiers | 4 |
| LOC estimé | ~200 (modifications nettes) |
| Risque | Medium |
| Justification | Refonte logique workflow, impact sur 3 commandes principales |

---

## §2 — Spécifications Techniques

### 2.1 Nouveau Flux de Données

```
┌─────────────────────────────────────────────────────────────────────┐
│                         epci-brief                                   │
│                                                                      │
│  ┌──────────────┐   ┌──────────────┐   ┌─────────────────────────┐  │
│  │  @Explore    │ → │ Clarify +    │ → │ Génère Output selon     │  │
│  │  (thorough)  │   │ Évalue       │   │ catégorie               │  │
│  └──────────────┘   └──────────────┘   └───────────┬─────────────┘  │
│                                                     │                │
│         ┌───────────────────────────────────────────┤                │
│         │                                           │                │
│         ▼                                           ▼                │
│  ┌─────────────────────┐                 ┌─────────────────────┐    │
│  │ TINY/SMALL          │                 │ STANDARD/LARGE      │    │
│  │ → Brief inline      │                 │ → Feature Document  │    │
│  │   (pas de fichier)  │                 │   (docs/features/)  │    │
│  └─────────────────────┘                 └─────────────────────┘    │
└─────────────────────────────────────────────────────────────────────┘
                             │
         ┌───────────────────┼───────────────────┐
         ▼                   ▼                   ▼
   ┌───────────┐       ┌───────────┐       ┌───────────┐
   │epci-quick │       │   epci    │       │epci-spike │
   │           │       │           │       │           │
   │ Brief     │       │ Lit §1    │       │ (inchangé)│
   │ inline    │       │ Feature   │       │           │
   │ → Code    │       │ Document  │       │           │
   └───────────┘       │ → §2 Plan │       └───────────┘
                       │ → §3 Code │
                       │ → §4 Final│
                       └───────────┘
```

### 2.2 Modifications `epci-brief.md`

#### Step 1: Initial Analysis (ENRICHI)

```markdown
### Step 1: Exploration Complète

**Invoke @Explore** (thorough level) to:
- Scan complete project structure
- Identify all technologies, frameworks, versions
- Map architectural patterns (Repository, Service, Controller, etc.)
- Identify files potentially impacted by the brief
- Estimate dependencies and coupling
- Detect existing test patterns

**Output interne** (pour usage dans les steps suivants):
- Liste fichiers candidats avec action probable (Create/Modify/Delete)
- Stack technique détaillé
- Patterns architecturaux détectés
- Risques identifiés
```

#### Step 5: Output (NOUVEAU - différencié par catégorie)

```markdown
### Step 5: Génération Output

#### Si TINY ou SMALL → Brief Inline

Générer un brief structuré en réponse (pas de fichier):

~~~markdown
# Brief Fonctionnel — [Title]

## Contexte
[Résumé 2-3 phrases]

## Stack
[Stack détecté]

## Fichiers Cibles
- `path/to/file.ext` (action)

## Critères d'Acceptation
- [ ] Critère mesurable

## Catégorie: [TINY|SMALL]

→ Lancer `/epci-quick`
~~~

#### Si STANDARD ou LARGE → Feature Document

Créer fichier `docs/features/<slug>.md`:

~~~markdown
# Feature Document — [Title]

## §1 — Brief Fonctionnel

### Contexte
[Résumé du besoin]

### Stack Détecté
- Framework: [detected]
- Language: [detected]
- Patterns: [detected]

### Fichiers Identifiés
| Fichier | Action | Risque |
|---------|--------|--------|
| path/to/file | Modify | Medium |

### Critères d'Acceptation
- [ ] Critère 1
- [ ] Critère 2

### Contraintes
- [Contrainte technique]

### Hors Scope
- [Exclusion explicite]

### Évaluation
- **Catégorie**: [STANDARD|LARGE]
- **Fichiers estimés**: X
- **LOC estimé**: ~Y
- **Risque**: [Low|Medium|High]

---

## §2 — Plan d'Implémentation
[À compléter par /epci Phase 1]

## §3 — Implémentation
[À compléter par /epci Phase 2]

## §4 — Finalisation
[À compléter par /epci Phase 3]
~~~

→ Proposer de lancer `/epci` ou `/epci --large`
```

#### Configuration Thinking

```markdown
### Configuration

| Element | Value |
|---------|-------|
| **Thinking** | `think hard` (STANDARD) / `ultrathink` (LARGE/incertain) |
| **Skills** | epci-core, architecture-patterns, [stack] |
| **Subagents** | @Explore (thorough) |
```

### 2.3 Modifications `epci.md`

#### Phase 1 (SIMPLIFIÉ)

```markdown
## Phase 1: Planification (anciennement "Analysis and Planning")

### Configuration

| Element | Value |
|---------|-------|
| **Thinking** | `think hard` |
| **Skills** | epci-core, architecture-patterns, [stack] |
| **Subagents** | @plan-validator |

**Note**: @Plan n'est plus invoqué - l'exploration a été faite par epci-brief.

### Process

1. **Lecture Feature Document**
   - Lire `docs/features/<slug>.md`
   - Vérifier que §1 est complet (sinon → erreur, suggérer /epci-brief)
   - Extraire: fichiers identifiés, stack, contraintes

2. **Planification directe**
   - Utiliser les fichiers identifiés dans §1
   - Décomposer en tâches atomiques (2-15 min)
   - Ordonner par dépendances
   - Associer un test à chaque tâche

3. **Validation** (via @plan-validator)
   - Soumettre plan
   - Si NEEDS_REVISION → corriger et resoumettre
   - Si APPROVED → procéder au breakpoint

4. **Mise à jour §2**
   - Écrire le plan dans le Feature Document
```

#### Suppression exploration

```markdown
### Éléments supprimés de Phase 1

- ~~Analyse technique via @Plan~~ (fait par epci-brief)
- ~~Identification fichiers impactés~~ (déjà dans §1)
- ~~Analyse dépendances~~ (déjà dans §1)
- ~~Évaluation risques techniques~~ (déjà dans §1)
```

### 2.4 Modifications `epci-quick.md`

#### Process (SIMPLIFIÉ)

```markdown
## Process

### 1. Réception Brief

Le brief structuré est fourni par `/epci-brief`.
Contient déjà:
- Fichiers cibles identifiés
- Stack détecté
- Mode (TINY/SMALL) déterminé

**Si brief absent ou incomplet** → Suggérer `/epci-brief` d'abord.

### 2. Implémentation Directe

#### TINY Mode
~~~
1. Lire fichier cible (déjà identifié)
2. Appliquer modification
3. Vérifier (lint, syntax)
4. Done
~~~

#### SMALL Mode
~~~
1. Lire fichiers concernés (déjà identifiés)
2. Pour chaque modification:
   a. Si test demandé → écrire test
   b. Implémenter
   c. Vérifier
3. Exécuter tests existants
4. Review light si besoin
~~~

### 3. Éléments supprimés

- ~~Quick Analysis~~ (fait par epci-brief)
- ~~Mode Detection~~ (fait par epci-brief)
- ~~Identify file(s) to modify~~ (déjà dans brief)
```

#### Configuration Thinking

```markdown
### Configuration

| Element | Value |
|---------|-------|
| **Thinking** | `think` (standard, pas de mode avancé) |
| **Skills** | epci-core, code-conventions, [stack] |
| **Subagents** | @code-reviewer (light, SMALL uniquement) |
```

### 2.5 Récapitulatif Modes de Pensée

| Commande | Phase | Thinking | Justification |
|----------|-------|----------|---------------|
| `epci-brief` | Exploration | `think hard` | Analyse approfondie codebase |
| `epci-brief` | Exploration (LARGE/incertain) | `ultrathink` | Complexité élevée |
| `epci` | Phase 1 - Plan | `think hard` | Planification détaillée |
| `epci` | Phase 2 - Code | `think` | Implémentation standard |
| `epci` | Phase 3 - Finalize | `think` | Finalisation standard |
| `epci --large` | Phase 1 | `ultrathink` | Planification complexe |
| `epci --large` | Phase 2-3 | `think hard` | Implémentation critique |
| `epci-quick` | Tout | `think` | Workflow rapide |

### 2.6 Mise à jour CLAUDE.md

Sections à mettre à jour:
- §3.1 Workflow EPCI : Nouveau diagramme
- §3.2 Routing : Préciser rôle epci-brief
- §3.4 Cycle de vie Feature Document : epci-brief crée §1
- §4.1 Commands : Descriptions mises à jour

---

## §2b — Plan d'Implémentation

### Fichiers Impactés

| Fichier | Action | Risque | LOC estimé |
|---------|--------|--------|------------|
| `src/commands/epci-brief.md` | Modify | Medium | +80 / -20 |
| `src/commands/epci.md` | Modify | Medium | +30 / -50 |
| `src/commands/epci-quick.md` | Modify | Low | +20 / -40 |
| `CLAUDE.md` | Modify | Low | +20 / -15 |

### Tâches

#### T1. Modifier `epci-brief.md` — Exploration enrichie (10 min)
- **Action**: Remplacer Step 1 "Initial Analysis" par "Exploration Complète"
- **Modifications précises**:
  - Ligne 20: `@Explore (medium level)` → `@Explore (thorough level)`
  - Ajouter sous-points: "Identify files potentially impacted", "Map architectural patterns", "Estimate dependencies"
- **Critères d'acceptation**:
  - [ ] @Explore niveau thorough documenté
  - [ ] Liste des outputs internes définie (fichiers, stack, patterns, risques)
- **Dépendances**: Aucune

#### T2. Modifier `epci-brief.md` — Configuration thinking (5 min)
- **Action**: Ajouter section Configuration après Overview
- **Modifications précises**:
  - Insérer tableau Configuration avec Thinking, Skills, Subagents
  - Thinking: `think hard` (défaut) / `ultrathink` (LARGE ou incertitude élevée)
- **Critères d'acceptation**:
  - [ ] Section Configuration présente avec tableau
  - [ ] Modes thinking documentés avec conditions
- **Dépendances**: T1

#### T3. Modifier `epci-brief.md` — Output différencié (10 min)
- **Action**: Remplacer section "Output" et "Transition" par "Génération Output"
- **Modifications précises**:
  - Cas TINY/SMALL: Brief inline avec sections (Contexte, Stack, Fichiers Cibles, Critères, Catégorie)
  - Cas STANDARD/LARGE: Créer `docs/features/<slug>.md` avec §1 complet + §2-§4 placeholders
  - Structure §1: Contexte, Stack Détecté, Fichiers Identifiés (tableau), Critères d'Acceptation, Contraintes, Hors Scope, Évaluation
- **Critères d'acceptation**:
  - [ ] Template brief inline défini pour TINY/SMALL
  - [ ] Template Feature Document défini avec §1 complet
  - [ ] Instructions création fichier `docs/features/` présentes
- **Dépendances**: T1, T2

#### T4. Modifier `epci.md` — Simplifier Phase 1 (10 min)
- **Action**: Refactorer Phase 1 "Analysis and Planning" → "Planification"
- **Modifications précises**:
  - Titre: "Analysis and Planning" → "Planification"
  - Supprimer ligne 76: `@Plan (native)` du tableau Subagents
  - Supprimer section "Technical analysis (via @Plan)" (lignes 86-89)
  - Remplacer "Brief reception" par "Lecture Feature Document" avec:
    - Lire `docs/features/<slug>.md`
    - Vérifier §1 complet (sinon erreur + suggérer /epci-brief)
    - Extraire fichiers, stack, contraintes depuis §1
  - Ajouter note: "@Plan n'est plus invoqué - exploration faite par epci-brief"
- **Critères d'acceptation**:
  - [ ] @Plan supprimé de la Phase 1
  - [ ] Lecture Feature Document documentée
  - [ ] Guard "§1 incomplet" présent
- **Dépendances**: T3

#### T5. Modifier `epci-quick.md` — Supprimer analyse (8 min)
- **Action**: Simplifier le process
- **Modifications précises**:
  - Supprimer section "1. Mode Detection" (lignes 40-46)
  - Supprimer section "2. Quick Analysis" (lignes 48-52)
  - Ajouter section "1. Réception Brief" avec prérequis epci-brief
  - Renommer "3. Implementation" → "2. Implémentation Directe"
  - Ajouter guard: "Si brief absent → suggérer /epci-brief"
- **Critères d'acceptation**:
  - [ ] Mode Detection supprimé
  - [ ] Quick Analysis supprimé
  - [ ] Prérequis brief documenté
  - [ ] Guard brief absent présent
- **Dépendances**: T3

#### T6. Mettre à jour `CLAUDE.md` — Documentation (7 min)
- **Action**: Synchroniser documentation avec nouvelles responsabilités
- **Modifications précises**:
  - §3.1: Mettre à jour diagramme workflow (epci-brief génère Feature Doc)
  - §3.2: Clarifier que epci-brief fait l'exploration unique
  - §3.4: epci-brief crée §1, epci commence à §2
  - §4.1: Mettre à jour descriptions des 3 commandes
- **Critères d'acceptation**:
  - [ ] Diagramme §3.1 à jour
  - [ ] Descriptions commandes cohérentes
- **Dépendances**: T4, T5

#### T7. Validation workflow (5 min)
- **Action**: Vérifier cohérence end-to-end
- **Tests**:
  - Relire les 3 commandes modifiées pour cohérence
  - Vérifier que le flux epci-brief → epci est logique
  - Vérifier que le flux epci-brief → epci-quick est logique
- **Critères d'acceptation**:
  - [ ] Pas d'incohérence entre commandes
  - [ ] Flux STANDARD/LARGE cohérent
  - [ ] Flux TINY/SMALL cohérent
- **Dépendances**: T4, T5, T6

### Risques et Mitigations

| Risque | Prob. | Impact | Mitigation concrète |
|--------|-------|--------|---------------------|
| Incohérence entre commandes | Medium | High | T7 valide la cohérence; checklist: (1) epci-brief génère §1, (2) epci lit §1 sans explorer, (3) epci-quick reçoit brief inline |
| Oubli cas edge (brief incomplet) | Low | Medium | Guards explicites dans T4 et T5: "Si §1/brief absent → erreur + suggérer /epci-brief" |
| Documentation désynchronisée | Low | Low | T6 exécuté après T4+T5; référence croisée avec commandes modifiées |

### Rollback Plan

Si problème critique détecté:
1. Les fichiers originaux sont dans git (pas de backup nécessaire)
2. `git checkout -- src/commands/epci-brief.md src/commands/epci.md src/commands/epci-quick.md`
3. CLAUDE.md peut être restauré indépendamment

### Ordre d'exécution

```
T1 → T2 → T3 ─┬→ T4 ─┬→ T6 → T7
              └→ T5 ─┘
```

### Validation

- **@plan-validator**: APPROVED (révision 2)

---

## §3 — Implémentation

### Progress
- [x] T1 — Modifier epci-brief.md (exploration enrichie)
- [x] T2 — Modifier epci-brief.md (configuration thinking)
- [x] T3 — Modifier epci-brief.md (output différencié)
- [x] T4 — Modifier epci.md (simplifier Phase 1)
- [x] T5 — Modifier epci-quick.md (supprimer analyse)
- [x] T6 — Mettre à jour CLAUDE.md
- [x] T7 — Validation workflow

### Fichiers Modifiés
| Fichier | Lignes | Description |
|---------|--------|-------------|
| `src/commands/epci-brief.md` | +85 / -30 | Exploration thorough, Configuration, Output différencié |
| `src/commands/epci.md` | +25 / -15 | Phase 1 → Planification, suppression @Plan |
| `src/commands/epci-quick.md` | +20 / -35 | Configuration, Brief Reception, suppression Mode Detection |
| `CLAUDE.md` | +30 / -20 | Diagramme, cycle de vie, descriptions |

### Reviews
- **@code-reviewer**: APPROVED (0 Critical, 2 Minor nice-to-have)
- **@security-auditor**: N/A (pas de fichiers sensibles)
- **@qa-reviewer**: N/A (pas de tests)

### Déviations
Aucune déviation par rapport au plan.

---

## §4 — Finalisation

[À compléter par /epci Phase 3]
