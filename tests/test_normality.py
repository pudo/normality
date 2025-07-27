from datetime import datetime, UTC

from normality import normalize, latinize_text, ascii_text
from normality import (
    stringify,
    slugify,
    guess_encoding,
    guess_file_encoding,
    predict_file_encoding,
    predict_encoding,
)


def test_empty():
    assert slugify(None) is None
    assert ascii_text(None) == ""  # type: ignore
    assert ascii_text("") == ""
    assert latinize_text(None) == ""  # latinize_text returns empty string for None
    assert normalize(None) is None
    assert normalize("") is None
    assert normalize(" ") is None


def test_petro():
    text = "Порошенко Петро Олексійович"
    assert slugify(text) == "porosenko-petro-oleksijovic"
    assert ascii_text(text) == "Porosenko Petro Oleksijovic"
    assert latinize_text(text) == "Porošenko Petro Oleksíjovič"
    assert normalize(text) == "порошенко петро олексіиович"


def test_ahmad():
    text = "əhməd"
    assert ascii_text(text) == "ahmad"


def test_azeri():
    text = "FUAD ALIYEV ƏHMƏD OĞLU"
    assert ascii_text(text) == "FUAD ALIYEV AHMAD OGLU"


def test_slugify():
    text = "BABY! camel-is good"
    assert slugify(text, sep="-") == "baby-camel-is-good"
    assert slugify("testʼs", sep="-") == "tests"
    assert slugify("test_s", sep="-") == "test-s"
    assert slugify("-", sep="-") is None
    assert slugify("", sep="-") is None
    assert slugify("- -", sep="-") is None
    assert slugify(None, sep="-") is None


def test_georgian():
    text = "ავლაბრის ფონდი"
    assert ascii_text(text) == "avlabris pondi"


def test_german():
    text = "Häschen Spaß"
    assert ascii_text(text) == "Haschen Spass"
    assert slugify(text, sep="-") == "haschen-spass"


def test_stringify():
    assert stringify(" . ") == "."
    assert stringify(5) == "5"
    assert stringify(0.5) == "0.5"


def test_stringify_datetime():
    dt = datetime.now(UTC)
    text = stringify(dt)
    assert text is not None
    assert text.startswith("%s-" % dt.year), text


def test_guess_encoding():
    text = "Порошенко Петро Олексійович"
    encoded = text.encode("iso-8859-5")
    out = guess_encoding(encoded)
    assert out == "iso8859-5"


def test_predict_encoding():
    text = "Порошенко Петро Олексійович"
    encoded = text.encode("iso-8859-5")
    out = predict_encoding(encoded)
    assert out == "iso8859-5"


def test_guess_file_encoding():
    with open("tests/fixtures/utf-16.txt", "rb") as fh:
        out = guess_file_encoding(fh)
        assert out == "utf-16"


def test_predict_file_encoding():
    with open("tests/fixtures/utf-16.txt", "rb") as fh:
        out = predict_file_encoding(fh)
        assert out == "utf-16"


def test_petro_iso_encoded():
    text = "Порошенко Петро Олексійович"
    encoded = text.encode("iso8859-5")
    out = stringify(encoded)
    assert out == text


def test_petro_utf16_encoded():
    text = "Порошенко Петро Олексійович"
    encoded = text.encode("utf-16")
    out = stringify(encoded)
    assert out == text
