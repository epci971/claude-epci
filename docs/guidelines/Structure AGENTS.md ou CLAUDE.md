Below is a **precise, complete plan** for your global `AGENTS.md`, written so you can:

- give the **outline itself** to Claude,
    
- plus a short set of meta-instructions like:  
    “Fill every section of this plan, strictly following the constraints and data sources described.”
    

Everything is in **English**, multi-LLM compatible, with a **preference for Claude Code**, and designed to stay within **2–5k tokens when filled**.

---

# 📘 Global `AGENTS.md` — Full Structural Plan for Claude

> **Meta-instruction to Claude (you can prepend this):**  
> “You are given this structural plan for `AGENTS.md`. Analyze the repository and fully populate each section.  
> Never invent anything that is not supported by the code or documentation. Always indicate your sources (files/paths).  
> Respect all constraints and anti-hallucination rules explicitly listed below.”

---

## 0. File Meta-Rules (applies to entire `AGENTS.md`)

Claude must respect these global rules when filling any section:

- **Sources:**
    
    - For every non-trivial statement, mention the **exact file(s)** used (`path`, optionally line ranges).
        
    - If something is not found, write explicitly: `Not found in repository` (do not guess).
        
- **No hallucination:**
    
    - Do not invent technologies, commands, endpoints, or workflows.
        
    - Only describe what is **actually present** in the repository.
        
- **Brevity & priority:**
    
    - Target **2–5k tokens total**.
        
    - Prioritize: stack, layout, commands, conventions, workflows, agent rules, and security.
        
    - Use bullet lists and tables over long paragraphs.
        
- **Tone and style:**
    
    - Technical, concise, neutral.
        
    - Markdown only (no HTML).
        
- **Secrets & sensitive data:**
    
    - Never print actual secrets, tokens, passwords, keys.
        
    - Use placeholders instead (e.g. `<API_KEY>`).
        
    - If real secrets are detected, state the risk and the file path, **without** copying the value.
        

---

## 1. Project Context

### 1.1 Project Identity

**Goal:** give Claude/Codex/Gemini a short, accurate picture of what this repo does.

Claude must:

- Derive from: `README.md`, main package manifest(s), root folder names, high-level docs.
    
- Fill:
    
    - **Project name**
        
    - **Short description (1–3 sentences)**
        
    - **Main purpose / domain** (e.g. “tax collection for tourism”, “B2B marketplace backend”)
        
    - **Primary user types / actors** (humans + external systems, if identifiable)
        
- Add a line:  
    `Sources: ...`
    

### 1.2 Main Business Flows / Use Cases

Claude must:

- Infer **3–7 key business flows** or use cases from:
    
    - controllers / views / endpoints,
        
    - UI routes,
        
    - domain services,
        
    - documentation.
        
- For each:
    
    - **Name** (e.g. `Create booking`, `Export tax report`)
        
    - **Short description** (what it achieves)
        
    - **Key entry points** (main endpoints/routes/components)
        
    - `Sources: ...`
        

Represent as a **table**:

| Flow | Description | Entry points | Sources |

If not inferable, write a short note: “Business flows not clearly identifiable in codebase.”

---

## 2. Technical Stack

**Goal:** give a precise, non-hallucinated view of backend, frontend, infra, and integrations.

Claude must inspect:

- `composer.json`, `package.json`, `pyproject.toml`, `requirements.txt`, `Pipfile`, etc.
    
- `Dockerfile`, `docker-compose.yml`, `Makefile`, CI configs.
    
- `config/`, `.github/workflows/`, `.gitlab-ci.yml`, `azure-pipelines.yml`, etc.
    

### 2.1 Backend

Fields:

- **Language(s)** (e.g. `PHP 8.2`, `Python 3.12`)
    
- **Main framework(s)** (Symfony, Django, etc.)
    
- **ORM / query tools** (Doctrine, Eloquent, Prisma…)
    
- **Key backend libraries** (auth, HTTP clients, logging…)
    
- `Sources: ...`
    

### 2.2 Frontend

Fields:

- **Framework(s)** (React, Vue, Next, etc.)
    
- **Build / bundler** (Vite, Webpack…)
    
- **Routing** (React Router, Next router, etc.)
    
- **State management** (Redux, Zustand, Context API, etc.)
    
- `Sources: ...`
    

### 2.3 Infrastructure & Operations

Fields:

- **Database(s)** (PostgreSQL, MySQL, etc.)
    
- **Cache / queue / messaging** (Redis, RabbitMQ, etc.)
    
- **Containerization** (Docker yes/no, main images)
    
- **CI/CD** (GitHub Actions, GitLab CI, etc. + main pipelines names)
    
- `Sources: ...`
    

### 2.4 External Integrations

Fields:

- **APIs & services** (e.g. Stripe, SendGrid, GeoApify…)
    
- **Auth / SSO** providers (Keycloak, Auth0, OAuth…)
    
- For each: short description + main files using it.
    
- `Sources: ...`
    

---

## 3. Codebase Layout & Domains

**Goal:** allow any agent to quickly understand the project structure.

Claude must:

- Scan top-level directories and key subfolders.
    
- Identify **modules / bounded contexts / domains**.
    

### 3.1 High-Level Directory Tree (condensed)

Provide a small, relevant tree:

```text
apps/
src/
  Domain/
  Application/
  Infrastructure/
frontend/
config/
tests/
docs/
...
```

Only include folders relevant to development (exclude `vendor/`, `node_modules/`, build artifacts).

### 3.2 Modules / Domains Table

For each **module/domain** (up to ~10):

- **Name** (e.g. `Tax`, `Booking`, `User`, `Reporting`)
    
- **Responsibilities / scope**
    
- **Key directories / namespaces**
    
- `Sources: ...`
    

Table:

| Module / Domain | Responsibilities | Key Paths / Namespaces | Sources |

---

## 4. Canonical Commands

**Goal:** list only the real entry points (dev, build, tests, lint, migrations…).

Claude must:

- Extract from `package.json` `"scripts"`, `composer.json` `"scripts"`, `Makefile`, CI jobs, etc.
    
- **Never invent** commands or flags.
    

For each command:

- **Purpose** (dev server, test suite, lint, build, static analysis, etc.)
    
- **Exact command** (as used in code)
    
- **Source file** where it comes from.
    

Table:

|Purpose|Command|Source|Notes|
|---|---|---|---|
|Dev server|`npm run dev`|`package.json`||
|Run tests|`php bin/phpunit`|`Makefile`||
|Lint frontend|`npm run lint`|`package.json`||
|DB migrations|`php bin/console ...`|`composer.json`||

---

## 5. Global Conventions & Patterns

**Goal:** give agents a clear set of conventions they must respect.

### 5.1 Coding & Naming Conventions

Claude must search for any explicit conventions in:

- `CONTRIBUTING.md`, `README.md`
    
- `docs/`, `coding-style.md`, `.php-cs-fixer.dist.php`, ESLint/Prettier configs, etc.
    

Fields (if available):

- **Naming conventions** (classes, methods, variables)
    
- **Directory structure rules**
    
- **Commit message conventions**
    
- **Branch naming** (if documented)
    
- **Formatting / linting standards** (PSR-12, Prettier, ESLint rules…)
    
- `Sources: ...`
    

If not documented, say so: “No explicit coding conventions found; follow existing patterns in code.”

### 5.2 Golden Rules (Global, Always Present)

These rules must be reproduced as-is (or very close), as they apply to **all tools and agents**:

1. Do not invent commands, endpoints, or files. Always verify in the repository.
    
2. Before introducing a new pattern, search the codebase and reuse existing patterns when possible.
    
3. Never remove tests or validations unless explicitly requested and justified.
    
4. When something is unclear, explain your assumptions and/or ask clarification questions.
    
5. Never log or expose secrets (passwords, API keys, tokens, private keys).
    
6. Prefer small, incremental changes over massive refactors in one step.
    
7. For every non-trivial statement, specify the source file(s) used.
    

---

## 6. Secrets & Security

**Goal:** set expectations for security and secret handling across all agents.

Claude must:

- Scan for typical secret locations (`.env`, `config/`, CI secrets references, etc.).
    
- **Never** print actual secret values.
    

Sections:

### 6.1 Secret Handling Rules

- Do not display contents of `.env` or secret vaults.
    
- Replace any sensitive example by placeholders (`<SECRET_VALUE>`, `<API_TOKEN>`).
    
- If hardcoded secrets are detected, mention:
    
    - file path,
        
    - type of secret,
        
    - a short warning.
        

### 6.2 Security Concerns (if detectable)

- Mention:
    
    - Presence of HTTP endpoints without auth (if obvious).
        
    - Known security middlewares (CORS, CSRF, rate limiting, etc.).
        
    - Security libraries used.
        
- `Sources: ...`
    

If nothing is obvious, simply state: “No explicit security configuration detected; agents must be cautious and avoid introducing vulnerabilities.”

---

## 7. Multi-LLM Usage Guidelines

**Goal:** explain how this `AGENTS.md` should be used by different tools.

Claude should fill:

### 7.1 Claude Code

- Role of `AGENTS.md` as **main rule + context file**.
    
- Priority reading order:
    
    1. Golden Rules & Secrets
        
    2. Stack & Layout
        
    3. Canonical Commands
        
    4. Agent Roles & Pipelines (if present)
        
- Reminder:
    
    - No code generation before plan approval.
        
    - Must respect this file over any generic coding intuition.
        

### 7.2 Codex CLI

- How Codex should use this file:
    
    - As rulebook + project map.
        
    - To understand commands, entry points, and conventions before running actions.
        

### 7.3 Gemini CLI

- How Gemini should use it:
    
    - For high-level understanding, documentation, and summarization tasks.
        
    - Focus on sections: Context, Stack, Layout, Commands, Patterns.
        

If some tools are not used, Claude can state: “Tool X not detected / not configured in this project.”

---

## 8. Local Agents (If Any)

**Goal:** document Orchestrator/Architector/etc. if this repo defines them.

Claude must:

- Look for local agent files: e.g. `ORCHESTRATOR.md`, `.cursor/rules/`, `agents/`, `docs/agents/`, etc.
    

If found, create a table:

|Agent Name|Role Summary|Mode (Thinking/Execution)|Scope / Responsibilities|Source|
|---|---|---|---|---|
|Orchestrator|Functional planning & scoping|Thinking|Features, roadmap, value, dependencies...|...|
|Architector|Technical backlog per feature|Thinking|Tasks, diagrams, complexity, risks...|...|
|Editor|Pure execution of backlogs|Execution|Code diffs, tests, lint, etc.|...|
|...|||||

If no local agent files exist:  
“Project does not define local agents; use only global rules from this AGENTS.md.”

---

## 9. Standard Workflow / Pipeline

**Goal:** describe how work should flow between “thinking” and “execution” phases.

Claude should:

- Prefer project-specific workflows if documented (CI, docs, etc.).
    
- Otherwise fall back to this generic workflow (you can lock this as default):
    

|Phase|Name|Description|Typical Agent(s)|User Validation|
|---|---|---|---|---|
|0|Explore|Analyze context, locate files & patterns|Any (Thinking)|No|
|1|Plan|Propose structured plan / backlog|Orchestrator / Architector|Yes|
|2|Critique|Check coherence, risks, missing pieces|Any (Thinking)|No|
|3|Suggest|Suggest improvements / alternatives|Any (Thinking)|Optional|
|4|Execute|Apply approved plan (code changes)|Editor|Yes|
|5|Test|Run tests / checks, analyze failures|Debuggor / Editor|Yes/No|
|6|Refine|Refactor, improve quality|Refactorizor|Optional|
|7|Document|Generate / update documentation|Documentor|Yes|

Claude must briefly describe:

- When to **ask questions**.
    
- When to **stop and wait** for explicit user approval.
    
- What is **forbidden** (e.g. no direct Execute without Plan validation).
    

---

## 10. Expected Deliverables (Per Phase / Agent)

**Goal:** standardize what agents should output.

Claude must list, for this project:

- **Planning outputs:**
    
    - Feature tables, backlogs, matrices, diagrams (if relevant).
        
- **Execution outputs:**
    
    - Code diffs, file lists, brief rationale.
        
- **Debugging outputs:**
    
    - Error analysis, root cause, correction plan.
        
- **Refactoring outputs:**
    
    - Technical debt list, refactor plan, impacted files.
        
- **Documentation outputs:**
    
    - Markdown structure, diagrams, API descriptions.
        

For each type, mention:

- **Format** (Markdown table, diff, Mermaid diagram, etc.).
    
- **Constraints** (self-contained, references to files, no secrets).
    

---

## 11. Iteration & Validation Rules

Claude must restate **project-wide iteration rules** that every agent must follow:

- Each non-trivial output must include:
    
    - A short **critique** (what might be wrong / incomplete).
        
    - A **clarity score** (e.g. /10).
        
    - **Improvement suggestions**.
        
- Agents must **not**:
    
    - Skip from problem directly to code without a plan, except for very trivial tweaks.
        
    - Modify files outside the agreed scope.
        
- User interaction:
    
    - On planning / refactor proposals → wait for **explicit approval** (“OK”, “approved”, etc.).
        
    - On code diffs → always present a **summary** before applying.
        

---

## 12. Special Commands / Modes (If Relevant)

If your toolchain (Claude/Codex/Gemini or editor integration) supports commands / flags, list them here:

- `mode light` / `mode full`
    
- `focus backend` / `focus frontend` / `focus tests`
    
- `rollback <phase>`
    
- `export markdown`
    
- `export diff`
    
- `analysis-depth=N`
    

If there is no command system, Claude should simply say:  
“No explicit command system; user interacts through natural language instructions.”

---

## 13. Source Attribution Summary

At the end of `AGENTS.md`, Claude must add a compact summary:

- **Files scanned / referenced** (grouped by type: config, backend, frontend, docs, CI).
    
- **Sections that could not be populated** because of missing information.
    
- Any **potential inconsistencies** detected (e.g. `AGENTS.md` vs. actual scripts).
    

Example:

```markdown
## Source Attribution Summary

- Config: composer.json, package.json, docker-compose.yml
- Backend: src/Controller/*, src/Domain/*
- Frontend: frontend/src/*
- Docs: README.md, docs/*
- CI: .github/workflows/*.yml

Missing:
- No explicit coding-style or CONTRIBUTING docs found.
- No documented branch naming convention.
```

---

If you want, next step can be:

- I turn this **plan** into a **concise “instruction block” for Claude** (e.g. “You must fill sections 1–13 as follows…”) so you can just paste it once into Claude Code as a reusable system prompt for generating `AGENTS.md` on any repo.