import codecs
import chardet
from typing import BinaryIO, TYPE_CHECKING
from normality.util import Encoding

if TYPE_CHECKING:
    from chardet import _IntermediateResultType

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
    if encoding is None:
        return default
    encoding = encoding.lower().strip()
    if encoding in ["", "ascii"]:
        return default
    if _is_encoding_codec(encoding):
        return encoding
    encoding = encoding.replace("-", "")
    if _is_encoding_codec(encoding):
        return encoding
    return default


def normalize_result(
    result: "_IntermediateResultType", default: Encoding, threshold: float = 0.2
) -> Encoding:
    """Interpret a chardet result."""
    if result is None:
        return default
    confidence = result.get("confidence")
    if confidence is None:
        return default
    if float(confidence) < threshold:
        return default
    encoding = result.get("encoding")
    if encoding is None:
        return default
    return normalize_encoding(encoding, default=default)


def guess_encoding(text: bytes, default: Encoding = DEFAULT_ENCODING) -> Encoding:
    """Guess string encoding.

    Given a piece of text, apply character encoding detection to
    guess the appropriate encoding of the text.
    """
    result = chardet.detect(text)
    return normalize_result(result, default=default)


def guess_file_encoding(fh: BinaryIO, default: Encoding = DEFAULT_ENCODING) -> Encoding:
    """Guess encoding from a file handle."""
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
