# coding: utf-8
import unittest
from datetime import datetime

from normality import normalize, latinize_text, ascii_text
from normality import stringify, slugify


# these tests assume PyICU is installed
class NormalityTest(unittest.TestCase):

    def test_petro(self):
        text = u'Порошенко Петро Олексійович'
        self.assertEqual('porosenko-petro-oleksijovic', slugify(text))
        self.assertEqual('Porosenko Petro Oleksijovic', ascii_text(text))
        self.assertEqual(u'Porošenko Petro Oleksíjovič', latinize_text(text))
        self.assertEqual(u'порошенко петро олексіиович', normalize(text))

    def test_ahmad(self):
        text = u'FUAD ALIYEV ƏHMƏD OĞLU'
        self.assertEqual('FUAD ALIYEV AHMAD OGLU', ascii_text(text))

    def test_georgian(self):
        text = u'ავლაბრის ფონდი'
        self.assertEqual('avlabris pondi', ascii_text(text))

    def test_german(self):
        text = u'Häschen Spaß'
        self.assertEqual('Haschen Spass', ascii_text(text))

    def test_stringify_datetime(self):
        dt = datetime.utcnow()
        text = stringify(dt)
        self.assertTrue(text.startswith('%s-' % dt.year), text)

    def test_petro_iso_encoded(self):
        text = u'Порошенко Петро Олексійович'
        encoded = text.encode('iso-8859-5')
        out = stringify(encoded)
        self.assertEqual(text, out)

    def test_petro_utf16_encoded(self):
        text = u'Порошенко Петро Олексійович'
        encoded = text.encode('utf-16')
        out = stringify(encoded)
        self.assertEqual(text, out)
