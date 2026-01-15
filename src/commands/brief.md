---
description: >-
    Valider et reformuler un brief, explorer le codebase, évaluer la complexité,
    et router vers le workflow approprié (/quick ou /epci).
argument-hint: "[brief] [--turbo] [--rephrase] [--no-rephrase] [--no-clarify] [--c7] [--seq] [--magic] [--play]"
allowed-tools: [Read, Write, Glob, Grep, Task]
---

# EPCI Brief — Entry Point

## Overview

Cette commande est le point d'entrée unique du workflow EPCI.
Elle transforme un brief brut en brief structuré et route vers le workflow approprié.

**Principe clé**: Valider le besoin AVANT d'explorer le codebase.

## Configuration

| Element       | Value                                                                                                      |
| ------------- | ---------------------------------------------------------------------------------------------------------- |
| **Thinking**  | `think hard` (default) / `ultrathink` (LARGE ou incertitude élevée)                                        |
| **Skills**    | project-memory, epci-core, architecture-patterns, flags-system, mcp, personas, input-clarifier, [stack-skill auto-detected] |
| **Subagents** | @Explore (thorough), @clarifier (turbo mode)                                                               |

**Sélection du mode thinking:**

- `think hard`: Par défaut pour la plupart des briefs
- `ultrathink`: Quand complexité LARGE ou incertitude technique élevée

## Arguments

| Argument | Type | Requis | Description |
|----------|------|--------|-------------|
| `brief` | string | Oui | Le brief à analyser (texte ou chemin fichier) |
| `--turbo` | flag | Non | Mode rapide avec @clarifier (Haiku) |
| `--rephrase` | flag | Non | Force la reformulation du brief |
| `--no-rephrase` | flag | Non | Désactive la reformulation |
| `--no-clarify` | flag | Non | Désactive la clarification d'artefacts vocaux |
| `--c7` | flag | Non | Active Context7 MCP |
| `--seq` | flag | Non | Active Sequential MCP |
| `--magic` | flag | Non | Active Magic MCP (21st.dev) |
| `--play` | flag | Non | Active Playwright MCP |

## Flags

| Flag | Effet | Défaut |
|------|-------|--------|
| `--turbo` | Mode rapide: @clarifier Haiku, max 2 questions, breakpoints réduits | Off |
| `--rephrase` | Force la reformulation même si brief structuré | Off |
| `--no-rephrase` | Désactive reformulation, garde brief original | Off |
| `--no-clarify` | Désactive détection artefacts vocaux | Off |
| `--c7` | Active Context7 pour documentation externe | Auto |
| `--seq` | Active Sequential pour raisonnement multi-étapes | Auto |
| `--magic` | Active Magic pour génération UI | Auto |
| `--play` | Active Playwright pour tests E2E | Auto |

**Auto-activation**: Les flags MCP sont auto-activés selon les personas détectés (voir Step 3.5).

> Voir @src/commands/references/brief/turbo-mode.md pour les instructions détaillées du mode --turbo.

## Output

| Catégorie | Output | Emplacement |
|-----------|--------|-------------|
| TINY | Brief inline | Réponse directe (pas de fichier) |
| SMALL | Brief inline | Réponse directe (pas de fichier) |
| STANDARD | Feature Document | `docs/features/<slug>.md` |
| LARGE | Feature Document | `docs/features/<slug>.md` |

**Après génération**: Route automatiquement vers `/quick` (TINY/SMALL) ou `/epci` (STANDARD/LARGE).

> Voir @src/commands/references/brief/output-templates.md pour les templates détaillés.

## Process

**Suivre TOUTES les étapes en séquence. Les Steps 1 et 4 ont des BREAKPOINTS OBLIGATOIRES.**

---

### Step 0: Charger la Mémoire Projet

**Skill**: `project-memory`

Charger le contexte projet depuis `.project-memory/`. Le skill gère:

- Lecture context, conventions, settings, patterns
- Chargement métriques vélocité et historique features
- Application des défauts et affichage statut mémoire

**Si `.project-memory/` n'existe pas:** Continuer sans contexte. Suggérer `/memory init` à la fin du workflow.

---

### Step 0.5: Détection Type Input (CONDITIONNEL)

**Détecter type input et extraire contenu brief:**

```
IF input commence par "/" ou "./" ou "docs/" ou "@":
   → INPUT_TYPE = "file"
   → Lire contenu fichier avec Read tool
   → Extraire contenu brief du fichier
   → Détecter slug depuis filename ou path
ELSE:
   → INPUT_TYPE = "text"
   → Utiliser input directement comme contenu brief
```

**Gestion Input Fichier (depuis /brainstorm ou externe):**

| Source | Pattern Path | Action |
|--------|--------------|--------|
| `/brainstorm` | `docs/briefs/<slug>/brief-*.md` | Lire fichier, extraire brief structuré |
| Fichier externe | `*.md` ou `@filepath` | Lire fichier, utiliser comme brief brut |

**IMPORTANT:** Même avec input fichier depuis `/brainstorm`, Step 5 DOIT créer un Feature Document dans `docs/features/<slug>.md`. Le output brainstorm dans `docs/briefs/` est une **source**, pas le Feature Document final.

---

### Step 1: Reformulation + Validation (BREAKPOINT OBLIGATOIRE)

**BREAKPOINT OBLIGATOIRE** — Toujours affiché pour valider le besoin AVANT exploration.

> Voir @src/commands/references/brief/reformulation-process.md pour la logique détaillée de reformulation.

**Afficher ce breakpoint:**

```
┌─────────────────────────────────────────────────────────────────────┐
│ 📝 VALIDATION DU BRIEF                                              │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│ 📄 BRIEF ORIGINAL                                                   │
│ "{raw_brief}"                                                       │
│                                                                     │
│ [Si reformulé:]                                                     │
│ 📊 DÉTECTION                                                        │
│ ├── Artefacts vocaux: {COUNT} trouvés                              │
│ ├── Type détecté: {FEATURE|PROBLEM|DECISION}                       │
│ └── Reformulation: OUI                                             │
│                                                                     │
│ ✨ BRIEF REFORMULÉ                                                  │
│ ┌─────────────────────────────────────────────────────────────────┐ │
│ │ **Objectif**: {goal}                                            │ │
│ │ **Contexte**: {context}                                         │ │
│ │ **Contraintes**: {constraints}                                  │ │
│ │ **Critères de succès**: {success_criteria}                      │ │
│ └─────────────────────────────────────────────────────────────────┘ │
│                                                                     │
│ [Si NON reformulé:]                                                 │
│ ✅ Brief propre — pas de reformulation nécessaire                   │
│                                                                     │
├─────────────────────────────────────────────────────────────────────┤
│ OPTIONS:                                                            │
│   [1] Valider → Continuer vers l'exploration                       │
│   [2] Modifier → Je reformule moi-même                             │
│   [3] Annuler → Arrêter le workflow                                │
└─────────────────────────────────────────────────────────────────────┘
```

> Référence détaillée: @src/commands/references/brief/breakpoint-formats.md

**Attendre choix utilisateur:**

| Choix | Action |
|-------|--------|
| **[1] Valider** | Stocker brief validé, procéder au Step 2 |
| **[2] Modifier** | Attendre input utilisateur, mettre à jour brief, réafficher breakpoint |
| **[3] Annuler** | Arrêter workflow |

---

### Step 2: Exploration (OBLIGATOIRE)

**Exécuter hooks `pre-brief`** (si configurés dans `hooks/active/`)

**Utiliser le brief VALIDÉ du Step 1.**

**Action:** Invoquer @Explore (niveau thorough) via Task tool pour:

- Scanner structure projet complète
- Identifier toutes technologies, frameworks, versions
- Mapper patterns architecturaux (Repository, Service, Controller, etc.)
- Identifier fichiers potentiellement impactés par le brief
- Estimer dépendances et couplage
- Détecter patterns de test existants

**Sorties internes** (stocker pour Step 3):

- Liste fichiers candidats avec action probable (Create/Modify/Delete)
- Stack technique détaillé
- Patterns architecturaux détectés
- Risques identifiés

#### Gestion des Erreurs

Si @Explore échoue ou timeout:
1. Logger warning: "Exploration incomplète"
2. Continuer avec résultats partiels si disponibles
3. Marquer complexité comme UNKNOWN
4. Suggérer `--think-hard` par sécurité
5. Afficher warning dans breakpoint Step 4

---

### Step 3: Analyse & Évaluation Complexité (Interne)

**NE RIEN AFFICHER DANS CETTE ÉTAPE** — Préparer données pour le breakpoint.

Analyser brief et résultats exploration pour préparer:

#### 3.1 Évaluation Complexité

| Critère        | TINY | SMALL    | STANDARD | LARGE |
| -------------- | ---- | -------- | -------- | ----- |
| Fichiers       | 1    | 2-3      | 4-10     | 10+   |
| LOC estimé     | <50  | <200     | <1000    | 1000+ |
| Risque         | Aucun| Faible   | Moyen    | Élevé |
| Tests requis   | Non  | Optionnel| Oui      | Oui+  |
| Arch impactée  | Non  | Non      | Possible | Oui   |

**Auto-Activation Flags:**

| Condition                      | Seuil  | Flag           |
| ------------------------------ | ------ | -------------- |
| Fichiers impactés              | 3-10   | `--think`      |
| Fichiers impactés              | >10    | `--think-hard` |
| Refactoring/migration détecté  | true   | `--think-hard` |
| Patterns fichiers sensibles    | match  | `--safe`       |
| Score complexité               | >0.7   | `--wave`       |

**Patterns fichiers sensibles:**

```
**/auth/**  **/security/**  **/payment/**
**/password/**  **/api/v*/admin/**
```

#### 3.2 Questions de Clarification (2-3 max)

- Identifier lacunes, ambiguïtés, informations manquantes
- Préparer suggestions pour chaque question
- **Assigner tags priorité** (voir skill `clarification-intelligente`):
  - 🛑 Critique (bloquant) — DOIT répondre avant de continuer
  - ⚠️ Important (risque) — Recommandé, suggestion appliquée si ignoré
  - ℹ️ Information (optionnel) — Optionnel, suggestion appliquée silencieusement

#### 3.3 Suggestions IA (3-5 max)

- Recommandations architecture
- Approche implémentation
- Risques et mitigations
- Best practices spécifiques stack

#### 3.4 Détection Persona (F09)

- Scorer les 6 personas avec algorithme depuis `src/skills/personas/SKILL.md`
- `Score = (keywords × 0.4) + (files × 0.4) + (stack × 0.2)`
- Si score > 0.6: Auto-activer persona
- Si score 0.4-0.6: Suggérer persona dans breakpoint
- Inclure persona actif/suggéré dans ligne FLAGS

#### 3.5 Activation MCP (F12)

- Selon personas activés, déterminer serveurs MCP à activer
- Vérifier triggers keywords dans texte brief
- Vérifier triggers patterns fichiers dans fichiers impactés
- Vérifier triggers flags (`--c7`, `--seq`, `--magic`, `--play`, `--think-hard`)
- Auto-activer MCPs selon matrice `src/skills/mcp/SKILL.md`
- Inclure flags MCP actifs dans ligne FLAGS: `--c7 (auto: architect)`

---

### Step 4: BREAKPOINT — Revue Analyse (OBLIGATOIRE)

**OBLIGATOIRE:** Afficher ce breakpoint et ATTENDRE choix utilisateur avant de continuer.

**Afficher ce breakpoint:**

```
┌─────────────────────────────────────────────────────────────────────┐
│ ⏸️  BREAKPOINT — ANALYSE DU BRIEF                                   │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│ 📊 EXPLORATION                                                      │
│ ├── Stack détecté: {STACK}                                         │
│ ├── Fichiers impactés: {FILE_COUNT}                                │
│ ├── Patterns identifiés: {PATTERNS}                                │
│ └── Risques détectés: {RISK_COUNT}                                 │
│                                                                     │
│ 📋 QUESTIONS DE CLARIFICATION                                       │
│                                                                     │
│ Q1: {TAG_1} {question_1}                                            │
│     → Suggestion: {suggestion_1}                                    │
│                                                                     │
│ Q2: {TAG_2} {question_2}                                            │
│     → Suggestion: {suggestion_2}                                    │
│                                                                     │
│ Q3: {TAG_3} {question_3}                                            │
│     → Suggestion: {suggestion_3}                                    │
│                                                                     │
│ Légende: 🛑 Critique (obligatoire) | ⚠️ Important | ℹ️ Optionnel    │
│                                                                     │
│ 💡 SUGGESTIONS IA                                                   │
│                                                                     │
│ Architecture:                                                       │
│   • {architecture_suggestion}                                       │
│                                                                     │
│ Implémentation:                                                     │
│   • {implementation_suggestion}                                     │
│                                                                     │
│ Risques à considérer:                                               │
│   • {risk_suggestion}                                               │
│                                                                     │
│ Best practices {stack}:                                             │
│   • {stack_suggestion}                                              │
│                                                                     │
│ 📈 ÉVALUATION                                                       │
│ ├── Catégorie: {CATEGORY}                                          │
│ ├── Fichiers: {FILE_COUNT}                                         │
│ ├── LOC estimé: ~{LOC}                                             │
│ ├── Risque: {RISK_LEVEL}                                           │
│ └── Flags: {FLAGS}                                                 │
│                                                                     │
│ 🚀 COMMANDE RECOMMANDÉE: {COMMAND} {FLAGS}                         │
│                                                                     │
│ [Si STANDARD ou LARGE:]                                             │
│ 💡 TIP: Worktree recommandé                                         │
│    Pour isoler cette feature dans un worktree:                      │
│      ./src/scripts/worktree-create.sh {slug}                        │
│      cd ~/worktrees/{project}/{slug}                                │
│      claude                                                         │
│                                                                     │
├─────────────────────────────────────────────────────────────────────┤
│ OPTIONS:                                                            │
│                                                                     │
│   [1] Répondre aux questions                                        │
│       → Je fournis mes réponses aux questions de clarification     │
│                                                                     │
│   [2] Valider les suggestions                                       │
│       → J'accepte les suggestions IA telles quelles                │
│                                                                     │
│   [3] Modifier les suggestions                                      │
│       → Je veux changer certaines suggestions                      │
│                                                                     │
│   [4] Lancer {COMMAND} {FLAGS}                                      │
│       → Tout est OK, on passe à l'implémentation                   │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

> Référence détaillée: @src/commands/references/brief/breakpoint-formats.md

**Attendre réponse utilisateur.** Traiter selon choix:

| Choix            | Action                                                                                   |
| ---------------- | ---------------------------------------------------------------------------------------- |
| **[1] Répondre** | Attendre réponses utilisateur, incorporer dans brief, réafficher breakpoint              |
| **[2] Valider**  | Utiliser suggestions telles quelles, générer output (Step 5), réafficher breakpoint avec éval mise à jour |
| **[3] Modifier** | Attendre modifications, mettre à jour suggestions, réafficher breakpoint                 |
| **[4] Lancer**   | Générer output (Step 5) puis exécuter commande recommandée                               |

**Après [1], [2], ou [3]:** Mettre à jour analyse et réafficher breakpoint jusqu'à choix [4].
**Après [4]:** Procéder au Step 5 (générer output) puis Step 6 (exécuter commande).

---

### Step 5: Générer Output (OBLIGATOIRE)

**NE PAS IGNORER CETTE ÉTAPE** — OBLIGATOIRE de générer l'output approprié selon complexité.

> Voir @src/commands/references/brief/output-templates.md pour les templates détaillés et instructions critiques.

**Selon évaluation complexité:**

| Catégorie | Action | Output |
|-----------|--------|--------|
| TINY/SMALL | Générer brief inline | Réponse directe |
| STANDARD/LARGE | Créer Feature Document avec Write tool | `docs/features/<slug>.md` |

**CRITIQUE:** Utiliser Write tool, PAS EnterPlanMode. Les Feature Documents vont dans `docs/features/`, PAS dans `~/.claude/plans/`.

---

**Exécuter hooks `post-brief`** (si configurés dans `hooks/active/`)

---

### Step 6: Exécuter Commande Recommandée

**OBLIGATOIRE:** Après génération output, exécuter la commande recommandée.

**Table de routing:**

| Catégorie | Commande             | Output           | Flags typiques              |
| --------- | -------------------- | ---------------- | --------------------------- |
| TINY      | `/epci:quick --autonomous` | Brief inline | `--autonomous` (auto)      |
| SMALL     | `/epci:quick`        | Brief inline     | `--think` si 3+ fichiers    |
| STANDARD  | `/epci:epci`         | Feature Document | `--think` ou `--think-hard` |
| LARGE     | `/epci:epci --large` | Feature Document | `--think-hard --wave`       |

**Routing Optimisé TINY:**
```
IF category == TINY:
   Ignorer questions clarification (pas d'ambiguïté attendue)
   Router directement vers /quick --autonomous
   Afficher: "Mode TINY détecté → exécution autonome"
```

**Note:** `--large` est un alias pour `--think-hard --wave`. Les deux formes sont acceptées.

**Action:** Utiliser Skill tool pour exécuter la commande recommandée avec flags.

---

### Step 7: Suggestion Rules (Optionnel)

Si répertoire `.claude/` n'existe pas dans le projet:

```
💡 Aucune règle projet détectée (.claude/ absent).
   → Lancez /rules pour générer les conventions projet automatiquement.
```

Cette suggestion apparaît à la fin du breakpoint, après la commande recommandée.
L'utilisateur peut exécuter `/rules` avant ou après le workflow principal.
