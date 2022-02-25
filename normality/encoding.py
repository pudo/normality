import codecs
import chardet
import warnings
from charset_normalizer import from_bytes, CharsetMatches
from typing import BinaryIO, TYPE_CHECKING
from normality.util import Encoding

if TYPE_CHECKING:
    from chardet import _IntermediateResultType
    from charset_normalizer import CharsetMatches

DEFAULT_ENCODING = "utf-8"


def _is_encoding_codec(encoding: Encoding) -> bool:
    """Check if a given string is a valid encoding name."""
    try:
        codecs.lookup(encoding)
        return True
    except LookupError:
        return False


def normalize_encoding(encoding: str, default: Encoding = DEFAULT_ENCODING) -> str:
    """Normalize the encoding name, replace ASCII w/ UTF-8."""
    warnings.warn(
        "normalize_encoding is now deprecated. Use tidy_encoding instead",
        DeprecationWarning,
    )
    if encoding is None:
        return default
    encoding = encoding.lower().strip()
    if encoding in ["", "ascii"]:
        return default
    if _is_encoding_codec(encoding):
        return encoding
    encoding = encoding.replace("-", "")
    encoding = encoding.replace("_", "")
    if _is_encoding_codec(encoding):
        return encoding
    return default


def tidy_encoding(encoding: str, default: Encoding = DEFAULT_ENCODING) -> str:
    """Normalize the encoding name, replace ASCII w/ UTF-8."""
    return normalize_encoding(encoding, default)


def normalize_result(
    result: "_IntermediateResultType", default: Encoding, threshold: float = 0.2
) -> Encoding:
    """Interpret a chardet result."""
    warnings.warn(
        "normalize_result is now deprecated. Use tidy_result instead",
        DeprecationWarning,
    )
    if result is None:
        return default
    confidence: float = result.get("confidence")
    if confidence is None:
        return default
    if float(confidence) < threshold:
        return default
    encoding: Encoding = result.get("encoding")
    if encoding is None:
        return default
    return normalize_encoding(encoding, default=default)


def tidy_result(result: CharsetMatches, default: Encoding) -> Encoding:
    """Interpret a chardet result."""
    res = result.best()
    if res is None:
        return default
    encoding: Encoding = res.encoding
    if encoding is None:
        return default

    return tidy_encoding(encoding, default=default)


def guess_encoding(text: bytes, default: Encoding = DEFAULT_ENCODING) -> Encoding:
    """Guess string encoding.

    Given a piece of text, apply character encoding detection to
    guess the appropriate encoding of the text.
    """
    warnings.warn(
        "guess_encoding is now deprecated. Use predict_encoding instead",
        DeprecationWarning,
    )
    result = chardet.detect(text)
    return normalize_result(result, default=default)


def predict_encoding(text: bytes, default: Encoding = DEFAULT_ENCODING) -> Encoding:
    """Guess string encoding.

    Given a piece of text, apply character encoding detection to
    guess the appropriate encoding of the text.
    """
    result = from_bytes(text, explain=False)

    return tidy_result(result, default=default)


def guess_file_encoding(fh: BinaryIO, default: Encoding = DEFAULT_ENCODING) -> Encoding:
    """Guess encoding from a file handle."""
    warnings.warn(
        "guess_encoding is now deprecated. Use predict_encoding instead",
        DeprecationWarning,
    )
    start = fh.tell()
    detector = chardet.UniversalDetector()
    while True:
        data = fh.read(1024 * 10)
        if not data:
            detector.close()
            break
        detector.feed(data)
        if detector.done:
            break

    fh.seek(start)
    return normalize_result(detector.result, default=default)


def predict_file_encoding(
    fh: BinaryIO, default: Encoding = DEFAULT_ENCODING
) -> Encoding:
    """Guess encoding from a file handle."""
    start = fh.tell()
    result: CharsetMatches = CharsetMatches()

    while True:
        data = fh.read(1024 * 10)
        if not data:
            break

        result = from_bytes(data, explain=False)
        if result:
            break

    fh.seek(start)
    return tidy_result(result, default=default)
