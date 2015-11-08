import argparse
import inspect
import sys

from . import options

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
        return _horetu_one(p, f)(p.parse_args())
    else:
        p = argparse.ArgumentParser(name, description = description,
            formatter_class = argparse.ArgumentDefaultsHelpFormatter)
        g = _horetu_many(dest_prefix, parser, f)
            
        def fallback(_):
            import sys
            p.print_usage()
            sys.exit(2)
        args = p.parse_args()
        f = None
        while not hasattr(f, '__call__'):
            f = g.get(args.command, fallback)
        return f(args)

def _horetu_many(dest_prefix, parser, f):
    subparsers = parser.add_subparsers(dest = dest_prefix)
    g = {}
    for k, v in f.items():
        if hasattr(v, '__call__'):
            dest = dest_prefix + '_' + f.__name__
            sp = subparsers.add_parser(dest, description = options.description(f))
            g[k] = _horetu_many(dest, sp, f)
        else:
            dest = dest_prefix + '_' + k
            sp = subparsers.add_parser(dest)
            g[k] = _horetu_many(dest, sp, v)
    return g

def _horetu_one(parser, f):
    params = inspect.signature(f).parameters.values()
    helps = dict(options.docs(f))

    for param in params:
        if param.kind == param.VAR_KEYWORD:
            raise ValueError('Variable keyword args (**kwargs) are not allowed.')
        p.add_argument(options.name_or_flags(param), nargs = options.nargs(param),
                       type = options.argtype(param), choices = options.argchoices(param),
                       help = helps.get(param.name, ''), default = options.default(param))

    positional_arguments = [param.name for param in params if param.kind != param.VAR_KEYWORD]
    keyword_arguments = [param.name for param in params if param.kind == param.VAR_KEYWORD]

    def g(parsed_args):
        args = [getattr(parsed_args, attr) for attr in positional_arguments]
        kwargs = {attr:getattr(parsed_args, attr) for attr in keyword_arguments}
        return f(*args, **kwargs)
    return g

