import argparse
import sys

from . import options

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
        return _horetu_one(p, f)(p.parse_args(_args))
    else:
        p = argparse.ArgumentParser(name, description = description,
            formatter_class = argparse.ArgumentDefaultsHelpFormatter)

        key = '_command'
        g = _horetu_many(key, p, f)
            
        def fallback(_):
            import sys
            p.print_usage()
            sys.exit(2)
        args = p.parse_args(_args)

        key = key + '.0'
        value = getattr(args, key, fallback)
        while True:
            print(key, value, g)
            if hasattr(value, '__call__'):
                return value(args)
            else:
                newkey = g[key][value]
                g = g[key]
                key = newkey
                value = getattr(args, key, fallback)
            print('----')
