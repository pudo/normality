from normality.scripts import ALPHABET, CYRILLIC, CJK
from normality.scripts import char_tags, is_modern_alphabet


def test_char_tags():
    assert ALPHABET in char_tags("a")
    assert CYRILLIC not in char_tags("a")
    assert CYRILLIC in char_tags("д")
    assert CJK in char_tags("近")
    assert ALPHABET not in char_tags("近")


def test_is_modern_alphabet():
    assert not is_modern_alphabet(" 习近平")
    assert is_modern_alphabet("Xí Jìnpíng")
    assert is_modern_alphabet("Ротенберг Аркадий")
    assert is_modern_alphabet(".,[]{}()!@#$%^&*()_+)«»‘“")
    assert not is_modern_alphabet("တပ်မတော်(ကြည်")
