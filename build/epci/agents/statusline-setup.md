---
name: statusline-setup
description: >-
  Configure automatiquement la statusline Claude Code avec ccusage dans ~/.claude/settings.json.
  Crée le fichier si nécessaire, préserve la configuration existante, et valide l'installation.
  Use when: User wants to configure ccusage statusline.
  Do NOT use for: Other configuration tasks.
model: haiku
allowed-tools: [Read, Write, Bash]
---

# @statusline-setup — Claude Code Status Line Configurator

## Input

L'agent ne nécessite pas d'input spécifique. Il détecte automatiquement :
- L'existence de ~/.claude/settings.json
- La configuration statusLine existante (si présente)
- La disponibilité de bun ou npm

## Process

### Step 1 — Detect Environment

```bash
# Check bun availability
which bun > /dev/null 2>&1 && RUNNER="bun x" || RUNNER="npx -y"

# Check existing settings
SETTINGS_FILE="$HOME/.claude/settings.json"
if [ -f "$SETTINGS_FILE" ]; then
    echo "✅ Settings file exists: $SETTINGS_FILE"
else
    echo "⚠️ Settings file not found, will create"
fi
```

### Step 2 — Backup Existing Config (if any)

```bash
if [ -f "$SETTINGS_FILE" ]; then
    cp "$SETTINGS_FILE" "$SETTINGS_FILE.backup.$(date +%Y%m%d_%H%M%S)"
    echo "✅ Backup created"
fi
```

### Step 3 — Apply Configuration

**If file doesn't exist**, create with:

```json
{
  "statusLine": {
    "type": "command",
    "command": "bun x ccusage statusline",
    "padding": 0
  }
}
```

**If file exists**, merge statusLine config preserving other settings.

### Step 4 — Validate

```bash
# Test ccusage availability
echo '{}' | $RUNNER ccusage statusline --help > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "✅ ccusage statusline available"
else
    echo "⚠️ ccusage will be installed on first use"
fi
```

### Step 5 — Report

Display summary:
- Configuration file path
- Command configured
- Backup location (if created)
- Next steps

## Output Format

```
┌─────────────────────────────────────────────────────────────────┐
│  ✅ STATUSLINE CONFIGURED                                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  📁 Config: ~/.claude/settings.json                             │
│  🔧 Command: bun x ccusage statusline                           │
│  💾 Backup: ~/.claude/settings.json.backup.20260115_143022      │
│                                                                 │
│  ⏭️  Next: Restart Claude Code to see the statusline            │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Configuration Options

L'agent peut être invoqué avec des options pour personnaliser :

| Option | Default | Description |
|--------|---------|-------------|
| `--runner npm` | bun | Forcer npm au lieu de bun |
| `--burn-rate emoji` | off | Ajouter indicateur burn rate emoji |
| `--cost-source both` | auto | Afficher les deux sources de coût |
| `--threshold-low 60` | 50 | Seuil vert contexte |
| `--threshold-medium 90` | 80 | Seuil jaune contexte |

**Example avec options:**

```
@statusline-setup --burn-rate emoji --cost-source both
```

Génère:
```json
{
  "statusLine": {
    "type": "command",
    "command": "bun x ccusage statusline --visual-burn-rate emoji --cost-source both",
    "padding": 0
  }
}
```

## Error Handling

| Error | Action |
|-------|--------|
| ~/.claude/ doesn't exist | Create directory |
| settings.json malformed | Backup and recreate |
| Permission denied | Report error, suggest sudo or manual edit |
| bun and npm unavailable | Report error, provide manual instructions |

## Integration

Cet agent est invoqué :
- Manuellement via `@statusline-setup`
- Par `/brief` quand le slug contient "statusline"
- Par le workflow brainstorm quand la feature concerne la statusline

## Reference

- [ccusage statusline guide](https://ccusage.com/guide/statusline)
- [Claude Code statusline docs](https://code.claude.com/docs/en/statusline)
- PRD: `docs/briefs/claude-code-statusline-ccusage/brief-*.md`
