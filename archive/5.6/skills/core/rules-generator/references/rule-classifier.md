# Rule Classifier

Reference pour la classification et le routage des règles dans `/rules` mode ADD.

---

## 1. Input Classification

### Détection "Est-ce une règle ?"

**Indicateurs positifs** (score += 0.2 chacun) :

| Catégorie | Patterns |
|-----------|----------|
| Impératifs | "toujours", "jamais", "doit", "ne pas", "interdit", "obligatoire" |
| Recommandations | "devrait", "préférer", "éviter", "convention", "standard" |
| Scope | "dans les fichiers", "pour le code", "en Python", "composants React" |
| Structure | "[contexte] + [action/contrainte]" |

**Indicateurs négatifs** (score -= 0.3 chacun) :

| Pattern | Raison |
|---------|--------|
| "?" en fin | Question, pas une règle |
| "génère", "crée les règles" | Demande workflow complet |
| "--force", "--validate-only" | Flags explicites → workflow standard |

**Seuils** :

| Score | Action |
|-------|--------|
| >= 0.7 | Mode ADD activé |
| 0.4 - 0.7 | Demander confirmation : "Voulez-vous ajouter une règle ?" |
| < 0.4 | Workflow standard (génération complète) |

---

## 2. Severity Detection

### Mapping mots-clés → sévérité

```
🔴 CRITICAL (score_critical)
├── "doit" (+0.4)
├── "obligatoire" (+0.5)
├── "jamais" (+0.5)
├── "interdit" (+0.5)
├── "critique" (+0.4)
├── "bloquant" (+0.4)
└── "ne pas" + verbe (+0.3)

🟡 CONVENTIONS (score_convention)
├── "devrait" (+0.4)
├── "convention" (+0.5)
├── "standard" (+0.4)
├── "recommandé" (+0.4)
├── "normalement" (+0.3)
└── "éviter" (+0.3)

🟢 PREFERENCES (score_preference)
├── "préférer" (+0.5)
├── "idéalement" (+0.4)
├── "si possible" (+0.4)
├── "optionnel" (+0.5)
├── "quand applicable" (+0.3)
└── "considérer" (+0.3)
```

### Algorithme de décision

```
severity = max(score_critical, score_convention, score_preference)

IF severity < 0.3:
   → Demander clarification via @rule-clarifier
ELSE:
   → Utiliser la sévérité avec le score max
```

---

## 3. Scope Extraction

### Patterns de détection

| Input Pattern | Extracted Scope |
|---------------|-----------------|
| "fichiers Python" | `**/*.py` |
| "code Python" | `**/*.py` |
| "dans backend/" | `backend/**/*` |
| "backend Python" | `backend/**/*.py` |
| "dans frontend/" | `frontend/**/*` |
| "composants React" | `**/*.tsx` |
| "fichiers TypeScript" | `**/*.ts` |
| "tests" | `**/test_*.py` ou `**/*.test.ts` |
| "tests Python" | `**/test_*.py` |
| "tests Jest" | `**/*.test.ts`, `**/*.test.tsx` |
| "API", "endpoints" | `**/api/**/*.py` ou `**/routes/**/*.ts` |
| "modèles", "models" | `**/models/**/*` |
| "services" | `**/services/**/*` |
| "hooks React" | `**/hooks/**/*.ts` |

### Fallback par stack détecté

Si aucun scope explicite mais stack détectable :

```
IF requirements.txt OR pyproject.toml exists:
   → Default: **/*.py

IF package.json + react exists:
   → Default: **/*.tsx, **/*.ts

IF composer.json + symfony exists:
   → Default: **/*.php

IF pom.xml OR build.gradle exists:
   → Default: **/*.java
```

### Scope global

Si vraiment aucun indice :
- Scope = `[]` (vide = global)
- Destination = `CLAUDE.md`

---

## 4. Placement Decision

### Arbre de décision

```
                    Input scope
                         │
         ┌───────────────┴───────────────┐
         │                               │
    Global (vide)                   Spécifique
         │                               │
         ▼                               ▼
    CLAUDE.md                  Fichier rules/ existant
                               avec paths similaires ?
                                    │
                         ┌──────────┴──────────┐
                         │                     │
                        OUI                   NON
                         │                     │
                         ▼                     ▼
                   Append au              Créer nouveau
                   fichier existant       rules/*.md
```

### Matching fichiers existants

```python
def find_matching_rule_file(new_scope: str, rules_dir: Path) -> Optional[Path]:
    """Trouve le fichier rules le plus approprié pour le scope."""
    best_match = None
    best_overlap = 0.0
    
    for rule_file in rules_dir.glob("*.md"):
        existing_paths = extract_paths_from_frontmatter(rule_file)
        overlap = calculate_path_overlap(new_scope, existing_paths)
        
        if overlap > best_overlap and overlap > 0.7:
            best_overlap = overlap
            best_match = rule_file
    
    return best_match
```

### Calcul overlap

```
overlap = |intersection(new_patterns, existing_patterns)| / |new_patterns|

Exemple:
- new_scope: backend/**/*.py
- existing: backend/**/*.py, backend/**/test_*.py
- overlap: 1.0 (100% match) → append au fichier existant
```

### Naming nouveau fichier

| Scope détecté | Nom fichier |
|---------------|-------------|
| `**/*.py` | `python-conventions.md` |
| `backend/**/*.py` | `backend-python.md` |
| `frontend/**/*.tsx` | `frontend-react.md` |
| `**/test_*.py` | `testing-python.md` |
| `**/*.ts` | `typescript-conventions.md` |
| Autre | `rules-custom.md` |

---

## 5. Clarity Score

### Calcul du score de clarté

```
clarity = 0.0

# Scope clair ?
IF scope explicitement mentionné:
   clarity += 0.4
ELIF scope déductible du contexte:
   clarity += 0.2

# Sévérité claire ?
IF severity_score >= 0.3:
   clarity += 0.3

# Contenu actionnable ?
IF rule contient verbe d'action:
   clarity += 0.2

IF rule > 5 mots:
   clarity += 0.1
```

### Seuils

| Clarity | Action |
|---------|--------|
| >= 0.8 | Reformulation directe |
| 0.5 - 0.8 | 1-2 questions ciblées |
| < 0.5 | Clarification complète (3 questions) |

---

## 6. Exemples complets

### Exemple 1 : Input clair

```
Input: "Les fichiers Python dans backend/ doivent toujours avoir des docstrings"

Classification:
- is_rule: 0.9 ("doivent", "toujours", structure [contexte]+[action])
- severity: CRITICAL (0.9 - "doit", "toujours")
- scope: backend/**/*.py (explicite)
- clarity: 0.9

→ Reformulation directe, pas de clarification
```

### Exemple 2 : Input ambigu

```
Input: "Faire attention aux injections SQL"

Classification:
- is_rule: 0.5 ("attention" faible indicateur)
- severity: ? (aucun mot-clé)
- scope: ? (aucun indice)
- clarity: 0.3

→ Clarification via @rule-clarifier
   Q1: Quel scope ? (API, backend, tous?)
   Q2: Quelle sévérité ? (probablement CRITICAL)
```

### Exemple 3 : Input semi-clair

```
Input: "Préférer les composants fonctionnels en React"

Classification:
- is_rule: 0.8 ("préférer", structure claire)
- severity: PREFERENCES (0.5 - "préférer")
- scope: **/*.tsx (déduit de "React")
- clarity: 0.7

→ 1 question possible sur le scope exact
   Ou reformulation avec scope suggéré
```

---

## 7. Quick Reference

| Élément | Seuil | Action |
|---------|-------|--------|
| is_rule | >= 0.7 | Mode ADD |
| clarity | >= 0.8 | Reformulation directe |
| clarity | < 0.8 | @rule-clarifier |
| overlap | >= 0.7 | Append fichier existant |
| tokens | > 1800 | Warning limite proche |
