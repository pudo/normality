import string
from typing import Any, Optional

from normality.cleaning import collapse_spaces, category_replace
from normality.constants import SLUG_CATEGORIES, WS
from normality.transliteration import latinize_text
from normality.stringify import stringify

VALID_CHARS = string.ascii_lowercase + string.digits + WS


def slugify(value: Any, sep: str = "-") -> Optional[str]:
    """A simple slug generator. Slugs are pure ASCII lowercase strings
    that can be used in URLs an other places where a name has to be
    machine-safe."""
    text = stringify(value)
    if text is None:
        return None
    text = text.replace(sep, WS)
    # run this first because it'll give better results on special
    # characters.
    text = category_replace(text, SLUG_CATEGORIES)
    text = latinize_text(text, ascii=True)
    if text is None:
        return None
    text = text.lower()
    text = "".join([c for c in text if c in VALID_CHARS])
    text = collapse_spaces(text)
    if text is None or len(text) == 0:
        return None
    return text.replace(WS, sep)
