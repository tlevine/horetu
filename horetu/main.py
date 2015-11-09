import argparse
import inspect
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
        while True:
            x = g.get(getattr(args, key, None), fallback)
            print([[[key, getattr(args, key, None), x, g]]])
            if hasattr(x, '__call__'):
                return x(args)
            else:
                g = g[x]

def _horetu_many(dest, parser, fs):
    subparsers = parser.add_subparsers(dest = dest)
    g = {}
    for i, (k, f) in enumerate(fs.items()):
        sp = subparsers.add_parser(k)
        if hasattr(f, '__call__'):
            g[f.__name__] = _horetu_one(sp, f)
            g[k] = f.__name__
        else:
            subdest = '%s.%d' % (dest, i)
            g[subdest] = _horetu_many(subdest, sp, f)
            g[k] = subdest
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

