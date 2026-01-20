# Brainstorm Flags Reference

> Reference complete des flags disponibles pour la commande `/brainstorm`.

---

## Core Flags

| Flag | Effet |
|------|-------|
| `--template [name]` | Forcer template (feature/problem/decision) |
| `--no-hmw` | Desactiver HMW |
| `--quick` | 3 iter max, skip validation |
| `--turbo` | Mode turbo (voir turbo-mode.md) |
| `--no-security` | Desactiver @security-auditor auto |
| `--no-plan` | Desactiver @planner auto |
| `--no-technique` | Desactiver auto-suggestion techniques |
| `--no-clarify` | Desactiver clarification input initial |
| `--force-clarify` | Forcer clarification meme si input clair |
| `--competitive` | Activer section Competitive Analysis dans le brief (PRD v3.0) |

---

## Technique Mode Flags (v5.0)

| Flag | Effet |
|------|-------|
| `--random` | Selection aleatoire techniques avec equilibrage categories |
| `--progressive` | Mode 4 phases progressives (Expansion → Exploration → Convergence → Action) |

---

## Collaboration Mode Flags (v5.0)

| Flag | Effet |
|------|-------|
| `--party` | Demarrer en party mode (multi-persona) |
| `--panel` | Demarrer en expert panel mode |

**Note**: `--party` et `--panel` sont mutuellement exclusifs. Un seul mode actif a la fois.

---

## Flag Combinations

**Quick exploration**: `--quick --no-hmw`

**Deep analysis**: `--competitive --progressive`

**Minimal overhead**: `--turbo --no-security --no-plan`

**Full features**: (no flags) - Default behavior with all features enabled
