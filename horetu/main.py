import argparse
import sys
import os
from functools import partial

from . import options
from .sub import nest
from .one import one

def horetu(f, args = None,
           config = None,
           name = None, description = None, version = None,
           subcommand_dest = '_subcommand'):
    '''
    :type f: Callable or dict
    :param f: The callable to produce the argument parser too,
        or a dict of (dicts of...) str to callable to make subparsers.
    :param list args: Pass argv here for testing; use the actual argv by default.
    :param str name: Name of the program (``$0``)
    :param str description: Short description of what the program does
    :param str subcommand_dest: Attribute to save the base subcommand under
    '''
    if name == None and hasattr(f, '__call__'):
        name = f.__name__

    if config == None and name != None:
        config = os.path.expanduser('~/.' + name)

    if hasattr(f, '__call__'):
        if description == None:
            description = options.description(f)
        p = argparse.ArgumentParser(name, description = description,
            formatter_class = argparse.ArgumentDefaultsHelpFormatter)
        if version:
            p.add_argument('--version', action = 'version', version = version)
        main = one({}, p, f)
    else:
        p = argparse.ArgumentParser(name, description = description,
            formatter_class = argparse.ArgumentDefaultsHelpFormatter)
        if version:
            p.add_argument('--version', action = 'version', version = version)
        sp = p.add_subparsers(dest = subcommand_dest)
        if isinstance(f, dict):
            routes = {subcommand_dest: nest(sp, subcommands = f)}
        else:
            raise TypeError

        def _main(routes, args):
            while isinstance(routes, dict):
                for k in list(routes):
                    if hasattr(args, k):
                        if getattr(args, k) == None:
                            p.print_usage()
                            sys.exit(2)
                        g = routes[k][getattr(args, k)]
                        routes = routes[k]
                        break
                else:
                    break
            return g(args)
        main = partial(_main, routes)

    return main(p.parse_args(args))
