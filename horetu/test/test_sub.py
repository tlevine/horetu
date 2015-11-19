import argparse

from ..sub import sub

def test_triple_nested():
    def command1(a:int, b:int, c:int):
        return a + b - c
    def command2(a:int, b:int):
        return a * b
    def command3():
        return 2

    parser = argparse.ArgumentParser()
    g = sub(parser, 'sub', [command1, command2, command3])
    
    args = parser.parse_args(['command1', '1', '2', '3'])
    assert args.sub == 'command1'
    assert args.a == 1
    assert args.b == 2
    assert args.c == 3

    assert set(g) == {'command1', 'command2', 'command3'}
