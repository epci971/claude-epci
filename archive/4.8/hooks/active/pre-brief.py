#!/usr/bin/env python3
"""
Pre-brief hook — Execute avant l'exploration (apres validation du brief).
Logging du brief valide pour tracabilite.

Usage:
    python3 src/hooks/runner.py pre-brief --context '{"brief": "...", "reformulated": true}'

Context attendu:
    - brief: Le brief valide (original ou reformule)
    - reformulated: Boolean indiquant si reformulation a eu lieu
    - artifacts_count: Nombre d'artefacts vocaux detectes (optionnel)
"""
import json
import sys
from datetime import datetime
from pathlib import Path


def main():
    """Point d'entree du hook pre-brief."""
    # Parser le contexte depuis les arguments
    context = {}
    if len(sys.argv) > 2 and sys.argv[1] == "--context":
        try:
            context = json.loads(sys.argv[2])
        except json.JSONDecodeError:
            print("Warning: Invalid JSON context, continuing with empty context")

    # Extraire les donnees du contexte
    brief_text = context.get("brief", "")
    reformulated = context.get("reformulated", False)
    artifacts_count = context.get("artifacts_count", 0)
    timestamp = datetime.now().isoformat()

    # Creer le repertoire de logs si necessaire
    log_dir = Path(".project-memory/logs")
    log_dir.mkdir(parents=True, exist_ok=True)

    # Ecrire l'entree de log
    log_file = log_dir / "brief-history.jsonl"
    log_entry = {
        "timestamp": timestamp,
        "event": "pre-brief",
        "brief": brief_text[:500] if brief_text else "",  # Tronquer si trop long
        "reformulated": reformulated,
        "artifacts_count": artifacts_count
    }

    with open(log_file, "a", encoding="utf-8") as f:
        f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")

    # Afficher confirmation
    status = "reformule" if reformulated else "original"
    print(f"pre-brief: Brief {status} enregistre ({len(brief_text)} chars)")

    return 0


if __name__ == "__main__":
    sys.exit(main())
