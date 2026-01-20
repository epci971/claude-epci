#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EPCI Voice Cleaner

Cleans voice transcriptions by removing hesitations, fillers, and normalizing
spoken patterns to written form. Preserves rupture markers for multi-task detection.

Usage:
    from project_memory.voice_cleaner import clean_voice_transcript, VoiceCleaningResult

    result = clean_voice_transcript("euh faudrait fixer le login tu vois")
    print(result.cleaned_text)  # "Le système doit corriger le login."
    print(result.artifacts_removed)  # 2
"""

import re
from dataclasses import dataclass, field
from typing import List, Set, Tuple, Dict


# =============================================================================
# CONSTANTS
# =============================================================================

# Hesitations (always remove)
HESITATIONS_FR: Set[str] = {"euh", "heu", "hum", "hmm", "bah", "ben", "euuuh", "heuuu"}
HESITATIONS_EN: Set[str] = {"uh", "um", "er", "erm", "ah", "uhh", "umm"}
HESITATIONS: Set[str] = HESITATIONS_FR | HESITATIONS_EN

# Fillers (usually remove)
FILLERS_FR: List[str] = [
    "tu vois", "genre", "quoi", "voilà", "en fait", "du coup",
    "bon", "bref", "donc", "alors", "c'est-à-dire", "disons"
]
FILLERS_EN: List[str] = [
    "you know", "like", "right", "actually", "so", "well",
    "basically", "i mean", "kind of", "sort of"
]
FILLERS: List[str] = FILLERS_FR + FILLERS_EN

# Rupture markers (CRITICAL: preserve these)
RUPTURE_MARKERS: Set[str] = {
    # French
    "aussi", "également", "en plus", "et puis",
    "sinon", "autre chose", "autrement", "à part ça",
    "ah et", "oh et", "tiens", "au fait",
    # English
    "also", "additionally", "besides", "furthermore",
    "another thing", "by the way", "oh and"
}

# Self-correction markers
CORRECTION_MARKERS: List[str] = [
    "non", "plutôt", "en fait", "je veux dire", "pardon",
    "enfin", "finally", "actually", "i mean", "sorry"
]

# Tense normalization (spoken -> written)
TENSE_NORMALIZATIONS: Dict[str, str] = {
    "faudrait que": "doit",
    "il faudrait": "le système doit",
    "on voudrait": "le système doit",
    "ça serait bien si": "le système doit",
    "ça serait bien de": "le système doit",
    "ce serait bien si": "le système doit",
    "ce serait bien de": "le système doit",
    "faudrait": "doit",
}

# Voice normalization (1st/2nd person -> system-centric)
VOICE_NORMALIZATIONS: Dict[str, str] = {
    "je veux": "le système doit",
    "je voudrais": "le système doit",
    "j'aimerais": "le système doit",
    "tu peux": "le système peut",
    "on fait": "le système réalise",
    "on va faire": "le système va réaliser",
    "on doit": "le système doit",
}


# =============================================================================
# DATACLASSES
# =============================================================================

@dataclass
class VoiceCleaningResult:
    """Result of voice cleaning operation."""
    cleaned_text: str
    original_text: str
    artifacts_removed: int
    hesitations_found: List[str] = field(default_factory=list)
    fillers_found: List[str] = field(default_factory=list)
    corrections_applied: int = 0
    normalizations_applied: int = 0
    rupture_markers_preserved: List[str] = field(default_factory=list)


@dataclass
class HesitationDensity:
    """Hesitation density metrics for fuzziness scoring."""
    total_words: int
    hesitation_count: int
    filler_count: int
    density: float  # (hesitations + fillers) / total_words


# =============================================================================
# FUNCTIONS
# =============================================================================

def clean_voice_transcript(text: str) -> VoiceCleaningResult:
    """
    Clean a voice transcription by removing artifacts and normalizing text.

    Pipeline:
    1. Identify and preserve rupture markers
    2. Remove hesitations
    3. Remove fillers (except rupture markers)
    4. Process self-corrections
    5. Normalize tense and voice
    6. Clean up punctuation and whitespace

    Args:
        text: Raw voice transcription.

    Returns:
        VoiceCleaningResult with cleaned text and metrics.
    """
    if not text:
        return VoiceCleaningResult(
            cleaned_text="",
            original_text="",
            artifacts_removed=0
        )

    original = text
    result = VoiceCleaningResult(
        cleaned_text="",
        original_text=original,
        artifacts_removed=0
    )

    # Step 1: Identify rupture markers to preserve
    preserved_markers = _identify_rupture_markers(text)
    result.rupture_markers_preserved = preserved_markers

    # Step 2: Remove hesitations
    text, hesitations = _remove_hesitations(text)
    result.hesitations_found = hesitations
    result.artifacts_removed += len(hesitations)

    # Step 3: Remove fillers (preserving rupture markers)
    text, fillers = _remove_fillers(text, preserved_markers)
    result.fillers_found = fillers
    result.artifacts_removed += len(fillers)

    # Step 4: Process self-corrections
    text, corrections = _process_corrections(text)
    result.corrections_applied = corrections

    # Step 5: Normalize tense and voice
    text, normalizations = _normalize_speech(text)
    result.normalizations_applied = normalizations

    # Step 6: Clean up
    text = _cleanup_text(text)

    result.cleaned_text = text
    return result


def calculate_hesitation_density(text: str) -> HesitationDensity:
    """
    Calculate the density of hesitations and fillers in text.

    Used for fuzziness scoring - high density indicates voice-dictated content.

    Args:
        text: Raw text to analyze.

    Returns:
        HesitationDensity with metrics.
    """
    if not text:
        return HesitationDensity(
            total_words=0,
            hesitation_count=0,
            filler_count=0,
            density=0.0
        )

    text_lower = text.lower()
    words = text_lower.split()
    total_words = len(words)

    if total_words == 0:
        return HesitationDensity(
            total_words=0,
            hesitation_count=0,
            filler_count=0,
            density=0.0
        )

    # Count hesitations
    hesitation_count = sum(1 for word in words if word.strip(".,!?") in HESITATIONS)

    # Count fillers
    filler_count = sum(1 for filler in FILLERS if filler in text_lower)

    # Calculate density
    density = (hesitation_count + filler_count) / total_words

    return HesitationDensity(
        total_words=total_words,
        hesitation_count=hesitation_count,
        filler_count=filler_count,
        density=round(min(density, 1.0), 3)
    )


def is_voice_dictated(text: str, threshold: float = 0.1) -> bool:
    """
    Determine if text appears to be voice-dictated based on artifact density.

    Args:
        text: Text to analyze.
        threshold: Minimum density to consider as voice-dictated (default 0.1 = 10%).

    Returns:
        True if text appears voice-dictated.
    """
    density = calculate_hesitation_density(text)
    return density.density >= threshold


# =============================================================================
# INTERNAL HELPERS
# =============================================================================

def _identify_rupture_markers(text: str) -> List[str]:
    """Identify rupture markers present in text."""
    text_lower = text.lower()
    found = []

    for marker in RUPTURE_MARKERS:
        if marker in text_lower:
            found.append(marker)

    return found


def _remove_hesitations(text: str) -> Tuple[str, List[str]]:
    """Remove hesitation sounds from text."""
    found = []

    # Build pattern for word boundaries
    pattern = r'\b(' + '|'.join(re.escape(h) for h in HESITATIONS) + r')\b'

    def replacer(match):
        found.append(match.group(1))
        return ''

    text = re.sub(pattern, replacer, text, flags=re.IGNORECASE)

    return text, found


def _remove_fillers(text: str, preserved_markers: List[str]) -> Tuple[str, List[str]]:
    """Remove filler phrases, preserving rupture markers."""
    found = []

    # Sort fillers by length (longest first) to avoid partial matches
    sorted_fillers = sorted(FILLERS, key=len, reverse=True)

    for filler in sorted_fillers:
        # Skip if this filler is (or contains) a preserved rupture marker
        if any(marker in filler.lower() for marker in preserved_markers):
            continue

        pattern = r'\b' + re.escape(filler) + r'\b'
        matches = re.findall(pattern, text, flags=re.IGNORECASE)

        if matches:
            found.extend(matches)
            text = re.sub(pattern, '', text, flags=re.IGNORECASE)

    return text, found


def _process_corrections(text: str) -> Tuple[str, int]:
    """
    Process self-corrections, keeping only the corrected version.

    Example: "CSV, non pardon, JSON" -> "JSON"
    """
    corrections = 0

    for marker in CORRECTION_MARKERS:
        # Pattern: [something] [marker] [correction]
        # We keep only the correction part
        pattern = r'(\b\w+(?:\s+\w+)?\b)\s*,?\s*' + re.escape(marker) + r'\s*,?\s*(\b\w+(?:\s+\w+)?\b)'

        while re.search(pattern, text, flags=re.IGNORECASE):
            text = re.sub(pattern, r'\2', text, count=1, flags=re.IGNORECASE)
            corrections += 1

    return text, corrections


def _normalize_speech(text: str) -> Tuple[str, int]:
    """Normalize spoken patterns to written form."""
    normalizations = 0

    # Apply tense normalizations
    for spoken, written in TENSE_NORMALIZATIONS.items():
        pattern = re.compile(re.escape(spoken), re.IGNORECASE)
        if pattern.search(text):
            text = pattern.sub(written, text)
            normalizations += 1

    # Apply voice normalizations
    for spoken, written in VOICE_NORMALIZATIONS.items():
        pattern = re.compile(re.escape(spoken), re.IGNORECASE)
        if pattern.search(text):
            text = pattern.sub(written, text)
            normalizations += 1

    return text, normalizations


def _cleanup_text(text: str) -> str:
    """Clean up whitespace and punctuation."""
    # Remove multiple spaces
    text = re.sub(r'\s+', ' ', text)

    # Remove spaces before punctuation
    text = re.sub(r'\s+([.,!?;:])', r'\1', text)

    # Remove leading/trailing whitespace
    text = text.strip()

    # Capitalize first letter
    if text:
        text = text[0].upper() + text[1:]

    # Ensure ends with punctuation
    if text and text[-1] not in '.!?':
        text += '.'

    return text


# =============================================================================
# CLI (for testing)
# =============================================================================

def main():
    """CLI entry point for testing."""
    import sys

    if len(sys.argv) < 2:
        print("Usage: python voice_cleaner.py '<transcription>'")
        print("Example: python voice_cleaner.py 'euh faudrait fixer le login tu vois'")
        return 1

    text = ' '.join(sys.argv[1:])
    result = clean_voice_transcript(text)

    print(f"Original: {result.original_text}")
    print(f"Cleaned:  {result.cleaned_text}")
    print(f"Artifacts removed: {result.artifacts_removed}")
    print(f"  Hesitations: {result.hesitations_found}")
    print(f"  Fillers: {result.fillers_found}")
    print(f"  Corrections: {result.corrections_applied}")
    print(f"  Normalizations: {result.normalizations_applied}")
    print(f"  Rupture markers preserved: {result.rupture_markers_preserved}")

    density = calculate_hesitation_density(text)
    print(f"\nHesitation density: {density.density:.1%}")
    print(f"Voice-dictated: {is_voice_dictated(text)}")

    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
