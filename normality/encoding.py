try:
    import cchardet as chardet
except ImportError:
    import chardet


def guess_encoding(text, default=None):
    """Guess string encoding.

    Given a piece of text, apply character encoding detection to
    guess the appropriate encoding of the text.
    """
    result = chardet.detect(text)
    if result:
        encoding = result.get('encoding')
        if encoding.lower().strip() == 'ascii':
            encoding = 'utf-8'
        return encoding
    return default