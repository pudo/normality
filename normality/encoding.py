import io
import six
import codecs
try:
    import cchardet as chardet
except ImportError:
    import chardet

DEFAULT_ENCODING = 'utf-8'


def normalize_encoding(encoding, default=DEFAULT_ENCODING):
    """Normalize the encoding name, replace ASCII w/ UTF-8."""
    if encoding is None:
        return default
    encoding = encoding.lower().strip()
    if encoding in ['', 'ascii']:
        return default
    try:
        codecs.lookup(encoding)
        return encoding
    except LookupError:
        return default


def normalize_result(result, default, threshold=0.2):
    """Interpret a chardet result."""
    if result is None or result.get('confidence') < threshold:
        return default
    return normalize_encoding(result.get('encoding'),
                              default=default)


def guess_encoding(text, default=DEFAULT_ENCODING):
    """Guess string encoding.

    Given a piece of text, apply character encoding detection to
    guess the appropriate encoding of the text.
    """
    result = chardet.detect(text)
    return normalize_result(result, default=default)


def guess_file_encoding(fh, default=DEFAULT_ENCODING):
    """Guess encoding from a file handle."""
    start = fh.tell()
    detector = chardet.UniversalDetector()
    for idx in six.moves.range(1024):
        data = fh.read(1024)
        if not len(data):
            break
        detector.feed(data)
        if detector.done:
            break

    detector.close()
    fh.seek(start)
    return normalize_result(detector.result, default=default)


def guess_path_encoding(file_path, default=DEFAULT_ENCODING):
    """Wrapper to open that damn file for you, lazy bastard."""
    with io.open(file_path, 'r') as fh:
        return guess_file_encoding(fh, default=default)
