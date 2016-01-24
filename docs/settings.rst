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

These are the steps for determining the name.

1. Use the name keyword argument passed to horetu (``name``) if it is available.
2. If a function, rather than a dictionary, is passed as ``f``, use the function's
   name (``f.__name__``).
3. Otherwise, use the first argv (``sys.argv[0]``).

And these are the steps for determining the description.

1. Use the description keyword argument passed to horetu (``description``) if
   it is available.
2. If a function, rather than a dictionary, is passed as ``f``, and the
   function has a docstring, use the first line of the function's docstring.
3. Otherwise, don't include a description.

Parameter-specific settings
----------------------------
Parameter-specific settings are set all over the place.

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

Fun fact: I wanted to use the docstring parser from Sphinx, but it turns out
to be just a regular expression encapsulated under many layers of abstraction.
So I just wrote my own.

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
    horetu.horetu(main, ['chainsaws.csv', '--some-password', 'abc', '-n' '2'])

horetu tries to turn long keyword arguments are also turned into
one-hyphen flags too, using the first letter as the flag.
It does this only when all keyword arguments have different first letters.

.. testcode::

    def main(some_file, some_password = None, n = 8):
        pass
    horetu.horetu(main, ['toilets.csv', '-s', 'abc', '-n' '2'])

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
    horetu.horetu(f, ['one', 'two', '-z', 'three'])

In some cases horetu accepts several shell arguments and turns them into a list.
One such situation is var-positional arguments, which take zero or more values;
the following interface takes exactly one "A" and zero or more "B".

.. testcode::

    def f(a, *b):
        pass
    horetu.horetu(f, ['one'])
    horetu.horetu(f, ['one', 'two', 'three'])

The other situation is keyword arguments annotated with type :py:class:`list`.

.. testcode::

    def f(color: list = None):
        pass
    horetu.horetu(f, [])
    horetu.horetu(f, ['--color', 'pink', '--color', 'cyan'])

This interface takes as many colors as you want and interprets them as a
list. If you pass no colors, the value ``None`` is passed as ``colors``.

When keyword arguments are annotated with :py:class:`list` and are plural
English words, the resulting flags are named with the singular equivalent.
So we can switch the argument name from ``color`` to ``colors``.

.. testcode::

    def f(colors: list = None):
        pass
    horetu.horetu(f, ['--color', 'pink', '--color', 'cyan'])

Annoyingly, because of how horetu is implemented with :py:mod:`argparse`,
if the default argument is a list, it is extended, rather than replaced,
with the new arguments.

.. testcode::

    def f(colors: list = ['pink']):
        print(colors)
    horetu.horetu(f, ['--color', 'green'])

.. testoutput::

    ['pink', 'green']

Choices
^^^^^^^^^^
Annotate a parameter with a tuple to limit choices for that particular
parameter. For example, this succeeds,

.. testcode::

    def web(dest):
        pass
    def level(dest):
        pass

    def scrape(output_format: ('web', 'level'), destination):
        '''
        :param output_format: Output to the web server or directly to leveldb?
        :param destination: Domain name (web output) or database path (leveldb)
        '''
        return {
            'web': web,
            'level': level,
        }[output_format](destination)
    horetu.horetu(scrape, ['level', '/blah'])

and this fails.

::

    horetu.horetu(scrape, ['not-a-choice', '/blah'])

Argument type
^^^^^^^^^^^^^^^^
If you annotate a parameter with something other than the special values
referenced above, horetu (really :py:mod:`argparse`) will call that something
on the string that is passed in the shell arguments and print a reasonable
error message if the parse fails.

::

    def main(n: int, infile: argparse.FileType('rb')):
        pass
    horetu.horetu(main, ['not-a-number'])

Boolean flags
^^^^^^^^^^^^^^^^
Keyword arguments with default values of ``True`` or ``False`` turn into flags
that do not take additional arguments. Passing the flag switches the value to
be opposite the default.

.. testcode::

    def main(force = False):
        pass
    horetu.horetu(main, ['--force'])

Counting
^^^^^^^^^^^^^
Annotate a parameter with :py:data:`horetu.COUNT` to count the number of times
the argument appears. The number of flags is added to the default value.

.. testcode::

    def main(verbose: horetu.COUNT = 1):
        pass
    horetu.horetu(main, []) # verbose = 1
    horetu.horetu(main, ['-v', '-v']) # verbose = 3

Optional arguments
^^^^^^^^^^^^^^^^^^^^^^
There are two (three?) ways to make a positional argument optional.

I prefer this first method, but it only works in Python 3.

.. testcode::

    import sys
    def main(start = 0, stop = 1000, *, output = sys.stdout):
        pass

``start`` and ``stop`` become positional arguments with the defaults
of 0 and 1000, respectively. In Python, ``*`` tells us that the following
keyword arguments must be addressed as keyword arguments, not as positional
arguments. ``output`` becomes the flag ``--output/-o``.

Python 2 does not have built-in ignoring of variable positional arguments,
so you have to name the variable positional argument. Since this would
otherwise create an entry in the command-line interface, annotate that
argument with :py:data:`horetu.Ignore`.

.. testcode::

    import sys
    @annotate(int, int, horetu.Ignore)
    def main(start = 0, stop = 1000, *_ignore):
        pass

Unfortunately, Python 2 does not support keyword-only arguments (:pep:`3102`)
either, so the only way to create the above ``output`` keyword argument would
be with a variable keyword argument (:pep:`0362#parameter-object`), which
horetu presently does not support. Also, Python 2 doesn't have function
annotations, so you would really need to do this.

If you're on Python 2, or if you just want to use the other interface, you can
annotate a positional argument with :py:data:`horetu.Optional` to make it
optional; if that argument isn't passed in the command line we will use
``None`` as its value.

.. testcode::

    @horetu.annotate(horetu.Optional, str)
    def main(infile: horetu.Optional, *outfiles):
        pass

You can, of course, use the Python 3 annotation syntax as well.

.. testcode::

    def main(infile: horetu.Optional, *outfiles):
        pass

If you want something to be optional but of a different type, you can do this.

.. testcode::

    @horetu.annotate(int, horetu.Optional(int))
    def main(start, stop):
        pass

And if you want to set a default, pass it as the second argument to ``Optional``.

.. testcode::

    @horetu.annotate(int, horetu.Optional(int, 888))
    def main(start, stop):
        pass

Final note on settings
-----------------------
I prefer to think of horetu as a means of converting a Python function to a
shell interface rather than a means of creating a particular shell interface in
Python. Express your function cleanly and clearly in Python, and horetu will
make you a nice shell interface.
