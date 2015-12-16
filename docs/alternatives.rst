I tried out plac and concluded that horetu is mostly better. Here are
some features that plac has and horetu doesn't.

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
