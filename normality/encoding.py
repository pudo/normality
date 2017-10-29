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
        if encoding is not None:
            encoding = encoding.lower().strip()
            if encoding != 'ascii':
                return encoding
    return default


def guess_file_encoding(fh, default='utf-8'):
    """Guess encoding from a file handle."""
    start = fh.tell()
    detector = chardet.UniversalDetector()
    for idx in xrange(1024):
        data = fh.read(1024)
        if not len(data):
            break
        detector.feed(data)
        if detector.done:
            break

    detector.close()
    fh.seek(start)
    result = detector.result
    if result.get('confidence') < 0.2:
        return default
    encoding = result.get('encoding') or default
    return encoding.lower()
