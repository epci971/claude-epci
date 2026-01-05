---
description: >-
  Brainstorming guide v4.1 pour decouvrir et specifier une feature.
  Personas adaptatifs, phases Divergent/Convergent, scoring EMS v2.
  v4.1: One-at-a-Time questions, Section-by-Section validation,
  @planner/@security-auditor integration, spike pour validation technique.
  Use when: idee vague a transformer en specs, incertitude technique a valider.
argument-hint: "[description] [--template feature|problem|decision] [--quick] [--turbo] [--no-hmw] [--no-security] [--c7] [--seq]"
allowed-tools: [Read, Write, Bash, Glob, Grep, Task, WebFetch, WebSearch]
---

# /brainstorm — Feature Discovery v4.1

## Overview

Transforme une idee vague en brief fonctionnel complet, pret pour EPCI.
Utilise l'analyse du codebase, des personas adaptatifs et des questions
iteratives pour construire des specifications exhaustives.

**Nouveau v4:** Integre l'exploration technique (spike) pour valider
la faisabilite avant de finaliser les specs.

## Usage

```
/brainstorm [description de la feature souhaitee]
```

## Exemples

```
/brainstorm systeme de notifications en temps reel
/brainstorm refonte du module d'authentification
/brainstorm dashboard analytics pour les admins
```

## Configuration

| Element | Valeur |
|---------|--------|
| **Thinking** | `think hard` (adaptatif selon complexite) |
| **Skills** | `brainstormer`, `project-memory`, `architecture-patterns`, `mcp` |
| **Subagents** | `@Explore` (codebase), `@clarifier` (turbo), `@planner` (convergent), `@security-auditor` (conditionnel) |
| **Personas** | 📐 Architecte (defaut), 🥊 Sparring, 🛠️ Pragmatique |
| **Phases** | 🔀 Divergent → 🎯 Convergent |
| **MCP** | Context7 (patterns architecture), Sequential (raisonnement complexe) |
| **v4.1** | One-at-a-Time questions, Section-by-Section validation |

## Process

### Phase 1 — Initialisation

1. **Charger le contexte projet**
   - Skill: `project-memory`
   - Si `.project-memory/` existe → charger
   - Sinon → continuer sans contexte

2. **Analyser le codebase**
   - Invoquer `@Explore` avec Task tool
   - Scan complet : structure, stack, patterns, fichiers pertinents

3. **Reformuler le besoin**
   - Paraphraser la demande utilisateur
   - Detecter template (feature/problem/decision)

4. **Initialiser session**
   - Phase → 🔀 Divergent
   - Persona → 📐 Architecte
   - EMS → ~25/100

5. **Generer HMW** (si pas `--no-hmw`)
   - 3 questions "How Might We" orientees dev
   - Permettent de cadrer l'exploration

6. **Questions de cadrage** (3-5 max)
   - Basees sur l'analyse codebase
   - Suggestions incluses quand pertinent

7. **Afficher breakpoint compact**

### Phase 2 — Iterations

Boucle jusqu'a `finish` :

**MANDATORY at EACH iteration:**

1. **Integrer les reponses** utilisateur
2. **Recalculer EMS** en utilisant la formule 5 axes de `references/ems-system.md`
   - Evaluer chaque axe (Clarte, Profondeur, Couverture, Decisions, Actionnabilite)
   - Calculer le score composite
   - Determiner le delta depuis la derniere iteration
3. **Appliquer frameworks** si pertinent (MoSCoW, 5 Whys, etc.)
4. **Generer UNE question** avec suggestion (voir One-at-a-Time pattern)
5. **Afficher breakpoint compact avec EMS visible**

**NEVER skip EMS calculation or display — it's the core metric of brainstorming progress.**

---

## One-at-a-Time Question Pattern (v4.1 — SuperPowers)

**CRITICAL: Poser UNE seule question a la fois pour reduire la charge cognitive.**

### Regles

1. **Une question par iteration** (sauf mode turbo)
2. **Choix multiples preferes** — Options claires A/B/C
3. **Suggestion incluse** — "Recommande: option B parce que..."
4. **Focus sur les blocages** — Ignorer les nice-to-have

### Format Question

```
-------------------------------------------------------
🔀 DIVERGENT | 📐 Architecte | Iter X | EMS: XX/100 (+Y)
-------------------------------------------------------
Done: [elements valides]

Question: [Question claire avec contexte]

Options:
  A) [Option 1] — [consequence]
  B) [Option 2] — [consequence] (Recommande)
  C) [Option 3] — [consequence]
  D) Autre (preciser)

-> A, B, C, D, ou reponse libre | skip | finish
-------------------------------------------------------
```

### Exemple

```
Question: Quel systeme de cache pour les sessions utilisateur?

Options:
  A) Redis — Plus rapide, necessite infra supplementaire
  B) Memcached — Simple, pas de persistence
  C) Database — Deja en place, plus lent (Recommande si < 1000 users)
  D) Autre
```

### Quand poser plusieurs questions

- Mode `--turbo` : 2-3 questions max
- Commande `batch` : Grouper les questions connexes
- Phase finale : Confirmer plusieurs points mineurs

---

**Commandes disponibles :**

| Commande | Action |
|----------|--------|
| `continue` | Question suivante |
| `batch` | Poser 3-5 questions groupees (mode classique) |
| `dive [topic]` | Approfondir un aspect specifique |
| `pivot` | Reorienter si le vrai besoin emerge |
| `status` | Afficher EMS detaille (5 axes) |
| `modes` | Afficher/changer persona |
| `mode [nom]` | Forcer un persona (architecte/sparring/pragmatique) |
| `premortem` | Lancer exercice d'anticipation des risques |
| `diverge` | Forcer phase Divergent |
| `converge` | Forcer phase Convergent + invoquer @planner |
| `scoring` | Evaluer et prioriser les idees |
| `framework [x]` | Appliquer un framework (moscow/5whys/swot) |
| `spike [duration] [question]` | Lancer exploration technique time-boxed |
| `security-check` | Invoquer @security-auditor (auto si auth/security detecte) |
| `finish` | Generer brief + journal avec validation section par section |

---

## Spike — Exploration Technique Integree

### Quand utiliser `spike`

Pendant le brainstorm, si une **incertitude technique** emerge :
- "Est-ce que l'API X peut gerer nos volumes ?"
- "GraphQL est-il adapte a notre cas ?"
- "Comment integrer Redis avec notre stack ?"

### Commande

```
spike [duration] [question technique]
```

**Exemples :**
```
spike 30min Est-ce que Stripe supporte les webhooks async ?
spike 1h GraphQL vs REST pour notre API mobile
spike 2h Integration Redis avec notre stack Django
```

### Process Spike

#### 1. Framing (5 min)

Afficher le setup avant exploration :

```markdown
-------------------------------------------------------
🔬 SPIKE MODE | [duration]
-------------------------------------------------------
**Question:** [Question technique precise]

**Criteres de succes:**
- [ ] Critere 1 (mesurable)
- [ ] Critere 2 (mesurable)

**Scope:**
- Inclus: [Ce qu'on explore]
- Exclus: [Ce qu'on n'explore pas]
-------------------------------------------------------
```

#### 2. Exploration

- Invoquer `@Explore` (thorough level)
- Lire documentation, tester hypotheses
- Creer prototypes **jetables** (pas de code production)
- Respecter strictement le time-box

**Regles :**
- Le code produit est jetable
- Documenter les decouvertes au fur et a mesure
- Rester focus sur la question initiale

#### 3. Verdict

A la fin du time-box, determiner :

| Verdict | Signification | Action |
|---------|---------------|--------|
| **GO** | Faisable, approche identifiee | Continuer brainstorm avec cette info |
| **NO-GO** | Non faisable ou trop couteux | Pivoter vers alternative |
| **MORE_RESEARCH** | Besoin d'un autre spike | Planifier spike supplementaire |

#### 4. Retour au Brainstorm

Afficher resume et reprendre :

```markdown
-------------------------------------------------------
🔬 SPIKE COMPLETE | [duration]
-------------------------------------------------------
Verdict: [GO | NO-GO | MORE_RESEARCH]

Decouvertes cles:
1. [Decouverte 1]
2. [Decouverte 2]

Impact sur le brief:
- [Ajustement 1]
- [Ajustement 2]

-> Retour au brainstorm (EMS recalcule)
-------------------------------------------------------
```

Le verdict et les decouvertes sont integres :
- Dans le **brief final** (section "Technical Validation")
- Dans le **journal** (historique du spike)

---

## @planner — Quick Plan en Phase Convergent (v4.1)

**Objectif**: Generer un plan preliminaire pour valider la faisabilite et estimer la complexite.

### Quand invoquer @planner

- **Auto**: Commande `converge` (passage en phase Convergent)
- **Auto**: EMS >= 70 et Actionnabilite >= 60
- **Manuel**: Commande `plan-preview`

### Process

1. **Invoquer @planner** via Task tool (model: sonnet)
   ```
   Input: Brief actuel + contexte codebase
   Output: Plan preliminaire avec taches atomiques
   ```

2. **Afficher le plan preview**
   ```
   -------------------------------------------------------
   📋 PLAN PREVIEW (by @planner)
   -------------------------------------------------------
   Estimated complexity: [TINY|SMALL|STANDARD|LARGE]
   Estimated tasks: X tasks
   Estimated duration: X-Y hours

   Critical path:
   1. [Task 1] (X min) → file.ext
   2. [Task 2] (X min) → file2.ext
   ...

   Risks identified:
   - [Risk 1] — [Mitigation]

   -> continue brainstorm | finish | adjust scope
   -------------------------------------------------------
   ```

3. **Integrer dans le brief**
   - Section "Preliminary Plan" avec estimation
   - Section "Estimated Complexity" mise a jour

### Avantages

- Valide la faisabilite technique pendant le brainstorm
- Detecte les risques plus tot
- Affine l'estimation de complexite (TINY → LARGE)
- Evite les surprises en Phase 1 de /epci

---

## @security-auditor — Analyse Securite Conditionnelle (v4.1)

**Objectif**: Detecter les considerations securite des la phase de specs.

### Detection Automatique

**@security-auditor est invoque automatiquement si le brief contient:**

| Pattern | Exemples |
|---------|----------|
| Auth keywords | `auth`, `login`, `password`, `jwt`, `oauth`, `session` |
| Security keywords | `security`, `permission`, `role`, `access`, `admin` |
| Data sensitive | `payment`, `stripe`, `pci`, `gdpr`, `personal data` |
| API exposed | `api public`, `webhook`, `external endpoint` |

### Process

1. **Detection** pendant Phase 2 (iteration)
   ```
   ⚠️ Security patterns detected: [auth, payment]
   -> Invoking @security-auditor for early analysis...
   ```

2. **Invoquer @security-auditor** via Task tool (model: opus)
   ```
   Input: Brief actuel + patterns detectes
   Output: Security considerations report
   ```

3. **Afficher le rapport**
   ```
   -------------------------------------------------------
   🔒 SECURITY CONSIDERATIONS (by @security-auditor)
   -------------------------------------------------------
   Risk level: [LOW|MEDIUM|HIGH|CRITICAL]

   OWASP concerns:
   - A01 (Access Control): [Concern if any]
   - A02 (Crypto): [Concern if any]
   - A03 (Injection): [Concern if any]

   Recommendations:
   1. [Recommendation 1]
   2. [Recommendation 2]

   Questions for brief:
   - [Security question to add to iteration]

   -> continue (questions added) | acknowledge | skip security
   -------------------------------------------------------
   ```

4. **Integrer dans le brief**
   - Section "Security Considerations" avec analyse
   - Questions securite ajoutees aux iterations
   - Risques securite dans Pre-mortem si applicable

### Invocation Manuelle

Commande `security-check` pour forcer l'analyse meme sans detection.

### Desactiver

Flag `--no-security` pour skipper l'analyse automatique.

---

### Phase 3 — Generation (USE WRITE TOOL)

**MANDATORY: You MUST use the Write tool to create BOTH files. Do NOT just display the content.**

---

## Section-by-Section Validation (v4.1 — SuperPowers)

**CRITICAL: Valider chaque section du brief avec l'utilisateur AVANT de passer a la suivante.**

### Process

Au lieu de generer le brief complet d'un coup, proceder section par section :

```
1. Afficher section Contexte (200-300 mots max)
   -> "Does this look right? [y/edit/skip]"

2. SI "y" -> Afficher section Objectif
   SI "edit" -> Permettre modification puis reafficher
   SI "skip" -> Passer a la section suivante

3. Continuer pour chaque section majeure:
   - Contexte ✓
   - Objectif
   - Specifications Fonctionnelles
   - Regles Metier
   - Contraintes Techniques
   - Criteres d'Acceptation

4. Une fois toutes sections validees -> Ecrire le fichier complet
```

### Format Validation Section

```
-------------------------------------------------------
📝 BRIEF SECTION: [Nom Section] (X/6)
-------------------------------------------------------

[Contenu de la section - 200-300 mots max]

-------------------------------------------------------
-> y (valider) | edit (modifier) | skip (passer)
-------------------------------------------------------
```

### Exemple

```
-------------------------------------------------------
📝 BRIEF SECTION: Contexte (1/6)
-------------------------------------------------------

Le systeme actuel de notifications utilise un pattern polling
qui consomme des ressources inutiles. Les utilisateurs ne
recoivent pas les alertes en temps reel, ce qui impacte
l'experience sur les workflows critiques (paiements, alertes).

Le projet vise a implementer un systeme push-based avec
WebSockets pour les notifications temps reel, tout en
gardant le fallback email pour les notifications non-urgentes.

-------------------------------------------------------
-> y (valider) | edit (modifier) | skip (passer)
-------------------------------------------------------
```

### Quand skipper la validation

- Flag `--quick` : Generer directement sans validation
- Flag `--turbo` : Validation groupee a la fin
- EMS >= 85 : Proposer skip de la validation

---

#### Step 3.1: Create Brief File

**USE WRITE TOOL** to create `./docs/briefs/[slug]/brief-[slug]-[date].md`:
- Format: voir `references/brief-format.md`
- **Inclure la section "Exploration Summary"** avec stack, patterns, fichiers candidats
- **Si spike effectue:** Inclure section "Technical Validation" avec verdict et decouvertes
- **Si @planner invoque:** Inclure section "Preliminary Plan" avec estimation
- **Si @security-auditor invoque:** Inclure section "Security Considerations"
- Create `./docs/briefs/[slug]` directory first if it doesn't exist (use Bash: `mkdir -p ./docs/briefs/[slug]`)

#### Step 3.2: Create Journal File

**USE WRITE TOOL** to create `./docs/briefs/[slug]/journal-[slug]-[date].md`:
- Historique des iterations
- Decisions prises
- Questions resolues
- **Si spike effectue:** Section dedicee avec details de l'exploration
- **Si agents invoques:** Section avec outputs de @planner et/ou @security-auditor

#### Step 3.3: Display Confirmation

**After BOTH files are written**, display resume final (MANDATORY format):

```
-------------------------------------------------------
✅ BRAINSTORM COMPLETE
-------------------------------------------------------
EMS Final: XX/100 [emoji]
Spikes: [X spike(s) effectue(s) | Aucun]
Agents: [@planner | @security-auditor | Aucun]

Fichiers generes:
   - Brief: ./docs/briefs/[slug]/brief-[slug]-[date].md
   - Journal: ./docs/briefs/[slug]/journal-[slug]-[date].md

Prochaine etape:
   Lancer /brief avec le contenu du brief ci-dessus.
   L'exploration ciblee affinera les fichiers impactes.
-------------------------------------------------------
```

## Format Breakpoint (compact pour CLI)

```
-------------------------------------------------------
[phase] | [persona] | Iter X | EMS: XX/100 (+Y) [emoji]
-------------------------------------------------------
Done: [elements valides]
Open: [elements a clarifier]

Questions:
1. [Question] -> Suggestion: [si applicable]
2. [Question]
3. [Question]

-> continue | dive [topic] | spike [duration] [q] | finish
-------------------------------------------------------
```

## Flags

| Flag | Effet |
|------|-------|
| `--template [name]` | Forcer template (feature/problem/decision) |
| `--no-hmw` | Desactiver generation des questions HMW |
| `--quick` | Mode rapide (3 iter max, skip section validation) |
| `--turbo` | Mode turbo: @clarifier (Haiku), max 3 iter, 2-3 questions groupees |
| `--no-security` | Desactiver @security-auditor auto-detection |
| `--no-plan` | Desactiver @planner auto-invocation en phase Convergent |

### --turbo Mode (MANDATORY Instructions)

**When `--turbo` flag is active, you MUST follow these rules:**

1. **Use @clarifier agent** (Haiku model) for generating clarification questions:
   ```
   Invoke @clarifier via Task tool with model: haiku
   Input: Current brief + codebase context
   Output: 2-3 targeted questions with suggestions
   ```

2. **Maximum 3 iterations** — Auto-finish after iteration 3

3. **Auto-accept suggestions** if EMS > 60:
   - If EMS reaches 60+, suggest `finish` proactively
   - If user provides quick confirmation ("ok", "oui", "c"), auto-accept all suggestions

4. **Reduced breakpoint** — Compact format only, skip detailed explanations

5. **Skip HMW questions** — Equivalent to `--no-hmw`

**Turbo Process:**
```
Init -> @clarifier (Haiku) -> Iter 1 -> Iter 2 -> Iter 3 (max) -> finish
                              |
                        EMS > 60? -> Auto-suggest finish
```

## Output

| Fichier | Description |
|---------|-------------|
| `./docs/briefs/[slug]/brief-[slug]-[date].md` | Brief fonctionnel EPCI-ready |
| `./docs/briefs/[slug]/journal-[slug]-[date].md` | Journal d'exploration (incluant spikes) |

## Integration EPCI

Le brief genere s'integre dans le workflow EPCI:

1. **Lancer `/brief`** avec le contenu du brief comme description
2. L'exploration ciblee (avec un brief precis) identifie les fichiers exacts
3. Le brief et le journal servent de **documentation** de la phase de decouverte

## Skills Charges

- `brainstormer` — Logique metier principale
- `project-memory` — Contexte projet
- `architecture-patterns` — Suggestions architecture
- `clarification-intelligente` — Systeme de questions
