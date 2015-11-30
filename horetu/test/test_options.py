from inspect import Parameter, signature

from .. import options

def test_docs():
    assert list(options.docs(lambda:8)) == []

def test_description():
    assert options.description(lambda:8) == ''

def test_name_or_flags():
    param = Parameter('input_file', Parameter.POSITIONAL_ONLY,
                      default = Parameter.empty)
    assert options.name_or_flags(param) == 'input-file'

    param = Parameter('n_cores', Parameter.POSITIONAL_OR_KEYWORD,
                      default = 3)
    assert options.name_or_flags(param) == '--n-cores'

    param = Parameter('n', Parameter.POSITIONAL_OR_KEYWORD,
                      default = 3)
    assert options.name_or_flags(param) == '-n'

def test_action():
    def f(x, y: list = None, z: options.COUNT = 2):
        pass
    params = signature(f).parameters
    assert options.action(params['x']) == 'store'
    assert options.action(params['y']) == 'append'
    assert options.action(params['z']) == 'count'

def test_nargs():
    def f(x, y: options.OPTIONAL, *z):
        pass
    params = signature(f).parameters
    assert options.nargs(params['x']) == None
    assert options.nargs(params['y']) == '?'
    assert options.nargs(params['z']) == '*'
