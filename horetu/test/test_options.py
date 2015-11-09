from .. import options

def test_docs():
    assert list(options.docs(lambda:8)) == []

def test_description():
    assert options.description(lambda:8) == ''
