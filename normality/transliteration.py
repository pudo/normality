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
from warnings import warn

try:
    # try to use pyicu (i.e. ICU4C)
    from icu import Transliterator

    def _latinize_internal(text):
        if not hasattr(latinize_text, '_tr'):
            rule = 'Any-Latin; Latin-ASCII'
            latinize_text._tr = Transliterator.createInstance(rule)
        return latinize_text._tr.transliterate(text)

except ImportError:
    try:
        # try to use unidecode (all Python, hence a bit slower)
        from unidecode import unidecode

        def _latinize_internal(text):
            # weirdly, schwa becomes an @ by default in unidecode
            text = text.replace(u'ə', 'a')
            return unidecode(text)

    except ImportError:

        def _latinize_internal(text):
            warn("No transliteration library is available. Install 'pyicu' or 'unidecode'.", UnicodeWarning)  # noqa
            return text


def latinize_text(text):
    """Transliterate the given text to the latin script.

    This attempts to convert a given text to latin script using the
    closest match of characters vis a vis the original script.
    """
    if text is None or not len(text):
        return
    text = _latinize_internal(text)
    return six.text_type(text)


if __name__ == '__main__':
    # Just to sanity-check the system:
    text = u'Порошенко Петро Олексійович'
    print(latinize_text(u'Порошенко Петро Олексійович'))