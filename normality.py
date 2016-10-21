import re
import six
import unicodedata

WS = ' '
COLLAPSE = re.compile(r'\s+')

# Unicode character classes, see:
# http://www.fileformat.info/info/unicode/category/index.htm
CATEGORY_DEFAULTS = {
    'C': WS,
    'Lm': None,
    'M': None,
    'Z': WS,
    'P': WS,
    'S': WS
}


def normalize(text, lowercase=True, collapse=True, decompose=True,
              replace_categories=CATEGORY_DEFAULTS):
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
    if not isinstance(text, six.string_types):
        return

    # TODO: Python 3?
    if six.PY2 and not isinstance(text, six.text_type):
        text = text.decode('utf-8')

    if lowercase:
        # Yeah I made a Python package for this.
        text = text.lower()

    # if transliterate:
    #    # Perform unicode-based transliteration, e.g. of cyricllic
    #    # or CJK scripts into latin.
    #    text = unidecode(text)
    #    if six.PY2:
    #        text = unicode(text)

    if decompose:
        # Apply a canonical unicode normalization form, e.g.
        # transform all composite characters with diacritics
        # into a series of characters followed by their
        # diacritics as separate unicode codepoints.
        text = unicodedata.normalize('NFKD', text)

    # Perform unicode category-based character replacement. This is
    # used to filter out whole classes of characters, such as symbols,
    # punctuation, or whitespace-like characters.
    characters = []
    for character in text:
        category = unicodedata.category(character)
        if category not in replace_categories:
            category = category[0]
        replacement = replace_categories.get(category, character)
        if replacement is not None:
            characters.append(replacement)
    text = u''.join(characters)

    if collapse:
        # Remove consecutive whitespace.
        text = COLLAPSE.sub(WS, text).strip(WS)

    return text


def slugify(text, sep='-'):
    """A simple slug generator."""
    text = normalize(text, collapse=True)
    if text is not None:
        return text.replace(WS, sep)
