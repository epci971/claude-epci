# Templates — Propositor

> Detailed structures for all 5 proposal templates

---

## Template Overview

| Template | Use Case | Specificity |
|----------|----------|-------------|
| `dev` | New development | MVP approach, sprints, architecture |
| `refonte` | Migration/refactoring | Existing analysis, migration plan, regression |
| `tma` | Maintenance contract | SLA, processes, flat-rate/time-based |
| `audit` | Technical audit | Methodology, evaluation grid, deliverables |
| `ao-public` | Public tender | DC1/DC2, technical memo, BPU, compliance |

---

## Template A: `dev` (New Development)

### When to Use
- New application from scratch
- New major module on existing platform
- MVP development

### Structure

```markdown
# Proposition Commerciale — [Project Name]

## 1. Page de garde
- Client logo placeholder
- Project name
- Date and reference
- Validity period

## 2. Synthèse exécutive
[10-15 lines: Context + Solution + Benefits + Budget/Timeline]

## 3. Compréhension du besoin
### 3.1 Contexte
### 3.2 Enjeux identifiés
### 3.3 Objectifs du projet
### 3.4 Périmètre
- Inclus
- Exclus

## 4. Solution proposée
### 4.1 Vue d'ensemble
### 4.2 Architecture fonctionnelle
[Optional Mermaid diagram]
### 4.3 Choix technologiques
[Table: Component | Technology | Justification]
### 4.4 Points forts de la solution

## 5. Méthodologie
### 5.1 Approche projet
[Agile/Scrum methodology description]
### 5.2 Phases du projet
[Table: Phase | Description | Deliverables]
### 5.3 Gouvernance
[Meeting rhythm, stakeholders]
### 5.4 Gestion des risques

## 6. Planning prévisionnel
### 6.1 Planning macro
[Mermaid Gantt]
### 6.2 Jalons clés
[Table: Milestone | Date | Deliverable]

## 7. Équipe projet
### 7.1 Organisation
[Table: Role | Profile | Responsibilities | Allocation]
### 7.2 Références similaires
[2-3 relevant project cards]

## 8. Proposition financière
### 8.1 Synthèse budgétaire
[Table: Lot | Description | Amount HT]
### 8.2 Détail de l'estimation
[Scenarios table from Estimator]
### 8.3 Options
[Optional items with pricing]
### 8.4 Conditions de facturation
[Payment milestones]

## 9. Conditions
### 9.1 Validité de l'offre
### 9.2 Conditions de réalisation
### 9.3 Propriété intellectuelle
### 9.4 Confidentialité
### 9.5 Conditions générales

## 10. Annexes
- Annexe A: Détail estimation
- Annexe B: CV intervenants (optional)
- Annexe C: CGV

## Acceptation
[Signature block]
```

### Key Sections Emphasis
- **Architecture diagram**: Expected for dev projects
- **Sprint approach**: Mention iterations, demos
- **MVP concept**: Highlight if applicable

---

## Template B: `refonte` (Migration/Refactoring)

### When to Use
- Legacy system migration
- Major technical refactoring
- Platform modernization

### Structure

```markdown
# Proposition Commerciale — Refonte [Project Name]

## 1. Page de garde

## 2. Synthèse exécutive
[Emphasis on modernization benefits and risk mitigation]

## 3. Analyse de l'existant
### 3.1 Contexte actuel
[Current system description]
### 3.2 Limites identifiées
[Technical debt, performance issues]
### 3.3 Enjeux de la refonte
[Business and technical drivers]

## 4. Stratégie de migration
### 4.1 Approche technique
[Big bang vs progressive, strangler pattern, etc.]
### 4.2 Plan de migration
[Detailed migration steps]
### 4.3 Gestion des risques régression
[Testing strategy, rollback plan]
### 4.4 Coexistence ancien/nouveau
[Transition period management]

## 5. Solution cible
### 5.1 Architecture cible
[Target state diagram]
### 5.2 Choix technologiques
[Modernization stack]
### 5.3 Améliorations apportées
[Benefits vs current system]

## 6. Méthodologie
### 6.1 Approche projet
[Iterative migration methodology]
### 6.2 Phases de migration
[Table with migration waves]
### 6.3 Gouvernance
### 6.4 Plan de tests
[Regression testing emphasis]

## 7. Planning
### 7.1 Planning des vagues
[Migration waves Gantt]
### 7.2 Jalons critiques
[Go/no-go points]

## 8. Équipe projet

## 9. Proposition financière
[Include contingency for unforeseen legacy issues]

## 10. Conditions
[Include specific clauses for existing system access]

## 11. Annexes
```

### Key Sections Emphasis
- **Existing analysis**: Critical for credibility
- **Migration strategy**: Multiple options if appropriate
- **Regression risks**: Show awareness and mitigation

---

## Template C: `tma` (Maintenance Contract)

### When to Use
- Ongoing maintenance contract
- Support agreement
- Evolution maintenance

### Structure

```markdown
# Proposition de Maintenance — [Application Name]

## 1. Page de garde

## 2. Synthèse de l'offre
[Service overview, commitment, pricing model]

## 3. Périmètre de la prestation
### 3.1 Applications couvertes
[List of systems in scope]
### 3.2 Types d'interventions
- Maintenance corrective
- Maintenance évolutive (minor)
- Support utilisateur
### 3.3 Exclusions
[What's not covered]

## 4. Niveaux de service (SLA)
### 4.1 Catégories d'intervention
| Catégorie | Définition | Exemple |
|-----------|------------|---------|
| P1 - Critique | Production bloquée | ... |
| P2 - Majeur | Fonctionnalité impactée | ... |
| P3 - Mineur | Anomalie non bloquante | ... |
| P4 - Évolution | Demande d'amélioration | ... |

### 4.2 Délais de réponse
| Catégorie | Prise en compte | Résolution cible |
|-----------|-----------------|------------------|
| P1 | 1h | 4h |
| P2 | 4h | 1 jour |
| P3 | 1 jour | 5 jours |
| P4 | À planifier | Sprint suivant |

### 4.3 Indicateurs de performance (KPIs)
[SLA compliance metrics]

### 4.4 Pénalités (optional)
[SLA breach penalties if applicable]

## 5. Organisation et gouvernance
### 5.1 Équipe dédiée
### 5.2 Points de contact
### 5.3 Comités de suivi
### 5.4 Reporting

## 6. Processus d'intervention
### 6.1 Signalement d'incident
[Ticketing process]
### 6.2 Traitement
[Workflow diagram]
### 6.3 Communication
[Status updates]
### 6.4 Clôture
[Validation process]

## 7. Proposition financière
### 7.1 Modèle de facturation
[Flat-rate / Time-based / Hybrid]
### 7.2 Forfait mensuel
[If applicable]
### 7.3 Tarifs horaires
[If applicable]
### 7.4 Évolutions hors forfait
[Pricing for out-of-scope requests]

## 8. Conditions contractuelles
### 8.1 Durée du contrat
### 8.2 Reconduction
### 8.3 Résiliation
### 8.4 Révision tarifaire

## 9. Annexes
- Annexe A: Inventaire applicatif
- Annexe B: Procédures détaillées
```

### Key Sections Emphasis
- **SLA clarity**: Detailed, measurable commitments
- **Process transparency**: Clear intervention workflow
- **Pricing model**: Flat-rate vs time-based clearly explained

---

## Template D: `audit` (Technical Audit)

### When to Use
- Code quality audit
- Security audit
- Architecture review
- Performance audit

### Structure

```markdown
# Proposition d'Audit Technique — [Subject]

## 1. Page de garde

## 2. Contexte et objectifs
### 2.1 Contexte de la demande
[Why this audit]
### 2.2 Objectifs de l'audit
[Expected outcomes]
### 2.3 Questions clés
[Specific questions to answer]

## 3. Périmètre de l'audit
### 3.1 Applications/systèmes audités
### 3.2 Aspects couverts
- Code quality
- Security
- Performance
- Architecture
- DevOps practices
### 3.3 Hors périmètre

## 4. Méthodologie d'audit
### 4.1 Approche
[Analysis methodology]
### 4.2 Grille d'évaluation
| Critère | Poids | Échelle |
|---------|-------|---------|
| Maintenabilité | 20% | 1-5 |
| Sécurité | 30% | 1-5 |
| Performance | 25% | 1-5 |
| Documentation | 15% | 1-5 |
| Tests | 10% | 1-5 |

### 4.3 Outils utilisés
[Static analysis, security scanners, etc.]
### 4.4 Standards de référence
[OWASP, SOLID, etc.]

## 5. Livrables attendus
### 5.1 Rapport d'audit
- Synthèse exécutive
- Analyse détaillée par critère
- Scoring et benchmarks
- Recommandations priorisées
### 5.2 Présentation des résultats
[Restitution meeting]
### 5.3 Plan d'action recommandé
[Remediation roadmap]

## 6. Planning d'intervention
### 6.1 Phases
| Phase | Durée | Activités |
|-------|-------|-----------|
| Préparation | X jours | Accès, documentation |
| Analyse | X jours | Code review, tests |
| Synthèse | X jours | Report writing |
| Restitution | 0.5 jour | Presentation |

### 6.2 Prérequis client
[Access requirements, documentation needed]

## 7. Proposition financière
[Fixed price for defined scope]

## 8. Conditions
### 8.1 Confidentialité
[Strong NDA for audit data]
### 8.2 Accès aux systèmes
### 8.3 Utilisation des résultats

## 9. Références similaires
[Past audit experience]
```

### Key Sections Emphasis
- **Methodology transparency**: Build trust
- **Evaluation grid**: Objective, measurable
- **Deliverables clarity**: What client will receive

---

## Template E: `ao-public` (Public Tender)

### When to Use
- Response to public sector RFP
- Government contracts
- Regulated procurement

### Structure

```markdown
# Réponse à l'Appel d'Offres — [AO Reference]

## Pièce 1: Lettre de candidature (DC1)
[Standard form or letter format]
- Identification du candidat
- Objet du marché
- Déclaration sur l'honneur

## Pièce 2: Déclaration du candidat (DC2)
[Standard form]
- Capacités économiques et financières
- Capacités techniques et professionnelles
- Références

## Pièce 3: Mémoire technique

### 3.1 Compréhension du besoin
[Detailed reformulation of requirements]
[Show understanding of public sector constraints]

### 3.2 Solution technique proposée
#### 3.2.1 Architecture générale
#### 3.2.2 Choix technologiques
[Justify against specs requirements]
#### 3.2.3 Conformité aux exigences
[Compliance matrix]
| Exigence RC | Réponse | Référence |
|-------------|---------|-----------|
| EX-001 | Conforme | §3.2.1 |
| EX-002 | Conforme avec variante | §3.2.2 |

### 3.3 Méthodologie de réalisation
#### 3.3.1 Organisation du projet
#### 3.3.2 Processus qualité
#### 3.3.3 Gestion des risques
#### 3.3.4 Recette et validation

### 3.4 Moyens humains et matériels
#### 3.4.1 Équipe projet
[Detailed team with qualifications]
#### 3.4.2 Moyens techniques
[Infrastructure, tools]
#### 3.4.3 Sous-traitance éventuelle

### 3.5 Planning détaillé
[Detailed Gantt aligned with RC requirements]

### 3.6 Références et certifications
[Minimum 3 similar references with contact details]

### 3.7 Développement durable (if required)
[Environmental and social commitments]

## Pièce 4: Bordereau des Prix Unitaires (BPU)
| Désignation | Unité | Prix unitaire HT |
|-------------|-------|------------------|
| Jour/homme Chef de projet | jour | XXX € |
| Jour/homme Développeur senior | jour | XXX € |
| Jour/homme Développeur | jour | XXX € |

## Pièce 5: Détail Quantitatif Estimatif (DQE)
[Detailed pricing breakdown per lot/phase]

## Pièce 6: Acte d'engagement
[Pricing summary and commitment]

## Annexes obligatoires
- Kbis ou équivalent
- Attestations fiscales et sociales
- Attestation d'assurance
- RIB
- CVs des intervenants
- Certifications
```

### Key Sections Emphasis
- **Compliance matrix**: Critical for scoring
- **Detailed pricing**: BPU format required
- **References**: Verified, contactable
- **Formal language**: Administrative precision required
- **Complete documentation**: All required pieces

---

## Template Selection Logic

```
IF project.type == "tma" → tma
ELSE IF project.type == "audit" → audit
ELSE IF client.sector == "public" OR brief.contains("appel d'offres") → ao-public
ELSE IF project.type == "refonte" → refonte
ELSE → dev
```

---

## Common Elements Across Templates

### Page de Garde
All templates include:
- Project name
- Client name
- Date
- Reference number (PROP-YYYY-NNN)
- Validity period
- Version

### Acceptance Block
All templates end with:
```markdown
## Acceptation

Pour accord, merci de retourner ce document signé.

| | Client | Prestataire |
|--|--------|-------------|
| Nom | | [Your name] |
| Fonction | | [Your role] |
| Date | | |
| Signature | | |
```
