import argparse
import inspect
import sys

from . import options

def horetu(*fs, name = None, description = None, _args = None):
    '''
    :type fs: Callables or lists
    :param f: The callable to produce the argument parser too,
        or a dict from str to callable to make subparsers.
    '''
    if len(fs) == 1:
        f = fs[0]
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
        g = _horetu_many('', p, fs)
            
        def fallback(_):
            import sys
            p.print_usage()
            sys.exit(2)
        args = p.parse_args(_args)
        return g.get(args.command, fallback)(args)

def _horetu_many(dest_prefix, parser, fs):
    subparsers = parser.add_subparsers(dest = dest_prefix)
    if hasattr(fs, '__call__'):
        f = fs
        sp = subparsers.add_parser(f.__name__, description = options.description(f))
        return _horetu_one(sp, f)
    else:
        g = {}
        for f in fs:
            if dest_prefix:
                dest = dest_prefix + '_' + f.__name__
            else:
                dest = f.__name__
            sp = subparsers.add_parser(dest)
            g[dest] = _horetu_many(dest, sp, f)
        return g

def _horetu_one(parser, f):
    params = inspect.signature(f).parameters.values()
    helps = dict(options.docs(f))

    for param in params:
        if param.kind == param.VAR_KEYWORD:
            raise ValueError('Variable keyword args (**kwargs) are not allowed.')
        parser.add_argument(options.name_or_flags(param), nargs = options.nargs(param),
                            type = options.argtype(param), choices = options.argchoices(param),
                            help = helps.get(param.name, ''), default = options.default(param))

    positional_arguments = [param.name for param in params if param.kind != param.VAR_KEYWORD]
    keyword_arguments = [param.name for param in params if param.kind == param.VAR_KEYWORD]

    def g(parsed_args):
        args = [getattr(parsed_args, attr) for attr in positional_arguments]
        kwargs = {attr:getattr(parsed_args, attr) for attr in keyword_arguments}
        return f(*args, **kwargs)
    return g

