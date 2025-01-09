from normality.cleaning import remove_unsafe_chars, collapse_spaces


def test_remove_unsafe_chars():
    assert remove_unsafe_chars(None) is None
    assert remove_unsafe_chars("") == ""
    assert remove_unsafe_chars(" ") == " "
    assert remove_unsafe_chars("\u2028 ") == " "
    assert remove_unsafe_chars("\ufeff ") == " "
    assert remove_unsafe_chars("lalala\ufeff ") == "lalala\ufeff "
    assert remove_unsafe_chars("lalala\u200bx") == "lalalax"


def test_collapse_spaces():
    assert collapse_spaces(None) is None
    assert collapse_spaces("") == ""
    assert collapse_spaces(" ") == ""
    assert collapse_spaces("  ") == ""
    assert collapse_spaces(" \n ") == ""
    assert collapse_spaces(" \n\n ") == ""
    assert collapse_spaces(" \njfshdhdfjk\n ") == "jfshdhdfjk"
    assert collapse_spaces(" \n\u2028\u2029\u200b\u200c\n ") == ""
    assert collapse_spaces("a\u200bx") == "a x"
