from inspect import Parameter

from .. import options

def test_docs():
    assert list(options.docs(lambda:8)) == []

def test_description():
    assert options.description(lambda:8) == ''

def test_name_or_flags():
    param = Parameter('input_file', Parameter.POSITIONAL_ONLY)
    assert options.name_or_flags(param) == 'input-file'

    param = Parameter('n_cores', Parameter.POSITIONAL_OR_KEYWORD)
    assert options.name_or_flags(param) == '--n-cores'

    param = Parameter('n', Parameter.POSITIONAL_OR_KEYWORD)
    assert options.name_or_flags(param) == '-n'
