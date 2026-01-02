# Journal de Brainstorm — EPCI Rules Generator

> **Feature**: epci-rules
> **Date**: 2026-01-02
> **Durée**: ~30 minutes
> **EMS Final**: 92/100

---

## Historique des itérations

### Iteration 0 — Initialisation

**Phase**: 🔀 Divergent | **Persona**: 📐 Architecte | **EMS**: 45/100

**Context chargé**:
- Briefs existants analysés (epci-rules-command.md, rules-generator-guide.md)
- Codebase EPCI scanné via @Explore (10 commands, 24 skills, 9 agents)
- Factory patterns identifiés (templates, references, validation)
- Stack detection existante (project-memory/detector.py)

**HMW générées**:
1. Comment générer des rules contextualisées qui s'adaptent à chaque projet sans duplication avec les linters existants?
2. Comment intégrer la commande /rules dans le workflow EPCI existant?
3. Comment maintenir les rules à jour quand le code évolue (drift detection)?

**Questions posées**:
1. Intégration workflow (standalone vs auto-suggérée)
2. Scope de génération v1 (frameworks)
3. Synchronisation linters (priorité)
4. Validation des rules (agent vs script)
5. Gestion des rules existantes

---

### Iteration 1 — Cadrage

**Phase**: 🔀 Divergent | **Persona**: 📐 Architecte | **EMS**: 58/100 (+13)

**Décisions validées**:
- ✓ Intégration: Standalone + auto-suggérée par /brief
- ✓ Scope v1: Réutiliser skills stack (Symfony, React, Django, SpringBoot)
- ✓ Sync linters: Différé v1.1
- ✓ Validation: Script Python (validate_rules.py)
- ✓ Existantes: Confirmation avec preview

**Questions posées**:
1. Architecture composants (Command seule vs +Skill vs +Skill+Agent)
2. Stockage templates (nouveau skill vs extension skills stack)
3. Détection patterns (Niveau 1/2/3)
4. Format CLAUDE.md (<50 lignes?)
5. Hook d'intégration

---

### Iteration 2 — Architecture

**Phase**: 🎯 Convergent | **Persona**: 📐 Architecte | **EMS**: 72/100 (+14)

**Décisions validées**:
- ✓ Architecture: Option C — Command + Skill + Agent (validation poussée)
- ✓ Templates: Dans skills stack existants (éviter double maintenance)
- ✓ Détection: Niveau 3 (stack + architecture + conventions AST)
- ✓ CLAUDE.md: >50 lignes, focus fonctionnel/projet (technique dans rules)
- ✓ Hook: Oui pour traçabilité (post-rules-init)

**Analyse skills stack**:
- Lecture complète des 5 skills: php-symfony, python-django, javascript-react, java-springboot, frontend-editor
- Structure commune: SKILL.md + references/ + sections Quick Reference, Patterns, Anti-patterns

**Questions posées**:
1. Extension skills stack (structure rules-templates/)
2. Format CLAUDE.md enrichi (proposition)
3. Scope agent @rules-validator
4. Mapping skills → rules (marqueurs vs convention vs fichier externe)

---

### Iteration 3 — Convergence

**Phase**: 🎯 Convergent | **Persona**: 📐 Architecte | **EMS**: 85/100 (+13)

**Décisions validées**:
- ✓ Structure `rules-templates/` dans chaque skill stack
- ✓ Format CLAUDE.md enrichi (fonctionnel + architecture + stack + décisions)
- ✓ Agent @rules-validator: tous scopes (syntaxe, cohérence, complétude, qualité)
- ✓ Mapping via marqueurs inline (Option A)
- ✓ Cohérence CLAUDE.md ↔ rules maintenue par la commande

**Questions posées**:
1. Priorité actions (P1/P2/P3)
2. Comportement multi-stack
3. Niveau de détail des rules (sections à extraire)

---

### Iteration 4 — Finalisation

**Phase**: 🎯 Convergent | **Persona**: 📐 Architecte | **EMS**: 92/100 (+7)

**Décisions finales**:
- ✓ Architecture monorepo: `backend/` + `frontend/`
- ✓ Backend: Python/Django OU PHP/Symfony
- ✓ Frontend: React + Tailwind (frontend-editor obligatoire)
- ✓ Niveau détail: Maximum — toutes sections (Quick Reference, Common Patterns, Anti-patterns, Examples)
- ✓ Paths/regex: Attention particulière pour frontend-editor
- ✓ Priorités: P1 (init, validate), P2 (update), P3 (sync différé v1.1)

---

## Décisions clés

| Décision | Choix | Rationale |
|----------|-------|-----------|
| Architecture composants | Command + Skill + Agent | Validation poussée, séparation des responsabilités |
| Stockage templates | Dans skills stack existants | Évite double maintenance, source unique de vérité |
| Niveau détection | Niveau 3 (stack + archi + AST) | Précision maximale pour les conventions |
| Format CLAUDE.md | >50 lignes, fonctionnel | Séparation vision projet / conventions techniques |
| Mapping skills→rules | Marqueurs inline | Pas de fichier externe, maintenance facilitée |
| Priorité actions | init+validate P1 | Base fonctionnelle avant incréments |
| Sync linters | Différé v1.1 | Complexité élevée, focus sur le core d'abord |

---

## Questions résolues

1. **Où stocker les templates?** → Dans `skills/stack/*/rules-templates/`
2. **Comment mapper skills vers rules?** → Marqueurs `<!-- RULE:path:section -->`
3. **Quel niveau de détail?** → Maximum (toutes sections des skills)
4. **Comment valider?** → Agent @rules-validator (opus) + script Python
5. **Comment tracer?** → Hook post-rules-init vers .project-memory/
6. **Multi-stack?** → Génère rules pour chaque stack détectée
7. **CLAUDE.md vs rules?** → CLAUDE.md = fonctionnel, rules = technique

---

## Composants identifiés

### À créer

| Composant | Fichier | Priorité |
|-----------|---------|----------|
| Command | `src/commands/rules.md` | P1 |
| Skill | `src/skills/core/rules-generator/SKILL.md` | P1 |
| Agent | `src/agents/rules-validator.md` | P1 |
| Script | `src/scripts/validate_rules.py` | P1 |
| Hook | `src/hooks/active/post-rules-init.py` | P1 |
| Templates PHP | `src/skills/stack/php-symfony/rules-templates/*.md` | P1 |
| Templates Python | `src/skills/stack/python-django/rules-templates/*.md` | P1 |
| Templates React | `src/skills/stack/javascript-react/rules-templates/*.md` | P1 |
| Templates Java | `src/skills/stack/java-springboot/rules-templates/*.md` | P2 |
| Templates Tailwind | `src/skills/stack/frontend-editor/rules-templates/*.md` | P1 |

### À modifier

| Fichier | Modification |
|---------|--------------|
| `src/commands/brief.md` | Ajouter auto-suggestion si .claude/ absent |
| `CLAUDE.md` (projet) | Documenter la nouvelle commande |
| `src/skills/stack/*/SKILL.md` | Ajouter marqueurs RULE inline |

---

## Risques identifiés

| Risque | Probabilité | Impact | Mitigation |
|--------|-------------|--------|------------|
| Marqueurs inline complexes à parser | Moyenne | Moyen | Regex robuste, tests unitaires |
| Drift detection faux positifs | Moyenne | Faible | Seuils configurables, mode --strict |
| Templates trop génériques | Faible | Moyen | Itérer sur des projets réels |
| Paths regex incorrects | Moyenne | Élevé | Tests d'intégration avec vrais projets |

---

## Métriques EMS détaillées (final)

| Axe | Score | Justification |
|-----|-------|---------------|
| **Clarté** | 95/100 | Objectifs et scope très bien définis |
| **Profondeur** | 90/100 | Architecture détaillée, formats spécifiés |
| **Couverture** | 92/100 | Tous les aspects couverts, multi-stack inclus |
| **Décisions** | 95/100 | Toutes les décisions prises et justifiées |
| **Actionnabilité** | 88/100 | Prêt pour implémentation, quelques détails à affiner en Phase 1 |

**Score composite**: 92/100

---

## Prochaine étape

Lancer `/epci:brief` avec le contenu du brief généré pour:
1. Affiner les fichiers impactés exactement
2. Estimer la complexité précise
3. Démarrer le workflow EPCI complet

---

*Journal généré automatiquement par /brainstorm*
