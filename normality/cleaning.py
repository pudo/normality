# coding: utf-8
import re
from unicodedata import normalize, category

from normality.constants import UNICODE_CATEGORIES

COLLAPSE_RE = re.compile(r'\s+', re.U)

try:
    # try to use pyicu (i.e. ICU4C)
    from icu import Transliterator

    def _decompose_nfkd(text):
        if not hasattr(_decompose_nfkd, '_tr'):
            _decompose_nfkd._tr = Transliterator.createInstance('Any-NFKD')
        return _decompose_nfkd._tr.transliterate(text)

except ImportError:

    def _decompose_nfkd(text):
        return normalize('NFKD', text)


def decompose_nfkd(text):
    """Perform unicode compatibility decomposition.

    This will replace some non-standard value representations in unicode and
    normalise them, while also separating characters and their diacritics into
    two separate codepoints.
    """
    return _decompose_nfkd(text)


def category_replace(text, replacements=UNICODE_CATEGORIES):
    """Remove characters from a string based on unicode classes.

    This is a method for removing non-text characters (such as punctuation,
    whitespace, marks and diacritics) from a piece of text by class, rather
    than specifying them individually.
    """
    characters = []
    for character in decompose_nfkd(text):
        cat = category(character)
        replacement = replacements.get(cat, character)
        if replacement is not None:
            characters.append(replacement)
    return u''.join(characters)


def collapse_spaces(text):
    """Remove newlines, tabs and multiple spaces with single spaces."""
    return COLLAPSE_RE.sub(' ', text).strip(' ')
