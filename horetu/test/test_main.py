import pytest

from ..main import horetu

def test_flat():
    def f():
        return 8
    assert horetu(f, name = None, description = None, _args = []) == 8

nest = [
    (['c1', '8', '2', '9'], 1),
]

@pytest.mark.parametrize('args, expected', nest)
def test_nested(args, expected):
    def command1(a, b, c):
        return a + b - c
    def command2(a, b):
        return a * b
    def command3():
        return 2
    observed = horetu({'c1': command1, 'c2': command2, 'c3': command3}, _args = args)
    assert observed == expected

