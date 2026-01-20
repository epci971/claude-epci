---
saved_at: "2026-01-20T16:09:14Z"
source: "~/.claude/plans/expressive-gathering-rabin.md"
slug: "integration-perplexity-research"
original_filename: "expressive-gathering-rabin.md"
auto_detected: true
---

# Plan : Intégration Perplexity Research (Human-in-the-Loop)

## Résumé

Créer un système de recherche externe via Perplexity Pro (sans API) avec breakpoints interactifs dans les commandes `/brief`, `/debug` et `/brainstorm`.

**Principe** : Claude détecte le besoin de recherche → affiche un breakpoint avec prompt prêt à copier → l'utilisateur fait la recherche dans Perplexity → colle les résultats → Claude intègre.

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    NOUVEAU SKILL                                 │
│              perplexity-research/SKILL.md                        │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │ • Logique de détection du besoin de recherche               ││
│  │ • Génération de prompts Perplexity optimisés                ││
│  │ • Indication Deep Research (oui/non)                        ││
│  │ • Patterns de recherche par contexte                        ││
│  └─────────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼ invoque
┌─────────────────────────────────────────────────────────────────┐
│                 BREAKPOINT-DISPLAY (existant)                    │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │ NOUVEAU TYPE: research-prompt                               ││
│  │ • Affiche contexte + prompt copyable                        ││
│  │ • Indique mode (Standard / Deep Research)                   ││
│  │ • AskUserQuestion: [Rechercher] / [Pas nécessaire]          ││
│  └─────────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼ utilisé par
┌─────────────────────────────────────────────────────────────────┐
│            COMMANDES EPCI (modification)                         │
│  • /brief   → Step 2 (après @Explore)                           │
│  • /debug   → Step 1.2 (Research)                               │
│  • /brainstorm → Phase 1 + Phase 2 (itérations)                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Fichiers à créer/modifier

### 1. Nouveau skill : `perplexity-research`

**Créer** : `src/skills/core/perplexity-research/SKILL.md`

```yaml
name: perplexity-research
description: >-
  Système de recherche externe via Perplexity Pro (human-in-the-loop).
  Détecte le besoin de recherche, génère des prompts optimisés,
  indique si Deep Research est recommandé.
applicable-to: ["/brief", "/debug", "/brainstorm"]
integration: ["breakpoint-display"]
```

**Contenu** :
- Triggers de détection (quand proposer une recherche)
- Patterns de prompts par catégorie (librairie, bug, architecture, best practices)
- Critères pour recommander Deep Research vs Standard
- Format de retour des résultats

### 2. Nouveau type breakpoint : `research-prompt`

**Modifier** : `src/skills/core/breakpoint-display/SKILL.md`
- Ajouter type `research-prompt` dans la table des types supportés

**Créer** : `src/skills/core/breakpoint-display/templates/research-prompt.md`

```
┌─────────────────────────────────────────────────────────────────────┐
│ 🔍 RECHERCHE PERPLEXITY SUGGÉRÉE                                    │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│ 📋 CONTEXTE                                                         │
│ {data.context}                                                      │
│                                                                     │
│ 🎯 OBJECTIF DE RECHERCHE                                            │
│ {data.objective}                                                    │
│                                                                     │
│ 📝 PROMPT PERPLEXITY (copier ci-dessous)                            │
│ ┌─────────────────────────────────────────────────────────────────┐ │
│ │ {data.prompt}                                                   │ │
│ └─────────────────────────────────────────────────────────────────┘ │
│                                                                     │
│ ⚙️ MODE RECOMMANDÉ: {data.mode} (Standard | Deep Research)          │
│ [SI data.mode == "Deep Research":]                                  │
│ 💡 Deep Research recommandé car: {data.deep_reason}                 │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

**Modifier** : `src/skills/core/breakpoint-display/references/execution-templates.md`
- Ajouter template ASCII pour `research-prompt`

### 3. Modifications des commandes

**Modifier** : `src/commands/brief.md`
- Step 2 (après @Explore) : Ajouter invocation conditionnelle `@skill:perplexity-research`
- Trigger : Si librairie externe détectée OU best practices requises

**Modifier** : `src/commands/debug.md`
- Step 1.2 (Research) : Ajouter invocation `@skill:perplexity-research`
- Trigger : Si erreur non trouvée via Context7/WebSearch OU framework peu documenté

**Modifier** : `src/commands/brainstorm.md`
- Phase 1 : Après @Explore, proposer recherche marché/concurrence
- Phase 2 : Sur axes faibles, proposer recherche ciblée

---

## Détails d'implémentation

### Triggers de détection (dans le skill)

| Contexte | Trigger | Mode recommandé |
|----------|---------|-----------------|
| Librairie inconnue | Package non dans Context7 | Standard |
| Bug complexe | Erreur rare, peu de résultats web | Deep Research |
| Architecture | Patterns distribués, microservices | Deep Research |
| Best practices | Framework récent, nouvelles versions | Standard |
| Analyse concurrentielle | `--competitive` flag | Deep Research |
| Incertitude technique | `/brainstorm` avec EMS < 50 | Standard |

### Structure du prompt Perplexity

```
[Contexte]: {domaine technique}
[Question]: {question précise}
[Contraintes]: {stack, versions, limitations}
[Format attendu]: {liste, comparaison, tutoriel step-by-step}
```

### Critères Deep Research

Recommandé si :
- Question architecturale complexe (plusieurs composants)
- Analyse comparative (3+ options à évaluer)
- Recherche de patterns peu documentés
- Problème nécessitant synthèse de multiples sources

### Workflow utilisateur

```
1. Breakpoint s'affiche avec prompt
2. Utilisateur choisit [Effectuer recherche] ou [Pas nécessaire]
3. Si recherche :
   a. Copier le prompt
   b. Ouvrir Perplexity Pro
   c. Coller et exécuter (activer Deep Research si indiqué)
   d. Copier la réponse Perplexity
   e. Coller dans Claude après le breakpoint
4. Claude intègre les informations et continue
```

---

## Invocation dans les commandes

### Pattern d'invocation

```yaml
@skill:perplexity-research
  trigger: "library_unknown"  # ou "bug_complex", "architecture", "best_practices"
  context: "{description du besoin}"
  stack: "{technologies détectées}"
  specific_question: "{question ciblée}"
```

Le skill :
1. Évalue si la recherche est pertinente
2. Si oui, génère le prompt optimisé
3. Invoque `@skill:breakpoint-display type:research-prompt`
4. Attend le retour utilisateur
5. Intègre les résultats ou continue sans

### Exemple dans /debug

```yaml
# Step 1.2: Research
IF Context7 result empty OR WebSearch insufficient:
  @skill:perplexity-research
    trigger: "bug_complex"
    context: "Erreur {error_message} dans {framework}"
    stack: "{detected_stack}"
    specific_question: "Solutions et root causes pour cette erreur"
```

---

## Fichiers impactés (résumé)

| Action | Fichier | Changement |
|--------|---------|------------|
| **Créer** | `src/skills/core/perplexity-research/SKILL.md` | Nouveau skill complet |
| **Créer** | `src/skills/core/breakpoint-display/templates/research-prompt.md` | Template nouveau type |
| **Modifier** | `src/skills/core/breakpoint-display/SKILL.md` | Ajouter type `research-prompt` |
| **Modifier** | `src/skills/core/breakpoint-display/references/execution-templates.md` | Template ASCII |
| **Modifier** | `src/commands/brief.md` | Invocation skill Step 2 |
| **Modifier** | `src/commands/debug.md` | Invocation skill Step 1.2 |
| **Modifier** | `src/commands/brainstorm.md` | Invocation skill Phase 1 + 2 |
| **Modifier** | `CLAUDE.md` | Ajouter skill dans liste (35 skills) |

---

## Vérification

1. **Test unitaire skill** : Valider génération de prompts pour chaque trigger
2. **Test breakpoint** : Vérifier affichage correct du template research-prompt
3. **Test intégration /debug** : Scénario bug avec recherche Perplexity
4. **Test intégration /brief** : Scénario avec librairie externe
5. **Test intégration /brainstorm** : Scénario avec analyse concurrentielle

```bash
# Validation structure skill
python src/scripts/validate_skill.py src/skills/core/perplexity-research/

# Validation commandes modifiées
python src/scripts/validate_command.py src/commands/brief.md
python src/scripts/validate_command.py src/commands/debug.md
python src/scripts/validate_command.py src/commands/brainstorm.md
```

---

## Notes

- **Pas d'API** : Tout le workflow est manuel (human-in-the-loop)
- **Perplexity Pro** : Exploite Deep Research disponible avec l'abonnement
- **Backward compatible** : Les commandes fonctionnent sans le skill (recherche optionnelle)
- **Token efficient** : Réutilise breakpoint-display existant (~80 tokens/breakpoint)
