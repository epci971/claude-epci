# Plan d'Action — Externalisation brainstorm.md

> **Objectif** : Réduire brainstorm.md de 949 → ~350-400 lignes
> **Complexité** : STANDARD
> **Estimation** : 2-3h

---

## 1. État Actuel

### Fichier source
- **Fichier** : `src/commands/brainstorm.md`
- **Taille** : 949 lignes
- **Limite recommandée** : < 500 lignes (~5000 tokens)

### References existantes (5 fichiers, 1029 lignes)
```
src/skills/core/brainstormer/references/
├── brief-format.md      # Format de sortie du brief
├── ems-system.md        # Scoring EMS v2
├── frameworks.md        # 5 frameworks d'analyse
├── personas.md          # 3 personas
├── session-format.md    # Format YAML session (v4.2)
└── techniques/          # 4 fichiers (v4.2)
```

---

## 2. Sections à Externaliser

| # | Section | Lignes actuelles | Destination | Priorité |
|---|---------|------------------|-------------|----------|
| 1 | Question Format | 140-228 (~88) | `references/question-format.md` | P1 |
| 2 | Spike | 229-322 (~93) | `references/spike-guide.md` | P1 |
| 3 | Energy Checkpoints | 394-444 (~50) | `references/energy-checkpoints.md` | P1 |
| 4 | Session Commands | 445-492 (~47) | `references/session-commands.md` | P1 |
| 5 | @planner section | 493-563 (~70) | `references/agents-integration.md` | P2 |
| 6 | @security-auditor | 564-652 (~88) | (même fichier) | P2 |
| 7 | Section Validation | 653-763 (~110) | Fusionner dans `brief-format.md` | P2 |
| 8 | Flags (modes) | 799-928 (~129) | `references/modes.md` | P1 |

**Gain estimé** : ~550-600 lignes

---

## 3. Tâches Détaillées

### Phase A — Créer les fichiers references (P1)

#### Task A1 : `references/question-format.md`
**Contenu à extraire** (lignes 140-228) :
- Règles 3-5 questions
- Format Breakpoint v4.2
- Exemple avec suggestions A/B/C
- Quand utiliser une seule question

**Remplacement dans brainstorm.md** :
```markdown
## Question Format
→ Voir [question-format.md](../skills/core/brainstormer/references/question-format.md)
```

#### Task A2 : `references/spike-guide.md`
**Contenu à extraire** (lignes 229-322) :
- Quand utiliser spike
- Commande et exemples
- Process Spike (Framing, Exploration, Verdict)
- Format de sortie

**Remplacement** :
```markdown
## Spike
Exploration technique time-boxed intégrée au brainstorm.
→ Voir [spike-guide.md](../skills/core/brainstormer/references/spike-guide.md)

**Commande rapide** : `spike [duration] [question]`
```

#### Task A3 : `references/energy-checkpoints.md`
**Contenu à extraire** (lignes 394-444) :
- Triggers (4 conditions)
- Format Energy Check
- Actions par choix
- Commande `energy`

**Remplacement** :
```markdown
## Energy Checkpoints
Points de contrôle pour gérer la fatigue cognitive.
→ Voir [energy-checkpoints.md](../skills/core/brainstormer/references/energy-checkpoints.md)

**Triggers** : EMS 50, EMS 75, Iter ≥7, Phase change
```

#### Task A4 : `references/session-commands.md`
**Contenu à extraire** (lignes 445-492) :
- Commande `save`
- Commande `back`
- Auto-save behavior

**Remplacement** :
```markdown
## Session Commands
→ Voir [session-commands.md](../skills/core/brainstormer/references/session-commands.md)

| Commande | Action |
|----------|--------|
| `save` | Sauvegarder session |
| `back` | Revenir à l'itération précédente |
```

#### Task A5 : `references/modes.md`
**Contenu à extraire** (lignes 799-928) :
- --turbo Mode (existant)
- --random Mode (nouveau v4.2)
- --progressive Mode (nouveau v4.2)

**Remplacement** :
```markdown
## Flags

| Flag | Effet |
|------|-------|
| `--template [name]` | Forcer template |
| `--quick` | Mode rapide (3 iter max) |
| `--turbo` | Mode turbo (@clarifier) |
| `--random` | Sélection aléatoire pondérée |
| `--progressive` | 3 phases structurées |
| `--no-hmw` | Désactiver HMW |
| `--no-security` | Désactiver @security-auditor |
| `--no-plan` | Désactiver @planner |

→ Détails des modes : [modes.md](../skills/core/brainstormer/references/modes.md)
```

---

### Phase B — Consolider agents et validation (P2)

#### Task B1 : `references/agents-integration.md`
**Contenu à extraire** (lignes 493-652) :
- @planner — Quand invoquer, confirmation [Y/n], process
- @security-auditor — Détection auto, confirmation, process

**Remplacement** :
```markdown
## Agents Auto-invoqués

### @planner
- **Trigger** : `converge` ou EMS ≥70
- **Confirmation** : [Y/n] avant invocation auto
- **Output** : Plan préliminaire avec estimation

### @security-auditor
- **Trigger** : Patterns auth/security/payment détectés
- **Confirmation** : [Y/n] avant invocation auto
- **Output** : Security considerations report

→ Détails : [agents-integration.md](../skills/core/brainstormer/references/agents-integration.md)
```

#### Task B2 : Fusionner Section Validation dans `brief-format.md`
**Contenu à déplacer** (lignes 653-763) :
- Section-by-Section Validation
- Format validation section
- Quand skipper

Le fichier `brief-format.md` existe déjà — ajouter une section "Generation Process".

---

### Phase C — Nettoyage final

#### Task C1 : Supprimer mentions redondantes "(v4.2)"
- Garder uniquement dans Overview : `**Version**: 4.2`
- Supprimer les ~20 occurrences de "(v4.2)" dans les titres

#### Task C2 : Simplifier la table des commandes
- La table complète des commandes (lignes 203-228) peut être réduite
- Garder les essentielles, référencer le reste

#### Task C3 : Vérifier cohérence SKILL.md
- S'assurer que SKILL.md référence les nouveaux fichiers
- Mettre à jour la liste des "Reference Documents"

---

## 4. Structure Finale Cible

### brainstorm.md (~350-400 lignes)
```markdown
---
frontmatter (10 lignes)
---

# /brainstorm — Feature Discovery v4.2

## Overview (~15 lignes)
## Usage (~5 lignes)
## Exemples (~10 lignes)
## Configuration (~15 lignes)

## Process (~80 lignes)
### Phase 0 — Session Detection
### Phase 1 — Initialisation
### Phase 2 — Iterations
### Phase 3 — Generation

## Question Format (~10 lignes + référence)
## Spike (~10 lignes + référence)
## Energy Checkpoints (~10 lignes + référence)
## Session Commands (~15 lignes + référence)
## Agents (~20 lignes + référence)
## Flags (~30 lignes + référence modes)
## Output (~10 lignes)
## Skills Chargés (~5 lignes)
```

### Nouveaux fichiers references/
```
references/
├── question-format.md     # ~90 lignes
├── spike-guide.md         # ~95 lignes
├── energy-checkpoints.md  # ~55 lignes
├── session-commands.md    # ~50 lignes
├── modes.md               # ~140 lignes (turbo+random+progressive)
└── agents-integration.md  # ~160 lignes (planner+security)
```

---

## 5. Ordre d'Exécution

```
Phase A (P1) — ~1h30
├── A1: question-format.md
├── A2: spike-guide.md
├── A3: energy-checkpoints.md
├── A4: session-commands.md
└── A5: modes.md

Phase B (P2) — ~45min
├── B1: agents-integration.md
└── B2: Fusionner dans brief-format.md

Phase C (Cleanup) — ~30min
├── C1: Supprimer "(v4.2)"
├── C2: Simplifier table commandes
└── C3: Vérifier SKILL.md
```

---

## 6. Validation

### Critères de succès
- [ ] brainstorm.md < 450 lignes
- [ ] Tous les liens references/ fonctionnent
- [ ] SKILL.md référence les nouveaux fichiers
- [ ] Pas de duplication de contenu
- [ ] `python src/scripts/validate_command.py src/commands/brainstorm.md` passe

### Tests manuels
- [ ] `/brainstorm` fonctionne normalement
- [ ] Les modes --random et --progressive sont documentés
- [ ] Les références sont accessibles

---

## 7. Risques

| Risque | Impact | Mitigation |
|--------|--------|------------|
| Liens cassés | Medium | Tester chaque référence après création |
| Perte de contenu | High | Git diff avant/après pour vérifier |
| Incohérence docs | Medium | Relecture SKILL.md + brainstorm.md |

---

*Plan généré le 2026-01-06 — Projet brainstorm-v4.2 externalisation*
