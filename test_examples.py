import os
import subprocess
import pytest

testcases = [
    ('do_something.py', [], 2),
    ('getitem', [], 2),
    ('hi', [], 2),
    ('nest', [], 2),
#   ('requests', [], 0),
    ('spacecraft', [], 2),
]
@pytest.mark.parametrize('fn, args, returncode', testcases)
def test_example(fn, args, returncode):
    path = os.path.join('examples', fn)
    sp = subprocess.Popen([path] + args)
    assert sp.wait() == returncode
