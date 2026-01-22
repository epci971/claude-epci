# Triggers Matrix — Perplexity Research

> Matrice détaillée des triggers de recherche par commande et contexte.

---

## Trigger Categories

| Category | ID | Description | Default Mode |
|----------|------|-------------|--------------|
| **Library Unknown** | `library_unknown` | Package non documenté dans Context7 | Standard |
| **Bug Complex** | `bug_complex` | Erreur rare avec peu de résultats | Deep Research |
| **Architecture** | `architecture` | Patterns distribués, design decisions | Deep Research |
| **Best Practices** | `best_practices` | Framework récent, nouvelles conventions | Standard |
| **Market Analysis** | `market` | Analyse concurrentielle, solutions existantes | Deep Research |
| **Targeted Research** | `targeted` | Recherche ciblée sur axe faible spécifique | Standard |

---

## Triggers par Commande

### /brief — Step 2.1

| Trigger | Condition de détection | Mode |
|---------|------------------------|------|
| `library_unknown` | Package détecté par @Explore mais absent de Context7 registry | Standard |
| `best_practices` | Framework version >= latest-1, ou package avec `@latest` | Standard |
| `architecture` | Keywords: `microservices`, `distributed`, `event-driven`, `CQRS` | Deep Research |

**Détection automatique :**

```
IF @Explore detected packages:
  FOR EACH package IN detected_packages:
    IF NOT Context7.has(package) AND package.usage == "core":
      trigger = "library_unknown"
      BREAK

IF @Explore detected patterns:
  IF patterns INTERSECT ["microservices", "event-driven", "CQRS", "saga"]:
    trigger = "architecture"
```

**Skip conditions :**
- Package déjà documenté dans Context7
- Brief catégorie TINY (trop simple pour recherche)
- Flag `--no-research` (si implémenté)

---

### /debug — Step 1.2

| Trigger | Condition de détection | Mode |
|---------|------------------------|------|
| `bug_complex` | Context7 results < 3 AND WebSearch results < 5 | Deep Research |
| `bug_complex` | Error message contains `unknown`, `undefined`, `rare` | Deep Research |
| `library_unknown` | Stack trace points to undocumented library | Standard |

**Détection automatique :**

```
AFTER Context7 query:
  IF results.count < 3:
    confidence = 0.4

AFTER WebSearch query:
  IF results.count < 5:
    confidence = confidence - 0.2

IF confidence < 0.6:
  trigger = "bug_complex"
  mode = "Deep Research"
```

**Skip conditions :**
- Route Trivial (typo, missing import)
- Confidence >= 80% après Context7
- Error est un pattern commun (null pointer, syntax error)

---

### /brainstorm — Phase 1 (Initialisation)

| Trigger | Condition de détection | Mode |
|---------|------------------------|------|
| `market` | Flag `--competitive` actif | Deep Research |
| `market` | Keywords: `concurrent`, `marché`, `alternative`, `benchmark` | Deep Research |
| `architecture` | Feature implique nouvelle architecture | Deep Research |

**Détection automatique :**

```
IF flags.includes("--competitive"):
  trigger = "market"
  mode = "Deep Research"

IF description MATCHES /concurrent|marché|alternative|versus|vs\./i:
  trigger = "market"
  mode = "Deep Research"

IF @Explore.patterns.includes("greenfield") OR description.includes("nouvelle architecture"):
  trigger = "architecture"
  mode = "Deep Research"
```

**Skip conditions :**
- Feature simple (refactoring, bugfix)
- Codebase patterns déjà établis
- Flag `--no-research`

---

### /brainstorm — Phase 2 (Itérations)

| Trigger | Condition de détection | Mode |
|---------|------------------------|------|
| `targeted` | EMS < 50 AND weak_axes.length > 0 AND iteration >= 2 | Standard |
| `targeted` | Même axe faible pendant 2+ itérations | Standard |
| `best_practices` | Axe "Actionnabilité" faible, besoin de patterns concrets | Standard |

**Détection automatique :**

```
IF ems.score < 50 AND iteration >= 2:
  IF weak_axes.includes("Couverture"):
    trigger = "targeted"
    question_focus = "perspectives manquantes"

  IF weak_axes.includes("Profondeur"):
    trigger = "targeted"
    question_focus = "détails techniques"

  IF weak_axes.includes("Actionnabilité"):
    trigger = "best_practices"
    question_focus = "patterns implémentation"
```

**Skip conditions :**
- EMS >= 70 (proche finalisation)
- Technique déjà appliquée dans cette itération
- Recherche déjà proposée pour cet axe

---

## Mode Selection Logic

### Standard Mode

Utiliser pour :
- Questions factuelles avec réponse attendue courte
- Documentation lookup
- Best practices établies
- Single source sufficient

**Exemples :**
- "Comment configurer X dans Y ?"
- "Quelle est la syntaxe pour Z ?"
- "Best practices pour authentication JWT"

### Deep Research Mode

Utiliser pour :
- Analyse comparative (3+ options)
- Questions architecturales complexes
- Synthèse de multiples sources nécessaire
- Problèmes peu documentés

**Exemples :**
- "Comparaison Redis vs Kafka vs RabbitMQ pour event streaming"
- "Architecture microservices pour e-commerce haute disponibilité"
- "Root causes possibles pour memory leak en production Node.js"

---

## Deep Research Criteria

| Critère | Poids | Description |
|---------|-------|-------------|
| **Multiple options** | +0.3 | 3+ alternatives à évaluer |
| **Architecture** | +0.3 | Impact sur structure système |
| **Novel domain** | +0.2 | Domaine peu documenté |
| **Synthesis required** | +0.2 | Besoin de croiser sources |

**Seuil Deep Research :** score >= 0.5

---

## Cooldown Logic

Pour éviter de spammer l'utilisateur avec des propositions de recherche :

```yaml
cooldown_rules:
  same_trigger_category:
    min_interval: "2 iterations"  # brainstorm
    or: "1 step"  # brief/debug

  same_session:
    max_proposals: 3
    reset_on: "new_session"

  user_skipped:
    backoff: "double"  # 1 → 2 → 4 iterations
```

---

## Examples

### Example 1: /brief with unknown library

```yaml
# Context
@Explore detected: "@tanstack/query v5.0.0"
Context7 query: "@tanstack/query" → 0 results

# Trigger
trigger: "library_unknown"
mode: "Standard"
context: "Intégration @tanstack/query v5 dans React app"
question: "Best practices et patterns pour React Query v5"
```

### Example 2: /debug with rare error

```yaml
# Context
Error: "EPERM: operation not permitted, symlink"
Context7 results: 1
WebSearch results: 3 (old, 2019-2020)

# Trigger
trigger: "bug_complex"
mode: "Deep Research"
context: "Erreur EPERM symlink sur Windows WSL2"
question: "Root causes et solutions pour EPERM symlink errors"
```

### Example 3: /brainstorm Phase 1 competitive

```yaml
# Context
Description: "système de notifications temps réel"
Flag: --competitive

# Trigger
trigger: "market"
mode: "Deep Research"
context: "Analyse marché notifications temps réel"
question: "Solutions existantes (Pusher, OneSignal, etc.), gaps, pricing"
```

### Example 4: /brainstorm Phase 2 weak axis

```yaml
# Context
EMS: 45, iteration: 3
weak_axes: ["Couverture"]

# Trigger
trigger: "targeted"
mode: "Standard"
context: "Améliorer couverture pour feature auth"
question: "Perspectives manquantes pour système authentication (security, UX, compliance)"
```
