import configparser
import os
import pytest

from .. import horetu

def simple(a:int = 0, aoeu:int = 8, bloeu:int = 3):
    return a + bloeu

multiple = {
    'aa': lambda x: x + 'boop',
    'bb': simple,
    'cc': lambda x,y=4,z=1:int(x)+int(y)+int(z),
}

cases = [
    ('simple.ini', simple, [], 7),
    ('multiple.ini', multiple, ['aa', 'beep'], 'beepboop'),
    ('multiple.ini', multiple, ['bb'], 4),
    ('multiple.ini', multiple, ['cc', '3', '-y', '8'], 12),
]
@pytest.mark.parametrize('filename, function, argv, result', cases)
def test_file(filename, function, argv, result):
    config = os.path.abspath(os.path.join(__file__, '..', 'configuration-files', filename))
    observed = horetu(function, config=config, args = argv)
    assert observed == result
