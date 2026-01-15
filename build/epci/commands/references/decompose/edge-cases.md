# Decompose Edge Cases

> Reference file for `/decompose` command edge case handling.

---

## EC1: PRD Without Clear Structure

**Detection:** Less than 3 `##` headers or no "Phase/Step" patterns.

**Behavior:**

```
Document structure insufficient.

Proposed structuring:

## Proposed Structure

1. Phase Preparation (estimated: Xd)
   - ...

2. Phase Implementation (estimated: Xd)
   - ...

3. Phase Validation (estimated: Xd)
   - ...

Options: [Validate structure] [Modify] [Cancel]
```

---

## EC2: PRD Too Small

**Detection:** Total estimated effort < 3 days.

**Behavior:**

```
This document seems simple enough for a single EPCI session.

Estimated effort: {X} days
Recommendation: Use /brief directly

/brief @{file}
```

**No decomposition** — command ends.

---

## EC3: Sub-Spec Too Large

**Detection:** A sub-spec exceeds `--max-days`.

**Behavior:**

```
ALERT: Sub-spec {ID} too large ({X} days estimated)

Suggestion: Split {ID} into sub-parts:
  {ID}a: {title_a} ({Xa}d)
  {ID}b: {title_b} ({Xb}d)

Options:
[1] Apply sub-decomposition
[2] Keep {ID} as is
[3] Define manually
```

---

## EC4: Circular Dependency

**Detection:** Cycle in dependency graph.

**Behavior:**

```
ERROR: Circular dependency detected

{SA} → {SB} → {SA}

This indicates an error in the source document.

Document references:
  Line {X}: "{quote_1}"
  Line {Y}: "{quote_2}"

Options:
[1] Ignore {SA}→{SB}
[2] Ignore {SB}→{SA}
[3] Cancel — Fix source document
```

---

## EC5: Missing Estimates

**Detection:** No estimation patterns found.

**Behavior:**

```
No estimates found in document

Using default estimates based on:
  Lines per section
  Detected complexity (models, services, tests)

Estimates are indicative. Adjust if needed.
```

---

## EC6: Brainstorm Brief Input

**Detection:** `### US1 —` pattern found, no `## Phase` patterns.

**Behavior:**

```
📋 Format détecté: Brief Brainstorm (User Stories)

Mapping User Stories → Sous-specs:

| US  | Titre           | Complexité | Effort | Priorité    |
|-----|-----------------|------------|--------|-------------|
| US1 | {title}         | M          | 3j     | Must-have   |
| US2 | {title}         | S          | 1j     | Should-have |
| US3 | {title}         | L          | 5j     | Could-have  |

Dépendances détectées: US3 → US1 (via AC reference)

Options: [Valider] [Modifier mapping] [Annuler]
```

**Mapping rules:**

| Complexité | Effort |
|------------|--------|
| S (Small)  | 1 jour |
| M (Medium) | 3 jours |
| L (Large)  | 5 jours |

| Priorité MoSCoW | Priority |
|-----------------|----------|
| Must-have       | 1        |
| Should-have     | 2        |
| Could-have      | 3        |
| Won't-have      | Excluded |
