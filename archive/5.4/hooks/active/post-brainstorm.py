#!/usr/bin/env python3
"""
Post-brainstorm hook — Execute apres completion d'une session brainstorm.
Sauvegarde les metadonnees de session et met a jour la memoire projet.

v5.0: Support Party Mode, Expert Panel, technique categories/sources.

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
        "technique_categories": {"structured": 1, "creative": 1},
        "technique_source": "auto",
        "session_mode": "standard",
        "party_rounds": 0,
        "party_personas_used": [],
        "panel_rounds": 0,
        "panel_phase": "",
        "panel_experts_used": [],
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
    - technique_categories: Dict categories utilisees (v5.0)
    - technique_source: Source technique (auto|manual|random|progressive) (v5.0)
    - session_mode: Mode session (standard|party|panel) (v5.0)
    - party_rounds: Nombre de rounds party mode (v5.0)
    - party_personas_used: Personas party utilises (v5.0)
    - panel_rounds: Nombre de rounds panel (v5.0)
    - panel_phase: Phase panel finale (v5.0)
    - panel_experts_used: Experts panel utilises (v5.0)
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

    # v5.0: Nouvelles metriques
    technique_categories = context.get("technique_categories", {})
    technique_source = context.get("technique_source", "manual")
    session_mode = context.get("session_mode", "standard")
    party_rounds = context.get("party_rounds", 0)
    party_personas_used = context.get("party_personas_used", [])
    panel_rounds = context.get("panel_rounds", 0)
    panel_phase = context.get("panel_phase", "")
    panel_experts_used = context.get("panel_experts_used", [])

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
        "journal_file": journal_file,
        # v5.0 fields
        "technique_categories": technique_categories,
        "technique_source": technique_source,
        "session_mode": session_mode,
        "party_rounds": party_rounds,
        "party_personas_used": party_personas_used,
        "panel_rounds": panel_rounds,
        "panel_phase": panel_phase,
        "panel_experts_used": panel_experts_used
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
                "techniques_usage": {},
                # v5.0 fields
                "technique_categories_usage": {},
                "technique_sources": {"auto": 0, "manual": 0, "random": 0, "progressive": 0},
                "by_mode": {"standard": 0, "party": 0, "panel": 0},
                "party_sessions": 0,
                "party_personas_usage": {},
                "panel_sessions": 0,
                "panel_experts_usage": {},
                "panel_phases_usage": {}
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

        # v5.0: Compteurs technique categories
        if "technique_categories_usage" not in stats:
            stats["technique_categories_usage"] = {}
        for cat, count in technique_categories.items():
            stats["technique_categories_usage"][cat] = stats["technique_categories_usage"].get(cat, 0) + count

        # v5.0: Compteurs technique sources
        if "technique_sources" not in stats:
            stats["technique_sources"] = {"auto": 0, "manual": 0, "random": 0, "progressive": 0}
        if technique_source:
            stats["technique_sources"][technique_source] = stats["technique_sources"].get(technique_source, 0) + 1

        # v5.0: Compteurs par mode
        if "by_mode" not in stats:
            stats["by_mode"] = {"standard": 0, "party": 0, "panel": 0}
        stats["by_mode"][session_mode] = stats["by_mode"].get(session_mode, 0) + 1

        # v5.0: Party mode stats
        if party_rounds > 0:
            stats["party_sessions"] = stats.get("party_sessions", 0) + 1
            if "party_personas_usage" not in stats:
                stats["party_personas_usage"] = {}
            for persona in party_personas_used:
                stats["party_personas_usage"][persona] = stats["party_personas_usage"].get(persona, 0) + 1

        # v5.0: Panel mode stats
        if panel_rounds > 0:
            stats["panel_sessions"] = stats.get("panel_sessions", 0) + 1
            if "panel_experts_usage" not in stats:
                stats["panel_experts_usage"] = {}
            for expert in panel_experts_used:
                stats["panel_experts_usage"][expert] = stats["panel_experts_usage"].get(expert, 0) + 1
            if panel_phase:
                if "panel_phases_usage" not in stats:
                    stats["panel_phases_usage"] = {}
                stats["panel_phases_usage"][panel_phase] = stats["panel_phases_usage"].get(panel_phase, 0) + 1

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
    print(f"                 Template: {template}, Mode: {session_mode}, Iterations: {iterations}")
    if personas_used:
        print(f"                 Personas: {', '.join(personas_used)}")
    if party_rounds > 0:
        print(f"                 Party: {party_rounds} rounds, {', '.join(party_personas_used)}")
    if panel_rounds > 0:
        print(f"                 Panel: {panel_rounds} rounds ({panel_phase}), {', '.join(panel_experts_used)}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
