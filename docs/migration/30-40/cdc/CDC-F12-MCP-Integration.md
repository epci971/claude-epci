# Cahier des Charges — F12: MCP Integration

> **Document**: CDC-F12-001
> **Version**: 1.0.0
> **Date**: 2025-12-15
> **Statut**: Validé
> **Feature ID**: F12
> **Version cible**: EPCI v4.0
> **Priorité**: P2
> **Source**: Analyse WD Framework v2.0 [NEW]

---

## 1. Contexte Global EPCI

### 1.1 Philosophie EPCI v4.0

```
┌─────────────────────────────────────────────────────────────────────┐
│                        PHILOSOPHIE EPCI                             │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  🎯 SIMPLICITÉ        — 5 commandes ciblées, pas 22                │
│  📋 TRAÇABILITÉ       — Feature Document pour chaque feature        │
│  ⏸️  BREAKPOINTS       — L'humain valide entre les phases           │
│  🔄 TDD               — Red → Green → Refactor systématique         │
│  🧩 MODULARITÉ        — Skills, Agents, Commands séparés            │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### 1.2 État Actuel (Baseline v3.0.0)

EPCI v3.0.0 n'intègre pas de **serveurs MCP** (Model Context Protocol) pour enrichir le contexte avec des données externes.

### 1.3 Glossaire Pertinent

| Terme | Définition |
|-------|------------|
| **MCP** | Model Context Protocol — serveurs enrichissant le contexte de Claude |
| **Context7** | MCP pour documentation de librairies externes |
| **Sequential** | MCP pour analyse multi-étapes structurée |
| **Magic** | MCP pour génération UI moderne (21st.dev) |
| **Playwright** | MCP pour tests E2E et automatisation browser |

---

## 2. Description de la Feature

### 2.1 Contexte et Justification

**Source** : Analyse comparative WD Framework v2.0

**Problème** : EPCI ne bénéficie pas des capacités MCP :
- Pas d'accès aux docs à jour des librairies
- Pas de raisonnement structuré multi-étapes
- Pas de génération UI moderne
- Pas de tests E2E automatisés

**Solution** : Intégration de 4 serveurs MCP avec :
- Activation automatique selon le contexte
- Mapping avec les personas
- Mode dégradé si indisponible
- Configuration par projet

### 2.2 Objectif

Enrichir EPCI avec des capacités externes via 4 serveurs MCP, activés intelligemment selon le contexte et la persona active.

---

## 3. Les 4 MCP Servers

### 3.1 Vue d'Ensemble

```
┌─────────────────────────────────────────────────────────────────────┐
│                    MCP SERVERS EPCI                                 │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  📚 CONTEXT7 — Documentation librairies                            │
│  ├── Fonction: Recherche docs librairies/frameworks externes       │
│  ├── URL: https://context7.dev                                     │
│  ├── Déclencheurs:                                                 │
│  │   ├── Imports externes détectés                                 │
│  │   ├── Questions sur un framework                                │
│  │   └── --persona-frontend ou --persona-backend                   │
│  └── Exemple: "Doctrine pagination" → KnpPaginator, Pagerfanta     │
│                                                                     │
│  🔗 SEQUENTIAL — Analyse multi-étapes                               │
│  ├── Fonction: Raisonnement structuré pour problèmes complexes     │
│  ├── Déclencheurs:                                                 │
│  │   ├── --think-hard ou --ultrathink                              │
│  │   ├── Debugging complexe                                        │
│  │   └── --persona-architect ou --persona-security                 │
│  └── Exemple: "Perf dégradée" → Analyse systématique 5 étapes      │
│                                                                     │
│  ✨ MAGIC — Génération UI                                           │
│  ├── Fonction: Génération composants UI modernes (21st.dev)        │
│  ├── Déclencheurs:                                                 │
│  │   ├── --persona-frontend                                        │
│  │   ├── Fichiers *.jsx, *.tsx, *.vue                              │
│  │   └── Keywords: component, button, form, modal                  │
│  └── Exemple: "DataTable" → Composant accessible + variants        │
│                                                                     │
│  🎭 PLAYWRIGHT — Tests E2E & Browser                                │
│  ├── Fonction: Automatisation browser, tests E2E, a11y             │
│  ├── Déclencheurs:                                                 │
│  │   ├── --persona-qa                                              │
│  │   ├── Fichiers *.spec.ts, *.e2e.ts                              │
│  │   └── Keywords: e2e, browser, accessibility                     │
│  └── Exemple: "Test inscription" → Parcours complet + a11y         │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### 3.2 Détail Context7

| Attribut | Valeur |
|----------|--------|
| **Fonction** | Documentation librairies externes |
| **Outils** | `resolve-library-id`, `get-library-docs` |
| **Auto-trigger keywords** | import, require, use, framework names |
| **Auto-trigger files** | `package.json`, `composer.json`, `requirements.txt` |
| **Personas** | architect, frontend, backend, doc |

**Workflow** :
1. Détecter import/dépendance
2. `resolve-library-id` → Trouver ID Context7
3. `get-library-docs` → Récupérer documentation
4. Intégrer patterns dans la génération

### 3.3 Détail Sequential

| Attribut | Valeur |
|----------|--------|
| **Fonction** | Raisonnement structuré multi-étapes |
| **Outils** | `sequentialthinking` |
| **Auto-trigger flags** | `--think-hard`, `--ultrathink` |
| **Auto-trigger keywords** | debug, analyze, investigate, complex |
| **Personas** | architect, security, analyzer |

**Workflow** :
1. Décomposer problème en étapes
2. Analyser chaque étape séquentiellement
3. Construire raisonnement progressif
4. Synthétiser conclusions

### 3.4 Détail Magic

| Attribut | Valeur |
|----------|--------|
| **Fonction** | Génération composants UI modernes |
| **Outils** | `21st_magic_component_builder`, `logo_search` |
| **Auto-trigger keywords** | component, button, form, modal, table |
| **Auto-trigger files** | `*.jsx`, `*.tsx`, `*.vue` |
| **Personas** | frontend |

**Workflow** :
1. Analyser besoin UI
2. Chercher composants similaires sur 21st.dev
3. Générer code avec best practices
4. Intégrer accessibilité et responsivité

### 3.5 Détail Playwright

| Attribut | Valeur |
|----------|--------|
| **Fonction** | Tests E2E, automatisation browser |
| **Outils** | `browser_navigate`, `browser_click`, `browser_snapshot`, etc. |
| **Auto-trigger keywords** | e2e, browser, accessibility, test |
| **Auto-trigger files** | `*.spec.ts`, `*.e2e.ts`, `*test*` |
| **Personas** | qa, frontend |

**Workflow** :
1. Définir parcours utilisateur
2. Automatiser interactions browser
3. Capturer snapshots et métriques
4. Générer rapport de test

---

## 4. Structure des Fichiers

```
skills/
└── mcp/                               # NOUVEAU dossier
    ├── MCP.md                         # Index et configuration
    ├── context7.md                    # Documentation Context7
    ├── sequential.md                  # Documentation Sequential
    ├── magic.md                       # Documentation Magic
    └── playwright.md                  # Documentation Playwright
```

### 4.1 Format `MCP.md`

```yaml
# MCP Integration Index

## Available Servers

| Server | Status | Auto-activate |
|--------|--------|---------------|
| Context7 | ✅ | Yes |
| Sequential | ✅ | Yes |
| Magic | ✅ | Yes |
| Playwright | ✅ | Yes |

## Activation Matrix

[Matrice Persona × MCP]

## Configuration

See project-memory/settings.json for per-project configuration.
```

---

## 5. Configuration

### 5.1 Configuration Globale

```json
// project-memory/settings.json
{
  "mcp": {
    "enabled": true,
    "servers": {
      "context7": {
        "enabled": true,
        "auto_activate": true
      },
      "sequential": {
        "enabled": true,
        "auto_activate": true
      },
      "magic": {
        "enabled": true,
        "auto_activate": true
      },
      "playwright": {
        "enabled": true,
        "auto_activate": true
      }
    }
  }
}
```

### 5.2 Flags Manuels

```bash
# Activer spécifiquement
/epci --c7 --seq           # Context7 + Sequential
/epci --magic              # Magic uniquement
/epci --play               # Playwright uniquement

# Désactiver spécifiquement
/epci --no-magic           # Tout sauf Magic
/epci --no-mcp             # Aucun MCP
```

---

## 6. Matrice Persona × MCP

| Persona | Context7 | Sequential | Magic | Playwright |
|---------|:--------:|:----------:|:-----:|:----------:|
| architect | ● | ● | ○ | ○ |
| frontend | ● | ○ | ● | ● |
| backend | ● | ● | ○ | ○ |
| security | ○ | ● | ○ | ○ |
| qa | ○ | ○ | ○ | ● |
| doc | ● | ○ | ○ | ○ |

`●` Auto-activé avec persona | `○` Disponible sur demande

---

## 7. Mode Dégradé

### 7.1 Comportement si MCP Indisponible

| Situation | Comportement | Message |
|-----------|--------------|---------|
| MCP timeout | Retry 2x, puis skip | "⚠️ Context7 unreachable, continuing without" |
| MCP non configuré | Skip silencieux | — |
| MCP erreur | Log, continue | "⚠️ Sequential error, fallback to standard" |

### 7.2 Fallbacks

| MCP | Fallback |
|-----|----------|
| Context7 | WebSearch pour documentation |
| Sequential | Raisonnement natif Claude |
| Magic | Génération basique sans 21st.dev |
| Playwright | Suggestions tests manuels |

---

## 8. Critères d'Acceptation

| ID | Critère | Méthode de vérification |
|----|---------|-------------------------|
| F12-AC1 | 4 MCPs documentés | Fichiers `skills/mcp/` présents |
| F12-AC2 | Auto-activation persona | Test avec différentes personas |
| F12-AC3 | Configuration projet | `settings.json` fonctionnel |
| F12-AC4 | Mode dégradé | Test avec MCP down |
| F12-AC5 | Flags manuels | `--c7`, `--seq`, `--magic`, `--play` |

---

## 9. Dépendances

### 9.1 Dépendances Entrantes (cette feature dépend de)

| Feature | Type | Description |
|---------|------|-------------|
| F09 Personas | Forte | Activation MCP selon persona |

### 9.2 Dépendances Sortantes (dépendent de cette feature)

| Feature | Type | Description |
|---------|------|-------------|
| F05 Clarification | Faible | Context7 pour docs externes |

---

## 10. Effort Estimé

| Tâche | Effort |
|-------|--------|
| 4 fichiers documentation | 8h |
| MCP.md index | 2h |
| Auto-activation | 6h |
| Intégration personas | 4h |
| Mode dégradé | 4h |
| Tests | 4h |
| **Total** | **28h (3.5j)** |

---

## 11. Livrables

1. `skills/mcp/MCP.md` — Index et documentation
2. `skills/mcp/context7.md` — Doc Context7
3. `skills/mcp/sequential.md` — Doc Sequential
4. `skills/mcp/magic.md` — Doc Magic
5. `skills/mcp/playwright.md` — Doc Playwright
6. Module d'auto-activation MCP
7. Mode dégradé et fallbacks
8. Tests unitaires et d'intégration

---

## 12. Exemples d'Usage

### 12.1 Context7 Auto-activé

```
Brief: "Ajouter pagination sur la liste produits"
Stack: Symfony (composer.json détecté)

→ Context7 activé automatiquement
→ resolve-library-id("doctrine pagination")
→ get-library-docs(topic="pagination")
→ Intègre patterns KnpPaginator dans le code généré
```

### 12.2 Sequential avec --think-hard

```
Brief: "Diagnostiquer pourquoi les perfs sont dégradées"
Flag: --think-hard

→ Sequential activé (--think-hard)
→ Analyse structurée en 5 étapes:
  1. Identifier les symptômes
  2. Collecter les métriques
  3. Analyser les causes possibles
  4. Tester les hypothèses
  5. Proposer solutions
```

### 12.3 Magic avec --persona-frontend

```
Brief: "Créer un composant DataTable réutilisable"
Persona: --persona-frontend

→ Magic activé (persona frontend)
→ Recherche composants similaires sur 21st.dev
→ Génère DataTable avec:
  - Sorting, filtering, pagination
  - Accessibilité WCAG 2.1
  - Responsive design
  - Variants (loading, empty, error)
```

---

## 13. Hors Périmètre

- Création de nouveaux MCP servers
- MCP servers custom par projet
- Cache des résultats MCP
- Métriques d'usage MCP

---

*Document généré depuis CDC-EPCI-UNIFIE-v4.md*
