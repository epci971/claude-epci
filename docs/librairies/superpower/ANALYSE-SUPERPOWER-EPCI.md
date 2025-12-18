# Analyse Exhaustive du Plugin SuperPower pour Intégration EPCI

> **Date** : 2024-12-18
> **Version analysée** : SuperPower v4.0.0
> **Objectif** : Identifier les éléments pertinents à intégrer dans le plugin EPCI

---

## Table des Matières

1. [Vue d'Ensemble](#1-vue-densemble)
2. [Cartographie des Skills (EF1)](#2-cartographie-des-skills-ef1)
3. [Système de Hooks (EF2)](#3-système-de-hooks-ef2)
4. [Commandes Slash (EF3)](#4-commandes-slash-ef3)
5. [Workflow Subagent-Driven-Development (EF4)](#5-workflow-subagent-driven-development-ef4)
6. [Système de Découverte de Skills (EF5)](#6-système-de-découverte-de-skills-ef5)
7. [Comparaison EPCI vs SuperPower](#7-comparaison-epci-vs-superpower)
8. [Recommandations d'Intégration EPCI (EF6)](#8-recommandations-dintégration-epci-ef6)

---

## 1. Vue d'Ensemble

### 1.1 Philosophie SuperPower

SuperPower transforme Claude Code en "développeur senior" via un système de skills composables qui s'activent automatiquement selon le contexte. Les principes fondamentaux sont :

| Principe | Description |
|----------|-------------|
| **TDD avant tout** | Écrire les tests d'abord, toujours |
| **Systématique vs ad-hoc** | Process structuré plutôt que devinettes |
| **Réduction de complexité** | Simplicité comme objectif premier |
| **Evidence over claims** | Vérifier avant de déclarer succès |

### 1.2 Architecture Globale

```
superpowers/
├── .claude-plugin/
│   └── plugin.json          # Manifest v4.0.0
├── hooks/
│   ├── hooks.json           # Configuration hooks
│   └── session-start.sh     # Injection contexte initial
├── commands/                 # 3 commandes slash
│   ├── brainstorm.md
│   ├── write-plan.md
│   └── execute-plan.md
├── skills/                   # 14 skills (dossiers)
│   ├── using-superpowers/   # Meta-skill d'entrée
│   ├── brainstorming/
│   ├── writing-plans/
│   ├── executing-plans/
│   ├── subagent-driven-development/
│   ├── test-driven-development/
│   ├── systematic-debugging/
│   ├── verification-before-completion/
│   ├── requesting-code-review/
│   ├── receiving-code-review/
│   ├── dispatching-parallel-agents/
│   ├── using-git-worktrees/
│   ├── finishing-a-development-branch/
│   └── writing-skills/
├── agents/
│   └── code-reviewer.md     # Subagent custom
├── lib/
│   └── skills-core.js       # Module partagé
└── tests/                    # Infrastructure de test
    ├── skill-triggering/
    ├── claude-code/
    └── subagent-driven-dev/
```

### 1.3 Workflow Principal

```
Idée brute
    │
    ▼
/brainstorm (skill: brainstorming)
    │ Questions socratiques, validation incrémentale
    ▼
Design validé → docs/plans/YYYY-MM-DD-<topic>-design.md
    │
    ▼
/write-plan (skill: writing-plans) + git worktree
    │ Plan bite-sized (2-5 min/tâche)
    ▼
Plan validé → docs/plans/YYYY-MM-DD-<feature>.md
    │
    ├──► Option A: /execute-plan (executing-plans)
    │      Batch de 3 tâches + checkpoint humain
    │
    └──► Option B: subagent-driven-development
           Subagent par tâche + double review automatique
    │
    ▼
finishing-a-development-branch
    │ Merge/PR/Keep/Discard
    ▼
Feature terminée
```

---

## 2. Cartographie des Skills (EF1)

### 2.1 Skills par Catégorie

#### Testing (1 skill + fichiers support)

| Skill | Déclencheur | Comportement | Pertinence EPCI |
|-------|-------------|--------------|-----------------|
| **test-driven-development** | Implémentation de feature/bugfix | RED-GREEN-REFACTOR strict, Iron Law "NO PRODUCTION CODE WITHOUT FAILING TEST" | **5/5** |
| ↳ testing-anti-patterns.md | Lors d'écriture de mocks | 5 anti-patterns documentés avec gate functions | **4/5** |

#### Debugging (1 skill + fichiers support)

| Skill | Déclencheur | Comportement | Pertinence EPCI |
|-------|-------------|--------------|-----------------|
| **systematic-debugging** | Bug, test failure, comportement inattendu | 4 phases obligatoires, Iron Law "NO FIXES WITHOUT ROOT CAUSE" | **5/5** |
| ↳ root-cause-tracing.md | Bug profond dans call stack | Traçage backward jusqu'à la source | **4/5** |
| ↳ defense-in-depth.md | Après fix d'un bug | Validation à 4 couches | **4/5** |
| ↳ condition-based-waiting.md | Tests flaky, race conditions | Polling conditionnel vs timeouts arbitraires | **4/5** |

#### Collaboration (9 skills)

| Skill | Déclencheur | Comportement | Pertinence EPCI |
|-------|-------------|--------------|-----------------|
| **brainstorming** | Création feature, composant, modification comportement | Questions socratiques 1 à la fois, design en sections 200-300 mots | **5/5** |
| **writing-plans** | Spec validée, avant code | Plan bite-sized (2-5 min/step), TDD, YAGNI, DRY | **5/5** |
| **executing-plans** | Plan écrit, session parallèle | Batch de 3 tâches + checkpoint humain | **4/5** |
| **subagent-driven-development** | Plan écrit, même session | Subagent/tâche + double review (spec + quality) | **5/5** |
| **dispatching-parallel-agents** | 2+ tâches indépendantes | Un agent par domaine problème, exécution parallèle | **4/5** |
| **requesting-code-review** | Après task/feature majeure | Dispatch code-reviewer avec template SHA | **4/5** |
| **receiving-code-review** | Réception feedback | Vérification technique, pas d'accord performatif | **3/5** |
| **using-git-worktrees** | Début feature isolée | Création worktree, .gitignore check, baseline tests | **4/5** |
| **finishing-a-development-branch** | Implémentation complète | 4 options (Merge/PR/Keep/Discard) + cleanup | **4/5** |

#### Meta (2 skills)

| Skill | Déclencheur | Comportement | Pertinence EPCI |
|-------|-------------|--------------|-----------------|
| **using-superpowers** | Début conversation | Règle absolue: check skills AVANT toute réponse | **5/5** |
| **writing-skills** | Création/édition de skills | TDD appliqué à la documentation, pressure testing | **5/5** |

### 2.2 Mécanismes Clés par Skill

#### using-superpowers — Le "Gardien"

**Concept innovant** : Injection automatique au démarrage via hook `SessionStart`. Crée une obligation psychologique de consulter les skills.

```markdown
<EXTREMELY-IMPORTANT>
If you think there is even a 1% chance a skill might apply to what you are doing,
you ABSOLUTELY MUST read the skill.

IF A SKILL APPLIES TO YOUR TASK, YOU DO NOT HAVE A CHOICE. YOU MUST USE IT.
</EXTREMELY-IMPORTANT>
```

**Red Flags Table** — Pensées qui signalent rationalisation :

| Pensée | Réalité |
|--------|---------|
| "This is just a simple question" | Questions are tasks. Check for skills. |
| "I need more context first" | Skill check comes BEFORE clarifying questions. |
| "Let me explore the codebase first" | Skills tell you HOW to explore. Check first. |

#### test-driven-development — Iron Laws

```
NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST
```

**Différenciateur** : Table exhaustive de "Common Rationalizations" avec réponses directes. Chaque excuse anticipée = contre-argument documenté.

| Excuse | Reality |
|--------|---------|
| "Too simple to test" | Simple code breaks. Test takes 30 seconds. |
| "I'll test after" | Tests passing immediately prove nothing. |
| "TDD is dogmatic, being pragmatic means adapting" | TDD IS pragmatic: finds bugs before commit. |

#### verification-before-completion — Gate Function

**Concept innovant** : "Gate Function" — workflow obligatoire avant toute claim de succès.

```
BEFORE claiming any status or expressing satisfaction:
1. IDENTIFY: What command proves this claim?
2. RUN: Execute the FULL command (fresh, complete)
3. READ: Full output, check exit code, count failures
4. VERIFY: Does output confirm the claim?
5. ONLY THEN: Make the claim

Skip any step = lying, not verifying
```

#### writing-skills — TDD pour Documentation

**Concept innovant** : Appliquer RED-GREEN-REFACTOR aux skills eux-mêmes.

| TDD Concept | Skill Creation |
|-------------|----------------|
| Test case | Pressure scenario avec subagent |
| Production code | Document SKILL.md |
| Test fails (RED) | Agent viole règle sans skill |
| Test passes (GREEN) | Agent comply avec skill |
| Refactor | Close loopholes |

**Pressure Types** pour tests :

| Type | Exemple |
|------|---------|
| Time | Emergency, deadline |
| Sunk cost | Hours of work to delete |
| Authority | Senior says skip it |
| Exhaustion | End of day |
| Social | Looking dogmatic |

---

## 3. Système de Hooks (EF2)

### 3.1 Configuration (`hooks/hooks.json`)

```json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "startup|resume|clear|compact",
        "hooks": [
          {
            "type": "command",
            "command": "\"${CLAUDE_PLUGIN_ROOT}/hooks/run-hook.cmd\" session-start.sh"
          }
        ]
      }
    ]
  }
}
```

### 3.2 Hook SessionStart

**Rôle** : Injecter le contenu de `using-superpowers` dans le contexte dès le démarrage.

**Mécanisme** :
1. Lit `skills/using-superpowers/SKILL.md`
2. Vérifie migration legacy (`~/.config/superpowers/skills`)
3. Retourne JSON avec `additionalContext` injecté

```bash
cat <<EOF
{
  "hookSpecificOutput": {
    "hookEventName": "SessionStart",
    "additionalContext": "<EXTREMELY_IMPORTANT>\nYou have superpowers.\n\n${using_superpowers_content}\n</EXTREMELY_IMPORTANT>"
  }
}
EOF
```

### 3.3 Comparaison avec EPCI Hooks (v3.1)

| Aspect | SuperPower | EPCI v3.1 |
|--------|------------|-----------|
| **Points de hook** | SessionStart uniquement | pre/post-phase-1/2/3, on-breakpoint |
| **Objectif** | Injection contexte | Extensibilité workflow |
| **Format** | JSON stdout | JSON stdin/stdout |
| **Activation** | Automatique (plugin) | Symlinks dans `active/` |

**Observation** : SuperPower utilise un seul hook critique, EPCI a un système plus complet mais sous-exploité.

---

## 4. Commandes Slash (EF3)

### 4.1 Architecture des Commandes

Les commandes SuperPower sont des **thin wrappers** qui délèguent aux skills.

| Commande | Fichier | Contenu |
|----------|---------|---------|
| `/superpowers:brainstorm` | `commands/brainstorm.md` | "Use and follow the brainstorming skill exactly as written" |
| `/superpowers:write-plan` | `commands/write-plan.md` | "Use the writing-plans skill exactly as written" |
| `/superpowers:execute-plan` | `commands/execute-plan.md` | "Use the executing-plans skill exactly as written" |

### 4.2 Pattern de Description

```yaml
---
description: "You MUST use this before any creative work - creating features,
              building components, adding functionality, or modifying behavior.
              Explores requirements and design before implementation."
---
```

**Observation** : Descriptions impératives avec déclencheurs explicites, pas de résumé du workflow (évite le "Description Trap").

### 4.3 Comparaison avec EPCI

| Aspect | SuperPower | EPCI v3.0 |
|--------|------------|-----------|
| **Nombre** | 3 | 5 |
| **Pattern** | Délégation pure aux skills | Logique inline |
| **Frontmatter** | Description seule | Description + argument-hint + allowed-tools |
| **Taille** | ~6 lignes | ~200-500 lignes |

---

## 5. Workflow Subagent-Driven-Development (EF4)

### 5.1 Architecture du Workflow

```
Plan validé
    │
    ├─► Controller lit plan UNE FOIS
    │   Extrait TOUTES les tâches avec texte complet
    │   Crée TodoWrite
    │
    ▼ Pour chaque tâche
    │
    ├─► Dispatch IMPLEMENTER subagent
    │   │ Prompt: implementer-prompt.md
    │   │ Reçoit: full task text + context
    │   │ Peut: poser questions AVANT et PENDANT
    │   │
    │   ├─► Questions? → Controller répond → Continue
    │   │
    │   └─► Implémente → Tests → Commit → Self-review
    │
    ├─► Dispatch SPEC REVIEWER subagent
    │   │ Prompt: spec-reviewer-prompt.md
    │   │ Vérifie: code matches spec EXACTLY
    │   │ NE TRUST PAS le rapport de l'implementer
    │   │
    │   ├─► Issues? → Implementer fix → Re-review
    │   │
    │   └─► ✅ Spec compliant
    │
    └─► Dispatch CODE QUALITY REVIEWER subagent
        │ Prompt: code-quality-reviewer-prompt.md
        │ Vérifie: clean, tested, maintainable
        │
        ├─► Issues? → Implementer fix → Re-review
        │
        └─► ✅ Approved → Mark task complete
    │
    ▼ Plus de tâches?
    │
    ├─► Oui → Prochaine tâche
    │
    └─► Non → Final code-reviewer → finishing-a-development-branch
```

### 5.2 Prompts Templates

#### implementer-prompt.md (Extraits clés)

```markdown
## Before You Begin

If you have questions about:
- The requirements or acceptance criteria
- The approach or implementation strategy
- Dependencies or assumptions

**Ask them now.** Raise any concerns before starting work.

## Before Reporting Back: Self-Review

Review your work with fresh eyes. Ask yourself:

**Completeness:**
- Did I fully implement everything in the spec?
- Did I miss any requirements?

**Quality:**
- Is this my best work?
- Are names clear and accurate?

**Discipline:**
- Did I avoid overbuilding (YAGNI)?
- Did I follow existing patterns in the codebase?
```

#### spec-reviewer-prompt.md (Extraits clés)

```markdown
## CRITICAL: Do Not Trust the Report

The implementer finished suspiciously quickly. Their report may be incomplete,
inaccurate, or optimistic. You MUST verify everything independently.

**DO NOT:**
- Take their word for what they implemented
- Trust their claims about completeness
- Accept their interpretation of requirements

**DO:**
- Read the actual code they wrote
- Compare actual implementation to requirements line by line
```

### 5.3 Différenciateurs Clés

| Aspect | Valeur Ajoutée |
|--------|----------------|
| **Double review** | Spec compliance PUIS code quality (ordre critique) |
| **Skeptical reviewer** | Ne trust pas le rapport implementer |
| **Questions encouraged** | Avant ET pendant le travail |
| **Self-review** | Checklist avant report |
| **Full context** | Controller fournit texte complet, pas de lecture fichier |
| **Review loops** | Issues → Fix → Re-review jusqu'à approval |

### 5.4 Comparaison avec EPCI Subagents

| Aspect | SuperPower | EPCI v3.0 |
|--------|------------|-----------|
| **Pattern** | Controller + Workers | Invocation ponctuelle |
| **Review stages** | 2 (spec + quality) | 1 (conditionnel) |
| **Prompts** | Templates externalisés | Inline |
| **Loops** | Review → Fix → Re-review | One-shot |
| **Context** | Texte complet fourni | Lecture fichier |

---

## 6. Système de Découverte de Skills (EF5)

### 6.1 Mécanisme de Découverte (`lib/skills-core.js`)

```javascript
function resolveSkillPath(skillName, superpowersDir, personalDir) {
  // Strip superpowers: prefix if present
  const forceSuperpowers = skillName.startsWith('superpowers:');
  const actualSkillName = forceSuperpowers ? skillName.replace(/^superpowers:/, '') : skillName;

  // Try personal skills first (unless explicitly superpowers:)
  if (!forceSuperpowers && personalDir) {
    const personalSkillFile = path.join(personalDir, actualSkillName, 'SKILL.md');
    if (fs.existsSync(personalSkillFile)) {
      return { skillFile: personalSkillFile, sourceType: 'personal' };
    }
  }

  // Try superpowers skills
  if (superpowersDir) {
    const superpowersSkillFile = path.join(superpowersDir, actualSkillName, 'SKILL.md');
    if (fs.existsSync(superpowersSkillFile)) {
      return { skillFile: superpowersSkillFile, sourceType: 'superpowers' };
    }
  }

  return null;
}
```

### 6.2 Shadowing (Personal > Plugin)

**Pattern** : Les skills personnels (`~/.claude/skills/`) peuvent override les skills SuperPower.

```
Priorité de résolution:
1. Personal skills (~/.claude/skills/<name>/)
2. Plugin skills (superpowers/skills/<name>/)

Exception: Préfixe explicite superpowers: force le plugin
```

### 6.3 Claude Search Optimization (CSO)

**Concept innovant** : Optimiser les descriptions pour que Claude trouve les skills pertinents.

**Règles clés** :

1. **Description = WHEN, pas WHAT**
   ```yaml
   # ❌ BAD: Summarizes workflow
   description: Use when executing plans - dispatches subagent per task with code review

   # ✅ GOOD: Triggering conditions only
   description: Use when executing implementation plans with independent tasks
   ```

2. **Keyword Coverage**
   - Messages d'erreur: "Hook timed out", "race condition"
   - Symptômes: "flaky", "hanging", "zombie"
   - Synonymes: "timeout/hang/freeze"

3. **Token Efficiency**
   - getting-started: < 150 mots
   - Skills fréquents: < 200 mots
   - Autres: < 500 mots

### 6.4 Tests de Triggering

**Infrastructure** (`tests/skill-triggering/`) :

```bash
./run-test.sh systematic-debugging ./prompts/systematic-debugging.txt
```

**Prompts naïfs** (sans mention explicite du skill) :

```text
# systematic-debugging.txt
I have a test that's failing intermittently. Sometimes it passes, sometimes
it fails with "timeout waiting for response". The test worked fine yesterday.
I've tried increasing the timeout but that didn't help. What should I do?
```

**Validation** : Le skill doit se déclencher sans être nommé.

---

## 7. Comparaison EPCI vs SuperPower

### 7.1 Tableau Comparatif Global

| Dimension | EPCI v3.0 | SuperPower v4.0 |
|-----------|-----------|-----------------|
| **Philosophie** | Phases séquentielles (E→P→C→I) | Skills composables auto-activés |
| **Point d'entrée** | `/epci-brief` | Hook SessionStart + skills |
| **Routing** | Par complexité (TINY→LARGE) | Par symptôme/contexte |
| **Feature Document** | Obligatoire STANDARD+ | Design + Plan (séparés) |
| **TDD** | Recommandé | Iron Law obligatoire |
| **Subagents** | 5 customs (ponctuel) | Pattern Controller/Workers |
| **Review** | 1 stage conditionnel | 2 stages obligatoires |
| **Skills** | 14 (core+stack+factory) | 14 (process-focused) |
| **Hooks** | 7 points de phase | 1 point (SessionStart) |
| **Auto-activation** | Via description | Via using-superpowers gardien |

### 7.2 Forces Relatives

| Aspect | Avantage EPCI | Avantage SuperPower |
|--------|---------------|---------------------|
| **Structure** | Phases claires, BREAKPOINTS | Flexibilité contextuelle |
| **Routing** | Classification par complexité | Activation par symptôme |
| **Documentation** | Feature Document unifié | Design + Plan séparés |
| **Extensibilité** | Component Factory | CSO + shadowing |
| **Hooks** | Plus de points d'extension | Plus simple |
| **TDD** | — | Enforcement plus strict |
| **Subagents** | Plus de rôles spécialisés | Double review systématique |
| **Vérification** | — | Gate Function avant claims |
| **Stack** | Skills par technologie | Process-agnostic |

---

## 8. Recommandations d'Intégration EPCI (EF6)

### 8.1 Priorité 1 — Intégration Immédiate (Haute Valeur, Faible Effort)

#### R1.1 — Gate Function de Vérification

**Source** : `verification-before-completion`

**Justification** : Empêche les claims de succès non vérifiées, problème fréquent en EPCI.

**Implémentation** :
```markdown
# Dans epci.md Phase 2 et Phase 3

## Gate Function — Avant toute claim de complétion

BEFORE claiming "Phase complete" or "Tests pass":
1. IDENTIFY: What command proves this claim?
2. RUN: Execute the FULL command
3. READ: Full output, check exit code
4. VERIFY: Does output confirm the claim?
5. ONLY THEN: Update Feature Document

Skip any step = phase non complète
```

**Effort** : 1-2h
**Impact** : Élevé (qualité des livrables)

#### R1.2 — Table de Rationalisations dans Testing Strategy

**Source** : `test-driven-development`

**Justification** : Renforce l'adhésion TDD avec des contre-arguments préparés.

**Implémentation** : Ajouter dans `skills/core/testing-strategy/SKILL.md`

```markdown
## Rationalisations Courantes et Réalités

| Excuse | Réalité |
|--------|---------|
| "Trop simple pour tester" | Le code simple casse. Le test prend 30 secondes. |
| "Je testerai après" | Les tests passant immédiatement ne prouvent rien. |
| "J'ai déjà testé manuellement" | Pas de trace, pas de re-run possible. |
| "Effacer X heures est gaspilleur" | Sunk cost fallacy. Le code non vérifié est dette technique. |
```

**Effort** : 1h
**Impact** : Moyen (discipline développeur)

#### R1.3 — Red Flags dans Using-Superpowers Pattern

**Source** : `using-superpowers`

**Justification** : Le skill `epci-core` devrait avoir un mécanisme similaire de "gardien".

**Implémentation** : Ajouter dans `skills/core/epci-core/SKILL.md`

```markdown
## Red Flags — Pensées qui signalent un problème

Si vous pensez :
- "C'est juste une petite modification" → Vérifier quand même le workflow
- "Je connais déjà la solution" → L'exploration peut révéler des contraintes
- "Pas besoin de Feature Document" → Si >3 fichiers, si oui.
- "Les tests passeront" → Exécuter AVANT de claim

Ces pensées = STOP et reconsidérer.
```

**Effort** : 1h
**Impact** : Moyen (prévention erreurs)

### 8.2 Priorité 2 — Intégration Moyenne Terme (Haute Valeur, Effort Modéré)

#### R2.1 — Double Review Stage en Phase 2

**Source** : `subagent-driven-development`

**Justification** : La review unique rate souvent le delta spec vs implémentation.

**Implémentation** :
1. Créer `agents/spec-reviewer.md` (adapté du template SuperPower)
2. Modifier `/epci` Phase 2 pour invoquer :
   - D'abord `@spec-reviewer` (conformité spec)
   - Puis `@code-reviewer` (qualité code)
3. Ajouter boucle fix → re-review

```yaml
# agents/spec-reviewer.md
---
name: spec-reviewer
description: Vérifie que l'implémentation correspond EXACTEMENT au §2 du Feature Document
allowed-tools: [Read, Grep]
---

## CRITIQUE: Ne pas faire confiance au rapport

L'implémenteur a peut-être fini trop vite. Son rapport peut être incomplet.

**FAIRE:**
- Lire le code réel écrit
- Comparer ligne par ligne avec les requirements du §2
- Chercher les requirements manquants ET le sur-engineering

**Report:**
- ✅ Conforme au spec
- ❌ Issues: [liste avec file:line]
```

**Effort** : 4-6h
**Impact** : Élevé (qualité implémentation)

#### R2.2 — Systematic Debugging Skill

**Source** : `systematic-debugging`

**Justification** : EPCI manque de guidance structurée pour le debugging.

**Implémentation** : Créer `skills/core/systematic-debugging/SKILL.md`

```markdown
---
name: systematic-debugging
description: >-
  Use when encountering any bug, test failure, or unexpected behavior.
  Do NOT use for feature implementation or refactoring.
---

# Debugging Systématique

## Iron Law

```
NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST
```

## Les 4 Phases

### Phase 1: Investigation Root Cause
1. Lire les messages d'erreur COMPLÈTEMENT
2. Reproduire de manière consistante
3. Vérifier les changements récents (git diff)
4. Tracer le flux de données

### Phase 2: Analyse des Patterns
1. Trouver du code similaire qui fonctionne
2. Comparer avec références
3. Identifier les différences

### Phase 3: Hypothèse et Test
1. Former UNE hypothèse claire
2. Tester minimalement
3. Vérifier avant de continuer

### Phase 4: Implémentation
1. Créer test de régression AVANT fix
2. Implémenter fix unique
3. Vérifier fix + pas de régression

## Red Flags — STOP et retour Phase 1

- "Quick fix pour l'instant"
- "Juste essayer de changer X"
- "Je ne comprends pas vraiment mais ça pourrait marcher"
```

**Effort** : 3-4h
**Impact** : Élevé (efficacité debugging)

#### R2.3 — Injection Contexte via Hook SessionStart

**Source** : `hooks/session-start.sh`

**Justification** : EPCI a un système de hooks mais pas d'injection automatique du contexte core.

**Implémentation** :
1. Créer `hooks/session-start.sh` qui injecte `epci-core`
2. Configurer `hooks.json` pour SessionStart
3. Le skill injecté rappelle les workflows et règles

**Effort** : 2-3h
**Impact** : Moyen (adoption workflow)

### 8.3 Priorité 3 — Intégration Long Terme (Valeur Stratégique)

#### R3.1 — Infrastructure de Test de Skills

**Source** : `tests/skill-triggering/`

**Justification** : Valider que les skills se déclenchent sur des prompts naïfs.

**Implémentation** :
1. Adapter `run-test.sh` pour EPCI
2. Créer prompts de test pour chaque skill
3. Intégrer dans CI

**Effort** : 8-12h
**Impact** : Élevé (maintenabilité)

#### R3.2 — Pattern Controller/Workers pour Subagents

**Source** : `subagent-driven-development`

**Justification** : Plus efficace que l'invocation ponctuelle actuelle.

**Implémentation** :
1. Définir pattern orchestrateur dans `/epci` Phase 2
2. Templates de prompts externalisés
3. Boucles review/fix

**Effort** : 12-16h
**Impact** : Élevé (qualité workflow)

#### R3.3 — CSO pour Descriptions de Skills

**Source** : `writing-skills` (Claude Search Optimization)

**Justification** : Améliorer la découverte automatique des skills EPCI.

**Implémentation** :
1. Réviser toutes les descriptions pour format "Use when..."
2. Supprimer les résumés de workflow des descriptions
3. Ajouter keywords de symptômes

**Effort** : 4-6h
**Impact** : Moyen (activation automatique)

### 8.4 Matrice de Priorisation

| ID | Recommandation | Effort | Impact | Priorité |
|----|----------------|--------|--------|----------|
| R1.1 | Gate Function Vérification | 1-2h | Élevé | **P1** |
| R1.2 | Table Rationalisations | 1h | Moyen | **P1** |
| R1.3 | Red Flags Pattern | 1h | Moyen | **P1** |
| R2.1 | Double Review Stage | 4-6h | Élevé | **P2** |
| R2.2 | Systematic Debugging Skill | 3-4h | Élevé | **P2** |
| R2.3 | Hook SessionStart | 2-3h | Moyen | **P2** |
| R3.1 | Tests de Skills | 8-12h | Élevé | **P3** |
| R3.2 | Pattern Controller/Workers | 12-16h | Élevé | **P3** |
| R3.3 | CSO Descriptions | 4-6h | Moyen | **P3** |

### 8.5 Quick Wins Immédiats

| Action | Source | Lignes à copier |
|--------|--------|-----------------|
| Ajouter "Iron Law" TDD | test-driven-development | ~20 lignes |
| Copier Gate Function | verification-before-completion | ~10 lignes |
| Copier Red Flags table | using-superpowers | ~15 lignes |
| Template spec-reviewer | spec-reviewer-prompt.md | Fichier complet |

---

## Annexes

### A. Glossaire SuperPower

| Terme | Définition |
|-------|------------|
| **Iron Law** | Règle absolue sans exception |
| **Gate Function** | Workflow obligatoire avant action |
| **Pressure Testing** | Test de skill sous contraintes multiples |
| **CSO** | Claude Search Optimization |
| **Shadowing** | Override de skill plugin par skill personnel |

### B. Références Fichiers Clés

| Fichier | Contenu |
|---------|---------|
| `skills/using-superpowers/SKILL.md` | Gardien d'activation skills |
| `skills/test-driven-development/SKILL.md` | TDD strict |
| `skills/verification-before-completion/SKILL.md` | Gate Function |
| `skills/subagent-driven-development/SKILL.md` | Pattern Controller/Workers |
| `skills/writing-skills/testing-skills-with-subagents.md` | Pressure testing methodology |
| `lib/skills-core.js` | Résolution et shadowing |

### C. Flowcharts Clés (DOT)

Les flowcharts DOT de SuperPower sont particulièrement efficaces :
- `using-superpowers`: skill_flow
- `subagent-driven-development`: process, when_to_use
- `test-driven-development`: tdd_cycle

Ces diagrammes servent de **spécification exécutable** — la prose est support, le flowchart est autorité.

---

*Document généré le 2024-12-18 — Analyse basée sur SuperPower v4.0.0*
