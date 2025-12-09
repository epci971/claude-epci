# epci-spike — Time-boxed Exploration Workflow (v2.7)

> **EXPLORATION MODE** — Learn before you commit
> 
> `epci-spike` is for **technical uncertainty**: when you need to explore 
> feasibility, compare options, or estimate effort before committing to a feature.
> 
> Output: A **decision** (GO / NO-GO / MORE RESEARCH), not a feature.

> **Philosophy**: "Measure twice, cut once."

---

## Critical Rules

- ⚠️ **Time-box is STRICT** — Stop when time runs out, even if incomplete
- ⚠️ **NO production code** — All code is throwaway/prototype
- ⚠️ **Decision required** — Must end with GO / NO-GO / MORE RESEARCH
- ⚠️ **Document findings** — Learnings must survive the spike
- ⚠️ **No scope creep** — Answer the question, nothing more
- ⚠️ **Personas enhance exploration** — Use them for specialized focus (v2.7)

---

## Supported Flags (v2.7)

`epci-spike` supports **exploration-focused flags** — no production code means no production safety flags.

### Available Flags

| Flag | Effect | Use Case |
|------|--------|----------|
| `--uc` | Ultra-compressed output | Quick spike reports |
| `--verbose` | Maximum exploration detail | Deep investigation spikes |
| `--introspect` | Show reasoning and decision logic | Justify recommendations |

### Not Available Flags

| Flag | Reason |
|------|--------|
| `--preview` | Exploration IS preview — no production writes |
| `--safe-mode` | No production file modifications |
| `--validate` | No production code to validate |
| `--dry-run` | Nothing to simulate |

### Usage Examples

```bash
# Detailed architecture exploration
epci-spike --verbose --introspect
$ARGUMENTS=<SPIKE_BRIEF>

# Quick feasibility check
epci-spike --uc
$ARGUMENTS=<SPIKE_BRIEF>

# Show decision reasoning
epci-spike --introspect
$ARGUMENTS=<SPIKE_BRIEF>
```

### Flag Behaviour

| Flag | Effect in epci-spike |
|------|---------------------|
| `--uc` | Minimal report: Question → Key findings → Decision |
| `--verbose` | Full exploration log with all details |
| `--introspect` | Adds reasoning blocks explaining exploration choices and decision logic |

---

## Supported Personas (v2.7)

`epci-spike` supports **all 7 personas** — specialized expertise is highly valuable during exploration.

### Persona-Spike Alignment

| Persona | Best for Spike Type | Focus Areas |
|---------|---------------------|-------------|
| `--persona-architect` | Architecture, Comparison | Design patterns, scalability, modularity |
| `--persona-security` | Feasibility, Risk assessment | Auth, vulnerabilities, data protection |
| `--persona-performance` | Comparison, Feasibility | Speed, caching, optimization |
| `--persona-backend` | Investigation, Estimation | APIs, databases, services |
| `--persona-frontend` | Comparison, Feasibility | UI libraries, rendering, UX |
| `--persona-qa` | Estimation, Risk assessment | Testability, coverage, edge cases |
| `--persona-devops` | Feasibility, Architecture | Infrastructure, deployment, CI/CD |

### Auto-activation Rules

| Spike Question Contains | Auto-activated Persona |
|------------------------|------------------------|
| "architecture", "design", "structure" | `--persona-architect` |
| "security", "auth", "vulnerability" | `--persona-security` |
| "performance", "speed", "cache" | `--persona-performance` |
| "API", "database", "backend" | `--persona-backend` |
| "UI", "component", "frontend" | `--persona-frontend` |
| "test", "quality", "coverage" | `--persona-qa` |
| "deploy", "CI/CD", "infrastructure" | `--persona-devops` |

### Usage Examples

```bash
# Architecture exploration with architect persona
epci-spike --persona-architect --introspect
QUESTION: What's the best approach for implementing event sourcing?

# Security feasibility check
epci-spike --persona-security
QUESTION: Can we replace our custom auth with Google OAuth2?

# Performance comparison
epci-spike --persona-performance --verbose
QUESTION: Redis vs Memcached for session storage?
```

### Persona Behaviour in Spikes

When a persona is active, it influences:

1. **Exploration Focus**: Persona prioritizes domain-specific aspects
2. **Risk Assessment**: Persona highlights domain-specific risks
3. **Questions Asked**: Persona adds domain-specific investigation areas
4. **Recommendations**: Persona weighs in on final decision

> **Note:** For complete personas documentation, see `epci-personas.md`.

---

## 1. When to Use epci-spike

### 1.1 Valid Triggers (USE epci-spike)

| Question Type | Example | Suggested Persona |
|---------------|---------|-------------------|
| **Feasibility** | "Can we integrate with the XYZ API?" | `--persona-backend` |
| **Comparison** | "Should we use Library A or Library B?" | Depends on domain |
| **Estimation** | "How long would feature X take to build?" | `--persona-architect` |
| **Architecture** | "What's the best approach to implement Y?" | `--persona-architect` |
| **Investigation** | "How does this legacy module actually work?" | `--persona-backend` |
| **Risk assessment** | "What are the blockers for migrating to Z?" | Depends on domain |

### 1.2 Invalid Triggers (DO NOT USE)

| Situation | Use Instead |
|-----------|-------------|
| You know what to build | `epci-0-briefing` |
| Just want to learn (no decision needed) | Free research |
| It's actually a small feature | `epci-soft` or `epci-micro` |
| Production incident | `epci-hotfix` |
| "Let me just try something" without a question | Define the question first |

### 1.3 Decision Rule

```
Do you have a specific QUESTION to answer?
├── NO → Define the question first, then come back
└── YES ↓

Do you need a DECISION at the end (go/no-go)?
├── NO → This is research, not a spike
└── YES ↓

Is the answer UNCERTAIN (requires exploration)?
├── NO → You already know, just do it
└── YES → USE epci-spike ✓
```

---

## 2. Inputs

### 2.1 Spike Brief Format

```text
$ARGUMENTS=<SPIKE_BRIEF>
  QUESTION: <the specific question to answer>
  CONTEXT: <why this matters, what decision depends on it>
  SUCCESS_CRITERIA: <what would a good answer look like>
  TIME_BOX: 30min | 1h | 2h | 4h
  CONSTRAINTS: <technical, business, or time constraints>
```

### 2.2 Example Inputs

**Feasibility Spike:**
```text
$ARGUMENTS=<SPIKE_BRIEF>
  QUESTION: Can we replace our custom auth with Google OAuth2?
  CONTEXT: Security audit recommended moving away from custom auth
  SUCCESS_CRITERIA: Clear yes/no with effort estimate and blockers
  TIME_BOX: 2h
  CONSTRAINTS: Must maintain backward compatibility with existing sessions
```

**Comparison Spike:**
```text
$ARGUMENTS=<SPIKE_BRIEF>
  QUESTION: Redis vs Memcached for our session storage?
  CONTEXT: Current file-based sessions causing performance issues
  SUCCESS_CRITERIA: Recommendation with pros/cons and migration estimate
  TIME_BOX: 1h
  CONSTRAINTS: Must work with our Kubernetes setup
```

**Estimation Spike:**
```text
$ARGUMENTS=<SPIKE_BRIEF>
  QUESTION: How long to add multi-language support?
  CONTEXT: Sales team needs estimate for enterprise client proposal
  SUCCESS_CRITERIA: T-shirt size (S/M/L/XL) with breakdown and risks
  TIME_BOX: 1h
  CONSTRAINTS: None - pure estimation
```

---

## 3. Workflow Steps

### 3.1 Overview

```
┌─────────────────────────────────────────────────────────────────┐
│  STEP 1        STEP 2        STEP 3        STEP 4               │
│  FRAME    →   EXPLORE   →  SYNTHESIZE  →  DECIDE               │
│  (5 min)     (time-box)    (10 min)      (5 min)               │
└─────────────────────────────────────────────────────────────────┘
                    │
                    │ ⏱️ STRICT TIME-BOX
                    │ Stop when time runs out!
                    ▼
```

### 3.2 Step 1 — Frame the Question (5 minutes)

**Objective**: Clarify exactly what we're exploring and why.

**Actions**:
1. Restate the question in precise terms
2. Define what "success" looks like
3. Identify known constraints
4. Set the time-box explicitly
5. Note active flags and persona (v2.7)

**Output**:
```markdown
## 1. Spike Definition

### Question
Can we integrate Google OAuth2 as our primary authentication while 
maintaining backward compatibility with existing user sessions?

### Success Criteria
- [ ] Confirm Google OAuth2 supports our requirements
- [ ] Identify integration points in current codebase
- [ ] Estimate effort (T-shirt size)
- [ ] List blockers and risks

### Constraints
- Must not break existing sessions
- Must work with current User entity
- No budget for third-party auth services

### Time-box
2 hours — hard stop at 16:00 UTC

### Active Configuration (v2.7)
- Flags: `--introspect`
- Persona: `--persona-security` (auto-detected: auth-related question)
```

### 3.3 Step 2 — Explore (Time-boxed)

**Objective**: Gather information to answer the question.

**Actions**:
- Read documentation, code, APIs
- Write throwaway prototypes (NOT production code)
- Test hypotheses quickly
- Use sub-agents liberally for parallel investigation
- Take notes as you go
- Apply persona lens to exploration (v2.7)

**Key Behaviors**:
- **Breadth over depth** — Survey the landscape first
- **Prototype freely** — Code is throwaway, don't polish
- **Note blockers immediately** — Don't lose insights
- **Watch the clock** — Stop when time-box ends, even if incomplete
- **Persona focus** — Let active persona guide exploration priorities (v2.7)

> 💡 **Sub-agent tip**: Use sub-agents extensively during exploration.
> Each sub-agent can investigate a specific aspect without polluting 
> your main context.
>
> Examples:
> - "Use a sub-agent to analyze our current AuthController"
> - "Use a sub-agent to test if the Google OAuth API supports refresh tokens"
> - "Use a sub-agent to check how session migration was done in project X"

**Output** (Exploration Log):
```markdown
## 2. Exploration Log

### 2.1 Google OAuth2 Research
- ✅ Supports authorization code flow (web apps)
- ✅ Provides refresh tokens (long-lived sessions)
- ✅ Required scopes available: email, profile, openid
- ⚠️ Rate limits: 10,000 requests/day on free tier
- ❌ No support for custom claims (we use role in JWT)

### 2.2 Current Auth Analysis
Files examined:
- `AuthController.php` — 450 LOC, handles login/logout/register
- `SessionManager.php` — 200 LOC, PHP sessions
- `User.php` — entity with required `password` field

Key finding: User entity has `password` as NOT NULL in database.
Google users won't have passwords.

### 2.3 Persona-Specific Observations (v2.7)

> 🔒 **Security Persona Notes:**
> - OAuth2 authorization code flow is the correct choice (not implicit)
> - Token storage must be encrypted at rest
> - Refresh token rotation should be enabled
> - PKCE extension recommended for additional security
> - Need to validate Google's ID token signature
> - Consider: what happens if Google account is compromised?

### 2.4 Prototype Results
Created branch `spike/oauth2-google` (THROWAWAY):
- ✅ Successfully completed OAuth2 flow with Google
- ✅ Retrieved user email and profile
- ❌ Failed: Can't create User without password
- 💡 Solution options:
  1. Make password nullable (DB migration)
  2. Create separate OAuthUser entity
  3. Generate random password (hacky)

### 2.5 Effort Mapping

| Component | Estimate | Notes |
|-----------|----------|-------|
| Google OAuth integration | 1 day | Standard implementation |
| User entity changes | 0.5 day | Need to decide approach |
| Session compatibility | 1 day | Tricky edge cases |
| Testing | 1 day | Many flows to cover |
| Documentation | 0.5 day | User guide + API docs |
```

### 3.4 Step 3 — Synthesize Findings (10 minutes)

**Objective**: Consolidate what you learned into actionable insights.

**Actions**:
1. Summarize key findings
2. List what worked and what didn't
3. Identify risks and blockers (persona-weighted) (v2.7)
4. Prepare effort estimate

**Output**:
```markdown
## 3. Findings Summary

### What We Learned
1. Google OAuth2 integration is technically straightforward
2. Main complexity: backward compatibility with password-based users
3. Database migration required (password field → nullable)
4. Session coexistence is possible but needs careful handling

### What Worked
- OAuth2 flow implementation (standard, well-documented)
- Google's API is reliable and fast

### What Didn't Work / Blockers
- Can't use existing User entity as-is (password constraint)
- Custom JWT claims not supported by Google (need workaround)

### Risks (Persona-weighted) (v2.7)

| Risk | Likelihood | Impact | Mitigation | Persona |
|------|------------|--------|------------|---------|
| Token storage vulnerability | Low | Critical | Encrypt at rest | 🔒 Security |
| Google rate limits | Low | High | Implement token caching | |
| Password migration | Medium | Medium | Feature flag rollout | |
| Session hijacking | Low | Critical | PKCE + token rotation | 🔒 Security |
| User confusion | Medium | Low | Clear UI messaging | |

### Effort Estimate

| Size | Meaning | This Spike |
|------|---------|------------|
| S | < 2 days | |
| M | 2-5 days | |
| **L** | **1-2 weeks** | **✓ Estimated: 4-5 days** |
| XL | > 2 weeks | |

**Confidence**: Medium (some unknowns remain around session edge cases)
```

### 3.5 Step 4 — Decide (5 minutes)

**Objective**: Make a clear recommendation.

**Three Possible Outcomes**:

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│   ┌─────────────┐   ┌─────────────┐   ┌─────────────────────┐  │
│   │     GO      │   │   NO-GO     │   │   MORE RESEARCH     │  │
│   │             │   │             │   │                     │  │
│   │ Proceed to  │   │ Don't do    │   │ Need another spike  │  │
│   │ epci-0      │   │ this, here's│   │ to answer:          │  │
│   │ briefing    │   │ why         │   │ [specific question] │  │
│   └─────────────┘   └─────────────┘   └─────────────────────┘  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**Output**:
```markdown
## 4. Decision

### Recommendation: ✅ GO

### Rationale
- Technical feasibility: Confirmed ✓
- Effort reasonable: 4-5 days (acceptable for the value)
- Security: Improved vs current custom auth (persona assessment)
- Risks: Manageable with proper mitigations

### Introspection (--introspect) (v2.7)

> 🔍 **Decision Reasoning:**
> - Chose GO because: all success criteria met, effort acceptable, security improved
> - Considered NO-GO because: DB migration required, but impact is low
> - Persona influence: Security persona confirmed OAuth2 is more secure than custom auth
> - Confidence factors: +Google API well-documented, +standard flow, -session edge cases unknown
> - Key assumption: Team has OAuth2 experience (verified: 2 devs have done it before)

### Next Steps
1. Create detailed EPCI-0 brief with spike findings
2. Plan DB migration for password field
3. Spike follow-up: Session compatibility deep-dive (if needed)

### Open Questions
- How to handle users who have both password and Google login?
- What's the migration path for existing sessions?

### Suggested Persona for Implementation (v2.7)
`--persona-security` recommended for EPCI workflow (auth-related feature)
```

---

## 4. Spike Patterns by Type

### 4.1 Feasibility Spike

**Question pattern**: "Can we do X?"

**Focus**: Yes/no answer with blockers

**Output**: GO / NO-GO with clear reasoning

**Time-box**: 30 min - 2 hours

**Recommended persona**: Depends on domain

```markdown
Example output:

## Feasibility: ✅ YES, with caveats

**Can we integrate with the legacy SOAP API?**

- ✅ API is accessible and documented
- ✅ PHP has SOAP client built-in
- ⚠️ API uses XML-RPC, not REST (need adapter)
- ⚠️ No sandbox environment (test against production)
- ❌ Rate limit: 100 req/hour (may need caching)

**Blockers**: Rate limiting requires caching layer
**Effort**: M (3-4 days with caching)
**Decision**: GO — but implement caching first
```

### 4.2 Comparison Spike

**Question pattern**: "A vs B — which one?"

**Focus**: Pros/cons matrix, recommendation

**Output**: Recommendation with justification

**Time-box**: 1-2 hours

**Recommended persona**: Domain expert (e.g., `--persona-performance` for cache comparison)

```markdown
Example output:

## Comparison: Redis vs Memcached

| Criterion | Redis | Memcached | Winner |
|-----------|-------|-----------|--------|
| Performance | ~100k ops/s | ~100k ops/s | Tie |
| Persistence | ✅ Yes | ❌ No | Redis |
| Data types | Rich | Simple | Redis |
| Memory efficiency | Good | Better | Memcached |
| Clustering | ✅ Built-in | ❌ External | Redis |
| Our K8s setup | ✅ Helm chart | ⚠️ Manual | Redis |

**Recommendation**: Redis

**Rationale**: 
- Persistence valuable for session recovery
- Native clustering simplifies our K8s deployment
- Rich data types enable future use cases

**Persona note (--persona-performance)**:
> For pure session storage, performance is nearly identical.
> Redis wins on operational simplicity and future flexibility.
```

### 4.3 Estimation Spike

**Question pattern**: "How long would X take?"

**Focus**: T-shirt size with breakdown

**Output**: Estimate + confidence level + risks

**Time-box**: 30 min - 1 hour

**Recommended persona**: `--persona-architect`

```markdown
Example output:

## Estimation: Multi-language Support

### T-shirt Size: L (1-2 weeks)

### Breakdown

| Component | Estimate | Confidence |
|-----------|----------|------------|
| i18n library setup | 0.5 day | High |
| Extract strings (50 files) | 2 days | Medium |
| Translation workflow | 1 day | Medium |
| Date/number formatting | 1 day | High |
| RTL support | 2 days | Low |
| Testing | 2 days | Medium |

### Risks
- String extraction may find more files than estimated
- RTL support complexity unknown (never done before)
- Translation turnaround time not included

### Confidence: Medium
> Estimate could vary ±30% based on RTL complexity
```

### 4.4 Architecture Spike

**Question pattern**: "How should we build X?"

**Focus**: Design options, trade-offs, recommendation

**Output**: Architecture decision with diagrams

**Time-box**: 2-4 hours

**Recommended persona**: `--persona-architect` (strongly recommended)

```markdown
Example output:

## Architecture: Event Sourcing for Booking System

### Options Evaluated

| Option | Complexity | Fit | Risk |
|--------|------------|-----|------|
| A: Full event sourcing | High | ✅ Perfect | Medium |
| B: Event sourcing + CQRS | Very High | ✅ Perfect | High |
| C: Audit log only | Low | ⚠️ Partial | Low |

### Recommendation: Option A (Full event sourcing)

**Rationale**: 
- Business requires full audit trail
- Replay capability valuable for debugging
- Team willing to invest in learning

**Persona note (--persona-architect)**:
> Event sourcing adds complexity but provides immutability and auditability.
> For a booking system with financial implications, this is the right trade-off.
> Recommend starting without CQRS, add later if read performance becomes issue.

**Architecture Sketch**:
```
[Command] → [Aggregate] → [Event Store] → [Projections]
                              ↓
                         [Event Bus] → [Read Models]
```
```

### 4.5 Investigation Spike

**Question pattern**: "How does X work?"

**Focus**: Understanding existing code/system

**Output**: Documentation + diagram

**Time-box**: 1-4 hours

**Recommended persona**: `--persona-backend` or domain-specific

```markdown
Example output:

## Investigation Complete

**How does the legacy billing module work?**

### Flow Discovered
1. `CronJob` triggers `BillingProcessor` daily at 00:00
2. `BillingProcessor` queries all active subscriptions
3. For each subscription, calls `PaymentGateway::charge()`
4. Results logged to `billing_log` table
5. Failed charges queued for retry (max 3 attempts)

### Key Files
- `src/Legacy/BillingProcessor.php` — Main orchestrator
- `src/Legacy/PaymentGateway.php` — Stripe wrapper
- `config/billing.yaml` — Retry settings

### Diagram
```
[Cron] → [BillingProcessor] → [DB: subscriptions]
              ↓
         [PaymentGateway] → [Stripe API]
              ↓
         [DB: billing_log]
```

### Gotchas Found
- ⚠️ No transaction wrapping (partial failures possible)
- ⚠️ Hardcoded retry delays (not configurable)
- ⚠️ No dead-letter queue (failed charges lost after 3 retries)
```

---

## 5. Output Format

### 5.1 Standard Spike Report Template

```markdown
# SPIKE REPORT: <title>

## Meta
- **Spike ID**: spike-<descriptive-slug>
- **Question**: <the question being answered>
- **Time-box**: <duration>
- **Date**: <date>
- **Author**: <who did the spike>
- **Flags**: <active flags> (v2.7)
- **Persona**: <active persona> (v2.7)

---

## 1. Spike Definition

### Question
<Precise statement of what we're trying to learn>

### Success Criteria
- [ ] Criterion 1
- [ ] Criterion 2
- [ ] ...

### Constraints
<Any limitations or requirements>

### Time-box
<Duration and hard stop time>

### Active Configuration (v2.7)
- Flags: `--introspect`, `--verbose`
- Persona: `--persona-architect`

---

## 2. Exploration Log

### 2.1 <Area 1>
<Findings, observations, test results>

### 2.2 <Area 2>
<Findings, observations, test results>

### 2.3 Persona-specific Observations (v2.7)
<Domain expert insights>

### 2.4 Prototype Results (if any)
<What was tried, what worked, what didn't>

---

## 3. Findings Summary

### What We Learned
1. <Key insight 1>
2. <Key insight 2>
3. ...

### Risks Identified

| Risk | Likelihood | Impact | Mitigation | Persona |
|------|------------|--------|------------|---------|
| ... | ... | ... | ... | ... |

### Effort Estimate
<T-shirt size with breakdown>

---

## 4. Decision

### Recommendation: ✅ GO | ❌ NO-GO | 🔄 MORE RESEARCH

### Introspection (if --introspect) (v2.7)
<Decision reasoning and confidence factors>

### Rationale
<Why this recommendation>

### Next Steps
1. <Action 1>
2. <Action 2>

### Suggested Persona for Implementation (v2.7)
<Recommended persona for EPCI workflow>

### Open Questions
<Questions that remain unanswered>

---

## 5. Artifacts

### Throwaway Code
<Branch name — DO NOT MERGE>

### Diagrams
<Any visual artifacts>

### References
<Links to docs, APIs, etc.>
```

### 5.2 Ultra-Compressed Output (--uc)

```markdown
# SPIKE: <title>

**Question**: <question>
**Time-box**: <duration> | **Persona**: <persona>

## Findings
- ✅ <positive finding 1>
- ⚠️ <risk 1>
- ❌ <blocker 1>

## Decision: ✅ GO | ❌ NO-GO | 🔄 MORE RESEARCH

**Effort**: <T-shirt size>
**Next**: <immediate next step>
```

---

## 6. Constraints & Boundaries

### 6.1 Time-box Guidelines

| Spike Type | Recommended Time-box | Suggested Persona |
|------------|---------------------|-------------------|
| Feasibility | 30 min - 1 hour | Domain-specific |
| Comparison | 1 - 2 hours | Domain-specific |
| Estimation | 30 min - 1 hour | `--persona-architect` |
| Architecture | 2 - 4 hours | `--persona-architect` |
| Investigation | 1 - 4 hours | `--persona-backend` |

**Maximum time-box**: 4 hours

If you need more than 4 hours, either:
1. Break into multiple smaller spikes
2. This might be a project, not a spike

### 6.2 What epci-spike MUST Do

1. ✅ Start with a clear question
2. ✅ Set a strict time-box
3. ✅ Explore broadly before going deep
4. ✅ Apply persona lens if relevant (v2.7)
5. ✅ Document findings as you go
6. ✅ End with a clear decision
7. ✅ Show reasoning if `--introspect` (v2.7)
8. ✅ Suggest persona for implementation (v2.7)
9. ✅ Create next steps (GO → epci-0, NO-GO → archive)

### 6.3 What epci-spike MUST NOT Do

1. ❌ Write production-quality code
2. ❌ Merge any code to main branches
3. ❌ Exceed the time-box
4. ❌ Scope creep into implementation
5. ❌ Skip the decision step
6. ❌ Lose the learnings (always document)
7. ❌ Use production safety flags (--safe-mode, --validate) (v2.7)

---

## 7. Recovery — When Things Go Wrong

### 7.1 Time-box Expired, Question Unanswered

```
IF time runs out and you don't have an answer:
  1. STOP anyway (time-box is sacred)
  2. Document what you learned so far
  3. Decision: "MORE RESEARCH" with specific next question
  4. Schedule follow-up spike if valuable
```

### 7.2 Question Was Wrong

```
IF during exploration you realize the question was wrong:
  1. Note the original question and why it was wrong
  2. Reframe to the right question
  3. If time permits, continue with new question
  4. If not, document and schedule new spike
```

### 7.3 Scope Creep Temptation

```
IF you find yourself wanting to "just implement this real quick":
  1. STOP — this is scope creep
  2. Note it as a finding: "Implementation straightforward"
  3. Let epci-0 handle the actual implementation
  4. Your job is to DECIDE, not to BUILD
```

### 7.4 Wrong Persona Selected (v2.7)

```
IF persona doesn't match the exploration needs:
  1. Note which persona would be better
  2. Continue with adjusted focus
  3. Document persona recommendation for implementation
```

---

## 8. Integration with EPCI Workflow

### 8.1 Decision Point

```
Do you know exactly what to build?
├── YES → epci-0-briefing
└── NO  → epci-spike first
            │
            ├── GO → epci-0-briefing [with suggested persona]
            ├── NO-GO → Archive, move on
            └── MORE RESEARCH → Another spike
```

### 8.2 Spike → EPCI-0 Transition

When a spike results in GO:

```markdown
## Spike Completed: GO ✅

### Auto-generated EPCI-0 Brief

$ARGUMENTS=<EPCI_READY_BRIEF>
  FEATURE_TITLE: Google OAuth2 Integration
  FEATURE_SLUG: google-oauth2-integration
  OBJECTIVE: Replace custom authentication with Google OAuth2
  CONTEXT: 
    - Spike report: docs/spikes/spike-oauth2-google.md
    - Effort estimate: L (4-5 days)
    - Key risk: Session compatibility
  FUNCTIONAL_REQUIREMENTS:
    - [FR1] Users can sign in with Google account
    - [FR2] Existing users can link Google account
    - [FR3] Sessions remain valid during transition
  CONSTRAINTS: 
    - Must maintain backward compatibility
    - Google rate limits (implement caching)

### v2.7 Recommendations
- Suggested persona: `--persona-security` (auth feature)
- Suggested flags: `--validate` (security-critical)

→ Run: epci-0-briefing --persona-security with above brief
```

---

## 9. File Organization

### 9.1 Where to Store Spike Reports

```
docs/
├── features/           # Feature Documents (EPCI standard)
│   ├── user-auth.md
│   └── booking-flow.md
└── spikes/             # Spike Reports
    ├── spike-oauth2-google.md
    ├── spike-redis-vs-memcached.md
    └── _archive/       # Completed/rejected spikes
        └── spike-graphql-migration.md
```

### 9.2 Spike Naming Convention

```
spike-<topic>-<specific>.md

Examples:
- spike-oauth2-google.md
- spike-cache-comparison.md
- spike-i18n-effort.md
- spike-legacy-billing.md
```

---

## 10. Example — Complete Spike Session

Below is a **complete example** of an `epci-spike` session with v2.7 features.

````markdown
User: I need to know if we can add real-time notifications to our app.
The product team is asking for effort estimates.

---

# SPIKE REPORT: Real-time Notifications Feasibility

## Meta
- **Spike ID**: spike-realtime-notifications
- **Question**: Can we add real-time notifications? What's the effort?
- **Time-box**: 2 hours
- **Date**: 2025-01-15
- **Flags**: `--introspect`
- **Persona**: `--persona-backend` (auto-detected: infrastructure question)

---

## 1. Spike Definition

### Question
Can we add real-time notifications to our web app, and how long would it take?

### Success Criteria
- [ ] Identify viable technologies (WebSocket, SSE, polling)
- [ ] Assess compatibility with current stack
- [ ] Estimate effort (T-shirt size)
- [ ] List blockers and risks

### Constraints
- Must work with current Symfony backend
- Must scale to 10,000 concurrent users
- No dedicated DevOps support for new infrastructure

### Time-box
2 hours — hard stop at 16:00 UTC

### Active Configuration (v2.7)
- Flags: `--introspect`
- Persona: `--persona-backend`

---

## 2. Exploration Log

### 2.1 Technology Options

| Option | Pros | Cons |
|--------|------|------|
| WebSockets | Real-time, bi-directional | Needs dedicated server |
| Server-Sent Events (SSE) | Simple, HTTP-based | One-way only |
| Long Polling | Works everywhere | High server load |
| Mercure | Symfony native, SSE-based | New dependency |

### 2.2 Current Stack Analysis
- Symfony 6.2 — good Mercure integration
- nginx — supports WebSocket with config
- PostgreSQL — can use LISTEN/NOTIFY
- No Redis currently (would need for pub/sub)

### 2.3 Persona-specific Observations (v2.7)

> 🔧 **Backend Persona Notes:**
> - Mercure is the Symfony-native choice, reduces integration effort
> - PostgreSQL LISTEN/NOTIFY could work for small scale
> - For 10k concurrent users, need external message broker
> - Consider: Mercure Hub can be self-hosted or cloud
> - Scaling concern: WebSocket connections are stateful

### 2.4 Prototype Results
Created branch `spike/mercure-notifications` (THROWAWAY):
- ✅ Mercure Hub running locally (Docker)
- ✅ Symfony integration working (MercureBundle)
- ✅ Browser receiving SSE events
- ⚠️ Auth: Need to implement JWT for Mercure
- ❓ Scaling: Not tested beyond local

### 2.5 Effort Mapping

| Component | Estimate | Notes |
|-----------|----------|-------|
| Mercure Hub setup | 0.5 day | Docker + config |
| Symfony integration | 1 day | MercureBundle + auth |
| Notification service | 2 days | Events, queuing |
| Frontend integration | 1 day | React hooks |
| Testing | 1 day | Unit + integration |
| Load testing | 0.5 day | Verify 10k target |

---

## 3. Findings Summary

### What We Learned
1. Mercure is the cleanest option for Symfony
2. SSE (via Mercure) is simpler than WebSockets
3. Scaling to 10k will require Mercure Hub clustering
4. No Redis needed for basic implementation

### Risks Identified

| Risk | Likelihood | Impact | Mitigation | Persona |
|------|------------|--------|------------|---------|
| Mercure Hub scaling | Medium | High | Cloud option available | 🔧 Backend |
| JWT auth complexity | Low | Medium | Well-documented | |
| Browser compatibility | Low | Low | SSE widely supported | |
| Connection management | Medium | Medium | Implement heartbeat | 🔧 Backend |

### Effort Estimate

| Size | Meaning | This Spike |
|------|---------|------------|
| S | < 2 days | |
| **M** | **2-5 days** | **✓ Estimated: 6 days** |
| L | 1-2 weeks | |
| XL | > 2 weeks | |

**Confidence**: High (Mercure is well-documented, prototype worked)

---

## 4. Decision

### Recommendation: ✅ GO

### Introspection (--introspect) (v2.7)

> 🔍 **Decision Reasoning:**
> - Chose GO because: Mercure proven, effort acceptable, scales to requirements
> - Considered alternatives: WebSockets (more complex), Polling (inefficient)
> - Persona influence: Backend confirmed Symfony integration is clean
> - Confidence factors: +prototype worked, +good docs, -scaling untested
> - Key assumption: Mercure cloud option available if self-hosted doesn't scale

### Rationale
- Technical feasibility: Confirmed ✓
- Stack compatibility: Excellent (Symfony native)
- Effort: 6 days (acceptable for the feature value)
- Scaling: Achievable with cloud Mercure if needed

### Next Steps
1. Create EPCI-0 brief for notifications feature
2. Decide: self-hosted vs cloud Mercure
3. Plan: start with self-hosted, cloud as fallback

### Suggested Persona for Implementation (v2.7)
`--persona-backend` recommended (infrastructure + API focus)

### Open Questions
- What's the notification payload format?
- Which events trigger notifications?
- User preferences for notification types?

---

## 5. Artifacts

### Throwaway Code
Branch: `spike/mercure-notifications` — DO NOT MERGE

### References
- Mercure docs: https://mercure.rocks
- Symfony MercureBundle: https://symfony.com/doc/current/mercure.html
````

---

## 11. Summary

`epci-spike` is the **exploration mode** of the EPCI workflow:

- It is for **technical uncertainty** — when you don't know if/how to build something
- It is **time-boxed** — strict limits prevent analysis paralysis
- It produces **decisions**, not features — GO / NO-GO / MORE RESEARCH
- It creates **throwaway code** — prototypes are not production quality
- It **documents learnings** — findings survive even if the spike is rejected

The philosophy is **"Measure twice, cut once."**

When a spike results in GO, transition to standard EPCI workflow with the findings and recommendations.

**v2.7 improvements:**

- **Exploration flags:** `--uc`, `--verbose`, `--introspect`
- **Full persona support:** All 7 personas with auto-activation
- **Introspection output:** Decision reasoning visible with `--introspect`
- **Persona-specific observations:** Domain expert insights during exploration
- **Risk weighting by persona:** Risks tagged with relevant persona
- **Implementation recommendations:** Suggested persona for EPCI workflow
- **Explicit exclusions:** Documents why production flags are NOT available

**Design principle:**

> Spikes are about **learning**, not building. Personas and introspection enhance the learning process. Production safety flags don't apply because there's no production code.

---

## 12. Related Documentation

| Document | Purpose |
|----------|---------|
| `epci-flags.md` | Universal flags reference |
| `epci-personas.md` | Expert personas system |
| `epci-0-briefing.md` | Standard EPCI entry point (after GO decision) |
| `epci-workflow-guide.md` | Complete workflow documentation |

---

*This document is part of the EPCI v2.7 workflow system.*
