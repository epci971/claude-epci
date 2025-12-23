# EMS — Exploration Maturity Score

> Système de scoring pour mesurer la maturité de l'exploration

---

## Vue d'ensemble

L'EMS (Exploration Maturity Score) est un indicateur composite qui mesure la progression d'un brainstorming vers un résultat exploitable. Il est calculé à chaque fin d'itération et affiché sous forme de radar.

**Nouveautés v3.0** :
- Ancres objectives par axe (critères observables)
- Intégration avec les phases Divergent/Convergent
- Recommandations contextuelles selon la phase

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

## Ancres Objectives (NOUVEAU v3.0)

Chaque axe dispose maintenant de **critères observables** pour un scoring plus cohérent.

### Clarté (25%)

| Score | Ancre Observable |
|-------|------------------|
| **20** | Sujet énoncé mais pas reformulé ni validé |
| **40** | Brief validé avec périmètre in/out défini |
| **60** | + Contraintes identifiées (≥2) + critères de succès définis |
| **80** | + Objectifs SMART + parties prenantes identifiées |
| **100** | Zéro question ouverte sur le "quoi" — définition cristalline |

**Signaux de progression** :
- User valide la reformulation → +20
- Contraintes explicites mentionnées → +10 par contrainte (max 2)
- Critères de succès définis → +10
- Parties prenantes listées → +10

### Profondeur (25%)

| Score | Ancre Observable |
|-------|------------------|
| **20** | Questions de surface uniquement (quoi, qui, quand) |
| **40** | Au moins une chaîne de "pourquoi" (2+ niveaux) |
| **60** | Framework appliqué OU deep dive complété |
| **80** | Insights non-évidents + connexions cross-domain |
| **100** | Cause racine identifiée + validée + implications tracées |

**Signaux de progression** :
- Premier "pourquoi" creusé → +20
- Deuxième niveau de "pourquoi" → +15
- Framework appliqué (5 Whys, Fishbone...) → +15
- Analogie pertinente d'un autre domaine → +10
- Cause racine explicitement nommée → +15

### Couverture (20%)

| Score | Ancre Observable |
|-------|------------------|
| **20** | Une seule perspective explorée |
| **40** | 2-3 angles différents explorés |
| **60** | Risques explicitement adressés OU alternatives comparées |
| **80** | Six Hats complet OU ≥3 alternatives avec critères OU multi-stakeholders |
| **100** | Aucun angle mort identifiable — exploration exhaustive |

**Signaux de progression** :
- Nouvel angle exploré → +15 par angle (max 3)
- Section risques abordée → +15
- Alternative comparée → +10 par alternative (max 2)
- Perspective stakeholder ajoutée → +10

### Décisions (20%)

| Score | Ancre Observable |
|-------|------------------|
| **20** | Tout reste ouvert, aucune orientation |
| **40** | 1-2 orientations prises mais réversibles |
| **60** | Décisions clés verrouillées avec rationale |
| **80** | Arbitrages faits + priorisation établie |
| **100** | Toutes les décisions du scope prises, fils fermés |

**Signaux de progression** :
- Première orientation prise → +20
- Décision explicite avec justification → +15 par décision
- Priorisation établie (MoSCoW, scoring...) → +15
- Thread fermé explicitement → +10 par thread

### Actionnabilité (10%)

| Score | Ancre Observable |
|-------|------------------|
| **20** | Idées vagues, aucune action concrète |
| **40** | "Il faudrait..." mais sans qui/quand |
| **60** | Actions identifiées avec owner OU timeline |
| **80** | Actions + owner + timeline + dépendances |
| **100** | Plan d'action complet, prêt à exécuter |

**Signaux de progression** :
- Première action concrète nommée → +20
- Owner assigné → +15
- Timeline définie → +15
- Dépendances identifiées → +10
- Quick win identifié → +10

---

## Intégration avec les Phases (NOUVEAU v3.0)

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

### Format Standard (fin d'itération)

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

L'EMS démarre à **0** et est initialisé après validation du brief :

| Condition | Score initial |
|-----------|---------------|
| Brief validé | Clarté: 40, autres: 20 |
| + Sources analysées | Profondeur: +10, Couverture: +10 |
| + Historique trouvé | Clarté: +10 |
| + HMW générés | Couverture: +5 |

---

## EMS dans les Checkpoints

Le checkpoint sauvegarde l'état complet :

```yaml
ems_state:
  global: 68
  clarity: 78
  depth: 65
  coverage: 72
  decisions: 52
  actionability: 45
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

*EMS System v2.0 — Brainstormer v3.0*
