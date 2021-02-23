from datetime import datetime, date
from decimal import Decimal
from typing import Any, Optional

from normality.cleaning import remove_unsafe_chars
from normality.encoding import guess_encoding
from normality.encoding import DEFAULT_ENCODING


def stringify(
    value: Any, encoding_default: str = DEFAULT_ENCODING, encoding: Optional[str] = None
) -> Optional[str]:
    """Brute-force convert a given object to a string.

    This will attempt an increasingly mean set of conversions to make a given
    object into a unicode string. It is guaranteed to either return unicode or
    None, if all conversions failed (or the value is indeed empty).
    """
    if value is None:
        return None

    if not isinstance(value, str):
        if isinstance(value, (date, datetime)):
            return value.isoformat()
        elif isinstance(value, (float, Decimal)):
            return Decimal(value).to_eng_string()
        elif isinstance(value, bytes):
            if encoding is None:
                encoding = guess_encoding(value, default=encoding_default)
            value = value.decode(encoding, "replace")
            value = remove_unsafe_chars(value)
        else:
            value = str(value)

    # XXX: is this really a good idea?
    value = value.strip()
    if not len(value):
        return None
    return value
