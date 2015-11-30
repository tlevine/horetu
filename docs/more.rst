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

* `aaargh <https://pypi.python.org/pypi/aaargh>`_
* `plac <https://pypi.python.org/pypi/plac>`_
* `opster <http://opster.readthedocs.org/en/latest/>`_
* `clint <http://docs.python-guide.org/en/latest/>`_
* `click <http://click.pocoo.org/>`_
* `docopt <http://docopt.org/>`_
* `cliff <http://docs.openstack.org/developer/cliff/>`_
* `clap <https://pypi.python.org/pypi/Clap/>`_ 
* `cement <https://pypi.python.org/pypi/cement>`_

It turns out that plac and aaargh are very especially similar to horetu.
Unfortunately, I discovered this only after writing horetu.

References

* `The Hitchhiker's Guide to Python <http://docs.python-guide.org/en/latest/scenarios/cli/>`_
* `aaargh readme <https://pypi.python.org/pypi/aaargh>`_
* `plac documentation <http://plac.googlecode.com/hg/doc/plac.html#trivia-the-story-behind-the-name>`_
