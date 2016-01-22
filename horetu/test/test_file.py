import configparser
import os
import pytest

from .. import horetu

def simple(a = 0, aoeu = 8, bloeu = 3):
    return a + bloeu

cases = [
    ('simple.ini', simple, [], 7),
]
@pytest.mark.parametrize('filename, function, argv, result', cases)
def test_file(filename, function, argv, result):
    config = os.path.abspath(os.path.join(__file__, '..', 'configuration-files', filename))
    observed = horetu(function, config=config, args = argv)
    assert observed == result
