# Ambiguity Patterns

Reference des patterns de detection d'ambiguite pour le clarification-engine.

---

## Vue d'ensemble

Le clarification-engine detecte 6 types d'ambiguite dans les requirements:

| Type | Description | Priorite |
|------|-------------|----------|
| **Scope** | Limites non definies | High |
| **Behavior** | Edge cases manquants | High |
| **Technical** | Choix techniques non specifies | Medium |
| **Priority** | Ordre des features non clair | Medium |
| **Constraint** | Limitations non precisees | Medium |
| **Integration** | Points de connexion flous | Low |

---

## 1. Scope Ambiguity (Ambiguite de Perimetre)

**Detection**: Limites du feature non clairement definies.

### Patterns Declencheurs

| Pattern | Exemple | Question Generee |
|---------|---------|------------------|
| No boundaries | "ajouter notifications" | "Quels types de notifications ?" |
| Vague scope | "ameliorer la performance" | "Quelles parties specifiques ?" |
| Missing platform | "creer une app" | "Web, mobile, ou les deux ?" |
| No users defined | "pour les utilisateurs" | "Quels roles d'utilisateurs ?" |

### Keywords Indicateurs

```
tous, tout, plusieurs, divers, etc., general, global,
complet, entier, partout, n'importe quel
```

### Exemples

| Input | Ambiguite | Question |
|-------|-----------|----------|
| "Gerer les fichiers" | Type non defini | "Quels types de fichiers ? (images, documents, tous)" |
| "Support multilingue" | Langues non listees | "Quelles langues supporter initialement ?" |
| "Ameliorer le dashboard" | Zone non definie | "Quels widgets/sections du dashboard ?" |

### Scoring

```
scope_ambiguity_score = count(vague_terms) * 0.15 + (1 if no_explicit_boundary else 0) * 0.20
```

---

## 2. Behavior Ambiguity (Ambiguite de Comportement)

**Detection**: Edge cases et scenarios non specifies.

### Patterns Declencheurs

| Pattern | Exemple | Question Generee |
|---------|---------|------------------|
| No error handling | "sauvegarder les donnees" | "Que faire en cas d'echec ?" |
| No timeout defined | "attendre la reponse" | "Timeout maximum acceptable ?" |
| Missing fallback | "utiliser l'API" | "Comportement si API indisponible ?" |
| State transitions | "changer le statut" | "Quels etats sont autorises ?" |

### Keywords Indicateurs

```
gerer, traiter, si possible, eventuellement, peut-etre,
automatiquement, intelligemment, intuitivement
```

### Edge Cases Typiques

| Domaine | Edge Cases a Verifier |
|---------|----------------------|
| Auth | Session expiree, compte bloque, MFA |
| Data | Valeurs nulles, limites, formats invalides |
| Network | Offline, timeout, rate limiting |
| UI | Responsive, accessibilite, loading states |
| Files | Taille max, formats, corruption |

### Exemples

| Input | Edge Case Manquant | Question |
|-------|-------------------|----------|
| "Uploader une image" | Taille/format limits | "Taille max et formats acceptes ?" |
| "Envoyer email de confirmation" | Echec envoi | "Que faire si l'email echoue ?" |
| "Charger les donnees utilisateur" | Utilisateur nouveau | "Comportement pour nouvel utilisateur (pas de donnees) ?" |

---

## 3. Technical Ambiguity (Ambiguite Technique)

**Detection**: Choix d'implementation non specifies.

### Patterns Declencheurs

| Pattern | Exemple | Question Generee |
|---------|---------|------------------|
| No tech specified | "ajouter base de donnees" | "SQL ou NoSQL ? Quelle DB ?" |
| Vague integration | "connecter avec le service" | "API REST, GraphQL, ou autre ?" |
| No storage type | "stocker les fichiers" | "Local, cloud (S3/GCS), ou CDN ?" |
| Auth method missing | "securiser l'endpoint" | "JWT, OAuth, API key ?" |

### Keywords Indicateurs

```
implementer, creer, developper, ajouter, integrer,
connecter, stocker, sauvegarder, synchroniser
```

### Decision Points Techniques

| Domaine | Decisions Requises |
|---------|-------------------|
| API | REST vs GraphQL vs gRPC |
| Auth | JWT vs Session vs OAuth |
| Storage | Local vs Cloud vs CDN |
| Queue | Redis vs RabbitMQ vs Kafka |
| Cache | Memory vs Redis vs CDN |
| Search | SQL LIKE vs Elasticsearch vs Algolia |

### Exemples

| Input | Decision Manquante | Question |
|-------|-------------------|----------|
| "Implementer la recherche" | Moteur de recherche | "Recherche simple (SQL) ou avancee (Elasticsearch) ?" |
| "Ajouter notifications push" | Provider | "Firebase, OneSignal, ou autre service ?" |
| "Creer job asynchrone" | Queue system | "Redis, RabbitMQ, ou base de donnees ?" |

---

## 4. Priority Ambiguity (Ambiguite de Priorite)

**Detection**: Ordre d'importance des features non clair.

### Patterns Declencheurs

| Pattern | Exemple | Question Generee |
|---------|---------|------------------|
| Multiple features | "ajouter X, Y et Z" | "Ordre de priorite ?" |
| Nice-to-have vs must | "avec eventuellement" | "Feature obligatoire ou optionnelle ?" |
| No MVP defined | "version complete" | "Quel scope pour le MVP ?" |
| Timeline missing | "le plus tot possible" | "Deadline specifique ?" |

### Keywords Indicateurs

```
aussi, egalement, en plus, eventuellement, idealement,
si possible, plus tard, bonus, nice-to-have, optionnel
```

### MoSCoW Detection

| Indicateur | Classification |
|------------|---------------|
| "doit", "obligatoire", "critique" | Must-have |
| "devrait", "important" | Should-have |
| "pourrait", "utile" | Could-have |
| "eventuellement", "futur" | Won't-have (now) |

### Exemples

| Input | Ambiguite | Question |
|-------|-----------|----------|
| "Dashboard avec graphiques, exports et alertes" | 3 features sans ordre | "Priorite: graphiques, exports, alertes ?" |
| "Ameliorer UX avec animations" | Optionnel vs required | "Animations obligatoires pour le MVP ?" |
| "Ajouter plusieurs methodes de paiement" | Order not clear | "Methode de paiement prioritaire ?" |

---

## 5. Constraint Ambiguity (Ambiguite de Contraintes)

**Detection**: Limitations et requirements non-fonctionnels non specifies.

### Patterns Declencheurs

| Pattern | Exemple | Question Generee |
|---------|---------|------------------|
| No performance req | "rapide" | "Temps de reponse attendu ?" |
| No scale defined | "beaucoup d'utilisateurs" | "Nombre d'utilisateurs simultanes ?" |
| Security level vague | "securise" | "Niveau de securite requis ?" |
| No compatibility | "compatible" | "Quels navigateurs/versions ?" |

### Keywords Indicateurs

```
rapide, performant, securise, fiable, scalable,
robuste, stable, compatible, accessible
```

### Non-Functional Requirements

| Categorie | Questions Standard |
|-----------|-------------------|
| Performance | Latence, throughput, concurrent users |
| Security | Auth level, encryption, audit |
| Availability | SLA, uptime, DR |
| Scalability | Growth expectation, peaks |
| Compatibility | Browsers, devices, versions |
| Accessibility | WCAG level, languages |

### Exemples

| Input | Contrainte Vague | Question |
|-------|-----------------|----------|
| "Page rapide" | Temps non defini | "Temps de chargement cible ? (< 1s, < 3s)" |
| "Support utilisateurs simultanes" | Nombre non defini | "Combien d'utilisateurs simultanes max ?" |
| "Haute disponibilite" | SLA non defini | "SLA cible ? (99%, 99.9%, 99.99%)" |

---

## 6. Integration Ambiguity (Ambiguite d'Integration)

**Detection**: Points de connexion avec systemes existants non clairs.

### Patterns Declencheurs

| Pattern | Exemple | Question Generee |
|---------|---------|------------------|
| System reference vague | "integrer avec le systeme" | "Quel systeme exactement ?" |
| Data flow unclear | "synchroniser les donnees" | "Dans quelle direction ? Frequence ?" |
| API version missing | "utiliser l'API existante" | "Quelle version de l'API ?" |
| Migration path | "migrer vers" | "Migration progressive ou big bang ?" |

### Keywords Indicateurs

```
integrer, connecter, synchroniser, lier, migrer,
importer, exporter, fusionner, mapper
```

### Integration Decisions

| Type | Questions |
|------|-----------|
| Direction | Unidirectionnel ou bidirectionnel ? |
| Frequence | Temps reel, batch, on-demand ? |
| Transformation | Mapping requis ? Validation ? |
| Fallback | Comportement si systeme indisponible ? |

### Exemples

| Input | Point Flou | Question |
|-------|-----------|----------|
| "Integrer CRM" | CRM non specifie | "Quel CRM ? (Salesforce, HubSpot, autre)" |
| "Sync avec ERP" | Direction non claire | "Sync bidirectionnel ou import seulement ?" |
| "Migrer les donnees" | Strategy non definie | "Migration big bang ou progressive ?" |

---

## Matrice de Priorite

Detection et priorite des questions selon impact.

| Ambiguite | Impact Si Ignore | Priorite Question |
|-----------|-----------------|-------------------|
| Scope | Scope creep, hors sujet | Critical |
| Behavior | Bugs en production | Critical |
| Technical | Refactoring majeur | High |
| Constraint | Performance issues | High |
| Priority | Mauvais focus | Medium |
| Integration | Retravail integration | Medium |

---

## Algorithme de Detection

```python
def detect_ambiguities(input: str) -> list[Ambiguity]:
    """
    Detecte les ambiguites dans un requirement.

    Returns:
        Liste triee par importance
    """
    ambiguities = []

    # Check each category
    if has_vague_scope(input):
        ambiguities.append(Ambiguity("scope", importance="high"))

    if missing_edge_cases(input):
        ambiguities.append(Ambiguity("behavior", importance="high"))

    if needs_tech_decision(input):
        ambiguities.append(Ambiguity("technical", importance="medium"))

    if has_multiple_features(input) and no_priority(input):
        ambiguities.append(Ambiguity("priority", importance="medium"))

    if has_nfr_keywords(input) and no_specific_values(input):
        ambiguities.append(Ambiguity("constraint", importance="medium"))

    if has_integration_keywords(input) and vague_target(input):
        ambiguities.append(Ambiguity("integration", importance="low"))

    return sorted(ambiguities, key=lambda x: x.importance, reverse=True)
```

---

## Quick Reference

| Type | Declencheur | Question Type | Priorite |
|------|-------------|---------------|----------|
| Scope | Limites floues | "Quel perimetre ?" | High |
| Behavior | Edge cases | "Que faire si ?" | High |
| Technical | Choix impl | "Quelle techno ?" | Medium |
| Priority | Multi-features | "Dans quel ordre ?" | Medium |
| Constraint | NFR vagues | "Quelle valeur cible ?" | Medium |
| Integration | Connexions floues | "Quel systeme ?" | Low |

---

## Seuils d'Activation

| Condition | Action |
|-----------|--------|
| 0 ambiguites | Continuer sans clarification |
| 1-2 ambiguites (medium/low) | Suggerer defaults, optionnel |
| 1+ ambiguite (high) | Question obligatoire |
| 3+ ambiguites (any) | Clarification loop requise |

**Max questions par iteration: 3**
