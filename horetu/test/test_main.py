import pytest

from ..main import horetu

def test_optional_positional():
    def f(required:int, optional_positional:int=0, *, kwarg:int=8):
        return required + optional_positional + kwarg
    assert horetu(f, ['2']) == 10
    assert horetu(f, ['2', '100']) == 110
    assert horetu(f, ['2', '--kwarg', '3', '100']) == 105

def test_flat():
    def f():
        return 8
    assert horetu(f, name = None, description = None, args = []) == 8

nest = [
    (['f1', '8', '2', '9'], 1),
    (['f2', '8', '2'], 16),
]

@pytest.mark.parametrize('args, expected', nest)
def test_nested(args, expected):
    def f1(a:int, b:int, c:int):
        return a + b - c
    def f2(a:int, b:int):
        return a * b
    def f3():
        return 2
    fs = {'f1': f1, 'f2': f2, 'f3': f3}
    observed = horetu(fs, args = args, name = 'do-something')
    assert observed == expected

triple_nest = [
 #  (['aa', 'bb', '10', '3'], 30),
    (['aa', 'cc', 'BB'], 2),
 #  (['zz'], 8),
]
@pytest.mark.parametrize('args, expected', triple_nest)
def test_triple_nested(args, expected):
    def command1(a:int, b:int, c:int):
        return a + b - c
    def command2(a:int, b:int):
        return a * b
    def command3():
        return 2
    commands = {'aa': {'bb': command2, 'cc': {'AA': command1, 'BB': command3}}, 'zz': lambda: 8}
    observed = horetu(commands, args = args, name = 'do-something')
    assert observed == expected

def test_version():
    def main():
        pass
    try:
        horetu(main, args = ['--version'], version = 'blah')
    except SystemExit as e:
        assert e.args[0] == 0
    else:
        raise AssertionError('Version should be printed.')

def test_choices():
    def main(output_format: ('groff', 'RUNOFF')):
        assert output_format == 'RUNOFF'

    horetu(main, args = ['RUNOFF'])

    try:
        horetu(main, args = ['troff'])
    except SystemExit as e:
        assert e.args[0] == 2
    else:
        raise AssertionError('This should fail.')

def test_annotate_list():
    def f(colors: list = ['pink']):
        assert colors == ['pink', 'green']
    horetu(f, args = ['--color', 'green'])

def test_hyphen():
    def main(some_file, some_password = None, n = 8):
        pass
    horetu(main, args = ['toilets.csv', '-s', 'abc', '-n' '2'])
