# Rules Catalog — Command Auditor

> 95 rules across 7 categories for auditing EPCI commands

---

## Overview

| Category | Code | Rules | Focus |
|----------|------|-------|-------|
| Frontmatter | FM | 15 | YAML syntax, metadata |
| Structure | ST | 20 | Sections, organization |
| Rédaction | RD | 25 | Content quality |
| Workflow | WF | 10 | Process logic |
| Integration | IN | 15 | Skills, subagents, hooks |
| Detection | DG | 10 | Generation suggestions |
| **Total** | | **95** | |

---

## Severity Distribution

| Severity | Count | Score Impact | Action Required |
|----------|-------|--------------|-----------------|
| BLOQUANT | 12 | -10 points | Must fix before merge |
| ERREUR | 45 | -3 points | Should fix |
| WARNING | 28 | -1 point | Consider fixing |
| SUGGESTION | 10 | 0 points | Optional improvement |

---

## Quick Index by Category

### CAT-FM: Frontmatter (15 rules)

| ID | Règle | Sévérité |
|----|-------|----------|
| FM-001 | Frontmatter YAML présent (délimiteurs `---`) | BLOQUANT |
| FM-002 | Champ `description` obligatoire | BLOQUANT |
| FM-003 | Description ≤ 500 caractères | ERREUR |
| FM-004 | Description commence par verbe infinitif | ERREUR |
| FM-005 | Frontmatter < 15 lignes | WARNING |
| FM-006 | `argument-hint` si commande accepte des args | ERREUR |
| FM-007 | Format argument-hint: `[optionnel]` `<requis>` `--flag` | ERREUR |
| FM-008 | `allowed-tools` si outils restreints | WARNING |
| FM-009 | Outils déclarés valides (Read, Write, Edit, Bash, etc.) | ERREUR |
| FM-010 | Bash restreint par pattern `Bash(cmd:*)`, jamais `Bash(*)` | BLOQUANT |
| FM-011 | Pas de tabs dans YAML (espaces uniquement) | BLOQUANT |
| FM-012 | Caractères spéciaux échappés (:, #, ") | BLOQUANT |
| FM-013 | Pas de champs non reconnus dans frontmatter | WARNING |
| FM-014 | Si `!` utilisé dans contenu → `allowed-tools` doit inclure `Bash` | BLOQUANT |
| FM-015 | Budget description < 15,000 caractères | WARNING |

→ Details: [frontmatter-rules.md](frontmatter-rules.md)

### CAT-ST: Structure (20 rules)

| ID | Règle | Sévérité |
|----|-------|----------|
| ST-001 | Section `## Overview` présente | BLOQUANT |
| ST-002 | Overview: 2-4 phrases maximum | ERREUR |
| ST-003 | Section `## Process` ou `## Workflow` présente | BLOQUANT |
| ST-004 | Process: étapes numérotées ou `### Step N:` | ERREUR |
| ST-005 | Section `## Output` présente | ERREUR |
| ST-006 | Section `## Arguments` si argument-hint présent | ERREUR |
| ST-007 | Arguments en format tableau ou liste structurée | WARNING |
| ST-008 | Section `## Skills Loaded` si skills utilisés | ERREUR |
| ST-009 | Section `## Subagents` si subagents invoqués | ERREUR |
| ST-010 | Au moins 1 exemple concret | WARNING |
| ST-011 | Longueur totale 50-200 lignes (idéal) | WARNING |
| ST-012 | Longueur totale < 500 lignes (max) | ERREUR |
| ST-013 | Headers corrects (## sections, ### sous-sections) | ERREUR |
| ST-014 | Pas de sections vides | ERREUR |
| ST-015 | Ordre logique des sections | WARNING |
| ST-016 | Section `## Error Handling` pour commandes complexes | WARNING |
| ST-017 | Section `## Constraints` ou `## Boundaries` | WARNING |
| ST-018 | Breakpoints en format ASCII box si présents | ERREUR |
| ST-019 | Section `## See Also` si commandes liées | WARNING |
| ST-020 | Section `## Flags` si flags documentés | ERREUR |

→ Details: [structure-rules.md](structure-rules.md)

### CAT-RD: Rédaction (25 rules)

| ID | Règle | Sévérité |
|----|-------|----------|
| RD-001 | Longueur totale < 5000 tokens (~20KB) | BLOQUANT |
| RD-002 | Pas de contenu dupliqué entre sections | ERREUR |
| RD-003 | Code blocks avec langage spécifié | WARNING |
| RD-004 | Tables pour données structurées | WARNING |
| RD-005 | Références externes avec syntaxe `@fichier` | ERREUR |
| RD-006 | Pas de liens markdown `[text](url)` pour refs internes | ERREUR |
| RD-007 | Invocations subagents: format `@subagent-name` | ERREUR |
| RD-008 | Impératifs pour instructions (Use, Create, Run) | WARNING |
| RD-009 | Conditions explicites (IF, WHEN, UNLESS) | ERREUR |
| RD-010 | Pas de double négation | WARNING |
| RD-011 | Flags documentés format `--flag-name` | ERREUR |
| RD-012 | Pas de chemins hardcodés absolus | ERREUR |
| RD-013 | Variables placeholders en format `{variable}` ou `$variable` | WARNING |
| RD-014 | Cohérence terminologie | ERREUR |
| RD-015 | Pas de TODO/FIXME/XXX dans contenu final | ERREUR |
| RD-016 | Pas de commentaires personnels | ERREUR |
| RD-017 | Emojis limités aux breakpoints et headers | WARNING |
| RD-018 | Références `@` pointent vers fichiers existants | BLOQUANT |
| RD-019 | Contexte dynamique `!` < 30 lignes | WARNING |
| RD-020 | Instructions < 100 lignes | WARNING |
| RD-021 | Frontmatter < 15 lignes | WARNING |
| RD-022 | Spécificité: une commande = une tâche | ERREUR |
| RD-023 | Déterminisme: mêmes inputs → mêmes outputs | WARNING |
| RD-024 | Testabilité: vérifiable par l'utilisateur | WARNING |
| RD-025 | Maintenabilité: simple à modifier | WARNING |

→ Details: [content-rules.md](content-rules.md)

### CAT-WF: Workflow (10 rules)

| ID | Règle | Sévérité |
|----|-------|----------|
| WF-001 | Workflow cohérent (pas d'étapes orphelines) | BLOQUANT |
| WF-002 | Séquence logique des étapes | ERREUR |
| WF-003 | Pas de boucles infinies dans les conditions | BLOQUANT |
| WF-004 | Points de sortie explicites | ERREUR |
| WF-005 | Conditions IF/ELSE complètes (pas de cas manquants) | ERREUR |
| WF-006 | Étapes critiques marquées MANDATORY | ERREUR |
| WF-007 | Breakpoints aux points de décision utilisateur | WARNING |
| WF-008 | Fallbacks documentés pour erreurs | WARNING |
| WF-009 | Workflow représentable en DAG (pas de cycles) | ERREUR |
| WF-010 | Routing documenté vers autres commandes | WARNING |

→ Details: [content-rules.md](content-rules.md#workflow-rules)

### CAT-IN: Integration (15 rules)

| ID | Règle | Sévérité |
|----|-------|----------|
| IN-001 | Skills chargés documentés avec condition | ERREUR |
| IN-002 | Subagents invoqués avec condition et rôle | ERREUR |
| IN-003 | Hooks documentés (pre-, post-, on-) | WARNING |
| IN-004 | MCP servers activés documentés | WARNING |
| IN-005 | Personas suggérés documentés | WARNING |
| IN-006 | Thinking level recommandé | WARNING |
| IN-007 | Workflow routing documenté (if/then) | ERREUR |
| IN-008 | Breakpoints MANDATORY marqués | ERREUR |
| IN-009 | Output paths documentés | ERREUR |
| IN-010 | Error handling explicite | WARNING |
| IN-011 | Fallbacks documentés | WARNING |
| IN-012 | Context file schema documenté | ERREUR |
| IN-013 | Session persistence expliquée | WARNING |
| IN-014 | Memory hooks documentés (post-phase-3) | ERREUR |
| IN-015 | Intégration avec validate_command.py | INFO |

→ Details: [integration-rules.md](integration-rules.md)

### CAT-DG: Detection & Generation (10 rules)

| ID | Règle | Sévérité |
|----|-------|----------|
| DG-001 | Détecter besoin de skill si > 500 tokens de logique | SUGGESTION |
| DG-002 | Détecter besoin de subagent si délégation explicite | SUGGESTION |
| DG-003 | Détecter besoin de référence si section > 100 lignes | SUGGESTION |
| DG-004 | Détecter pattern répété (copier-coller) | ERREUR |
| DG-005 | Détecter template candidat | SUGGESTION |
| DG-006 | Détecter hook candidat | SUGGESTION |
| DG-007 | Détecter script candidat (logique déterministe) | SUGGESTION |
| DG-008 | Suggérer décomposition si > 300 lignes | SUGGESTION |
| DG-009 | Suggérer references/ si contenu dense | SUGGESTION |
| DG-010 | Détecter overlap avec commandes existantes | ERREUR |

→ Details: [generation-detection.md](generation-detection.md)

---

## Scoring Algorithm

```python
def calculate_score(violations: list[dict]) -> int:
    """
    Calculate audit score from 0-100.

    Args:
        violations: List of {rule_id, severity, details}

    Returns:
        Integer score (0-100)
    """
    score = 100

    for v in violations:
        if v['severity'] == 'BLOQUANT':
            score -= 10
        elif v['severity'] == 'ERREUR':
            score -= 3
        elif v['severity'] == 'WARNING':
            score -= 1
        # SUGGESTION: no impact

    return max(0, score)

def determine_verdict(score: int, has_blocking: bool) -> str:
    """
    Determine audit verdict.

    Returns: PASS | WARN | FAIL | BLOCKED
    """
    if has_blocking:
        return "BLOCKED"
    elif score >= 90:
        return "PASS"
    elif score >= 70:
        return "WARN"
    else:
        return "FAIL"
```

---

## Report Format {#report-format}

```markdown
# Audit Report — {command_name}.md

> **Date**: {YYYY-MM-DD HH:mm}
> **Auditor**: command-auditor v1.0.0
> **Mode**: {STRICT|LENIENT}

---

## Executive Summary

| Metric | Value |
|--------|-------|
| Score | {XX}/100 |
| Rules Checked | 95 |
| Blocking Errors | {N} |
| Errors | {N} |
| Warnings | {N} |
| Suggestions | {N} |
| **Verdict** | **{PASS|WARN|FAIL|BLOCKED}** |

---

## Detected Workflow

\`\`\`mermaid
flowchart TD
    A[Start] --> B{Step 1}
    B --> C[Step 2]
    ...
\`\`\`

---

## Results by Category

### Frontmatter (CAT-FM)

| Status | ID | Rule | Detail |
|--------|-----|------|--------|
| ✅ | FM-001 | Frontmatter present | OK |
| ❌ | FM-004 | Description verb | "This command..." → "Auditer..." |

[Repeat for each category]

---

## Blocking Errors (MUST FIX)

1. **{RULE_ID}**: {description}
   - Line: {N}
   - Fix: {suggested_correction}

---

## Generation Suggestions

| Type | Reason | Suggested Action |
|------|--------|------------------|
| Skill | Section > 500 tokens | Extract to `my-skill/SKILL.md` |
| Subagent | Delegation detected | Create `@validator` |

---

## Action Items

- [ ] Fix {N} blocking errors
- [ ] Fix {N} errors
- [ ] Consider {N} suggestions

---

## Legend

| Symbol | Meaning |
|--------|---------|
| ❌ | Error (blocking or not) |
| ⚠️ | Warning |
| 💡 | Suggestion |
| ✅ | Compliant |
```

---

## Sources

| Source | Role | Priority |
|--------|------|----------|
| Anthropic Official Study 2025-01-14 | Primary reference | HIGH |
| EPCI Commands (14 files) | Context only | MEDIUM |
| SuperClaude Framework | Patterns | LOW |
| Superpowers | Patterns | LOW |

---

*Rules Catalog v1.0.0 — Command Auditor*
