---
description: >-
  Brainstorming guide v4.2 pour decouvrir et specifier une feature.
  Personas adaptatifs, phases Divergent/Convergent, scoring EMS v2.
  v4.2: Session persistence, back command, energy checkpoints, 3-5 questions,
  agent confirmation [Y/n]. Spike pour validation technique.
  Use when: idee vague a transformer en specs, incertitude technique a valider.
argument-hint: "[description] [--template feature|problem|decision] [--quick] [--turbo] [--random] [--progressive] [--no-hmw] [--no-security] [--c7] [--seq]"
allowed-tools: [Read, Write, Bash, Glob, Grep, Task, WebFetch, WebSearch]
---

# /brainstorm — Feature Discovery v4.2

## Overview

Transforme une idee vague en brief fonctionnel complet, pret pour EPCI.
Utilise l'analyse du codebase, des personas adaptatifs et des questions
iteratives pour construire des specifications exhaustives.

**Nouveau v4.2:**
- **Session persistence** — Sauvegarder et reprendre les sessions (`save`, `back`)
- **Energy checkpoints** — Points de controle pour gerer la fatigue cognitive
- **3-5 questions** — Plusieurs questions par iteration avec suggestions A/B/C
- **Agent confirmation** — Prompt [Y/n] avant @planner/@security-auditor
- **Spike integre** — Exploration technique time-boxed

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
| **v4.2** | Session persistence, energy checkpoints, 3-5 questions, agent confirmation |
| **Storage** | `.project-memory/brainstorm-sessions/[slug].yaml` |

## Process

### Phase 0 — Session Detection (v4.2)

**MANDATORY: Check for existing session before starting.**

1. **Check for existing session**
   - Look in `.project-memory/brainstorm-sessions/` for matching slug
   - If found and `status: in_progress`:

```
-------------------------------------------------------
Session existante detectee: "[slug]" (EMS: XX)
   Derniere activite: [time ago]
   Phase: [phase] | Iteration: [n]

[1] Reprendre cette session
[2] Nouvelle session
-------------------------------------------------------
```

2. **If user chooses [1] Resume**:
   - Load session from YAML
   - Restore `ems`, `phase`, `persona`, `iteration`
   - Display last questions from `history`
   - Continue from where left off

3. **If user chooses [2] New**:
   - Archive existing session (rename to `{slug}-archived-{timestamp}.yaml`)
   - Start fresh Phase 1

4. **If no existing session**: Proceed to Phase 1

---

### Phase 1 — Initialisation

1. **Charger le contexte projet**
   - Skill: `project-memory`
   - Si `.project-memory/` existe → charger
   - Sinon → continuer sans contexte

2. **Analyser le codebase (parallelise)**
   - Invoquer `@Explore` avec Task tool et `run_in_background: true`
   - Scan complet : structure, stack, patterns, fichiers pertinents
   - **Continue avec etapes 3-6 pendant que @Explore tourne**
   - Integrer les resultats @Explore avant etape 7 (breakpoint)

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
3. **Appliquer frameworks/techniques** si pertinent (voir auto-suggestion)
4. **Generer 3-5 questions** avec suggestions A/B/C (voir Question Format v4.2)
5. **Afficher breakpoint compact avec EMS visible**

**NEVER skip EMS calculation or display — it's the core metric of brainstorming progress.**

---

## Question Format (v4.2)

**3-5 questions par iteration avec choix multiples A/B/C et suggestions.**

### Regles

1. **3-5 questions par iteration** (defaut v4.2)
2. **Choix multiples preferes** — Options claires A/B/C par question
3. **Suggestions incluses** — Pour chaque question quand pertinent
4. **Focus sur les blocages** — Ignorer les nice-to-have

### Format Breakpoint (v4.2)

```
-------------------------------------------------------
🔀 DIVERGENT | 📐 Architecte | Iter X | EMS: XX/100 (+Y)
-------------------------------------------------------
Done: [elements valides]
Open: [elements a clarifier]

1. [Question 1]
   A) Option A  B) Option B  C) Option C
   → Suggestion: B

2. [Question 2]
   A) Option A  B) Option B  C) Option C
   → Suggestion: A

3. [Question 3]
   A) Option A  B) Option B  C) Option C

-> continue | dive [topic] | back | save | energy | finish
-------------------------------------------------------
```

### Exemple

```
1. Quel systeme de cache pour les sessions?
   A) Redis — Plus rapide, infra supplementaire
   B) Memcached — Simple, pas de persistence
   C) Database — Deja en place, plus lent
   → Suggestion: A (si > 1000 users concurrents)

2. Strategie de refresh token?
   A) Rotation a chaque refresh
   B) Expiration fixe sans rotation
   C) Sliding window
   → Suggestion: A (securite optimale)

3. Gestion multi-device?
   A) Un token par device
   B) Token unique partage
   C) Limite configurable de devices
```

### Quand utiliser une seule question

- **Decisions complexes** — Choix architectural majeur
- **Mode `--turbo`** avec `--single` — Force une question
- **Commande `dive`** — Focus profond sur un aspect

---

**Commandes disponibles (v4.2) :**

| Commande | Action |
|----------|--------|
| `continue` | Iteration suivante (3-5 questions) |
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
| `technique [x]` | Afficher documentation complete d'une technique (v4.2) |
| `spike [duration] [question]` | Lancer exploration technique time-boxed |
| `security-check` | Invoquer @security-auditor (auto si auth/security detecte) |
| `save` | Sauvegarder session (v4.2) |
| `back` | Revenir a l'iteration precedente (v4.2) |
| `energy` | Forcer un energy check (v4.2) |
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

## Technique — Bibliotheque de Techniques (v4.2)

### Overview

Commande pour afficher la documentation complete d'une technique de brainstorming.
Contrairement a `framework [x]` qui applique un format rapide, `technique [x]` affiche
la methodologie complete avec exemples.

### Commande

```
technique [nom]
```

**Exemples:**
```
technique scamper
technique first-principles
technique six-hats
technique moscow
```

### Techniques Disponibles (20)

| Categorie | Techniques | Phase |
|-----------|------------|-------|
| **Analysis** (8) | moscow, 5whys, swot, scoring, premortem, constraint-mapping, assumption-reversal, question-storming | Convergent |
| **Ideation** (6) | scamper, six-hats, mind-mapping, what-if, analogical, first-principles | Divergent |
| **Perspective** (3) | role-playing, time-travel, reversal | Les deux |
| **Breakthrough** (3) | inner-child, chaos-engineering, nature-solutions | Deblocage |

### Output Format

```
-------------------------------------------------------
📚 TECHNIQUE: [Nom]
-------------------------------------------------------
**Description:** [2-3 lignes]

**Quand utiliser:**
- [Situation 1]
- [Situation 2]

**Phase recommandee:** [Divergent | Convergent | Deblocage]

**Questions types:**
1. [Question guidee 1]
2. [Question guidee 2]
3. [Question guidee 3]

**Exemple:**
> [Exemple concret dans contexte dev]

-> continue | appliquer | autre technique
-------------------------------------------------------
```

### Auto-suggestion

Les techniques sont suggerees automatiquement selon les axes EMS faibles:

| Axe faible | Techniques suggerees |
|------------|---------------------|
| Clarte | question-storming, 5whys |
| Profondeur | first-principles, dive |
| Couverture | scamper, six-hats |
| Decisions | moscow, scoring |
| Actionnabilite | premortem, constraint-mapping |

---

## Energy Checkpoints (v4.2)

**Objectif**: Points de controle pour gerer la fatigue cognitive et maintenir l'engagement.

### Triggers (4 conditions)

| Trigger | Condition | Raison |
|---------|-----------|--------|
| **EMS 50** | EMS atteint 50 | Mi-parcours, verification du flow |
| **EMS 75** | EMS atteint 75 | Pres de la fin, suggerer finish |
| **Iter 7+** | Iteration >= 7 sans commande | Session longue, risque de fatigue |
| **Phase change** | Divergent → Convergent | Transition importante |

### Format Energy Check

```
-------------------------------------------------------
⚡ ENERGY CHECK | EMS: XX/100 | Phase: [emoji] [phase]
-------------------------------------------------------
On a bien avance sur l'exploration. Comment tu te sens?

[1] Continuer — Je suis dans le flow
[2] Pause — Sauvegarder et reprendre plus tard
[3] Accelerer — Passons a la convergence
[4] Pivoter — Je veux changer d'angle
-------------------------------------------------------
```

### Actions par choix

| Choix | Action |
|-------|--------|
| **[1] Continuer** | Poursuivre l'iteration normale |
| **[2] Pause** | Executer `save`, afficher instructions pour reprendre |
| **[3] Accelerer** | Executer `converge`, passer en phase Convergent |
| **[4] Pivoter** | Executer `pivot`, reorienter l'exploration |

### Commande `energy`

Force un energy check a tout moment:
```
> energy
```

Utile pour:
- Faire une pause planifiee
- Evaluer son etat avant une decision importante
- Changer de direction explicitement

---

## Session Commands (v4.2)

### Commande `save`

Sauvegarde explicite de la session en cours.

```
> save

-------------------------------------------------------
💾 Session sauvegardee
   Fichier: .project-memory/brainstorm-sessions/feature-auth.yaml
   EMS: 52/100 | Phase: Divergent | Iteration: 3

   Pour reprendre: /brainstorm feature-auth
-------------------------------------------------------
```

**Auto-save**: La session est aussi sauvegardee automatiquement:
- A chaque changement de phase
- Avant `finish`
- Apres chaque energy check

### Commande `back`

Revient a l'iteration precedente.

```
> back

-------------------------------------------------------
⏪ Retour a l'iteration 2
   EMS: 38/100 (etait 52)
   Phase: Divergent

   Questions restaurees:
   1. [Question de l'iteration 2]
   2. [Question de l'iteration 2]
-------------------------------------------------------
```

**Limitations**:
- 1 step back uniquement (pas de back multiple)
- Impossible si iteration == 1
- L'historique de l'iteration annulee est conserve (peut revenir en avant avec `continue`)

---

## @planner — Quick Plan en Phase Convergent (v4.2)

**Objectif**: Generer un plan preliminaire pour valider la faisabilite et estimer la complexite.

### Quand invoquer @planner

- **Auto**: Commande `converge` (passage en phase Convergent)
- **Auto**: EMS >= 70 et Actionnabilite >= 60
- **Manuel**: Commande `plan-preview`

### Confirmation [Y/n] (v4.2)

**MANDATORY: Demander confirmation avant de lancer @planner automatiquement.**

```
-------------------------------------------------------
🎯 EMS atteint 72 — Pret pour un plan preliminaire?
   Lancer @planner? [Y/n]
-------------------------------------------------------
```

- Si **Y** (ou Enter): Invoquer @planner
- Si **n**: Continuer le brainstorm sans plan
- Si autre input: Interpreter comme reponse a la question en cours

**Note**: La confirmation n'est pas demandee pour:
- Commande manuelle `plan-preview`
- Flag `--no-confirm` (futur)

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

## @security-auditor — Analyse Securite Conditionnelle (v4.2)

**Objectif**: Detecter les considerations securite des la phase de specs.

### Detection Automatique

**@security-auditor est invoque automatiquement si le brief contient:**

| Pattern | Exemples |
|---------|----------|
| Auth keywords | `auth`, `login`, `password`, `jwt`, `oauth`, `session` |
| Security keywords | `security`, `permission`, `role`, `access`, `admin` |
| Data sensitive | `payment`, `stripe`, `pci`, `gdpr`, `personal data` |
| API exposed | `api public`, `webhook`, `external endpoint` |

### Confirmation [Y/n] (v4.2)

**MANDATORY: Demander confirmation avant de lancer @security-auditor automatiquement.**

```
-------------------------------------------------------
🔒 Patterns securite detectes: [auth, payment]
   Lancer @security-auditor? [Y/n]
-------------------------------------------------------
```

- Si **Y** (ou Enter): Invoquer @security-auditor
- Si **n**: Continuer sans analyse securite
- Si autre input: Interpreter comme reponse a la question en cours

**Note**: La confirmation n'est pas demandee pour:
- Commande manuelle `security-check`
- Flag `--no-confirm` (futur)

### Process

1. **Detection** pendant Phase 2 (iteration)
   - Patterns detectes mais confirmation demandee d'abord

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

## Section-by-Section Validation

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

## Format Breakpoint (compact pour CLI — v4.2)

```
-------------------------------------------------------
[phase] | [persona] | Iter X | EMS: XX/100 (+Y) [emoji]
-------------------------------------------------------
Done: [elements valides]
Open: [elements a clarifier]

1. [Question 1]
   A) Option A  B) Option B  C) Option C
   → Suggestion: B

2. [Question 2]
   A) Option A  B) Option B  C) Option C
   → Suggestion: A

3. [Question 3]
   A) Option A  B) Option B  C) Option C

-> continue | dive [topic] | back | save | energy | finish
-------------------------------------------------------
```

## Flags

| Flag | Effet |
|------|-------|
| `--template [name]` | Forcer template (feature/problem/decision) |
| `--no-hmw` | Desactiver generation des questions HMW |
| `--quick` | Mode rapide (3 iter max, skip section validation) |
| `--turbo` | Mode turbo: @clarifier (Haiku), max 3 iter, 2-3 questions groupees |
| `--random` | Selection aleatoire ponderee de techniques par phase |
| `--progressive` | Mode 3 phases structurees: Divergent → Transition → Convergent |
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

### --random Mode (MANDATORY Instructions)

**When `--random` flag is active, you MUST follow these rules:**

1. **Weighted technique selection** based on current phase:

   | Phase | Ideation | Perspective | Breakthrough | Analysis |
   |-------|----------|-------------|--------------|----------|
   | Divergent | 0.4 | 0.3 | 0.2 | 0.1 |
   | Convergent | 0.1 | 0.2 | 0.2 | 0.5 |

2. **Exclude used techniques** — Check `session.techniques_used` array and exclude from selection pool

3. **Update techniques_used** — After selecting a technique, add it to `session.techniques_used`

4. **Display format** at each iteration:
   ```
   -------------------------------------------------------
   🎲 RANDOM MODE | Technique: [NAME] ([CATEGORY])
   -------------------------------------------------------
   [Apply selected technique's questions to current context]
   ```

5. **Fallback behavior** — If all techniques in a category are used, expand to other categories

**Random Process:**
```
Check phase -> Calculate weights -> Filter used techniques -> Weighted random select -> Apply technique -> Update techniques_used
```

**Usage:**
```
/brainstorm --random "ameliorer le systeme de cache"
```

### --progressive Mode (MANDATORY Instructions)

**When `--progressive` flag is active, you MUST follow these rules:**

1. **Three structured phases:**

   | Phase | EMS Range | Focus | Techniques |
   |-------|-----------|-------|------------|
   | DIVERGENT | 0-49 | Exploration, generation | Ideation, Perspective, Breakthrough |
   | TRANSITION | ~50 | Energy check + summary | Forced pause |
   | CONVERGENT | 50-100 | Decisions, prioritization | Analysis |

2. **Forced transition at EMS 50:**
   - When EMS reaches 50, MUST trigger energy check
   - Display mid-session summary
   - Auto-switch to Convergent phase after validation

3. **Phase-specific technique auto-selection:**
   - Divergent: Prioritize creative techniques (SCAMPER, Six Hats, What-If)
   - Convergent: Prioritize analytical techniques (MoSCoW, Scoring, Pre-mortem)

4. **Transition checkpoint format:**
   ```
   -------------------------------------------------------
   ⚡ TRANSITION | EMS: 50/100 | Phase: 🔀 → 🎯
   -------------------------------------------------------
   Mi-parcours atteint! Resume des idees explorees:

   ✅ Valide:
   - [Idea 1]
   - [Idea 2]

   🔄 A approfondir:
   - [Idea 3]

   [1] Continuer vers Convergent
   [2] Pause — Sauvegarder
   [3] Revenir en Divergent (annuler transition)
   -------------------------------------------------------
   ```

5. **@planner availability** — Auto-available at EMS 70+ in Convergent phase

**Progressive Process:**
```
DIVERGENT (EMS 0-49)
       │
       ▼ (EMS reaches 50)
   TRANSITION
   ├── Energy check
   ├── Summary display
   └── Direction validation
       │
       ▼
CONVERGENT (EMS 50-100)
       │
       ▼ (EMS reaches 70)
   @planner available
```

**Usage:**
```
/brainstorm --progressive "nouveau module de paiement"
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
