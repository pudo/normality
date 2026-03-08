from normality.cleaning import remove_unsafe_chars, collapse_spaces, squash_spaces


def test_remove_unsafe_chars():
    assert remove_unsafe_chars("") == ""
    assert remove_unsafe_chars(" ") == " "
    assert remove_unsafe_chars("\u2028 ") == "  "
    assert remove_unsafe_chars("\ufeff ") == " "
    assert remove_unsafe_chars("lalala\ufeff ") == "lalala "
    assert remove_unsafe_chars("lalala\u200bx") == "lalalax"


def test_remove_unsafe_chars_controls() -> None:
    # C0 control chars (except \t \n \r) are deleted
    for cp in [*range(0x00, 0x09), *range(0x0B, 0x0D), *range(0x0E, 0x20), 0x7F]:
        assert remove_unsafe_chars(chr(cp)) == "", f"expected deletion of U+{cp:04X}"
    # C1 controls are deleted
    for cp in range(0x80, 0xA0):
        assert remove_unsafe_chars(chr(cp)) == "", f"expected deletion of U+{cp:04X}"


def test_remove_unsafe_chars_spaces() -> None:
    # Unsafe space-like chars are replaced with a regular space
    for cp in [*range(0x2000, 0x200B), 0x2028, 0x2029, 0x0A00, 0x1680, 0x202F, 0x205F, 0x3000]:
        assert remove_unsafe_chars(chr(cp)) == " ", f"expected space for U+{cp:04X}"


def test_remove_unsafe_chars_invisible() -> None:
    # Zero-width and invisible formatting chars are deleted
    for cp in [*range(0x200B, 0x2010), 0x061C, *range(0x2060, 0x2065), 0x00AD, 0xFEFF]:
        assert remove_unsafe_chars(chr(cp)) == "", f"expected deletion of U+{cp:04X}"
    # Lone UTF-16 surrogates are deleted
    for cp in [0xD800, 0xDFFF, 0xD83D]:
        assert remove_unsafe_chars(chr(cp)) == "", f"expected deletion of U+{cp:04X}"


def test_remove_unsafe_chars_clean_passthrough() -> None:
    # Common clean strings are returned unchanged
    for text in ["hello", "Acme Corp.", "שלום", "шрека", "日本語"]:
        assert remove_unsafe_chars(text) == text


def test_collapse_spaces():
    assert collapse_spaces(None) is None  # type: ignore
    assert collapse_spaces("") is None
    assert collapse_spaces(" ") is None
    assert collapse_spaces("  ") is None
    assert collapse_spaces("\xa0") is None
    assert collapse_spaces(" \n ") is None
    assert collapse_spaces(" \n\n ") is None
    assert collapse_spaces(" \njfshdhdfjk\n ") == "jfshdhdfjk"
    assert collapse_spaces(" \njfshd\t\thdfjk\n ") == "jfshd hdfjk"
    assert collapse_spaces(" \n\u2028\u2029\u3000\n ") is None
    assert collapse_spaces("a\u3000x") == "a x"


def test_squash_spaces():
    assert squash_spaces("") == ""
    assert squash_spaces(" ") == ""
    assert squash_spaces("  ") == ""
    assert squash_spaces("\xa0") == ""
    assert squash_spaces(" \n ") == ""
    assert squash_spaces(" \n\n ") == ""
    assert squash_spaces(" \njfshdhdfjk\n ") == "jfshdhdfjk"
    assert squash_spaces(" \njfshd\t\thdfjk\n ") == "jfshd hdfjk"
    assert squash_spaces(" \n\u2028\u2029\u200b\u200c\n ") == ""
    assert squash_spaces("a\u3000x") == "a x"
    assert squash_spaces("a\u200bx") == "ax"
    # zero-width joiner / non-joiner deleted
    assert squash_spaces("a\u200cx") == "ax"
    assert squash_spaces("a\u200dx") == "ax"
    # soft hyphen deleted
    assert squash_spaces("a\u00adx") == "ax"
    # mid-string BOM deleted
    assert squash_spaces("a\ufeffe") == "ae"
    # word joiner and invisible operators deleted
    assert squash_spaces("a\u2060x") == "ax"
    assert squash_spaces("a\u2064x") == "ax"
    # mixed delete+space: zero-width between spaces collapses to single space
    assert squash_spaces("a\u200b\u2003x") == "a x"
