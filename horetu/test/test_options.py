from functools import partial
from inspect import Parameter, signature

from .. import options

def test_docs_empty():
    assert list(options.docs(lambda:8)) == []

def test_docs_withtype():
    def f(abc):
        '''
        :param int abc: A word
        '''
        pass
    assert list(options.docs(f)) == [('abc', 'A word')]

def test_docs_withouttype():
    def hi(name: str, times: int = 8,
           case: ('title', 'lower', 'upper') = 'title'):
        '''
        :param name: Name
        :param times: Number of times to say hi
        :param case: Case of the greeting
        '''
        for _ in range(times):
            print('Hi ' + getattr(name, case)())

    assert list(options.docs(hi)) == [
        ('name', 'Name'),
        ('times', 'Number of times to say hi'),
        ('case', 'Case of the greeting'),
    ]

def test_description():
    assert options.description(lambda:8) == ''

def test_name_or_flag():
    f = partial(options.name_or_flag, False)
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
    assert options.name_or_flag(True, params['b']) == 'b'

def test_action():
    def f(x, y: list = None, z: options.Count = 2):
        pass
    params = signature(f).parameters
    assert options.action(params['x']) == 'store'
    assert options.action(params['y']) == 'append'
    assert options.action(params['z']) == 'count'

def test_nargs():
    def f(x, y: options.Option, *z):
        pass
    params = signature(f).parameters
    assert options.nargs(False, params['x']) == None
    assert options.nargs(False, params['y']) == '?'
    assert options.nargs(False, params['z']) == '*'

def test_bool():
    def f(force = False, waaa = True):
        pass
    params = signature(f).parameters
    force = params['force']
    waaa = params['waaa']
    assert options.action(force) == 'store_true'
    assert options.action(waaa) == 'store_false'
