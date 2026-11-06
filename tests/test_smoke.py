import framework


def test_import_is_correct():
    title = framework.__name__
    assert title is not None
