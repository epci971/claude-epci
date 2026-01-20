# Template: Research Prompt Breakpoint

## Overview

Breakpoint pour proposer une recherche externe via Perplexity Pro (human-in-the-loop).
Affiche contexte, prompt copyable, et mode recommandé (Standard/Deep Research).

**Usage:** `/brief` Step 2.1, `/debug` Step 1.2, `/brainstorm` Phase 1 + 2

## Data Structure

```typescript
{
  type: "research-prompt",
  title: "{TITLE}",
  data: {
    context: "{Contexte technique ou problématique}",
    objective: "{Objectif de la recherche}",
    prompt: "{Prompt Perplexity prêt à copier}",
    mode: "Standard|Deep Research",
    deep_reason: "{Raison si Deep Research - optionnel si Standard}",
    category: "library|bug|architecture|best-practices|market|targeted"
  },
  ask: {
    question: "{QUESTION}",
    header: "{HEADER}",  // Max 12 chars
    options: [
      {label: "{LABEL}", description: "{DESCRIPTION}"},
      ...
    ]
  }
}
```

## Display Format

```
┌─────────────────────────────────────────────────────────────────────┐
│ 🔍 {title}                                                          │
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
│ │                                                                 │ │
│ │ [Multi-line prompt content...]                                  │ │
│ └─────────────────────────────────────────────────────────────────┘ │
│                                                                     │
│ ⚙️ MODE RECOMMANDÉ: {data.mode}                                     │
│ [SI data.mode == "Deep Research":]                                  │
│ 💡 Deep Research recommandé car: {data.deep_reason}                 │
│                                                                     │
│ 🏷️ Catégorie: {data.category}                                       │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

Then invoke `AskUserQuestion` with options.

## Example: Library Unknown

```typescript
{
  type: "research-prompt",
  title: "RECHERCHE PERPLEXITY SUGGÉRÉE",
  data: {
    context: "Intégration @tanstack/query v5 dans projet React 18",
    objective: "Obtenir best practices et patterns d'intégration",
    prompt: `[Contexte]: Je travaille sur un projet React 18 + TypeScript et j'ai besoin d'intégrer @tanstack/query (version 5.0.0).

[Question]: Quelles sont les best practices pour intégrer @tanstack/query dans une application React ? Notamment :
- Configuration initiale recommandée
- Patterns d'utilisation courants
- Pièges à éviter
- Exemples de code concrets

[Contraintes]:
- Stack: React 18.2, TypeScript 5.3, Vite
- Version: @tanstack/query 5.0.0

[Format attendu]: Liste structurée avec exemples de code`,
    mode: "Standard",
    deep_reason: null,
    category: "library"
  },
  ask: {
    question: "Souhaitez-vous effectuer cette recherche Perplexity ?",
    header: "🔍 Research",
    options: [
      {label: "Rechercher (Recommended)", description: "Copier prompt, effectuer recherche, coller résultats"},
      {label: "Skip", description: "Ignorer recherche, continuer workflow"}
    ]
  }
}
```

## Example: Bug Complex (Deep Research)

```typescript
{
  type: "research-prompt",
  title: "RECHERCHE PERPLEXITY SUGGÉRÉE",
  data: {
    context: "Erreur EPERM symlink sur Windows WSL2 lors de npm install",
    objective: "Identifier root causes et solutions pour cette erreur rare",
    prompt: `[Erreur]: EPERM: operation not permitted, symlink 'C:\\...' -> 'C:\\...'

[Contexte]:
- Framework: Next.js 14.2.0
- Environnement: Windows 11 WSL2, Node 20.10
- Fréquence: Always (sur npm install)
- Derniers changements: Migration vers pnpm

[Question]: Quelles sont les causes possibles de cette erreur et les solutions recommandées ?
1. Root causes classées par probabilité
2. Solutions pour chaque cause
3. Comment diagnostiquer laquelle s'applique

[Format attendu]: Liste classée par probabilité avec solutions détaillées`,
    mode: "Deep Research",
    deep_reason: "Erreur rare nécessitant synthèse de multiples sources",
    category: "bug"
  },
  ask: {
    question: "Souhaitez-vous effectuer cette recherche Perplexity ?",
    header: "🔍 Research",
    options: [
      {label: "Rechercher (Recommended)", description: "Copier prompt, effectuer recherche Deep Research"},
      {label: "Skip", description: "Ignorer recherche, continuer avec données existantes"}
    ]
  }
}
```

## Example: Market Analysis

```typescript
{
  type: "research-prompt",
  title: "RECHERCHE MARCHÉ SUGGÉRÉE",
  data: {
    context: "Développement système de notifications temps réel pour SaaS B2B",
    objective: "Analyser solutions existantes et identifier gaps/opportunités",
    prompt: `[Domaine]: Notifications temps réel pour applications SaaS

[Question]: Quelles sont les solutions existantes ? Pour chaque solution :
1. Fonctionnalités principales
2. Pricing model
3. Points forts / Points faibles
4. Type de clients cibles

[Critères de comparaison]:
- Support multi-canal (push, email, in-app)
- Pricing par message vs flat
- Self-hosted vs SaaS

[Format attendu]: Tableau comparatif des 5-7 solutions principales`,
    mode: "Deep Research",
    deep_reason: "Analyse comparative nécessitant synthèse de multiples sources",
    category: "market"
  },
  ask: {
    question: "Souhaitez-vous effectuer cette analyse marché ?",
    header: "🔍 Market",
    options: [
      {label: "Rechercher (Recommended)", description: "Analyse concurrentielle via Deep Research"},
      {label: "Skip", description: "Ignorer analyse marché"}
    ]
  }
}
```

## Workflow After Selection

### If "Rechercher" selected:

1. Display instruction:
   ```
   📋 Instructions:
   1. Copiez le prompt ci-dessus
   2. Ouvrez Perplexity Pro (perplexity.ai)
   3. [Si Deep Research] Activez "Deep Research" avant d'envoyer
   4. Collez le prompt et lancez la recherche
   5. Copiez la réponse Perplexity
   6. Collez-la ici pour continuer
   ```

2. Wait for user to paste results

3. Integrate results into workflow context

### If "Skip" selected:

Continue workflow without external research. Log skip in session state.

## Token Savings

**Avant:** N/A (nouvelle fonctionnalité)
**Après:** ~85 tokens (skill invocation)

## Special Considerations

1. **Prompt box** must preserve formatting (newlines, indentation)
2. **Deep Research indicator** should be prominent when applicable
3. **Category badge** helps user understand research type
4. **No timeout** - wait indefinitely for user response
