More on command-line applications
===================================
horetu is just one of many ways to parse command-line arguments,
and it is quite limited in the sorts of command-line flags that it allows.
Here are some other tools for producing command-line argument parsers.

Low-level
^^^^^^^^^^^
At the lowest level, you can look at the value of :py:data:`sys.argv` and parse
them however you want. These are always a :py:class:`list` of :py:class:`str`
elements.

Standard parser modules
^^^^^^^^^^^^^^^^^^^^^^^^^^
Python comes with a few standard libraries for building command-line argument
parsers.

* :py:mod:`argparse`
* :py:mod:`optparse` (deprecated)

Other modules
^^^^^^^^^^^^^^^
There are also several third-party command-line argument parsers.
The `The Hitchhiker's Guide to Python <http://docs.python-guide.org/en/latest/scenarios/cli/>`_
suggests the following libraries.

* `clint <http://docs.python-guide.org/en/latest/>`_
* `click <http://click.pocoo.org/>`_
* `docopt <http://docopt.org/>`_
* `plac <https://pypi.python.org/pypi/plac>`_
* `cliff <http://docs.openstack.org/developer/cliff/>`_

It turns out that plac is especially similar to horetu.
Unfortunately, I discovered this only after writing horetu.
