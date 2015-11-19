import argparse
import sys

from . import options
from .sub import nest
from .one import one

def horetu(f, name = None, description = None):
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
        def main(argv = None):
            return one(p, f)(p.parse_args(argv))
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
        def main(argv = None):
            args = p.parse_args(argv)
            xs = argv if argv else []
            for k, v in routes.items():
                print(k, getattr(args, k, None), v)

    print(_args)
    return main(p.parse_args(_args))
