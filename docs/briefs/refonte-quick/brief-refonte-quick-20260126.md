# CDC: Refonte du Skill /quick

> **Version**: PRD v3.0
> **Date**: 2026-01-26
> **EMS Final**: 76/100
> **Complexite**: STANDARD
> **Routing**: `/spec` -> `/implement`

---

## 1. Resume Executif

### Contexte

Le mode plan natif de Claude Code fait deja tres bien les phases Exploration et Plan automatiquement. Le skill `/quick` doit etre repense pour s'integrer comme **suite naturelle** du mode plan, sans dupliquer le travail.

### Objectif Principal

Refondre `/quick` pour qu'il soit :
1. La suite naturelle du mode plan de Claude Code natif
2. Un workflow simplifie par rapport a `/implement` (pas de Feature Document, moins de breakpoints)
3. Integre avec les stack skills et la memoire legere (index.json enrichi)

### Decisions Cles Validees

| Decision | Choix | Justification |
|----------|-------|---------------|
| Mode d'input | Plan-first + fallback text | Flexibilite sans sacrifier l'UX plan-native |
| Format memoire | index.json enrichi | Deja implemente v6.0.4, pas de fichier supplementaire |
| Subagents | @implementer only | Single agent pour workflow "mostly write" |
| Stack skills | Auto-detection | Detection automatique au debut du workflow |
| Documentation | Update only | MAJ CHANGELOG/README si impact, pas de Feature Doc |

---

## 2. Specifications Fonctionnelles

### 2.1 Workflow Cible

```
/quick [@plan-path | "description"]
        |
        v
[DETECT] Plan natif ou text ?
        |
        +-- Plan natif --> Skip E-P --> [C] --> [T] --> [D?] --> [M]
        |                                  |
        +-- Text --> Mini-[E] --> Mini-[P] --> [C] --> [T] --> [D?] --> [M]
                                        |
                                        +-- Auto-detect stack skill
```

### 2.2 Phases Detaillees

| Phase | Nom | Description | Skippable | Duree Cible |
|-------|-----|-------------|-----------|-------------|
| DETECT | Detection | Analyser input, detecter stack | Non | <1s |
| E | Mini-Explore | Scan codebase rapide | Oui (si @plan) | 5-10s |
| P | Mini-Plan | Planning minimal | Oui (si @plan) | 10-15s |
| C | Code | Implementation TDD via @implementer | Non | Variable |
| T | Test | Red-Green-Verify cycle | Non | 5-10s |
| D | Document | Update CHANGELOG/README | Conditionnel | 5s |
| M | Memory | MAJ index.json | Non | <1s |

### 2.3 Comparaison /quick vs /implement

| Aspect | /quick | /implement |
|--------|--------|------------|
| **Input** | @plan-path ou text | feature-slug + @spec/@plan |
| **Phases** | E-P (skippable) + C-T-D-M | E-P-C-I-M (full) |
| **Breakpoints** | 0-1 (optionnel plan) | 3+ (phase transitions) |
| **Feature Doc** | Non | Oui |
| **Code Review** | Skip | Full @code-reviewer |
| **Security Audit** | Skip | Conditionnel |
| **Subagents** | @implementer only | @implementer + reviewers |
| **Complexite** | TINY, SMALL | STANDARD, LARGE |
| **Duree cible** | <30s TINY, <90s SMALL | Variable |

### 2.4 Structure Plan Natif Attendue

Le plan doit etre un "vrai document" (pas un paragraphe) :

```markdown
# Plan: [Feature Name]

## Objectif
[1-2 phrases claires]

## Fichiers Concernes
- [ ] path/to/file1.ts -- [action: create|modify|delete]
- [ ] path/to/file2.ts -- [action]

## Etapes
1. [ ] [Action verb] [target] -- [critere de succes]
2. [ ] [Action verb] [target] -- [critere de succes]
3. [ ] [Action verb] [target] -- [critere de succes]

## Tests
- [ ] Test unitaire: [description]
- [ ] Test integration: [si applicable]

## Critere de Completion
[Comment savoir que c'est fini]
```

### 2.5 Detection Plan Natif

```python
def is_native_plan(file_path: str) -> bool:
    """Detecte si le fichier est un plan natif Claude Code."""
    # Pattern 1: Chemin conventionnel
    if ".claude/plans/" in file_path or "docs/plans/" in file_path:
        return True

    # Pattern 2: Frontmatter avec saved_at
    content = read_file(file_path)
    frontmatter = parse_yaml_frontmatter(content)
    if frontmatter and "saved_at" in frontmatter:
        return True

    return False
```

---

## 3. Specifications Techniques

### 3.1 Stack Detection

Pattern de registre declaratif avec scoring :

```python
STACK_SIGNATURES = {
    "python-django": {
        "files": ["manage.py", "settings.py", "wsgi.py"],
        "deps": {
            "requirements.txt": ["django"],
            "pyproject.toml": ["django"],
            "Pipfile": ["django"]
        },
        "dirs": ["templates/", "static/"],
        "confidence_base": 0.9
    },
    "javascript-react": {
        "files": ["package.json"],
        "deps": {
            "package.json": ["react", "react-dom"]
        },
        "dirs": ["src/components/", "src/pages/"],
        "extensions": [".tsx", ".jsx"],
        "confidence_base": 0.85
    },
    "java-springboot": {
        "files": ["pom.xml", "build.gradle", "build.gradle.kts"],
        "deps": {
            "pom.xml": ["spring-boot"],
            "build.gradle": ["org.springframework.boot"]
        },
        "dirs": ["src/main/java/"],
        "confidence_base": 0.9
    },
    "php-symfony": {
        "files": ["composer.json", "bin/console", "symfony.lock"],
        "deps": {
            "composer.json": ["symfony/framework-bundle"]
        },
        "dirs": ["src/Controller/", "src/Entity/"],
        "confidence_base": 0.9
    },
    "frontend-editor": {
        "files": ["tailwind.config.js", "tailwind.config.ts", "tailwind.config.mjs"],
        "deps": {
            "package.json": ["tailwindcss"]
        },
        "confidence_base": 0.8
    }
}

def detect_stack(root: str) -> list[StackResult]:
    """Detecte les stacks avec scoring de confidence."""
    results = []
    for stack_name, signatures in STACK_SIGNATURES.items():
        score = 0
        evidence = []

        # Check files
        for file in signatures.get("files", []):
            if exists(join(root, file)):
                score += 30
                evidence.append(f"file:{file}")

        # Check deps in manifests
        for manifest, deps in signatures.get("deps", {}).items():
            if exists(join(root, manifest)):
                content = read_file(join(root, manifest))
                for dep in deps:
                    if dep in content:
                        score += 25
                        evidence.append(f"dep:{dep}")

        # Check dirs
        for dir in signatures.get("dirs", []):
            if isdir(join(root, dir)):
                score += 15
                evidence.append(f"dir:{dir}")

        if score >= 30:  # Threshold minimum
            confidence = min(1.0, score / 100 * signatures["confidence_base"])
            results.append(StackResult(
                name=stack_name,
                confidence=confidence,
                evidence=evidence
            ))

    return sorted(results, key=lambda r: r.confidence, reverse=True)
```

### 3.2 Cycle TDD dans @implementer

Mode strict "Red -> Green" pour /quick :

```python
class TDDCycle:
    """Cycle TDD simplifie pour /quick."""

    def execute_task(self, task: Task) -> TaskResult:
        # RED: Ecrire test qui echoue
        test_code = self.generate_test(task.success_criteria)
        self.write_test(test_code)

        red_result = self.run_tests()
        if red_result.passed:
            return TaskResult(error="Test should fail initially (RED phase)")

        # GREEN: Code minimal pour faire passer
        impl_code = self.generate_minimal_impl(task, test_code)
        self.write_impl(impl_code)

        green_result = self.run_tests()
        if not green_result.passed:
            # Retry once
            impl_code = self.fix_impl(green_result.errors)
            self.write_impl(impl_code)
            green_result = self.run_tests()

        # VERIFY: Tests + lint OK
        lint_result = self.run_lint()

        return TaskResult(
            success=green_result.passed and lint_result.passed,
            files_modified=self.get_modified_files(),
            test_count=self.count_new_tests()
        )

    # Note: REFACTOR est SKIP pour /quick (vitesse > perfection)
```

### 3.3 Memory Update (index.json)

Schema enrichi v6.0.4 :

```json
{
  "id": "fix-login-button",
  "status": "completed",
  "current_phase": "memory",
  "complexity": "SMALL",
  "branch": "feature/fix-login-button",
  "created_at": "2026-01-26T10:00:00Z",
  "last_update": "2026-01-26T10:02:15Z",
  "created_by": "/quick",
  "summary": "Fixed login button alignment using flexbox centering",
  "modified_files": [
    "src/components/LoginButton.tsx",
    "src/components/LoginButton.test.tsx"
  ],
  "test_count": 2
}
```

### 3.4 Documentation Conditionnelle

Update CHANGELOG/README seulement si :
- Nouvelle feature visible (pas un bugfix interne)
- Impact sur API publique
- Changement de comportement utilisateur

```python
def should_update_docs(task_result: TaskResult, plan: Plan) -> bool:
    """Determine si la documentation doit etre mise a jour."""
    # Keywords indiquant changement visible
    visible_keywords = ["feature", "add", "new", "change", "breaking"]

    plan_text = plan.objective.lower()
    return any(kw in plan_text for kw in visible_keywords)
```

---

## 4. Contraintes

| Contrainte | Valeur | Rationale |
|------------|--------|-----------|
| Complexite max | SMALL (200 LOC, 3 fichiers) | Au-dela, /implement est plus adapte |
| Duree TINY | < 30s | One-shot rapide |
| Duree SMALL | < 90s | Workflow accelere |
| Subagent | @implementer only | Single agent pour "mostly write" |
| Breakpoints | 0-1 max | Fluidite du workflow |
| Tests | TDD obligatoire (Red-Green) | Qualite garantie |
| Refactor | Skip | Vitesse prioritaire |

---

## 5. Criteres de Succes

### 5.1 Fonctionnels

- [ ] /quick accepte @plan-path et skip E-P automatiquement
- [ ] /quick accepte text description avec mini-E-P
- [ ] Stack detection fonctionne pour les 5 stacks supportes
- [ ] Cycle TDD Red-Green execute correctement
- [ ] index.json mis a jour avec summary, modified_files, test_count
- [ ] Escalade vers /implement si complexite > SMALL

### 5.2 Performance

- [ ] TINY < 30s temps total
- [ ] SMALL < 90s temps total
- [ ] Stack detection < 1s
- [ ] Memory update < 1s

### 5.3 UX

- [ ] Zero breakpoint par defaut (fluidite)
- [ ] Message de completion clair avec stats
- [ ] Suggestion /implement si escalade necessaire

---

## 6. Risques

| Risque | Impact | Probabilite | Mitigation |
|--------|--------|-------------|------------|
| Plan natif mal formate | Medium | Medium | Validation structure + fallback parsing |
| Stack mal detecte | Low | Low | Confidence threshold + override manuel |
| TDD echoue en boucle | Medium | Low | Max 2 retries, puis escalade |
| Complexite sous-estimee | Medium | Medium | Re-evaluation apres E, suggestion /implement |

---

## 7. Dependances

### 7.1 Core Skills

- `complexity-calculator` : Validation scope, routing
- `state-manager` : Update index.json
- `tdd-enforcer` : Cycle Red-Green-Verify
- `project-memory` : Contexte projet

### 7.2 Stack Skills (auto-detection)

- `python-django`
- `javascript-react`
- `java-springboot`
- `php-symfony`
- `frontend-editor`

### 7.3 Subagents

- `@implementer` (Sonnet) : Execution TDD des taches

---

## 8. Livrables

| Livrable | Emplacement | Description |
|----------|-------------|-------------|
| SKILL.md refonte | `src/skills/quick/SKILL.md` | Workflow complet refait |
| Stack detection | `src/skills/quick/references/stack-detection.md` | Algorithme de detection |
| Plan structure | `src/skills/quick/references/plan-structure.md` | Format plan attendu |
| TDD rules | `src/skills/quick/references/tdd-rules.md` | Cycle Red-Green pour /quick |

---

## 9. Hors Scope

Ce CDC ne couvre PAS :
- Refonte de `/implement` (autre CDC)
- Nouveaux stack skills (extension future)
- Mode fully autonomous (sans humain)
- Integration CI/CD directe

---

## 10. Annexes

### A. Sources Perplexity Analysees

1. **Plan-first Workflow** : Cycle court plan -> code -> test -> commit valide
2. **TDD AI Automation** : Test-as-prompt, modes separes, garde-fous automatiques
3. **Stack Detection** : Registre declaratif, scoring, confidence thresholds
4. **Feature Memory** : MD pour narratif, JSON pour index (notre choix valide)
5. **Subagent Delegation** : Single agent pour "mostly write" (confirme @implementer only)

### B. Routing Complexity

```
IF complexity == TINY:
    -> /quick (full workflow)
ELSE IF complexity == SMALL:
    -> /quick (full workflow)
ELSE IF complexity == STANDARD:
    -> Suggest /implement
ELSE IF complexity == LARGE:
    -> Suggest /implement with enhanced reviews
```

---

*Document genere par brainstorm EPCI v6.0*
*EMS Final: 76/100 | Iterations: 3 | Duree: ~25 min*
