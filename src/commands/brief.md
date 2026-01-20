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
| **Skills**    | project-memory, epci-core, architecture-patterns, flags-system, mcp, personas, input-clarifier, complexity-calculator, [stack-skill auto-detected] |
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

> Voir @references/brief/turbo-mode.md pour les instructions détaillées du mode --turbo.

## Output

| Catégorie | Output | Emplacement |
|-----------|--------|-------------|
| TINY | Brief inline | Réponse directe (pas de fichier) |
| SMALL | Brief inline | Réponse directe (pas de fichier) |
| STANDARD | Feature Document | `docs/features/<slug>.md` |
| LARGE | Feature Document | `docs/features/<slug>.md` |

**Après génération**: Route automatiquement vers `/quick` (TINY/SMALL) ou `/epci` (STANDARD/LARGE).

> Voir @references/brief/output-templates.md pour les templates détaillés.

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

> Voir @references/brief/reformulation-process.md pour la logique détaillée de reformulation.

**Invoquer le skill breakpoint-display :**

```yaml
@skill:breakpoint-display
  type: validation
  title: "VALIDATION DU BRIEF"
  data:
    original_brief: "{raw_brief}"
    reformulated: true
    reformulated_brief:
      objectif: "{goal}"
      contexte: "{context}"
      contraintes: "{constraints}"
      success_criteria: "{success_criteria}"
  ask:
    question: "Le brief vous convient-il ?"
    header: "📝 Validation"
    multiSelect: false
    options:
      - label: "Valider (Recommended)"
        description: "Continuer vers exploration"
      - label: "Modifier"
        description: "Je reformule moi-même"
      - label: "Annuler"
        description: "Arrêter workflow"
```

**Traiter selon choix:**

| Choix | Action |
|-------|--------|
| **Valider (Recommended)** | Stocker brief validé, procéder au Step 2 |
| **Modifier** | Attendre input utilisateur, mettre à jour brief, réafficher breakpoint |
| **Annuler** | Arrêter workflow |

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

### Step 2.1: Recherche Externe (CONDITIONNEL)

**Skill:** `perplexity-research`

Après @Explore, évaluer si recherche externe Perplexity est nécessaire.

```
IF @Explore detected external library NOT in Context7:
   OR @Explore detected architecture pattern requiring best practices:
   OR brief mentions emerging framework/technology:
THEN:
   @skill:perplexity-research
     trigger: "library_unknown|architecture|best_practices"
     context: "{detected_context}"
     stack: "{detected_stack}"
     specific_question: "{generated_question}"
```

**Triggers /brief:**

| Trigger | Condition |
|---------|-----------|
| `library_unknown` | Package détecté mais absent de Context7 |
| `best_practices` | Framework version récente (>= latest-1) |
| `architecture` | Keywords: microservices, distributed, event-driven |

**Skip conditions:**
- Brief catégorie TINY (trop simple)
- Tous packages dans Context7
- Flag `--no-research` (si implémenté)

**Si recherche proposée:** Le skill affiche un breakpoint `research-prompt`, l'utilisateur effectue la recherche dans Perplexity et colle les résultats, qui sont intégrés au contexte.

> Voir documentation du skill `perplexity-research` pour détails complets.

---

### Step 3: Analyse & Évaluation Complexité (Interne)

**NE RIEN AFFICHER DANS CETTE ÉTAPE** — Préparer données pour le breakpoint.

Analyser brief et résultats exploration pour préparer:

#### 3.1 Évaluation Complexité

**Skill:** `complexity-calculator`

Invoquer le skill pour calculer la catégorie de complexité :

```yaml
@skill:complexity-calculator
  input:
    brief: "{validated_brief}"
    files_impacted: [{path: "...", action: "Create|Modify|Delete"}]
    exploration_results:
      stack: "{stack_info}"
      patterns: ["{pattern1}", "{pattern2}"]
      risks: ["{risk1}", "{risk2}"]
```

Le skill retourne:
- `category`: TINY | SMALL | STANDARD | LARGE
- `score`: 0.0-1.0
- `confidence`: 0.0-1.0
- `workflow_command`: /quick | /epci
- `flags_recommended`: [flags]
- `warnings`: [warnings]

> Voir documentation du skill `complexity-calculator` pour la formule complète et les seuils.

**Auto-Activation Flags** (basé sur le résultat du skill):

| Condition                      | Seuil  | Flag           |
| ------------------------------ | ------ | -------------- |
| Fichiers impactés              | 3-10   | `--think`      |
| Fichiers impactés              | >10    | `--think-hard` |
| Refactoring/migration détecté  | true   | `--think-hard` |
| Risk factor détecté            | match  | `--safe`       |
| Score complexité               | >0.7   | `--wave`       |

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

- Scorer les 6 personas avec algorithme du skill `personas`
- `Score = (keywords × 0.4) + (files × 0.4) + (stack × 0.2)`
- Si score > 0.6: Auto-activer persona
- Si score 0.4-0.6: Suggérer persona dans breakpoint
- Inclure persona actif/suggéré dans ligne FLAGS

#### 3.5 Activation MCP (F12)

- Selon personas activés, déterminer serveurs MCP à activer
- Vérifier triggers keywords dans texte brief
- Vérifier triggers patterns fichiers dans fichiers impactés
- Vérifier triggers flags (`--c7`, `--seq`, `--magic`, `--play`, `--think-hard`)
- Auto-activer MCPs selon matrice du skill `mcp`
- Inclure flags MCP actifs dans ligne FLAGS: `--c7 (auto: architect)`

---

### Step 4: BREAKPOINT — Revue Analyse (OBLIGATOIRE)

**OBLIGATOIRE:** Afficher ce breakpoint et ATTENDRE choix utilisateur avant de continuer.

**Invoquer le skill breakpoint-display :**

```yaml
@skill:breakpoint-display
  type: analysis
  title: "ANALYSE DU BRIEF"
  data:
    exploration:
      stack: "{STACK}"
      files_impacted: {FILE_COUNT}
      patterns: ["{pattern1}", "{pattern2}"]
      risks: ["{risk1}", "{risk2}"]
    questions:
      - tag: "🛑"
        text: "{question_text}"
        suggestion: "{suggestion}"
      - tag: "⚠️"
        text: "{question_text}"
        suggestion: "{suggestion}"
    suggestions:
      architecture: "{architecture_suggestion}"
      implementation: "{implementation_suggestion}"
      risks: "{risk_suggestion}"
      stack_specific: "{stack_best_practices}"
    personas:
      active:
        - name: "{persona_name}"
          score: {0.XX}
          source: "auto"
      suggested:
        - name: "{persona_name}"
          score: {0.XX}
    mcp_servers:
      active:
        - server: "{c7|seq|magic|play}"
          source: "{persona_name|keyword|flag}"
      available: ["{server1}", "{server2}"]
    evaluation:
      category: "{TINY|SMALL|STANDARD|LARGE}"
      files: {FILE_COUNT}
      loc_estimate: {LOC}
      risk: "{LOW|MEDIUM|HIGH}"
      flags: ["{flag1}", "{flag2}"]
    recommended_command: "{COMMAND} {FLAGS}"
  ask:
    question: "Comment souhaitez-vous procéder avec cette analyse ?"
    header: "🚀 Action"
    multiSelect: false
    options:
      - label: "Répondre questions"
        description: "Je fournis réponses clarification"
      - label: "Valider suggestions (Recommended)"
        description: "J'accepte suggestions IA telles quelles"
      - label: "Modifier suggestions"
        description: "Je veux changer certaines suggestions"
      - label: "Lancer {COMMAND}"
        description: "Tout OK, passer implémentation"
```

**Traiter selon choix:**

| Choix | Action |
|-------|--------|
| **Répondre questions** | Attendre réponses utilisateur, incorporer dans brief, réafficher breakpoint |
| **Valider suggestions (Recommended)** | Utiliser suggestions telles quelles, générer output (Step 5), réafficher breakpoint avec éval mise à jour |
| **Modifier suggestions** | Attendre modifications, mettre à jour suggestions, réafficher breakpoint |
| **Lancer {COMMAND}** | Générer output (Step 5) puis exécuter commande recommandée |

**Après premiers 3 choix:** Mettre à jour analyse et réafficher breakpoint jusqu'à choix final.
**Après choix "Lancer":** Procéder au Step 5 (générer output) puis Step 6 (exécuter commande).

---

### Step 5: Générer Output (OBLIGATOIRE)

**NE PAS IGNORER CETTE ÉTAPE** — OBLIGATOIRE de générer l'output approprié selon complexité.

> Voir @references/brief/output-templates.md pour les templates détaillés et instructions critiques.

```
╔══════════════════════════════════════════════════════════════════════════════╗
║ ⚠️  GARDE ANTI-PLAN-NATIF — VERIFICATION OBLIGATOIRE                         ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║ AVANT d'écrire quoi que ce soit, VÉRIFIER :                                  ║
║                                                                              ║
║ ❌ SI output_path contient ".claude/plans" OU "~/.claude/plans":             ║
║    → ERREUR: Mauvais chemin détecté                                          ║
║    → STOP et utiliser docs/features/<slug>.md à la place                     ║
║                                                                              ║
║ ❌ SI tu es tenté d'utiliser EnterPlanMode:                                  ║
║    → ERREUR: Mauvais outil                                                   ║
║    → STOP et utiliser Write tool à la place                                  ║
║                                                                              ║
║ ✅ SEUL chemin autorisé: docs/features/<slug>.md                             ║
║ ✅ SEUL outil autorisé: Write tool                                           ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

**Selon évaluation complexité:**

| Catégorie | Action | Output |
|-----------|--------|--------|
| TINY/SMALL | Générer brief inline | Réponse directe |
| STANDARD/LARGE | Créer Feature Document avec **Write tool** | `docs/features/<slug>.md` |

**CRITIQUE:**
- Utiliser **Write tool**, PAS EnterPlanMode
- Les Feature Documents vont dans **`docs/features/`**, PAS dans `~/.claude/plans/`
- **JAMAIS** basculer en mode plan natif pendant `/brief`

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
