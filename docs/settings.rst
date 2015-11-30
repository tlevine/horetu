.. testsetup::

    import argparse

    import horetu

Settings
==========
As much as possible, horetu tries come up with an interface based on things
that you have probably already specified in your function definition, such
as positional arguments, keyword arguments, type annotations, docstrings,
and the function name. The program-wide settings that can fall back to values
that you explicitly pass to horetu.

Program-wide settings
------------------------------
horetu supports the following program-wide settings.

name
    Displayed in the command-line help
description
    Displayed in the command-line help
version
    Add a ``--version`` flag that displays the version and exits.

Each of these can be set in the call to horetu.

.. autofunction:: horetu.horetu

The name is determined thusly.

1. Use the name keyword argument passed to horetu (``name``) if it is available.
2. If a function, rather than a dictionary, is passed as ``f``, use the function's
   name (``f.__name__``).
3. Otherwise, use the first argv (``sys.argv[0]``).

The description is determined thusly.

1. Use the description keyword argument passed to horetu (``description``) if
   it is available.
2. If a function, rather than a dictionary, is passed as ``f``, and the
   function has a docstring, use the first line of the function's docstring.
3. Otherwise, don't include a description.

Parameter-specific settings
----------------------------
Parameter-specific settings are set in all kinds of different places.

Help
^^^^^^^^^^
Help is taken from parameter annotations in the docstring; in the following
function,

.. testcode::

    def main(n_cores: int = 8):
        '''
        :param int n_cores: Number of cores to use for processing
        '''

"Number of cores to use for processing" is used as the help text for
the parameter ``n_cores``.

Argument names
^^^^^^^^^^^^^^^^^^
Positional arguments keep the same names in the command-line interface,
except that underscores are replaced with hyphens.

Keyword arguments with single-character names are turned into one-hyphen flags,
and keyword arguments with longer names are turned into two-hyphen flags.
Also, underscores are replaced with hyphens.

.. testcode::

    def main(some_file, some_password = None, n = 8):
        pass
    horetu.horetu(some_file, _args = ['--some-password', 'abc', '-n' '2'])

horetu tries to turn long keyword arguments are also turned into
one-hyphen flags too, using the first letter as the flag.
It does this only when all keyword arguments have different first letters.

.. testcode::

    def main(some_file, some_password = None, n = 8):
        pass
    horetu.horetu(some_file, _args = ['-s', 'abc', '-n' '2'])

Default arguments
^^^^^^^^^^^^^^^^^^^
Positional arguments produce required shell arguments, and keyword arguments
produce optional shell arguments. If the keyword argument is not specified in
the shell, the function uses the default that is set in the function definition.

List-type arguments
^^^^^^^^^^^^^^^^^^^^^^
In most cases, horetu will produce an interface that expects one shell argument
to be passed for each Python argument. For example, the following interface
requires one "X", one "Y", and optionally, one "Z".

.. testcode::

    def f(x, y, z = 'elephant'):
        pass
    horetu.horetu(f)

In some cases horetu accepts several shell arguments and turns them into a list.
One such situation is var-positional arguments, which take zero or more values;
the following interface takes exactly one "A" and zero or more "B".

.. testcode::

    def f(a, \*b):
        pass
    horetu.horetu(f)

The other situation is keyword arguments annotated with type :py:class:`list`.

.. testcode::

    def f(colors: list = None):
        pass
    horetu.horetu(f)

This last interface takes as many "COLORS" as you want and iterprets them as a
list. If you pass no colors, the value ``None`` is passed as ``colors``.

Annoyingly, because of how horetu is implemented with :py:mod:`argparse`,
if the default argument is a list, it is extended, rather than replaced,
with the new arguments.

.. testcode::

    def f(colors: list = ['pink']):
        return colors
    >>> horetu(f, _args = ['--colors', 'green'])
    ['pink', 'green']


It would be neat if arguments that take multiple values would be named with
singular grammatical forms when appropriate in the command-line help. But they
don't. Oh well.

Choices
^^^^^^^^^^
Annotate a parameter with a tuple to limit choices for that particular
parameter. For example, this succeeds,

.. testcode::

    def scrape(output_format: ('web', 'level'), destination):
        '''
        :param output_format: Output to the web server or directly to leveldb?
        :param destination: Domain name (web output) or database path (leveldb)
        '''
        return {
            'web': scraper.web,
            'level': scraper.level,
        }[output_format](destination)
    horetu.horetu(scrape, _args = ['level', '/blah'])

and this fails.

::

    horetu.horetu(scrape, _args = ['not-a-choice', '/blah'])

Argument type
^^^^^^^^^^^^^^^^
If you annotate a parameter with something other than the special values
referenced above, horetu (really :py:mod:`argparse`) will call that something
on the string that is passed in the shell arguments and print a reasonable
error message if the parse fails.

::

    def main(n: int, infile: argparse.FileType('rb')):
        pass
    horetu.horetu(main, _args = ['not-a-number'])

Boolean flags
^^^^^^^^^^^^^^^^
Keyword arguments with default values of ``True`` or ``False`` turn into flags
that do not take additional arguments. Passing the flag switches the value to
be opposite the default.

.. testcode::

    def main(force = False):
        pass
    horetu.horetu(main, _args = ['--force'])

Counting
^^^^^^^^^^^^^
Annotate a parameter with :py:data:`horetu.COUNT` to count the number of times
the argument appears. The number of flags is added to the default value.

.. testcode::

    def main(verbose: horetu.COUNT = 1):
        pass
    horetu.horetu(main, _args = []) # verbose = 1
    horetu.horetu(main, _args = ['-v', '-v']) # verbose = 3

Optional arguments
^^^^^^^^^^^^^^^^^^^^^^
Annotate a positional argument with :py:data:`horetu.OPTIONAL` to make it
optional; if that argument isn't passed in the command line we will use
``None`` as its value.

.. testcode::

    def main(infile: horetu.OPTIONAL, *outfiles):
        pass

Final note on settings
-----------------------
You should think of horetu as a means of converting your Python function to a
shell interface rather than a means of creating a particular shell interface in
Python. Express your function cleanly and clearly in Python, and horetu will
make you a nice shell interface.
