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
