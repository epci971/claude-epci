# Reference Projects Library

> Collection de projets de reference pour comparaison et inspiration EPCI.
> Utilise automatiquement par Phase 10 de l'audit (Suggestions d'Evolution).

---

## Purpose

Ces projets servent de reference pour:

1. **Audit Phase 10** — Comparaison automatique des patterns avec EPCI
2. **Evolution** — Identification de nouvelles fonctionnalites a integrer
3. **Benchmark** — Evaluation des pratiques EPCI vs industrie

---

## Projects Index

| Projet | Version | Focus Principal | Date Ajout |
|--------|---------|-----------------|------------|
| [wd-framework-master](#wd-framework) | 2.2.0 | Token optimization, Wave orchestration | 2025-01 |
| [SuperClaude_Framework-master](#superclaude) | master | Modes, Business Panel, Agents | 2024-12 |
| [superpowers-main](#superpowers) | main | One-at-a-time questions, Personas | 2024-12 |
| [BMAD-METHOD-main](#bmad) | main | Methodology structure | 2025-01 |

---

## Project Details

### WD Framework

**Dossier:** `wd-framework-master/`

**Focus:** Token optimization, Wave orchestration, DAG execution

**Fichiers cles:**
- `.claude/WORKFLOWS.md` — Workflows principaux
- `commands/*.md` — Definitions de commandes
- Configuration Wave/DAG

**Patterns interessants pour EPCI:**
- Gestion tokens optimisee
- Orchestration parallele (Wave)
- Structure de commandes modulaires

---

### SuperClaude

**Dossier:** `SuperClaude_Framework-master/`

**Focus:** Modes de fonctionnement, Business Panel, Systeme d'agents

**Fichiers cles:**
- `core/PRINCIPLES.md` — Principes fondamentaux
- `agents/*.md` — Definitions d'agents
- `modes/*.md` — Modes de fonctionnement

**Patterns interessants pour EPCI:**
- Business Panel pour tracking
- Modes contextuels
- Orchestration agents avancee

---

### Superpowers

**Dossier:** `superpowers-main/`

**Focus:** One-at-a-time questions, Personas adaptatifs

**Fichiers cles:**
- Documentation patterns
- Systeme de questions
- Personas

**Patterns interessants pour EPCI:**
- Questions une par une (UX)
- Personas dynamiques
- Validation incrementale

---

### BMAD Method

**Dossier:** `BMAD-METHOD-main/`

**Focus:** Structure methodologique, Architecture patterns

**Fichiers cles:**
- Architecture documentation
- Patterns de methodologie

**Patterns interessants pour EPCI:**
- Structure de methodologie
- Patterns architecturaux
- Documentation

---

## Usage in Audit Phase 10

L'audit Phase 10 utilise automatiquement ces projets:

```bash
# Recherche automatique de patterns
grep -r "{{COMMAND}}|workflow|phase|breakpoint" docs/librairies/[project]/
```

**Resultats formattes dans le rapport:**

| Projet | Feature | Delta vs EPCI | Suggestion |
|--------|---------|---------------|------------|
| [nom] | [feature trouvee] | [difference] | [action] |

---

## Patterns Comparison Matrix

| Pattern | WD | SuperClaude | Superpowers | BMAD |
|---------|:--:|:-----------:|:-----------:|:----:|
| Command structure | X | X | - | X |
| Agent orchestration | X | X | - | - |
| Wave/DAG execution | X | - | - | - |
| Token optimization | X | X | X | - |
| One-at-a-time UX | - | X | X | - |
| Business Panel | - | X | - | - |
| Personas dynamiques | - | - | X | - |
| Breakpoint system | X | X | - | - |
| MCP integration | - | - | - | - |
| Hook system | X | - | - | - |

---

## Adding New Projects

### Prerequisites

1. Le projet doit etre pertinent pour EPCI (Claude Code, AI assistant, workflow)
2. Documentation claire et lisible
3. Patterns extractibles et actionnables

### Procedure

1. **Clone/download** le projet dans `docs/librairies/[project-name]/`

2. **Update this README** — Ajouter une entree dans la table et une section details

3. **Update scoring-matrix.yaml** — Ajouter le projet dans:
   ```yaml
   evolution_scoring.sources.reference_projects.projects:
     - name: "[project-name]"
       focus: "[focus principal]"
   ```

4. **Identifier les fichiers cles** — Documenter les fichiers a scanner

### Structure Recommandee

```
docs/librairies/[project-name]/
├── README.md (ou docs/)     # Documentation principale
├── commands/                 # Definitions commandes
├── agents/                   # Definitions agents
├── core/                     # Principes/patterns
└── ...
```

---

## Maintenance

### Frequence

- **Mise a jour trimestrielle** des projets existants
- **Ajout immediat** si nouveau projet pertinent identifie

### Checklist de Maintenance

- [ ] Verifier si nouvelles versions disponibles
- [ ] Mettre a jour la matrice de comparaison
- [ ] Supprimer projets obsoletes
- [ ] Documenter nouveaux patterns identifies

### Derniere mise a jour

**Date:** 2025-01-08
**Par:** EPCI Team
