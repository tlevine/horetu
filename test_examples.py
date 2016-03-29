import os
import subprocess
import pytest

testcases = [
    ('annotate', [], 0),
    ('do_something.py', [], 0),
    ('getitem', [], 0),
    ('hi', [], 0),
    ('nest', [], 0),
    ('requests', [], 0),
    ('spacecraft', [], 0),
]
@pytest.mark.parametrize('fn, args, returncode', testcases)
def test_example(fn, args, returncode):
    path = os.path.join('examples', fn)
    sp = subprocess.Popen([path] + args)
    assert sp.wait() == returncode
