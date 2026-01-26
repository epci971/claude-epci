# Task File Format

> Detailed specification for task-XXX.md files.

## Overview

Each task file is a self-contained specification for a 1-2 hour work unit. It includes all information needed for independent execution.

## File Naming

```
task-{NNN}-{slug}.md

Where:
- NNN = 3-digit number (001, 002, ...)
- slug = kebab-case task identifier
```

**Examples:**
- `task-001-setup-models.md`
- `task-002-implement-services.md`
- `task-003-create-api-endpoints.md`

## YAML Frontmatter

Required fields:

```yaml
---
id: task-001                    # Unique identifier
title: Setup Database Models    # Human-readable title
slug: setup-models              # URL-friendly identifier
feature: auth-oauth             # Parent feature slug
complexity: S|M|L               # S=simple, M=medium, L=complex
estimated_minutes: 90           # 60-120 range
dependencies:                   # List of task IDs this depends on
  - task-000
files_affected:                 # Files to create or modify
  - path: src/models/user.py
    action: create
  - path: src/models/__init__.py
    action: modify
test_approach: Unit             # Unit|Integration|E2E
---
```

## Body Sections

### 1. Objective

Single paragraph explaining what this task delivers.

```markdown
## Objective

Implement the User and Profile database models with proper relationships,
field validations, and migration files. This provides the data layer
foundation for the authentication feature.
```

**Guidelines:**
- Start with action verb
- Explain "what" and "why"
- Keep to 2-3 sentences

### 2. Context

Background information relevant to this specific task.

```markdown
## Context

The authentication system requires User and Profile models as defined
in the brief. The User model handles authentication while Profile
stores additional user data (avatar, preferences).

Key decisions from specification:
- Email-based authentication (not username)
- Soft delete for GDPR compliance
- Profile is optional (created on first edit)
```

**Guidelines:**
- Reference decisions from source brief
- Mention architectural constraints
- Keep focused on this task

### 3. Acceptance Criteria

Testable conditions that define "done".

```markdown
## Acceptance Criteria

### AC1: User Model Fields
- **Given**: A new User instance
- **When**: All required fields are provided
- **Then**: The user is saved with:
  - email (unique, indexed)
  - password_hash (not plain text)
  - created_at (auto-set)
  - is_active (default true)

### AC2: Profile Relationship
- **Given**: An existing User
- **When**: A Profile is created
- **Then**: The Profile links to User via foreign key

### AC3: Soft Delete
- **Given**: A User marked for deletion
- **When**: delete() is called
- **Then**: User.deleted_at is set (not physically deleted)
```

**Formats Accepted:**
- Given-When-Then (preferred)
- Checkbox list
- Table format

**Minimum:** 2 acceptance criteria per task

### 4. Steps

Atomic execution units (15-30 minutes each).

```markdown
## Steps

### Step 1: Create User Model (20 min)

**Input**: Model specifications from brief

**Actions**:
1. Create `src/models/user.py`
2. Define User class with fields:
   - id (UUID, primary key)
   - email (string, unique, indexed)
   - password_hash (string)
   - is_active (boolean, default=True)
   - created_at (datetime, auto)
   - updated_at (datetime, auto)
   - deleted_at (datetime, nullable)
3. Add `__str__` method returning email
4. Add soft_delete() method

**Output**: User model file created

**Validation**:
- Model can be instantiated
- All fields accessible
```

**Step Structure:**
- Title with duration
- Input requirements
- Numbered actions
- Output deliverable
- Validation criteria

### 5. Files

Table of files affected.

```markdown
## Files

| Path | Action | Description |
|------|--------|-------------|
| `src/models/user.py` | create | User model class |
| `src/models/profile.py` | create | Profile model class |
| `src/models/__init__.py` | modify | Export models |
| `migrations/001_users.py` | create | Database migration |
```

**Actions:**
- `create` — New file
- `modify` — Change existing
- `delete` — Remove file (rare)

### 6. Test Approach

Testing strategy for this task.

```markdown
## Test Approach

- **Type**: Unit
- **Framework**: pytest
- **Location**: tests/models/test_user.py
- **Coverage Target**: 90%

### Test Cases

| # | Description | Type | Priority |
|---|-------------|------|----------|
| 1 | User creation with valid data | Unit | High |
| 2 | Email uniqueness constraint | Unit | High |
| 3 | Password is hashed on save | Unit | High |
| 4 | Soft delete sets deleted_at | Unit | Medium |
| 5 | Profile cascades on user delete | Unit | Medium |
```

### 7. Dependencies

Relationship to other tasks.

```markdown
## Dependencies

### Requires (blockedBy)
- **task-000**: Project setup must be complete

### Blocks (blocks)
- **task-002**: Services layer needs these models
- **task-003**: API endpoints need these models
```

### 8. Notes (optional)

Additional context, warnings, or considerations.

```markdown
## Notes

- Consider adding database indexes for email lookups
- Password hashing uses bcrypt (see project conventions)
- Migration should be reversible
- TODO: Add audit logging in future task
```

## Complete Example

See [examples/task-example.md](examples/task-example.md) for a complete task file.

## Validation Checklist

Before generating:

- [ ] ID is unique within feature
- [ ] Title is action-oriented
- [ ] Estimated minutes in 60-120 range
- [ ] Dependencies reference valid task IDs
- [ ] At least 2 acceptance criteria
- [ ] Steps are 15-30 minutes each
- [ ] Test approach defined
- [ ] Files table complete

## Anti-Patterns

| Anti-Pattern | Problem | Fix |
|--------------|---------|-----|
| Vague objective | Unclear deliverable | Be specific |
| No acceptance criteria | Can't verify completion | Add Given-When-Then |
| Steps too large | Not atomic | Split into smaller steps |
| Missing dependencies | Incorrect execution order | Analyze prerequisites |
| No test approach | Quality gap | Define test strategy |
