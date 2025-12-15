# Cahier des Charges — Skill Estimator

> **Version** : 1.0  
> **Date** : 2025-12-15  
> **Auteur** : Édouard (via Brainstormer)  
> **Statut** : Prêt pour skill-factory  

---

## 1. Vision et Objectif

### 1.1 Mission

**Estimator** transforme un besoin fonctionnel en chiffrage structuré, argumenté et présentable au client, à travers un workflow interactif avec points de validation.

### 1.2 Problème résolu

L'estimation de projets est chronophage, souvent approximative, et manque de traçabilité. Les fourchettes sont rarement documentées, les risques mal intégrés, et la granularité inadaptée au contexte.

### 1.3 Valeur ajoutée

| Bénéfice | Description |
|----------|-------------|
| **Méthodologie reproductible** | Workflow standardisé en 4 phases avec checkpoints |
| **Fourchettes documentées** | Optimiste / Réaliste / Pessimiste avec justification |
| **Risques intégrés** | Coefficients auto-calculés selon contexte client |
| **Format client-ready** | Output Markdown structuré, consommable par Propositor |
| **Interactivité** | Validation utilisateur à chaque phase critique |

---

## 2. Cas d'usage cibles

| Cas d'usage | Description | Fréquence |
|-------------|-------------|-----------|
| Chiffrage nouveau projet | Projet complet de développement web | Hebdomadaire |
| Chiffrage évolution | Nouvelles fonctionnalités sur existant | Hebdomadaire |
| Chiffrage refonte | Migration ou refonte technique | Mensuel |
| Chiffrage TMA | Forfait de maintenance annuel | Mensuel |
| Chiffrage audit | Estimation d'un audit technique | Ponctuel |
| Re-chiffrage | Révision après changement de scope | Ponctuel |

---

## 3. Déclenchement

### 3.1 Triggers suggérés

```yaml
triggers:
  - "estime", "estimation", "chiffre", "chiffrage"
  - "combien coûterait", "budget pour", "évalue le coût"
  - "jours/homme", "JH", "charge de travail"
  - "use estimator"
```

### 3.2 Inputs acceptés

| Source | Type | Priorité |
|--------|------|----------|
| Output `brainstormer` | Rapport de synthèse | ⭐ Idéal |
| Output `code-promptor` | Brief technique | ⭐ Idéal |
| Output `resumator` | Compte-rendu réunion | Bon |
| Cahier des charges client | Document externe | Bon |
| Brief textuel libre | Texte conversation | Acceptable |
| Transcription vocale | Via corrector/clarifior | Acceptable |

---

## 4. Workflow détaillé

### 4.1 Vue d'ensemble

```
┌─────────────────────────────────────────────────────────────────┐
│                 ESTIMATOR — WORKFLOW INTERACTIF                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  PHASE 1          PHASE 2            PHASE 3          PHASE 4   │
│  ───────          ───────            ───────          ───────   │
│                                                                  │
│  Qualification → Découpage FCT → Évaluation → Valorisation      │
│       │               │              │              │           │
│       ▼               ▼              ▼              ▼           │
│  📍 CP1           📍 CP2         📍 CP3        📍 FINAL        │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 4.2 Phase 1 — Qualification

**Objectif** : Comprendre le contexte et calibrer l'estimation.

**Actions** :
1. Analyser l'input (brief, brainstorm, CDC)
2. Poser des questions de cadrage (≤3 si brief clair)
3. Auto-détecter : type projet, granularité, coefficients

**Questions de cadrage** :
- Type de projet : Nouveau / Évolution / Refonte / TMA / Audit ?
- Contexte technique : Stack existante ? Contraintes particulières ?
- Client : Connu ou nouveau ? Clarté des specs ?
- Granularité souhaitée : Auto ou forcée ?

**📍 Checkpoint 1** :

```markdown
📍 Checkpoint 1 — Compréhension du projet

**Ma compréhension** :
[Reformulation du besoin en 3-5 lignes]

**Paramètres détectés** :
- Type projet : [dev/refonte/tma/audit]
- Granularité : [macro/standard/détaillé]
- Coefficient effort : [0.xx] (client [connu/nouveau], specs [claires/partielles/floues])
- Coefficient risque : [1.xx]

**Options :**
→ `valider` — Passer au découpage fonctionnel
→ `modifier [paramètre]` — Ajuster un paramètre
→ `question [sujet]` — Clarifier un point
```

### 4.3 Phase 2 — Découpage fonctionnel

**Objectif** : Identifier toutes les fonctionnalités (explicites ET implicites).

**Actions** :
1. Extraire les fonctionnalités du brief
2. Identifier les fonctionnalités implicites (auth, logs, admin...)
3. Attribuer un ID unique (FCT-001, FCT-002...)
4. Prioriser : MVP / Should / Could
5. Proposer des suggestions IA

**Format du tableau fonctionnel** :

| ID | Fonctionnalité | Description | Priorité | Module | Dépendances |
|----|----------------|-------------|----------|--------|-------------|
| FCT-001 | Authentification | Connexion sécurisée OAuth2 | MVP | Auth | — |
| FCT-002 | Dashboard | Tableau de bord utilisateur | MVP | Core | FCT-001 |
| FCT-003 | Export PDF | Génération de rapports | Should | Reports | FCT-002 |

**📍 Checkpoint 2** :

```markdown
📍 Checkpoint 2 — Découpage fonctionnel

J'ai identifié [N] fonctionnalités réparties en [X] modules :

[Tableau récapitulatif]

💡 **Suggestions IA** :
- Avez-vous prévu [fonctionnalité implicite] ?
- Le module [X] pourrait nécessiter [dépendance externe]

❓ **Questions en suspens** :
- [Question 1] ?
- [Question 2] ?

**Options :**
→ `valider` — Passer à l'évaluation des tâches
→ `ajouter [fonctionnalité]` — Compléter le découpage
→ `modifier FCT-xxx` — Ajuster une fonctionnalité
→ `supprimer FCT-xxx` — Retirer une fonctionnalité
→ `question [sujet]` — Clarifier avant de valider
```

### 4.4 Phase 3 — Évaluation et chiffrage

**Objectif** : Estimer chaque tâche avec fourchettes.

**Structure des lots** :

| Mode | Blocs | Usage |
|------|-------|-------|
| **Light** | 4 blocs fusionnés | Projet < 30 JH |
| **Standard** | 12 blocs | 30-200 JH |
| **Détaillé** | 12 blocs + sous-modules | > 200 JH |

**Blocs standardisés (mode Standard)** :

1. Cadrage
2. Architecture
3. Backend (modulaire si détaillé)
4. Frontend (modulaire si détaillé)
5. Intégrations
6. Conformité
7. Reprise de données
8. Tests
9. Recette
10. Formation
11. Documentation
12. Production/Maintenance

**Format du tableau par lot** :

| Tâche | Description | JH Bas | JH Moyen | JH Haut | Réf. FCT | Type | Criticité |
|-------|-------------|--------|----------|---------|----------|------|-----------|
| Setup projet | Init repo, CI/CD | 2 | 3 | 4 | — | DevOps | Moyenne |
| API Auth | Endpoints authentification | 3 | 4 | 6 | FCT-001 | Back | Élevée |

**Formules de calcul** :

```
JH_Bas = Somme(tâches) × 0.8
JH_Moyen = Somme(tâches) × coeff_effort
JH_Haut = Somme(tâches) × 1.3

Recette = (JH blocs 2-8) × taux_recette × coeff_effort × coeff_risque
```

**Taux de recette par type projet** :

| Type | Taux recette | Justification |
|------|--------------|---------------|
| Développement | 15% | Standard |
| Refonte | 20% | Risques régression |
| TMA | 10% | Tests non-régression |
| Audit | 0% | Livrable = rapport |

**📍 Checkpoint 3** :

```markdown
📍 Checkpoint 3 — Estimation détaillée

**Synthèse par lot** :

| Lot | JH Bas | JH Moyen | JH Haut |
|-----|--------|----------|---------|
| Cadrage | X | X | X |
| Backend | X | X | X |
| ... | ... | ... | ... |
| **TOTAL** | **X** | **X** | **X** |

**Coefficients appliqués** :
- Effort : [0.xx]
- Risque : [1.xx]

⚠️ **Points d'attention** :
- [Tâche X] : incertitude élevée, fourchette large
- [Lot Y] : dépendance externe non confirmée

**Options :**
→ `valider` — Passer à la valorisation
→ `ajuster-jh [ID] [valeur]` — Modifier un JH
→ `recalculer` — Relancer le calcul après modifications
→ `détailler [lot]` — Voir le détail d'un lot
```

### 4.5 Phase 4 — Valorisation et synthèse

**Objectif** : Convertir les JH en budget et documenter les hypothèses.

**Grille TJM par défaut** :

| Profil | TJM | Usage |
|--------|-----|-------|
| Dev Junior | 350-400€ | Tâches simples |
| Dev Confirmé | 450€ (défaut) | Développement standard |
| Dev Senior | 550-650€ | Architecture, complexe |
| Chef de projet | 500-600€ | Coordination |

**Scénarios budgétaires** :

| Scénario | Calcul | Usage |
|----------|--------|-------|
| Light | JH_Bas × 0.7 × TJM | MVP réduit (optionnel) |
| Bas | JH_Bas × TJM | Minimum viable |
| Moyen | JH_Moyen × TJM | **Recommandé** |
| Haut | JH_Haut × TJM | Sécurisé |

**Registre technique** (obligatoire) :
- Hypothèses posées
- Risques identifiés
- Choix stack justifiés
- Éléments hors périmètre

**📍 Checkpoint Final** :

```markdown
📍 Checkpoint Final — Estimation complète

## Synthèse budgétaire

| Scénario | JH | Montant HT |
|----------|-----|------------|
| Light (option) | X | XX XXX € |
| Bas | X | XX XXX € |
| **Moyen** | **X** | **XX XXX €** |
| Haut | X | XX XXX € |

**Recommandation** : Scénario Moyen — XX XXX € HT

## Registre technique
[Hypothèses, risques, choix stack]

**Options :**
→ `exporter` — Générer le document final
→ `modifier [section]` — Revenir sur une section
→ `propositor` — Enchaîner vers la proposition commerciale
```

---

## 5. Coefficients automatiques

### 5.1 Grille d'auto-détection

| Type client | Clarté specs | coeff_effort | coeff_risque |
|-------------|--------------|--------------|--------------|
| Connu | Claires | 0.85 | 1.05 |
| Connu | Partielles | 0.90 | 1.10 |
| Nouveau | Claires | 0.90 | 1.10 |
| Nouveau | Floues | 0.95 | 1.20 |

### 5.2 Override manuel

L'utilisateur peut forcer les coefficients via :
- Flag `--coeff [valeur]` au lancement
- Commande `modifier coeff [valeur]` au checkpoint 1

---

## 6. Granularité automatique

| Critère | Granularité | Conséquence |
|---------|-------------|-------------|
| Projet < 30 JH | Macro | 4 blocs fusionnés, ±30% |
| Projet 30-200 JH | Standard | 12 blocs, ±20% |
| Projet > 200 JH | Détaillé | 12 blocs + sous-modules Back/Front, ±10% |

---

## 7. Stack technique

### 7.1 Hiérarchie des préférences

| Domaine | Priorité 1 | Priorité 2 | Fallback |
|---------|------------|------------|----------|
| Backend | **Symfony 7** | Django | Spring Boot, Express |
| Frontend | **React 18** | Vue 3 | Angular |
| Base de données | **PostgreSQL** | MySQL | MongoDB |
| Infrastructure | **Docker** | PaaS | VM traditionnelle |
| Mobile | **React Native** | Flutter | Natif |

### 7.2 Justification obligatoire

Chaque choix de stack doit être justifié dans le registre technique :
- Adéquation au besoin
- Expertise disponible
- Contraintes client
- Maintenabilité

---

## 8. Format de sortie

### 8.1 Structure du document

```markdown
# Estimation — [Nom du Projet]

> Généré le [date] — Version 1.0
> Granularité : [Macro/Standard/Détaillée]
> Référence : EST-[AAAA]-[NNN]

---

## 1. Contexte et périmètre

### 1.1 Description du besoin
[Reformulation]

### 1.2 Périmètre
- **Inclus** : [Liste]
- **Exclus** : [Liste]
- **Hypothèses** : [Liste]

### 1.3 Type de projet
[dev/refonte/tma/audit]

---

## 2. Découpage fonctionnel

| ID | Fonctionnalité | Description | Priorité | Module | Dépendances |
|----|----------------|-------------|----------|--------|-------------|
| FCT-001 | ... | ... | MVP | ... | — |

---

## 3. Stack technique

| Composant | Technologie | Version | Justification |
|-----------|-------------|---------|---------------|
| Backend | Symfony | 7.x LTS | ... |
| Frontend | React | 18.x | ... |

---

## 4. Estimation détaillée

### 4.1 Lot 1 — Cadrage
| Tâche | JH Bas | JH Moyen | JH Haut | Réf. FCT | Type |
|-------|--------|----------|---------|----------|------|

### 4.2 Lot 2 — Backend
[Même structure...]

[Répéter pour chaque lot]

---

## 5. Synthèse de la charge

<!-- ESTIMATOR_DATA_START -->
| Lot | JH Bas | JH Moyen | JH Haut |
|-----|--------|----------|---------|
| Cadrage | X | X | X |
| Backend | X | X | X |
| Frontend | X | X | X |
| ... | ... | ... | ... |
| **TOTAL** | **X** | **X** | **X** |
<!-- ESTIMATOR_DATA_END -->

---

## 6. Valorisation financière

### 6.1 Paramètres
- TJM appliqué : XXX €
- Coefficient effort : 0.XX
- Coefficient risque : 1.XX

### 6.2 Scénarios budgétaires

<!-- ESTIMATOR_BUDGET_START -->
| Scénario | JH | Montant HT |
|----------|-----|------------|
| Light (option) | X | XX XXX € |
| Bas | X | XX XXX € |
| **Moyen** | **X** | **XX XXX €** |
| Haut | X | XX XXX € |
<!-- ESTIMATOR_BUDGET_END -->

**Recommandation** : Scénario [Moyen] — **XX XXX € HT**

---

## 7. Risques identifiés

| Risque | Probabilité | Impact | Mitigation |
|--------|-------------|--------|------------|
| [Risque 1] | Moyenne | +X JH | [Action] |

---

## 8. Registre technique

### 8.1 Hypothèses
- [Hypothèse 1]
- [Hypothèse 2]

### 8.2 Choix techniques justifiés
- Backend : [Justification]
- Frontend : [Justification]

### 8.3 Hors périmètre explicite
- [Élément 1]
- [Élément 2]

---

## 9. Conditions

- **Validité** : 30 jours
- **Base** : [Documents de référence]
- **Révision si** : Changement de périmètre

---

*Document généré par Estimator — Prêt pour Propositor*
```

### 8.2 Balises de données

Les balises `<!-- ESTIMATOR_DATA_START/END -->` et `<!-- ESTIMATOR_BUDGET_START/END -->` permettent à Propositor de parser automatiquement les données structurées.

---

## 9. Commandes et flags

### 9.1 Commandes en session

| Commande | Action |
|----------|--------|
| `valider` | Confirmer le checkpoint, passer à la phase suivante |
| `ajouter [élément]` | Ajouter une fonctionnalité ou tâche |
| `modifier [ID]` | Modifier un élément existant |
| `supprimer [ID]` | Retirer un élément |
| `question [sujet]` | Poser une question avant de valider |
| `ajuster-jh [ID] [valeur]` | Modifier manuellement un JH |
| `recalculer` | Relancer le calcul après modifications |
| `détailler [lot]` | Voir le détail d'un lot |
| `exporter` | Générer le document final |
| `restart` | Reprendre depuis le début |
| `propositor` | Enchaîner vers Propositor |

### 9.2 Flags de lancement

| Flag | Effet | Défaut |
|------|-------|--------|
| `--macro` | Granularité macro (±30%) | Auto |
| `--standard` | Granularité standard (±20%) | ✅ |
| `--detailed` | Granularité détaillée (±10%) | Auto si >200 JH |
| `--tjm [montant]` | Forcer un TJM spécifique | 450€ |
| `--type [dev/refonte/tma/audit]` | Forcer le type de projet | Auto-détecté |
| `--coeff [0.6-1.0]` | Override coefficient effort | Auto |
| `--no-suggestions` | Désactiver suggestions IA | Activées |
| `--client [nom]` | Pré-renseigner le client | — |

---

## 10. Synergies

### 10.1 Flux entrants

| Skill source | Données récupérées | Usage |
|--------------|-------------------|-------|
| `brainstormer` | Rapport de synthèse | Contexte, fonctionnalités |
| `code-promptor` | Brief technique | Spécifications, contraintes |
| `resumator` | Compte-rendu réunion | Besoins exprimés |
| `auditor` (futur) | Rapport d'audit | Base remédiation |

### 10.2 Flux sortants

| Vers skill | Données transmises | Usage |
|------------|-------------------|-------|
| `propositor` | **Estimation complète** | Sections financières, planning |
| `planificator` (futur) | JH par lot | Planning détaillé |
| `tracker` (futur) | Estimation initiale | Référence suivi |

---

## 11. Règles critiques

1. **Interactivité obligatoire** — Pas de génération one-shot, checkpoints à chaque phase
2. **Suggestions IA proactives** — Fonctionnalités implicites, risques, alternatives
3. **Questions si incertitude** — Ne pas deviner, demander clarification
4. **Traçabilité FCT-xxx** — Chaque tâche référence une fonctionnalité
5. **Registre technique complet** — Hypothèses et choix documentés
6. **Langue de l'utilisateur** — Output dans la langue de l'input
7. **Balises de données** — Format parsable pour Propositor

---

## 12. Critères d'acceptance

- [ ] Workflow interactif avec 4 checkpoints
- [ ] Décomposition en lots/fonctionnalités/tâches
- [ ] Métriques de complexité appliquées
- [ ] Trois fourchettes calculées (Bas/Moyen/Haut)
- [ ] Coefficients auto-détectés + override possible
- [ ] Buffer de risque intégré et justifié
- [ ] Stack technique avec justifications
- [ ] Registre technique complet
- [ ] Document Markdown structuré avec balises
- [ ] Suggestions IA à chaque checkpoint
- [ ] Intégration outputs brainstormer/code-promptor
- [ ] Enchaînement fluide vers Propositor

---

## 13. Limitations

Ce skill ne gère PAS :
- La facturation ou comptabilité
- Les contrats ou aspects juridiques
- Les estimations sans périmètre technique
- La négociation (voir `negociator`)
- Le planning détaillé (voir `planificator`)

---

*Fin du CDC Estimator v1.0 — Prêt pour skill-factory*
