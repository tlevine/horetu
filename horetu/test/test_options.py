from inspect import Parameter, signature

from .. import options

def test_docs():
    assert list(options.docs(lambda:8)) == []

def test_description():
    assert options.description(lambda:8) == ''

def test_name_or_flags():
    f = options.name_or_flags([])
    param = Parameter('input_file', Parameter.POSITIONAL_ONLY,
                      default = Parameter.empty)
    assert f(param) == 'input_file'

    param = Parameter('n_cores', Parameter.POSITIONAL_OR_KEYWORD,
                      default = 3)
    assert f(param) == '--n-cores'

    param = Parameter('n', Parameter.POSITIONAL_OR_KEYWORD,
                      default = 3)
    assert f(param) == '-n'

    def f(a, b = 8, *, d = 4):
        pass
    params = signature(f).parameters
    assert options.name_or_flags(params)(params['b']) == 'b'

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

def test_bool():
    def f(force = False, waaa = True):
        pass
    params = signature(f).parameters
    force = params['force']
    waaa = params['waaa']
    assert options.default(force) == None
    assert options.action(force) == 'store_true'
    assert options.default(waaa) == None
    assert options.action(waaa) == 'store_false'
