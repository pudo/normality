# coding: utf-8
"""
Transliterate the given text to the latin script.

This attempts to convert a given text to latin script using the
closest match of characters vis a vis the original script.

Transliteration requires an extensive unicode mapping. Since all
Python implementations are either GPL-licensed (and thus more
restrictive than this library) or come with a massive C code
dependency, this module requires neither but will use a package
if it is installed.
"""
import six
from icu import Transliterator


def latinize_text(text, ascii=False):
    """Transliterate the given text to the latin script.

    This attempts to convert a given text to latin script using the
    closest match of characters vis a vis the original script.
    """
    if text is None or not isinstance(text, six.string_types) or not len(text):
        return text

    if ascii:
        if not hasattr(latinize_text, '_ascii'):
            # Transform to latin, separate accents, decompose, remove
            # symbols, compose, push to ASCII
            latinize_text._ascii = Transliterator.createInstance('Any-Latin; NFKD; [:Symbol:] Remove; [:Nonspacing Mark:] Remove; NFKC; Accents-Any; Latin-ASCII')  # noqa
        return latinize_text._ascii.transliterate(text)

    if not hasattr(latinize_text, '_tr'):
        latinize_text._tr = Transliterator.createInstance('Any-Latin')
    return latinize_text._tr.transliterate(text)


def ascii_text(text):
    """Transliterate the given text and make sure it ends up as ASCII."""
    text = latinize_text(text, ascii=True)
    if isinstance(text, six.text_type):
        text = text.encode('ascii', 'ignore').decode('ascii')
    return text
