# coding: utf-8
from normality import normalize, latinize_text, ascii_text, slugify

SAMPLES = [
    u'Порошенко Петро Олексійович',
    u'FUAD ALIYEV ƏHMƏD OĞLU',
    u'Häschen Spaß',
    u'ავლაბრის ფონდი',
]

for sample in SAMPLES:
    print 'SAMPLE :', sample
    print '  NORM :', normalize(sample)
    print '  SLUG :', slugify(sample)
    print '  LATIN:', latinize_text(sample)
    print '  ASCII:', ascii_text(sample)
