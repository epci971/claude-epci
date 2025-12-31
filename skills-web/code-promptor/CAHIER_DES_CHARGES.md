# Cahier des Charges — Code-Promptor v2.1

> **Document généré le** : 31 décembre 2025
> **Auteur** : Édouard (via session Brainstormer)
> **Statut** : Validé — Prêt pour implémentation

---

## 1. Contexte et objectifs

### 1.1 Contexte

Le skill `code-promptor` v2.0 transforme des transcriptions vocales ou textuelles en briefs de développement structurés. La v2.1 répond à de nouveaux besoins identifiés :

- **Enchaînement de briefs** : Pouvoir dicter plusieurs features dans une même conversation sans pollution de contexte
- **Intégration Notion native** : Créer directement les tâches dans Notion sans copier-coller manuel
- **Détection intelligente** : Identifier automatiquement si une dictée contient plusieurs tâches distinctes
- **Sous-tâches générées** : Proposer un plan d'implémentation même si non dicté explicitement

### 1.2 Objectifs

| Objectif | Mesure de succès |
|----------|------------------|
| Productivité | Dicter 5 features → 5 tâches Notion en < 10 min |
| Qualité | Briefs exploitables directement par Claude Code |
| Fluidité | Workflow dicté → Notion sans friction |
| Intelligence | Détection multi-tâches fiable (> 80% précision) |

### 1.3 Périmètre

**In scope :**
- Mode session avec cloisonnement
- Détection multi-tâches agressive
- 3 niveaux de complexité adaptatifs
- Sous-tâches auto-générées
- Export Notion direct
- Commandes de manipulation (merge, split, edit, ref...)

**Out of scope :**
- Modification de tâches Notion existantes
- Import bulk depuis fichiers
- Intégration autres outils (Jira, Linear, GitHub Issues)
- Exécution des tâches (reste un pré-processeur)

---

## 2. Spécifications fonctionnelles

### 2.1 Mode Session (Batch)

#### 2.1.1 Activation

| Trigger | Exemple |
|---------|---------|
| `promptor session` | "promptor session" |
| `session promptor` | "session promptor" |
| `mode série promptor` | "mode série promptor" |
| `batch promptor` | "batch promptor" |

#### 2.1.2 Initialisation

```
User: "promptor session"

Claude: 
🎯 **Session Promptor active**

Mode: Traitement en série
Règle: Chaque dictée = brief(s) indépendant(s)
Export: Direct vers Notion

📂 **Projet Notion ?** (ou 'aucun' pour tâches sans projet)
```

```
User: "Gardel"

Claude:
✅ Projet: **Gardel** verrouillé pour cette session.

Envoyez votre première dictée.
```

#### 2.1.3 Comportement session

| Règle | Description |
|-------|-------------|
| Cloisonnement total | Chaque dictée traitée sans contexte des précédentes |
| Projet persistant | Le projet défini à l'init s'applique à toutes les tâches |
| Compteur interne | Suivi du nombre de briefs générés |
| Fin explicite ou implicite | `fin session` ou changement de sujet |

#### 2.1.4 Résumé de fin de session

```
User: "fin session"

Claude:
📊 **Résumé session Promptor**

| # | Tâche | Type | Temps | Lien |
|---|-------|------|-------|------|
| 1 | Implémenter le calcul TCB | Evolution | 8h | [→](lien) |
| 2 | Corriger l'affichage dates | Bloquant | 1h | [→](lien) |
| 3 | Ajouter export PDF rapports | Evolution | 4h | [→](lien) |

✅ **3 tâches créées** dans projet Gardel
⏱️ **Temps total estimé** : 13h

Session terminée. Nouvelle session avec `promptor session`.
```

#### 2.1.5 Commandes session

| Commande | Action |
|----------|--------|
| `projet [nom]` | Changer de projet en cours de session |
| `fin session` | Terminer et afficher résumé |
| `status` | Afficher état session (projet, nb tâches créées) |

---

### 2.2 Détection Multi-tâches

#### 2.2.1 Mode de détection

**Mode retenu : AGRESSIF**

Le skill tend à détecter plusieurs tâches plutôt qu'une seule. L'utilisateur peut fusionner si nécessaire.

#### 2.2.2 Algorithme

```
DICTÉE REÇUE
     │
     ▼
┌─────────────────────────────────────┐
│ PHASE 1: NETTOYAGE                  │
│ - Supprimer hésitations             │
│ - Garder marqueurs de rupture       │
└─────────────────────────────────────┘
     │
     ▼
┌─────────────────────────────────────┐
│ PHASE 2: SEGMENTATION               │
│ - Découper sur marqueurs            │
│ - Identifier segments distincts     │
└─────────────────────────────────────┘
     │
     ▼
┌─────────────────────────────────────┐
│ PHASE 3: SCORING                    │
│ - Calculer indépendance par segment │
│ - Seuil ≥ 40 = tâche distincte      │
└─────────────────────────────────────┘
     │
     ▼
┌─────────────────────────────────────┐
│ PHASE 4: DÉCISION                   │
│ - ≥ 2 segments qualifiés → MULTI    │
│ - Sinon → MONO                      │
└─────────────────────────────────────┘
```

#### 2.2.3 Marqueurs de rupture

**Explicites (+30 points)**

| Catégorie | Marqueurs |
|-----------|-----------|
| Addition | "aussi", "également", "en plus", "et puis" |
| Rupture | "sinon", "autre chose", "autrement", "à part ça" |
| Transition | "ah et", "oh et", "tiens", "au fait" |
| Énumération | "premièrement/deuxièmement", "d'abord/ensuite" |

**Implicites (+15-25 points)**

| Pattern | Points |
|---------|--------|
| Changement de sujet grammatical | +15 |
| Changement de domaine technique | +25 |
| Verbe d'action différent sur objet différent | +20 |

#### 2.2.4 Score d'indépendance

```
SCORE_SEGMENT = 
    SUJET_DIFFÉRENT × 25 +
    ACTION_DIFFÉRENTE × 20 +
    DOMAINE_DIFFÉRENT × 25 +
    MARQUEUR_EXPLICITE × 30 +
    MARQUEUR_IMPLICITE × 15
```

**Seuil multi-tâches** : Score ≥ 40 pour au moins 2 segments

#### 2.2.5 Domaines techniques

| Domaine | Mots-clés |
|---------|-----------|
| Backend | API, service, endpoint, BDD, Symfony, Django, controller |
| Frontend | UI, interface, composant, React, affichage, formulaire |
| DevOps | déploiement, CI/CD, Docker, config, serveur |
| Data | export, import, CSV, Excel, PDF, rapport |
| Auth | login, authentification, mot de passe, session, token |

#### 2.2.6 Garde-fous

| Limite | Valeur | Action si dépassée |
|--------|--------|-------------------|
| Maximum tâches | 5 | Warning "Dictée très dense" |
| Minimum mots/tâche | 10 | Warning "Tâche très courte" |
| Confiance minimum | 60% | Afficher "⚠️ Découpage incertain" |

---

### 2.3 Checkpoint de validation

#### 2.3.1 Déclenchement

Affiché automatiquement quand MULTI-TÂCHES détecté.

#### 2.3.2 Format

```
📋 **3 tâches détectées dans cette dictée**

┌───┬────────────────────────────────────────┬───────────┬────────────┬───────┐
│ # │ Titre suggéré                          │ Type      │ Complexité │ Temps │
├───┼────────────────────────────────────────┼───────────┼────────────┼───────┤
│ 1 │ Corriger le bug d'authentification     │ Bloquant  │ Quick fix  │ 1h    │
│ 2 │ Implémenter l'export PDF des rapports  │ Evolution │ Standard   │ 4h    │
│ 3 │ Refactorer le service AuthManager      │ Tache     │ Standard   │ 4h    │
└───┴────────────────────────────────────────┴───────────┴────────────┴───────┘

📝 **Segments extraits :**
   1 ← "le login est cassé depuis hier"
   2 ← "aussi faudrait ajouter l'export PDF sur les rapports"
   3 ← "ah et le service auth c'est le bordel, faut nettoyer"

📖 **Commandes disponibles :**
   `ok`          Générer tous les briefs
   `ok 1,2`      Générer seulement certains briefs
   `merge 1,3`   Fusionner en une seule tâche
   `edit N "x"`  Modifier le titre de la tâche N
   `drop N`      Supprimer la tâche N
   `split N`     Découper en sous-tâches
   `reanalyze`   Relancer la détection

Ton choix ?
```

#### 2.3.3 Commandes checkpoint

| Commande | Syntaxe | Action |
|----------|---------|--------|
| Valider tout | `ok` | Génère tous les briefs |
| Valider partiel | `ok N,M` | Génère seulement N et M |
| Fusionner | `merge N,M` | Combine N et M en une tâche |
| Modifier titre | `edit N "nouveau titre"` | Change le titre de N |
| Supprimer | `drop N` | Retire N du batch |
| Découper | `split N` | Demande sous-découpage de N |
| Relancer | `reanalyze` | Réanalyse depuis le début |
| Correction libre | (texte) | Interprété en langage naturel |

---

### 2.4 Niveaux de complexité

#### 2.4.1 Critères de détection

| Niveau | Critères | Temps estimé |
|--------|----------|--------------|
| **Quick fix** | < 50 mots dictés ET verbe correctif ET scope très limité | 1h |
| **Standard** | 50-200 mots OU scope clair avec 1-2 composants | 4h |
| **Majeure** | > 200 mots OU multi-composants OU intégrations externes | 8h |

#### 2.4.2 Verbes par niveau

| Niveau | Verbes typiques |
|--------|-----------------|
| Quick fix | corriger, fixer, débugger, réparer, ajuster |
| Standard | créer, ajouter, implémenter, développer |
| Majeure | concevoir, architecturer, intégrer, refondre |

#### 2.4.3 Affichage

Chaque brief affiche son niveau :
```
📦 **Quick fix** | ⏱️ 1h | 🎯 Confidence: HIGH
```

---

### 2.5 Formats de sortie

#### 2.5.1 Structure commune

Tous les briefs contiennent :
- **Header** : Complexité, temps, confidence
- **Titre** : Format action + objet (Notion-ready)
- **Objectif** : 2-4 phrases
- **Description** : Contexte et fonctionnement
- **Exigences fonctionnelles** : Liste des FR

#### 2.5.2 Format Quick fix

```markdown
# Corriger le bug d'affichage des dates laboratoire

📦 **Quick fix** | ⏱️ 1h | 🎯 Confidence: HIGH

## Objectif

Corriger l'affichage incorrect des dates dans le module laboratoire.

## Contexte

Le problème apparaît sur la page de résultats d'analyses. Les dates s'affichent en format US au lieu de FR.

## Correction attendue

- Identifier le composant d'affichage des dates
- Appliquer le format `d/m/Y`
- Vérifier la cohérence sur les autres vues

## Notes

- Aucune note complémentaire.
```

#### 2.5.3 Format Standard

Inclut en plus :
- **Contraintes techniques** (si mentionnées)
- **Plan d'implémentation** avec sous-tâches groupées

```markdown
## Plan d'implémentation

1. **Backend — Service PDF**
   - [ ] Créer le service `RapportPdfGenerator`
   - [ ] Implémenter le template HTML
   - [ ] Ajouter l'endpoint API

2. **Frontend — Interface**
   - [ ] Ajouter le bouton "Exporter PDF"
   - [ ] Gérer l'état de chargement
   - [ ] Déclencher le téléchargement

3. **Finalisation**
   - [ ] Tests
   - [ ] Documentation
```

#### 2.5.4 Format Majeure

Inclut en plus :
- **Exigences non-fonctionnelles** (NFR)
- **Plan d'implémentation détaillé** (5-6 sections)

#### 2.5.5 Séparateur entre briefs

```
═══════════════════════════════════════════════════════════════════
📋 TÂCHE 1/3 — Copier dans Notion
═══════════════════════════════════════════════════════════════════

[Brief 1]

═══════════════════════════════════════════════════════════════════
📋 TÂCHE 2/3 — Copier dans Notion
═══════════════════════════════════════════════════════════════════

[Brief 2]
```

---

### 2.6 Sous-tâches auto-générées

#### 2.6.1 Principe

Le skill génère des sous-tâches intelligentes basées sur le type de tâche et le domaine technique, même si non dictées explicitement.

#### 2.6.2 Templates par type

| Type | Sous-tâches générées |
|------|----------------------|
| Backend API | Créer endpoint, Valider données, Gérer erreurs, Documenter API |
| Backend Service | Créer service, Implémenter logique, Ajouter logs, Tests unitaires |
| Frontend Composant | Créer composant, Gérer états, Styler, Responsive |
| Bug fix | Identifier cause, Corriger, Tester régression |
| Refacto | Analyser existant, Refactorer, Mettre à jour tests |

#### 2.6.3 Templates par stack

| Stack | Sous-tâches spécifiques |
|-------|-------------------------|
| Symfony | Controller, Service, Repository, Form/DTO |
| Django | View, Serializer, Model, Migration, Celery task |
| React | Component, Hook custom, Context, Tests Jest |

---

### 2.7 Intégration Notion

#### 2.7.1 Export automatique

Après validation du checkpoint, les tâches sont créées automatiquement dans Notion.

#### 2.7.2 Propriétés remplies

| Propriété Notion | Source | Exemple |
|------------------|--------|---------|
| Nom | Titre du brief | "Implémenter l'export PDF" |
| Description | Corps du brief | Markdown complet |
| Type | Auto-détecté | "Evolution" |
| Temps estimé | Basé sur complexité | 4 |
| Projet | Défini à l'init session | Relation vers projet |

#### 2.7.3 Propriétés laissées à Notion IA

- État (défaut: "En attente")
- Priorité
- Difficulté
- Étiquettes
- Résumé
- Module

#### 2.7.4 Mapping Types

| Détection Promptor | Type Notion |
|-------------------|-------------|
| Bug, fix, corriger | Bloquant |
| Feature, créer, ajouter | Evolution |
| Refacto, nettoyer, optimiser | Tache |
| Backend spécifique (API, service, BDD) | Backend |
| Frontend spécifique (UI, composant) | Frontend |
| Défaut | Tache |

#### 2.7.5 Gestion erreurs

Si erreur API Notion :
1. Afficher le brief complet en texte
2. Message : "⚠️ Erreur Notion — Brief affiché ci-dessus, copier-coller manuel possible"
3. Proposer retry

---

### 2.8 Commande de référencement

#### 2.8.1 Syntaxe

```
ref [N]
```

#### 2.8.2 Comportement

Crée une dépendance entre la tâche courante et la tâche N de la session.

#### 2.8.3 Affichage dans brief

```markdown
## Dépendances

- ⚠️ Requiert : [Tâche 1 — Créer l'API d'export](lien_notion)
```

#### 2.8.4 Dans Notion

Si export Notion actif, crée la relation dans la propriété "Dépendances".

---

## 3. Spécifications techniques

### 3.1 Structure du skill

```
code-promptor/
├── SKILL.md
├── config/
│   ├── notion-ids.md
│   └── projects-cache.md
├── references/
│   ├── output-format.md
│   ├── processing-rules.md
│   ├── multi-task-detection.md
│   ├── subtask-templates.md
│   ├── type-mapping.md
│   └── voice-cleaning.md
└── templates/
    ├── brief-quickfix.md
    ├── brief-standard.md
    ├── brief-major.md
    └── checkpoint-format.md
```

### 3.2 Dépendances

| Outil | Usage |
|-------|-------|
| Notion MCP | Création des pages/tâches |
| notion-search | Résolution projet |
| notion-create-pages | Création tâches |

### 3.3 Base de données Notion cible

| Propriété | Type | Requis |
|-----------|------|--------|
| Nom | Title | ✅ |
| Description | Text | ✅ |
| Type | Multi-select | ✅ |
| Temps estimé | Number | ✅ |
| Projet | Relation | ⚪ Optionnel |
| État | Status | Auto (Notion) |
| Priorité | Select | Auto (Notion IA) |
| Difficulté | Select | Auto (Notion IA) |
| Étiquettes | Multi-select | Auto (Notion IA) |

---

## 4. Règles métier

### 4.1 Règles critiques

1. **Jamais demander de clarification** — Produire le brief avec l'information disponible
2. **Jamais inventer de requirements** — Si non mentionné, marquer absent
3. **Jamais référencer la source** — Brief auto-suffisant
4. **Une dictée = contexte isolé** — Pas de pollution entre dictées
5. **Later wins** — En cas de contradiction, la dernière version prime

### 4.2 Règles de génération

1. **Titre = Action + Objet** — Format Notion-ready
2. **Sous-tâches générées** — Même si non dictées
3. **Estimation basée sur complexité** — Quick fix=1h, Standard=4h, Majeure=8h
4. **Plan adaptatif** — Seulement si complexité ≥ Standard

### 4.3 Règles session

1. **Projet demandé à l'init** — Optionnel mais recommandé
2. **Cloisonnement strict** — Chaque dictée = contexte frais
3. **Résumé en fin** — Liste des tâches créées avec liens

---

## 5. Cas d'usage

### 5.1 Cas nominal — Session multi-tâches

```
User: "promptor session"
Claude: [Init session, demande projet]

User: "Gardel"
Claude: [Confirme projet Gardel]

User: "Donc faut fixer le login qui marche plus, et puis aussi ajouter l'export PDF sur les rapports"
Claude: [Détecte 2 tâches, affiche checkpoint]

User: "ok"
Claude: [Génère 2 briefs, crée dans Notion, affiche confirmations]

User: "maintenant le dashboard, faut refaire les graphiques"
Claude: [Nouvelle dictée, contexte frais, génère brief, crée dans Notion]

User: "fin session"
Claude: [Affiche résumé : 3 tâches créées]
```

### 5.2 Cas — Modification checkpoint

```
User: [Dictée avec 3 tâches détectées]
Claude: [Affiche checkpoint 3 tâches]

User: "merge 1,2"
Claude: [Fusionne tâches 1 et 2, nouveau checkpoint avec 2 tâches]

User: "edit 1 'Implémenter auth complète avec export'"
Claude: [Modifie titre, nouveau checkpoint]

User: "ok"
Claude: [Génère 2 briefs]
```

### 5.3 Cas — Erreur Notion

```
User: "ok"
Claude: 
[Génère briefs]
⚠️ **Erreur Notion** — Impossible de créer les tâches

Briefs générés ci-dessous (copier-coller manuel) :

═══════════════════════════════════════════════════════════════════
📋 TÂCHE 1/2
═══════════════════════════════════════════════════════════════════
[Brief complet]
...

🔄 Réessayer ? (retry / skip)
```

---

## 6. Évolutions futures (hors scope v2.1)

| Évolution | Description | Priorité |
|-----------|-------------|----------|
| Templates projet | Structures pré-définies par type de projet | Moyenne |
| Import batch | Importer depuis fichier texte | Basse |
| Intégration GitHub | Créer issues GitHub en parallèle | Basse |
| Mode révision | "Plus détaillé" / "Plus court" après génération | Moyenne |
| Estimation ML | Temps basé sur historique réel | Basse |

---

## 7. Validation

### 7.1 Critères d'acceptation

| Critère | Validation |
|---------|------------|
| Session avec cloisonnement | ✅ Validé brainstorming |
| Détection multi-tâches | ✅ Algorithme défini |
| Checkpoint interactif | ✅ Format et commandes définis |
| 3 formats de brief | ✅ Templates définis |
| Export Notion | ✅ Mapping défini |
| Sous-tâches auto | ✅ Templates par type/stack |

### 7.2 Approbation

| Rôle | Nom | Date | Signature |
|------|-----|------|-----------|
| Product Owner | Édouard | 31/12/2025 | ✅ |
| Brainstormer | Claude | 31/12/2025 | ✅ |

---

**Fin du cahier des charges**
