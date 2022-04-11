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
import warnings
from typing import cast, Optional, Callable
from functools import lru_cache

from normality.cleaning import compose_nfkc
from normality.util import is_text

# Transform to latin, separate accents, decompose, remove
# symbols, compose, push to ASCII
ASCII_SCRIPT = "Any-Latin; NFKD; [:Nonspacing Mark:] Remove; Accents-Any; [:Symbol:] Remove; [:Nonspacing Mark:] Remove; Latin-ASCII"  # noqa
# nb. 2021-11-05 Accents-Any is now followed with another nonspacing mark remover.
# This script is becoming a bit silly, there has to be a nicer way to do this?


class ICUWarning(UnicodeWarning):
    pass


@lru_cache(maxsize=2**16)
def latinize_text(text: Optional[str], ascii: bool = False) -> Optional[str]:
    """Transliterate the given text to the latin script.

    This attempts to convert a given text to latin script using the
    closest match of characters vis a vis the original script.
    """
    if text is None or not is_text(text) or not len(text):
        return text

    if ascii:
        if not hasattr(latinize_text, "_ascii"):
            latinize_text._ascii = make_trans(ASCII_SCRIPT)  # type: ignore
        return latinize_text._ascii(text)  # type: ignore

    if not hasattr(latinize_text, "_tr"):
        latinize_text._tr = make_trans("Any-Latin")  # type: ignore
    return latinize_text._tr(text)  # type: ignore


def ascii_text(text: Optional[str]) -> Optional[str]:
    """Transliterate the given text and make sure it ends up as ASCII."""
    text = latinize_text(text, ascii=True)
    if text is None or not is_text(text):
        return None
    return text.encode("ascii", "replace").decode("ascii")


def make_trans(script: str) -> Callable[[str], Optional[str]]:
    try:
        from icu import Transliterator  # type: ignore

        inst = Transliterator.createInstance(script)
        return cast(Callable[[str], str], inst.transliterate)
    except ImportError:
        from text_unidecode import unidecode  # type: ignore

        warnings.warn(
            "Install 'pyicu' for better text transliteration.", ICUWarning, stacklevel=4
        )  # noqa

        def transliterate(text: str) -> Optional[str]:
            clean = compose_nfkc(text)
            if clean is None:
                return None
            return cast(Optional[str], unidecode(clean))

        return transliterate
