import pytest

from normality import stringify
from normality.cleaning import remove_unsafe_chars

BIDI_CONTROLS = [*range(0x202A, 0x202F), *range(0x2066, 0x206A)]
BIDI_IDS = [f"U+{codepoint:04X}" for codepoint in BIDI_CONTROLS]


@pytest.mark.parametrize("codepoint", BIDI_CONTROLS, ids=BIDI_IDS)
def test_remove_unsafe_chars_bidi_controls(codepoint: int) -> None:
    char = chr(codepoint)
    assert remove_unsafe_chars(char) == ""
    assert remove_unsafe_chars(f"left{char}right") == "leftright"


@pytest.mark.parametrize("codepoint", BIDI_CONTROLS, ids=BIDI_IDS)
def test_stringify_bytes_bidi_controls(codepoint: int) -> None:
    text = f"left{chr(codepoint)}right"
    assert stringify(text.encode("utf-8"), encoding="utf-8") == "leftright"


@pytest.mark.parametrize(
    "text",
    [
        (
            "Français Español Português Deutsch Nederlands Polski Svenska"
            " Norsk Dansk Suomi Eesti Lietuvių Magyar Türkçe"
        ),
        "Русский Українська",
        "العربية",
        "中文",
        "日本語",
        "한국어",
        "\u0600\u06dd",  # Visible Arabic format characters remain intact.
        "\t\n\r",
    ],
)
def test_remove_unsafe_chars_preserves_other_text(text: str) -> None:
    assert remove_unsafe_chars(text) == text
