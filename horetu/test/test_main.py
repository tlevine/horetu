import pytest

from ..main import horetu

def test_flat():
    def f():
        return 8
    assert horetu(f, name = None, description = None, _args = []) == 8

nest = [
    (['command1', '8', '2', '9'], 1),
    (['command2', '8', '2'], 16),
]

@pytest.mark.parametrize('args, expected', nest)
def test_nested(args, expected):
    def command1(a:int, b:int, c:int):
        return a + b - c
    def command2(a:int, b:int):
        return a * b
    def command3():
        return 2
    commands = {'command1': command1, 'command2': command2, 'command3': command3}
    observed = horetu(commands, _args = args, name = 'do-something')
    assert observed == expected

triple_nest = [
    (['aa', 'bb', '10', '3'], 30),
    (['aa', 'cc', 'BB'], 2),
]
@pytest.mark.parametrize('args, expected', triple_nest)
def test_triple_nested(args, expected):
    def command1(a:int, b:int, c:int):
        return a + b - c
    def command2(a:int, b:int):
        return a * b
    def command3():
        return 2
    commands = {'aa': {'bb': command2, 'cc': {'AA': command1, 'BB': command3}}}
    observed = horetu(commands, _args = args, name = 'do-something')
    assert observed == expected

