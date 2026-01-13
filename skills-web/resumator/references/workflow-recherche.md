# Workflow de recherche web

## Vue d'ensemble

```
Phase 1: Initialisation
├── Extraction thèmes des sources
├── Identification des lacunes
└── Plan de recherche (5-7 axes)

Phase 2: Recherche itérative
├── Génération requêtes par axe
├── Exécution web_search
├── Évaluation pertinence (≥70%)
├── web_fetch sources retenues
└── Vérification saturation

Phase 3: Synthèse
├── Consolidation multi-sources
├── Résolution contradictions
└── Rédaction avec traçabilité
```

---

## Phase 1 : Initialisation

### 1.1 Extraction des thèmes clés

Pour chaque source fournie :
```yaml
Source: [nom/type]
Sujet principal: [1 phrase]
Entités: 
  - Personnes mentionnées
  - Outils/technologies
  - Concepts clés
Sous-thèmes:
  - [liste]
Questions implicites:
  - Ce qui est mentionné mais non développé
  - Ce qui manque pour comprendre
```

### 1.2 Identification des lacunes

Analyser ce qui MANQUE :
- Informations datées → chercher mises à jour
- Affirmations non sourcées → vérifier
- Sujets survolés → approfondir
- Perspectives absentes → diversifier

### 1.3 Plan de recherche

Générer 5-7 axes de recherche :

```yaml
Plan de recherche:
  Axe 1 - Fondamentaux:
    - "[sujet] official documentation"
    - "[sujet] features 2025"
  Axe 2 - Technique:
    - "[sujet] API integration"
    - "[sujet] tutorial"
  Axe 3 - Comparatif:
    - "[sujet] vs [alternative] comparison"
  Axe 4 - Retours:
    - "[sujet] review"
    - "[sujet] limitations"
  Axe 5 - Actualités:
    - "[sujet] latest update 2025"
    - "[sujet] announcement"
```

---

## Phase 2 : Recherche itérative

### 2.1 Types de requêtes

| Type | Objectif | Pattern |
|------|----------|---------|
| Définitionnelle | Comprendre | "what is [X]" |
| Documentaire | Sources officielles | "[X] documentation site:[domain]" |
| Comparative | Positionnement | "[X] vs [Y] comparison" |
| Technique | Implémentation | "[X] tutorial how to" |
| Opinion | Retours terrain | "[X] review reddit" |
| Actualité | News récentes | "[X] 2025 update news" |
| Problèmes | Limitations | "[X] issues limitations problems" |

### 2.2 Évaluation des sources

**Score de fiabilité (1-5 ⭐)** :

| Score | Type de source | Exemples |
|-------|---------------|----------|
| ⭐⭐⭐⭐⭐ | Sources primaires | docs.*, annonces officielles, peer-reviewed |
| ⭐⭐⭐⭐ | Secondaires fiables | TechCrunch, Ars Technica, experts identifiés |
| ⭐⭐⭐ | Communautaires | Stack Overflow (voté), Reddit (argumenté), Dev.to |
| ⭐⭐ | À vérifier | Blogs non sourcés, sans date |
| ⭐ | Non retenues | Obsolète (>2 ans si tech), scraping, promo |

### 2.3 Critères de sélection

**Retenir si** :
- Score ≥ ⭐⭐⭐
- Pertinence ≥ 70% par rapport à l'axe
- Date < 2 ans (pour tech) ou pertinente
- Apporte information nouvelle

**Écarter si** :
- Score ≤ ⭐⭐
- Contenu manifestement promotionnel
- Duplicate d'une source déjà retenue
- Hors sujet

### 2.4 Critères d'arrêt

Arrêter la recherche quand :
- [ ] Tous les axes couverts
- [ ] Saturation (nouvelles sources répètent l'existant)
- [ ] Au moins 3 sources fiables par axe majeur
- [ ] Questions identifiées ont une réponse
- [ ] Contradictions détectées et documentées

---

## Phase 3 : Synthèse

### 3.1 Gestion des contradictions

```
Contradiction détectée
        │
        ▼
┌───────────────────┐
│ Type de           │
│ contradiction ?   │
└───────┬───────────┘
        │
   ┌────┼────┬────────┐
   ▼    ▼    ▼        ▼
Factuelle  Opinion  Temporelle  Incertaine
   │         │         │           │
   ▼         │         │           │
Chercher     │         │           │
source       │         │           │
primaire     │         │           │
   │         │         │           │
   ▼         ▼         ▼           ▼
Adopter   Documenter  Prioriser   Mentionner
si trouvée les deux   récent      incertitude
```

### 3.2 Consolidation

Pour chaque information :
```yaml
Information: "[contenu]"
Sources: [1, 2, 🌐3]
Confiance: ⭐⭐⭐⭐
Recoupement: Oui (3 sources concordantes)
Date: 2025-01 (plus récente)
```

### 3.3 Règles de rédaction

| Règle | Application |
|-------|-------------|
| Traçabilité | Chaque affirmation → [N] ou [🌐N] |
| Transparence | Incertitudes → "⚠️ non vérifié" |
| Équilibre | Points de vue divergents représentés |
| Hiérarchie | Primaire > Récent > Secondaire |
| Fraîcheur | Dater les sources anciennes |

---

## Feedback de progression

Pour les recherches longues (niveau 4-5), afficher :

```
📥 Analyse des sources fournies... (2/3)
🔍 Recherche web — Axe 2/5 : Limitations
   └── Requête : "Claude Code limitations 2025"
   └── Sources évaluées : 8, retenues : 3
📊 Synthèse en cours... (section 6/12)
⏱️ Temps estimé restant : ~4 minutes
```

---

## Métriques finales

À inclure dans le rapport (niveau 5) :

```markdown
## 📈 Métriques de recherche

| Indicateur | Valeur |
|------------|--------|
| Sources fournies analysées | 3/3 ✅ |
| Axes de recherche | 5 |
| Requêtes web exécutées | 12 |
| Sources web évaluées | 24 |
| Sources web retenues | 8 |
| Sources écartées | 16 |
| Contradictions détectées | 2 |
| Contradictions résolues | 2/2 ✅ |
| Score de confiance global | ⭐⭐⭐⭐ (4/5) |
```
