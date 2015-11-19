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

Argument names
------------------
Positional arguments keep the same names in the command-line interface,
except that underscores are replaced with hyphens.

Keyword arguments with single-character names are turned into one-hyphen flags,
and keyword arguments with longer names are turned into two-hyphen flags.
Also, underscores are replaced with hyphens.

::

    def main(some_file, some_password = None, n = 8):
        pass
    horetu(some_file, _args = ['--some-password', 'abc', '-n' '2'])

(XXX Next thing isn't implemented.)
horetu tries to turn long keyword arguments are also turned into
one-hyphen flags too, using the first letter as the flag.
It does this only when all keyword arguments have different first letters.

::

    def main(some_file, some_password = None, n = 8):
        pass
    horetu(some_file, _args = ['-s', 'abc', '-n' '2'])

If you specify clashing argument names (and the above situation doesn't count
as clashing), :py:module:`argparse` will raise an exception.

Default arguments
^^^^^^^^^^^^^^^^^^^


Number of arguments
^^^^^^^^^^^^^^^^^^^^^^
In most cases, horetu will produce an interface that expects one shell argument
to be passed for each Python argument. For example, the following interface
requires one "X", one "Y", and optionally, one "Z".

::

    def f(x, y, z = 'elephant'):
        pass
    horetu(f)

One exception is arbitrary argument lists, which take zero or more values;
the following interface takes exactly one "A" and zero or more "B".

::

    def f(a, *b):
        pass
    horetu(f)

The other exception is keyword arguments annotated with type :py:class:`list`.
(XXX This is not implemented.)

::
    def f(colors:list = None):
        pass
    horetu(f)

This last interface takes as many "COLORS" as you want and iterprets them as a
list. If you pass no colors, the value ``None`` is passed to ``colors``.

Annoyingly, because of how horetu is implemented with :py:mod:`argparse`,
if the default argument is a list, it is extended, rather than replaced,
with the new arguments.

::
    def f(colors:list = ['pink']):
        return colors
    >>> horetu(f, _args = ['--colors', 'green'])
    ['pink', 'green']


It would be neat if arguments that take multiple values would be named with
singular grammatical forms when appropriate in the command-line help. But they
don't. Oh well.

^^^^^^^^^^
^^^^^^^^^^

Final note
------------
You should think of horetu as a means of converting your Python function to a
shell interface rather than a means of creating a particular shell interface in
Python. Express your function cleanly and clearly in Python, and horetu will
make you a nice shell interface.
