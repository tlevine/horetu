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
    g = sub(parser, 'sub', {'c1': command1, 'c2': command2, 'c3': command3}) 
    
    args = parser.parse_args(['c1', '1', '2', '3'])
    assert args.sub == 'c1'
    assert args.a == 1
    assert args.b == 2
    assert args.c == 3
