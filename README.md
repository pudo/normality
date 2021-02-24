# normality

[![build](https://github.com/pudo/normality/actions/workflows/build.yml/badge.svg)](https://github.com/pudo/normality/actions/workflows/build.yml)

Normality is a Python micro-package that contains a small set of text
normalization functions for easier re-use. These functions accept a
snippet of unicode or utf-8 encoded text and remove various classes
of characters, such as diacritics, punctuation etc. This is useful as
a preparation to further text analysis.

**WARNING**: This library works much better when used in combination 
with ``pyicu``, a Python binding for the International Components for
Unicode C library. ICU provides much better text transliteration than
the default ``text-unidecode``.

## Example

```python
# coding: utf-8
from normality import normalize, slugify, collapse_spaces

text = normalize('Nie wieder "Grüne Süppchen" kochen!')
assert text == 'nie wieder grune suppchen kochen'

slug = slugify('My first blog post!')
assert slug == 'my-first-blog-post'

text = 'this \n\n\r\nhas\tlots of \nodd spacing.'
assert collapse_spaces(text) == 'this has lots of odd spacing.'
```

## License

``normality`` is open source, licensed under a standard MIT license
(included in this repository as ``LICENSE``).
