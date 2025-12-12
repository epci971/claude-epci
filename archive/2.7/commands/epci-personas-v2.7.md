# epci-personas — Specialized Expert Personas System (v2.7)

> **EPCI Enhancement** — Activate specialized expertise on demand
>
> Personas bring focused expertise to specific phases of the EPCI workflow.
> Each persona has unique strengths, output styles, and auto-activation triggers.

---

## Critical Rules

- ⚠️ Only ONE persona active at a time (no stacking)
- ⚠️ Personas enhance, they don't replace EPCI workflow rules
- ⚠️ Auto-activation can be overridden with explicit `--persona-*` flag
- ⚠️ Persona output format is ADDITIVE to standard EPCI output
- ⚠️ Not available in `epci-micro` and `epci-hotfix` (too lightweight/urgent)

---

## 1. Overview

### 1.1 What Are Personas?

Personas are **specialized expert modes** that Claude can activate during EPCI commands. Each persona brings:

- **Domain expertise** — Deep knowledge in a specific area
- **Focused perspective** — Prioritizes specific concerns (security, performance, etc.)
- **Tailored output** — Adds persona-specific sections to EPCI output
- **Relevant questions** — Asks domain-specific clarification questions

### 1.2 Available Personas

| Persona | Flag | Specialization | Best For |
|---------|------|----------------|----------|
| **Architect** | `--persona-architect` | System design, patterns, scalability | LARGE features, refactoring |
| **Security** | `--persona-security` | Vulnerabilities, auth, compliance | Auth flows, data handling |
| **Performance** | `--persona-performance` | Optimization, profiling, caching | Hot paths, scaling issues |
| **QA** | `--persona-qa` | Testing, validation, edge cases | Test strategy, coverage |
| **Frontend** | `--persona-frontend` | UI/UX, React, Vue, accessibility | Components, user flows |
| **Backend** | `--persona-backend` | API design, databases, services | Endpoints, data models |
| **DevOps** | `--persona-devops` | CI/CD, deployment, infrastructure | Pipelines, containers |

### 1.3 Persona Lifecycle

```
┌─────────────────────────────────────────────────────────────────┐
│                    PERSONA ACTIVATION                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   1. TRIGGER                                                    │
│      ├── Explicit: --persona-security                           │
│      └── Auto: keywords detected in brief                       │
│                                                                 │
│   2. ACTIVE DURING COMMAND                                      │
│      ├── Adds persona-specific analysis                         │
│      ├── Asks domain-specific questions                         │
│      └── Enhances output with expert sections                   │
│                                                                 │
│   3. DEACTIVATE                                                 │
│      └── At end of command (not persistent across commands)     │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 2. Persona Definitions

### 2.1 Architect (`--persona-architect`)

**Expertise**: System design, architectural patterns, scalability, modularity

**Auto-triggers**:
- Complexity = LARGE
- Keywords: "architecture", "design", "refactor", "restructure", "scalability", "modular"

**Focus Areas**:
- Separation of concerns
- Design patterns applicability
- Dependency management
- Future extensibility
- Technical debt assessment

**Additional Output Section**:
```markdown
### 🏗️ Architect Analysis

#### Design Considerations
- Pattern recommendation: [Repository/Strategy/etc.]
- Coupling assessment: [Low/Medium/High]
- Cohesion assessment: [Low/Medium/High]

#### Scalability Notes
- Horizontal scaling: [considerations]
- Vertical scaling: [considerations]
- Bottleneck risks: [identified risks]

#### Technical Debt
- Existing debt affected: [list]
- New debt introduced: [list or "None"]
- Recommended follow-ups: [list]
```

**Example Questions**:
- "Should this be a separate bounded context?"
- "Is this feature likely to need horizontal scaling?"
- "Are there existing patterns in the codebase we should follow?"

---

### 2.2 Security (`--persona-security`)

**Expertise**: Vulnerabilities, authentication, authorization, data protection, compliance

**Auto-triggers**:
- Keywords: "auth", "login", "password", "token", "permission", "role", "encrypt", "GDPR", "sensitive", "credential"

**Focus Areas**:
- Input validation
- Authentication/Authorization flows
- Data encryption (at rest, in transit)
- OWASP Top 10 considerations
- Compliance requirements

**Additional Output Section**:
```markdown
### 🔒 Security Analysis

#### Threat Assessment
- Attack surface: [identified entry points]
- Risk level: [Low/Medium/High/Critical]
- OWASP relevance: [applicable categories]

#### Security Requirements
- [ ] Input validation: [specific validations needed]
- [ ] Authentication: [requirements]
- [ ] Authorization: [requirements]
- [ ] Data protection: [encryption, masking needs]

#### Compliance Notes
- GDPR implications: [if applicable]
- Data retention: [considerations]
- Audit logging: [requirements]
```

**Example Questions**:
- "What authentication method is required?"
- "Is this data considered PII under GDPR?"
- "Should failed attempts be rate-limited?"

---

### 2.3 Performance (`--persona-performance`)

**Expertise**: Optimization, profiling, caching, database tuning, algorithmic efficiency

**Auto-triggers**:
- Keywords: "slow", "fast", "optimize", "performance", "latency", "cache", "speed", "bottleneck", "scale"

**Focus Areas**:
- Query optimization
- Caching strategies
- Algorithm complexity
- Memory usage
- Response time targets

**Additional Output Section**:
```markdown
### ⚡ Performance Analysis

#### Performance Targets
- Response time target: [e.g., < 200ms]
- Throughput target: [e.g., 1000 req/s]
- Current baseline: [if known]

#### Optimization Opportunities
- Database: [query optimizations, indexes]
- Caching: [what to cache, TTL strategy]
- Algorithm: [complexity considerations]

#### Monitoring Recommendations
- Key metrics to track: [list]
- Alerting thresholds: [suggestions]

#### Load Considerations
- Expected load: [requests/day, concurrent users]
- Peak handling: [strategy]
```

**Example Questions**:
- "What's the acceptable response time for this endpoint?"
- "How many concurrent users are expected?"
- "Is this data cacheable? What's the freshness requirement?"

---

### 2.4 QA (`--persona-qa`)

**Expertise**: Testing strategies, edge cases, validation, quality metrics

**Auto-triggers**:
- Keywords: "test", "coverage", "quality", "edge case", "validation", "regression"
- Auto-activated in `epci-3-finalize`

**Focus Areas**:
- Test coverage strategy
- Edge case identification
- Regression risk assessment
- Test data requirements
- Acceptance criteria validation

**Additional Output Section**:
```markdown
### 🧪 QA Analysis

#### Test Strategy
- Unit tests: [specific tests needed]
- Integration tests: [specific tests needed]
- E2E tests: [if applicable]
- Coverage target: [percentage]

#### Edge Cases Identified
| # | Edge Case | Expected Behavior | Test Priority |
|---|-----------|-------------------|---------------|
| 1 | [case] | [behavior] | High/Medium/Low |
| 2 | [case] | [behavior] | High/Medium/Low |

#### Regression Risks
- Affected existing functionality: [list]
- Recommended regression tests: [list]

#### Test Data Requirements
- [specific test data needed]
```

**Example Questions**:
- "What's the minimum acceptable test coverage?"
- "Are there existing test fixtures we should use?"
- "Should we add performance/load tests?"

---

### 2.5 Frontend (`--persona-frontend`)

**Expertise**: UI/UX, component architecture, accessibility, responsive design, state management

**Auto-triggers**:
- Keywords: "component", "UI", "UX", "React", "Vue", "CSS", "responsive", "accessibility", "a11y", "form"

**Focus Areas**:
- Component structure
- State management approach
- Accessibility compliance
- Responsive behavior
- User experience flow

**Additional Output Section**:
```markdown
### 🎨 Frontend Analysis

#### Component Architecture
- Component breakdown: [list of components]
- State management: [local/global, library]
- Reusability: [opportunities]

#### UX Considerations
- User flow: [description]
- Loading states: [strategy]
- Error states: [strategy]
- Empty states: [strategy]

#### Accessibility
- WCAG level target: [A/AA/AAA]
- Key a11y requirements: [list]
- Screen reader considerations: [notes]

#### Responsive Behavior
- Breakpoints: [mobile/tablet/desktop]
- Mobile-specific considerations: [notes]
```

**Example Questions**:
- "Is this a controlled or uncontrolled component?"
- "What accessibility level are we targeting?"
- "Should this work offline?"

---

### 2.6 Backend (`--persona-backend`)

**Expertise**: API design, database modeling, service architecture, data integrity

**Auto-triggers**:
- Keywords: "API", "endpoint", "database", "query", "migration", "service", "REST", "GraphQL"

**Focus Areas**:
- API contract design
- Database schema design
- Data integrity constraints
- Service boundaries
- Error handling strategy

**Additional Output Section**:
```markdown
### ⚙️ Backend Analysis

#### API Design
- Endpoints affected: [list]
- HTTP methods: [GET/POST/PUT/DELETE]
- Request/Response contracts: [summary]
- Versioning impact: [notes]

#### Database Considerations
- Schema changes: [migrations needed]
- Indexes: [new indexes recommended]
- Data integrity: [constraints, validations]
- Migration strategy: [if applicable]

#### Service Architecture
- Services affected: [list]
- Dependencies: [external services]
- Transaction boundaries: [notes]

#### Error Handling
- Expected errors: [list with HTTP codes]
- Error response format: [structure]
```

**Example Questions**:
- "Should this be a new endpoint or extend an existing one?"
- "Is this data normalized correctly?"
- "What's the transaction boundary for this operation?"

---

### 2.7 DevOps (`--persona-devops`)

**Expertise**: CI/CD, deployment, infrastructure, monitoring, containerization

**Auto-triggers**:
- Keywords: "deploy", "CI", "CD", "pipeline", "Docker", "Kubernetes", "infrastructure", "monitoring", "environment"

**Focus Areas**:
- Deployment strategy
- Environment configuration
- Infrastructure requirements
- Monitoring and alerting
- Rollback procedures

**Additional Output Section**:
```markdown
### 🚀 DevOps Analysis

#### Deployment Considerations
- Deployment strategy: [rolling/blue-green/canary]
- Feature flags: [needed? which ones?]
- Environment variables: [new ones needed]
- Secrets management: [requirements]

#### Infrastructure
- Resource requirements: [CPU/memory estimates]
- Scaling configuration: [auto-scaling rules]
- Dependencies: [external services, databases]

#### CI/CD Impact
- Pipeline changes: [if any]
- New build steps: [if any]
- Test stages: [recommendations]

#### Monitoring & Observability
- New metrics: [to add]
- Log entries: [key logs to add]
- Alerts: [new alerts needed]
- Dashboards: [updates needed]
```

**Example Questions**:
- "Is this a breaking change requiring blue-green deployment?"
- "Do we need a new environment variable?"
- "Should this be behind a feature flag?"

---

## 3. Auto-Activation Rules

### 3.1 Trigger Priority

1. **Explicit flag** (highest priority) — User specifies `--persona-*`
2. **Keyword detection** — Brief contains trigger keywords
3. **Context inference** — Complexity level or command type suggests persona
4. **None** — No persona activated (default behavior)

### 3.2 Keyword Detection

```
Brief content is scanned for keywords:

"Add user authentication with JWT tokens"
       ^^^^^^^^^^^^^^^^^^^^     ^^^^^^
       triggers: Security       triggers: Security

→ Auto-activate: --persona-security
```

### 3.3 Command-Based Defaults

| Command | Default Persona | Reason |
|---------|-----------------|--------|
| `epci-3-finalize` | QA | Focus on verification and testing |
| `epci-1-analyse` (LARGE) | Architect | Complex design decisions |
| Others | None | Context-dependent |

### 3.4 Override Behavior

```bash
# Auto-detection would activate Security, but user wants Performance focus
epci-1-analyse @auth-feature.md --persona-performance

# Explicitly disable auto-activation
epci-1-analyse @auth-feature.md --no-persona
```

---

## 4. Persona Combinations

### 4.1 Compatible Sequences

Personas can be used **sequentially** across EPCI commands:

```bash
# Phase 1: Architecture focus
epci-1-analyse @feature.md --persona-architect

# Phase 2: Security review
epci-2-code @feature.md --persona-security

# Phase 3: QA focus (default for finalize)
epci-3-finalize @feature.md --persona-qa
```

### 4.2 Incompatible (Single Command)

Only ONE persona per command. These are **invalid**:

```bash
# ❌ INVALID - Multiple personas
epci-1-analyse @feature.md --persona-architect --persona-security

# ✅ VALID - Run separately
epci-1-analyse @feature.md --persona-architect
# Then review with different focus:
epci-1-analyse @feature.md --persona-security --preview
```

### 4.3 Recommended Combinations by Feature Type

| Feature Type | EPCI-1 Persona | EPCI-2 Persona | EPCI-3 Persona |
|--------------|----------------|----------------|----------------|
| **Auth/Security** | Security | Security | QA |
| **New API** | Backend | Backend | QA |
| **UI Component** | Frontend | Frontend | QA |
| **Performance Fix** | Performance | Performance | QA |
| **Large Refactor** | Architect | Architect | QA |
| **Infrastructure** | DevOps | DevOps | DevOps |

---

## 5. Integration with Feature Document

### 5.1 Persona Notes in Feature Document

When a persona is active, its analysis is recorded in the Feature Document:

```markdown
## 2. Technical Plan — EPCI-1

*(Managed by epci-1-analyse. Do not modify manually.)*

### Scope & Goal
...

### 🔒 Security Analysis (persona: security)

*(Added by --persona-security)*

#### Threat Assessment
- Attack surface: Login endpoint, password reset flow
- Risk level: High
- OWASP relevance: A2 (Broken Authentication), A7 (XSS)

#### Security Requirements
- [ ] Input validation: email format, password strength
- [ ] Rate limiting: 5 attempts per minute
- [ ] Audit logging: all auth events
```

### 5.2 Tracking Active Personas

The Feature Document header can note which personas were used:

```markdown
# User Authentication Feature

> **Personas used**: Security (EPCI-1), QA (EPCI-3)
> **Last updated**: 2025-01-15

## 1. Functional Brief — EPCI-0
...
```

---

## 6. Usage Examples

### 6.1 Explicit Activation

```bash
# Security-focused analysis
epci-1-analyse
FEATURE_SLUG=user-authentication
--persona-security

# Output includes:
# - Standard EPCI-1 sections
# - 🔒 Security Analysis section
# - Security-focused questions
```

### 6.2 Auto-Activation

```bash
# Brief contains "login", "password", "JWT"
epci-0-briefing
$ARGUMENTS=<RAW_REQUEST>
  TASK: AUTH-123
  RAW_BRIEF: Add JWT-based login with password reset functionality

# Claude detects keywords → auto-activates Security persona
# Output: "🔒 Security persona auto-activated based on keywords: login, password, JWT"
```

### 6.3 Full Workflow with Personas

```bash
# Step 1: Briefing (auto-detects Security)
epci-0-briefing @auth-brief.txt
# → Routes to epci-1-analyse with Security recommendation

# Step 2: Analysis with Security focus
epci-1-analyse @auth.md --persona-security
# → Detailed security analysis, threat assessment

# Step 3: Implementation with Security focus
epci-2-code @auth.md --persona-security
# → Security-conscious implementation, input validation

# Step 4: Finalization with QA focus
epci-3-finalize @auth.md --persona-qa
# → Comprehensive test coverage, edge case verification
```

---

## 7. Compatibility Matrix

| Command | Personas Available | Notes |
|---------|-------------------|-------|
| `epci-0-briefing` | All 7 | Influences questions and routing |
| `epci-1-analyse` | All 7 | Enhances exploration and planning |
| `epci-2-code` | All 7 | Guides implementation focus |
| `epci-3-finalize` | All 7 (QA default) | QA auto-activated |
| `epci-soft` | All 7 | Full persona support |
| `epci-micro` | ❌ None | Too lightweight |
| `epci-hotfix` | ❌ None | Emergency mode, no extras |
| `epci-spike` | ❌ None | Exploration mode, neutral |
| `epci-discover` | ❌ None | Pre-briefing, neutral |

---

## 8. Summary

The EPCI Personas system provides:

1. **7 specialized experts** — Architect, Security, Performance, QA, Frontend, Backend, DevOps
2. **Flexible activation** — Explicit flags or automatic keyword detection
3. **Enhanced output** — Domain-specific analysis sections added to EPCI output
4. **Feature Document integration** — Persona analyses recorded for traceability
5. **Workflow compatibility** — Works across most EPCI commands

Use personas to bring focused expertise to your development workflow without leaving the structured EPCI process.

---

*This document is part of the EPCI v2.7 workflow system.*
