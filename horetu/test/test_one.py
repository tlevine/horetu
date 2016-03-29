import argparse

import pytest

from ..one import one

def f(a, b, c = 'xxx'):
    return a + b + c

def g(host = 'blah', port: int = 'blah'):
    return host, port

def h(*args):
    return len(args)

def i(x):
    '''
    :param x: Something to return
    '''
    return x

def j(x: float):
    return x

def k(a, b = None, *, c = 8, d = 4):
    return a, b

def Folder(x):
    if x.startswith('+'):
        return x[1:]
    else:
        raise ValueError('Folders must start with "+".')

def optional_with_types(folder: Folder = None, msg: str = None):
    return folder, msg

cases = [
    (f, ['1', '2'], '12xxx'),
    (g, ['-p', '8888'], ('blah', 8888)),
    (h, ['a', 'b', 'd', 'c'], 4),
    (i, ['aoeu'], 'aoeu'),
    (j, ['8.4'], 8.4),
    (k, ['aoeu'], ('aoeu', None)),
#   (optional_with_types, ['+INBOX', 'blah@blah.blah'], ('INBOX', 'blah@blah.blah')),
#   (optional_with_types, ['blah@blah.blah'], (None, 'blah@blah.blah')),
]

@pytest.mark.parametrize('function, argv, result', cases)
def test_one(function, argv, result):
    parser = argparse.ArgumentParser()
    assert one(None, None, parser, function)(parser.parse_args(argv)) == result

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
    one(None, None, parser, function)
    assert parser.optional_names_or_flags == optional_names_or_flags
