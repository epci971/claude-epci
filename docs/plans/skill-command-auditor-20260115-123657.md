---
saved_at: "2026-01-15T12:36:57Z"
source: "~/.claude/plans/mighty-honking-sunrise.md"
slug: "skill-command-auditor"
original_filename: "mighty-honking-sunrise.md"
auto_detected: true
---

# Plan d'Implémentation — Skill `command-auditor`

> **Feature** : Audit automatique des commandes EPCI
> **Complexité** : STANDARD (4-6 fichiers, ~800 LOC estimé)
> **Date** : 2025-01-15

---

## Objectif

Créer un skill capable d'auditer une commande EPCI pour vérifier sa conformité aux bonnes pratiques officielles, avec :
- Rapport d'audit Markdown structuré (✅/❌/💡)
- Diagramme Mermaid du workflow détecté
- Détection des besoins de génération (skills, subagents, références)
- Mode STRICT : non-conformité = erreur bloquante

---

## Sources de règles

| Source | Statut | Rôle |
|--------|--------|------|
| Étude officielle 2025-01-14 | **Référence principale** | Bonnes pratiques officielles Anthropic |
| SuperClaude Framework | Patterns inspirants | Structure frontmatter, boundaries |
| Superpowers | Patterns inspirants | Invocation skills, minimalisme |
| WD Framework | Patterns inspirants | Tiers de complexité, personas |
| Commandes EPCI existantes | **Contexte seulement** | Pas forcément gold standard |

---

## Structure du skill

```
src/skills/core/command-auditor/
├── SKILL.md                              # Entry point (< 2000 tokens)
└── references/
    ├── rules-catalog.md                  # 70+ règles catégorisées
    ├── frontmatter-rules.md              # Règles FM-001 à FM-015
    ├── structure-rules.md                # Règles ST-001 à ST-020
    ├── redaction-rules.md                # Règles RD-001 à RD-025
    ├── workflow-rules.md                 # Règles WF-001 à WF-010 (NOUVEAU)
    ├── integration-rules.md              # Règles IN-001 à IN-015
    ├── generation-detection.md           # Règles DG-001 à DG-010
    ├── gold-standard-examples.md         # 3-5 exemples annotés
    └── mermaid-generator.md              # Template génération diagramme
```

---

## Catalogue des règles (7 catégories)

### CAT-FM : Frontmatter (15 règles)

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

### CAT-ST : Structure (20 règles)

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

### CAT-RD : Rédaction (25 règles)

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

### CAT-WF : Workflow (10 règles) — NOUVEAU

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

### CAT-IN : Intégration (15 règles)

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

### CAT-DG : Détection Génération (10 règles)

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

---

## Format du rapport d'audit

```markdown
# Audit Report — {command_name}.md

> **Date**: {YYYY-MM-DD HH:mm}
> **Auditor**: command-auditor v1.0.0
> **Mode**: STRICT

---

## Résumé Exécutif

| Métrique | Valeur |
|----------|--------|
| Score Global | {XX}/100 |
| Règles Vérifiées | {NN} |
| Erreurs Bloquantes | {N} |
| Erreurs | {N} |
| Warnings | {N} |
| Suggestions | {N} |
| **Statut** | **{PASS|FAIL|BLOCKED}** |

---

## Workflow Détecté (Mermaid)

\`\`\`mermaid
flowchart TD
    A[Start] --> B{Condition 1}
    B -->|Yes| C[Action 1]
    B -->|No| D[Action 2]
    C --> E[End]
    D --> E
\`\`\`

---

## Résultats par Catégorie

### Frontmatter (CAT-FM)
| Status | ID | Règle | Détail |
|--------|-----|-------|--------|
| ❌ | FM-004 | Description verbe infinitif | "This command..." → "Analyser..." |
| ✅ | FM-001 | Frontmatter présent | OK |

### Structure (CAT-ST)
...

### Rédaction (CAT-RD)
...

### Workflow (CAT-WF)
...

### Intégration (CAT-IN)
...

### Détection Génération (CAT-DG)
...

---

## Erreurs Bloquantes (MUST FIX)

1. **FM-010**: `Bash(*)` détecté — trop permissif
   - Ligne: 5
   - Correction: `Bash(git add:*), Bash(git commit:*)`

2. **WF-001**: Étape orpheline détectée
   - Ligne: 45-52
   - Correction: Relier Step 3 au flux principal

---

## Suggestions de Génération

| Type | Raison | Action suggérée |
|------|--------|-----------------|
| 📦 Skill | Section Process > 500 tokens | Extraire vers `my-skill/SKILL.md` |
| 👤 Subagent | Délégation "validator" détectée | Créer `@command-validator` |
| 📎 Référence | Section > 100 lignes | Extraire vers `references/details.md` |

---

## Action Items

- [ ] Corriger {N} erreurs bloquantes
- [ ] Corriger {N} erreurs
- [ ] Considérer {N} suggestions

---

## Légende

| Symbole | Signification |
|---------|---------------|
| ❌ | Erreur (bloquante ou non) |
| ⚠️ | Warning |
| 💡 | Suggestion |
| ✅ | Conforme |
```

---

## Fichiers critiques à lire/modifier

| Fichier | Rôle |
|---------|------|
| `src/scripts/validate_command.py` | Pattern de validation existant |
| `src/skills/factory/skills-creator/SKILL.md` | Modèle structure skill |
| `src/skills/factory/skills-creator/references/validation-checklist.md` | Checklist existante |
| `docs/guidelines/ETUDE_2025-01-14_slash-commands-claude-code.md` | Source officielle des règles |
| `src/commands/*.md` (14 fichiers) | Contexte commandes existantes |

---

## Plan d'exécution

### Phase 1 : Structure skill (SKILL.md + dossier)

1. Créer `src/skills/core/command-auditor/`
2. Rédiger `SKILL.md` avec :
   - Overview (but, invocation)
   - Process (workflow d'audit)
   - Output (format rapport)
   - Configuration (flags)

### Phase 2 : Fichiers de références

3. `references/rules-catalog.md` — Vue d'ensemble 95 règles
4. `references/frontmatter-rules.md` — Détails FM-001 à FM-015
5. `references/structure-rules.md` — Détails ST-001 à ST-020
6. `references/redaction-rules.md` — Détails RD-001 à RD-025
7. `references/workflow-rules.md` — Détails WF-001 à WF-010
8. `references/integration-rules.md` — Détails IN-001 à IN-015
9. `references/generation-detection.md` — Détails DG-001 à DG-010
10. `references/gold-standard-examples.md` — 3-5 exemples annotés
11. `references/mermaid-generator.md` — Template génération diagramme

### Phase 3 : Validation

12. Tester sur 3-4 commandes EPCI existantes
13. Ajuster règles si faux positifs
14. Documenter edge cases

---

## Vérification

Pour tester le skill :

```bash
# Invocation manuelle
/audit-command @src/commands/brief.md

# Vérification output
# → Rapport Markdown généré
# → Diagramme Mermaid inclus
# → Statut PASS/FAIL/BLOCKED clair
```

---

## Flags supportés

| Flag | Effet |
|------|-------|
| `--strict` | Mode strict (défaut) — bloquant |
| `--lenient` | Mode souple — suggestions uniquement |
| `--json` | Output JSON (CI/CD) |
| `--no-mermaid` | Désactiver génération diagramme |

> **Note** : Pas de mode auto-fix. Le rapport est consultatif, l'utilisateur corrige manuellement.

---

## Estimation

| Métrique | Valeur |
|----------|--------|
| Fichiers à créer | 11 |
| LOC estimé | ~800 |
| Règles totales | 95 |
| Durée estimée | 2-3h |
