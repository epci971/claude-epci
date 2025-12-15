# Lots Templates — Estimator

> Standard lot structures for different granularity levels

---

## Standard 12-Lot Structure

### Lot Overview

| # | Lot Name | Description | Typical % |
|---|----------|-------------|-----------|
| 1 | Cadrage | Project setup, specs | 5-10% |
| 2 | Architecture | Technical design | 5-10% |
| 3 | Backend | Server-side development | 25-35% |
| 4 | Frontend | Client-side development | 20-30% |
| 5 | Intégrations | External systems | 5-15% |
| 6 | Conformité | Security, RGPD | 3-5% |
| 7 | Reprise | Data migration | 0-10% |
| 8 | Tests | Unit, integration tests | 10-15% |
| 9 | Recette | UAT, client validation | 15% (auto) |
| 10 | Formation | User training | 2-5% |
| 11 | Documentation | Technical docs | 3-5% |
| 12 | Production | Deployment, maintenance | 3-5% |

---

## Lot 1: Cadrage

**Purpose**: Project initialization, requirements gathering, specifications

### Standard Tasks

| Task | Description | JH Low | JH Mid | JH High | Type |
|------|-------------|--------|--------|---------|------|
| Kick-off | Launch meeting, stakeholders | 0.5 | 1 | 1.5 | PO |
| Workshops | Requirements workshops | 2 | 3 | 5 | PO |
| Specs writing | Functional specifications | 3 | 5 | 8 | PO |
| Specs validation | Review and sign-off | 1 | 2 | 3 | PO |
| Project setup | Repo, CI/CD, environments | 1 | 2 | 3 | DevOps |

---

## Lot 2: Architecture

**Purpose**: Technical design, infrastructure setup

### Standard Tasks

| Task | Description | JH Low | JH Mid | JH High | Type |
|------|-------------|--------|--------|---------|------|
| Tech analysis | Stack selection, POC | 2 | 3 | 5 | Back |
| Architecture doc | Technical specifications | 2 | 3 | 4 | Back |
| DB modeling | Database schema design | 2 | 3 | 5 | Back |
| API design | Endpoints specification | 1 | 2 | 3 | Back |
| Infra setup | Docker, staging env | 2 | 3 | 4 | DevOps |

---

## Lot 3: Backend

**Purpose**: Server-side development

### Standard Tasks (adapt to features)

| Task | Description | JH Low | JH Mid | JH High | FCT Ref | Type |
|------|-------------|--------|--------|---------|---------|------|
| Core setup | Framework, base structure | 2 | 3 | 4 | — | Back |
| Authentication | Login, OAuth, sessions | 3 | 5 | 8 | FCT-xxx | Back |
| User management | CRUD users, roles | 2 | 4 | 6 | FCT-xxx | Back |
| [Module X] API | Endpoints for module | 3 | 5 | 8 | FCT-xxx | Back |
| [Module Y] API | Endpoints for module | 3 | 5 | 8 | FCT-xxx | Back |
| Business logic | Core algorithms | 4 | 6 | 10 | FCT-xxx | Back |
| Data validation | Input validation, sanitization | 2 | 3 | 4 | — | Back |

### Detailed Mode: Backend Sub-Modules

For projects > 200 JH, break Backend into:

```
Lot 3: Backend
├── 3.1 Core & Auth
├── 3.2 Module [Name 1]
├── 3.3 Module [Name 2]
├── 3.4 Module [Name N]
└── 3.5 Background Jobs
```

---

## Lot 4: Frontend

**Purpose**: Client-side development

### Standard Tasks (adapt to features)

| Task | Description | JH Low | JH Mid | JH High | FCT Ref | Type |
|------|-------------|--------|--------|---------|---------|------|
| Project setup | React/Vue setup, config | 1 | 2 | 3 | — | Front |
| Design system | Components library | 3 | 5 | 8 | — | Front |
| Auth screens | Login, register, forgot | 2 | 3 | 5 | FCT-xxx | Front |
| Dashboard | Main dashboard view | 3 | 5 | 8 | FCT-xxx | Front |
| [Module X] UI | Screens for module | 4 | 6 | 10 | FCT-xxx | Front |
| [Module Y] UI | Screens for module | 4 | 6 | 10 | FCT-xxx | Front |
| Responsive | Mobile adaptation | 2 | 4 | 6 | — | Front |
| API integration | Connect to backend | 3 | 5 | 8 | — | Front |

### Detailed Mode: Frontend Sub-Modules

For projects > 200 JH, break Frontend into:

```
Lot 4: Frontend
├── 4.1 Core & Layout
├── 4.2 Module [Name 1] UI
├── 4.3 Module [Name 2] UI
├── 4.4 Module [Name N] UI
└── 4.5 Shared Components
```

---

## Lot 5: Intégrations

**Purpose**: External system connections

### Standard Tasks

| Task | Description | JH Low | JH Mid | JH High | Type |
|------|-------------|--------|--------|---------|------|
| API [Name] | Integration with [service] | 2 | 4 | 6 | Back |
| Payment gateway | Stripe/PayPal integration | 3 | 5 | 8 | Back |
| Email service | SendGrid/Mailjet setup | 1 | 2 | 3 | Back |
| SSO | OAuth2/SAML integration | 3 | 5 | 8 | Back |
| File storage | S3/Cloud storage | 1 | 2 | 3 | Back |

---

## Lot 6: Conformité

**Purpose**: Security, compliance, RGPD

### Standard Tasks

| Task | Description | JH Low | JH Mid | JH High | Type |
|------|-------------|--------|--------|---------|------|
| Security audit | OWASP checks | 1 | 2 | 3 | QA |
| RGPD compliance | Consent, data rights | 2 | 3 | 5 | Back |
| Data encryption | At rest, in transit | 1 | 2 | 3 | Back |
| Access logs | Audit trail | 1 | 2 | 3 | Back |

---

## Lot 7: Reprise

**Purpose**: Data migration from existing systems

### Standard Tasks

| Task | Description | JH Low | JH Mid | JH High | Type |
|------|-------------|--------|--------|---------|------|
| Data analysis | Source data study | 2 | 3 | 5 | Back |
| Migration scripts | ETL development | 3 | 5 | 10 | Back |
| Data cleaning | Quality, deduplication | 2 | 4 | 8 | Back |
| Migration tests | Dry runs, validation | 2 | 3 | 5 | QA |
| Cutover | Final migration | 1 | 2 | 3 | DevOps |

**Note**: Set to 0 if no migration needed.

---

## Lot 8: Tests

**Purpose**: Automated testing

### Standard Tasks

| Task | Description | JH Low | JH Mid | JH High | Type |
|------|-------------|--------|--------|---------|------|
| Unit tests BE | Backend unit tests | 3 | 5 | 8 | QA |
| Unit tests FE | Frontend unit tests | 2 | 4 | 6 | QA |
| Integration tests | API tests | 2 | 4 | 6 | QA |
| E2E tests | Cypress/Playwright | 3 | 5 | 8 | QA |
| Test data | Fixtures, factories | 1 | 2 | 3 | QA |

---

## Lot 9: Recette

**Purpose**: Client acceptance testing

### Automatic Calculation

```
recette_jh = (sum lots 2-8) × recette_rate × coeff_effort × coeff_risk
```

### Standard Tasks

| Task | Description | JH Low | JH Mid | JH High | Type |
|------|-------------|--------|--------|---------|------|
| Preparation | Test scenarios, environment | 2 | 3 | 4 | QA |
| Execution | Client testing support | 3 | 5 | 8 | QA |
| Bug fixes | Corrections from feedback | 4 | 6 | 10 | Back/Front |
| Re-testing | Validation of fixes | 2 | 3 | 4 | QA |
| Sign-off | Final acceptance | 1 | 2 | 2 | PO |

---

## Lot 10: Formation

**Purpose**: User and admin training

### Standard Tasks

| Task | Description | JH Low | JH Mid | JH High | Type |
|------|-------------|--------|--------|---------|------|
| Training materials | Guides, videos | 2 | 3 | 5 | PO |
| User training | End-user sessions | 1 | 2 | 3 | PO |
| Admin training | Administrator sessions | 1 | 2 | 3 | PO |

---

## Lot 11: Documentation

**Purpose**: Technical documentation

### Standard Tasks

| Task | Description | JH Low | JH Mid | JH High | Type |
|------|-------------|--------|--------|---------|------|
| README | Repository documentation | 0.5 | 1 | 1.5 | Back |
| API docs | Swagger/OpenAPI | 1 | 2 | 3 | Back |
| Architecture docs | System documentation | 1 | 2 | 3 | Back |
| Deployment guide | Installation procedures | 1 | 2 | 2 | DevOps |

---

## Lot 12: Production & Maintenance

**Purpose**: Deployment and post-launch support

### Standard Tasks

| Task | Description | JH Low | JH Mid | JH High | Type |
|------|-------------|--------|--------|---------|------|
| Prod setup | Production environment | 2 | 3 | 4 | DevOps |
| Deployment | Go-live | 1 | 2 | 3 | DevOps |
| Monitoring | Alerts, dashboards | 1 | 2 | 3 | DevOps |
| Hypercare | Post-launch support (2 weeks) | 2 | 3 | 5 | Back |

---

## Macro Mode: 4 Merged Lots

For projects < 30 JH:

| Lot | Contains | Typical % |
|-----|----------|-----------|
| **Cadrage** | Lots 1-2 | 15-20% |
| **Développement** | Lots 3-7 | 50-60% |
| **Recette** | Lots 8-9 | 15-20% |
| **Déploiement** | Lots 10-12 | 10-15% |

---

## Task Type Legend

| Type | Description | Typical Profile |
|------|-------------|-----------------|
| PO | Project management, specs | Chef de projet |
| Back | Backend development | Dev Symfony/Django |
| Front | Frontend development | Dev React/Vue |
| QA | Quality assurance | Testeur |
| DevOps | Infrastructure, deployment | DevOps engineer |
