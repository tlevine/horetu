import os
import subprocess
import pytest

testcases = [
    ('do_something.py', [], 2),
    ('getitem', [], 2),
    ('hi', [], 2),
    ('nest', [], 2),
    ('spacecraft', [], 2),

    ('do_something.py', ['a file', 'another file'], 0),
    ('getitem', ['namedtuple', '-n', '2'], 0),
    ('hi', ['Tom'], 0),
    ('nest', ['subcommand2', '8'], 0),
    ('spacecraft', ['mars'], 0),

    ('do_something.py', ['a file'], 2),
    ('getitem', ['invalid', '-n', '2'], 2),
    ('hi', ['Tom', '-t', '3'], 0),
    ('nest', ['subcommand2', 'a'], 1),
    ('spacecraft', ['mars'], 0),
]
try:
    import requests
except ImportError:
    pass
else:
    testcases.extend([
        ('requests', ['-h'], 0),
        ('requests', ['get', '-h'], 0),
        ('requests', ['put'], 2),
        ('requests', ['post', 'badformat'], 1),
    ])
@pytest.mark.parametrize('fn, args, returncode', testcases)
def test_example(fn, args, returncode):
    path = os.path.join('examples', fn)
    sp = subprocess.Popen([path] + args)
    assert sp.wait() == returncode
