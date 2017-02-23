try:
    import cchardet as chardet
except ImportError:
    import chardet


def guess_encoding(text, default='utf-8'):
    """Guess string encoding.

    Given a piece of text, apply character encoding detection to
    guess the appropriate encoding of the text.
    """
    result = chardet.detect(text)
    if result:
        encoding = result.get('encoding')
        encoding = encoding.lower().strip()
        if encoding == 'ascii':
            encoding = default
        return encoding
    return default
