#!/usr/bin/env python3
"""
CRITIQUOR v2.0 — Triggering Test Suite
Tests semantic matching for skill activation
"""

# Test cases for CRITIQUOR triggering
# Format: (query, should_trigger, expected_mode, notes)

TRIGGER_TESTS = [
    # === SHOULD TRIGGER (Standard Mode) ===
    ("Critique ce mail", True, "standard", "Basic French trigger"),
    ("Critique ce texte", True, "standard", "Basic text critique"),
    ("Analyse ce document", True, "standard", "Document analysis"),
    ("Relis ce mail", True, "standard", "Proofreading request"),
    ("Donne-moi une critique de cette proposition", True, "standard", "Explicit critique request"),
    ("Évalue cette proposition commerciale", True, "standard", "Evaluation request"),
    ("Qu'est-ce que tu penses de ce texte ?", True, "standard", "Opinion request in critique context"),
    ("Peux-tu relire et corriger ce document ?", True, "standard", "Proofread and correct"),
    ("Review this email before I send it", True, "standard", "English trigger"),
    ("Analyze my proposal", True, "standard", "English analysis"),
    ("critiquor", True, "standard", "Direct skill invocation"),
    
    # === SHOULD TRIGGER (Express Mode) ===
    ("--express critique ce mail", True, "express", "Express flag"),
    ("--quick analyse ce texte", True, "express", "Quick flag"),
    ("Critique rapide de ce mail", True, "express", "Implicit express"),
    
    # === SHOULD TRIGGER (Focus Mode) ===
    ("--focus intro critique ce texte", True, "focus", "Focus on intro"),
    ("Critique seulement la conclusion", True, "focus", "Focus on conclusion"),
    ("--focus section:2 analyse ce document", True, "focus", "Focus on section"),
    
    # === SHOULD TRIGGER (Compare Mode) ===
    ("--compare ces deux versions", True, "compare", "Compare flag"),
    ("compare\nVersion A\n---\nVersion B", True, "compare", "Compare format"),
    ("Quelle version est meilleure ?", True, "compare", "Implicit compare"),
    
    # === SHOULD TRIGGER (Checklist Mode) ===
    ("--checklist ce mail avant envoi", True, "checklist", "Checklist flag"),
    ("Validation pré-envoi de ce mail", True, "checklist", "Pre-send validation"),
    
    # === SHOULD TRIGGER (With Persona) ===
    ("--avocat critique cette proposition", True, "standard", "Devil's advocate"),
    ("--mentor analyse ce texte", True, "standard", "Mentor mode"),
    ("--strict critique ce mail", True, "standard", "Strict severity"),
    
    # === SHOULD TRIGGER (With Grid) ===
    ("--grille prompt critique ces instructions", True, "standard", "Prompt grid"),
    ("--grille api analyse cette documentation", True, "standard", "API grid"),
    
    # === SHOULD NOT TRIGGER ===
    ("Corrige les fautes d'orthographe", False, None, "Simple spell-check only"),
    ("Écris un mail pour mon client", False, None, "Content creation → corrector"),
    ("Génère un prompt pour Claude", False, None, "Prompt creation → promptor"),
    ("Résume cette réunion", False, None, "Meeting summary → resumator"),
    ("Traduis ce texte en anglais", False, None, "Translation request"),
    ("Quelle est la capitale de la France ?", False, None, "General knowledge"),
    ("Aide-moi à coder une fonction Python", False, None, "Coding request"),
    ("Analyse cette image", False, None, "Image analysis (not supported)"),
    ("Crée une présentation PowerPoint", False, None, "Content creation"),
]

# Test cases for theme detection
THEME_DETECTION_TESTS = [
    # (sample_text_snippet, expected_theme)
    ("Cher client, suite à notre échange...", "Professional"),
    ("Le ROI de cette campagne...", "Marketing"),
    ("async function fetchData()...", "IT/Development"),
    ("Le modèle GPT utilise des transformers...", "AI/ML"),
    ("Conformément à l'article L.121-1...", "Legal"),
    ("Le CA du T3 s'élève à 2.3M€...", "Finance"),
    ("POST /api/v1/users", "API Documentation"),
    ("Tu es un assistant qui...", "Prompt Engineering"),
    ("<button>Valider</button>", "UX Writing"),
    ("Slide 1: Problem\nSlide 2: Solution", "Pitch Deck"),
    ("Décisions prises:\n- Action 1: Jean", "Meeting Notes"),
]

# Test cases for persona auto-switch
PERSONA_SWITCH_TESTS = [
    # (context, expected_persona)
    ("First document in session", "Mentor"),
    ("Technical documentation", "Editor"),
    ("Sales proposal", "Devil's Advocate"),
    ("Email to client", "Target Reader"),
    ("--strict mode", "Editor"),
    ("--doux mode", "Mentor"),
    ("Stress-test this pitch", "Devil's Advocate"),
]

def run_tests():
    """Run all triggering tests and report results."""
    print("=" * 60)
    print("CRITIQUOR v2.0 — Triggering Test Suite")
    print("=" * 60)
    
    # Trigger tests
    print("\n📋 TRIGGER TESTS")
    print("-" * 40)
    passed = 0
    failed = 0
    
    for query, should_trigger, expected_mode, notes in TRIGGER_TESTS:
        # In real implementation, this would call the actual matching logic
        # Here we just report the expected behavior
        status = "✅" if should_trigger else "❌"
        mode_str = f" [{expected_mode}]" if expected_mode else ""
        print(f"{status} {query[:40]:<40}{mode_str}")
        print(f"   → {notes}")
        passed += 1
    
    print(f"\n📊 Results: {passed}/{len(TRIGGER_TESTS)} test cases defined")
    
    # Theme detection tests
    print("\n📋 THEME DETECTION TESTS")
    print("-" * 40)
    for snippet, theme in THEME_DETECTION_TESTS:
        print(f"🎯 \"{snippet[:30]}...\" → {theme}")
    
    print(f"\n📊 Results: {len(THEME_DETECTION_TESTS)} theme cases defined")
    
    # Persona switch tests
    print("\n📋 PERSONA AUTO-SWITCH TESTS")
    print("-" * 40)
    for context, persona in PERSONA_SWITCH_TESTS:
        icon = {"Mentor": "🎓", "Editor": "✂️", "Devil's Advocate": "😈", "Target Reader": "👤"}[persona]
        print(f"{icon} {context:<35} → {persona}")
    
    print(f"\n📊 Results: {len(PERSONA_SWITCH_TESTS)} persona cases defined")
    
    print("\n" + "=" * 60)
    print("Test suite complete. Use these cases to validate triggering.")
    print("=" * 60)

if __name__ == "__main__":
    run_tests()
