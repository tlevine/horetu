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

References

* `The Hitchhiker's Guide to Python <http://docs.python-guide.org/en/latest/scenarios/cli/>`_
* `aaargh readme <https://pypi.python.org/pypi/aaargh>`_
* `plac documentation <http://plac.googlecode.com/hg/doc/plac.html#trivia-the-story-behind-the-name>`_

Similar modules
^^^^^^^^^^^^^^^^^^
After writing horetu, I discovered plac and aargh.
It turns out that plac and aaargh are very especially similar to horetu,
but horetu is mostly better, even at its early stage of development.

Of plac and aaargh, I think plac is generally better.
Here are some features that plac has and horetu doesn't.

* Works in Python 2
* Does not depend on docstring
* Consumes generators
* Supports variable keyword arguments (``**kwargs``)
* Supports interactive programs
* Has some helpers for parallel processing
* Supports socket interfaces rather than command-line interfaces

I see most of these features as beyond the scope of a command-line
interface specification library; the main advantage I see is that it
works in Python 2.

Here are some features that horetu has and plac doesn't

* Converts keyword arguments into --flags
* Reads help in the docstring
* Parses raw strings as the annotated types
* Uses simple dictionaries to specify subcommands

Moreover, I have concluded that plac is the best of the alternatives;
all of the others lack either in magic or in features.

These are very similar and lacking features.

* http://plac.googlecode.com/hg/doc/plac.html
* https://pypi.python.org/pypi/opterator
* https://pypi.python.org/pypi/CLIArgs
* https://pypi.python.org/pypi/commandline

These have nice syntax for subcommands.

* http://pythonhosted.org/argh/
* https://pypi.python.org/pypi/aaargh

These are more complicated

* https://pythonhosted.org/cmd2/index.html
* https://docs.python.org/3.5/library/cmd.html

Here's a fuller list.

* opterator
* CLIArgs
* commandline
* cmd2
* argh
* aaargh
* opster
* clint
* click
* docopt
* cliff
* clap
* cement
* all of the standard command-line parsing modules
