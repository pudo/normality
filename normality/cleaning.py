import re

COLLAPSE_RE = re.compile(r'\s+', re.U)


def collapse_spaces(text):
	"""Remove newlines, tabs and multiple spaces with single spaces."""
	return COLLAPSE_RE.sub(' ', text).strip(' ')
