Usage
===============
horetu figures out a good command-line interface based on standard Python
function annotations and properties.

Install
^^^^^^^^^^^^
Install from PyPI. ::

    pip install horetu

This installs the :py:mod:`horetu` module. The most notable of its contents is
the :py:func:`horetu.horetu` function.

Simple usage
^^^^^^^^^^^^^^
Consider the following Python program, called ``do_something.py``.

.. testcode::
    
  #!/usr/bin/env python3
  from horetu import horetu

  def something(input_file, output_file, n_cores: int = 3):
      '''
      Do something to a file with several cores.
      '''
      # Pretend that something happens here.
  horetu(something)

Run it with the help flag; this is the result.

::

    $ ./do_something.py --help
    usage: something [-h] [--n-cores N_CORES] input_file output_file

    Do something to a file with several cores.

    positional arguments:
      input_file
      output_file

    optional arguments:
      -h, --help            show this help message and exit
      --n-cores N_CORES, -n N_CORES

    You can set configurations either as command-line flags, as documented
    above, or as options in the file /home/tlevine/.something.conf
    under the something section, like so.

      [something]
      foo = bar

    Options names are the long form of the flags; "--foo" becomes "foo",
    and "-f" becomes "f" only if "-f" has no long form.

    If you want to use a different file as the configuration file, set the
    environment variable SOMETHING_CONFIG to that file's path.

Subcommands
^^^^^^^^^^^^^^^
Instead of calling :py:func:`horetu.horetu` on a callable, you can call
it on a list of callables or a dictionary of strings to callables,
lists of callables, or dictionaries of the same.
arguments. A "valid argument" is a callable, list, or dictionary,
This turns each element into a
sub-command, and it uses the key, rather than the callable's name, as the
command name. For example, this Python code

::

    #!/usr/bin/env python

    # ...
    
    def main():
        commands = {
            'scrape': scrape,
            'serve': server.main,
            'set-password': set_password,
            'save-hucs': scraper.save_hucs,
        }
        description = 'Catalog and process public notices for Section 404 permit applications.'
        horetu(commands, name = 'scott', description = description)

produces this command-line interface.

::

    $ scott -h
    usage: scott [-h] {serve,set-password,scrape,save-hucs} ...

    Catalog and process public notices for Section 404 permit applications.

    positional arguments:
      {serve,set-password,scrape,save-hucs}

    optional arguments:
      -h, --help            show this help message and exit

    You can set configurations either as command-line flags, as documented
    above, or as options in the file /home/tlevine/.scott.conf
    under the following sections.

      [save-hucs]
      [serve]
      [set-password]
      [scrape]

    It might look like this, for example.

      [save-hucs]
      foo = bar

    Options names are the long form of the flags; "--foo" becomes "foo",
    and "-f" becomes "f" only if "-f" has no long form.

    If you want to use a different file as the configuration file, set the
    environment variable SCOTT_CONFIG to that file's path.

In the above example you can in fact use a :py:class:`list` instead of a
:py:class:`dict`; the names are taken from the function names.

::

    #!/usr/bin/env python

    # ...
    
    def main():
        commands = [
            scrape,
            server.main,
            set_password,
            scraper.save_hucs,
        ]
        description = 'Catalog and process public notices for Section 404 permit applications.'
        horetu(commands, name = 'scott', description = description)

You can have nested subcommands too.

::

    f = g = h = i = j = lambda x: int(x) + 4
    commands = {
        'subcommand1': {
            'subsubcommand1.1': f,
            'subsubcommand1.2': g,
        },
        'subcommand2': h,
        'subcommand3': {
            'subsubcommand3.1': i,
            'subsubcommand3.2': {
                'subsubsubcommand3.2.1': j,
            }
        },
    }
    horetu(commands)
