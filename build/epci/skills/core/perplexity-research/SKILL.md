---
name: perplexity-research
description: >-
  Système de recherche externe via Perplexity Pro (human-in-the-loop).
  Détecte le besoin de recherche, génère des prompts optimisés,
  indique si Deep Research est recommandé.
  Use when: /brief, /debug, /brainstorm need external research beyond Context7.
  Not for: Internal codebase exploration, simple documentation lookup.
applicable-to: ["/brief", "/debug", "/brainstorm"]
integration: ["breakpoint-display"]
allowed-tools: [Read, Glob, Grep]
---

# Perplexity Research — Human-in-the-Loop External Research

## Overview

Skill pour intégrer la recherche externe via Perplexity Pro dans les workflows EPCI.
Fonctionne en mode human-in-the-loop : Claude détecte le besoin, génère un prompt optimisé,
l'utilisateur effectue la recherche dans Perplexity, puis colle les résultats.

**Bénéfices :**
- 🔍 **Recherche ciblée** : Prompts optimisés pour Perplexity
- 🧠 **Deep Research** : Indication quand utiliser le mode approfondi
- 🔄 **Backward compatible** : Commandes fonctionnent sans recherche
- 💰 **Token efficient** : Réutilise breakpoint-display (~80 tokens)

---

## MANDATORY EXECUTION — Instructions Impératives

**QUAND tu rencontres `@skill:perplexity-research` dans une commande, tu DOIS exécuter ces étapes :**

### Étape 1 : Évaluer le besoin de recherche

Analyser le contexte et déterminer si recherche externe est pertinente :

```
IF trigger matches (voir Triggers Matrix):
   → research_needed = true
   → Déterminer catégorie et mode
ELSE:
   → research_needed = false
   → SKIP (continuer workflow sans recherche)
```

### Étape 2 : Générer le prompt Perplexity

Si research_needed, construire le prompt optimisé :

```
prompt_structure:
  context: "{Domaine technique ou problématique}"
  question: "{Question précise basée sur trigger}"
  constraints: "{Stack, versions, limitations détectées}"
  format: "{Format attendu: liste, comparaison, tutoriel}"
```

> Voir @references/prompt-templates.md pour templates par catégorie.

### Étape 3 : Déterminer le mode (Standard vs Deep Research)

| Mode | Critères |
|------|----------|
| **Standard** | Question factuelle, lookup documentation, best practices simples |
| **Deep Research** | Analyse comparative 3+ options, architecture complexe, synthèse multi-sources |

> Voir @references/triggers.md pour critères détaillés par contexte.

### Étape 4 : Invoquer breakpoint-display

Afficher le breakpoint avec prompt copyable :

```yaml
@skill:breakpoint-display
  type: research-prompt
  title: "RECHERCHE PERPLEXITY SUGGÉRÉE"
  data:
    context: "{contexte_technique}"
    objective: "{objectif_recherche}"
    prompt: "{prompt_genere}"
    mode: "{Standard|Deep Research}"
    deep_reason: "{raison si Deep Research}"
    category: "{library|bug|architecture|best-practices|market|targeted}"
  ask:
    question: "Souhaitez-vous effectuer cette recherche Perplexity ?"
    header: "🔍 Research"
    multiSelect: false
    options:
      - label: "Rechercher (Recommended)"
        description: "Copier prompt, effectuer recherche, coller résultats"
      - label: "Skip"
        description: "Ignorer recherche, continuer workflow"
```

### Étape 5 : Traiter la réponse

| Choix utilisateur | Action |
|-------------------|--------|
| **Rechercher** | Attendre que l'utilisateur colle les résultats Perplexity |
| **Skip** | Continuer le workflow sans recherche |

**Si résultats collés** : Intégrer dans le contexte et continuer le workflow.

---

## Configuration

| Element | Value |
|---------|-------|
| **Modèle** | N/A (human-in-the-loop) |
| **Timeout** | Aucun (attendre réponse utilisateur) |
| **Fallback** | Continuer sans recherche |
| **Cache** | Session-scoped (éviter re-proposition même recherche) |

---

## Triggers Matrix

| Contexte | Commande | Trigger | Mode recommandé |
|----------|----------|---------|-----------------|
| Librairie inconnue | `/brief` | Package non dans Context7 | Standard |
| Bug complexe | `/debug` | Erreur rare, peu de résultats web | Deep Research |
| Architecture | `/brief`, `/brainstorm` | Patterns distribués, microservices | Deep Research |
| Best practices | `/brief` | Framework récent, nouvelles versions | Standard |
| Analyse concurrentielle | `/brainstorm` | `--competitive` flag | Deep Research |
| Incertitude technique | `/brainstorm` | EMS < 50, axes faibles | Standard |

> Voir @references/triggers.md pour matrice complète avec conditions de détection.

---

## Usage Pattern

### Invocation dans une commande

```yaml
@skill:perplexity-research
  trigger: "{library_unknown|bug_complex|architecture|best_practices|market|targeted}"
  context: "{description du besoin}"
  stack: "{technologies détectées}"
  specific_question: "{question ciblée}"
```

### Exemple dans /brief (Step 2.1)

```yaml
# Après @Explore, si librairie externe détectée
IF Context7 result empty OR package not in registry:
  @skill:perplexity-research
    trigger: "library_unknown"
    context: "Intégration de {package_name} dans {stack}"
    stack: "{detected_stack}"
    specific_question: "Best practices et patterns d'intégration"
```

### Exemple dans /debug (Step 1.2)

```yaml
# Après Context7 et WebSearch insuffisants
IF results < 3 OR confidence < 60%:
  @skill:perplexity-research
    trigger: "bug_complex"
    context: "Erreur: {error_message}"
    stack: "{detected_stack}"
    specific_question: "Root causes et solutions pour cette erreur"
```

### Exemple dans /brainstorm (Phase 1)

```yaml
# Après @Explore, si --competitive ou market research needed
IF --competitive flag OR feature_category == "new_market":
  @skill:perplexity-research
    trigger: "market"
    context: "Analyse marché pour {feature_domain}"
    stack: "N/A"
    specific_question: "Solutions existantes, gaps, opportunités"
```

### Exemple dans /brainstorm (Phase 2)

```yaml
# Si axes faibles détectés et iteration >= 2
IF weak_axes.length > 0 AND iteration >= 2:
  @skill:perplexity-research
    trigger: "targeted"
    context: "Approfondissement axe {weak_axis}"
    stack: "{detected_stack}"
    specific_question: "Patterns et solutions pour améliorer {weak_axis}"
```

---

## Prompt Templates (Summary)

| Catégorie | Structure |
|-----------|-----------|
| **library** | `[Contexte]: Intégration {lib} dans {stack}. [Question]: Best practices ? [Format]: Liste avec exemples` |
| **bug** | `[Erreur]: {error}. [Stack]: {versions}. [Question]: Root causes et solutions ? [Format]: Ranked list` |
| **architecture** | `[Contexte]: {domain}. [Question]: Patterns recommandés ? [Format]: Comparaison avec trade-offs` |
| **best-practices** | `[Framework]: {framework} {version}. [Question]: Best practices {topic} ? [Format]: Checklist` |
| **market** | `[Domaine]: {domain}. [Question]: Solutions existantes ? [Format]: Tableau comparatif` |
| **targeted** | `[Contexte]: {context}. [Axe faible]: {axis}. [Question]: Comment améliorer ? [Format]: Suggestions actionables` |

> Voir @references/prompt-templates.md pour templates complets.

---

## Integration Points

### Commandes supportées

| Commande | Point d'insertion | Trigger principal |
|----------|-------------------|-------------------|
| `/brief` | Step 2.1 (après @Explore) | Librairie externe, best practices |
| `/debug` | Step 1.2 (Research) | Bug complexe, erreur rare |
| `/brainstorm` | Phase 1 (init) + Phase 2 (iterations) | Market analysis, axes faibles |

### Dépendances

- `breakpoint-display` : Pour affichage du breakpoint research-prompt
- `project-memory` : Pour contexte session (éviter re-proposition)

---

## Session State

Pour éviter de re-proposer la même recherche dans une session :

```yaml
# .project-memory/sessions/<session-id>.yaml
perplexity_research:
  proposed:
    - timestamp: "2026-01-20T16:30:00Z"
      trigger: "library_unknown"
      category: "library"
      status: "completed|skipped"
      results_summary: "..." # Si completed
```

---

## Error Handling

| Situation | Action |
|-----------|--------|
| Utilisateur ne répond pas | Attendre (pas de timeout) |
| Résultats collés invalides | Demander clarification ou ignorer |
| Recherche déjà proposée | Skip (éviter spam) |
| Trigger non reconnu | Log warning, skip recherche |

---

## Anti-patterns

| Anti-pattern | Problème | Alternative |
|--------------|----------|-------------|
| Proposer pour tout | Fatigue utilisateur | Utiliser triggers stricts |
| Ignorer résultats | Perte de valeur | Toujours intégrer si collés |
| Re-proposer même recherche | Spam | Tracker dans session state |
| Prompt trop vague | Mauvais résultats | Templates structurés |

---

## References

- Triggers détaillés: @references/triggers.md
- Prompt templates: @references/prompt-templates.md
- Breakpoint integration: @src/skills/core/breakpoint-display/templates/research-prompt.md
- Commands using this skill:
  - @src/commands/brief.md (Step 2.1)
  - @src/commands/debug.md (Step 1.2)
  - @src/commands/brainstorm.md (Phase 1 + 2)
