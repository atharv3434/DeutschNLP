"""
Custom Compound Noun Deconstructive Matcher for German.
Splits compound nouns into sub-lexemes while handling linking morphemes (Fugen-S, -en, -n).
"""

import re
from typing import List

# Common German compound bridge morphemes (Fugenelemente)
FUGEN_ELEMENTS = ["s", "es", "en", "n", "er", "e"]

# Common German lexical base components for offline decomposition fallback
COMMON_BASES = {
    "donau", "dampf", "schiff", "fahrt", "gesellschaft", "kapitän",
    "kranken", "haus", "wagen", "auto", "bahn", "hof", "flug", "hafen",
    "arbeit", "geber", "nehmer", "zeit", "plan", "hand", "schuh",
    "tier", "arzt", "garten", "haus", "schlüssel", "tür", "fenster",
    "feuer", "wehr", "polizei", "amt", "stadt", "zentrum", "sprache",
    "schule", "lehrer", "zimmer", "küche", "schrank", "wasser", "glas"
}

def split_german_compound(word: str) -> List[str]:
    """
    Deconstructs a German compound word into recognized lexical sub-parts.
    """
    clean_word = word.strip().lower()
    if len(clean_word) < 6:
        return [word]

    parts = []
    current = clean_word
    
    while len(current) > 3:
        matched = False
        # Try longest match from the left
        for i in range(len(current), 2, -1):
            sub = current[:i]
            if sub in COMMON_BASES:
                parts.append(sub.capitalize())
                remainder = current[i:]
                
                # Check and strip linking elements (Fugenelemente)
                for fug in FUGEN_ELEMENTS:
                    if remainder.startswith(fug) and len(remainder) > len(fug) + 2:
                        remainder = remainder[len(fug):]
                        break
                        
                current = remainder
                matched = True
                break
                
        if not matched:
            if parts:
                parts.append(current.capitalize())
            else:
                parts.append(word)
            break
            
    return parts if len(parts) > 1 else [word]