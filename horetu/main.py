import argparse
import sys
from functools import partial

from . import options
from .sub import nest
from .one import one

def horetu(f, name = None, description = None,
           subcommand_dest = 'subcommand', _args = None):
    '''
    :type f: Callable or dict
    :param f: The callable to produce the argument parser too,
        or a dict from str to callable to make subparsers.
    '''
    if hasattr(f, '__call__'):
        if name == None:
            name = f.__name__
        if description == None:
            description = options.description(f)
        p = argparse.ArgumentParser(name, description = description,
            formatter_class = argparse.ArgumentDefaultsHelpFormatter)
        main = one(p, f)
    else:
        p = argparse.ArgumentParser(name, description = description,
            formatter_class = argparse.ArgumentDefaultsHelpFormatter)
        sp = p.add_subparsers(dest = subcommand_dest)
        if isinstance(f, dict):
            routes = {subcommand_dest: nest(sp, subcommands = f)}
        else:
            raise TypeError

        def _main(routes, args):
            while isinstance(routes, dict):
                for k in list(routes):
                    if hasattr(args, k):
                        g = routes[k][getattr(args, k)]
                        routes = routes[k]
                        break
                else:
                    break
            return g(args)
        main = partial(_main, routes)

    return main(p.parse_args(_args))
