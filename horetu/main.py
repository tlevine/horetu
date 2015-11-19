import argparse
import sys
from functools import partial

from . import options
from .sub import nest
from .one import one

def horetu(f, name = None, description = None, _args = None):
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
        sp = p.add_subparsers()
        if isinstance(f, list):
            routes = nest(sp, commands = f)
        elif isinstance(f, dict):
            routes = nest(sp, subcommands = f)
        else:
            raise TypeError

        def _main(routes, args):
            print(routes)
            while len(routes) > 0:
                for k in list(routes):
                    if hasattr(args, k):
                        routes = routes[k]
                        print(k, args, routes)
                        break
                    elif hasattr(routes[k], '__call__'):
                        return routes[k](args)
                else:
                    break
        main = partial(_main, routes)

    print(_args)
    return main(p.parse_args(_args))
