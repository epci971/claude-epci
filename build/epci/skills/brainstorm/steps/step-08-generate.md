# Step 08: Generate

> Write brief and journal files to disk.

## Trigger

- Previous step: `step-07-validate.md` completed
- Or: `--quick` mode skipped validation

## Inputs

| Input | Source | Required |
|-------|--------|----------|
| `brief_final` | From step-07 (or brief_v0 if quick) | Yes |
| `ems` | Session state | Yes |
| `decisions[]` | Session state | Yes |
| `open_threads[]` | Session state | No |
| `techniques_applied` | Session state | No |
| `edit_history` | From step-07 | No |
| `security_audit` | From step-06 | No |
| `--quick` flag | From step-00 | No |

## Protocol

### 1. Generate Slug and Paths

```python
slug = slugify(idea_refined)  # e.g., "auth-oauth-integration"
date = datetime.now().strftime("%Y%m%d")

output_dir = f"docs/briefs/{slug}/"
brief_path = f"{output_dir}brief-{slug}-{date}.md"
journal_path = f"{output_dir}journal-{slug}-{date}.md"
```

### 2. Create Output Directory

```bash
mkdir -p docs/briefs/{slug}/
```

### 3. Generate Brief (PRD v3.0 Format)

Apply template from [references/brief-format.md](../references/brief-format.md):
- Populate all sections with session data (EMS, decisions, scope)
- Include complexity routing from step-06
- Inject security audit recommendations if available
- Write to: `{brief_path}`

### 4. Write Brief File

```python
Write(brief_path, brief_content)
```

### 5. Generate Journal

Apply template from [references/journal-format.md](../references/journal-format.md):
- Populate iteration history with all EMS progression data
- Include all decisions, open threads, and persona switches
- Add techniques applied and phase transitions
- Write to: `{journal_path}`

### 6. Write Journal File

```python
Write(journal_path, journal_content)
```

### 7. Update Session State

```json
{
  "generation_complete": true,
  "output_files": [
    "{brief_path}",
{journal_path}
  ],
  "slug": "{slug}"
}
```

## Outputs

| Output | Destination |
|--------|-------------|
| `brief-{slug}-{date}.md` | `docs/briefs/{slug}/` |
| `journal-{slug}-{date}.md` | `docs/briefs/{slug}/` |
| `generation_complete` | Session state |
| `output_files` | Session state |

## Next Step

→ `step-09-report.md`

## Error Handling

| Error | Resolution |
|-------|------------|
| Directory creation fails | Try alternative path |
| Write permission denied | Warn user, output to console |
| File already exists | Add suffix (-v2, -v3) |
