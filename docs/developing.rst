Developing
==============
Clone the git repository. ::

    git clone git://github.com/tlevine/horetu

The module code is in the ``horetu`` directory.

Install additional development dependencies. ::

    pip install -e .[dev]

Build documentation like this. ::

    cd docs && make html

Run tests like this. ::

    py.test
