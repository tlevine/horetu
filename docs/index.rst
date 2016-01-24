Introduction
==================================

.. py:module:: horetu

horetu turns a Python function into a command-line program with a command-line
argument parser and an optional configuration file parser. It accepts
configurations from the command line, falls back to the configuration file if
it exists, and then falls back to any defaults that are set in the Python
function.

.. toctree::
    :maxdepth: 3

    usage
    settings
    more
    developing

`Tom <https://thomaslevine.com>`_ occasionaly bangs arbitrarily on a
`Dvorak keyboard <https://en.wikipedia.org/wiki/Dvorak_Simplified_Keyboard>`_
in search of inspiration. One day, Horetus, the god of configuration option
parsing, spoke to Tom and told him to make a module that would automatically
assemble a command-line interface for specified Python functions.

After Tom implemented this command-line interface, Horetus spoke again to Tom,
this time through `q3k <https://q3k.org/>`_
in `Warsaw Hackerspace <https://hackerspace.pl/>`_.
Tom then extended horetu so it would
produce a configuration file parser as well.

This sort of unanticipated extension of existing software is why Tom is wary
of descriptive names for software.
