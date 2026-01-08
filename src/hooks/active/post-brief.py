#!/usr/bin/env python3
"""
Post-brief hook — Execute apres generation output (inline brief ou Feature Document).
Met a jour les metriques et prepare le contexte pour /epci ou /quick.

Usage:
    python3 src/hooks/runner.py post-brief --context '{
        "category": "STANDARD",
        "slug": "auth-oauth",
        "output_type": "feature_document",
        "next_command": "/epci"
    }'

Context attendu:
    - category: TINY|SMALL|STANDARD|LARGE
    - slug: Identifiant de la feature
    - output_type: inline|feature_document
    - next_command: /quick ou /epci avec flags
    - files_count: Nombre de fichiers impactes (optionnel)
    - flags: Liste des flags actifs (optionnel)
"""
import json
import sys
from datetime import datetime
from pathlib import Path


def main():
    """Point d'entree du hook post-brief."""
    # Parser le contexte depuis les arguments
    context = {}
    if len(sys.argv) > 2 and sys.argv[1] == "--context":
        try:
            context = json.loads(sys.argv[2])
        except json.JSONDecodeError:
            print("Warning: Invalid JSON context, continuing with empty context")

    # Extraire les donnees du contexte
    category = context.get("category", "UNKNOWN")
    slug = context.get("slug", "unnamed")
    output_type = context.get("output_type", "inline")
    next_command = context.get("next_command", "/quick")
    files_count = context.get("files_count", 0)
    flags = context.get("flags", [])
    timestamp = datetime.now().isoformat()

    # Creer le repertoire de logs si necessaire
    log_dir = Path(".project-memory/logs")
    log_dir.mkdir(parents=True, exist_ok=True)

    # Ecrire l'entree de log
    log_file = log_dir / "brief-history.jsonl"
    log_entry = {
        "timestamp": timestamp,
        "event": "post-brief",
        "category": category,
        "slug": slug,
        "output_type": output_type,
        "next_command": next_command,
        "files_count": files_count,
        "flags": flags
    }

    with open(log_file, "a", encoding="utf-8") as f:
        f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")

    # Mettre a jour les metriques de brief si le fichier existe
    metrics_file = Path(".project-memory/metrics/brief-stats.json")
    if metrics_file.parent.exists():
        try:
            if metrics_file.exists():
                with open(metrics_file, "r", encoding="utf-8") as f:
                    stats = json.load(f)
            else:
                stats = {"total_briefs": 0, "by_category": {}, "by_output_type": {}}

            # Incrementer les compteurs
            stats["total_briefs"] = stats.get("total_briefs", 0) + 1
            stats["by_category"][category] = stats.get("by_category", {}).get(category, 0) + 1
            stats["by_output_type"][output_type] = stats.get("by_output_type", {}).get(output_type, 0) + 1
            stats["last_brief"] = timestamp

            with open(metrics_file, "w", encoding="utf-8") as f:
                json.dump(stats, f, indent=2, ensure_ascii=False)

        except (json.JSONDecodeError, IOError) as e:
            print(f"Warning: Could not update brief stats: {e}")

    # Afficher confirmation
    output_label = "Feature Document" if output_type == "feature_document" else "Inline Brief"
    print(f"post-brief: {category} -> {output_label} ({slug})")
    print(f"           Next: {next_command}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
