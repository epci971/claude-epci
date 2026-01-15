# Existing Skills Reference

Reference catalog of all existing EPCI skills for consistency and inspiration.

## Core Skills (5)

### epci-core
- **Category**: core
- **Purpose**: EPCI workflow, Feature Document, phases
- **Loaded by**: All commands
- **Key sections**: Workflow phases, Feature Document structure, routing

### architecture-patterns
- **Category**: core
- **Purpose**: SOLID, DDD, Clean Architecture patterns
- **Loaded by**: `/brief`, `/epci` Phase 1
- **Key sections**: Design patterns, layer separation, dependency rules

### code-conventions
- **Category**: core
- **Purpose**: Naming, formatting, code structure standards
- **Loaded by**: `/quick`, `/epci` Phase 2
- **Key sections**: Naming conventions, file organization, style guides

### testing-strategy
- **Category**: core
- **Purpose**: TDD, BDD, coverage, mocking patterns
- **Loaded by**: `/epci` Phase 2
- **Key sections**: Test pyramid, coverage targets, mocking strategies

### git-workflow
- **Category**: core
- **Purpose**: Conventional Commits, branching, PR workflow
- **Loaded by**: `/epci` Phase 3
- **Key sections**: Commit format, branch naming, PR templates

## Stack Skills (4)

### php-symfony
- **Category**: stack
- **Detection**: `composer.json` with symfony
- **Key sections**: Bundles, Services, Doctrine, PHPUnit

### javascript-react
- **Category**: stack
- **Detection**: `package.json` with react
- **Key sections**: Hooks, Components, State management, Jest/RTL

### python-django
- **Category**: stack
- **Detection**: `requirements.txt` or `pyproject.toml` with django
- **Key sections**: Models, Views, DRF, pytest

### java-springboot
- **Category**: stack
- **Detection**: `pom.xml` or `build.gradle` with spring-boot
- **Key sections**: Annotations, Beans, JPA, JUnit 5

## Factory Skills (4)

### skills-creator
- **Category**: factory
- **Purpose**: Guided skill creation
- **Invoked by**: `/epci:create skill`

### commands-creator
- **Category**: factory
- **Purpose**: Guided command creation
- **Invoked by**: `/epci:create command`

### subagents-creator
- **Category**: factory
- **Purpose**: Guided subagent creation
- **Invoked by**: `/epci:create agent`

### component-advisor
- **Category**: factory
- **Purpose**: Passive pattern detection
- **Mode**: Auto-activated on pattern detection

## Description Patterns

### Core Skills
```
[Generic capability]. Use when: [general contexts].
Not for: [exclusions].
```

### Stack Skills
```
Patterns and conventions for [Stack/Framework]. Includes [tools].
Use when: [stack] development, [detection file] detected.
Not for: [other stacks/frameworks].
```

### Factory Skills
```
[Creation/detection capability]. Use when: [trigger condition].
Not for: [other component types, modifications].
```

## Structural Patterns

### Standard Sections
1. **Overview** — 2-3 sentence description
2. **Main Content** — Domain-specific sections
3. **Quick Reference** — Tables, cheatsheets
4. **Examples** — Practical code samples
5. **Anti-patterns** — What to avoid

### Token Limits
- SKILL.md: < 5000 tokens
- Description: ≤ 1024 characters
- Name: ≤ 64 characters, kebab-case
