# Cahier des Charges — F05: Clarification Intelligente

> **Document**: CDC-F05-001
> **Version**: 1.0.0
> **Date**: 2025-12-15
> **Statut**: Validé
> **Feature ID**: F05
> **Version cible**: EPCI v3.5
> **Priorité**: P1

---

## 1. Contexte Global EPCI

### 1.1 Philosophie EPCI v4.0

```
┌─────────────────────────────────────────────────────────────────────┐
│                        PHILOSOPHIE EPCI                             │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  🎯 SIMPLICITÉ        — 5 commandes ciblées, pas 22                │
│  📋 TRAÇABILITÉ       — Feature Document pour chaque feature        │
│  ⏸️  BREAKPOINTS       — L'humain valide entre les phases           │
│  🔄 TDD               — Red → Green → Refactor systématique         │
│  🧩 MODULARITÉ        — Skills, Agents, Commands séparés            │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### 1.2 État Actuel (Baseline v3.0.0)

La phase de clarification dans `/epci-brief` pose des **questions génériques** qui ne tiennent pas compte du contexte projet.

### 1.3 Glossaire Pertinent

| Terme | Définition |
|-------|------------|
| **Clarification** | Phase de questions/réponses pour affiner le brief |
| **Project Memory** | Système de persistance du contexte projet (F04) |
| **Persona** | Mode de pensée influençant le comportement Claude (F09) |
| **MCP** | Model Context Protocol — serveurs enrichissant le contexte |

---

## 2. Description de la Feature

### 2.1 Contexte et Justification

**Problème** : Les questions de clarification sont actuellement :
- Génériques (même questions pour tous les projets)
- Répétitives (posent des questions déjà répondues dans le passé)
- Déconnectées du contexte (ne tiennent pas compte des features similaires)

**Solution** : Système de clarification intelligente qui :
- Analyse le contexte projet (F04 Project Memory)
- Détecte les features similaires passées
- Génère des questions spécifiques et pertinentes
- S'adapte à la persona active (F09)

### 2.2 Objectif

Transformer la clarification d'un questionnaire générique en une **conversation contextuelle intelligente** qui :
1. Pose maximum **3 questions ciblées**
2. Propose des **suggestions basées sur l'historique**
3. **Évite les questions redondantes**

---

## 3. Spécifications Fonctionnelles

### 3.1 Fonctionnement Global

```
┌─────────────────────────────────────────────────────────────────────┐
│                    CLARIFICATION INTELLIGENTE                       │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  Brief: "Ajouter un système de notifications"                       │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                 ANALYSE CONTEXTUELLE                         │   │
│  │                                                               │   │
│  │  Project Memory dit:                                          │   │
│  │  ├── Stack: Symfony + Messenger                              │   │
│  │  ├── Pattern: Event-driven déjà en place                     │   │
│  │  └── Feature similaire: user-alerts (il y a 2 mois)          │   │
│  │                                                               │   │
│  │  Questions générées:                                          │   │
│  │  ├── "Voulez-vous réutiliser le pattern Event de user-alerts?"│   │
│  │  ├── "Quels canaux: email, push, in-app?"                    │   │
│  │  └── "Intégration avec Messenger existant?"                  │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### 3.2 Sources de Contexte

| Source | Données | Usage |
|--------|---------|-------|
| **Project Memory (F04)** | Features passées, patterns | Suggestions réutilisation |
| **Stack Skill** | Patterns framework | Questions techniques pertinentes |
| **Persona Active (F09)** | Priorités, focus | Orientation des questions |
| **MCP Context7** | Docs externes | Best practices à suggérer |

### 3.3 Algorithme de Génération

```python
def generate_questions(brief: str, context: ProjectMemory) -> List[Question]:
    # 1. Analyser le brief
    keywords = extract_keywords(brief)
    domain = detect_domain(keywords)  # auth, api, ui, data, etc.

    # 2. Chercher features similaires
    similar_features = context.find_similar_features(keywords, threshold=0.7)

    # 3. Détecter patterns réutilisables
    reusable_patterns = context.get_patterns_for_domain(domain)

    # 4. Identifier lacunes du brief
    missing_info = analyze_missing_information(brief, domain)

    # 5. Générer questions (max 3)
    questions = []

    # Question sur réutilisation si feature similaire
    if similar_features:
        questions.append(generate_reuse_question(similar_features[0]))

    # Questions sur lacunes critiques
    for gap in missing_info[:2]:  # Max 2 questions sur lacunes
        questions.append(generate_gap_question(gap))

    # Adapter à la persona
    questions = adapt_to_persona(questions, context.active_persona)

    return questions[:3]  # Toujours max 3
```

### 3.4 Types de Questions

| Type | Déclencheur | Exemple |
|------|-------------|---------|
| **Réutilisation** | Feature similaire trouvée | "UserAlerts utilisait le pattern Observer. Réutiliser ?" |
| **Technique** | Lacune technique détectée | "Quelle stratégie de retry en cas d'échec ?" |
| **Scope** | Périmètre flou | "Inclure les notifications SMS ou uniquement email/push ?" |
| **Intégration** | Composants existants | "Intégrer avec le système de queue Messenger existant ?" |
| **Priorité** | Persona-specific | (Backend) "Quelle garantie de délivrance requise ?" |

### 3.5 Règles de Clarification

| Règle | Description |
|-------|-------------|
| **Maximum 3 questions** | Ne jamais dépasser 3 questions par itération |
| **Maximum 3 itérations** | Boucle de clarification limitée |
| **Pas de redondance** | Ne pas reposer une question déjà répondue |
| **Priorisation** | Questions bloquantes d'abord |
| **Suggestions** | Proposer des réponses par défaut basées sur l'historique |

---

## 4. Exigences Techniques

### 4.1 Analyse Contextuelle

| Exigence | Description | Priorité |
|----------|-------------|----------|
| [MUST] Extraction keywords | Identifier mots-clés du brief | P1 |
| [MUST] Matching features | Trouver features similaires | P1 |
| [MUST] Détection lacunes | Identifier informations manquantes | P1 |
| [SHOULD] Scoring similarité | Calculer score de proximité | P2 |

### 4.2 Génération Questions

| Exigence | Description | Priorité |
|----------|-------------|----------|
| [MUST] Template questions | Templates par type de question | P1 |
| [MUST] Personnalisation | Adapter au contexte projet | P1 |
| [MUST] Suggestions défaut | Proposer réponses basées historique | P1 |
| [SHOULD] Explication | Expliquer pourquoi la question est posée | P2 |

### 4.3 Intégration Persona

| Exigence | Description | Priorité |
|----------|-------------|----------|
| [MUST] Adaptation style | Questions adaptées au focus persona | P1 |
| [SHOULD] Priorités persona | Questions selon hiérarchie priorités | P2 |

---

## 5. Critères d'Acceptation

| ID | Critère | Méthode de vérification |
|----|---------|-------------------------|
| F05-AC1 | Questions contextuelles générées | Test avec historique de features |
| F05-AC2 | Maximum 3 questions par itération | Comptage automatique |
| F05-AC3 | Références features passées | Présence de références dans questions |
| F05-AC4 | Adaptation à la persona | Test avec différentes personas |
| F05-AC5 | Suggestions de réponses | Présence de valeurs par défaut |

---

## 6. Dépendances

### 6.1 Dépendances Entrantes (cette feature dépend de)

| Feature | Type | Description |
|---------|------|-------------|
| F04 Project Memory | **Forte** | Source de l'historique et du contexte |
| F09 Personas | Forte | Adaptation des questions |
| F12 MCP Integration | Faible | Contexte externe (docs) |

### 6.2 Dépendances Sortantes (dépendent de cette feature)

| Feature | Type | Description |
|---------|------|-------------|
| F08 Apprentissage Continu | Faible | Feedback sur pertinence questions |

---

## 7. Effort Estimé

| Tâche | Effort |
|-------|--------|
| Analyse contextuelle | 8h |
| Génération questions | 6h |
| Intégration Project Memory | 4h |
| Intégration Personas | 4h |
| Tests | 3h |
| **Total** | **25h (3j)** |

---

## 8. Livrables

1. Module d'analyse contextuelle
2. Générateur de questions intelligentes
3. Intégration avec Project Memory
4. Templates de questions par type
5. Tests unitaires et d'intégration

---

## 9. Exemples de Clarification

### 9.1 Avec Historique Riche

**Brief** : "Ajouter un système de notifications"

**Contexte détecté** :
- Feature similaire : `user-alerts` (il y a 2 mois)
- Pattern : Event-driven avec Messenger
- Stack : Symfony 7.0

**Questions générées** :
1. "La feature `user-alerts` utilise le pattern Observer avec Messenger. Voulez-vous réutiliser cette architecture ?" *(Suggestion: Oui)*
2. "Quels canaux de notification : email, push browser, in-app, SMS ?" *(Suggestion: email + in-app)*
3. "Quelle priorité de délivrance : temps réel ou batch acceptable ?" *(Suggestion: batch 5min)*

### 9.2 Sans Historique (Nouveau Projet)

**Brief** : "Ajouter un système de notifications"

**Contexte détecté** :
- Pas de features similaires
- Stack : Symfony 7.0 (détecté)
- Persona : --persona-backend

**Questions générées** :
1. "Quels canaux de notification prévoyez-vous ?" *(Pas de suggestion)*
2. "Quelle stratégie de queue : Symfony Messenger, RabbitMQ, autre ?"
3. "Les notifications doivent-elles être persistées en base ?"

### 9.3 Adaptation Persona

**Même brief, persona différente** :

| Persona | Questions orientées vers |
|---------|--------------------------|
| `--persona-backend` | Fiabilité, retry, queue, persistance |
| `--persona-frontend` | UI, UX, animations, accessibilité |
| `--persona-security` | Authentification, rate limiting, PII |

---

## 10. Hors Périmètre

- Clarification vocale / audio
- Clarification multi-utilisateurs
- Apprentissage automatique des questions (géré par F08)
- Interface graphique de clarification

---

*Document généré depuis CDC-EPCI-UNIFIE-v4.md*
