from functools import partial
from inspect import Parameter, signature

import pytest

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

def test_choose_name_args():
    f = partial(options.choose_name_args, {'-n', '-h'}, False)
    param = Parameter('input_file', Parameter.POSITIONAL_ONLY,
                      default = Parameter.empty)
    assert f(options.Step.positional, param) == ('input_file',)

    param = Parameter('n_cores', Parameter.POSITIONAL_OR_KEYWORD,
                      default = 3)
    assert f(options.Step.keyword2, param) == ('--n-cores',)
    assert f(options.Step.positional, param) == ('n_cores',)

    param = Parameter('n', Parameter.POSITIONAL_OR_KEYWORD,
                      default = 3)
    assert f(options.Step.keyword1, param) == ('-n',)

#   def f(a, b = 8, *, d = 4):
#       pass
#   params = signature(f).parameters
#   print(params)
#   assert f(options.Step.keyword1, params['b']) == ('b',)

def test_bool():
    def f(force = False, waaa = True):
        pass
    params = signature(f).parameters
    force = params['force']
    waaa = params['waaa']
    assert options.action(options.Step.keyword1, force) == 'store_true'
    assert options.action(options.Step.keyword2, force) == 'store_true'
    assert options.action(options.Step.keyword1, waaa) == 'store_false'
    assert options.action(options.Step.keyword2, waaa) == 'store_false'

def test_action():
    def f(x, y: list=None, z: options.COUNT=2):
        pass
    params = signature(f).parameters
    assert options.action(options.Step.positional, params['x']) == 'store'
    assert options.action(options.Step.keyword1, params['y']) == 'append'
    assert options.action(options.Step.keyword1, params['z']) == 'count'
