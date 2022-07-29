import re
import unicodedata
from typing import Any, Optional

from normality.constants import UNICODE_CATEGORIES, CONTROL_CODES, WS
from normality.util import Categories, is_text

COLLAPSE_RE = re.compile(r"\s+", re.U)
BOM_RE = re.compile("^\ufeff", re.U)
UNSAFE_RE = re.compile(r"^\ufeff|[\x00-\x08\x0b-\x0c\x0e-\x1f\x7f\x80-\x9f]|\u2028")
QUOTES_RE = re.compile(r'^["\'](.*)["\']$')


def decompose_nfkd(text: Any) -> Optional[str]:
    """Perform unicode compatibility decomposition.

    This will replace some non-standard value representations in unicode and
    normalise them, while also separating characters and their diacritics into
    two separate codepoints.
    """
    if not is_text(text):
        return None
    return unicodedata.normalize("NFKD", text)


def compose_nfc(text: Any) -> Optional[str]:
    """Perform unicode composition."""
    if not is_text(text):
        return None
    return unicodedata.normalize("NFC", text)


def compose_nfkc(text: Any) -> Optional[str]:
    """Perform unicode composition."""
    if not is_text(text):
        return None
    return unicodedata.normalize("NFKC", text)


def strip_quotes(text: Any) -> Optional[str]:
    """Remove double or single quotes surrounding a string."""
    if not is_text(text):
        return None
    return QUOTES_RE.sub("\\1", text)


def category_replace(
    text: Any, replacements: Categories = UNICODE_CATEGORIES
) -> Optional[str]:
    """Remove characters from a string based on unicode classes.

    This is a method for removing non-text characters (such as punctuation,
    whitespace, marks and diacritics) from a piece of text by class, rather
    than specifying them individually.
    """
    text = decompose_nfkd(text)
    if not is_text(text):
        return None
    characters = []
    for character in text:
        cat = unicodedata.category(character)
        replacement = replacements.get(cat, character)
        if replacement is not None:
            characters.append(replacement)
    return "".join(characters)


def remove_control_chars(text: Any) -> Optional[str]:
    """Remove just the control codes from a piece of text."""
    return category_replace(text, replacements=CONTROL_CODES)


def remove_unsafe_chars(text: Any) -> Optional[str]:
    """Remove unsafe unicode characters from a piece of text."""
    if not is_text(text):
        return None
    return UNSAFE_RE.sub("", text)


def remove_byte_order_mark(text: Any) -> Optional[str]:
    """Remove a BOM from the beginning of the text."""
    if not is_text(text):
        return None
    return BOM_RE.sub("", text)


def collapse_spaces(text: Any) -> Optional[str]:
    """Remove newlines, tabs and multiple spaces with single spaces."""
    if not is_text(text):
        return None
    return COLLAPSE_RE.sub(WS, text).strip(WS)
