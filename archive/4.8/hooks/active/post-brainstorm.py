#!/usr/bin/env python3
"""
Post-brainstorm hook — Execute apres completion d'une session brainstorm.
Sauvegarde les metadonnees de session et met a jour la memoire projet.

Usage:
    python3 src/hooks/runner.py post-brainstorm --context '{
        "feature_slug": "auth-oauth",
        "ems_score": 78,
        "session_file": ".project-memory/brainstorm-sessions/auth-oauth.yaml",
        "brief_file": "docs/briefs/auth-oauth/brief-auth-oauth-2026-01-08.md",
        "journal_file": "docs/briefs/auth-oauth/journal-auth-oauth-2026-01-08.md",
        "template": "feature",
        "personas_used": ["Architect", "Sparring"],
        "techniques_applied": ["Six Thinking Hats", "SCAMPER"],
        "iterations": 5,
        "duration_minutes": 25
    }'

Context attendu:
    - feature_slug: Identifiant de la session (REQUIRED)
    - ems_score: Score EMS final 0-100 (optionnel)
    - session_file: Chemin vers fichier session YAML (optionnel)
    - brief_file: Chemin vers brief genere (optionnel)
    - journal_file: Chemin vers journal genere (optionnel)
    - template: feature|problem|decision (optionnel)
    - personas_used: Liste des personas utilises (optionnel)
    - techniques_applied: Liste des techniques appliquees (optionnel)
    - iterations: Nombre d'iterations (optionnel)
    - duration_minutes: Duree de session en minutes (optionnel)
"""
import json
import sys
from datetime import datetime
from pathlib import Path


def main():
    """Point d'entree du hook post-brainstorm."""
    result = {
        "status": "success",
        "message": "Brainstorm session saved to Project Memory",
        "details": {}
    }

    # Parser le contexte depuis les arguments
    context = {}
    if len(sys.argv) > 2 and sys.argv[1] == "--context":
        try:
            context = json.loads(sys.argv[2])
        except json.JSONDecodeError:
            result["status"] = "warning"
            result["message"] = "Invalid JSON context, continuing with empty context"

    # Extraire les donnees du contexte
    feature_slug = context.get("feature_slug", "unnamed")
    ems_score = context.get("ems_score", 0)
    session_file = context.get("session_file", "")
    brief_file = context.get("brief_file", "")
    journal_file = context.get("journal_file", "")
    template = context.get("template", "feature")
    personas_used = context.get("personas_used", [])
    techniques_applied = context.get("techniques_applied", [])
    iterations = context.get("iterations", 0)
    duration_minutes = context.get("duration_minutes", 0)
    timestamp = datetime.now().isoformat()

    # Creer les repertoires de logs/metriques si necessaires
    log_dir = Path(".project-memory/logs")
    metrics_dir = Path(".project-memory/metrics")
    log_dir.mkdir(parents=True, exist_ok=True)
    metrics_dir.mkdir(parents=True, exist_ok=True)

    # 1. Ecrire l'entree de log dans l'historique brainstorm
    log_file = log_dir / "brainstorm-history.jsonl"
    log_entry = {
        "timestamp": timestamp,
        "event": "post-brainstorm",
        "feature_slug": feature_slug,
        "ems_score": ems_score,
        "template": template,
        "personas_used": personas_used,
        "techniques_applied": techniques_applied,
        "iterations": iterations,
        "duration_minutes": duration_minutes,
        "session_file": session_file,
        "brief_file": brief_file,
        "journal_file": journal_file
    }

    try:
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")
        result["details"]["log_written"] = True
    except IOError as e:
        result["details"]["log_error"] = str(e)

    # 2. Mettre a jour les metriques brainstorm
    metrics_file = metrics_dir / "brainstorm-stats.json"
    try:
        if metrics_file.exists():
            with open(metrics_file, "r", encoding="utf-8") as f:
                stats = json.load(f)
        else:
            stats = {
                "total_sessions": 0,
                "by_template": {},
                "by_ems_bucket": {"low": 0, "medium": 0, "high": 0},
                "avg_iterations": 0,
                "avg_duration_minutes": 0,
                "personas_usage": {},
                "techniques_usage": {}
            }

        # Incrementer les compteurs
        stats["total_sessions"] = stats.get("total_sessions", 0) + 1
        stats["by_template"][template] = stats.get("by_template", {}).get(template, 0) + 1

        # Categoriser par bucket EMS
        if ems_score >= 75:
            bucket = "high"
        elif ems_score >= 50:
            bucket = "medium"
        else:
            bucket = "low"
        stats["by_ems_bucket"][bucket] = stats.get("by_ems_bucket", {}).get(bucket, 0) + 1

        # Calculer moyenne iterations (moyenne mobile)
        total = stats["total_sessions"]
        if total > 1 and iterations > 0:
            prev_avg = stats.get("avg_iterations", 0)
            stats["avg_iterations"] = round((prev_avg * (total - 1) + iterations) / total, 1)
        elif iterations > 0:
            stats["avg_iterations"] = iterations

        # Calculer moyenne duree (moyenne mobile)
        if total > 1 and duration_minutes > 0:
            prev_avg = stats.get("avg_duration_minutes", 0)
            stats["avg_duration_minutes"] = round((prev_avg * (total - 1) + duration_minutes) / total, 1)
        elif duration_minutes > 0:
            stats["avg_duration_minutes"] = duration_minutes

        # Compteurs personas
        for persona in personas_used:
            stats["personas_usage"][persona] = stats.get("personas_usage", {}).get(persona, 0) + 1

        # Compteurs techniques
        for technique in techniques_applied:
            stats["techniques_usage"][technique] = stats.get("techniques_usage", {}).get(technique, 0) + 1

        stats["last_session"] = timestamp

        with open(metrics_file, "w", encoding="utf-8") as f:
            json.dump(stats, f, indent=2, ensure_ascii=False)

        result["details"]["metrics_updated"] = True

    except (json.JSONDecodeError, IOError) as e:
        result["details"]["metrics_error"] = str(e)

    # 3. Indexer le brief pour recherche "similar features" (si brief existe)
    if brief_file:
        index_file = Path(".project-memory/briefs-index.jsonl")
        index_entry = {
            "timestamp": timestamp,
            "slug": feature_slug,
            "brief_file": brief_file,
            "ems_score": ems_score,
            "template": template
        }
        try:
            with open(index_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(index_entry, ensure_ascii=False) + "\n")
            result["details"]["brief_indexed"] = True
        except IOError as e:
            result["details"]["index_error"] = str(e)

    # Afficher confirmation
    result["details"]["feature_slug"] = feature_slug
    result["details"]["ems_score"] = ems_score

    ems_label = f"EMS {ems_score}/100" if ems_score > 0 else "EMS N/A"
    print(f"post-brainstorm: {feature_slug} ({ems_label})")
    print(f"                 Template: {template}, Iterations: {iterations}")
    if personas_used:
        print(f"                 Personas: {', '.join(personas_used)}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
