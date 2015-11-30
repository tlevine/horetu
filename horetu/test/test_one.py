import argparse

import pytest

from ..one import one


def f(a, b, c = 'xxx'):
    return a + b + c

cases = [
    (f, ['1', '2'], '12xxx'),
]

@pytest.mark.parametrize('function, argv, result', cases)
def test_one(function, argv, result):
    parser = argparse.ArgumentParser()
    assert one(parser, function)(parser.parse_args(argv)) == result

class FakeParser(object):
    def __init__(self):
        self.names_or_flags = set()
    def add_argument(self, *args, **kwargs):
        for a in args:
            if isinstance(a, str):
                self.names_or_flags.add(a)

def g(verbose = False):
    pass

def h(thing, blah = 8, blub = 9, turtle = 10):
    pass

flag_cases = [
    (f, {'a', 'b', '-c'}),
    (g, {'--verbose', '-v'}),
    (h, {'--blah', '--blub', '--turtle', '-t', 'thing'}),
]

@pytest.mark.parametrize('function, names_or_flags', flag_cases)
def test_flags(function, names_or_flags):
    parser = FakeParser()
    one(parser, function)
    assert parser.names_or_flags == names_or_flags
