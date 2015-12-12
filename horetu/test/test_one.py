import argparse

import pytest

from ..one import one


def f(a, b, c = 'xxx'):
    return a + b + c

def g(host = 'blah', port = 'blah'):
    pass

def h(*args):
    return len(args)

cases = [
    (f, ['1', '2'], '12xxx'),
    (g, ['-p', '8888'], None),
    (h, ['a', 'b', 'd', 'c'], 4),
]

@pytest.mark.parametrize('function, argv, result', cases)
def test_one(function, argv, result):
    parser = argparse.ArgumentParser()
    assert one(parser, function)(parser.parse_args(argv)) == result

class FakeParser(object):
    def __init__(self):
        self.optional_names_or_flags = set()
    def add_argument(self, *args, **kwargs):
        for a in args:
            if isinstance(a, str):
                self.optional_names_or_flags.add(a)

def g(verbose = False):
    pass

def h(thing, blah = 8, blub = 9, turtle = 10):
    pass

def i(some_file, some_password = None, n = 8):
    pass

def plural_thing(things:list = None):
    pass

flag_cases = [
    (f, {'a', 'b', '-c'}),
    (g, {'--verbose', '-v'}),
    (h, {'--blah', '--blub', '--turtle', '-t', 'thing'}),
    (i, {'some_file', '--some-password', '-s', '-n'}),
    (plural_thing, {'--thing', '-t'}),
]

@pytest.mark.parametrize('function, optional_names_or_flags', flag_cases)
def test_flags(function, optional_names_or_flags):
    parser = FakeParser()
    one(parser, function)
    assert parser.optional_names_or_flags == optional_names_or_flags
