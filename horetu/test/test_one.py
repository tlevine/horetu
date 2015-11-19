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
