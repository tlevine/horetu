import pytest

from ..main import horetu

def test_flat():
    def f():
        return 8
    assert horetu(f, name = None, description = None, _args = []) == 8

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
    observed = horetu(fs, _args = args, name = 'do-something')
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
    observed = horetu(commands, _args = args, name = 'do-something')
    assert observed == expected

def test_version():
    def main(version = 'blah'):
        pass
    horetu(main, _args = ['--version'])
