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
2. If a function, rather than a list or dictionary, is passed as ``f``,
   use the function's name (``f.__name__``).
3. Otherwise, use the first argv (``sys.argv[0]``).

And these are the steps for determining the description.

1. Use the description keyword argument passed to horetu
   (``description``) if it is available.
2. If a function is passed as ``f`` and the function has a docstring,
   use the first line of the function's docstring.
3. Otherwise, don't include a description.

Parameter construction
----------------------------
Horetu breaks a Python function's arguments into four categories.
Arguments from these different categories turn into different sorts of
command-line arguments.

Argument categories
^^^^^^^^^^^^^^^^^^^^^^^
Here are the four argument categories.

1. Positional
2. Keyword 1
3. Variable positional
4. Keyword 2

I will describe these four different categories with example functions.

Let's start with a function that has only positional arguments. ::

    def example(a:int, b:int, c:int):
        return a + b - c

``a``, ``b``, and ``c`` are all positional arguments; they get turned
into required positional command-line arguments; you call it like this.

::

    example 3 8 2

Now let's add keyword arguments. We're starting with keyword 2
arguments; we'll do keyword 1 arguments later. ::

    def example(a:int, b:int, c:int, d:int=1):
        return (a + b - c) * d

The command-line interface from this can be called like so.

::

    example 3 8 2
    example -d 2 3 8 2
    example 3 8 2 -d 2

These

Parameter-specific settings are set all over the place, wherever you
would ordinarily set them.

Help
^^^^^^^^^^
Help is taken from parameter annotations in the docstring; in the following
function,

.. testcode::

    def main(n_cores: int=8):
        '''
        :param int n_cores: Number of cores to use for processing
        '''

"Number of cores to use for processing" is used as the help text for
the parameter ``n_cores``.

Fun fact: I wanted to use the docstring parser from Sphinx, but it turns out
to be just a very simple regular expression encapsulated under many
layers of abstraction. So I wrote my own.






Argument names
^^^^^^^^^^^^^^^^^^
Positional arguments keep the same names in the command-line interface,
except that underscores are replaced with hyphens.

Keyword arguments with single-character names are turned into one-hyphen flags,
and keyword arguments with longer names are turned into two-hyphen flags.
Also, underscores are replaced with hyphens.

.. testcode::

    def main(some_file, some_password=None, n=8):
        pass
    horetu.horetu(main, ['chainsaws.csv', '--some-password', 'abc', '-n' '2'])

horetu tries to turn long keyword arguments are also turned into
one-hyphen flags too, using the first letter as the flag.
It does this only when all keyword arguments have different first letters.

.. testcode::

    def main(some_file, some_password=None, n=8):
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

    def f(x, y, z='elephant'):
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

    def f(color: list=None):
        pass
    horetu.horetu(f, [])
    horetu.horetu(f, ['--color', 'pink', '--color', 'cyan'])

This interface takes as many colors as you want and interprets them as a
list. If you pass no colors, the value ``None`` is passed as ``colors``.

When keyword arguments are annotated with :py:class:`list` and are plural
English words, the resulting flags are named with the singular equivalent.
So we can switch the argument name from ``color`` to ``colors``.

.. testcode::

    def f(colors: list=None):
        pass
    horetu.horetu(f, ['--color', 'pink', '--color', 'cyan'])

Annoyingly, because of how horetu is implemented with :py:mod:`argparse`,
if the default argument is a list, it is extended, rather than replaced,
with the new arguments.

.. testcode::

    def f(colors: list=['pink']):
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

    def main(force=False):
        pass
    horetu.horetu(main, ['--force'])

Counting
^^^^^^^^^^^^^
Annotate a parameter with :py:data:`horetu.COUNT` to count the number of times
the argument appears. The number of flags is added to the default value.

.. testcode::

    def main(verbose: horetu.COUNT=1):
        pass
    horetu.horetu(main, []) # verbose = 1
    horetu.horetu(main, ['-v', '-v']) # verbose = 3

Optional arguments
^^^^^^^^^^^^^^^^^^^^^^
.. testcode::

    import sys
    def main(start=0, stop=1000, *, output=sys.stdout):
        pass

*Even more problematic, the implementation is buggy at the moment;
I'll probably change it so it actually works but is less amazing.*

``start`` and ``stop`` become positional arguments with the defaults
of 0 and 1000, respectively. In Python, ``*`` tells us that the following
keyword arguments must be addressed as keyword arguments, not as positional
arguments. ``output`` becomes the flag ``--output/-o``.

Final note on settings
-----------------------
I prefer to think of horetu as a means of converting a Python function to a
shell interface rather than a means of creating a particular shell interface in
Python. Express your function cleanly and clearly in Python, and horetu will
make you a nice shell interface. If you want your command-line interface
to look a particular way, don't use horetu.
