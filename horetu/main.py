import argparse
import sys
import os
from functools import partial

from . import util
from . import options
from .sub import nest
from .one import one

EPILOG_TEMPLATE_ONE = '''
You can set configurations either as command-line flags, as documented
above, or as options in the file %(file)s
under the %(section)s section, like so.

  [%(section)s]
  foo = bar

Options names are the long form of the flags; "--foo" becomes "foo",
and "-f" becomes "f" only if "-f" has no long form.

If you want to use a different file as the configuration file, set the
environment variable %(env)s to that file's path.
'''

EPILOG_TEMPLATE_MANY = '''
You can set configurations either as command-line flags, as documented
above, or as options in the file %(file)s
under the following sections.

  [%(sections)s]

It might look like this, for example.

  [%(first-section)s]
  foo = bar

Options names are the long form of the flags; "--foo" becomes "foo",
and "-f" becomes "f" only if "-f" has no long form.

If you want to use a different file as the configuration file, set the
environment variable %(env)s to that file's path.
'''


def horetu(f, args=None,
           config=None,
           name=None, description=None, version=None,
           subcommand_dest='_subcommand'):
    '''
    :type f: Callable or dict
    :param f: The callable to produce the argument parser too,
        or a dict of (dicts of...) str to callable to make subparsers.
    :param list args: Pass argv here for testing; use the actual argv by default.
    :param str name: Name of the program (``$0``)
    :param str description: Short description of what the program does
    :param str subcommand_dest: Attribute to save the base subcommand under
    '''
    if name is None and hasattr(f, '__call__'):
        name = f.__name__
    env = '%s_CONFIG' % (name if name else sys.argv[0]).upper()

    if env in os.environ:
        config = os.environ[env]
    elif config is None and name is not None:
        config = os.path.expanduser('~/.%s.conf' % name)

    if hasattr(f, '__call__'):
        if description is None:
            description = options.description(f)
        p = argparse.ArgumentParser(name, description=description,
                                    formatter_class=argparse.RawDescriptionHelpFormatter)
        if version:
            p.add_argument('--version', action='version', version=version)
        main = one(config, name, p, f)
        if config:
            params = {'file': config, 'section': name, 'env': env}
            p.epilog = EPILOG_TEMPLATE_ONE % params

    else:
        p = argparse.ArgumentParser(name, description=description,
                                    formatter_class=argparse.RawDescriptionHelpFormatter)
        if version:
            p.add_argument('--version', action='version', version=version)
        sp = p.add_subparsers(dest=subcommand_dest)
        if isinstance(f, dict):
            subcommand_tree = nest(config, name, sp, subcommands=f)
        else:
            raise TypeError

        def _main(subcommand_tree, args):
            section_name = ''
            routes = {subcommand_dest: subcommand_tree}
            while isinstance(routes, dict):
                for k in list(routes):
                    if hasattr(args, k):
                        if getattr(args, k) is None:
                            p.print_usage()
                            sys.exit(2)
                        g = routes[k][getattr(args, k)]
                        routes = routes[k]
                        section_name = util.extend(section_name, k)
                        break
                else:
                    break
            return g(args)
        main = partial(_main, subcommand_tree)
        if config:
            sections = list(sorted(util.expand_dict_keys(subcommand_tree)))
            params = {'file': config, 'first-section': sections[0],
                      'sections': ']\n    ['.join(sections), 'env': env}
            p.epilog = EPILOG_TEMPLATE_MANY % params

    return main(p.parse_args(args))
