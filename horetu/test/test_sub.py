import argparse

from ..sub import sub

def test_sub():
    def command1(a:int, b:int, c:int):
        return a + b - c
    def command2(a:int, b:int):
        return a * b
    def command3():
        return 2

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest = 'sub')
    g = sub(subparsers, [command1, command2, command3])
    
    args = parser.parse_args(['command1', '1', '2', '8'])
    assert args.sub == 'command1'
    assert args.a == 1
    assert args.b == 2
    assert args.c == 8

    assert set(g) == {'command1', 'command2', 'command3'}
    assert g['command1'](args) == -5
