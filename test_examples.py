import os
import shutil
import importlib
import tempfile
import pytest

@pytest.mark.parametrize('fn', os.listdir('examples'))
def test_example(fn):
    prevdir = os.getcwd()
    path = os.path.join('examples', fn)
    with tempfile.TemporaryDirectory() as tmp:
        shutil.copy(path, os.path.join(tmp, 'example.py'))
        os.chdir(tmp)
        importlib.import_module('example')
    os.chdir(prevdir)
