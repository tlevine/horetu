from .. import options

def test_docs():
    assert list(options.docs(lambda:8)) == []
