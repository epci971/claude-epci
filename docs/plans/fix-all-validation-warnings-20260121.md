# Plan de Correction des Warnings de Validation

> **Date**: 2026-01-21
> **Version cible**: 5.6.5
> **Objectif**: 109/109 validations passent (actuellement 75/109)

---

## Resume Executif

| Categorie | Issues | Effort | Priorite |
|-----------|--------|--------|----------|
| Phase 1: Scripts de validation | 3 scripts | 1h | CRITIQUE |
| Phase 2: Cross-references agents | 12 refs | 30min | HIGH |
| Phase 3: Skills descriptions | 7 skills | 45min | MEDIUM |
| Phase 4: Documentation externe | 190 refs | 30min | MEDIUM |
| Phase 5: Agents optimisation | 2 agents | 30min | LOW |
| Phase 6: Commande brainstorm | 1 fichier | 20min | LOW |
| **TOTAL** | ~215 issues | ~3h30 | |

---

## Phase 1: Correction des Scripts de Validation (CRITIQUE)

### 1.1 Mise a jour `validate_command.py` - Liste des tools

**Fichier**: `src/scripts/validate_command.py`
**Ligne**: ~114-117

**Probleme**: La liste `valid_tools` est incomplete (manque WebSearch, AskUserQuestion, patterns Bash).

**Code actuel**:
```python
valid_tools = [
    'Read', 'Write', 'Edit', 'Bash', 'Grep', 'Glob',
    'Task', 'WebFetch', 'LS', 'MultiEdit'
]
```

**Code corrige**:
```python
valid_tools = [
    # Core tools
    'Read', 'Write', 'Edit', 'Bash', 'Grep', 'Glob',
    'Task', 'WebFetch', 'LS', 'MultiEdit',
    # Additional Claude Code tools
    'WebSearch', 'AskUserQuestion', 'TodoWrite',
    'NotebookEdit', 'KillShell', 'TaskOutput',
]

# Bash patterns (accepted as Bash tool with restrictions)
bash_patterns = [
    'Bash(git:*)', 'Bash(python3:*)', 'Bash(npm:*)',
    'Bash(php:*)', 'Bash(pytest:*)', 'Bash(eslint:*)',
    'Bash(flake8:*)', 'Bash(mkdir:*)', 'Bash(ln:*)',
    'Bash(touch:*)', 'Bash(chmod:*)',
]
```

**Modifier la fonction `validate_allowed_tools`**:
```python
def validate_allowed_tools(frontmatter: dict, report: ValidationReport) -> bool:
    """Verifie allowed-tools."""
    tools = frontmatter.get('allowed-tools', [])

    valid_tools = [
        'Read', 'Write', 'Edit', 'Bash', 'Grep', 'Glob',
        'Task', 'WebFetch', 'LS', 'MultiEdit',
        'WebSearch', 'AskUserQuestion', 'TodoWrite',
        'NotebookEdit', 'KillShell', 'TaskOutput',
    ]

    if tools:
        for tool in tools:
            # Check for Bash patterns like Bash(git:*)
            if tool.startswith('Bash(') and tool.endswith(')'):
                continue  # Accept all Bash restriction patterns
            if tool not in valid_tools:
                report.add_warning(f"Unknown tool: {tool}")

    print(f"[OK] Allowed-tools: {len(tools)} tools defined")
    report.pass_check()
    return True
```

---

### 1.2 Mise a jour `validate_markdown_refs.py` - Exclusion docs externes

**Fichier**: `src/scripts/validate_markdown_refs.py`

**Probleme**: Le script valide les fichiers dans `docs/librairies/` qui sont des projets externes importes avec leurs propres liens relatifs.

**Solution**: Ajouter une liste d'exclusions pour les dossiers de documentation externe.

**Ajouter en haut du fichier**:
```python
# Directories to exclude from validation (external imported docs)
EXCLUDED_DIRS = [
    'docs/librairies',
    'docs/external',
    'docs/archives',
    'archive',
]

def is_excluded_path(file_path: Path, base_path: Path) -> bool:
    """Check if file is in an excluded directory."""
    try:
        rel_path = file_path.relative_to(base_path)
        rel_str = str(rel_path)
        return any(rel_str.startswith(excl) for excl in EXCLUDED_DIRS)
    except ValueError:
        return False
```

**Modifier la boucle de scan pour exclure ces dossiers**.

---

### 1.3 Correction `test_triggering.py` - Bug dans l'algorithme

**Fichier**: `src/scripts/test_triggering.py`

**Bug identifie**: L'algorithme `should_trigger()` extrait les mots-cles de TOUTE la description, y compris la section "Not for:". Resultat: quand on teste "email writing", les mots "email" et "writing" sont trouves car ils font partie du texte "Not for: email writing" dans la description.

**Correction**: Separer l'extraction des mots-cles positifs (Use when) et negatifs (Not for).

```python
def extract_use_when_keywords(description: str) -> set:
    """Extrait les mots-cles UNIQUEMENT de la section 'Use when:'."""
    # Trouver la section "Use when:" jusqu'au prochain point ou "Not for:"
    use_when_match = re.search(
        r'Use when[:\s]+(.+?)(?:\.|\s+Not for:|$)',
        description,
        re.IGNORECASE | re.DOTALL
    )
    if not use_when_match:
        # Fallback: extraire de la description principale (avant "Use when:")
        main_desc = re.split(r'Use when:', description, flags=re.IGNORECASE)[0]
        text = main_desc.lower()
    else:
        text = use_when_match.group(1).lower()

    # Mots-cles significatifs (4+ lettres)
    keywords = set(re.findall(r'\b[a-z]{4,}\b', text))

    # Filtrer les mots communs
    stop_words = {
        'when', 'with', 'that', 'this', 'from', 'have', 'been',
        'will', 'your', 'they', 'more', 'some', 'about', 'which',
        'their', 'would', 'make', 'like', 'just', 'into', 'over',
        'such', 'only', 'also', 'after', 'most', 'than', 'them',
        'should', 'could', 'other', 'load', 'invoke', 'auto',
        'need', 'work', 'help', 'used', 'uses', 'using'
    }
    return keywords - stop_words


def extract_not_for_phrases(description: str) -> List[str]:
    """Extrait les phrases d'exclusion de 'Not for:'."""
    not_for_match = re.search(
        r'Not for[:\s]+([^.]+)',
        description,
        re.IGNORECASE
    )
    if not not_for_match:
        return []

    not_for_text = not_for_match.group(1)
    # Separer par virgules et nettoyer
    phrases = [p.strip().lower() for p in not_for_text.split(',')]
    return [p for p in phrases if p]


def should_trigger(query: str, description: str) -> bool:
    """Determine si une requete devrait declencher le skill."""
    query_lower = query.lower()

    # Extraire mots-cles UNIQUEMENT de "Use when:" (pas de "Not for:")
    keywords = extract_use_when_keywords(description)

    if not keywords:
        return False

    # Verifier combien de mots-cles apparaissent dans la requete
    matches = sum(1 for kw in keywords if kw in query_lower)

    # Seuil: au moins 2 mots-cles correspondants
    return matches >= 2


def should_not_trigger(query: str, description: str) -> bool:
    """Determine si une requete NE devrait PAS declencher le skill."""
    query_lower = query.lower()

    # Extraire les phrases d'exclusion
    exclusions = extract_not_for_phrases(description)

    if not exclusions:
        # Pas d'exclusions definies - verifier qu'on ne matche pas positivement
        return not should_trigger(query, description)

    # Verifier si une phrase d'exclusion complete est presente
    for phrase in exclusions:
        # Chercher des mots significatifs de la phrase dans la query
        phrase_words = set(re.findall(r'\b[a-z]{4,}\b', phrase))
        if phrase_words:
            matches = sum(1 for w in phrase_words if w in query_lower)
            # Si 50%+ des mots de la phrase sont presents, c'est une exclusion
            if matches >= max(1, len(phrase_words) // 2):
                return True  # Correctement exclu (ne devrait PAS trigger)

    # Aucune exclusion matchee - verifier qu'on ne trigger pas positivement
    return not should_trigger(query, description)
```

**Modifier aussi `test_skill_triggering()`**:
```python
# Tests negatifs (ne doivent pas trigger)
for i, query in enumerate(negative_queries):
    exclusion_text = negative_triggers[i] if i < len(negative_triggers) else query
    result = should_not_trigger(query, description)
    report.negative_triggers.append((exclusion_text, result))
    if result:
        report.add_pass()
    else:
        report.add_fail()
```

---

## Phase 2: Correction des Cross-References Agents (HIGH)

### 2.1 Fichiers references manquants dans agents

| Agent | Reference | Action |
|-------|-----------|--------|
| `expert-panel.md` | `experts/martin.md` | Creer fichier stub |
| `expert-panel.md` | `experts/fowler.md` | Creer fichier stub |
| `expert-panel.md` | `experts/newman.md` | Creer fichier stub |
| `expert-panel.md` | `experts/gamma.md` | Creer fichier stub |
| `expert-panel.md` | `experts/beck.md` | Creer fichier stub |
| `ems-evaluator.md` | `ems-system.md` | Deja existe dans brainstormer/references/ - corriger le chemin |
| `technique-advisor.md` | `technique-mapping.md` | Deja existe dans brainstormer/references/ - corriger le chemin |
| `party-orchestrator.md` | `party-personas.md` | Deja existe dans brainstormer/references/ - corriger le chemin |

### 2.2 Creer le dossier experts/

```bash
mkdir -p src/agents/references/experts/
```

### 2.3 Creer les fichiers experts (template)

**Template pour chaque expert** (`src/agents/references/experts/{name}.md`):

```markdown
# Expert: {Full Name}

## Domain
{Domain of expertise}

## Key Contributions
- {Contribution 1}
- {Contribution 2}

## Perspective Style
{How this expert approaches problems}

## Typical Questions
- "{Question 1}"
- "{Question 2}"
```

**Fichiers a creer**:
- `martin.md` - Robert C. Martin (Clean Code, SOLID)
- `fowler.md` - Martin Fowler (Refactoring, Enterprise Patterns)
- `newman.md` - Sam Newman (Microservices)
- `gamma.md` - Erich Gamma (Design Patterns, Gang of Four)
- `beck.md` - Kent Beck (TDD, XP, Patterns)

### 2.4 Corriger les chemins dans les agents

**expert-panel.md** - Changer:
```markdown
references/experts/martin.md  → ../agents/references/experts/martin.md
```

**ems-evaluator.md** - Changer:
```markdown
ems-system.md → ../../skills/core/brainstormer/references/ems-system.md
```

**technique-advisor.md** - Changer:
```markdown
technique-mapping.md → ../../skills/core/brainstormer/references/technique-mapping.md
```

**party-orchestrator.md** - Changer:
```markdown
party-personas.md → ../../skills/core/brainstormer/references/party-personas.md
```

---

## Phase 3: Correction des Skills Descriptions (MEDIUM)

### 3.1 Skills sans "Use when:" et "Not for:"

| Skill | Fichier |
|-------|---------|
| `personas` | `src/skills/personas/SKILL.md` |
| `mcp` | `src/skills/mcp/SKILL.md` |
| `learning-optimizer` | `src/skills/core/learning-optimizer/SKILL.md` |
| `project-memory` | `src/skills/core/project-memory/SKILL.md` |
| `proactive-suggestions` | `src/skills/core/proactive-suggestions/SKILL.md` |
| `debugging-strategy` | `src/skills/core/debugging-strategy/SKILL.md` |
| `breakpoint-metrics` | `src/skills/core/breakpoint-metrics/SKILL.md` |

### 3.2 Template de description corrigee

Chaque description doit suivre ce format:
```
{Description principale}. Use when: {trigger conditions}. Not for: {exclusions}.
```

**Exemples de corrections**:

#### personas
```yaml
description: |
  Auto-activates specialized personas based on task context scoring.
  Use when: task matches domain expertise (architecture, frontend, backend, security, QA, doc).
  Not for: simple questions, brainstorming sessions (use brainstormer personas instead).
```

#### mcp
```yaml
description: |
  MCP server integration for external capabilities (Context7, Sequential, Magic, Playwright, Notion).
  Use when: persona detected, MCP flags used, or external context needed.
  Not for: simple tasks without external documentation or UI generation needs.
```

#### learning-optimizer
```yaml
description: |
  Calibration and learning system for EPCI workflows. Tracks estimation accuracy and user preferences.
  Use when: discussing estimation accuracy, calibration metrics, or suggestion scoring.
  Not for: basic EPCI usage, simple feature implementation.
```

#### project-memory
```yaml
description: |
  Project Memory management for EPCI workflows. Loads context, persists history, provides conventions.
  Use when: workflow start, feature completion, pattern lookup needed.
  Not for: ephemeral tasks, one-off questions without project context.
```

#### proactive-suggestions
```yaml
description: |
  Generates actionable suggestions from code review findings and discovery insights.
  Use when: /epci BP2 reached, code review done, or /brainstorm --suggest flag used.
  Not for: /quick workflows, or when suggestions disabled in learning preferences.
```

#### debugging-strategy
```yaml
description: |
  Structured debugging methodology with thought tree analysis and solution scoring.
  Use when: /debug called, error or bug mentioned, stack trace provided.
  Not for: feature development, refactoring without bugs.
```

#### breakpoint-metrics
```yaml
description: |
  Calculates and displays metrics at EPCI breakpoints (BP1/BP2).
  Use when: /epci BP1 or BP2 reached, complexity scoring for STANDARD/LARGE features.
  Not for: /quick workflows, /brainstorm sessions.
```

---

## Phase 4: Exclusion Documentation Externe (MEDIUM)

### 4.1 Option A: Modifier le validateur (recommande)

Deja couvert dans Phase 1.2.

### 4.2 Option B: Deplacer vers archive/

```bash
# Deplacer les docs externes vers archive/
mv docs/librairies archive/librairies-reference
```

Puis mettre a jour `.gitignore` si necessaire.

### 4.3 Fichiers dans src/ avec liens casses

Ces fichiers dans `src/skills/` ont des liens d'exemple qui ne doivent pas etre valides:

| Fichier | Ligne | Reference | Action |
|---------|-------|-----------|--------|
| `rules-catalog.md` | 92 | `[text](url)` | Exemple - marquer comme tel |
| `content-rules.md` | 96+ | `src/utils/helpers.js` | Exemple - marquer comme tel |
| `best-practices.md` | 79+ | `references/*.md` | Creer ou supprimer |
| `domain-templates.md` | 44+ | `references/*.md`, `templates/*.md` | Creer ou supprimer |

**Solution**: Ajouter un commentaire `<!-- example -->` ou creer les fichiers stub.

---

## Phase 5: Optimisation Agents (LOW)

### 5.1 technique-advisor.md - Trop long

**Probleme**: ~3369 tokens (recommande < 2000)

**Solution**: Extraire le contenu detaille vers `references/technique-selection.md`

### 5.2 implementer.md - Trop de write tools

**Probleme**: 3 write tools (Write, Edit, NotebookEdit)

**Solution**: Acceptable pour un implementer. Documenter pourquoi dans le fichier.

---

## Phase 6: Commande brainstorm.md (LOW)

### 6.1 Content trop long

**Probleme**: ~5975 tokens (limite 5000)

**Solution**:
1. Extraire les sections detaillees vers `references/brainstorm/`
2. Ou accepter le depassement avec justification

---

## Checklist d'Implementation

### Phase 1 (Scripts)
- [ ] 1.1 Mettre a jour `validate_command.py` - valid_tools
- [ ] 1.2 Mettre a jour `validate_markdown_refs.py` - exclusions
- [ ] 1.3 Mettre a jour `test_triggering.py` - algorithme

### Phase 2 (Cross-refs)
- [ ] 2.1 Creer `src/agents/references/experts/`
- [ ] 2.2 Creer martin.md, fowler.md, newman.md, gamma.md, beck.md
- [ ] 2.3 Corriger chemins dans expert-panel.md
- [ ] 2.4 Corriger chemins dans ems-evaluator.md
- [ ] 2.5 Corriger chemins dans technique-advisor.md
- [ ] 2.6 Corriger chemins dans party-orchestrator.md
- [ ] 2.7 Corriger reference rule-classifier.md dans rules.md
- [ ] 2.8 Corriger reference brief-format.md dans brainstorm.md

### Phase 3 (Skills descriptions)
- [ ] 3.1 Corriger personas/SKILL.md
- [ ] 3.2 Corriger mcp/SKILL.md
- [ ] 3.3 Corriger learning-optimizer/SKILL.md
- [ ] 3.4 Corriger project-memory/SKILL.md
- [ ] 3.5 Corriger proactive-suggestions/SKILL.md
- [ ] 3.6 Corriger debugging-strategy/SKILL.md
- [ ] 3.7 Corriger breakpoint-metrics/SKILL.md

### Phase 4 (Docs externes)
- [ ] 4.1 Verifier exclusions dans validate_markdown_refs.py
- [ ] 4.2 Optionnel: deplacer docs/librairies vers archive/

### Phase 5 (Agents optim)
- [ ] 5.1 Optionnel: refactorer technique-advisor.md
- [ ] 5.2 Documenter implementer.md write tools

### Phase 6 (Brainstorm)
- [ ] 6.1 Optionnel: reduire brainstorm.md tokens

---

## Verification Finale

```bash
# Apres toutes les corrections
python3 src/scripts/validate_all.py

# Attendu:
# RESULT: ✅ ALL VALIDATIONS PASSED (109/109)
```

---

## Notes

- Les Phases 1-3 sont obligatoires pour atteindre 100% de validation
- Les Phases 4-6 sont des optimisations recommandees
- Temps estime total: ~3h30
- Peut etre fait en plusieurs sessions
