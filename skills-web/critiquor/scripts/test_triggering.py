#!/usr/bin/env python3
"""
CRITIQUOR Triggering Test Suite

Tests semantic matching for the critiquor skill.
Run: python test_triggering.py

Expected: SHOULD_TRIGGER queries activate the skill
          SHOULD_NOT_TRIGGER queries do not activate
"""

# ============================================
# TEST CASES
# ============================================

SHOULD_TRIGGER = [
    # Explicit triggers - French
    "Critique ce texte",
    "Critique ce mail que je dois envoyer",
    "Analyse ce document",
    "Analyse cette proposition commerciale",
    "Relis ce texte s'il te plaît",
    "Évalue cette note de synthèse",
    "Donne-moi une critique de cet article",
    "Peux-tu relire et corriger ce mail ?",
    "Qu'est-ce que tu penses de ce texte ?",
    
    # Explicit triggers - English
    "Critique this text",
    "Analyze this document",
    "Proofread this email",
    "Review this proposal",
    "Evaluate this report",
    "Give me feedback on this article",
    "What do you think of this text?",
    
    # With severity level
    "Critique ce texte en mode strict",
    "Analyse ce mail en mode doux",
    "Critique this document in strict mode",
    
    # With custom criteria
    "Critique ce texte et ajoute le critère SEO",
    "Analyze this with focus on accessibility",
    "Critique cette page en ajoutant le critère RGPD",
    
    # Summary mode
    "Donne-moi une critique en mode résumé",
    "Quick summary critique of this email",
    "Critique en bref ce document",
    
    # Long document
    "Critique cette documentation technique de 3000 mots",
    "Analyze this long proposal section by section",
    
    # Context-specific
    "Critique ce mail professionnel",
    "Analyse cette proposition commerciale",
    "Review this technical documentation",
    "Évalue ce conte que j'ai écrit",
]

SHOULD_NOT_TRIGGER = [
    # Simple corrections (no full analysis)
    "Corrige juste les fautes d'orthographe",
    "Fix the typos in this text",
    "Just spell-check this",
    "Corrige la grammaire seulement",
    
    # Image/visual content
    "Critique cette image",
    "Analyze this diagram",
    "Review this chart",
    "Évalue ce logo",
    
    # Non-text requests
    "Critique ce code Python",  # Could trigger but code is different
    "Analyze this spreadsheet",
    "Review this database schema",
    
    # Generic requests
    "Aide-moi à écrire un mail",
    "Write an email for me",
    "Generate a proposal",
    "Écris un article",
    
    # Translation
    "Traduis ce texte",
    "Translate this document",
    
    # Summarization (without critique)
    "Résume ce document",
    "Summarize this article",
    
    # Other skills
    "Reformule ce message vocal",  # Clarifior
    "Fais un compte-rendu de réunion",  # Resumator
    "Crée un prompt pour...",  # Promptor
]

# ============================================
# TEST FRAMEWORK
# ============================================

def print_header(text: str):
    """Print formatted header"""
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60)

def print_test_case(query: str, expected: str, status: str = "MANUAL"):
    """Print test case for manual verification"""
    emoji = "✅" if status == "PASS" else "❌" if status == "FAIL" else "🔍"
    print(f"{emoji} [{expected}] {query}")

def run_tests():
    """Run all triggering tests"""
    
    print_header("CRITIQUOR TRIGGERING TEST SUITE")
    print("\nThis test suite helps verify semantic matching.")
    print("Run each query manually and verify the skill triggers correctly.\n")
    
    # Should trigger tests
    print_header("SHOULD TRIGGER (expect critiquor to activate)")
    for query in SHOULD_TRIGGER:
        print_test_case(query, "SHOULD_TRIGGER")
    
    print(f"\nTotal: {len(SHOULD_TRIGGER)} test cases")
    
    # Should not trigger tests
    print_header("SHOULD NOT TRIGGER (expect critiquor to NOT activate)")
    for query in SHOULD_NOT_TRIGGER:
        print_test_case(query, "SHOULD_NOT")
    
    print(f"\nTotal: {len(SHOULD_NOT_TRIGGER)} test cases")
    
    # Summary
    print_header("TEST SUMMARY")
    print(f"""
Total test cases: {len(SHOULD_TRIGGER) + len(SHOULD_NOT_TRIGGER)}
- Should trigger: {len(SHOULD_TRIGGER)}
- Should not trigger: {len(SHOULD_NOT_TRIGGER)}

Instructions:
1. Copy each query and paste into Claude
2. Verify critiquor skill activates (or not) as expected
3. Mark any failures for description refinement

Key trigger words to verify:
- critique, analyze, proofread, review, evaluate
- "qu'est-ce que tu penses de"
- "donne-moi une critique"
- "relis ce texte"

Key exclusions to verify:
- Simple spell-check requests
- Image/visual content
- Code review (different skill)
- Translation requests
""")

if __name__ == "__main__":
    run_tests()
