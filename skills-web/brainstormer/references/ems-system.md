# EMS — Exploration Maturity Score

> Système de scoring pour mesurer la maturité de l'exploration

---

## Vue d'ensemble

L'EMS (Exploration Maturity Score) est un indicateur composite qui mesure la progression d'un brainstorming vers un résultat exploitable. Il est calculé à chaque fin d'itération et affiché sous forme de radar.

**Nouveautés v3.2** :
- Ancres objectives par axe (critères observables)
- Intégration avec les phases Divergent/Convergent
- Recommandations contextuelles selon la phase
- Scoring **directionnel** contre les ancres, sans addition de points (Lot P1)

---

## Les 5 Axes

| Axe | Poids | Question clé |
|-----|-------|--------------|
| **Clarté** | 25% | Le sujet est-il bien défini et compris ? |
| **Profondeur** | 25% | A-t-on creusé suffisamment ? |
| **Couverture** | 20% | A-t-on exploré tous les angles pertinents ? |
| **Décisions** | 20% | A-t-on progressé et tranché ? |
| **Actionnabilité** | 10% | Peut-on agir concrètement après ça ? |

### Formule de calcul

```
EMS = (Clarté × 0.25) + (Profondeur × 0.25) + (Couverture × 0.20) 
    + (Décisions × 0.20) + (Actionnabilité × 0.10)
```

---

## Ancres Objectives

Chaque axe dispose de **critères observables** qui définissent ses paliers (20/40/60/80/100).

> **Comment noter** : le modèle **évalue chaque axe globalement contre ces ancres**. Il choisit le palier dont la description correspond le mieux à l'état réel de l'exploration, puis ajuste finement entre deux paliers. **Ce n'est pas une addition de points** — les listes « Ce qui fait progresser cet axe » indiquent *ce qui fait monter l'axe*, pas un barème à cumuler.

### Clarté (25%)

| Score | Ancre Observable |
|-------|------------------|
| **20** | Sujet énoncé mais pas reformulé ni validé |
| **40** | Brief validé avec périmètre in/out défini |
| **60** | + Contraintes identifiées (≥2) + critères de succès définis |
| **80** | + Objectifs SMART + parties prenantes identifiées |
| **100** | Zéro question ouverte sur le "quoi" — définition cristalline |

**Ce qui fait progresser cet axe** :
- User valide la reformulation
- Contraintes explicites mentionnées
- Critères de succès définis
- Parties prenantes listées

### Profondeur (25%)

| Score | Ancre Observable |
|-------|------------------|
| **20** | Questions de surface uniquement (quoi, qui, quand) |
| **40** | Au moins une chaîne de "pourquoi" (2+ niveaux) |
| **60** | Framework appliqué OU deep dive complété |
| **80** | Insights non-évidents + connexions cross-domain |
| **100** | Cause racine identifiée + validée + implications tracées |

**Ce qui fait progresser cet axe** :
- Premier "pourquoi" creusé
- Deuxième niveau de "pourquoi"
- Framework appliqué (5 Whys, Fishbone...)
- Analogie pertinente d'un autre domaine
- Cause racine explicitement nommée

### Couverture (20%)

| Score | Ancre Observable |
|-------|------------------|
| **20** | Une seule perspective explorée |
| **40** | 2-3 angles différents explorés |
| **60** | Risques explicitement adressés OU alternatives comparées |
| **80** | Six Hats complet OU ≥3 alternatives avec critères OU multi-stakeholders |
| **100** | Aucun angle mort identifiable — exploration exhaustive |

**Ce qui fait progresser cet axe** :
- Nouvel angle exploré
- Section risques abordée
- Alternative comparée
- Perspective stakeholder ajoutée

### Décisions (20%)

| Score | Ancre Observable |
|-------|------------------|
| **20** | Tout reste ouvert, aucune orientation |
| **40** | 1-2 orientations prises mais réversibles |
| **60** | Décisions clés verrouillées avec rationale |
| **80** | Arbitrages faits + priorisation établie |
| **100** | Toutes les décisions du scope prises, fils fermés |

**Ce qui fait progresser cet axe** :
- Première orientation prise
- Décision explicite avec justification
- Priorisation établie (MoSCoW, scoring...)
- Thread fermé explicitement

### Actionnabilité (10%)

| Score | Ancre Observable |
|-------|------------------|
| **20** | Idées vagues, aucune action concrète |
| **40** | "Il faudrait..." mais sans qui/quand |
| **60** | Actions identifiées avec owner OU timeline |
| **80** | Actions + owner + timeline + dépendances |
| **100** | Plan d'action complet, prêt à exécuter |

**Ce qui fait progresser cet axe** :
- Première action concrète nommée
- Owner assigné
- Timeline définie
- Dépendances identifiées
- Quick win identifié

---

## Intégration avec les Phases

Les recommandations EMS s'adaptent à la phase actuelle.

### En Phase 🔀 Divergente

**Focus principal** : Couverture, Profondeur

**Recommandations typiques** :
```
💡 Recommandations (phase divergente) :
   → Couverture à 45% : Explorons d'autres angles (stakeholders ? risques ?)
   → Profondeur à 38% : Un deep dive enrichirait l'exploration
```

**Comportement** :
- Ne pas pousser les Décisions (normal qu'elles soient basses)
- Encourager l'exploration large
- Suggérer des frameworks d'exploration (Six Hats, Starbursting)

### En Phase 🎯 Convergente

**Focus principal** : Décisions, Actionnabilité

**Recommandations typiques** :
```
💡 Recommandations (phase convergente) :
   → Décisions à 52% : 3 points restent ouverts, tranchons
   → Actionnabilité à 40% : Définissons des actions concrètes avec owners
```

**Comportement** :
- Pousser vers les décisions
- Suggérer des frameworks de décision (MoSCoW, Weighted Criteria)
- Insister sur les actions concrètes

### Suggestion de Changement de Phase

Quand la Couverture atteint 60%+ et qu'on est en Divergent depuis 3+ itérations :

```
💡 **Suggestion de phase**

L'exploration semble mature (Couverture: 72%, Profondeur: 68%).
On pourrait passer en mode 🎯 Convergent pour commencer à trancher.

→ `converge` — Passer en mode décision
→ `continue` — Rester en exploration ouverte
```

---

## Affichage EMS

### Cadence d'affichage (NOUVEAU — Lot P1)

Pour alléger le mobilier par tour (progressive disclosure), le radar complet est
affiché **périodiquement** en mode Standard ; une ligne compacte est affichée le
reste du temps.

**Mode Standard — fin d'itération :**

- **Radar complet** (5 axes + deltas + recommandations) si **au moins une** de
  ces conditions est vraie :
  - `iteration == 1` (établir la baseline), **OU**
  - `iteration % 3 == 0` (it. 3, 6, 9, …), **OU**
  - **franchissement de seuil** : l'icône de statut change vs l'itération
    précédente (🌱 → 🌿 → 🌳 → 🎯), **OU**
  - commande **`status`** (force toujours le radar complet), **OU**
  - **`finish` / fin de session**.
- **Ligne compacte** à tous les autres tours.
- **Alerte stagnation** : toujours affichée si déclenchée, quel que soit le
  format (signal indépendant du radar).

**Quick Mode** : inchangé — toujours la ligne simplifiée (score global seul).

### Format Standard — radar complet (périodique)

```
📊 EMS: 68/100 (+12) ████████████████░░░░

   Clarté       ████████████████░░░░ 78/100 (+8)
   Profondeur   ██████████████░░░░░░ 65/100 (+15) ⬆️
   Couverture   ████████████████░░░░ 72/100 (+10)
   Décisions    ██████████░░░░░░░░░░ 52/100 (+5) ⚠️
   Actionnab.   ████████░░░░░░░░░░░░ 45/100 (+8)

🌿 Exploration en développement

💡 Recommandations :
   → Décisions faible : 3 points clés restent à trancher
   → Actionnabilité : Commençons à définir des actions concrètes
```

### Format Standard — ligne compacte (entre deux radars)

Affichée aux tours sans radar complet. Le flag d'axe faible reprend le seuil de
la légende ci-dessous (⚠️ < 50) ; si plusieurs axes sont < 50, n'afficher que le
plus bas.

```
📊 EMS: 58/100 (+6) 🌿  ⚠️ Décisions 45
```

Sans axe faible (tous ≥ 50) :

```
📊 EMS: 72/100 (+8) 🌳
```

### Format Quick Mode (simplifié)

```
📊 EMS: 68/100 (+12) 🌿
```

### Légende des indicateurs

| Indicateur | Signification |
|------------|---------------|
| ⬆️ | Progression notable (+10 ou plus) |
| ⚠️ | Axe faible (< 50) |
| ✅ | Axe fort (≥ 80) |
| 🔴 | Axe critique (< 30) |

---

## Seuils et Messages

| Plage EMS | Statut | Icône | Message |
|-----------|--------|-------|---------|
| 0-29 | Début | 🌱 | "Exploration débutante — continuons" |
| 30-59 | Développement | 🌿 | "Exploration en développement" |
| 60-89 | Mature | 🌳 | "Exploration mature — `finish` disponible" |
| 90-100 | Complète | 🎯 | "Exploration très complète — `finish` recommandé" |

### Messages contextuels

**Stagnation détectée** (< 5 pts sur 2 itérations) :
```
⚠️ **Stagnation détectée**

L'EMS n'a progressé que de [X] points sur les 2 dernières itérations.

Options :
→ `dive [sujet]` — Approfondir un point spécifique
→ `pivot` — Réorienter vers un sujet émergent
→ `finish` — Synthétiser l'acquis actuel
```

**Score minimum non atteint** (avec `--min-score`) :
```
⚠️ **Score minimum non atteint**

EMS actuel : 58/100 | Minimum requis : 70/100

Axes à améliorer :
• Décisions : 45/100 (besoin : +25)
• Actionnabilité : 38/100 (besoin : +20)

Options :
→ `continue` — Poursuivre l'exploration
→ `finish --force` — Générer le rapport malgré le score
```

---

## Initialisation

L'EMS démarre à **0** et est initialisé après validation du brief, en plaçant chaque axe sur l'ancre qui correspond à l'état de départ :

| Condition | Effet sur les ancres |
|-----------|----------------------|
| Brief validé | Clarté ≈ palier 40 ; autres axes ≈ palier 20 |
| + Sources analysées | Profondeur et Couverture relevées d'un cran |
| + Historique trouvé | Clarté relevée |
| + HMW générés | Couverture relevée |

---

## EMS dans les Checkpoints

Le checkpoint sauvegarde l'état complet :

```yaml
ems_state:
  global: 68
  clarté: 78
  profondeur: 65
  couverture: 72
  décisions: 52
  actionnabilité: 45
  history:
    - iteration: 1
      score: 32
      delta: +32
    - iteration: 2
      score: 48
      delta: +16
    - iteration: 3
      score: 68
      delta: +20
```

---

## EMS dans le Rapport Final

Le rapport inclut :

1. **Score final** avec radar visuel
2. **Graphe de progression** (ASCII art)
3. **Analyse des axes** faibles/forts
4. **Vérification des critères de succès**

### Graphe de progression

```
Score EMS
100 ┤                                    ●─── 78 (Fin)
 80 ┤ · · · · · · · · · · · · · · · ·╭──╯· · · 
 60 ┤ · · · · · · · · · · · · · ·╭──╯· · · · · 
 48 ┤                      ╭────╯
 40 ┤ · · · · · · · · ·╭──╯· · · · · · · · · · 
 32 ┤            ╭────╯
 20 ┤      ╭────╯
  0 ┼─────┴─────┴─────┴─────┴─────┴─────┴─────
    Init  It.1  It.2  It.3  It.4  It.5  Fin
```

---

## Bonnes Pratiques

### Pour améliorer la Clarté
- Reformuler et faire valider
- Définir explicitement le périmètre (in/out)
- Lister les contraintes
- Définir les critères de succès

### Pour améliorer la Profondeur
- Appliquer les 5 Whys
- Faire un deep dive sur un point clé
- Chercher des analogies dans d'autres domaines
- Identifier la cause racine

### Pour améliorer la Couverture
- Appliquer les Six Hats
- Lister les risques
- Explorer les alternatives
- Considérer les différents stakeholders

### Pour améliorer les Décisions
- Appliquer MoSCoW
- Utiliser le scoring pondéré
- Fermer explicitement les threads
- Documenter les rationales

### Pour améliorer l'Actionnabilité
- Définir des actions concrètes
- Assigner des owners
- Fixer des deadlines
- Identifier les quick wins

---

## Limites du Système

- L'EMS est un **indicateur**, pas une vérité absolue
- Les ancres sont des **guides**, pas des règles rigides
- Un EMS élevé ne garantit pas un bon brainstorming (forme vs fond)
- Un EMS bas peut être approprié pour une exploration préliminaire
- Le système ne capture pas la **qualité** des idées, seulement la **maturité** du processus

---

*EMS System v3.2 — Brainstormer v3.2*
