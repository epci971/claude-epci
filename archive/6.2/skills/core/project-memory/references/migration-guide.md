# Migration Guide: v5 to v6

Guide for migrating project-memory data from EPCI v5 to v6.

## Overview

| Aspect | v5 | v6 |
|--------|----|----|
| Base path | `.epci/memory/` | `.claude/state/memory/` |
| Integration | Standalone | Aligned with state-manager |
| Schema version | None | "1.0" |
| Confidence tracking | No | Yes |
| Features storage | `.epci/memory/features/` | `.claude/state/memory/features/` |

---

## Path Mapping

### Directory Structure

| v5 Path | v6 Path |
|---------|---------|
| `.epci/` | `.claude/state/` |
| `.epci/memory/` | `.claude/state/memory/` |
| `.epci/memory/patterns.json` | `.claude/state/memory/patterns.json` |
| `.epci/memory/preferences.json` | `.claude/state/memory/preferences.json` |
| `.epci/memory/velocity.json` | `.claude/state/memory/velocity.json` |
| `.epci/memory/bugs.json` | `.claude/state/memory/bugs.json` |
| `.epci/memory/features/{slug}.json` | `.claude/state/memory/features/{slug}.json` |
| `.epci/features/<slug>/state.json` | `.claude/state/features/<slug>/state.json` (state-manager) |

---

## Automatic Migration

Migration runs automatically on first `init()` call when v5 data exists.

### Detection

```
if exists(".epci/memory/") and not exists(".claude/state/memory/"):
    run_migration()
```

### Process

1. **Create v6 directory structure**
   ```
   mkdir -p .claude/state/memory/features/
   ```

2. **Migrate patterns.json**
   - Add `version: "1.0"` field
   - Add `confidence` to each pattern (default: 0.7)
   - Copy examples if present

3. **Migrate preferences.json**
   - Add `version: "1.0"` field
   - Wrap values in confidence objects
   - Set default confidence: 0.7, observations: 3

4. **Migrate velocity.json**
   - Add `version: "1.0"` field
   - Rename complexity keys to UPPERCASE
   - Calculate missing fields (accuracy, adjustment_factor)

5. **Migrate bugs.json**
   - Add `version: "1.0"` field
   - Ensure all required fields present
   - Add `created_at` if missing (use file mtime)

6. **Migrate features/**
   - Copy each feature file
   - Add `version: "1.0"` field
   - Ensure schema compliance

7. **Create backup**
   ```
   mv .epci/memory/ .epci/memory.backup.{timestamp}/
   ```

---

## Manual Migration

If automatic migration fails or you need fine control:

### Step 1: Create v6 Structure

```bash
mkdir -p .claude/state/memory/features
```

### Step 2: Migrate patterns.json

**v5 format:**
```json
{
  "api_style": "REST",
  "error_handling": "try-catch",
  "naming": {
    "files": "kebab-case",
    "functions": "camelCase"
  }
}
```

**v6 format:**
```json
{
  "version": "1.0",
  "last_scan": "2026-01-22T10:00:00Z",
  "patterns": {
    "api_style": {
      "type": "REST",
      "confidence": 0.85,
      "examples": []
    },
    "error_handling": {
      "pattern": "try-catch",
      "confidence": 0.80
    },
    "naming": {
      "files": "kebab-case",
      "functions": "camelCase",
      "confidence": 0.90
    }
  }
}
```

### Step 3: Migrate preferences.json

**v5 format:**
```json
{
  "workflow": {
    "tdd_preference": "guided",
    "verbosity": "concise"
  },
  "technical": {
    "test_framework": "vitest"
  }
}
```

**v6 format:**
```json
{
  "version": "1.0",
  "last_update": "2026-01-22T14:30:00Z",
  "workflow": {
    "tdd_preference": {
      "value": "guided",
      "confidence": 0.75,
      "observations": 5
    },
    "verbosity": {
      "value": "concise",
      "confidence": 0.70,
      "observations": 3
    }
  },
  "technical": {
    "test_framework": {
      "value": "vitest",
      "confidence": 0.85,
      "observations": 7
    }
  }
}
```

### Step 4: Migrate velocity.json

**v5 format:**
```json
{
  "tiny": { "estimated_avg": 30, "actual_avg": 25 },
  "small": { "estimated_avg": 120, "actual_avg": 135 }
}
```

**v6 format:**
```json
{
  "version": "1.0",
  "last_update": "2026-01-22T16:00:00Z",
  "total_samples": 10,
  "calibration": {
    "TINY": {
      "estimated_avg": 30,
      "actual_avg": 25,
      "sample_count": 5,
      "accuracy": 0.83,
      "adjustment_factor": 0.83
    },
    "SMALL": {
      "estimated_avg": 120,
      "actual_avg": 135,
      "sample_count": 5,
      "accuracy": 0.89,
      "adjustment_factor": 1.13
    }
  }
}
```

**Calculation:**
```
accuracy = 1 - abs(estimated - actual) / estimated
adjustment_factor = actual / estimated
```

### Step 5: Migrate bugs.json

**v5 format:**
```json
{
  "bugs": [
    {
      "id": "oauth-fix",
      "description": "OAuth redirect issue",
      "fix": "Updated redirect URI"
    }
  ]
}
```

**v6 format:**
```json
{
  "version": "1.0",
  "last_update": "2026-01-22T11:00:00Z",
  "bugs": [
    {
      "id": "oauth-fix",
      "created_at": "2026-01-20T14:00:00Z",
      "description": "OAuth redirect issue",
      "root_cause": "Redirect URI mismatch",
      "fix_summary": "Updated redirect URI",
      "keywords": ["oauth", "redirect"],
      "category": "integration"
    }
  ]
}
```

### Step 6: Migrate Feature Files

For each file in `.epci/memory/features/`:

**v5 format:**
```json
{
  "slug": "auth-oauth",
  "summary": "OAuth implementation",
  "duration": 180,
  "files": ["src/auth.ts"]
}
```

**v6 format:**
```json
{
  "version": "1.0",
  "slug": "auth-oauth",
  "created_at": "2026-01-20T10:00:00Z",
  "completed_at": "2026-01-22T15:30:00Z",
  "summary": "OAuth implementation",
  "complexity": "STANDARD",
  "duration_minutes": 180,
  "estimated_minutes": 180,
  "keywords": ["auth", "oauth"],
  "files_modified": ["src/auth.ts"],
  "test_count": 0,
  "decisions": [],
  "learnings": []
}
```

### Step 7: Backup and Clean

```bash
# Backup v5 data
mv .epci/memory/ .epci/memory.backup.$(date +%Y%m%d)/

# Verify v6 data
ls -la .claude/state/memory/
cat .claude/state/memory/patterns.json | python -m json.tool

# Remove backup after verification (optional)
rm -rf .epci/memory.backup.*
```

---

## Migration Script

Quick migration using jq:

```bash
#!/bin/bash
# migrate-memory.sh

V5_PATH=".epci/memory"
V6_PATH=".claude/state/memory"
TIMESTAMP=$(date -Iseconds)

# Create v6 structure
mkdir -p "$V6_PATH/features"

# Migrate patterns.json
if [ -f "$V5_PATH/patterns.json" ]; then
  jq '{
    version: "1.0",
    last_scan: $timestamp,
    patterns: (. | to_entries | map({
      key: .key,
      value: (if type == "object" then . + {confidence: 0.75} else {type: ., confidence: 0.75} end)
    }) | from_entries)
  }' --arg timestamp "$TIMESTAMP" "$V5_PATH/patterns.json" > "$V6_PATH/patterns.json"
fi

# Migrate preferences.json
if [ -f "$V5_PATH/preferences.json" ]; then
  jq '{
    version: "1.0",
    last_update: $timestamp,
    workflow: (.workflow // {} | to_entries | map({
      key: .key,
      value: {value: .value, confidence: 0.75, observations: 3}
    }) | from_entries),
    technical: (.technical // {} | to_entries | map({
      key: .key,
      value: {value: .value, confidence: 0.75, observations: 3}
    }) | from_entries)
  }' --arg timestamp "$TIMESTAMP" "$V5_PATH/preferences.json" > "$V6_PATH/preferences.json"
fi

# Migrate velocity.json
if [ -f "$V5_PATH/velocity.json" ]; then
  jq '{
    version: "1.0",
    last_update: $timestamp,
    calibration: (to_entries | map({
      key: (.key | ascii_upcase),
      value: (.value + {
        sample_count: 5,
        accuracy: (1 - (((.value.estimated_avg - .value.actual_avg) | fabs) / .value.estimated_avg)),
        adjustment_factor: (.value.actual_avg / .value.estimated_avg)
      })
    }) | from_entries)
  }' --arg timestamp "$TIMESTAMP" "$V5_PATH/velocity.json" > "$V6_PATH/velocity.json"
fi

# Migrate bugs.json
if [ -f "$V5_PATH/bugs.json" ]; then
  jq '{
    version: "1.0",
    last_update: $timestamp,
    bugs: [.bugs[] | . + {
      created_at: ($timestamp),
      root_cause: (.root_cause // "Unknown"),
      fix_summary: (.fix // .fix_summary // ""),
      keywords: (.keywords // []),
      category: (.category // "logic")
    }]
  }' --arg timestamp "$TIMESTAMP" "$V5_PATH/bugs.json" > "$V6_PATH/bugs.json"
fi

# Migrate feature files
if [ -d "$V5_PATH/features" ]; then
  for file in "$V5_PATH/features"/*.json; do
    [ -f "$file" ] || continue
    basename=$(basename "$file")
    jq '. + {
      version: "1.0",
      created_at: (.created_at // $timestamp),
      completed_at: (.completed_at // $timestamp),
      complexity: (.complexity // "STANDARD"),
      duration_minutes: (.duration_minutes // .duration // 0),
      estimated_minutes: (.estimated_minutes // .duration // 0),
      keywords: (.keywords // []),
      files_modified: (.files_modified // .files // []),
      test_count: (.test_count // 0),
      decisions: (.decisions // []),
      learnings: (.learnings // [])
    }' --arg timestamp "$TIMESTAMP" "$file" > "$V6_PATH/features/$basename"
  done
fi

# Backup v5
mv "$V5_PATH" "${V5_PATH}.backup.$(date +%Y%m%d)"

echo "Migration complete. Backup at ${V5_PATH}.backup.$(date +%Y%m%d)"
```

---

## Rollback

If migration causes issues:

### Restore from Backup

```bash
# Remove failed v6 migration
rm -rf .claude/state/memory/

# Restore v5 backup
mv .epci/memory.backup.{date}/ .epci/memory/
```

### Re-run Migration

After fixing issues:

```bash
# Remove partial v6 data
rm -rf .claude/state/memory/

# Run migration again
./migrate-memory.sh
```

---

## Verification

After migration, verify data integrity:

### Check File Structure

```bash
tree .claude/state/memory/
# Expected:
# .claude/state/memory/
# ├── patterns.json
# ├── preferences.json
# ├── velocity.json
# ├── bugs.json
# └── features/
#     └── *.json
```

### Validate JSON

```bash
for file in .claude/state/memory/*.json; do
  echo "Validating $file"
  python -m json.tool "$file" > /dev/null && echo "  OK" || echo "  FAILED"
done
```

### Check Schema Compliance

```bash
# Check version field exists
for file in .claude/state/memory/*.json; do
  version=$(jq -r '.version // "MISSING"' "$file")
  echo "$file: version=$version"
done
```

---

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| JSON parse error | Corrupted v5 file | Manually fix JSON syntax |
| Missing fields | Incomplete v5 data | Add defaults during migration |
| Wrong path | Old config | Update all path references |
| Duplicate data | Partial migration | Remove v6, restore backup, retry |

---

## Post-Migration

1. **Update .gitignore** (if not already):
   ```
   .claude/state/
   ```

2. **Remove old path from .gitignore**:
   ```
   # Remove: .epci/
   ```

3. **Delete backup after verification**:
   ```bash
   rm -rf .epci/memory.backup.*
   ```

4. **Test memory functions**:
   - Run `init()` and verify no errors
   - Check `get_patterns()` returns data
   - Verify `recall_features()` finds old features
