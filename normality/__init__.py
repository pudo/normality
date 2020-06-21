"""Helper functions for string cleaning.

`normality` includes functions to convert arbitrary Python objects to
strings, transliterate them into the latin alphabet, make slugs for
URLs, or perform the substitution of characters based on unicode
character categories.
"""
from typing import Any, Optional

from normality.cleaning import collapse_spaces, category_replace
from normality.constants import UNICODE_CATEGORIES, WS
from normality.transliteration import latinize_text, ascii_text
from normality.encoding import guess_encoding, guess_file_encoding  # noqa
from normality.encoding import DEFAULT_ENCODING
from normality.stringify import stringify  # noqa
from normality.paths import safe_filename  # noqa
from normality.util import Categories, Encoding


def normalize(text: Any, lowercase: bool = True, collapse: bool = True,
              latinize: bool = False, ascii: bool = False,
              encoding_default: Encoding = DEFAULT_ENCODING,
              encoding: Optional[str] = None,
              replace_categories: Categories = UNICODE_CATEGORIES):
    """The main normalization function for text.

    This will take a string and apply a set of transformations to it so
    that it can be processed more easily afterwards. Arguments:

    * ``lowercase``: not very mysterious.
    * ``collapse``: replace multiple whitespace-like characters with a
      single whitespace. This is especially useful with category replacement
      which can lead to a lot of whitespace.
    * ``decompose``: apply a unicode normalization (NFKD) to separate
      simple characters and their diacritics.
    * ``replace_categories``: This will perform a replacement of whole
      classes of unicode characters (e.g. symbols, marks, numbers) with a
      given character. It is used to replace any non-text elements of the
      input string.
    """
    text = stringify(text, encoding_default=encoding_default,
                     encoding=encoding)
    if text is None:
        return

    if lowercase:
        # Yeah I made a Python package for this.
        text = text.lower()

    if ascii:
        # A stricter form of transliteration that leaves only ASCII
        # characters.
        text = ascii_text(text)
    elif latinize:
        # Perform unicode-based transliteration, e.g. of cyricllic
        # or CJK scripts into latin.
        text = latinize_text(text)

    if text is None:
        return

    # Perform unicode category-based character replacement. This is
    # used to filter out whole classes of characters, such as symbols,
    # punctuation, or whitespace-like characters.
    text = category_replace(text, replace_categories)

    if collapse:
        # Remove consecutive whitespace.
        text = collapse_spaces(text)
    return text


def slugify(text: Any, sep: str = '-') -> Optional[str]:
    """A simple slug generator."""
    text = stringify(text)
    if text is None:
        return None
    text = text.replace(sep, WS)
    text = normalize(text, ascii=True)
    if text is None:
        return None
    return text.replace(WS, sep)
