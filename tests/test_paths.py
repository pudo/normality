from normality.paths import MAX_LENGTH, safe_filename


def test_safe_filename():
    assert safe_filename(None) is None
    assert safe_filename("test.txt") == "test.txt"
    assert safe_filename("test .txt") == "test.txt"
    assert safe_filename("test bla.txt") == "test_bla.txt"
    assert safe_filename("test_bla.txt") == "test_bla.txt"
    assert safe_filename("test.bla.txt") == "test_bla.txt"
    assert safe_filename("test", extension="txt") == "test.txt"


def test_long_filename():
    long_name = ["long name"] * 100
    long_name = "-".join(long_name)

    shortened = safe_filename(long_name)
    assert shortened is not None
    assert len(shortened) <= MAX_LENGTH, shortened

    shortened = safe_filename(long_name, extension="html")
    assert shortened is not None
    assert len(shortened) <= MAX_LENGTH, shortened

    shortened = safe_filename("bla", extension=long_name)
    assert shortened is not None
    assert len(shortened) <= MAX_LENGTH, shortened

    shortened = safe_filename(long_name, extension=long_name)
    assert shortened is not None
    assert len(shortened) <= MAX_LENGTH, shortened
