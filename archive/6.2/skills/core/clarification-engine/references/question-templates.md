# Question Templates

Templates de questions contextualisees pour le clarification-engine.

---

## Vue d'ensemble

Templates organises par:
1. **Categorie** - Type d'ambiguite detectee
2. **Contexte** - Domaine technique
3. **Format** - Structure pour AskUserQuestion

---

## Structure Standard

Chaque question suit ce format:

```json
{
  "category": "scope | behavior | technical | priority | constraint | integration",
  "question": "Question claire et concise ?",
  "suggestions": [
    "Option 1 (Recommended)",
    "Option 2",
    "Option 3"
  ],
  "importance": "high | medium | low",
  "default": "Option recommandee si non repondu"
}
```

---

## 1. Templates par Categorie

### Scope Questions

**Template: Feature Boundary**
```yaml
question: "Quel est le perimetre exact de {feature} ?"
suggestions:
  - "Version minimale (MVP)"
  - "Version complete avec toutes les options"
  - "Definir manuellement le scope"
importance: high
default: "Version minimale (MVP)"
```

**Template: Platform**
```yaml
question: "Sur quelle(s) plateforme(s) doit fonctionner {feature} ?"
suggestions:
  - "Web uniquement (Recommended)"
  - "Mobile uniquement (iOS/Android)"
  - "Web + Mobile"
importance: high
default: "Web uniquement"
```

**Template: User Roles**
```yaml
question: "Quels roles utilisateurs sont concernes par {feature} ?"
suggestions:
  - "Tous les utilisateurs"
  - "Utilisateurs authentifies uniquement"
  - "Administrateurs uniquement"
importance: medium
default: "Utilisateurs authentifies uniquement"
```

---

### Behavior Questions

**Template: Error Handling**
```yaml
question: "Que faire si {operation} echoue ?"
suggestions:
  - "Afficher message d'erreur et permettre retry"
  - "Fallback silencieux vers comportement par defaut"
  - "Bloquer l'utilisateur et notifier support"
importance: high
default: "Afficher message d'erreur et permettre retry"
```

**Template: Timeout**
```yaml
question: "Quel timeout pour {operation} ?"
suggestions:
  - "Court (5 secondes)"
  - "Standard (30 secondes)"
  - "Long (2 minutes)"
importance: medium
default: "Standard (30 secondes)"
```

**Template: Edge Case**
```yaml
question: "Comportement quand {condition} ?"
suggestions:
  - "Ignorer silencieusement"
  - "Afficher avertissement"
  - "Bloquer l'operation"
importance: high
default: "Afficher avertissement"
```

**Template: Offline**
```yaml
question: "Comportement en mode offline ?"
suggestions:
  - "Non supporte (Recommended)"
  - "Cache local, sync plus tard"
  - "Mode degrade avec fonctions limitees"
importance: medium
default: "Non supporte"
```

---

### Technical Questions

**Template: Database Choice**
```yaml
question: "Quel type de stockage pour {data} ?"
suggestions:
  - "Base relationnelle existante (PostgreSQL/MySQL)"
  - "Document store (MongoDB)"
  - "Cache/Key-value (Redis)"
importance: medium
default: "Base relationnelle existante"
```

**Template: Auth Method**
```yaml
question: "Quelle methode d'authentification pour {endpoint} ?"
suggestions:
  - "JWT (Recommended)"
  - "Session classique"
  - "API Key"
  - "OAuth 2.0"
importance: high
default: "JWT"
```

**Template: API Style**
```yaml
question: "Quel style d'API pour {feature} ?"
suggestions:
  - "REST (Recommended)"
  - "GraphQL"
  - "gRPC"
importance: medium
default: "REST"
```

**Template: File Storage**
```yaml
question: "Ou stocker les fichiers pour {feature} ?"
suggestions:
  - "Stockage local serveur"
  - "Cloud (S3/GCS) (Recommended)"
  - "CDN avec origin cloud"
importance: medium
default: "Cloud (S3/GCS)"
```

**Template: Queue System**
```yaml
question: "Quel systeme de queue pour {job} ?"
suggestions:
  - "Base de donnees (simple)"
  - "Redis Queue"
  - "RabbitMQ/Kafka (haute charge)"
importance: medium
default: "Base de donnees (simple)"
```

---

### Priority Questions

**Template: Feature Order**
```yaml
question: "Ordre de priorite pour {features} ?"
suggestions:
  - "{feature1} en premier (Recommended)"
  - "{feature2} en premier"
  - "Tous en parallele"
importance: medium
default: "{feature1} en premier"
```

**Template: MVP Scope**
```yaml
question: "Quelles features pour le MVP ?"
suggestions:
  - "Fonctionnalites de base uniquement"
  - "Base + quelques extras"
  - "Version complete"
importance: high
default: "Fonctionnalites de base uniquement"
```

**Template: Optional Feature**
```yaml
question: "{feature} est-il obligatoire ou optionnel ?"
suggestions:
  - "Obligatoire (MVP)"
  - "Nice-to-have (post-MVP)"
  - "A evaluer apres MVP"
importance: medium
default: "Nice-to-have (post-MVP)"
```

---

### Constraint Questions

**Template: Performance Target**
```yaml
question: "Temps de reponse cible pour {operation} ?"
suggestions:
  - "Rapide (< 200ms)"
  - "Standard (< 1s) (Recommended)"
  - "Acceptable (< 3s)"
importance: medium
default: "Standard (< 1s)"
```

**Template: Scale**
```yaml
question: "Combien d'utilisateurs simultanes attendus ?"
suggestions:
  - "Faible (< 100)"
  - "Moyen (100-1000) (Recommended)"
  - "Eleve (1000+)"
importance: medium
default: "Moyen (100-1000)"
```

**Template: Security Level**
```yaml
question: "Niveau de securite requis pour {data} ?"
suggestions:
  - "Standard (auth + HTTPS)"
  - "Eleve (+ encryption at rest)"
  - "Tres eleve (+ audit logs, MFA)"
importance: high
default: "Standard (auth + HTTPS)"
```

**Template: Compatibility**
```yaml
question: "Quels navigateurs/versions supporter ?"
suggestions:
  - "Modernes uniquement (Chrome, Firefox, Safari, Edge recents)"
  - "Inclure IE11/Legacy"
  - "Mobile browsers prioritaires"
importance: low
default: "Modernes uniquement"
```

---

### Integration Questions

**Template: System Target**
```yaml
question: "Quel systeme {type} utiliser ?"
suggestions:
  - "{option1} (Recommended)"
  - "{option2}"
  - "Autre (preciser)"
importance: medium
default: "{option1}"
```

**Template: Sync Direction**
```yaml
question: "Direction de synchronisation avec {system} ?"
suggestions:
  - "Import uniquement (systeme -> notre app)"
  - "Export uniquement (notre app -> systeme)"
  - "Bidirectionnel"
importance: medium
default: "Import uniquement"
```

**Template: Sync Frequency**
```yaml
question: "Frequence de synchronisation avec {system} ?"
suggestions:
  - "Temps reel (webhook/streaming)"
  - "Batch periodique (toutes les heures)"
  - "On-demand (declenchement manuel)"
importance: medium
default: "Batch periodique"
```

**Template: Migration Strategy**
```yaml
question: "Strategie de migration vers {target} ?"
suggestions:
  - "Big bang (tout migrer d'un coup)"
  - "Progressive (par lots)"
  - "Parallel run (les deux systemes actifs)"
importance: high
default: "Progressive (par lots)"
```

---

## 2. Templates par Domaine

### Authentication Domain

| Scenario | Template |
|----------|----------|
| New auth system | "Auth method: JWT, Session, OAuth ?" |
| Social login | "Providers: Google, Facebook, GitHub ?" |
| MFA | "MFA obligatoire ou optionnel ?" |
| Password rules | "Regles: standard (8 chars) ou renforcees ?" |

```yaml
# Auth - Password Reset
question: "Duree de validite du lien de reset ?"
suggestions:
  - "15 minutes"
  - "1 heure (Recommended)"
  - "24 heures"
default: "1 heure"
```

```yaml
# Auth - Session
question: "Duree de session utilisateur ?"
suggestions:
  - "Courte (30 min inactivite)"
  - "Standard (24h) (Recommended)"
  - "Longue (7 jours avec remember me)"
default: "Standard (24h)"
```

---

### Data Domain

| Scenario | Template |
|----------|----------|
| Data retention | "Duree de retention: 1 an, 5 ans, indefini ?" |
| Soft delete | "Suppression logique ou physique ?" |
| Audit trail | "Audit complet ou operations critiques ?" |
| Export format | "Format export: CSV, JSON, Excel ?" |

```yaml
# Data - Retention
question: "Politique de retention des donnees {type} ?"
suggestions:
  - "1 an puis archive"
  - "5 ans (conformite) (Recommended)"
  - "Retention indefinie"
default: "5 ans"
```

```yaml
# Data - Deletion
question: "Type de suppression pour {entity} ?"
suggestions:
  - "Soft delete (marquage, recuperable)"
  - "Hard delete (irreversible)"
  - "Anonymisation (RGPD)"
default: "Soft delete"
```

---

### Notification Domain

| Scenario | Template |
|----------|----------|
| Channels | "Canaux: email, push, SMS ?" |
| Frequency | "Temps reel ou batch quotidien ?" |
| Preferences | "Utilisateur peut configurer ?" |
| Templates | "Templates editables par admin ?" |

```yaml
# Notification - Channels
question: "Canaux de notification pour {event} ?"
suggestions:
  - "Email uniquement (Recommended)"
  - "Email + Push mobile"
  - "Email + Push + SMS"
default: "Email uniquement"
```

```yaml
# Notification - Timing
question: "Quand envoyer la notification {type} ?"
suggestions:
  - "Immediatement"
  - "Batch quotidien (resume)"
  - "Configurable par utilisateur"
default: "Immediatement"
```

---

### File Upload Domain

| Scenario | Template |
|----------|----------|
| Size limits | "Taille max: 5MB, 25MB, 100MB ?" |
| File types | "Types autorises: images, documents, tous ?" |
| Processing | "Traitement: resize, compress, virus scan ?" |
| Storage | "Stockage: local, S3, CDN ?" |

```yaml
# File - Size
question: "Taille maximale pour upload {type} ?"
suggestions:
  - "5 MB (images standard)"
  - "25 MB (documents) (Recommended)"
  - "100 MB (videos/archives)"
default: "25 MB"
```

```yaml
# File - Types
question: "Types de fichiers acceptes pour {feature} ?"
suggestions:
  - "Images uniquement (jpg, png, gif)"
  - "Documents (pdf, doc, xls)"
  - "Tous les types courants"
default: "Images uniquement"
```

---

### Payment Domain

| Scenario | Template |
|----------|----------|
| Provider | "Provider: Stripe, PayPal, autre ?" |
| Methods | "Methodes: CB, virement, wallet ?" |
| Retry | "Retry auto sur echec ?" |
| Refund | "Politique de remboursement ?" |

```yaml
# Payment - Provider
question: "Provider de paiement a utiliser ?"
suggestions:
  - "Stripe (Recommended)"
  - "PayPal"
  - "Provider existant du projet"
default: "Stripe"
```

```yaml
# Payment - Failure
question: "Comportement en cas d'echec de paiement ?"
suggestions:
  - "Retry automatique (3 tentatives)"
  - "Notification manuelle a l'utilisateur"
  - "Bloquer immediatement l'acces"
default: "Retry automatique (3 tentatives)"
```

---

## 3. Format AskUserQuestion

### Single Question

```yaml
AskUserQuestion:
  questions:
    - question: "Quelle methode d'authentification ?"
      header: "Auth"
      options:
        - label: "JWT (Recommended)"
          description: "Standard moderne, stateless"
        - label: "Session"
          description: "Classique, server-side state"
        - label: "OAuth 2.0"
          description: "Pour SSO ou login social"
```

### Multiple Questions (Max 3)

```yaml
AskUserQuestion:
  questions:
    - question: "Scope de la feature ?"
      header: "Scope"
      options:
        - label: "MVP"
          description: "Fonctionnalites essentielles"
        - label: "Complet"
          description: "Toutes les options"

    - question: "Cible performance ?"
      header: "Perf"
      options:
        - label: "< 1s (Recommended)"
          description: "Standard acceptable"
        - label: "< 200ms"
          description: "Haute performance"

    - question: "Plateforme ?"
      header: "Platform"
      options:
        - label: "Web (Recommended)"
          description: "Navigateur uniquement"
        - label: "Web + Mobile"
          description: "Responsive + apps"
```

---

## 4. Regles de Selection

### Priorite des Questions

| Priorite | Critere | Action |
|----------|---------|--------|
| 1 | Bloquante (scope/behavior) | Toujours poser |
| 2 | Impactante (technical) | Poser si pertinent |
| 3 | Optimisation (constraint) | Suggerer default |
| 4 | Nice-to-have (priority) | Poser si temps |

### Regles de Combinaison

```python
def select_questions(ambiguities: list, max_questions: int = 3) -> list:
    """
    Selectionne les questions prioritaires.

    Rules:
    - Max 3 questions par iteration
    - Au moins 1 high importance si presente
    - Equilibrer les categories
    - Eviter redondance
    """
    selected = []

    # High priority first
    high = [a for a in ambiguities if a.importance == "high"]
    selected.extend(high[:2])

    # Fill with medium
    if len(selected) < max_questions:
        medium = [a for a in ambiguities if a.importance == "medium"]
        remaining = max_questions - len(selected)
        selected.extend(medium[:remaining])

    return selected[:max_questions]
```

### Skip Conditions

Ne PAS poser de question si:

| Condition | Raison |
|-----------|--------|
| Default evident | Pattern projet etabli |
| Deja repondu | Question precedente |
| Contexte clair | Specification explicite |
| Faible impact | Question low importance seule |

---

## 5. Personnalisation par Contexte

### Avec Project Memory

Si des features similaires existent:

```yaml
question: "La feature X utilise {pattern}. Reutiliser ?"
suggestions:
  - "Oui, meme approche (Recommended)"
  - "Non, approche differente"
  - "Adapter legerement"
```

### Sans Project Memory

Questions generiques:

```yaml
question: "Quelle approche pour {feature} ?"
suggestions:
  - "Approche simple et standard"
  - "Approche optimisee/avancee"
  - "Definir manuellement"
```

---

## Quick Reference

| Categorie | Question Type | Suggestions Count |
|-----------|---------------|-------------------|
| Scope | Boundary, Platform | 3 |
| Behavior | Error, Timeout, Edge | 3 |
| Technical | Choice (DB, Auth, API) | 3-4 |
| Priority | Order, MVP | 2-3 |
| Constraint | Target (perf, scale) | 3 |
| Integration | System, Direction, Freq | 3 |

**Format standard:**
- 1 question = 3 options + "Autre"
- Max 3 questions par iteration
- Option recommandee marquee "(Recommended)"
- Default fourni pour skip
