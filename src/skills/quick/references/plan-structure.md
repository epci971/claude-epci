# Plan Structure Reference

Format attendu pour les plans natifs Claude Code utilisés avec `/quick`.

## Structure Obligatoire

Un plan valide doit être un "vrai document" (pas un simple paragraphe) avec les sections suivantes :

```markdown
# Plan: [Feature Name]

## Objective
[1-2 phrases claires décrivant le but]

## Files
- [ ] path/to/file1.ts -- [action: create|modify|delete]
- [ ] path/to/file2.ts -- [action]

## Steps
1. [ ] [Action verb] [target] -- [critère de succès]
2. [ ] [Action verb] [target] -- [critère de succès]
3. [ ] [Action verb] [target] -- [critère de succès]

## Tests
- [ ] Unit: [description du test]
- [ ] Integration: [si applicable]

## Done When
[Critère clair de completion]
```

## Exemples de Plans Valides

### Exemple TINY (1 fichier, < 50 LOC)

```markdown
# Plan: Fix Login Button Alignment

## Objective
Center the login button horizontally using flexbox.

## Files
- [ ] src/components/LoginButton.tsx -- modify

## Steps
1. [ ] Add flex container class to button wrapper -- button centers
2. [ ] Add test for button alignment -- test passes

## Tests
- [ ] Unit: Button renders centered in container

## Done When
Login button is horizontally centered on all viewport sizes.
```

### Exemple SMALL (2-3 fichiers, < 200 LOC)

```markdown
# Plan: Add Email Validation

## Objective
Add client-side email validation to the registration form with error messages.

## Files
- [ ] src/components/RegisterForm.tsx -- modify
- [ ] src/utils/validation.ts -- create
- [ ] src/components/RegisterForm.test.tsx -- modify

## Steps
1. [ ] Create validation utility with email regex -- exports validateEmail
2. [ ] Add validation call on blur event -- shows error on invalid
3. [ ] Add error message component -- displays below input
4. [ ] Write tests for valid/invalid emails -- 3 tests pass

## Tests
- [ ] Unit: validateEmail returns true for valid emails
- [ ] Unit: validateEmail returns false for invalid emails
- [ ] Unit: RegisterForm shows error message on invalid email

## Done When
Invalid emails show error message, valid emails allow form submission.
```

## Détection de Plan Natif

### Pattern 1: Chemin Conventionnel

```python
PLAN_PATHS = [
    ".claude/plans/",
    "docs/plans/",
    ".plans/"
]

def is_conventional_path(path: str) -> bool:
    return any(p in path for p in PLAN_PATHS)
```

### Pattern 2: Frontmatter avec saved_at

Plans sauvegardés par Claude Code incluent :

```yaml
---
saved_at: 2026-01-26T10:00:00Z
title: Fix Login Button
---
```

```python
def has_saved_at_frontmatter(content: str) -> bool:
    import yaml
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            frontmatter = yaml.safe_load(parts[1])
            return frontmatter and "saved_at" in frontmatter
    return False
```

## Validation du Plan

### Checks Obligatoires

| Check | Validation |
|-------|------------|
| Has Objective | Non vide, 1-2 phrases |
| Has Files | Au moins 1 fichier listé |
| Has Steps | Au moins 1 step avec verbe d'action |
| Has Tests | Au moins 1 test défini |
| Has Done When | Critère de completion clair |

### Limites pour /quick

| Métrique | TINY | SMALL | Trop Grand |
|----------|------|-------|------------|
| Files | 1-2 | 2-3 | 4+ |
| Steps | 1-3 | 3-5 | 6+ |
| LOC estimé | < 50 | < 200 | 200+ |

## Parsing du Plan

Extraction des informations clés :

```python
def parse_plan(content: str) -> dict:
    """Parse plan markdown into structured data."""
    return {
        "title": extract_title(content),        # From # heading
        "objective": extract_section(content, "Objective"),
        "files": extract_file_list(content, "Files"),
        "steps": extract_checklist(content, "Steps"),
        "tests": extract_checklist(content, "Tests"),
        "done_when": extract_section(content, "Done When"),
    }

def extract_file_list(content: str, section: str) -> list:
    """Extract files with actions."""
    # Pattern: - [ ] path/to/file -- action
    pattern = r"- \[[ x]\] (.+?) -- (.+)"
    matches = re.findall(pattern, section_content)
    return [{"path": m[0], "action": m[1]} for m in matches]
```

## Fallback Parsing

Si le plan n'a pas la structure exacte, tenter extraction heuristique :

1. Chercher les chemins de fichiers mentionnés
2. Chercher les verbes d'action (add, fix, update, create)
3. Inférer l'objectif du titre ou premier paragraphe

```python
def fallback_parse(content: str) -> dict:
    """Heuristic parsing for non-standard plans."""
    files = re.findall(r"[a-zA-Z_/]+\.[a-z]+", content)
    actions = re.findall(r"\b(add|fix|update|create|modify|delete)\b", content.lower())

    return {
        "files": list(set(files))[:3],  # Max 3 files
        "inferred_action": actions[0] if actions else "modify",
        "raw_content": content
    }
```
