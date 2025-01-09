import unittest
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


class NormalityTest(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(None, slugify(None))
        self.assertEqual(None, ascii_text(None))
        self.assertEqual(None, latinize_text(None))
        self.assertEqual(None, normalize(None))
        self.assertEqual(None, normalize(""))
        self.assertEqual(None, normalize(" "))

    def test_petro(self):
        text = "Порошенко Петро Олексійович"
        self.assertEqual("porosenko-petro-oleksijovic", slugify(text))
        self.assertEqual("Porosenko Petro Oleksijovic", ascii_text(text))
        self.assertEqual("Porošenko Petro Oleksíjovič", latinize_text(text))
        self.assertEqual("порошенко петро олексіиович", normalize(text))

    def test_ahmad(self):
        text = "əhməd"
        self.assertEqual("ahmad", ascii_text(text))

    def test_azeri(self):
        text = "FUAD ALIYEV ƏHMƏD OĞLU"
        self.assertEqual("FUAD ALIYEV AHMAD OGLU", ascii_text(text))

    def test_slugify(self):
        text = "BABY! camel-is good"
        self.assertEqual("baby-camel-is-good", slugify(text, sep="-"))
        self.assertEqual("tests", slugify("testʼs", sep="-"))
        self.assertEqual("test-s", slugify("test_s", sep="-"))
        self.assertEqual(None, slugify("-", sep="-"))
        self.assertEqual(None, slugify("", sep="-"))
        self.assertEqual(None, slugify("- -", sep="-"))
        self.assertEqual(None, slugify(None, sep="-"))

    def test_georgian(self):
        text = "ავლაბრის ფონდი"
        self.assertEqual("avlabris pondi", ascii_text(text))

    def test_german(self):
        text = "Häschen Spaß"
        self.assertEqual("Haschen Spass", ascii_text(text))
        self.assertEqual("haschen-spass", slugify(text, sep="-"))

    def test_stringify(self):
        self.assertEqual(".", stringify(" . "))
        self.assertEqual("5", stringify(5))
        self.assertEqual("0.5", stringify(0.5))

    def test_stringify_datetime(self):
        dt = datetime.now(UTC)
        text = stringify(dt)
        self.assertTrue(text.startswith("%s-" % dt.year), text)

    def test_guess_encoding(self):
        text = "Порошенко Петро Олексійович"
        encoded = text.encode("iso-8859-5")
        out = guess_encoding(encoded)
        self.assertEqual("iso8859-5", out)

    def test_predict_encoding(self):
        text = "Порошенко Петро Олексійович"
        encoded = text.encode("iso-8859-5")
        out = predict_encoding(encoded)
        self.assertEqual("iso8859-5", out)

    def test_guess_file_encoding(self):
        with open("tests/fixtures/utf-16.txt", "rb") as fh:
            out = guess_file_encoding(fh)
            self.assertEqual("utf-16", out)

    def test_predict_file_encoding(self):
        with open("tests/fixtures/utf-16.txt", "rb") as fh:
            out = predict_file_encoding(fh)
            self.assertEqual("utf-16", out)

    def test_petro_iso_encoded(self):
        text = "Порошенко Петро Олексійович"
        encoded = text.encode("iso8859-5")
        out = stringify(encoded)
        self.assertEqual(text, out)

    def test_petro_utf16_encoded(self):
        text = "Порошенко Петро Олексійович"
        encoded = text.encode("utf-16")
        out = stringify(encoded)
        self.assertEqual(text, out)
