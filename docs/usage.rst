Usage
===============
horetu figures out a good command-line interface based on standard Python
function annotations and properties.

Simple usage
^^^^^^^^^^^^^^
Consider the following Python program, called ``do_something.py``.

.. testcode::
    
    #!/usr/bin/env python
    from horetu import horetu
    def something(input_file, output_file, n_cores: int = 3):
        '''
        Do something to a file with several cores.
        '''
        # Pretend that something happens here.
    horetu(something)

Run it with the help flag; this is the result.

::

    $ do_something.py --help
    usage: something [-h] [--n-cores N_CORES] input_file output_file

    Do something to a file with several cores.

    positional arguments:
      input_file
      output_file

    optional arguments:
      -h, --help            show this help message and exit
      --n-cores N_CORES, -n N_CORES

Subcommands
^^^^^^^^^^^^^^^

Instead of calling :py:func:`horetu.horetu` on a callable, you can call it on a
dictionary of strings to callables. This turns each element into a
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
