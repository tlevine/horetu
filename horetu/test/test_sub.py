import argparse

from ..sub import sub, nest

def test_sub():
    def command1(a:int, b:int, c:int):
        return a + b - c
    def command2(a:int, b:int):
        return a * b
    def command3():
        return 2

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest = 'sub')
    g = sub(None, 'zero', subparsers, [command1, command2, command3])
    
    args = parser.parse_args(['command1', '1', '2', '8'])
    assert args.sub == 'command1'
    assert args.a == 1
    assert args.b == 2
    assert args.c == 8

    assert set(g) == {'command1', 'command2', 'command3'}
    assert g['command1'](args) == -5


def test_nest():
    def command1(a:int, b:int, c:int):
        return a + b - c
    def command2(a:int, b:int):
        return a * b
    def command3():
        return 2
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest = 'sub')

    g = nest(None, 'zero', subparsers,
        subcommands={'command1': command1, 'c2': command2, 'c3': command3})
    args = parser.parse_args(['command1', '1', '2', '8'])
    assert g['command1'](args) == -5

    g = nest(None, 'zero', subparsers,
        subcommands = {'x': {'command1': command1, 'c2': command2, 'c3': command3}})
    args = parser.parse_args(['x', 'command1', '1', '2', '8'])
    assert g['x']['command1'](args) == -5

    g = nest(None, 'zero', subparsers,
        subcommands = {'x': {'command1': command1}})
    args = parser.parse_args(['x', 'command1', '1', '2', '8'])
    assert g['x']['command1'](args) == -5

    g = nest(None, 'zero', subparsers, subcommands = {'x': command1})
    args = parser.parse_args(['x', '1', '2', '8'])
    assert g['x'](args) == -5

def test_nest_list():
    def command1(a:int, b:int, c:int):
        return a + b - c
    def command2(a:int, b:int):
        return a * b
    def command3():
        return 2
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest = 'sub')

    g = nest(None, 'zero', subparsers,
        commands=[command1, command2, command3])
    args = parser.parse_args(['command1', '1', '2', '8'])
    assert g['command1'](args) == -5
