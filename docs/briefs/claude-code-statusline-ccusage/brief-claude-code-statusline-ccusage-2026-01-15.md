# PRD — Configuration Statusline Claude Code avec ccusage

| Metadata | Value |
|----------|-------|
| **Document ID** | PRD-2026-001 |
| **Version** | 1.0 |
| **Status** | Draft |
| **Owner** | EPCI User |
| **Created** | 2026-01-15 |
| **Last Updated** | 2026-01-15 |
| **Slug** | claude-code-statusline-ccusage |
| **EMS Score** | 87/100 |
| **Template** | feature |

### Change History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-01-15 | EPCI Brainstormer | Initial generation from /brainstorm |

---

## Executive Summary

**TL;DR** : Configurer une statusline Claude Code globale avec ccusage pour afficher en temps réel le modèle, la branche Git, l'utilisation du contexte avec progressbar, les coûts de session/jour/block 5h, et le nom du projet.

| Aspect | Description |
|--------|-------------|
| **Problem** | Aucune visibilité temps réel sur l'utilisation du contexte et les coûts de session Claude Code |
| **Solution** | Intégration ccusage statusline dans ~/.claude/settings.json avec toutes les métriques de coût |
| **Impact** | Éviter les auto-compact inattendus, maîtriser le budget, optimiser l'utilisation |
| **Target Launch** | Immédiat (configuration) |

---

## Background & Strategic Fit

### Why Now?

La statusline est une feature stable depuis décembre 2024 (v1.0.80+). L'utilisateur a réalisé une étude complète des options disponibles et souhaite maintenant passer à l'implémentation avec ccusage pour bénéficier du tracking avancé des coûts.

### Strategic Alignment

Cette feature s'aligne avec :
- [x] **OKR** : Productivité développeur — visibilité temps réel
- [x] **Vision Produit** : Configuration optimale de l'environnement Claude Code
- [x] **Position Marché** : Utilisation des outils communautaires éprouvés (ccusage)

---

## Problem Statement

### Current Situation

Actuellement, l'utilisateur n'a pas de visibilité temps réel sur :
- Le pourcentage d'utilisation de la fenêtre de contexte (risque d'auto-compact à 80%)
- Le coût de la session en cours
- Le coût cumulé de la journée
- Le statut du block 5h de facturation avec timer

### Problem Definition

Sans statusline configurée, l'utilisateur découvre tardivement que le contexte est saturé (déclenchement `/compact` automatique) ou que les coûts de session ont dépassé les attentes.

### Evidence & Data

- **Quantitative** : Auto-compact se déclenche à 80% du contexte — sans visibilité, impossible d'anticiper
- **Qualitative** : Frustration de perdre le contexte de conversation ; surprise sur les coûts en fin de session

### Impact of Not Solving

- **Business** : Coûts non maîtrisés, dépassements de budget
- **User** : Perte de contexte inattendue, productivité réduite
- **Technical** : Sessions interrompues, reprise coûteuse

---

## Goals

### Business Goals

- [x] Visibilité temps réel sur les coûts (session, jour, block 5h)
- [x] Anticipation des seuils de facturation

### User Goals

- [x] Voir le modèle actif en un coup d'œil
- [x] Identifier la branche Git sans commande supplémentaire
- [x] Anticiper l'auto-compact avec progressbar contexte
- [x] Contrôler le budget de la session

### Technical Goals

- [x] Configuration globale (~/.claude/settings.json) applicable à tous les projets
- [x] Utilisation de ccusage (outil éprouvé et maintenu)

---

## Non-Goals (Out of Scope v1)

**Explicitement NON inclus dans cette version** :

| Exclusion | Raison | Future Version |
|-----------|--------|----------------|
| Script Bash custom | ccusage couvre tous les besoins | Non prévu |
| Configuration par projet | Globale suffisante pour l'instant | v2 si besoin |
| Intégration ccstatusline TUI | Préférence pour ccusage pur | Non prévu |
| Themes/personnalisation avancée | Simplicité d'abord | v2 éventuel |

---

## Personas

### Persona Primaire — Développeur Claude Code

- **Role**: Développeur utilisant Claude Code quotidiennement
- **Contexte**: Multiples projets, sessions longues, besoin de suivi des coûts
- **Pain points**: Pas de visibilité sur le contexte, surprise sur les coûts, auto-compact inattendu
- **Objectifs**: Maîtriser l'utilisation et les coûts, anticiper les limites
- **Quote**: "Je veux voir d'un coup d'œil si je suis proche de la limite de contexte et combien me coûte cette session."

---

## Stack Détecté

- **Outil**: ccusage (npm/bun)
- **Configuration**: JSON (~/.claude/settings.json)
- **Prérequis**: bun ou npm installé
- **Dépendance**: jq non requis (ccusage gère le parsing)

---

## Exploration Summary

### Analyse Documentation

Le document `TECHNIQUE_2025-01-15_claude-code-statusline.md` fourni contient :
- Structure JSON d'entrée complète
- Script fonctionnel avec progressbar
- Options ccusage documentées
- Troubleshooting

### Configuration Cible

**Fichier** : `~/.claude/settings.json`

```json
{
  "statusLine": {
    "type": "command",
    "command": "bun x ccusage statusline",
    "padding": 0
  }
}
```

### Output Attendu

```
🤖 Opus | 💰 $0.23 session / $1.23 today / $0.45 block (2h 45m left) | 🔥 $0.12/hr | 🧠 25,000 (12%)
```

### Risques Identifiés

- **Low** : bun ou npm non installé — solution : installer préalablement
- **Low** : Première exécution lente (cache) — résolu après premier appel

---

## User Stories

### US1 — Configurer la statusline globalement

**En tant que** développeur Claude Code,
**Je veux** configurer ccusage statusline dans ~/.claude/settings.json,
**Afin de** voir les métriques en temps réel dans tous mes projets.

**Acceptance Criteria:**
- [x] Given fichier ~/.claude/settings.json existe, When j'ajoute la config statusLine, Then la statusline s'affiche au prochain lancement Claude Code
- [x] Given fichier ~/.claude/settings.json n'existe pas, When je le crée avec la config, Then la statusline s'affiche
- [x] Given ccusage non installé, When Claude Code lance la statusline, Then bun x installe automatiquement et exécute

**Priorité**: Must-have
**Complexité**: S (1 fichier à modifier/créer)

### US2 — Voir les métriques de coût complètes

**En tant que** développeur Claude Code,
**Je veux** voir le coût session + today + block 5h avec timer,
**Afin de** maîtriser mon budget en temps réel.

**Acceptance Criteria:**
- [x] Given session en cours, When je regarde la statusline, Then je vois "$X.XX session / $Y.YY today / $Z.ZZ block (Xh XXm left)"
- [x] Given nouveau block 5h, When le timer reset, Then le coût block repart à $0.00

**Priorité**: Must-have
**Complexité**: S (inclus dans ccusage)

### US3 — Voir le contexte avec progressbar

**En tant que** développeur Claude Code,
**Je veux** voir le pourcentage de contexte utilisé avec indicateur visuel,
**Afin de** anticiper l'auto-compact avant qu'il ne se déclenche.

**Acceptance Criteria:**
- [x] Given contexte < 50%, When je regarde la statusline, Then l'indicateur est vert
- [x] Given contexte 50-80%, When je regarde la statusline, Then l'indicateur est jaune
- [x] Given contexte > 80%, When je regarde la statusline, Then l'indicateur est rouge

**Priorité**: Must-have
**Complexité**: S (inclus dans ccusage)

---

## Règles Métier

- **RM1**: La statusline doit s'afficher globalement pour tous les projets
- **RM2**: ccusage utilise le mode offline par défaut (pas de latence réseau)
- **RM3**: Le format de sortie est une ligne unique compatible terminal ANSI

---

## Cas Limites & Edge Cases

| Cas | Comportement attendu |
|-----|---------------------|
| bun non installé | Utiliser npx -y ccusage statusline (npm) |
| Fichier settings.json corrompu | Claude Code affiche erreur, pas de statusline |
| Réseau indisponible | Mode offline par défaut, fonctionnement normal |
| Premier lancement (pas de cache) | Léger délai initial, puis normal |

---

## Success Metrics

| Métrique | Baseline | Cible | Méthode de mesure |
|----------|----------|-------|-------------------|
| Visibilité contexte | 0% | 100% | Statusline visible |
| Anticipation auto-compact | Non | Oui | Indicateur couleur <80% |
| Suivi coûts | Manuel | Temps réel | Affichage session/today/block |

---

## User Flow

### Current Experience (As-Is)

```
[Lancement Claude Code]
       |
       v
  [Pas de statusline] --> [Aucune visibilité]
                                  |
                         [Travail à l'aveugle]
                                  |
                                  v
                         [Surprise: auto-compact à 80%]
                         [Surprise: coût élevé en fin de session]
```

### Proposed Experience (To-Be)

```
[Lancement Claude Code]
       |
       v
  [Statusline ccusage affichée]
       |
       v
  [Modèle | Coûts | Contexte % visible]
       |
       +--> [Contexte approche 80%?]
       |         |
       |    [Oui] --> [/compact proactif]
       |         |
       |    [Non] --> [Continue normalement]
       |
       +--> [Coût block élevé?]
                 |
            [Oui] --> [Pause ou optimisation]
```

### Key Improvements

| Pain Point Actuel | Solution Proposée | Impact |
|-------------------|-------------------|--------|
| Pas de visibilité contexte | Progressbar + % | Anticipation auto-compact |
| Pas de suivi coûts | Session/Today/Block affiché | Maîtrise budget |
| Pas d'info modèle | Nom modèle affiché | Confirmation rapide |

---

## Contraintes Techniques Identifiées

| Contrainte | Impact | Mitigation |
|------------|--------|------------|
| bun ou npm requis | Installation préalable | Documenter prérequis |
| Terminal ANSI requis | Couleurs non visibles sur terminal basique | Plupart des terminaux modernes OK |

---

## Dépendances

- **Externes**: ccusage (npm package), bun ou npm

---

## Assumptions

Hypothèses considérées vraies pour le succès de cette feature :

- [x] **Technical** : bun ou npm disponible sur le système
- [x] **Technical** : Terminal compatible ANSI pour les couleurs
- [x] **User** : Utilisateur a les droits d'écriture sur ~/.claude/

---

## Critères d'Acceptation Globaux

- [x] Configuration ajoutée dans ~/.claude/settings.json
- [x] Statusline visible au lancement de Claude Code
- [x] Métriques affichées : modèle, coûts (session/today/block), contexte %, projet
- [x] Fonctionne sur tous les projets (configuration globale)

---

## Questions Ouvertes

> Aucune question ouverte — brief complet pour implémentation.

---

## FAQ

### Internal FAQ (Équipe)

**Q: Pourquoi ccusage plutôt qu'un script Bash custom ?**
A: ccusage offre toutes les métriques souhaitées (session/today/block) avec maintenance communautaire, sans développement custom.

**Q: Pourquoi bun plutôt que npm ?**
A: bun est plus rapide. npm fonctionne aussi avec `npx -y ccusage statusline`.

**Q: Peut-on personnaliser le format de sortie ?**
A: Oui, ccusage offre des flags comme `--visual-burn-rate emoji`, `--cost-source both`, etc.

### External FAQ (Utilisateurs)

**Q: La statusline ralentit-elle Claude Code ?**
A: Non, ccusage utilise le mode offline par défaut pour des réponses instantanées.

**Q: Puis-je avoir une config différente par projet ?**
A: Oui, en créant un .claude/settings.local.json dans le projet qui override la config globale.

---

## Estimation Préliminaire

| Métrique | Valeur |
|----------|--------|
| Complexité estimée | TINY |
| Fichiers impactés | 1 (settings.json) |
| Risque global | Low |

---

## Timeline & Milestones

### Target Launch

**Objectif** : Immédiat — configuration simple

### Key Milestones

| Milestone | Target Date | Owner | Status |
|-----------|-------------|-------|--------|
| PRD Review Complete | 2026-01-15 | User | ✅ Done |
| Configuration settings.json | 2026-01-15 | Claude Code | ⚪ Not Started |
| Validation statusline visible | 2026-01-15 | User | ⚪ Not Started |

### Phasing Strategy

**Phase 1 (MVP)** : Configuration ccusage statusline globale avec métriques complètes
**Phase 2** : Personnalisation flags si besoin (burn rate emoji, thresholds, etc.)

---

## Appendix

### Configuration ccusage — Options Disponibles

| Option | Description | Exemple |
|--------|-------------|---------|
| `--cost-source` | Source des coûts (auto/ccusage/cc/both) | `--cost-source both` |
| `--visual-burn-rate` | Indicateur burn rate (off/emoji/text/emoji-text) | `--visual-burn-rate emoji` |
| `--context-low-threshold` | Seuil vert contexte (défaut: 50) | `--context-low-threshold 60` |
| `--context-medium-threshold` | Seuil jaune contexte (défaut: 80) | `--context-medium-threshold 90` |
| `--no-offline` | Mode online (prix temps réel) | `--no-offline` |

### Sources

- [ccusage statusline guide](https://ccusage.com/guide/statusline)
- [Claude Code statusline docs](https://code.claude.com/docs/en/statusline)
- [ccstatusline GitHub](https://github.com/sirmalloc/ccstatusline)
- [cc-statusline GitHub](https://github.com/chongdashu/cc-statusline)

### Glossaire

| Terme | Définition |
|-------|------------|
| **context_window** | Fenêtre de contexte = mémoire de travail de Claude |
| **burn rate** | Taux de consommation tokens/heure ou $/heure |
| **block 5h** | Période de facturation de 5 heures pour Claude Code |
| **auto-compact** | Compression automatique du contexte à 80% de remplissage |

---

*PRD prêt pour EPCI — Lancer `/brief` avec ce contenu ou exécuter directement l'agent @statusline-setup.*
*Détails du processus de brainstorming dans le Journal d'Exploration.*
